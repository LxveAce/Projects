"""Flash Firmware window for the desktop GUI — detect chip, fetch firmware, flash."""

import os
import queue
import threading

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from marauder_core import flasher

BG = "#0b0f0a"
PANEL = "#11160f"
FG = "#c8f7c5"
ACCENT = "#39ff14"
DANGER = "#ff4d4d"
MUTED = "#7a8f76"


class FlasherWindow(tk.Toplevel):
    def __init__(self, master, controller, default_port=""):
        super().__init__(master)
        self.ctl = controller
        self.title("Flash Marauder Firmware")
        self.configure(bg=PANEL)
        self.geometry("760x620")

        self.q: "queue.Queue[str]" = queue.Queue()
        self.chip = None
        self.assets = []
        self.tag = ""
        self._label_to_asset = {}
        self._busy = False
        self._need_refill = False   # set by worker threads; applied on the UI thread in _poll

        self._build()
        self._poll()
        if not flasher.esptool_available():
            self._log("[!] esptool not found. Install it:  pip install esptool")

        if default_port:
            self.port_var.set(default_port)

    # --- layout ----------------------------------------------------------- #
    def _build(self):
        pad = {"padx": 8, "pady": 4}

        row = tk.Frame(self, bg=PANEL); row.pack(fill="x", **pad)
        tk.Label(row, text="Port:", bg=PANEL, fg=FG).pack(side="left")
        self.port_var = tk.StringVar()
        ttk.Entry(row, textvariable=self.port_var, width=24).pack(side="left", padx=6)
        ttk.Button(row, text="Detect chip", command=self._detect).pack(side="left", padx=4)
        self.chip_lbl = tk.Label(row, text="chip: ?", bg=PANEL, fg=MUTED)
        self.chip_lbl.pack(side="left", padx=8)

        # mode
        mrow = tk.Frame(self, bg=PANEL); mrow.pack(fill="x", **pad)
        tk.Label(mrow, text="Mode:", bg=PANEL, fg=FG).pack(side="left")
        self.mode = tk.StringVar(value="app")
        ttk.Radiobutton(mrow, text="Update app only (existing board)", value="app",
                        variable=self.mode).pack(side="left", padx=6)
        ttk.Radiobutton(mrow, text="Full flash (blank board)", value="full",
                        variable=self.mode).pack(side="left", padx=6)

        # source
        srow = tk.Frame(self, bg=PANEL); srow.pack(fill="x", **pad)
        tk.Label(srow, text="Firmware:", bg=PANEL, fg=FG).pack(side="left")
        self.source = tk.StringVar(value="download")
        ttk.Radiobutton(srow, text="Download latest release", value="download",
                        variable=self.source).pack(side="left", padx=6)
        ttk.Radiobutton(srow, text="Local .bin", value="local",
                        variable=self.source).pack(side="left", padx=6)

        # download row
        drow = tk.Frame(self, bg=PANEL); drow.pack(fill="x", **pad)
        ttk.Button(drow, text="Load release list", command=self._load_release).pack(side="left")
        self.showall = tk.BooleanVar(value=False)
        ttk.Checkbutton(drow, text="show all chips", variable=self.showall,
                        command=self._refill_variants).pack(side="left", padx=6)
        self.variant_var = tk.StringVar()
        self.variant_combo = ttk.Combobox(drow, textvariable=self.variant_var, width=46, state="readonly")
        self.variant_combo.pack(side="left", padx=6)

        # local row
        lrow = tk.Frame(self, bg=PANEL); lrow.pack(fill="x", **pad)
        self.local_var = tk.StringVar()
        ttk.Entry(lrow, textvariable=self.local_var, width=52).pack(side="left", padx=(0, 6))
        ttk.Button(lrow, text="Browse .bin", command=self._browse).pack(side="left")

        # baud + actions
        arow = tk.Frame(self, bg=PANEL); arow.pack(fill="x", **pad)
        tk.Label(arow, text="Baud:", bg=PANEL, fg=FG).pack(side="left")
        self.baud = tk.StringVar(value="921600")
        ttk.Combobox(arow, textvariable=self.baud, width=10, state="readonly",
                     values=["115200", "460800", "921600"]).pack(side="left", padx=6)
        self.flash_btn = ttk.Button(arow, text="⚡ FLASH", command=self._flash)
        self.flash_btn.pack(side="left", padx=10)
        ttk.Button(arow, text="Erase flash", command=self._erase).pack(side="left")

        tk.Label(self, text="Tip: classic ESP32 Gold boards → pick a non-S3 variant "
                 "(e.g. 'Generic ESP32 / original v4'). S3 → MultiBoard S3.",
                 bg=PANEL, fg=MUTED, wraplength=720, justify="left").pack(fill="x", padx=8)

        self.console = tk.Text(self, bg="#05080a", fg=ACCENT, wrap="word",
                               state="disabled", font=("monospace", 9))
        self.console.pack(fill="both", expand=True, padx=8, pady=6)

    # --- helpers ---------------------------------------------------------- #
    def _log(self, s):
        self.q.put(s)

    def _poll(self):
        try:
            while True:
                line = self.q.get_nowait()
                self.console.config(state="normal")
                self.console.insert("end", line + "\n")
                self.console.see("end")
                self.console.config(state="disabled")
        except queue.Empty:
            pass
        # all widget updates happen here on the UI thread (workers only set state/flags)
        self.flash_btn.config(state="disabled" if self._busy else "normal")
        self.chip_lbl.config(text=f"chip: {self.chip or '?'}",
                             fg=ACCENT if self.chip else MUTED)
        if self._need_refill:
            self._need_refill = False
            self._refill_variants()
        self.after(40, self._poll)

    def _free_port(self):
        """esptool needs exclusive access — drop the live serial connection."""
        if self.ctl and self.ctl.connected:
            self._log("[i] disconnecting live serial session so esptool can use the port")
            self.ctl.disconnect()

    def _worker(self, fn):
        if self._busy:
            messagebox.showinfo("Busy", "A flash/erase is already running.")
            return
        self._busy = True
        self.flash_btn.config(state="disabled")

        def run():
            try:
                fn()
            except Exception as e:
                self._log(f"[error] {e}")
            finally:
                self._busy = False     # _poll re-enables the button on the UI thread

        threading.Thread(target=run, daemon=True).start()

    # --- actions ---------------------------------------------------------- #
    def _detect(self):
        port = self.port_var.get().strip()
        if not port:
            messagebox.showwarning("Port", "Enter the serial port first."); return
        self._free_port()

        def job():
            self._log("[*] detecting chip...")
            self.chip = flasher.detect_chip(port, self._log)
            self._need_refill = True
        self._worker(job)

    def _load_release(self):
        def job():
            self._log("[*] fetching latest release...")
            self.tag, self.assets = flasher.latest_release()
            self._log(f"[i] {self.tag}: {len(self.assets)} firmware variants")
            self._need_refill = True
        self._worker(job)

    def _refill_variants(self):
        if not self.assets:
            return
        items = self.assets if (self.showall.get() or not self.chip) \
            else flasher.variants_for_chip(self.assets, self.chip)
        self._label_to_asset = {f"{a['label']}  [{a['name']}]": a for a in items}
        labels = list(self._label_to_asset)
        self.variant_combo["values"] = labels
        if labels:
            default = flasher.default_variant(items, self.chip) if self.chip else None
            pick = next((l for l, a in self._label_to_asset.items() if default and a["name"] == default["name"]), labels[0])
            self.variant_var.set(pick)

    def _browse(self):
        path = filedialog.askopenfilename(title="Select firmware .bin",
                                          filetypes=[("Firmware", "*.bin"), ("All", "*.*")])
        if path:
            self.local_var.set(path)
            self.source.set("local")

    def _resolve_chip(self, port):
        if self.chip:
            return self.chip
        self._log("[*] chip unknown — detecting first...")
        self.chip = flasher.detect_chip(port, self._log)
        return self.chip

    def _flash(self):
        port = self.port_var.get().strip()
        if not port:
            messagebox.showwarning("Port", "Enter the serial port first."); return
        mode = self.mode.get()
        source = self.source.get()
        baud = int(self.baud.get())

        if source == "download" and not self._label_to_asset:
            messagebox.showinfo("Firmware", "Click 'Load release list' and pick a variant."); return
        if source == "local" and not self.local_var.get().strip():
            messagebox.showinfo("Firmware", "Browse to a local .bin first."); return

        if not messagebox.askyesno("Confirm flash",
                                   f"Flash {mode} via {port} @ {baud}?\nDo not unplug during flashing."):
            return
        # capture all widget values on the UI thread BEFORE starting the worker
        asset = self._label_to_asset.get(self.variant_var.get()) if source == "download" else None
        local = self.local_var.get().strip()
        self._free_port()

        def job():
            chip = self._resolve_chip(port)
            if not chip:
                self._log("[error] could not detect chip; aborting"); return
            cache = flasher.cache_dir()

            if source == "download":
                if not asset:
                    self._log("[error] no variant selected"); return
                if asset["chip"] != chip:
                    self._log(f"[!] WARNING: variant is for {asset['chip']} but chip is {chip}")
                app = flasher.download_to(asset["url"], os.path.join(cache, asset["name"]), self._log)
            else:
                app = local

            support = None
            if mode == "full":
                self._log("[*] fetching bootloader/partitions/boot_app0...")
                support = flasher.support_files(chip, cache, self._log)

            self._log(f"[*] flashing ({mode}) {os.path.basename(app)} to {chip}...")
            rc = flasher.flash(port, chip, app, self._log, mode=mode, baud=baud, support=support)
            self._log("[✓] done — power-cycle the board" if rc == 0 else f"[x] esptool exit {rc}")
        self._worker(job)

    def _erase(self):
        port = self.port_var.get().strip()
        if not port:
            messagebox.showwarning("Port", "Enter the serial port first."); return
        if not messagebox.askyesno("Erase", "Erase the entire flash? This wipes the firmware."):
            return
        self._free_port()

        def job():
            chip = self._resolve_chip(port) or "esp32"
            flasher.erase(port, chip, self._log)
        self._worker(job)
