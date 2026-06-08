# Headless Marauder

**Native control + firmware flasher for a headless [ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder).**
No browser, no Web Serial, no cloud — a real Linux/Kali application that talks straight to the
board over USB serial, shows live Access-Point / Station tables, picks targets with checkboxes,
logs everything to disk, and flashes firmware itself.

> Built for a headless Marauder (e.g. a Lonely Binary "Gold" ESP32 with an external antenna and
> no screen) driven from a Raspberry Pi / laptop — including as the brain of a cyberdeck. Works
> with any ESP32 running Marauder firmware.

---

## Why

The browser UIs for Marauder rely on the **Web Serial API**, which only exists in Chromium — so
on Kali (Firefox by default) they simply don't work, and they're thin on options. This is a
**native app**: it owns `/dev/ttyUSB0` directly, exposes the *full* Marauder command set, and runs
in any environment (and can auto-start headless on a deck).

## Features

- **Three front-ends, one core** — a polished **PyQt5 GUI** (recommended), a simple **Tkinter GUI**, and a **Textual TUI** for the terminal/SSH.
- **Every Marauder command** (70+) as buttons/tree entries, with parameter forms, plus a raw command box for anything.
- **Live tables** — `scanap` auto-fills the **Access Points** tab (and the TUI table); APs/Stations parsed straight off the serial stream and de-duplicated.
- **Target picker** — click *Select APs* and check the networks you want; it builds the correct `select -a 0,2,5` from Marauder's real indices (manual entry still available).
- **Built-in firmware flasher** — detects the chip (classic ESP32 vs S3), pulls the right firmware variant from the official GitHub release, and flashes at the correct offsets with `--flash_size detect`. App-only update *or* full blank-board flash. Wraps `esptool`.
- **Data logging** — capture the raw serial stream + a live `latest.json` snapshot + `aps.csv`/`stations.csv` to a folder you choose; `tail -f`-friendly for other tools/devices.
- **Self-update** — *Help → Check for Updates* runs `git pull` + reinstall from this repo.
- **Installable** — `./install.sh` adds it to your application menu and a `headless-marauder` command. Touch-aware, but optimized for keyboard + mouse (shortcuts below).

---

## Install (Kali / Debian)

```bash
git clone https://github.com/LxveAce/headless-marauder-gui.git
cd headless-marauder-gui
./install.sh
```

That sets up a venv, installs dependencies (incl. PyQt5 and `esptool`), and adds:
- a menu entry **“Headless Marauder”**,
- a `headless-marauder` command (Qt GUI) and `headless-marauder-tui` (terminal UI).

Give yourself serial access without `sudo` (once, then re-login):
```bash
sudo usermod -aG dialout $USER
```

<details>
<summary>Manual / dev run (no installer)</summary>

```bash
sudo apt install -y python3-venv python3-tk python3-pyqt5
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt        # pyserial + textual + esptool
python3 gui_qt/app.py                   # or: gui/app.py  /  tui/app.py
# add --mock to explore with no board, --port /dev/ttyUSB0 to skip auto-detect, --log to record
```
</details>

---

## Using it

1. **Connect** — it auto-detects the board (115200 baud); the top bar turns green.
2. **Scan APs** — with **Auto-list** on (default), the **Access Points** tab fills itself while it scans.
3. **STOP** when you've seen enough.
4. **Select APs** — tick the network(s) in the picker → it sends `select -a …`.
5. Run an action — e.g. **Deauth (selected APs)** (leave `src`/`dst` blank for a normal broadcast deauth).

**Keyboard shortcuts (Qt):** `Ctrl+L` clear · `F5` refresh ports · `Ctrl+K` focus command box · `Ctrl+.` STOP · `Ctrl+U` check for updates · `Ctrl+Q` quit.

**Flashing:** *⚡ Flash Firmware* → **Detect chip** → **Load release list** → pick a variant → **Update app only** (existing board) or **Full flash** (blank board) → **FLASH**.

**Logging:** toggle **● Log** (or *File → Set Log Folder*). Writes to `~/marauder-logs` by default — `serial-*.log`, `latest.json`, `aps.csv`, `stations.csv`, all live-readable.

---

## Troubleshooting

- **No `/dev/ttyUSB0`** — the Gold uses a CH340. On Kali, `brltty` often steals it: `sudo apt remove brltty`, replug. Also ensure you're in `dialout`. In a VM, pass the USB device through.
- **Board boot-loops / `scanap` does nothing** — check the Console:
  - `invalid header: 0xffffffff` → flash is **blank** → flasher **Full flash**.
  - `Detected size(4096k) smaller than ... header(16384k)` → wrong flash-size header → the flasher fixes this with `--flash_size detect`; **Erase**, then re-flash.
- **Deauth "does nothing"** — Marauder prints `Starting Deauthentication attack` once, then runs silently. If a device doesn't drop, it's almost always **802.11w/PMF** (modern routers ignore deauth), a **5GHz** target (classic ESP32 is 2.4GHz only), or **no clients** connected.
- **Qt GUI won't start** — PyQt5 missing: `sudo apt install -y python3-pyqt5` (and make the venv with `--system-site-packages`), or use `headless-marauder-tui`.

---

## Architecture

```
marauder_core/   controller.py · parsing.py · commands.py · flasher.py · capture.py · updater.py
gui_qt/app.py    PyQt5 GUI (live tables, picker, flasher, logging)   ← recommended
gui/app.py       Tkinter GUI (simple, stdlib)
tui/app.py       Textual terminal UI
install.sh       app-menu install + launchers + self-update enablement
```
One command catalog and one parser feed all three front-ends; the serial layer streams to the UI, the parser, and the logger together.

---

## Legal

For **authorized security testing only** — use against networks and devices you own or have
explicit written permission to test. WiFi deauthentication, evil-portal, and BLE-spam features can
be illegal to use against others (e.g. US CFAA, FCC rules). You are responsible for how you use this.

## Credits & License

- Firmware: **[ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder)** by justcallmekoko (GPL) — this app only talks to it over serial.
- Built on [pyserial](https://pyserial.readthedocs.io/), [PyQt5](https://www.riverbankcomputing.com/software/pyqt/), [Textual](https://textual.textualize.io/), and [esptool](https://github.com/espressif/esptool).
- Part of the [Cyberdeck project](https://github.com/LxveAce/Projects/tree/main/projects/14-cyberdeck).

Licensed under the **[MIT License](LICENSE)**.
