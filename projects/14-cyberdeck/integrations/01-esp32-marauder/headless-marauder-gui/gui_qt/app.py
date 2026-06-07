#!/usr/bin/env python3
"""
Headless Marauder — PyQt5 desktop GUI.

The polished native app: command sidebar, live colorized console, live Access-Point and
Station tables (parsed from the serial stream), a built-in firmware flasher, connect/STOP.

Run:   python3 gui_qt/app.py            (auto-detects the port)
       python3 gui_qt/app.py --port /dev/ttyUSB0
       python3 gui_qt/app.py --mock     (no hardware, for trying the UI)

Needs PyQt5:   sudo apt install -y python3-pyqt5     (or: pip install PyQt5)
"""

import argparse
import os
import queue
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QPlainTextEdit, QTabWidget,
    QTableWidget, QTableWidgetItem, QGroupBox, QScrollArea, QSplitter, QDialog,
    QFormLayout, QCheckBox, QRadioButton, QFileDialog, QMessageBox, QAbstractItemView,
    QHeaderView, QButtonGroup,
)

from marauder_core import MarauderController, MarauderParser, commands, flasher

DARK_QSS = """
QWidget { background: #0b0f0a; color: #c8f7c5; font-size: 12px; }
QGroupBox { border: 1px solid #1d2b18; border-radius: 6px; margin-top: 10px; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; color: #39ff14; }
QPushButton { background: #14210f; border: 1px solid #2a3d22; border-radius: 5px; padding: 5px; }
QPushButton:hover { background: #1c3016; border-color: #39ff14; }
QPushButton#danger { color: #ff6b6b; border-color: #5a2222; }
QPushButton#stop { background: #ff4d4d; color: #ffffff; font-weight: bold; }
QPlainTextEdit, QTableWidget { background: #05080a; color: #39ff14; border: 1px solid #1d2b18; }
QLineEdit, QComboBox { background: #11160f; border: 1px solid #2a3d22; border-radius: 4px; padding: 3px; }
QHeaderView::section { background: #14210f; color: #39ff14; border: 0; padding: 4px; }
QTabBar::tab { background: #11160f; padding: 6px 12px; }
QTabBar::tab:selected { background: #1c3016; color: #39ff14; }
QLabel#status_ok { color: #39ff14; }
QLabel#status_bad { color: #ff4d4d; }
"""


# --------------------------------------------------------------------------- #
class ParamDialog(QDialog):
    def __init__(self, parent, cmd):
        super().__init__(parent)
        self.setWindowTitle(cmd.label)
        self.cmd = cmd
        self.widgets = {}
        lay = QVBoxLayout(self)
        if cmd.desc:
            lay.addWidget(QLabel(cmd.desc))
        form = QFormLayout()
        for p in cmd.params:
            if p.kind == "bool":
                w = QCheckBox()
            elif p.kind == "select":
                w = QComboBox(); w.addItems(p.choices)
            else:
                w = QLineEdit(); w.setPlaceholderText(p.placeholder or p.help)
            self.widgets[p.name] = w
            form.addRow(p.name + (" *" if p.required else ""), w)
        lay.addLayout(form)
        row = QHBoxLayout()
        ok = QPushButton("RUN ⚠" if cmd.danger else "Run"); ok.clicked.connect(self._ok)
        cancel = QPushButton("Cancel"); cancel.clicked.connect(self.reject)
        row.addWidget(ok); row.addWidget(cancel); lay.addLayout(row)
        self.values = None

    def _ok(self):
        vals = {}
        for p in self.cmd.params:
            w = self.widgets[p.name]
            if isinstance(w, QCheckBox):
                vals[p.name] = w.isChecked()
            elif isinstance(w, QComboBox):
                vals[p.name] = w.currentText()
            else:
                vals[p.name] = w.text()
            if p.required and not isinstance(w, QCheckBox) and not str(vals[p.name]).strip():
                QMessageBox.warning(self, "Missing", f"'{p.name}' is required.")
                return
        self.values = vals
        self.accept()


