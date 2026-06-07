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

from marauder_core import MarauderController, commands

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Tree, Input

try:                       # widget was renamed across Textual versions
    from textual.widgets import RichLog
except ImportError:        # older Textual
    from textual.widgets import TextLog as RichLog


class MarauderTUI(App):
    CSS = """
    Screen { layout: vertical; }
    #main { height: 1fr; }
    #tree { width: 42%; border: round $accent; }
    #log  { width: 1fr;  border: round $accent; }
    Input { dock: bottom; border: round $accent; }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "stop", "Stop scan"),
        ("ctrl+l", "clear", "Clear log"),
        ("c", "focus_input", "Command box"),
    ]

    def __init__(self, controller: MarauderController):
        super().__init__()
        self.ctl = controller
        self._q: "queue.Queue[str]" = queue.Queue()
        self.ctl.subscribe(self._q.put)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            yield Tree("Marauder", id="tree")
            yield RichLog(id="log", highlight=False, markup=False, wrap=True)
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

        self.set_interval(0.05, self._drain)

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
                self._log(self._q.get_nowait())
        except queue.Empty:
            pass

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

    def action_clear(self):
        self.query_one("#log", RichLog).clear()

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
