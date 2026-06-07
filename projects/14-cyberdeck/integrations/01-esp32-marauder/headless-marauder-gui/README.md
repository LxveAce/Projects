# Headless Marauder GUI/TUI

> **Part of:** [ESP32 Marauder — Cyberdeck Integration](../README.md) · [headless-on-kali](../headless-on-kali/)
> Our own control software for a **headless** ESP32 Marauder (the Gold board with the external
> antenna and no screen). Built because the browser UIs are thin on options and need Chromium's
> Web Serial — these are **native applications** that talk straight to `/dev/ttyUSB0`.

Three native apps, one shared core:

| App | What it is | Run | Needs |
|-----|------------|-----|-------|
| **Qt GUI** ⭐ | Polished **PyQt5** window — command sidebar, live colorized console, **live Access-Point & Station tables** (parsed from the serial stream), built-in flasher, STOP | `./run-qt.sh` | `pyserial` + `PyQt5` |
| **Tkinter GUI** | Simpler native window (stdlib) — same buttons/console/flasher, no extra install | `./run-gui.sh` | `pyserial` + `python3-tk` |
| **Terminal TUI** | **Textual** terminal app — command tree, live log, **live AP table**; great over SSH / on the deck console | `./run-tui.sh` | `pyserial` + `textual` |

