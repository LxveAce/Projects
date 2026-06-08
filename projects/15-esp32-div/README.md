# Project 15: ESP32-DIV — Open-Source Multi-Band Wireless Toolkit

> **Status:** Evaluating / To Build
> **Upstream:** [cifertech/esp32-div](https://github.com/cifertech/esp32-div) (MIT) · [cifertech.net](https://cifertech.net)
> **What it is:** A handheld, touchscreen ESP32-S3 multitool that puts Wi-Fi, Bluetooth, 2.4 GHz,
> Sub-GHz, IR, and RFID/NFC on one board — think "open-source DIY Flipper + Marauder."

---

## 1. Overview

ESP32-DIV (a.k.a. "ESP32 Diagnostic") is an open-source, MIT-licensed handheld built on the
**ESP32-S3** with a 2.8" touchscreen and a stackable RF **shield**. Where the [Marauder](../01-esp32-marauder/)
covers Wi-Fi/BLE, ESP32-DIV reaches into **Sub-GHz (CC1101)**, **2.4 GHz raw (3× NRF24)**,
**IR**, and **RFID/NFC** as well — much of the same ground a Flipper Zero covers, but DIY and ESP32-native.

It is the natural companion to the existing kit: it fills the deck's **non-WiFi/BLE** gaps with one
open-source device. (See the [cyberdeck integration](../14-cyberdeck/integrations/15-esp32-div/).)

---

## 2. Hardware

**Main board**
- ESP32-S3 MCU
- ILI9341 **2.8" TFT** display (touch UI)
- IP5306 battery management (LiPo)
- CP2102 USB-to-serial
- PCF8574 I/O expander
- microSD slot, WS2812 NeoPixels, buzzer, push buttons, antenna connector

**RF shield**
- **3× NRF24L01** modules (2.4 GHz)
- **1× CC1101** module (Sub-GHz: 315/433/868/915 MHz)
- **IR transceiver** (TX + RX)
- Multiple antennas

Build options: assemble the open-hardware PCB + shield (Gerbers/BOM in the repo), or source a
pre-made ESP32-DIV board. Many parts (ESP32-S3, NRF24, displays) overlap what's already in [INVENTORY.md](../../INVENTORY.md).

---

## 3. Features

Tagged by what they do. **"Deck status"** shows how each maps to the existing kit.

| Group | Feature | Type | Deck status |
|-------|---------|------|-------------|
| **Wi-Fi** | Wi-Fi Scanner, Packet Monitor | scan / analyze | duplicate of Marauder/Kismet |
| | Beacon Spammer, Deauth Attack, Captive Portal, Probe Flood | attack | duplicate of Marauder |
| | **Deauth Detector** | detect | useful (matches Marauder `sniffdeauth`) |
| **Bluetooth** | BLE Scanner, BLE Sniffer, BLE Spoofer, Sour Apple, BLE Rubber Ducky | scan/sniff/attack | duplicate of Marauder |
| | BLE Jammer | **jam** | ⛔ illegal to operate — not used |
| **2.4 GHz** | **2.4GHz Scanner** | analyze | ✅ **new** — NRF24 spectrum/airtime view |
| | Protokill | **jam** | ⛔ illegal to operate — not used |
| **Sub-GHz** | **Replay Attack**, **Saved Profiles** (CC1101) | attack/analyze | ✅ **new** to deck (Flipper-class) |
| | Sub-GHz Jammer | **jam** | ⛔ illegal to operate — not used |
| **IR** | **IR Replay**, **Universal IR Controller**, Saved Profiles | attack/analyze | ✅ **new** to deck |
| **RFID/NFC** | **Card Reader, Clone, Dump, Decode, Erase** | scan/attack/analyze | ✅ **new** to deck (Flipper-class) |
| | Jam Reader, Tag Disrupt, Disrupt Emulate | **jam** | ⛔ not used |
| **GPS** | Wardriver, Satellite Scanner | scan/log | overlaps Kismet wardriving |

**Genuinely new vs. the current kit:** 2.4 GHz NRF24 spectrum scanning, CC1101 Sub-GHz
(scan/replay/profiles), IR (replay + universal remote), and RFID/NFC (read/clone). These overlap a
**Flipper Zero** (project 02) — ESP32-DIV is the open-source DIY route to the same coverage, plus
the integrated NRF24 2.4 GHz analyzer the Flipper lacks.

---

## 4. Build & flash

1. Build/obtain the ESP32-DIV main board + RF shield (open hardware in the repo).
2. Flash the firmware: grab a release from the [repo](https://github.com/cifertech/esp32-div),
   or build from source (Arduino/PlatformIO, ESP32-S3 target). The device also supports
   **"Update Firmware" from the microSD card**.
3. Insert a FAT32 microSD (for captures, saved Sub-GHz/IR profiles, wardrive logs).

Flashing the bare ESP32-S3 follows the same pattern as the rest of the kit — see
[ESP Terminator](../13-esp-terminator/) / the [headless-marauder-gui flasher](../14-cyberdeck/integrations/01-esp32-marauder/headless-marauder-gui/).

---

## 5. Legal

For **authorized testing / your own devices only**. Two specific cautions:
- **The "jam" features (BLE Jammer, Protokill, Sub-GHz Jammer, RFID Jam/Disrupt) are illegal to
  operate** — operating any RF jammer violates US 47 U.S.C. §333 + the FCC ban (no exception, even
  on your own property). This kit **does not use them**. See [project 16](../16-bluejammer/) for the
  fuller jamming legal note.
- Sub-GHz replay, RFID clone, deauth, and captive portal are powerful — only against systems you
  own or are authorized to test (US CFAA, FCC, and equivalents).

---

## 6. Resources

- Repo: https://github.com/cifertech/esp32-div · Site: https://cifertech.net
- Cyberdeck integration: [14-cyberdeck/integrations/15-esp32-div](../14-cyberdeck/integrations/15-esp32-div/)
- Related: [Flipper Zero](../02-flipper-zero/) (same Sub-GHz/RFID/NFC/IR coverage), [Marauder](../01-esp32-marauder/) (WiFi/BLE)
