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
| 01 | [ESP32 Marauder](01-esp32-marauder/) | Primary WiFi/BLE offensive tool | Lonely Binary Gold #1 (classic ESP32) — **built**, standalone in Heltec V4 case + CYD #1 complete | [01-esp32-marauder](../../01-esp32-marauder/) |
| 02 | [Flipper Zero](02-flipper-zero/) | Sub-GHz / RFID / NFC / IR companion | Flipper Zero + ESP32 WiFi board | [02-flipper-zero](../../02-flipper-zero/) |
| 03 | [Pwnagotchi](03-pwnagotchi/) | Docked, runs separate — charge/offload bay | Pi Zero 2 W + e-ink | [03-pwnagotchi](../../03-pwnagotchi/) |
| 04 | [Meshtastic](04-meshtastic/) | Off-grid mesh node | Heltec LoRa V3 | [04-meshtastic](../../04-meshtastic/) |
| 05 | [RayHunter](05-rayhunter/) | **IMSI catcher / stingray detector (deck-integrated)** | Orbic Speed RC400L (USB-C → Pi 5 ADB) | [05-rayhunter](../../05-rayhunter/) |
| 06 | [Flock & Drone Detection](06-flock-drone-detection/) | ALPR camera + drone RemoteID detection | Gold #2 + WROOM-32 | [06-flock-drone-detection](../../06-flock-drone-detection/) |
| 07 | [Kismet Wardriving](07-kismet-wardriving/) | WiFi mapping / wardriving | Pi 5 + Panda PAU0F + RT5370 | [07-kismet-wardriving](../../07-kismet-wardriving/) |
| 08 | [BLE Detection](08-ble-detection/) | Bluetooth tracker / device detection | Lonely Binary Gold #3 | [08-ble-detection](../../08-ble-detection/) |
| 09 | [Project Nomad](09-project-nomad/) | Offline comms/media (companion, x64 only) | LattePanda / x64 SBC | [09-project-nomad](../../09-project-nomad/) |
| 10 | [Chasing Your Tail](10-chasing-your-tail/) | AirTag/Tile/SmartTag tail detection | Merged on Gold #3 | [10-chasing-your-tail](../../10-chasing-your-tail/) |
| 11 | [NyanBOX](11-nyan-box/) | Pre-built pentest toolkit (companion) | NyanBOX unit | [11-nyan-box](../../11-nyan-box/) |
| 12 | [USB Rubber Ducky](12-usb-rubber-ducky/) | Keystroke injection payload runner | Hak5 Ducky / DIY ESP32 | [12-usb-rubber-ducky](../../12-usb-rubber-ducky/) |
| 13 | [ESP Terminator](13-esp-terminator/) | The web flasher used to flash the deck's ESP32s | espterminator.com | [13-esp-terminator](../../13-esp-terminator/) |
| 15 | [ESP32-DIV](15-esp32-div/) | Sub-GHz / IR / RFID-NFC / 2.4GHz multitool (companion) | ESP32-DIV (CC1101 + NRF24) | [15-esp32-div](../../15-esp32-div/) |
| 16 | [RF Interference Detection](16-bluejammer/) | Lawful detector side of BlueJammer — **no jammer** | nRF24L01+ (RX-only) | [16-bluejammer](../../16-bluejammer/) |
| 18 | [HaleHound + IoT Recon](18-halehound/) | Multi-protocol attack station + IoT credential harvester | CYD #2 (HaleHound firmware) | [18-halehound](../../18-halehound/) |
| 19 | [RaspyJack](19-raspyjack/) | Wired network pentesting + Linux recon (Shark Jack alt) | Pi Zero 2 W + 1.44" LCD HAT | [19-raspyjack](../../19-raspyjack/) |

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
| Lonely Binary Gold #1 | Marauder (2.4GHz, CYD touchscreen) | Hub → switch SW1 | SMA #1 (2.4 GHz) | CYD #1 (Marauder) |
| Lonely Binary Gold #2 | Flock detection | Hub → switch SW2 | SMA #2 (2.4 GHz) | — (Pi 5 dashboard) |
| Lonely Binary Gold #3 | BLE + Chasing Your Tail | Hub → switch SW3 | SMA #3 (2.4 GHz) | — |
| **Waveshare ESP32-C5 #1** | **Dual-band Marauder (2.4+5GHz)** | Hub → switch SW4 | **SMA #4 (dual-band 2.4/5GHz)** | — (headless, Pi 5 GUI) |
| **Waveshare ESP32-C5 #2** | **Dual-band scanner/wardriving** | Hub → switch SW5 | **SMA #5 (dual-band 2.4/5GHz)** | — (headless, Pi 5 GUI) |
| Heltec LoRa V3 | Meshtastic | Hub → switch SW6 | SMA #6 (915 MHz) | onboard 0.96" |
| ESP32-WROOM-32 | Drone RemoteID | Hub → switch SW7 | internal PCB | — |
| CYD #2 | **HaleHound (IoT Recon + multi-protocol)** | Hub → switch SW8 | internal PCB (2.4 GHz) | built-in 2.8" touch |
| Pi Zero 2 W | **RaspyJack (wired network attacks)** | Hub → switch SW9 | internal | 1.44" LCD HAT |
| Panda PAU0F | Kismet primary (WiFi 6E) | Pi 5 USB 3.0 (direct, always on) | SMA #7 (built-in) | — |
| RT5370 | Kismet secondary | Hub → switch SW10 | internal | — |
| VK-162 GPS | Shared GPS | Hub → switch SW11 | internal | — |
| **Orbic RC400L** | **RayHunter IMSI/stingray detector** | Hub → switch SW12 | internal (cellular) | — (Pi 5 via ADB forward) |