# --------------------------------------------------------------------------- #
class FlasherDialog(QDialog):
    def __init__(self, parent, controller, default_port=""):
        super().__init__(parent)
        self.ctl = controller
        self.setWindowTitle("Flash Marauder Firmware")
        self.resize(780, 600)
        self.q = queue.Queue()
        self.chip = None
        self.assets = []
        self.by_name = {}
        self._busy = False
        self._need_refill = False   # set by worker threads; applied on the GUI thread in _drain

        lay = QVBoxLayout(self)

        prow = QHBoxLayout()
        prow.addWidget(QLabel("Port:"))
        self.port = QLineEdit(default_port); prow.addWidget(self.port)
        b = QPushButton("Detect chip"); b.clicked.connect(self._detect); prow.addWidget(b)
        self.chip_lbl = QLabel("chip: ?"); prow.addWidget(self.chip_lbl)
        lay.addLayout(prow)

        mrow = QHBoxLayout()
        mrow.addWidget(QLabel("Mode:"))
        self.mode_app = QRadioButton("Update app only"); self.mode_app.setChecked(True)
        self.mode_full = QRadioButton("Full flash (blank board)")
        g = QButtonGroup(self); g.addButton(self.mode_app); g.addButton(self.mode_full)
        mrow.addWidget(self.mode_app); mrow.addWidget(self.mode_full); mrow.addStretch()
        lay.addLayout(mrow)

        srow = QHBoxLayout()
        srow.addWidget(QLabel("Firmware:"))
        self.src_dl = QRadioButton("Download latest"); self.src_dl.setChecked(True)
        self.src_local = QRadioButton("Local .bin")
        sg = QButtonGroup(self); sg.addButton(self.src_dl); sg.addButton(self.src_local)
        srow.addWidget(self.src_dl); srow.addWidget(self.src_local); srow.addStretch()
        lay.addLayout(srow)

        drow = QHBoxLayout()
        lb = QPushButton("Load release list"); lb.clicked.connect(self._load); drow.addWidget(lb)
        self.showall = QCheckBox("show all chips"); self.showall.stateChanged.connect(self._refill)
        drow.addWidget(self.showall)
        self.variant = QComboBox(); self.variant.setMinimumWidth(380); drow.addWidget(self.variant)
        lay.addLayout(drow)

        lrow = QHBoxLayout()
        self.local = QLineEdit(); lrow.addWidget(self.local)
        bb = QPushButton("Browse"); bb.clicked.connect(self._browse); lrow.addWidget(bb)
        lay.addLayout(lrow)

        arow = QHBoxLayout()
        arow.addWidget(QLabel("Baud:"))
        self.baud = QComboBox(); self.baud.addItems(["115200", "460800", "921600"]); self.baud.setCurrentText("921600")
        arow.addWidget(self.baud)
        self.flash_btn = QPushButton("⚡ FLASH"); self.flash_btn.clicked.connect(self._flash); arow.addWidget(self.flash_btn)
        eb = QPushButton("Erase flash"); eb.clicked.connect(self._erase); arow.addWidget(eb)
        arow.addStretch()
        lay.addLayout(arow)

        self.console = QPlainTextEdit(); self.console.setReadOnly(True); lay.addWidget(self.console)

        self.timer = QTimer(self); self.timer.timeout.connect(self._drain); self.timer.start(40)
        if not flasher.esptool_available():
            self._log("[!] esptool not found — pip install esptool")

    def _log(self, s): self.q.put(s)

    def _drain(self):
        try:
            while True:
                self.console.appendPlainText(self.q.get_nowait())
        except queue.Empty:
            pass
        # all widget updates happen here on the GUI thread (workers only set state/flags)
        self.flash_btn.setEnabled(not self._busy)
        self.chip_lbl.setText(f"chip: {self.chip or '?'}")
        if self._need_refill:
            self._need_refill = False
            self._refill()

    def _free(self):
        if self.ctl and self.ctl.connected:
            self._log("[i] closing serial session for esptool")
            self.ctl.disconnect()

    def _work(self, fn):
        if self._busy:
            return
        self._busy = True       # _drain disables/enables the button on the GUI thread

        def run():
            try:
                fn()
            except Exception as e:
                self._log(f"[error] {e}")
            finally:
                self._busy = False
        threading.Thread(target=run, daemon=True).start()

    def _detect(self):
        port = self.port.text().strip()
        if not port:
            return
        self._free()

        def job():
            self.chip = flasher.detect_chip(port, self._log)
            self._need_refill = True
        self._work(job)

    def _load(self):
        def job():
            self._log("[*] fetching latest release...")
            tag, self.assets = flasher.latest_release()
            self._log(f"[i] {tag}: {len(self.assets)} variants")
            self._need_refill = True
        self._work(job)

    def _refill(self):
        if not self.assets:
            return
        items = self.assets if (self.showall.isChecked() or not self.chip) \
            else flasher.variants_for_chip(self.assets, self.chip)
        self.by_name = {f"{a['label']}  [{a['name']}]": a for a in items}
        self.variant.clear(); self.variant.addItems(list(self.by_name))
        d = flasher.default_variant(items, self.chip) if self.chip else None
        if d:
            for i, (lbl, a) in enumerate(self.by_name.items()):
                if a["name"] == d["name"]:
                    self.variant.setCurrentIndex(i); break

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select .bin", "", "Firmware (*.bin);;All (*)")
        if path:
            self.local.setText(path); self.src_local.setChecked(True)

    def _resolve_chip(self, port):
        if self.chip:
            return self.chip
        self._log("[*] detecting chip...")
        self.chip = flasher.detect_chip(port, self._log)
        return self.chip

    def _flash(self):
        port = self.port.text().strip()
        if not port:
            return
        mode = "app" if self.mode_app.isChecked() else "full"
        if self.src_dl.isChecked() and not self.by_name:
            QMessageBox.information(self, "Firmware", "Load release list + pick a variant."); return
        if self.src_local.isChecked() and not self.local.text().strip():
            QMessageBox.information(self, "Firmware", "Browse to a local .bin."); return
        if QMessageBox.question(self, "Confirm", f"Flash {mode} via {port}?\nDon't unplug.") != QMessageBox.Yes:
            return
        # capture all widget values on the GUI thread BEFORE starting the worker
        baud = int(self.baud.currentText())
        use_download = self.src_dl.isChecked()
        asset = self.by_name.get(self.variant.currentText()) if use_download else None
        local = self.local.text().strip()
        self._free()

        def job():
            chip = self._resolve_chip(port)
            if not chip:
                self._log("[error] chip unknown"); return
            cache = flasher.cache_dir()
            if use_download:
                if not asset:
                    self._log("[error] no variant selected"); return
                if asset["chip"] != chip:
                    self._log(f"[!] variant is {asset['chip']} but chip is {chip}")
                app = flasher.download_to(asset["url"], os.path.join(cache, asset["name"]), self._log)
            else:
                app = local
            support = flasher.support_files(chip, cache, self._log) if mode == "full" else None
            rc = flasher.flash(port, chip, app, self._log, mode=mode, baud=baud, support=support)
            self._log("[done] power-cycle the board" if rc == 0 else f"[x] exit {rc}")
        self._work(job)

    def _erase(self):
        port = self.port.text().strip()
        if not port:
            return
        if QMessageBox.question(self, "Erase", "Erase entire flash?") != QMessageBox.Yes:
            return
        self._free()
        self._work(lambda: flasher.erase(port, self._resolve_chip(port) or "esp32", self._log))