**No web server, no browser, no Web Serial.** Works on Kali regardless of which browser is installed
(the Firefox/Web-Serial dead-end doesn't apply here). Both front-ends drive the same
[`marauder_core`](marauder_core/) and the same full [command catalog](marauder_core/commands.py).

---

## Install on Kali Linux

Kali blocks system-wide `pip` (PEP 668), so use a venv. **Simple path:**

```bash
# 1. system bits (once)
sudo apt update
sudo apt install -y python3-venv python3-tk        # python3-tk = the Tkinter GUI

# 2. from this folder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt                    # pyserial + textual + esptool

# 3. for the prettier Qt GUI (recommended)
pip install PyQt5
#   ...if pip PyQt5 fails (sometimes on the Pi), use the system package instead:
#   deactivate; sudo apt install -y python3-pyqt5
#   python3 -m venv .venv --system-site-packages; source .venv/bin/activate; pip install -r requirements.txt
```

Make sure you can reach the serial port without sudo (log out/in after):
```bash
sudo usermod -aG dialout $USER
```
> Port issues (no `/dev/ttyUSB0`, `brltty` stealing the CH340, VM passthrough)? See
> [../headless-on-kali](../headless-on-kali/#troubleshooting-ls-devttyusb-says-no-such-file-or-directory).

---

## Run

```bash
./run-qt.sh                  # ⭐ Qt GUI with live AP/station tables (recommended)
./run-gui.sh                 # simple Tkinter window
./run-tui.sh                 # terminal app

# options (any app):
./run-qt.sh --port /dev/ttyUSB0     # skip auto-detect
./run-qt.sh --mock                  # no hardware — explore the UI
```

Both **auto-detect** the port (preferring the Gold's CH340), connect at **115200 baud**, then:
- click a command button (GUI) or pick one in the tree (TUI),
- commands with options pop a parameter form / pre-fill a template,
- everything the board prints streams into the console,
- **STOP** sends `stopscan`.

> Only one program can hold the serial port — close any `picocom`/`screen` session first.

---

## What it covers

The [catalog](marauder_core/commands.py) exposes the full Marauder CLI, grouped:
**WiFi · Scan** (scanap, scansta, scanall, sigmon, packetcount, wardrive) ·
**WiFi · Sniff** (raw, beacon, probe, deauth, esp, pwnagotchi, PMKID w/ channel+deauth+targeted) ·
**WiFi · Attack** (deauth APs/clients, beacon list/random/clone, probe flood, rickroll, badmsg, evil portal, karma) ·
**WiFi · Network** (join, pingscan, portscan) ·
**Bluetooth** (sniffbt airtag/flipper/flock, btwardrive, skimmer detect, BLE spam, AirTag spoof) ·
**Lists & Targets** (list/select/clearlist/info) · **SSID** · **Channel** · **GPS** · **Files (SD)** ·
**System** (settings, led, update, reboot, stopscan).

Anything not buttoned is still one keystroke away in the **raw command box**.

---

## Flash firmware (built in)

Both apps can flash Marauder firmware onto a board — **GUI:** the *⚡ Flash Firmware* button ·
**TUI:** press **`f`**. It wraps [`esptool`](https://github.com/espressif/esptool) and pulls
firmware straight from the official GitHub release.

What it does:
1. **Detect chip** over the port (`esptool chip_id`) — tells classic **ESP32** from **ESP32-S3**,
   so you never flash the wrong build (the mistake that fails ESP Terminator's preflight).
2. **Pick the firmware** — *Download latest release* (the variant list is filtered to your chip,
   with a sensible default) or *Local .bin* (browse).
3. **Choose a mode:**
   - **Update app only** — writes just the app at `0x10000`. Use this to update/re-flash a board
     that already runs Marauder (your Gold boards). Fast and safe.
   - **Full flash (blank board)** — also fetches bootloader + partitions + `boot_app0` from the
     repo's `FlashFiles/` tree and writes them at the right offsets
     (bootloader `0x1000` on classic ESP32, `0x0` on S3).
4. **FLASH** — `esptool` output streams live into the window. There's also an **Erase flash**.

Notes:
- There is **no generic "esp32" release build** — for a classic ESP32 Gold pick a non-S3 variant
  (e.g. *Generic ESP32 / original v4*, or *Generic ESP32 dev board, no display* for a headless
  board); for an S3 pick *MultiBoard S3*. The app defaults sensibly per detected chip.
- Flashing needs exclusive access to the port, so the app **auto-closes the live serial session**
  before it runs esptool.
- Requires `esptool` (in `requirements.txt`).

> **Authorization:** the attack/spam commands are for networks and devices you own or are
> explicitly authorized to test. See the legal section in the [full Marauder guide](../../../../01-esp32-marauder/).

---

## Architecture (and why it's built this way)

```
marauder_core/
  controller.py   # pyserial connection, port auto-detect, threaded reader, pub/sub, --mock
  commands.py     # the single command catalog (data-driven) — shared by ALL apps
  parsing.py      # parses scanap/scansta output into live AP/Station tables
  flasher.py      # esptool wrapper: detect chip, fetch firmware, flash at right offsets
gui_qt/app.py     # PyQt5 desktop app  (live tables — recommended)
gui/app.py        # Tkinter desktop app (simple, stdlib)
tui/app.py        # Textual terminal app
```

Live tables come from `parsing.py`: the AP line format (`RSSI: -57 Ch: 3 BSSID: .. ESSID: ..`)
is parsed as the stream arrives and de-duplicated by MAC, so the **Access Points** / **Stations**
tabs (Qt) and the AP table (TUI) update themselves while `scanap`/`scansta` run.

- **Server-side serial, native UI** — the app owns `/dev/ttyUSB0` directly, so there's no Web
  Serial / Chromium requirement and it can auto-start headless on the deck later.
- **One catalog, two UIs** — add a `Command(...)` in `commands.py` once and it appears in the GUI
  *and* the TUI. That's how we keep "all the options" without maintaining two lists.
- **Thread-safe output** — the reader thread pushes lines onto a queue; each UI drains it on its
  own main loop (`after()` in Tk, `set_interval()` in Textual).

## Extending it

Add a command — that's the whole edit:
```python
# marauder_core/commands.py
Command("my_id", "My Button", "somecmd -x", "WiFi · Scan",
        "what it does",
        params=[Param("value", "-n", "int", required=True, placeholder="5")])
```

## Roadmap → cyberdeck all-in-one UI

This is the seed for the deck's [dashboard](../../parts/dashboard/). Next steps:
- expose `marauder_core` over a small local IPC (or import it directly) so the deck UI reuses it,
- add response parsing (AP/station tables) for structured panels,
- fold in Kismet / Meshtastic / GPS alongside Marauder in one app.

## License / credit

Original work for this repo. Command set per the
[ESP32 Marauder CLI wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/cli)
(firmware by justcallmekoko, GPL). Built on [pyserial](https://pyserial.readthedocs.io/) and
[Textual](https://textual.textualize.io/).