### RayHunter Integration Notes

The **Orbic Speed RC400L** runs [RayHunter](https://github.com/EFForg/rayhunter) (EFF's IMSI catcher detector) and connects to the Pi 5 via **ADB over USB-C**. The Pi forwards port 8080 (`adb forward tcp:8080 tcp:8080`) and polls the RayHunter REST API at `http://localhost:8080/api/analysis` for real-time stingray alerts.

- **Autoboot mod:** Patch aboot partition (change byte `0x20` → `0xff` at sequence `03 02 00 0a 20`) so Orbic starts automatically with the deck
- **SIM required:** Any deactivated SIM card works — no active plan needed
- **Battery stays in:** The Orbic won't boot without its battery present; USB keeps it charged
- **No external antenna:** Internal cellular antenna only — position near case wall for best signal
- **Power draw:** ~3-5W (600mA typical, 1A peak)
- **Dashboard:** Flask app polls `/api/analysis` every 5s, displays alert level (green/yellow/orange/red)

### Dual-Band Upgrade Notes

The **ESP32-C5 boards** are the dual-band backbone of the deck. They run Marauder firmware with full 2.4GHz AND 5GHz WiFi 6 capability — packet injection, monitor mode, deauth, beacon spam, evil twin, wardriving on BOTH bands. Controlled headless from the Pi 5 via the [headless-marauder-gui](https://github.com/LxveAce/headless-marauder-gui).

- **C5 #1** runs dual-band Marauder — the primary 5GHz attack platform
- **C5 #2** runs dual-band scanning/wardriving — passive monitoring on 5GHz networks
- Both use **IPEX antenna connectors** → U.FL pigtails → SMA bulkheads → **Bingfu dual-band antennas** (2.4/5.8GHz, already in inventory)
- Classic ESP32 Gold boards remain for 2.4GHz CYD-integrated tasks (Marauder touchscreen, Flock, BLE)
- The C5 **cannot use both bands simultaneously** (single radio, band-switching) but covers the full 2.4+5GHz spectrum

### SMA Bulkhead Layout (7 total)

```
─── CASE SIDE PANEL ────────────────────────────────
[SMA1]  [SMA2]  [SMA3]  [SMA4]  [SMA5]  [SMA6]  [SMA7]
Gold#1  Gold#2  Gold#3  C5 #1   C5 #2   LoRa    PAU0F
2.4GHz  2.4GHz  2.4GHz  DUAL    DUAL    915MHz  6E
────────────────────────────────────────────────────
```

All ESP32 serial links run at **115200 baud** over USB to the Pi 5.

---

*Living document — keep this index in sync as guides are added or assignments change.*