# --------------------------------------------------------------------------- #
class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.ctl = controller
        self.parser = MarauderParser()
        self.q = queue.Queue()
        self.ctl.subscribe(self.q.put)

        self.setWindowTitle("Headless Marauder — Qt")
        self.resize(1180, 760)
        self.setStyleSheet(DARK_QSS)
        self._build()

        self.t_drain = QTimer(self); self.t_drain.timeout.connect(self._drain); self.t_drain.start(40)
        self.t_tables = QTimer(self); self.t_tables.timeout.connect(self._refresh_tables); self.t_tables.start(700)

    # --- ui --------------------------------------------------------------- #
    def _build(self):
        central = QWidget(); self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # top bar
        bar = QHBoxLayout()
        bar.addWidget(QLabel("Port:"))
        self.port = QComboBox(); self.port.setEditable(True); self.port.setMinimumWidth(220)
        self._refresh_ports(); bar.addWidget(self.port)
        rb = QPushButton("↻"); rb.setFixedWidth(32); rb.clicked.connect(self._refresh_ports); bar.addWidget(rb)
        self.connect_btn = QPushButton("Connect"); self.connect_btn.clicked.connect(self._toggle); bar.addWidget(self.connect_btn)
        self.status = QLabel("disconnected"); self.status.setObjectName("status_bad"); bar.addWidget(self.status)
        bar.addStretch()
        fb = QPushButton("⚡ Flash Firmware"); fb.clicked.connect(self._flasher); bar.addWidget(fb)
        sb = QPushButton("STOP"); sb.setObjectName("stop"); sb.clicked.connect(self._stop); bar.addWidget(sb)
        root.addLayout(bar)

        # body splitter
        split = QSplitter(Qt.Horizontal); root.addWidget(split, 1)
        split.addWidget(self._command_panel())

        right = QWidget(); rl = QVBoxLayout(right)
        self.tabs = QTabWidget()
        self.console = QPlainTextEdit(); self.console.setReadOnly(True)
        self.console.setFont(QFont("monospace", 10))
        self.tabs.addTab(self.console, "Console")
        self.ap_table = self._make_table(["SSID", "BSSID", "Ch", "RSSI"])
        self.tabs.addTab(self.ap_table, "Access Points")
        self.sta_table = self._make_table(["Station MAC", "AP BSSID", "RSSI"])
        self.tabs.addTab(self.sta_table, "Stations")
        rl.addWidget(self.tabs, 1)

        raw = QHBoxLayout()
        self.raw = QLineEdit(); self.raw.setPlaceholderText("raw command (e.g. scanap) — Enter to send")
        self.raw.returnPressed.connect(self._send_raw); raw.addWidget(self.raw)
        snd = QPushButton("Send"); snd.clicked.connect(self._send_raw); raw.addWidget(snd)
        clr = QPushButton("Clear"); clr.clicked.connect(lambda: (self.console.clear(), self.parser.clear())); raw.addWidget(clr)
        rl.addLayout(raw)
        split.addWidget(right)
        split.setSizes([430, 750])

    def _command_panel(self):
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setMinimumWidth(420)
        inner = QWidget(); v = QVBoxLayout(inner)
        for cat in commands.categories():
            box = QGroupBox(cat); grid = QGridLayout(box)
            cmds = [c for c in commands.COMMANDS if c.category == cat]
            for i, c in enumerate(cmds):
                btn = QPushButton(c.label)
                if c.danger:
                    btn.setObjectName("danger")
                btn.clicked.connect(lambda _, cmd=c: self._run(cmd))
                grid.addWidget(btn, i // 2, i % 2)
            v.addWidget(box)
        v.addStretch()
        scroll.setWidget(inner)
        return scroll

    def _make_table(self, headers):
        t = QTableWidget(0, len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.verticalHeader().setVisible(False)
        return t

    # --- actions ---------------------------------------------------------- #
    def _run(self, cmd):
        if cmd.danger and QMessageBox.question(
                self, "Confirm", f"Run attack/spam?\n\n{cmd.base}\n\nAuthorized targets only.") != QMessageBox.Yes:
            return
        if cmd.params:
            dlg = ParamDialog(self, cmd)
            if dlg.exec_() != QDialog.Accepted or dlg.values is None:
                return
            line = commands.build(cmd, dlg.values)
        else:
            line = cmd.base
        self._guarded_send(line)

    def _send_raw(self):
        line = self.raw.text().strip()
        if line:
            self._guarded_send(line); self.raw.clear()

    def _guarded_send(self, line):
        if not self.ctl.connected:
            self._append("[error] not connected"); return
        try:
            self.ctl.send(line)
        except Exception as e:
            self._append(f"[error] {e}")

    def _stop(self):
        if self.ctl.connected:
            self.ctl.stop()

    def _flasher(self):
        FlasherDialog(self, self.ctl, default_port=self.port.currentText().strip()).exec_()

    # --- connection ------------------------------------------------------- #
    def _refresh_ports(self):
        cur = self.port.currentText() if hasattr(self, "port") else ""
        self.port.clear()
        self.port.addItems([d for d, _ in MarauderController.list_ports()])
        if cur:
            self.port.setCurrentText(cur)

    def _toggle(self):
        if self.ctl.connected:
            self.ctl.disconnect()
            self.status.setText("disconnected"); self.status.setObjectName("status_bad")
            self.status.setStyleSheet("color:#ff4d4d;")
            self.connect_btn.setText("Connect"); return
        self.ctl.port = self.port.currentText().strip() or None
        try:
            port = self.ctl.connect()
            self.status.setText(f"connected: {port}"); self.status.setStyleSheet("color:#39ff14;")
            self.connect_btn.setText("Disconnect")
            self._append(f"[connected to {port} @ {self.ctl.baud} baud]")
        except Exception as e:
            QMessageBox.critical(self, "Connection failed", str(e))
            self._append(f"[error] {e}")

    # --- streaming -------------------------------------------------------- #
    def _drain(self):
        try:
            while True:
                line = self.q.get_nowait()
                self._append(line)
                self.parser.feed(line)
        except queue.Empty:
            pass

    def _append(self, line):
        self.console.appendPlainText(line)

    def _refresh_tables(self):
        if not self.parser.dirty:
            return
        self.parser.dirty = False
        aps = self.parser.ap_rows()
        self.ap_table.setRowCount(len(aps))
        for r, a in enumerate(aps):
            for c, val in enumerate([a.ssid, a.bssid, a.channel, a.rssi]):
                self.ap_table.setItem(r, c, QTableWidgetItem(str(val)))
        self.tabs.setTabText(1, f"Access Points ({len(aps)})")
        stas = self.parser.station_rows()
        self.sta_table.setRowCount(len(stas))
        for r, s in enumerate(stas):
            for c, val in enumerate([s.mac, s.ap_bssid, s.rssi]):
                self.sta_table.setItem(r, c, QTableWidgetItem(str(val)))
        self.tabs.setTabText(2, f"Stations ({len(stas)})")

    def closeEvent(self, ev):
        try:
            self.ctl.disconnect()
        except Exception:
            pass
        ev.accept()


def main():
    ap = argparse.ArgumentParser(description="Headless Marauder Qt GUI")
    ap.add_argument("--port"); ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--no-autoconnect", action="store_true")
    args = ap.parse_args()

    ctl = MarauderController(port=args.port, baud=args.baud, mock=args.mock)
    app = QApplication(sys.argv)
    win = MainWindow(ctl)
    win.show()
    if not args.no_autoconnect:
        try:
            port = ctl.connect()
            win.status.setText(f"connected: {port}"); win.status.setStyleSheet("color:#39ff14;")
            win.connect_btn.setText("Disconnect")
            win.port.setCurrentText(port)
            win._append(f"[connected to {port} @ {ctl.baud} baud]")
        except Exception as e:
            win._append(f"[not connected] {e}")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
