"""
Flasher — flash ESP32 Marauder firmware from inside the app.

Wraps `esptool` (subprocess, streamed) and pulls firmware straight from the official
GitHub release + the repo's FlashFiles/ tree, so you can flash a brand-new board or
update an existing one without leaving the GUI/TUI.

Key facts baked in (verified against the v1.12.1 release):
  * Releases ship ONLY app .bins (board-specific). There is no generic "esp32" build —
    classic ESP32 dev boards use `_old_hardware` / `_lddb` / etc., S3 uses `_multiboardS3`.
  * bootloader / partitions / boot_app0 are NOT in the release — they live in FlashFiles/:
        MarauderV4/                 classic-ESP32 bootloader+partitions
        FlipperZeroMultiBoardS3/    S3 bootloader+partitions + the shared boot_app0.bin
        FlipperZeroDevBoard/        S2 bootloader+partitions
  * Flash offsets: partitions 0x8000, boot_app0 0xE000, app 0x10000 always.
    bootloader 0x1000 on classic ESP32 / S2, but 0x0 on S3 / C-series.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from typing import Callable, Dict, List, Optional, Tuple

LATEST_API = "https://api.github.com/repos/justcallmekoko/ESP32Marauder/releases/latest"
RAW_BRANCHES = ("master", "main")
RAW_TMPL = "https://raw.githubusercontent.com/justcallmekoko/ESP32Marauder/{branch}/FlashFiles/{path}"
_UA = {"User-Agent": "headless-marauder-gui"}

Line = Callable[[str], None]

# bootloader sits at 0x0 on S3 and the RISC-V parts, 0x1000 on classic ESP32 / S2
_BOOTLOADER_0 = {"esp32s3", "esp32c2", "esp32c3", "esp32c6", "esp32c5", "esp32h2"}

# FlashFiles dir that holds bootloader+partitions for each chip family
_SUPPORT_DIR = {
    "esp32": "MarauderV4",
    "esp32s2": "FlipperZeroDevBoard",
    "esp32s3": "FlipperZeroMultiBoardS3",
}
_BOOT_APP0_PATH = "FlipperZeroMultiBoardS3/boot_app0.bin"
_BOOTLOADER_NAME = "esp32_marauder.ino.bootloader.bin"
_PARTITIONS_NAME = "esp32_marauder.ino.partitions.bin"

# Friendly labels for the release app variants (suffix -> description)
_VARIANT_LABELS = {
    "old_hardware": "Generic ESP32 / original v4 hardware (ILI9341)",
    "lddb": "Generic ESP32 dev board, no display (LDDB/NodeMCU/Wemos)",
    "v6": "Official Marauder v6", "v6_1": "Official Marauder v6.1",
    "v7": "Official Marauder v7", "v8": "Official Marauder v8",
    "kit": "Marauder Kit (Huzzah32)", "mini": "Marauder Mini",
    "mini_v3": "Marauder Mini v3 (ESP32-C5)",
    "marauder_dev_board_pro": "Dev Board Pro / BFFB (serial)",
    "multiboardS3": "Flipper MultiBoard / ESP32-S3",
    "flipper": "Flipper Zero WiFi Dev Board (ESP32-S2)",
    "rev_feather": "Rev Feather (ESP32-S2)",
    "m5cardputer": "M5Cardputer (ESP32-S3)", "m5cardputer_adv": "M5Cardputer Adv (ESP32-S3)",
    "m5stickc_plus": "M5StickC Plus", "m5stickc_plus2": "M5StickC Plus 2",
    "cyd_2432S028": "CYD 2.8\"", "cyd_2432S028_2usb": "CYD 2.8\" (2-USB)",
    "cyd_2432S024_guition": "CYD 2.4\" Guition", "cyd_3_5_inch": "CYD 3.5\"",
    "esp32c5devkitc1": "ESP32-C5 DevKitC-1",
}


def _chip_of_variant(name: str) -> str:
    n = name.lower()
    if "multiboards3" in n or "m5cardputer" in n:
        return "esp32s3"
    if "_flipper" in n or "rev_feather" in n:
        return "esp32s2"
    if "mini_v3" in n or "esp32c5devkitc1" in n:
        return "esp32c5"
    return "esp32"  # everything else (old_hardware, v6/7/8, kit, mini, lddb, cyd_*, m5stick...)


def _variant_label(name: str) -> str:
    # Match the most specific (longest) suffix so e.g. "esp32c5devkitc1" doesn't match "kit",
    # and "mini_v3" doesn't match "mini".
    best = ""
    for suffix in _VARIANT_LABELS:
        if suffix in name and len(suffix) > len(best):
            best = suffix
    return _VARIANT_LABELS[best] if best else name


# --------------------------------------------------------------------------- #
# esptool plumbing
# --------------------------------------------------------------------------- #

def esptool_argv(*args: str) -> List[str]:
    return [sys.executable, "-m", "esptool", *args]


def esptool_available() -> bool:
    try:
        return subprocess.run(esptool_argv("version"), capture_output=True, timeout=20).returncode == 0
    except Exception:
        return False


def _run_stream(argv: List[str], on_line: Line) -> int:
    """Run a command, stream combined stdout/stderr line-by-line, return exit code.

    On any exception mid-stream (e.g. the UI callback raises because a dialog closed), the
    child is killed and reaped so it can't keep holding the serial port — otherwise the next
    flash fails with 'port busy'.
    """
    on_line("$ " + " ".join(argv))
    try:
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, text=True, bufsize=1)
    except FileNotFoundError as e:
        on_line(f"[error] {e}")
        return 127
    try:
        for line in proc.stdout:                   # type: ignore[union-attr]
            on_line(line.rstrip("\n"))
        proc.wait()
    except Exception as e:
        on_line(f"[error] {e}")
        try:
            proc.kill()
            proc.wait(timeout=5)
        except Exception:
            pass
        return -1
    finally:
        try:
            if proc.stdout:
                proc.stdout.close()
        except Exception:
            pass
    on_line(f"[exit {proc.returncode}]")
    return proc.returncode


def detect_chip(port: str, on_line: Line) -> Optional[str]:
    """Return an esptool chip id ('esp32', 'esp32s3', ...) or None."""
    argv = esptool_argv("--port", port, "chip_id")
    out_lines: List[str] = []

    def cap(s: str):
        out_lines.append(s)
        on_line(s)

    _run_stream(argv, cap)
    text = "\n".join(out_lines)
    for token, chip in (("ESP32-S3", "esp32s3"), ("ESP32-S2", "esp32s2"),
                        ("ESP32-C6", "esp32c6"), ("ESP32-C5", "esp32c5"),
                        ("ESP32-C3", "esp32c3"), ("ESP32-C2", "esp32c2"),
                        ("ESP32-H2", "esp32h2")):
        if token in text:
            return chip
    if re.search(r"\bESP32\b", text):
        return "esp32"
    return None


# --------------------------------------------------------------------------- #
# firmware acquisition
# --------------------------------------------------------------------------- #

def _http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def latest_release() -> Tuple[str, List[Dict]]:
    """Return (tag, [ {name, url, chip, label} ... ]) for app .bin assets."""
    data = json.loads(_http_get(LATEST_API).decode("utf-8"))
    tag = data.get("tag_name", "latest")
    assets = []
    for a in data.get("assets", []):
        name = a.get("name", "")
        if not name.endswith(".bin"):
            continue
        assets.append({
            "name": name,
            "url": a.get("browser_download_url"),
            "chip": _chip_of_variant(name),
            "label": _variant_label(name),
        })
    return tag, assets


def variants_for_chip(assets: List[Dict], chip: str) -> List[Dict]:
    return [a for a in assets if a["chip"] == chip]


def default_variant(assets: List[Dict], chip: str) -> Optional[Dict]:
    pref = {"esp32": "old_hardware", "esp32s3": "multiboardS3",
            "esp32s2": "flipper", "esp32c5": "esp32c5devkitc1"}.get(chip)
    cands = variants_for_chip(assets, chip)
    if pref:
        for a in cands:
            if pref in a["name"]:
                return a
    return cands[0] if cands else None


def download_to(url: str, dest: str, on_line: Line) -> str:
    on_line(f"[download] {os.path.basename(dest)}")
    data = _http_get(url)
    with open(dest, "wb") as f:
        f.write(data)
    on_line(f"[download] {len(data)} bytes -> {dest}")
    return dest


def _fetch_flashfile(rel_path: str, dest: str, on_line: Line) -> str:
    last = None
    for branch in RAW_BRANCHES:
        url = RAW_TMPL.format(branch=branch, path=rel_path)
        try:
            return download_to(url, dest, on_line)
        except Exception as e:
            last = e
    raise RuntimeError(f"could not fetch {rel_path}: {last}")


def support_files(chip: str, cache: str, on_line: Line) -> Dict[str, str]:
    """Download bootloader/partitions/boot_app0 for a full flash. Returns offset->path."""
    sdir = _SUPPORT_DIR.get(chip)
    if not sdir:
        raise RuntimeError(f"No auto support-file mapping for {chip}; use local files for a full flash.")
    boot = _fetch_flashfile(f"{sdir}/{_BOOTLOADER_NAME}", os.path.join(cache, f"{chip}_bootloader.bin"), on_line)
    part = _fetch_flashfile(f"{sdir}/{_PARTITIONS_NAME}", os.path.join(cache, f"{chip}_partitions.bin"), on_line)
    bapp = _fetch_flashfile(_BOOT_APP0_PATH, os.path.join(cache, "boot_app0.bin"), on_line)
    bl_off = "0x0" if chip in _BOOTLOADER_0 else "0x1000"
    return {bl_off: boot, "0x8000": part, "0xe000": bapp}


# --------------------------------------------------------------------------- #
# flashing
# --------------------------------------------------------------------------- #

def cache_dir() -> str:
    d = os.path.join(tempfile.gettempdir(), "marauder_fw")
    os.makedirs(d, exist_ok=True)
    return d


def erase(port: str, chip: str, on_line: Line) -> int:
    return _run_stream(esptool_argv("--chip", chip, "--port", port, "erase_flash"), on_line)


def flash(port: str, chip: str, app_path: str, on_line: Line,
          mode: str = "app", baud: int = 921600,
          support: Optional[Dict[str, str]] = None) -> int:
    """
    mode 'app'  -> write only the application at 0x10000 (re-flash / update existing board)
    mode 'full' -> write bootloader+partitions+boot_app0+app (blank board); needs `support`
    """
    files: List[str] = []
    if mode == "full":
        if not support:
            on_line("[error] full flash needs bootloader/partitions/boot_app0 (none provided)")
            return 2
        for off, path in support.items():
            files += [off, path]
    files += ["0x10000", app_path]

    # --flash_size detect: auto-detect the chip's real flash size and patch the image header.
    # Without it esptool keeps the binary's header value (often 16MB), which boot-loops a 4MB
    # board with "Detected size(4096k) smaller than ... header(16384k). Probe failed."
    argv = esptool_argv("--chip", chip, "--port", port, "--baud", str(baud),
                        "--before", "default_reset", "--after", "hard_reset",
                        "write_flash", "-z", "--flash_size", "detect", *files)
    return _run_stream(argv, on_line)
