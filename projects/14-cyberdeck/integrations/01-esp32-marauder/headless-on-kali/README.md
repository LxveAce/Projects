# Headless Marauder on Kali Linux — Drive It + Open-Source GUIs

> **Part of:** [ESP32 Marauder — Cyberdeck Integration](../README.md) · [Project 14 — The Cyberdeck](../../../README.md)
> **For:** the **Gold board** Marauder (flashed with the standard ESP32 build, **no screen**).

> **Recommended:** Use **[Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui)** — a dedicated app with four front-ends (Qt GUI, Tkinter, TUI, browser), 70+ commands, live tables, firmware flasher, and data logging. Pre-built ARM64 binaries available for the Pi. The rest of this page covers the manual serial approach and third-party Web Serial GUIs if you want alternatives.

A headless Marauder is just an ESP32 exposing a **text command line over USB serial at
115200 baud**. That's the whole interface — anything that can read/write a serial port can
drive it, which is exactly why it's easy to wrap in your own UI.

---

## TL;DR

| Need | Use |
|------|-----|
| **Full-featured app (recommended)** | **[Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui)** — Qt/Tk/TUI/Browser, 70+ commands, flasher, logging. [ARM64 binary](https://github.com/LxveAce/headless-marauder-gui/releases/latest) for the Pi. |
| **Just use it now (terminal)** | `picocom -b 115200 /dev/ttyUSB0`, type `help` |
| **A Web Serial GUI (Chromium only)** | [marauder-ui-pro](https://github.com/ElectronicCats/marauder-ui-pro) or [Pranav Web GUI](https://github.com/Pranav-V-20/ESP32-Marauder-Web-GUI) |
| **Embed on the Pi (kiosk/auto-start)** | Headless Marauder GUI's browser UI at `localhost:5000`, or the [dashboard](../../parts/dashboard/) pyserial bridge |

---

## 1. Find the device on Kali

1. Plug the Gold board into a Kali/Pi USB port.
2. The Gold uses a **CH340**, which is built into the Linux kernel — **no driver install** needed.
3. Find the port:
   ```bash
   ls /dev/ttyUSB*          # usually /dev/ttyUSB0
   dmesg | grep -i ch341    # confirms the CH340 enumerated
   ```
4. Give yourself serial access without `sudo` (log out/in after):
   ```bash
   sudo usermod -aG dialout $USER
   ```

---

## 2. Drive it from the terminal (baseline)

Any serial terminal works. `picocom` is the simplest:

```bash
sudo apt install -y picocom
picocom -b 115200 /dev/ttyUSB0        # exit with Ctrl-A then Ctrl-X
```

Alternatives: `screen /dev/ttyUSB0 115200` (exit `Ctrl-A` then `K`) or `minicom -D /dev/ttyUSB0 -b 115200`.

Once connected, type `help` and press Enter — it prints the exact command set for *your*
firmware version. Core workflow:

```text
scanap                 # scan for access points
list -a                # list them with indexes (some builds: listap)
select -a 0            # select AP #0  (select -a all = everything)
attack -t deauth       # run the selected attack
stopscan               # stop

sniffpmkid             # capture WPA handshakes/PMKID (saves PCAP if an SD card is in)
sniffbt -t flock       # Flock ALPR camera detection
scansta                # scan client stations
reboot                 # restart the board
```

**Log everything to a file** (handy for the dashboard to parse later):
```bash
picocom -b 115200 /dev/ttyUSB0 | tee marauder-$(date +%F).log
# or:  screen -L /dev/ttyUSB0 115200   (writes screenlog.0)
```

> **Authorization:** only run attacks (`attack`, `evilportal`, BLE/`sourapple`, etc.) against
> networks and devices you own or are explicitly authorized to test. See the legal section in
> the [full Marauder guide](../../../../01-esp32-marauder/).

---

## 3. Open-source GUIs that run on Kali (Web Serial, in Chromium)

These are **browser** apps that talk to `/dev/ttyUSB0` through the **Web Serial API**. They work
in **Chromium / Chrome / Edge / Brave on Kali** — **not Firefox** (no Web Serial). No port
typing: you click **Connect** and pick the device. Great for hands-on use today.

| Project | Stack | License | Run it | Notes |
|---------|-------|---------|--------|-------|
| [Pranav-V-20/ESP32-Marauder-Web-GUI](https://github.com/Pranav-V-20/ESP32-Marauder-Web-GUI) | Static HTML | *unstated — check* | Open the `.html` in Chromium, or the [live page](https://pranav-v-20.github.io/ESP32-Marauder-Web-GUI/) | Zero-setup. Sidebar tools + terminal. Easiest start. |
| [michelangelomo/marauder-ui](https://github.com/michelangelomo/marauder-ui) | Vue 3 + Vite + Tailwind | **MIT** | `npm install && npm run dev` | Clean modern base. **Best to fork** for your own UI. |
| [ElectronicCats/marauder-ui-pro](https://github.com/ElectronicCats/marauder-ui-pro) | Vue 3 + Vite | Open-HW *(verify)* | `npm install && npm run dev` | "Pro" fork: GPS/OpenStreetMap map, SPIFFS/SD file browser, PCAP/log downloads, Evil Portal orchestrator. Tuned for ESP32-C5 but works generally. |
| [Linuxndroid/CLI-Esp32Marauder](https://github.com/Linuxndroid/CLI-Esp32Marauder) | Static HTML | *unstated — check* | [live page](https://linuxndroid.github.io/CLI-Esp32Marauder/) | Lightweight web-serial terminal (despite the "CLI" name it's browser-based). |
| [1amkaizen Web Serial Terminal](https://1amkaizen.github.io/esp32-marauder-cli/) | Static web | *unstated — check* | Open the page in Chromium | Minimal terminal-style dashboard. |

**Run a self-hosted one offline (recommended for the deck):**
```bash
git clone https://github.com/michelangelomo/marauder-ui
cd marauder-ui
npm install
npm run dev            # then open the printed http://localhost:5173 in CHROMIUM
# click Connect -> pick /dev/ttyUSB0
```
(If the port doesn't appear in the Chromium picker, confirm you're in the `dialout` group from step 1.)

---

## 4. TUI / scriptable control

> **Note:** [Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui) already includes a Textual TUI (`headless-marauder-tui`). The section below is for rolling your own if you want something custom.

Because the interface is plain serial text, wrapping it is a few lines of [`pyserial`](https://pyserial.readthedocs.io/):

```python
import serial
m = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
m.write(b"scanap\n")
import time; time.sleep(8)
m.write(b"list -a\n")
print(m.read(4096).decode(errors="replace"))
m.write(b"stopscan\n")
```

From that core you can build:
- a **TUI** with [Textual](https://textual.textualize.io/) or `urwid`, or
- a **web dashboard** with Flask/FastAPI + websockets feeding a browser frontend.

---

## 5. Pre-packaging into the cyberdeck all-in-one UI

[Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui) already handles this. Its `marauder_core` library is importable, and the deck's [dashboard](../../parts/dashboard/) reuses it to show Marauder alongside Kismet, Meshtastic, and GPS. The app's browser UI (`headless-marauder-web` at `localhost:5000`) can also run in a kiosk-style setup.

If you want to build something completely custom instead, avoid Web Serial (requires Chromium + manual port pick + user gesture each session — awkward to auto-start headless). Use a **server-side serial bridge**:

- A pyserial backend owns `/dev/ttyUSB0`, auto-connects on boot (systemd), exposes a websocket/REST API.
- A web frontend (Chromium kiosk on the 7" screen) talks to that backend alongside the other tools.

For a from-scratch frontend, [michelangelomo/marauder-ui](https://github.com/michelangelomo/marauder-ui) (MIT) is a clean Vue 3 base to fork.

---

## Troubleshooting: `ls /dev/ttyUSB*` says "No such file or directory"

The board isn't showing up as a serial port. Work down this list — on Kali the #1 cause is `brltty`.

1. **Cable + power:** use the **data** cable you flashed with (charge-only cables show nothing),
   plugged into a direct port (not a hub) for first contact.
2. **Does the OS see the USB device at all?**
   ```bash
   lsusb | grep -i 1a86        # the Gold's CH340 = "QinHeng" / 1a86:7522
   ```
   - **Listed →** it's a driver/naming/`brltty` issue → steps 3–4.
   - **Not listed →** the port isn't reaching this OS → steps 5–6.
3. **`brltty` is stealing it (most common on Kali/Debian).** `brltty` mistakes CH340 chips for a
   braille display and yanks `/dev/ttyUSB0` ~1 second after it appears. If the port flashes up then
   vanishes, this is it:
   ```bash
   sudo apt remove brltty       # then unplug/replug the board
   dmesg | tail -20             # confirm brltty no longer grabs it
   ```
4. **Wrong name / driver not loaded** — check both names; CH340 may land on `ttyACM`:
   ```bash
   ls /dev/ttyUSB* /dev/ttyACM*
   sudo modprobe ch341
   ```
   If it's `/dev/ttyACM0`, just use that path (`picocom -b 115200 /dev/ttyACM0`).
5. **Kali in a VM (VirtualBox/VMware):** the host OS owns the USB until you pass it through.
   VirtualBox → *Devices ▸ USB ▸* tick "QinHeng CH340" (needs the Extension Pack).
   VMware → *VM ▸ Removable Devices ▸ CH340 ▸ Connect*.
6. **Kali on WSL:** WSL2 has no `/dev/ttyUSB` by default — attach the device from Windows with
   [usbipd-win](https://github.com/dorssel/usbipd-win) (`usbipd bind` then `usbipd attach --wsl`).
7. Still nothing? Try a different cable/port, and confirm the board powers on (its LED).

## Source / Upstream

- **Headless Marauder GUI:** [LxveAce/headless-marauder-gui](https://github.com/LxveAce/headless-marauder-gui) — the recommended control app (Qt/Tk/TUI/Browser, ARM64 binary for Pi)
- Marauder CLI reference: [justcallmekoko/ESP32Marauder Wiki — CLI](https://github.com/justcallmekoko/ESP32Marauder/wiki/cli) · [CLI Usage](https://github.com/justcallmekoko/ESP32Marauder/wiki/cli-usage)
- Third-party Web Serial GUIs: [marauder-ui (MIT)](https://github.com/michelangelomo/marauder-ui) · [marauder-ui-pro](https://github.com/ElectronicCats/marauder-ui-pro) · [Pranav Web GUI](https://github.com/Pranav-V-20/ESP32-Marauder-Web-GUI)
- Deck dashboard architecture: [parts/dashboard](../../parts/dashboard/)
