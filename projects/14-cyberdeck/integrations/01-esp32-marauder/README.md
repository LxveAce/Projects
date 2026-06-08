# ESP32 Marauder — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/01-esp32-marauder](../../../01-esp32-marauder/)
> **Deck role:** Primary WiFi/BLE offensive tool
> **Status:** Both Marauders built — CYD #1 (touchscreen) complete, Gold #1 (headless) complete and running standalone in Meshnology Heltec V4 case

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Board** | Lonely Binary ESP32 **Gold #1** |
| **Chip** | **Classic ESP32** (WROOM-class, 16 MB flash, CH340 USB) — *not* an S3 |
| **Firmware** | ESP32 Marauder, the **standard ESP32 (WROOM)** build — *not* `_multiboardS3.bin` |
| **Flash tool** | [ESP Terminator](https://espterminator.com/) web flasher, or the [built-in flasher](https://github.com/LxveAce/headless-marauder-gui) in Headless Marauder GUI |
| **Display** | CYD #1 — its *own* standalone touchscreen Marauder (a separate device, **not** a display wired to the Gold) |
| **Antenna** | IPEX → U.FL pigtail → **SMA bulkhead #1** ("MAR") → Bingfu 2.4/5.8 GHz |
| **Power** | Powered USB hub, gated by toggle **SW1** |

> **Two independent Marauders, by design:** Marauder runs *on* the board it's flashed to —
> there is no "brain + dumb display" mode. So the deck runs **two** Marauders: **Gold #1**
> headless (no screen, driven by the Pi over USB serial, owns the external antenna for range),
> and **CYD #1** as a self-contained touchscreen Marauder you operate by hand. They do **not**
> wire to each other. The Gold earns its slot via the IPEX/U.FL external antenna — the CYD's
> onboard ESP32 has only a PCB-trace antenna (an external antenna would need a soldered mod).

> **Critical:** the Lonely Binary Gold reports as a **classic ESP32** — verified by esptool
> (`Device: ESP32`, CH340 converter, 16 MB flash). Use the **standard ESP32 (WROOM)** Marauder
> build. The `_multiboardS3.bin` (ESP32-S3) firmware fails the flasher's preflight
> (`Firmware target (ESP32-S3) does not match detected chip (ESP32)`) and won't boot.

### Does the Gold get its own screen?

The Gold has no built-in display — so a Marauder flashed on it is **headless** (serial CLI only).
Three ways to give it a "screen," in order of effort:

1. **Use the Pi's 7" dashboard (recommended, no hardware).** The Gold runs headless; the Pi reads
   its serial output and shows it on the 7" DSI via the [dashboard](../parts/dashboard/). The big
   external antenna lives on the Gold, the screen lives on the Pi. This is the deck's design.
   **See [headless-on-kali](headless-on-kali/) for how to drive a headless Gold from Kali and the
   open-source GUIs/TUIs you can use or pre-package into the all-in-one UI.**
2. **Carry the CYD as a second, standalone Marauder.** The CYD already has its own screen + ESP32 —
   it's a complete touch Marauder on its own (you can't move its screen onto the Gold; it's one PCB).
   Grab-and-go GUI without the Pi. (Its antenna is a PCB trace, so shorter range than the Gold.)
3. **Wire a bare ILI9341 SPI touch TFT directly to the Gold (advanced).** Gives the Gold its own
   local touchscreen *and* the external antenna, but needs jumper wiring + a build-from-source
   display firmware (TFT_eSPI `User_Setup.h`). Pin map is in the
   [full Marauder guide, Build Path 2](../../../01-esp32-marauder/). Soldering/wiring required.

---

## What You Need (from the repo inventory)

- Lonely Binary ESP32 Gold #1 — from the [3-pack](../../../../INVENTORY.md)
- CYD 2.8" Touchscreen #1 (ESP32-2432S028R, ILI9341)
- U.FL/IPEX → SMA pigtail (15–20 cm) → SMA bulkhead #1
- Bingfu 2.4/5.8 GHz antenna (+ Boobrie RP-SMA→SMA adapter)
- 128 GB micro SD (optional — PCAP capture, Evil Portal HTML)
- USB-C **data** cable for flashing

---

## Get It Running

### 1. Flash the firmware

1. Open **Chrome or Edge** (WebSerial required — Firefox/Safari won't work).
2. Go to [espterminator.com](https://espterminator.com/).
3. Plug Gold #1 into your PC with a USB-C data cable.
4. Hold **BOOT**, click **Connect**, pick the COM port, release BOOT.
5. Select **ESP32 Marauder** → the **standard ESP32 (WROOM)** target — the generic ESP32 one,
   **not** MultiBoard S3 and **not** a CYD-specific build.
6. Click **Install** / **Flash** and wait for "complete," then press **RST**.

CLI alternative (same result — note the classic-ESP32 chip and `0x1000` bootloader offset):
```bash
pip install esptool
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x1000 esp32_marauder.ino.bootloader.bin \
  0x8000 esp32_marauder.ino.partitions.bin \
  0xe000 boot_app0.bin \
  0x10000 esp32_marauder_v1.12.1.bin
```
(If it stalls at connect, hold BOOT during connect and drop to `--baud 115200`.)

### 2. Wire it into the deck

> **Bench first, case later.** Steps below are the *final in-case wiring*. Right now, on the
> bench, every board just runs off a USB cable on your desk — you don't need the plate, the
> hub, the switches, or any antenna to test. The "ESP32 plate" is a 3 mm acrylic mounting
> plate you cut and drill during the physical build — see [case-prep](../parts/case-prep/).

- **Mount:** Gold #1 on the ESP32 plate (the cut acrylic [mounting plate](../parts/case-prep/))
  via M3 brass standoffs. *(Build-time step — skip on the bench.)*
- **Antenna:** snap the U.FL pigtail straight down onto the Gold's IPEX socket (feel the
  click — never twist), route to **SMA bulkhead #1**, screw the antenna on outside.
  *U.FL is rated ~30 mating cycles — treat as semi-permanent.*
- **CYD #1:** it does **not** connect to the Gold. It's a separate standalone Marauder — mount
  it face-up, power it from its own hub port, operate it by hand. (See [displays](../parts/displays/).)
- **Power:** USB from the powered hub → inline **toggle SW1** → Gold #1.
- **Data:** the same USB run carries serial to the Pi 5 (`/dev/ttyUSBx`, 115200 baud).
- **SD (optional):** FAT32, ≤32 GB, SanDisk recommended — enables `SavePCAP`.

### 3. Verify

**Gold #1 (headless):** connect over serial and type a command —
```bash
screen /dev/ttyUSB0 115200      # then type:
scanap                          # should list nearby APs
stopscan
```
**CYD #1 (standalone):** just power it over USB — it boots straight into the Marauder
touchscreen GUI, no Pi or Gold involved.

---

## Cyberdeck Compatibility Notes

- **USB/serial budget:** consumes one powered-hub port; Pi reads it at `/dev/ttyUSBx`.
- **Dashboard:** the Pi 5 [dashboard](../parts/dashboard/) parses Marauder serial output and
  shows AP/station counts live. Command set: `scanap`, `scansta`, `attack -t deauth`,
  `sniffbt -t flock`, `stopscan`.
- **Overlap with Flock:** Marauder has a built-in `sniffbt -t flock`, so Gold #1 *can* do
  Flock detection too. The deck keeps [Flock on Gold #2](../06-flock-drone-detection/) for
  flexibility — but if you ever drop Gold #2, Marauder covers it.
- **Antenna:** owns bulkhead **#1** only — no conflict with the other radios.
- **Power modes:** SW1 fully cuts Marauder power for the "stealth" / low-draw profiles in the
  [power guide](../parts/power/) — zero RF emission when off.

## Current Status (June 2026)

Both Marauders are flashed and working:

- **CYD #1 (touchscreen Marauder):** Complete. Standalone touchscreen Marauder — power it via USB, use the touch GUI directly. No Pi needed.
- **Gold #1 (headless Marauder):** Complete. Currently housed in a **Meshnology Heltec V4 case** — the case has the right USB port and antenna cutouts, so it was rigged up as a standalone portable unit. Controlled over USB via [Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui) (any laptop/Pi, four front-ends).

**For the cyberdeck:** Gold #1 is currently committed to the standalone setup. To free it up for the deck, either pull it from the Heltec case (it's removable), or **purchase a 4th Lonely Binary Gold** to dedicate to the deck. A 4th Gold is the cleaner path — keeps the standalone headless unit intact while the deck gets its own board on SMA #1.

| Item | For | Est. Price |
|------|-----|-----------|
| Lonely Binary ESP32 Gold (single or 3-pack) | Cyberdeck Gold #1 slot (or standalone replacement) | ~$12-36 |

## Standalone Mode

Both Marauders work with the Pi off. **CYD #1** is a self-contained touchscreen Marauder —
power it and use it by hand (scans, attacks, PCAP to SD). **Gold #1** runs headless in the Heltec V4 case; plug it into any laptop via USB, run [Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui), and it's fully operational. Nothing about the deck wiring
ties either one down — pull either board out and it's the same Marauder on the bench.

## Headless Marauder GUI (the control app)

The Gold runs headless — no screen, serial CLI only. To actually use it from the Pi, there's a dedicated app:

**[Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui)** (v1.2.0) — a native Python app with four front-ends (PyQt5 GUI, Tkinter, TUI, browser UI), 70+ Marauder commands, live AP/Station tables, a target picker, built-in firmware flasher, and data logging.

**On the cyberdeck (Pi 5 / ARM64):**

- **Standalone binary (easiest):** download the [Linux ARM64 build](https://github.com/LxveAce/headless-marauder-gui/releases/latest) from the Releases page. No Python, no pip, no venv — just `chmod +x` and run. Requires a 64-bit Pi OS.
- **From source:** `git clone https://github.com/LxveAce/headless-marauder-gui.git && cd headless-marauder-gui && ./install.sh` — installs all four UIs as commands.
- **Browser UI:** run `headless-marauder-web` and open `localhost:5000` on the Pi's display or from any device on the same network (`--host 0.0.0.0`).

The app's `marauder_core` library is importable — the cyberdeck [dashboard](../parts/dashboard/) reuses it to show Marauder data alongside Kismet, Meshtastic, and GPS.

For the manual serial approach (picocom, screen, etc.) and third-party Web Serial GUIs, see [headless-on-kali](headless-on-kali/).

## Source / Upstream

- Upstream firmware: [justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder)
- Headless Marauder GUI: [LxveAce/headless-marauder-gui](https://github.com/LxveAce/headless-marauder-gui)
- Full options, attack usage, legal notes: [projects/01-esp32-marauder](../../../01-esp32-marauder/)
