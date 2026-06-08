#!/usr/bin/env python3
"""
Headless Marauder TUI — a terminal application (Textual) for Kali Linux.

Runs entirely in the terminal: a command tree on the left, live serial output on
the right, a raw command box at the bottom. Great over SSH / on the deck console.

Run:   python3 tui/app.py            (auto-detects the port)
       python3 tui/app.py --port /dev/ttyUSB0
       python3 tui/app.py --mock     (no hardware, for trying the UI)
"""

import argparse
import os
import queue
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marauder_core import MarauderController, MarauderParser, CaptureLogger, commands, flasher

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Tree, Input, Button, Select, Static, Label, DataTable

try:
    from textual.widgets import Markdown
except ImportError:
    Markdown = None


def _guide_text():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "GUIDE.md")
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ("# Guide\n\nGUIDE.md not found.\n\n"
                "https://github.com/LxveAce/headless-marauder-gui/blob/main/GUIDE.md")


class GuideScreen(ModalScreen):
    CSS = "#guidebox { width: 92%; height: 92%; border: round $accent; background: $surface; padding: 1; }"
    BINDINGS = [("escape", "close", "Close"), ("g", "close", "Close")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="guidebox"):
            if Markdown is not None:
                yield Markdown(_guide_text())
            else:
                yield Static(_guide_text())
        yield Footer()

    def action_close(self):
        self.dismiss()

try:                       # widget was renamed across Textual versions
    from textual.widgets import RichLog
except ImportError:        # older Textual
    from textual.widgets import TextLog as RichLog


class FlashScreen(ModalScreen):
    """Modal firmware flasher: detect chip, fetch firmware, flash."""

    CSS = """
    #flash { width: 90%; height: 90%; border: round $accent; background: $surface; padding: 1; }
    #flog { height: 1fr; border: round $accent; }
    #flash Button { margin: 0 1; }
    """
    BINDINGS = [("escape", "close", "Close")]

    def __init__(self, controller: MarauderController):
        super().__init__()
        self.ctl = controller
        self.chip = None
        self.assets = []
        self.tag = ""
        self._by_name = {}

    def compose(self) -> ComposeResult:
        with Vertical(id="flash"):
            yield Label("Flash Marauder Firmware")
            yield Input(value=(self.ctl.port or ""), placeholder="port e.g. /dev/ttyUSB0", id="fport")
            with Horizontal():
                yield Button("Detect chip", id="detect")
                yield Button("Load release", id="load")
            yield Static("chip: ?", id="chiplbl")
            yield Select([], prompt="firmware variant", id="variant")
            with Horizontal():
                yield Button("Flash app", id="flash_app", variant="success")
                yield Button("Full flash", id="flash_full", variant="warning")
                yield Button("Erase", id="erase", variant="error")
                yield Button("Close", id="close")
            yield RichLog(id="flog", highlight=False, markup=False, wrap=True)

    def on_mount(self):
        if not flasher.esptool_available():
            self._log("[!] esptool not found — pip install esptool")

    # helpers
    def _log(self, s): self.query_one("#flog", RichLog).write(s)
    def _line(self): return lambda s: self.app.call_from_thread(self._log, s)
    def _port(self): return self.query_one("#fport", Input).value.strip()

    def _free(self, on=None):
        # called from worker threads — never touch widgets here; log via the on() callback
        if self.ctl.connected:
            if on:
                on("[i] closing serial session so esptool can use the port")
            self.ctl.disconnect()

    def on_button_pressed(self, event: Button.Pressed):
        bid = event.button.id
        port = self._port()                       # read widgets on the UI thread, pass to workers
        if bid == "close":
            self.dismiss(); return
        if bid == "detect":
            self.run_worker(lambda: self._detect(port), thread=True); return
        if bid == "load":
            self.run_worker(self._load, thread=True); return
        if bid == "erase":
            self.run_worker(lambda: self._erase(port), thread=True); return
        if bid in ("flash_app", "flash_full"):
            mode = "app" if bid == "flash_app" else "full"
            name = self.query_one("#variant", Select).value
            self.run_worker(lambda: self._flash(mode, port, name), thread=True)

    # workers (run in threads) — all widget access via call_from_thread, all bodies guarded
    def _set_chip_label(self):
        self.query_one("#chiplbl", Static).update(f"chip: {self.chip or 'unknown'}")

    def _detect(self, port):
        on = self._line()
        try:
            self._free(on)
            self.chip = flasher.detect_chip(port, on)
            self.app.call_from_thread(self._set_chip_label)
            self.app.call_from_thread(self._refill)
        except Exception as e:
            on(f"[error] {e}")

    def _load(self):
        on = self._line()
        try:
            on("[*] fetching latest release...")
            self.tag, self.assets = flasher.latest_release()
            on(f"[i] {self.tag}: {len(self.assets)} variants")
            self.app.call_from_thread(self._refill)
        except Exception as e:
            on(f"[error] {e}")

    def _refill(self):
        items = flasher.variants_for_chip(self.assets, self.chip) if self.chip else self.assets
        if not items:
            items = self.assets
        self._by_name = {a["name"]: a for a in items}
        opts = [(f"{a['label']} [{a['name']}]", a["name"]) for a in items]
        sel = self.query_one("#variant", Select)
        sel.set_options(opts)
        if self.chip and items:
            d = flasher.default_variant(items, self.chip)
            if d:
                sel.value = d["name"]

    def _resolve_chip(self, port, on):
        if self.chip:
            return self.chip
        on("[*] detecting chip...")
        self.chip = flasher.detect_chip(port, on)
        return self.chip

    def _flash(self, mode, port, name):
        on = self._line()
        try:
            self._free(on)
            if not port:
                on("[error] enter a port"); return
            asset = self._by_name.get(name)
            if not asset:
                on("[error] Load release + pick a variant first"); return
            chip = self._resolve_chip(port, on)
            if not chip:
                on("[error] chip unknown"); return
            if asset["chip"] != chip:
                on(f"[!] variant is for {asset['chip']} but chip is {chip}")
            cache = flasher.cache_dir()
            app = flasher.download_to(asset["url"], os.path.join(cache, asset["name"]), on)
            support = None
            if mode == "full":
                on("[*] fetching bootloader/partitions/boot_app0...")
                support = flasher.support_files(chip, cache, on)
            rc = flasher.flash(port, chip, app, on, mode=mode, baud=921600, support=support)
            on("[done] power-cycle the board" if rc == 0 else f"[x] esptool exit {rc}")
        except Exception as e:
            on(f"[error] {e}")

    def _erase(self, port):
        on = self._line()
        try:
            self._free(on)
            chip = self._resolve_chip(port, on) or "esp32"
            flasher.erase(port, chip, on)
        except Exception as e:
            on(f"[error] {e}")

    def action_close(self):
        self.dismiss()


