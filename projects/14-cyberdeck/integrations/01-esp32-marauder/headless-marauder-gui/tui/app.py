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

from marauder_core import MarauderController, MarauderParser, commands, flasher

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Tree, Input, Button, Select, Static, Label, DataTable

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

    def _free(self):
        if self.ctl.connected:
            self._log("[i] closing serial session so esptool can use the port")
            self.ctl.disconnect()

    def on_button_pressed(self, event: Button.Pressed):
        bid = event.button.id
        if bid == "close":
            self.dismiss(); return
        if bid == "detect":
            self._free(); self.run_worker(self._detect, thread=True); return
        if bid == "load":
            self.run_worker(self._load, thread=True); return
        if bid == "erase":
            self._free(); self.run_worker(self._erase, thread=True); return
        if bid in ("flash_app", "flash_full"):
            self._free()
            mode = "app" if bid == "flash_app" else "full"
            self.run_worker(lambda: self._flash(mode), thread=True)

    # workers (run in threads)
    def _detect(self):
        on = self._line()
        chip = flasher.detect_chip(self._port(), on)
        self.chip = chip
        self.app.call_from_thread(self.query_one("#chiplbl", Static).update, f"chip: {chip or 'unknown'}")
        self.app.call_from_thread(self._refill)

    def _load(self):
        on = self._line()
        on("[*] fetching latest release...")
        self.tag, self.assets = flasher.latest_release()
        on(f"[i] {self.tag}: {len(self.assets)} variants")
        self.app.call_from_thread(self._refill)

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

    def _resolve_chip(self, on):
        if self.chip:
            return self.chip
        on("[*] detecting chip...")
        self.chip = flasher.detect_chip(self._port(), on)
        return self.chip

    def _flash(self, mode):
        on = self._line()
        if not self._port():
            on("[error] enter a port"); return
        asset = self._by_name.get(self.query_one("#variant", Select).value)
        if not asset:
            on("[error] Load release + pick a variant first"); return
        chip = self._resolve_chip(on)
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
        rc = flasher.flash(self._port(), chip, app, on, mode=mode, baud=921600, support=support)
        on("[done] power-cycle the board" if rc == 0 else f"[x] esptool exit {rc}")

    def _erase(self):
        on = self._line()
        chip = self._resolve_chip(on) or "esp32"
        flasher.erase(self._port(), chip, on)

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
    Input { dock: bottom; border: round $accent; }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "stop", "Stop scan"),
        ("f", "flash", "Flash fw"),
        ("ctrl+l", "clear", "Clear log"),
        ("c", "focus_input", "Command box"),
    ]

    def __init__(self, controller: MarauderController):
        super().__init__()
        self.ctl = controller
        self.parser = MarauderParser()
        self._q: "queue.Queue[str]" = queue.Queue()
        self.ctl.subscribe(self._q.put)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            yield Tree("Marauder", id="tree")
            with Vertical(id="rightcol"):
                yield RichLog(id="log", highlight=False, markup=False, wrap=True)
                yield DataTable(id="aptable")
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
        table.add_columns("SSID", "BSSID", "Ch", "RSSI")
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
        except queue.Empty:
            pass

    def _refresh_aps(self):
        if not self.parser.dirty:
            return
        self.parser.dirty = False
        table = self.query_one("#aptable", DataTable)
        table.clear()
        for a in self.parser.ap_rows()[:200]:
            table.add_row(a.ssid, a.bssid, a.channel, a.rssi)
        table.border_title = f"Access Points ({len(self.parser.aps)})"

    def _log(self, line: str):
        self.query_one("#log", RichLog).write(line)

    # --- interactions ----------------------------------------------------- #
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
    args = ap.parse_args()

    ctl = MarauderController(port=args.port, baud=args.baud, mock=args.mock)
    MarauderTUI(ctl).run()


if __name__ == "__main__":
    main()
