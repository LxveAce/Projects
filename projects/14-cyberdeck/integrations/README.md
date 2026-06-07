# Cyberdeck Integrations

> **Part of:** [Project 14 — The Cyberdeck](../README.md)

This folder takes every project and hardware subsystem in the repo and re-frames it
**specifically for the cyberdeck build**. Where the original project guides list *every*
option, board, and firmware variant, the guides here document **only the choice that was
made for the deck** — one path, the exact parts from the inventory, and the simple
step-by-step needed to get that piece flashed, built, and wired into the full rig.

Each guide is also written so the subsystem **still works on its own**. Pull the board
out of the deck and it runs standalone; the "Standalone Mode" section in every guide
explains what changes.

---

## How These Guides Differ from the Originals

| | Original project guide (`projects/NN-*/`) | Integration guide (here) |
|---|---|---|
| **Scope** | All options, boards, firmwares, background | The one choice made for the deck |
| **Goal** | Understand the whole landscape | Get *this* piece running in the deck, fast |
| **Parts** | Many alternatives with prices | The exact items from [INVENTORY.md](../../../INVENTORY.md) |
| **Audience** | Researching what to build | Building the deck right now |

The originals are **untouched** — treat them as the reference library. These are the build sheets.

---

## Project Integrations

Each maps to a numbered project in the repo. Numbers match the source project folder.

| # | Guide | Deck role | Board / device | Source |
|---|-------|-----------|----------------|--------|
| 01 | [ESP32 Marauder](01-esp32-marauder/) | Primary WiFi/BLE offensive tool | Lonely Binary Gold #1 (S3) | [01-esp32-marauder](../../01-esp32-marauder/) |
| 02 | [Flipper Zero](02-flipper-zero/) | Sub-GHz / RFID / NFC / IR companion | Flipper Zero + ESP32 WiFi board | [02-flipper-zero](../../02-flipper-zero/) |
| 03 | [Pwnagotchi](03-pwnagotchi/) | Docked, runs separate — charge/offload bay | Pi Zero 2 W + e-ink | [03-pwnagotchi](../../03-pwnagotchi/) |
| 04 | [Meshtastic](04-meshtastic/) | Off-grid mesh node | Heltec LoRa V3 | [04-meshtastic](../../04-meshtastic/) |
| 05 | [RayHunter](05-rayhunter/) | Stingray / IMSI-catcher detector (companion) | Orbic Speed RC400L | [05-rayhunter](../../05-rayhunter/) |
| 06 | [Flock & Drone Detection](06-flock-drone-detection/) | ALPR camera + drone RemoteID detection | Gold #2 + WROOM-32 | [06-flock-drone-detection](../../06-flock-drone-detection/) |
| 07 | [Kismet Wardriving](07-kismet-wardriving/) | WiFi mapping / wardriving | Pi 5 + Panda PAU0F + RT5370 | [07-kismet-wardriving](../../07-kismet-wardriving/) |
| 08 | [BLE Detection](08-ble-detection/) | Bluetooth tracker / device detection | Lonely Binary Gold #3 | [08-ble-detection](../../08-ble-detection/) |
| 09 | [Project Nomad](09-project-nomad/) | Offline comms/media (companion, x64 only) | LattePanda / x64 SBC | [09-project-nomad](../../09-project-nomad/) |
| 10 | [Chasing Your Tail](10-chasing-your-tail/) | AirTag/Tile/SmartTag tail detection | Merged on Gold #3 | [10-chasing-your-tail](../../10-chasing-your-tail/) |
| 11 | [NyanBOX](11-nyan-box/) | Pre-built pentest toolkit (companion) | NyanBOX unit | [11-nyan-box](../../11-nyan-box/) |
| 12 | [USB Rubber Ducky](12-usb-rubber-ducky/) | Keystroke injection payload runner | Hak5 Ducky / DIY ESP32 | [12-usb-rubber-ducky](../../12-usb-rubber-ducky/) |
| 13 | [ESP Terminator](13-esp-terminator/) | The web flasher used to flash the deck's ESP32s | espterminator.com | [13-esp-terminator](../../13-esp-terminator/) |

## Hardware Part Guides

The "separate parts" of the deck — the chassis-level subsystems that tie the boards together.

| Guide | What it covers |
|-------|----------------|
| [parts/pi5-brain](parts/pi5-brain/) | The Pi 5 + Kali brain: flash, first boot, serial/USB plumbing |
| [parts/power](parts/power/) | Anker 347 + powered USB hub + 7 per-device toggle switches |
| [parts/cooling](parts/cooling/) | 3-layer sealed cooling (IP67 fans + Noctua + membrane vent) |
| [parts/antennas](parts/antennas/) | 5× IP67 SMA bulkheads + U.FL pigtails + waterproofing |
| [parts/displays](parts/displays/) | 7" DSI + 2× CYD 2.8" + 2.42" OLED + Heltec OLED |
| [parts/gps](parts/gps/) | VK-162 USB GPS shared to all tools via `gpsd` |
| [parts/case-prep](parts/case-prep/) | Pelican 1300 NF drilling, sealing, mounting plates |
| [parts/dashboard](parts/dashboard/) | Flask + SocketIO dashboard in Chromium kiosk mode |

---

## The Master Wiring Decisions (Quick Reference)

These assignments are fixed across every guide so nothing collides.

| Board / device | Deck slot | Power | Antenna | Display |
|----------------|-----------|-------|---------|---------|
| Pi 5 8GB | Brain | Anker 347 USB-C PD (always on) | — | 7" DSI |
| Lonely Binary Gold #1 | Marauder | Hub → switch SW1 | SMA #1 (2.4/5.8 GHz) | CYD #1 |
| Lonely Binary Gold #2 | Flock | Hub → switch SW2 | SMA #2 (2.4 GHz) | CYD #2 |
| Lonely Binary Gold #3 | BLE + Chasing Your Tail | Hub → switch SW3 | SMA #3 (2.4 GHz) | — |
| Heltec LoRa V3 | Meshtastic | Hub → switch SW4 | SMA #4 (915 MHz) | onboard 0.96" |
| ESP32-WROOM-32 | Drone RemoteID | Hub → switch SW5 | internal PCB | CYD #2 (shared) |
| Panda PAU0F | Kismet primary | Pi 5 USB 3.0 (direct, always on) | SMA #5 (built-in) | — |
| RT5370 | Kismet secondary | Hub → switch SW6 | internal | — |
| VK-162 GPS | Shared GPS | Hub → switch SW7 | internal | — |

All ESP32 serial links run at **115200 baud** over USB to the Pi 5.

---

*Living document — keep this index in sync as guides are added or assignments change.*