class MarauderTUI(App):
    CSS = """
    Screen { layout: vertical; }
    #main { height: 1fr; }
    #tree { width: 42%; border: round $accent; }
    #rightcol { width: 1fr; }
    #log  { height: 1fr; border: round $accent; }
    #aptable { height: 45%; border: round $accent; }
    #desc { height: 1; color: $text-muted; padding: 0 1; }
    Input { dock: bottom; border: round $accent; }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "stop", "Stop scan"),
        ("f", "flash", "Flash fw"),
        ("g", "guide", "Guide"),
        ("ctrl+l", "clear", "Clear log"),
        ("c", "focus_input", "Command box"),
    ]

    def __init__(self, controller: MarauderController, logger=None):
        super().__init__()
        self.ctl = controller
        self.parser = MarauderParser()
        self.logger = logger or CaptureLogger()
        self._q: "queue.Queue[str]" = queue.Queue()
        self.ctl.subscribe(self._q.put)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            yield Tree("Marauder", id="tree")
            with Vertical(id="rightcol"):
                yield RichLog(id="log", highlight=False, markup=False, wrap=True)
                yield DataTable(id="aptable")
        yield Static("Select a command to see what it does · press g for the full Guide", id="desc")
        yield Input(placeholder="raw command (e.g. scanap) — Enter to send", id="raw")
        yield Footer()

    def on_mount(self):
        self.title = "Headless Marauder TUI"
        tree = self.query_one("#tree", Tree)
        tree.root.expand()
        for cat in commands.categories():
            node = tree.root.add(cat, expand=False)
            for c in [x for x in commands.COMMANDS if x.category == cat]:
                label = ("⚠ " if c.danger else "") + c.label
                node.add_leaf(label, data=c.id)

        table = self.query_one("#aptable", DataTable)
        table.add_columns("#", "SSID", "Ch", "RSSI", "BSSID")
        table.zebra_stripes = True

        self.set_interval(0.05, self._drain)
        self.set_interval(0.7, self._refresh_aps)

        try:
            port = self.ctl.connect()
            self.sub_title = f"connected: {port}"
            self._log(f"[connected to {port} @ {self.ctl.baud} baud]")
        except Exception as e:
            self.sub_title = "disconnected"
            self._log(f"[not connected] {e}")

    # --- serial output (drained on the UI thread) ------------------------- #
    def _drain(self):
        try:
            while True:
                line = self._q.get_nowait()
                self._log(line)
                self.parser.feed(line)
                self.logger.write_serial(line)
        except queue.Empty:
            pass

    def _refresh_aps(self):
        if not self.parser.dirty:
            return
        self.parser.dirty = False
        table = self.query_one("#aptable", DataTable)
        table.clear()
        rows = self.parser.ap_rows()
        for a in rows[:200]:
            idx = str(a.index) if a.index >= 0 else ""
            table.add_row(idx, a.ssid, a.channel, a.rssi, a.bssid)
        table.border_title = f"Access Points ({len(rows)})"
        if self.logger.enabled:
            self.logger.write_snapshot(rows, self.parser.station_rows(), {"port": self.ctl.port})

    def _log(self, line: str):
        self.query_one("#log", RichLog).write(line)

    # --- interactions ----------------------------------------------------- #
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted):
        cmd = commands.get(event.node.data) if event.node.data else None
        if cmd:
            tip = f"{cmd.desc}  ·  sends: {cmd.base}"
            if cmd.danger:
                tip += "  ·  ⚠ attack"
            self.query_one("#desc", Static).update(tip)
        else:
            self.query_one("#desc", Static).update("press g for the full Guide")

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        cmd_id = event.node.data
        if not cmd_id:
            return
        cmd = commands.get(cmd_id)
        if not cmd:
            return
        raw = self.query_one("#raw", Input)
        if cmd.params:
            # prefill a template the user can edit, then Enter to send
            tmpl = cmd.base + " " + " ".join(
                (p.flag + " " if p.flag else "") + f"<{p.name}>" for p in cmd.params
            )
            raw.value = tmpl.strip()
            raw.focus()
        else:
            self._send(cmd.base)

    def on_input_submitted(self, event: Input.Submitted):
        self._send(event.value.strip())
        event.input.value = ""

    def _send(self, line: str):
        if not line or "<" in line:
            if "<" in line:
                self._log("[fill in the <placeholders> before sending]")
            return
        if not self.ctl.connected:
            self._log("[error] not connected")
            return
        self.ctl.send(line)

    # --- actions ---------------------------------------------------------- #
    def action_stop(self):
        if self.ctl.connected:
            self.ctl.stop()

    def action_flash(self):
        self.push_screen(FlashScreen(self.ctl))

    def action_guide(self):
        self.push_screen(GuideScreen())

    def action_clear(self):
        self.query_one("#log", RichLog).clear()
        self.parser.clear()
        self.query_one("#aptable", DataTable).clear()

    def action_focus_input(self):
        self.query_one("#raw", Input).focus()

    def action_quit(self):
        try:
            self.ctl.disconnect()
        except Exception:
            pass
        self.exit()


def main():
    ap = argparse.ArgumentParser(description="Headless Marauder TUI (terminal app)")
    ap.add_argument("--port", help="Serial port (default: auto-detect)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--mock", action="store_true", help="Run without hardware")
    ap.add_argument("--log", nargs="?", const=True, default=None,
                    help="Log to a dir (default ~/marauder-logs)")
    args = ap.parse_args()

    ctl = MarauderController(port=args.port, baud=args.baud, mock=args.mock)
    logger = CaptureLogger(args.log if isinstance(args.log, str) else None)
    if args.log:
        logger.start()
    MarauderTUI(ctl, logger=logger).run()


if __name__ == "__main__":
    main()
