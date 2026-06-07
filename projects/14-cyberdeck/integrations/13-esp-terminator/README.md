# ESP Terminator — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/13-esp-terminator](../../../13-esp-terminator/)
> **Deck role:** The flashing tool — loads firmware onto every ESP32 board in the deck
> **Status:** Ready to use (browser web tool, no hardware to build)

---

## The Decision

ESP Terminator isn't a board in the deck — it's the **web flasher** you point at each ESP32
board to load the right firmware. This guide is the deck's "how to flash the boards" hub:
one general flashing flow, then the exact firmware that goes on each board.

| Question | Choice for the deck |
|----------|---------------------|
| **What it is** | [espterminator.com](https://espterminator.com/) — browser-based ESP32 firmware flasher |
| **Why it's used** | Recommended flasher for Marauder; one interface flashes every ESP32 in the rig |
| **Browser** | **Chrome or Edge** (Web Serial API — Firefox/Safari won't work) |
| **Driver** | **CH340** for the Gold boards ([WCH](http://www.wch-ic.com/downloads/CH341SER_EXE.html)); CP210x for some others ([Silicon Labs](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)) |
| **Cable** | USB **data** cable (not charge-only) |
| **Hardware to buy** | None — the tool is free and runs in the browser |

> **Note on Meshtastic:** ESP Terminator *can* flash Meshtastic, but the deck flashes the
> Heltec V3 with the official [flasher.meshtastic.org](https://flasher.meshtastic.org/)
> instead — see [../04-meshtastic/](../04-meshtastic/). ESP Terminator handles the four
> ESP32 security boards.

---

## What You Need (from the repo inventory)

- A PC running **Chrome or Edge** (the deck's Pi 5 can also do it, or any laptop)
- The right USB-serial driver for the board — the **Gold boards use a CH340** ([WCH driver](http://www.wch-ic.com/downloads/CH341SER_EXE.html)); some other boards use **CP210x** ([Silicon Labs](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)). Reboot after install.
- USB-C / Micro-USB **data** cable to match each board
- The deck's ESP32 boards from [INVENTORY.md](../../../../INVENTORY.md):
  - Lonely Binary Gold #1, #2, #3 (**classic ESP32**, CH340 — verified by esptool, *not* S3)
  - ESP32-WROOM-32

---

## Get It Running

### 1. General flashing flow (any ESP32)

1. Open **Chrome or Edge** and go to [espterminator.com](https://espterminator.com/).
2. Plug the target board into your PC with a USB **data** cable.
3. Hold the **BOOT** button on the board (needed for boards in manual/no-native-USB bootloader).
4. Click **Connect**, pick the COM port from the browser prompt, then release **BOOT**.
5. Pick the **firmware** for that board (see the per-board map below).
6. Click **Install** / **Flash**. Do **not** disconnect while it runs.
7. When it reports "complete," press **RST** — the board reboots into the new firmware.

> **Caveats from the source:** If the board isn't detected, check the USB-serial driver in
> Device Manager (CH340 for the Gold boards, CP210x for some others) and swap to a known data
> cable. If flashing stalls at connect, hold BOOT
> during connect; for ESP32-S2 boards use "No Reset" mode. ESP Terminator won't brick a
> board — you can always re-flash.

### 2. Per-board firmware map (the deck's boards)

| Board | Chip | Firmware to flash | Where it's used | Guide |
|-------|------|-------------------|-----------------|-------|
| **Gold #1** | classic ESP32 | ESP32 Marauder — **standard ESP32 (WROOM)** build | Primary WiFi/BLE tool | [../01-esp32-marauder/](../01-esp32-marauder/) |
| **Gold #2** | classic ESP32 | Marauder Flock mode (`sniffbt -t flock`) — or flock-you if its build targets classic ESP32 | Flock ALPR detection | [../06-flock-drone-detection/](../06-flock-drone-detection/) |
| **Gold #3** | classic ESP32 | ESP32-AirTag-Scanner (Arduino IDE → "ESP32 Dev Module") | BLE tracker detection | [../08-ble-detection/](../08-ble-detection/) |
| **WROOM-32** | classic ESP32 | Sky-Spy drone firmware | Drone RemoteID detection | [../06-flock-drone-detection/](../06-flock-drone-detection/) |
| Heltec V3 | **ESP32-S3** (LoRa) | Meshtastic — *use [flasher.meshtastic.org](https://flasher.meshtastic.org/)* | Off-grid mesh | [../04-meshtastic/](../04-meshtastic/) |

> **Critical:** the three Gold boards are **classic ESP32** (CH340, 16 MB — verified by esptool).
> For Marauder pick the **standard ESP32 (WROOM)** build, *not* `_multiboardS3.bin`, or the
> flasher's preflight rejects it (`target ESP32-S3 does not match detected chip ESP32`). The
> Heltec V3 genuinely *is* an ESP32-S3, but it's flashed with Meshtastic's own web flasher.

### 3. Verify

- **Boards with a display (Gold #1/#2 + CYD):** the firmware boot screen / GUI appears on power-up.
- **Headless boards (Gold #3, WROOM-32):** connect a serial terminal at **115200 baud** and
  confirm the firmware responds.

```bash
screen /dev/ttyUSB0 115200     # confirm the new firmware banner / prompt
```

---

## Cyberdeck Compatibility Notes

- **No deck slot, no power, no antenna, no display** — ESP Terminator lives on a PC/browser,
  not in the chassis. It consumes nothing from the [power](../parts/power/) or
  [antenna](../parts/antennas/) budgets.
- **One-time-per-board, then occasional:** you run it to provision each board, and again only
  when you update firmware. After flashing, the boards run on their own per their guides.
- **Re-flash anytime:** if a board misbehaves, this is the tool to recover it — it can't brick
  the board, just re-flash the correct firmware from the map above.
- **Driver dependency:** the same USB-serial driver that lets ESP Terminator see the board
  (CH340 for the Gold boards) is what the [Pi 5 brain](../parts/pi5-brain/) uses to read those
  boards at `/dev/ttyUSBx` — Linux/Kali has CH340 + CP210x built in, so they enumerate automatically.

## Standalone Mode

ESP Terminator flashes **any** ESP32 — deck board or not. Point it at a bench CYD, an AWOK
board, a generic WROOM dev board, or a Flipper Zero WiFi dev board and it loads Marauder,
GhostESP, Bruce, M5Launcher, and more. Nothing about it is deck-specific; the deck just uses
it for the five boards above.

## Source / Upstream

- Web flasher: [espterminator.com](https://espterminator.com/) (by [dagnazty](https://github.com/dagnazty))
- Marauder firmware update wiki: [justcallmekoko/ESP32Marauder — update-firmware](https://github.com/justcallmekoko/ESP32Marauder/wiki/update-firmware)
- Full options, supported firmware, legal notes: [projects/13-esp-terminator](../../../13-esp-terminator/)
