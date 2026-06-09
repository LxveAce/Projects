# OUI-Spy — Passive Wireless Surveillance Detection Platform

---

## Table of Contents

1. [Overview](#1-overview)
2. [How OUI Detection Works](#2-how-oui-detection-works)
3. [All Firmware Modes — Complete Feature Matrix](#3-all-firmware-modes----complete-feature-matrix)
4. [Compatible Hardware — All Boards & Displays](#4-compatible-hardware----all-boards--displays)
5. [Complete Parts List with Prices](#5-complete-parts-list-with-prices)
6. [Display Options — Adding a Screen](#6-display-options----adding-a-screen)
7. [Pin Connections & Wiring](#7-pin-connections--wiring)
8. [Step-by-Step Build Guide](#8-step-by-step-build-guide)
9. [Firmware Flashing — All Methods](#9-firmware-flashing----all-methods)
10. [OUI Database — Sources & Management](#10-oui-database----sources--management)
11. [3D Printed Cases](#11-3d-printed-cases)
12. [Companion Software & Apps](#12-companion-software--apps)
13. [Troubleshooting](#13-troubleshooting)
14. [Legal Considerations](#14-legal-considerations)
15. [All Resource Links](#15-all-resource-links)

---

## 1. Overview

OUI-Spy is an open-source passive wireless detection platform built on the ESP32-S3 microcontroller. It scans WiFi and Bluetooth traffic to identify nearby devices by their OUI (Organizationally Unique Identifier) — the first three bytes of a MAC address that reveal the device manufacturer. It detects surveillance cameras, drones, tracking devices, and any wireless hardware you configure it to watch for. Nothing is transmitted or exploited; it only listens.

**Creator:** colonelpanichacks (Colonel Panic) · [colonelpanic.tech](https://colonelpanic.tech/) · [GitHub](https://github.com/colonelpanichacks)

**Key Fork:** Luke Switzer's OUI-SPY Omni — concurrent multi-engine variant with Flutter companion app · [GitHub](https://github.com/lukeswitz/oui-spy-unified-blue)

**Stats (June 2026):** Ecosystem spans 8+ firmware repos, custom PCB available, active community. Codebase: C++ (~80%), C (~17%), Python (~3%).

**Philosophy:**
- **Blue Edition = Passive only.** No transmissions, no exploitation, no active attacks
- **Multi-mode in one firmware.** Switch detection modes from a web menu — no reflashing
- **Privacy-first.** MAC address randomized on every boot, all processing local, no cloud

**Related project in this repo:** [Flock & Drone Detection (Project 06)](../06-flock-drone-detection/) covers the Flock-You and Sky Spy modes in depth with legal analysis and detection research. This guide covers the full OUI-Spy platform including all modes, hardware builds, and display integration.

---

## 2. How OUI Detection Works

### What is an OUI?

Every network device (WiFi, Bluetooth, Ethernet) has a MAC address — a 48-bit hardware identifier formatted as six hex pairs: `70:C9:4E:12:34:56`. The first three bytes (`70:C9:4E`) are the **OUI** — a prefix assigned by IEEE to the manufacturer. The remaining three bytes are device-specific.

The IEEE maintains a public registry of 88,000+ OUI assignments. By matching the first three bytes of any detected MAC address against this database, you can instantly identify the manufacturer: Ring, Flock Safety, DJI, Apple, etc.

### Detection Methods Used by OUI-Spy

**1. BLE Advertisement Scanning**
- Listens for Bluetooth Low Energy advertisements broadcast by nearby devices
- Extracts MAC address → matches OUI prefix against target list
- Also matches device name patterns (`FS Ext Battery`, `Penguin`, `Flock`, `Pigvision`)
- Also matches manufacturer company IDs (e.g., `0x09C8` = XUNTONG, used by Flock batteries)
- Range: 10-30m typical, up to 100m+ with directional antenna

**2. WiFi Promiscuous Mode (Packet Sniffing)**
- ESP32 enters promiscuous mode to capture all WiFi frames on the current channel
- Parses management frames (beacons, probe requests/responses) for source MACs
- Three detection methods per frame:
  - **Wildcard probe** — probe request with wildcard SSID from known OUI (highest precision)
  - **addr2 match** — transmitter MAC OUI match
  - **addr1 match** — receiver MAC OUI match (catches sleeping devices responding to polls)
- Channel hopping across 1/6/11 (350ms dwell per channel)

**3. OpenDroneID / Remote ID Parsing**
- Drones broadcast FAA-mandated Remote ID via WiFi beacons and BLE advertisements
- OUI-Spy decodes ASTM F3411 protocol to extract serial number, GPS, altitude, speed, heading, and operator location
- Dual-protocol scanning: WiFi promiscuous for beacon frames + BLE for ODID advertisements

**4. RSSI Proximity Tracking (Foxhunter)**
- Locks onto a single target MAC and monitors signal strength in real-time
- Seven intensity tiers from "machine gun" (10-25ms beep, -35 to -25 dBm) to "painfully slow" (800ms beep, -85+ dBm)
- Designed for directional antenna use — walk toward the signal to locate the device

### MAC Randomization Awareness

Modern smartphones (iOS 14+, Android 10+, Windows 10+) randomize MAC addresses in probe requests. Randomized MACs have the locally administered bit set (second-least-significant bit of the first octet = 1). OUI-Spy filters these out when looking for infrastructure devices like Flock cameras, which use their real manufacturer OUI because they're embedded IoT devices — not privacy-conscious smartphones.

---

## 3. All Firmware Modes — Complete Feature Matrix

### 3A. OUI-SPY Unified Blue (Recommended — All-in-One)

The flagship firmware. Four detection modes selectable via web portal at boot — no reflashing to switch.

**Boot sequence:** Power on → creates WiFi AP `oui-spy` / `ouispy123` → browse to `192.168.4.1` → select mode → device reboots into that mode. Hold BOOT button 2 seconds to return to mode selector.

#### Mode 1: Detector — Multi-Target BLE Surveillance Scanner

| Feature | Details |
|---------|---------|
| **Scan method** | BLE advertisements, 16ms scan interval, 95% duty cycle |
| **Targets** | OUI prefix, full MAC address, device name pattern — configurable via web |
| **Range** | 10-30m typical |
| **Storage** | Up to 100 device aliases in NVS flash |
| **Alerts** | Buzzer beep + NeoPixel flash (pink breathing → blue/pink/purple sequence) |
| **Web portal** | AP: `snoopuntothem` / `astheysnoopuntous` at `192.168.4.1` |
| **MQTT** | Home Assistant auto-discovery integration (optional) |
| **Burn-in mode** | Locks configuration permanently — deploy and forget |

Pre-loaded with 31 Flock OUI prefixes + 11 Ring/doorbell OUIs. Add custom targets via web portal.

#### Mode 2: Foxhunter — Single-Target RSSI Radio Direction Finder

| Feature | Details |
|---------|---------|
| **Scan method** | BLE active scan, 16ms interval, 95% duty |
| **Target** | Single MAC entered via web portal |
| **Proximity tiers** | 7 levels from INSANE SPEED (10-25ms, -35 to -25 dBm) to PAINFULLY SLOW (800ms, -85+ dBm) |
| **Feedback** | Buzzer cadence + LED flash synchronized — faster = closer |
| **Best with** | 2.4GHz Yagi directional antenna (10.5 dBi) for directional tracking |
| **Web portal** | AP: `foxhunter` / `foxhunter` at `192.168.4.1` |

Walk toward the signal. Beeping gets faster as you approach the target.

#### Mode 3: Flock-You — Flock Safety & Raven Surveillance Detector

| Feature | Details |
|---------|---------|
| **Scan methods** | WiFi promiscuous mode + BLE scanning |
| **Detection layers** | 31 Flock OUI prefixes, BLE device names, manufacturer ID `0x09C8`, Raven service UUIDs, wildcard WiFi probes |
| **Channel hop** | Channels 1/6/11, 350ms dwell |
| **GPS** | Via phone browser Geolocation API |
| **Storage** | 200 unique detections with timestamps (SPIFFS, CRC-32 atomic writes) |
| **Export** | JSON, CSV, KML (Google Earth) |
| **Web portal** | AP: `flockyou` / `flockyou123` at `192.168.4.1` |
| **Dashboard** | Flask desktop companion app included |

> See [Project 06 — Flock & Drone Detection](../06-flock-drone-detection/) for the full Flock legal analysis, all 31 OUI prefixes, and detection research.

#### Mode 4: Sky Spy — FAA Remote ID Drone Detector

| Feature | Details |
|---------|---------|
| **Scan methods** | WiFi promiscuous (beacon frames) + BLE (OpenDroneID advertisements) |
| **Protocol** | ASTM F3411 Remote ID |
| **Data extracted** | Serial/registration, GPS (lat/lon/alt), speed, heading, operator location |
| **Multi-drone** | Tracks multiple drones simultaneously |
| **Alerts** | 3 quick beeps on detection + heartbeat every 5 seconds |
| **Output** | JSON serial for mesh-mapper.py visualization |
| **No AP** | Passive only, no web portal |

### 3B. OUI-SPY Omni — Luke Switzer's Advanced Fork

Runs **7-8 detection engines concurrently** — no reboot to switch. Controlled via **Flutter companion app** over BLE.

| Engine | Description |
|--------|-------------|
| **Detector** | Watchlist matching (MAC, OUI, name, UUID) |
| **Flock WiFi** | Promiscuous WiFi detection for Flock cameras |
| **Flock BLE** | BLE-only Flock detection |
| **Foxhunter** | RSSI proximity tracking |
| **Sky Spy** | Drone Remote ID |
| **UniPwn** | Unitree robot detection (authorized research only) |
| **Wardrive** | WiGLE-style WiFi logging with GPS |
| **PCAP** | Raw 802.11 frames to phone (Wireshark compatible) |

**App features:** Live detection feed with engine-colored rows, real-time wardrive map with geofence exclusion zones, 39,000+ OUI vendor database, WiGLE CSV export + direct API upload, per-engine configuration, iOS Dynamic Island notifications.

**Swarm mode (experimental):** ESP-NOW mesh networking with AES-GCM encryption, up to 6 peer nodes.

### 3C. Standalone Firmwares (Individual Repos)

For flashing a single mode without the Unified Blue boot selector:

| Firmware | Repo | Notes |
|----------|------|-------|
| Detector | [ouispy-detector](https://github.com/colonelpanichacks/ouispy-detector) | Standalone BLE scanner, MQTT, burn-in mode |
| Foxhunter | [ouispy-foxhunter](https://github.com/colonelpanichacks/ouispy-foxhunter) | Standalone RSSI tracker |
| Flock-You | [flock-you](https://github.com/colonelpanichacks/flock-you) (`promiscious-dev` branch) | WiFi promiscuous + Flask dashboard |
| Sky Spy | [Sky-Spy](https://github.com/colonelpanichacks/Sky-Spy) | Drone Remote ID only |
| UniPwn | [Oui-Spy-UniPwn](https://github.com/colonelpanichacks/Oui-Spy-UniPwn) | Unitree robot exploitation (authorized research only) |
| Remote-ID-Spoofer | [Remote-ID-Spoofer](https://github.com/colonelpanichacks/Remote-ID-Spoofer) | **Red Edition** — transmit-based. Illegal in most jurisdictions. Research only |

### 3D. Feature Matrix — All Firmwares Compared

| Feature | Unified Blue | Omni | Detector | Foxhunter | Flock-You | Sky Spy |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| BLE scanning | Yes | Yes | Yes | Yes | Yes | Yes |
| WiFi promiscuous | Yes (Flock/Sky) | Yes | No | No | Yes | Yes |
| Multi-target | Yes | Yes | Yes | No (single) | Yes | Yes |
| RSSI proximity | Foxhunter mode | Yes | No | Yes | No | No |
| GPS wardriving | Flock mode | Yes | No | No | Yes | No |
| Web portal | Yes | Yes | Yes | Yes | Yes | No |
| Flutter app | No | Yes | No | No | No | No |
| MQTT / Home Assistant | Detector mode | No | Yes | No | No | No |
| Export (JSON/CSV/KML) | Flock mode | Yes | Yes | No | Yes | Yes (JSON) |
| PCAP output | No | Yes | No | No | No | No |
| Swarm/mesh | No | Experimental | No | No | No | No |
| Session persistence | Yes (NVS/SPIFFS) | Yes | Yes (NVS) | Yes (NVS) | Yes (SPIFFS) | RAM only |
| Mode switching | Web boot menu | App toggle | N/A | N/A | N/A | N/A |

---

## 4. Compatible Hardware — All Boards & Displays

### 4A. ESP32 Chip Variants — Capability Comparison

| Feature | ESP32 (classic) | ESP32-S2 | ESP32-S3 | ESP32-C3 | ESP32-C5 | ESP32-C6 |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| CPU | LX6 dual-core | LX7 single | LX7 dual | RISC-V single | RISC-V single | RISC-V single |
| Clock | 240 MHz | 240 MHz | 240 MHz | 160 MHz | 240 MHz | 160 MHz |
| WiFi | 2.4 GHz | 2.4 GHz | 2.4 GHz | 2.4 GHz | 2.4 + 5 GHz | 2.4 GHz |
| Bluetooth | Classic + BLE 4.2 | **None** | **BLE 5.0** | BLE 5.0 | **None** | BLE 5.3 |
| Promiscuous mode | Yes | Yes | Yes | Yes | Yes | Yes |
| BLE scanning | Yes (4.2) | **No** | **Yes (5.0)** | Yes (5.0) | **No** | Yes (5.3) |
| USB native | No | OTG | OTG | No | No | No |
| PSRAM typical | 0-4 MB | 2-4 MB | **8 MB** | 0 | 0 | 0 |
| OUI-Spy support | WiFi-only modes | **Not supported** | **Full support** | Partial | WiFi-only | Partial |

> **For the full OUI-Spy experience (all modes including BLE Detector, Foxhunter, and Flock BLE), you need an ESP32-S3.** The classic ESP32 can run WiFi-only modes (Flock-You WiFi, Sky Spy WiFi promiscuous) but lacks BLE 5.0 for the Detector and Foxhunter modes. The ESP32-S2 and ESP32-C5 have no Bluetooth at all.

### 4B. Recommended Dev Boards

#### Tier 1: OUI-Spy Reference Board (Official)

| Board | Chip | Display | Key Features | Price |
|-------|------|---------|-------------|-------|
| **OUI-SPY PCB** (colonelpanic.tech) | ESP32-S3 | NeoPixel LED only | Custom 2-board PCB, integrated piezo (GPIO3), NeoPixel (GPIO21), SMA connector for external antenna, USB-C | $85 assembled / $25 PCBs only |

#### Tier 2: Best for Display Builds (Recommended)

| Board | Chip | Display | Key Features | Price |
|-------|------|---------|-------------|-------|
| **LILYGO T-Display S3** | ESP32-S3R8 (8MB PSRAM, 16MB flash) | **Built-in 1.9" ST7789V TFT (170x320)** | JST battery connector, 2 buttons, STEMMA QT/Qwiic, WiFi + BLE 5.0 | ~$18-25 |
| **Heltec WiFi Kit 32 V3** | ESP32-S3FN8 (8MB flash) | **Built-in 0.96" SSD1306 OLED (128x64)** | LiPo management (charge + protect), Type-C, WiFi + BLE | ~$18-22 |

#### Tier 3: Compact / Reference

| Board | Chip | Display | Key Features | Price |
|-------|------|---------|-------------|-------|
| **Seeed XIAO ESP32-S3** | ESP32-S3R8 (8MB each) | None (add external) | 21x17.5mm, WiFi + BLE 5.0, battery charge area, deep sleep 14uA | ~$8-14 |
| **Seeed XIAO ESP32-C3** | ESP32-C3 (4MB flash) | None | Budget, RISC-V, BLE 5.0, no classic BT | ~$5-7 |
| **Seeed XIAO ESP32-C6** | ESP32-C6 (4MB flash) | None | WiFi 6, BLE 5.3, Thread/Zigbee | ~$7-9 |
| **M5Stack Stamp S3** | ESP32-S3 | None | SK6812 NeoPixel built-in, same as XIAO S3 | ~$8-10 |

#### Tier 4: Classic ESP32 (WiFi-Only Modes)

| Board | Chip | Display | Key Features | Price |
|-------|------|---------|-------------|-------|
| **Lonely Binary ESP32 Gold** | ESP32-WROOM (CH340) | None | IPEX antenna connector, runs Flock-You WiFi + Sky Spy promiscuous. No BLE 5.0 | ~$12/each |
| **ESP32-WROOM-32 Dev Board** | ESP32-WROOM (CP2102) | None | Generic, 38-pin breakout. Same WiFi-only limitation | ~$4-8 |
| **CYD 2.8" Touchscreen** | ESP32 (ILI9341) | **Built-in 2.8" TFT (240x320, touch)** | Has a display but classic ESP32 — WiFi-only OUI scanning. Custom firmware needed | ~$8-10 |
| **AITRIP 4.0" Touchscreen** | ESP32 (ST7796) | **Built-in 4.0" TFT (320x480, touch)** | Same as CYD but larger. WiFi-only limitation applies | ~$15-20 |

### 4C. What You Already Own (From Inventory)

| Board | Chip | OUI-Spy Capability | Notes |
|-------|------|-------------------|-------|
| Lonely Binary Gold #1 | Classic ESP32 | **WiFi-only** (Flock-You WiFi, Sky Spy promiscuous) | Currently assigned to headless Marauder — standalone unit |
| Lonely Binary Gold #2 | Classic ESP32 | **WiFi-only** | Assigned to BLE Detection |
| Lonely Binary Gold #3 | Classic ESP32 | **WiFi-only** | Assigned to Flock/Drone Detection — **best candidate for WiFi-only OUI scanning** |
| ESP32-WROOM-32 | Classic ESP32 | **WiFi-only** | General spare |
| CYD 2.8" #1 | Classic ESP32 | **WiFi-only + built-in display** | Currently running Marauder touchscreen |
| CYD 2.8" #2 | Classic ESP32 | **WiFi-only + built-in display** | Unassigned — could run custom OUI scanning UI |
| AITRIP 4.0" | Classic ESP32 | **WiFi-only + built-in display** | Unassigned |
| ESP32-C5 x2 | ESP32-C5 | **WiFi-only (dual-band 2.4+5GHz)** | No Bluetooth. Could run WiFi promiscuous on 5GHz |
| Waveshare E-Ink 2.13" | N/A (Pi HAT) | Not ESP32-compatible | For Pwnagotchi only |

> **Verdict:** You can start WiFi-only OUI scanning today with Gold #3 or the spare CYD. For the full experience (all modes, BLE 5.0), you need an ESP32-S3 board. Best value: **LILYGO T-Display S3** (~$20) — has a built-in 1.9" color TFT and battery connector, no soldering needed.

---

## 5. Complete Parts List with Prices

### Build A: WiFi-Only Quick Start (~$0 — Use Existing Hardware)

Use what you already have for WiFi promiscuous OUI scanning (Flock-You WiFi + Sky Spy):

| Part | Source | Price |
|------|--------|-------|
| Lonely Binary Gold #3 (or CYD #2) | Already owned | $0 |
| DIYmall 2.4GHz WiFi antenna | Already owned | $0 |
| USB-C cable | Already owned | $0 |
| **Total** | | **$0** |

> Limited to WiFi-only modes. No BLE Detector, no Foxhunter, no BLE Flock detection. No screen unless using CYD (requires custom firmware port).

### Build B: Full-Featured with Display (~$25-35)

The recommended build. ESP32-S3 with built-in screen — all modes, no soldering.

| Part | Source | Price |
|------|--------|-------|
| LILYGO T-Display S3 | [AliExpress](https://lilygo.cc/products/t-display-s3) / Amazon | ~$18-25 |
| Passive piezo buzzer (3.3V, through-hole) | Amazon / electronics kit | ~$1-3 |
| 3.7V LiPo battery (500-1000mAh, JST 1.25mm) | Amazon | ~$5-8 |
| Dupont jumper wires (for buzzer) | Already owned (REXQualis kit) | $0 |
| **Total** | | **~$25-35** |

> Full BLE 5.0 + WiFi promiscuous. All modes work. Built-in 1.9" color TFT. Battery portable. Firmware needs TFT_eSPI display integration (custom build or community port).

### Build C: Compact Reference Build (~$15-25)

The official OUI-Spy hardware path — XIAO S3 with external OLED.

| Part | Source | Price |
|------|--------|-------|
| Seeed XIAO ESP32-S3 | [Seeed Studio](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html) / Amazon | ~$8-14 |
| SSD1306 0.96" OLED (128x64, I2C) | Amazon | ~$3-5 |
| Passive piezo buzzer (3.3V) | Amazon | ~$1-3 |
| WS2812B NeoPixel LED strip (1 pixel) | Amazon | ~$2-4 |
| Mini breadboard or perfboard | Already owned | $0 |
| **Total** | | **~$15-25** |

> All modes. Compact form factor (can fit in 3D-printed case). OLED shows detection status. Buzzer + LED for alerts. Requires custom firmware with SSD1306 display driver.

### Build D: Official OUI-SPY Board (~$85-95)

Buy the ready-made board from Colonel Panic's store.

| Part | Source | Price |
|------|--------|-------|
| OUI-SPY assembled board | [colonelpanic.tech](https://colonelpanic.tech/) / Tindie | ~$85 |
| SSD1306 0.96" OLED (optional screen add-on) | Amazon | ~$3-5 |
| 2.4GHz directional Yagi antenna (10.5dBi SMA) | Amazon | ~$8-12 |
| **Total** | | **~$85-95** |

> Pre-built, tested, ready to flash. Custom PCB art. Integrated piezo + NeoPixel + SMA antenna connector. Add OLED via I2C for visual output.

### Build E: Omni Advanced Build (~$15-30 + phone)

Luke Switzer's concurrent multi-engine build with Flutter app.

| Part | Source | Price |
|------|--------|-------|
| Seeed XIAO ESP32-S3 | Seeed Studio / Amazon | ~$8-14 |
| Passive piezo buzzer | Amazon | ~$1-3 |
| GPS module (optional, for wardriving) | Amazon | ~$10-15 |
| Phone (iOS/Android) for Flutter companion app | Already owned | $0 |
| **Total** | | **~$15-30** |

> 7-8 engines running simultaneously. Phone IS the display. Real-time wardrive map, geofence exclusion, 39K+ OUI database on phone. WiGLE export.

---

## 6. Display Options — Adding a Screen

OUI-Spy's official firmware uses NeoPixel LED + web dashboard + serial output. No physical screen in the reference design. Here's how to add one.

### Option 1: OLED (I2C) — Compact, Low Power

**SSD1306 0.96" (128x64)**
- Interface: I2C (2 wires + power)
- Library: `Adafruit_SSD1306` + `Adafruit_GFX`, or `U8g2`
- Power: 3.3V, ~20mA active
- Best for: Compact builds, status display (target count, last detection, RSSI, mode)
- Wiring: SDA → any GPIO, SCL → any GPIO (software I2C on ESP32)

**SH1106 1.3" (128x64)**
- Same as SSD1306 but slightly larger, better viewing angle
- Library: `Adafruit_SH110X` or `U8g2` (recommended — native SH1106 support, lower RAM)
- Same wiring as SSD1306

### Option 2: TFT (SPI) — Color, Rich UI

**ST7789 1.9" (170x320) — Built into T-Display S3**
- No external wiring needed (parallel bus on T-Display)
- Library: `TFT_eSPI` by Bodmer (ESP32-optimized)
- Full color, fast refresh, good for live detection feeds
- Power: ~40-60mA with backlight

**ILI9341 2.8" (240x320) — Built into CYD**
- No external wiring (built-in)
- Library: `TFT_eSPI`
- Touch support via XPT2046
- Limited to classic ESP32 WiFi-only modes

**ST7796 4.0" (320x480) — Built into AITRIP**
- No external wiring (built-in)
- Library: `TFT_eSPI`
- Largest option, best readability
- Same classic ESP32 limitation

### Option 3: E-Ink — Ultra Low Power, Outdoor Readable

**Not recommended for OUI-Spy.** Refresh rate is too slow (2-15 seconds) for real-time detection alerts. Good for wardriving logs where data is written infrequently, but defeats the purpose of live scanning.

### Option 4: Phone as Display (Omni Build)

Luke Switzer's Flutter companion app turns your phone into the display:
- iOS / Android / macOS
- BLE connection to ESP32
- Live detection feed, real-time map, per-engine configuration
- No hardware display needed — phone IS the screen

### Display Integration Summary

| Display | Size | Interface | Color | Touch | Power | Best For |
|---------|------|-----------|-------|-------|-------|----------|
| SSD1306 OLED | 0.96" | I2C | Mono | No | 20mA | Compact, status readout |
| SH1106 OLED | 1.3" | I2C | Mono | No | 25mA | Compact, better visibility |
| ST7789 TFT (T-Display S3) | 1.9" | Parallel | Full | No | 50mA | Best all-in-one ESP32-S3 build |
| ILI9341 TFT (CYD) | 2.8" | SPI | Full | Yes | 60mA | WiFi-only with touch UI |
| ST7796 TFT (AITRIP) | 4.0" | SPI | Full | Yes | 80mA | WiFi-only, max screen size |
| Phone (Flutter app) | Any | BLE | Full | Yes | 0mA | Omni build, no extra hardware |

---

## 7. Pin Connections & Wiring

### 7A. XIAO ESP32-S3 (Reference Design)

| Function | GPIO | Notes |
|----------|------|-------|
| Piezo buzzer (+) | GPIO3 (D2) | PWM signal (passive buzzer). GND to buzzer (-) |
| NeoPixel LED (DIN) | GPIO4 (D3) or GPIO21 | WS2812B data in. 3.3V to VCC, GND to GND |
| BOOT button | GPIO0 | Hold 2s → return to mode selector |
| Onboard LED | GPIO21 | Active LOW (logic 0 = LED on) |
| I2C SDA (for OLED) | GPIO5 (D4) | Software-configurable to any GPIO |
| I2C SCL (for OLED) | GPIO6 (D5) | Software-configurable to any GPIO |
| Serial TX (GPS) | GPIO43 | Optional UART for GPS module input |
| Serial RX (GPS) | GPIO44 | Optional |
| USB CDC | Built-in | 115200 baud, no external adapter needed |

### 7B. LILYGO T-Display S3

| Function | GPIO | Notes |
|----------|------|-------|
| Built-in TFT | Parallel bus (pre-wired) | ST7789V 170x320, no external wiring |
| Button 1 | GPIO0 | Left button |
| Button 2 | GPIO14 | Right button |
| Piezo buzzer (+) | GPIO43 or any free GPIO | Wire externally |
| NeoPixel LED (DIN) | GPIO18 or any free GPIO | Wire externally |
| Battery | JST-GH 1.25mm 2-pin | 3.7V LiPo, charging via USB-C |
| I2C SDA (STEMMA QT) | GPIO43 | For additional I2C devices |
| I2C SCL (STEMMA QT) | GPIO44 | For additional I2C devices |

### 7C. Classic ESP32 (Lonely Binary Gold / WROOM-32)

| Function | GPIO | Notes |
|----------|------|-------|
| I2C SDA (OLED) | GPIO21 | Default I2C data |
| I2C SCL (OLED) | GPIO22 | Default I2C clock |
| Piezo buzzer (+) | GPIO2 or GPIO5 | Pick any free output GPIO |
| NeoPixel LED (DIN) | GPIO4 or GPIO15 | Pick any free output GPIO |
| IPEX antenna | External connector | Lonely Binary Gold has IPEX for external antenna |

### 7D. Wiring Diagrams

**XIAO S3 + OLED + Buzzer + NeoPixel (Build C):**

```
XIAO ESP32-S3          SSD1306 OLED
───────────────         ─────────────
3.3V ──────────────────→ VCC
GND  ──────────────────→ GND
GPIO5 (D4) ────────────→ SDA
GPIO6 (D5) ────────────→ SCL

XIAO ESP32-S3          Piezo Buzzer
───────────────         ────────────
GPIO3 (D2) ────────────→ (+)
GND  ──────────────────→ (-)

XIAO ESP32-S3          WS2812B NeoPixel
───────────────         ────────────────
GPIO4 (D3) ────────────→ DIN
3.3V ──────────────────→ VCC
GND  ──────────────────→ GND
```

**T-Display S3 + Buzzer (Build B):**

```
T-Display S3            Piezo Buzzer
────────────────        ────────────
GPIO43 (or free) ──────→ (+)
GND  ──────────────────→ (-)

T-Display S3            LiPo Battery
────────────────        ────────────
JST 1.25mm connector ──→ 3.7V LiPo (500-1000mAh)
                         (polarity marked on board)
```

---

## 8. Step-by-Step Build Guide

### Build B: T-Display S3 Full-Featured (Recommended)

#### Step 1: Gather Parts

- LILYGO T-Display S3
- Passive piezo buzzer (3.3V compatible, through-hole)
- 3.7V LiPo battery with JST-SH 1.25mm 2-pin connector
- 2x Dupont jumper wires (female-to-bare or solder direct)
- USB-C data cable (not charge-only)

#### Step 2: Connect the Buzzer

1. Identify a free GPIO on the T-Display S3 (GPIO43, GPIO18, or any unused pin on the header)
2. Connect buzzer (+) to your chosen GPIO via jumper wire
3. Connect buzzer (-) to GND
4. Optional: add a 100-ohm resistor in series for volume control

#### Step 3: Connect Battery (Optional)

1. Plug the JST 1.25mm battery connector into the battery port on the T-Display S3
2. Check polarity — positive on the left when USB-C faces up (verify against board silkscreen)
3. The T-Display S3 handles charging automatically via USB-C when plugged in

#### Step 4: Flash Firmware

See [Section 9: Firmware Flashing](#9-firmware-flashing----all-methods) for detailed instructions.

#### Step 5: Verify

1. Power on via USB-C
2. Connect to WiFi AP `oui-spy` / `ouispy123` on your phone
3. Browse to `192.168.4.1`
4. You should see the mode selector (Detector / Foxhunter / Flock-You / Sky Spy)
5. Select Detector — device reboots
6. Connect to AP `snoopuntothem` / `astheysnoopuntous`
7. Browse to `192.168.4.1` — you should see the Detector web interface
8. Buzzer should beep 4 ascending tones on successful boot

### Build C: XIAO S3 + OLED Compact Build

#### Step 1: Gather Parts

- Seeed XIAO ESP32-S3
- SSD1306 0.96" OLED module (I2C, 4-pin: VCC/GND/SDA/SCL)
- Passive piezo buzzer
- WS2812B NeoPixel (single pixel module or cut from strip)
- Mini breadboard or perfboard
- Jumper wires

#### Step 2: Wire OLED

1. Mount XIAO S3 and OLED on breadboard
2. Connect VCC → 3.3V, GND → GND
3. Connect SDA → GPIO5 (D4), SCL → GPIO6 (D5)
4. Power on — OLED should light up (no display content yet, just backlight on OLED)

#### Step 3: Wire Buzzer and NeoPixel

1. Buzzer (+) → GPIO3 (D2), buzzer (-) → GND
2. NeoPixel DIN → GPIO4 (D3), VCC → 3.3V, GND → GND

#### Step 4: Flash Firmware

See [Section 9](#9-firmware-flashing----all-methods). Use the XIAO ESP32-S3 PlatformIO environment.

#### Step 5: Verify

Same as Build B Step 5. OLED will display detection data if using a display-enabled firmware fork (or serial output to OLED via custom code).

### Build A: WiFi-Only Quick Start (Existing Hardware)

#### Step 1: Choose a Board

- **Gold #3** for headless WiFi scanning
- **CYD #2** if you want the built-in 2.8" touchscreen (custom firmware needed)
- **AITRIP 4.0"** for the largest display option

#### Step 2: Flash Flock-You WiFi Firmware

> **Note:** Classic ESP32 boards run the WiFi-only Flock-You firmware (promiscuous mode), not the full Unified Blue. BLE modes (Detector, Foxhunter) require ESP32-S3.

1. Clone the repo: `git clone -b promiscious-dev https://github.com/colonelpanichacks/flock-you.git`
2. Open in PlatformIO (VSCode)
3. Edit `platformio.ini` to set your board type (e.g., `esp32dev` for Gold/WROOM)
4. Build and upload: `pio run -t upload`
5. Connect to AP `flockyou` / `flockyou123`
6. Browse to `192.168.4.1`

---

## 9. Firmware Flashing — All Methods

### Method 1: PlatformIO (Build from Source)

**Prerequisites:** Python 3.8+, PlatformIO Core or VSCode extension

```bash
# Install PlatformIO CLI
pip install platformio

# Clone the Unified Blue repo
git clone https://github.com/colonelpanichacks/oui-spy-unified-blue.git
cd oui-spy-unified-blue

# Build for XIAO ESP32-S3 (reference board)
pio run -e seeed_xiao_esp32s3

# Build for other boards
pio run -e seeed_xiao_esp32c3
pio run -e seeed_xiao_esp32c6

# Upload to connected board
pio run -e seeed_xiao_esp32s3 -t upload

# Monitor serial output
pio device monitor -e seeed_xiao_esp32s3 -b 115200
```

### Method 2: Python Flash Script (Pre-Built Binaries)

**Prerequisites:** Python 3.8+, esptool, pyserial

```bash
# Install dependencies
pip install esptool pyserial

# Clone and run flasher
git clone https://github.com/colonelpanichacks/oui-spy-unified-blue.git
cd oui-spy-unified-blue

# Interactive flash (auto-detects port)
python flash.py

# Batch mode (hands-free, for flashing multiple boards)
python flash.py --batch

# Full erase before flash (recommended for first flash)
python flash.py --erase
```

**Flash addresses:**
```
bootloader.bin    @ 0x0000
partitions.bin    @ 0x8000
boot_app0.bin     @ 0xe000
firmware.bin      @ 0x10000
```

### Method 3: esptool Direct (Manual)

```bash
esptool.py --chip esp32s3 --port COM3 --baud 921600 \
  --before default_reset --after hard_reset write_flash \
  0x0000 firmware/bootloader.bin \
  0x8000 firmware/partitions.bin \
  0xe000 firmware/boot_app0.bin \
  0x10000 firmware/oui-spy-unified-blue.bin
```

Replace `COM3` with your port (`COM#` on Windows, `/dev/ttyACM0` on Linux, `/dev/cu.usbmodem*` on Mac).

### Entering Download Mode

If the board doesn't flash automatically:

1. **XIAO ESP32-S3:** Hold BOOT button → press RESET → release BOOT
2. **T-Display S3:** Hold BOOT (GPIO0) → press RST → release BOOT
3. **Classic ESP32:** Hold BOOT → press EN → release BOOT
4. Board should appear as a new COM port in Device Manager

### Verifying Success

- 4 ascending beeps on boot = firmware running correctly
- NeoPixel breathes pink = scanning/ready state
- WiFi AP `oui-spy` appears in your phone's network list
- Serial monitor at 115200 baud shows boot messages

---

## 10. OUI Database — Sources & Management

### Pre-Loaded OUI Lists

#### Flock Safety OUI Prefixes (31 total)

From NitekryDPaul + DeFlockJoplin research:

```
70:c9:4e  3c:91:80  d8:f3:bc  80:30:49  b8:35:32
14:5a:fc  74:4c:a1  08:3a:88  9c:2f:9d  c0:35:32
94:08:53  e4:aa:ea  f4:6a:dd  f8:a2:d6  24:b2:b9
00:f4:8d  d0:39:57  e8:d0:fc  e0:4f:43  b8:1e:a4
70:08:94  58:8e:81  ec:1b:bd  3c:71:bf  58:00:e3
90:35:ea  5c:93:a2  64:6e:69  48:27:ea  a4:cf:12
82:6b:f2
```

#### Ring / Doorbell OUI Prefixes (11 total)

```
18:7f:88  24:2b:d6  34:3e:a4  54:e0:19  5c:47:5e
64:9a:63  90:48:6c  9c:76:13  ac:9f:c3  c4:db:ad
cc:3b:fb
```

### External OUI Database Sources

| Source | Entries | Update Freq | Format | License |
|--------|---------|------------|--------|---------|
| [Ringmast4r/OUI-Master-Database](https://github.com/Ringmast4r/OUI-Master-Database) | 88,873 OUIs | Monthly (1st) | TXT/CSV/JSON/SQLite/XML | MIT |
| [IEEE OUI Registry](https://standards.ieee.org/products-services/regauth/oui) | ~88,000+ | As registered | CSV | Public |
| [Wireshark manuf](https://gitlab.com/wireshark/wireshark/raw/master/manuf) | ~50,000+ | Continuous | TXT | GPLv2 |
| [macaddress.io](https://macaddress.io/database-download/csv) | ~50,000+ | Every 12 hours | CSV/JSON/XML | Free tier |

The Ringmast4r database is the most comprehensive — cross-validates IEEE, Wireshark, Nmap, and HDM sources. 43% of entries validated across all three primary sources. Used by Luke Switzer's Omni fork (39K+ subset on phone app).

### How OUI Lookup Works in Firmware

The firmware converts OUI strings to byte arrays at startup for fast matching in interrupt context:

```cpp
static uint8_t oui_bytes[OUI_COUNT][3];

void setup() {
  for (size_t i = 0; i < OUI_COUNT; i++) {
    sscanf(target_ouis[i], "%hhx:%hhx:%hhx",
           &oui_bytes[i][0], &oui_bytes[i][1], &oui_bytes[i][2]);
  }
}

// In IRAM callback (WiFi promiscuous) — <1ms lookup
bool match = (mac[0] == oui_bytes[i][0] &&
              mac[1] == oui_bytes[i][1] &&
              mac[2] == oui_bytes[i][2]);
```

For larger databases (39K+), the Omni fork stores the database on the phone and performs lookups via the Flutter app over BLE.

### Updating the OUI List

The detector firmware includes a sync script:

```bash
cd ouispy-detector
python sync-oui-list.py  # Fetches latest IEEE OUI assignments
```

For custom targets, add OUI prefixes via the web portal at `192.168.4.1` (Detector mode).

---

## 11. 3D Printed Cases

### OUI-SPY Specific

| Case | Platform | Features |
|------|----------|----------|
| OUI-SPY Case with antenna hole | [MakerWorld](https://makerworld.com/en/models/1807562) | SMA adapter cutout, wire routing (by out0fstep) |
| OUI-SPY Travel Case | [MakerWorld](https://makerworld.com/en/models/) | Transport protection (by out0fstep) |
| OUI-SPY Keychain | [MakerWorld](https://makerworld.com/en/models/) | Compact carry (by out0fstep) |
| Minimalist Oui Spy Box | [Printables](https://www.printables.com/model/) | Simple snap-fit enclosure |
| Case for Colonel Panic's OUI SPY | [Printables](https://www.printables.com/model/1552043) | USB-C + SMA holes (by TcW) |
| Mini Yagi Grip | MakerWorld | For 2.4GHz directional antenna |
| SMA Spacer | MakerWorld | Antenna offset mount (by Nitekry D Paul) |

### Generic ESP32 + OLED Cases

For Build C (XIAO S3 + OLED), search Printables/MakerWorld for:
- "XIAO ESP32 S3 case OLED"
- "ESP32 SSD1306 enclosure"
- "ESP32 project box with antenna"

### T-Display S3 Cases (Build B)

Search for "LILYGO T-Display S3 case" on Printables/MakerWorld. Many designs available with battery compartment and button access.

---

## 12. Companion Software & Apps

### Flask Desktop Dashboard (Flock-You)

Located in the `api/` folder of the Flock-You repo:

```bash
cd flock-you/api
pip install -r requirements.txt
python flockyou.py
```

Connects to OUI-Spy via serial, displays live detection feed, manages pattern databases, and handles JSON export.

### Mesh Mapper (Sky Spy)

Python visualization tool for drone detections:

```bash
python mesh-mapper.py
```

Ingests JSON serial output from Sky Spy mode, plots drone positions on a map.

### Flutter Companion App (Omni)

Luke Switzer's mobile app for the Omni fork:
- **Platforms:** iOS, Android, macOS (beta)
- **Connection:** BLE GATT to ESP32
- **Features:** Live detection feed (engine-colored), real-time wardrive map, 39K+ OUI database, WiGLE CSV export, per-engine configuration, geofence exclusion zones, iOS Dynamic Island notifications
- **Repo:** Part of [lukeswitz/oui-spy-unified-blue](https://github.com/lukeswitz/oui-spy-unified-blue)

### Home Assistant (Detector)

Detector mode supports MQTT auto-discovery. Add your Home Assistant MQTT broker credentials via the web portal. Detected devices appear as sensors in HA automatically.

### Serial Monitor

Any serial terminal at 115200 baud:
- **PlatformIO:** `pio device monitor -b 115200`
- **Arduino IDE:** Tools → Serial Monitor → 115200
- **PuTTY/screen:** Connect to COM port at 115200

---

## 13. Troubleshooting

### Board Not Detected via USB

1. **Check cable:** Use a data cable, not charge-only. Try a different cable
2. **Install driver:** XIAO S3 uses built-in USB CDC (no driver needed). Classic ESP32 needs CH340 or CP2102 driver
3. **Enter download mode:** Hold BOOT → press RESET → release BOOT
4. **Windows Device Manager:** Look under "Ports (COM & LPT)" for new device
5. **Try different USB port:** Front panel ports sometimes have power issues

### WiFi AP Not Appearing

1. **Wait 10 seconds** after power-on for AP to initialize
2. **Check serial output** at 115200 baud for error messages
3. **Verify firmware flash** — re-flash with `--erase` flag to clear NVS
4. **BOOT button:** Hold 2 seconds to force return to mode selector AP (`oui-spy`)

### No Detections

1. **Range:** BLE detections require devices within 10-30m. WiFi promiscuous requires active transmitters within ~50m
2. **Channel:** WiFi promiscuous only monitors one channel at a time (hops 1/6/11). Device may be on a different channel
3. **MAC randomization:** Smartphones randomize MACs — they won't match static OUI lists. Infrastructure devices (cameras, IoT) use real OUIs
4. **Check target list:** Verify OUI prefixes are entered correctly in the web portal (format: `XX:XX:XX`)
5. **Antenna:** For better range, use external antenna via IPEX/SMA connector

### Buzzer Not Working

1. **Check polarity:** Passive buzzers need PWM signal on (+). Active buzzers need DC
2. **Confirm GPIO:** Default is GPIO3 (D2) on XIAO S3. Check `config.h` or `main.cpp` for pin definition
3. **Test with serial:** If serial shows detections but no buzzer sound, it's a wiring issue

### OLED Display Blank (Build C)

1. **I2C address:** Most SSD1306 modules are `0x3C`. Some are `0x3D`. Run I2C scanner sketch to verify
2. **Wiring:** Double-check SDA/SCL connections. Try swapping them
3. **Power:** OLED needs 3.3V (some accept 5V). Check with multimeter
4. **Library:** If using custom firmware, ensure `Adafruit_SSD1306` or `U8g2` library is included in `platformio.ini`

### Flash Failed / Upload Error

1. **Wrong board selected:** Verify `platformio.ini` environment matches your board
2. **Port busy:** Close serial monitor before flashing
3. **Baud rate:** Try lower baud (460800 or 115200) if 921600 fails
4. **Erase flash:** `esptool.py --chip esp32s3 erase_flash` then re-flash all partitions

---

## 14. Legal Considerations

### Blue Edition (All Detection Modes) — Passive Listening

OUI-Spy Blue Edition firmware is **receive-only**. It captures publicly broadcast wireless signals (WiFi beacons, BLE advertisements) without transmitting any attack packets, injection frames, or exploitation attempts.

**Legal standing:**
- **ECPA / Wiretap Act (18 USC 2511):** The "readily accessible to the general public" exception applies to unencrypted WiFi management frames and BLE advertisements. These are broadcast openly by design
- **Federal precedent:** A federal judge ruled that passive WiFi monitoring of unencrypted frames is legal under this exception
- **FCC:** Passive reception of RF spectrum is generally permitted (analogous to radio scanning). WiFi *blocking* is prohibited, but OUI-Spy does not block anything
- **No active transmission:** OUI-Spy Blue Edition never sends deauth, injection, or spoofing frames

**Important caveats:**
- Intercepting **encrypted** WiFi data frames (WPA2/WPA3 payload) may violate ECPA even in passive mode
- State laws vary — some states have stricter electronic surveillance statutes
- Using detection results to stalk, harass, or surveil individuals is illegal regardless of the tool
- Always consult local legal counsel for your jurisdiction

### Red Edition (Remote-ID-Spoofer) — Transmit-Based

> **Illegal in most jurisdictions.** Spoofing FAA Remote ID broadcasts violates 14 CFR 89 and FCC regulations. For authorized security research only. Not included in Unified Blue.

### UniPwn (Unitree Robot Exploitation)

> **Requires explicit authorization.** Unauthorized access to computer systems is a felony under CFAA (18 USC 1030). Only use in controlled lab environments with written permission from the robot owner.

---

## 15. All Resource Links

### Official Repositories

| Repo | Description |
|------|-------------|
| [colonelpanichacks/oui-spy](https://github.com/colonelpanichacks/oui-spy) | Main repo — overview, PCB info, links |
| [colonelpanichacks/oui-spy-unified-blue](https://github.com/colonelpanichacks/oui-spy-unified-blue) | Unified Blue firmware (4 modes) |
| [lukeswitz/oui-spy-unified-blue](https://github.com/lukeswitz/oui-spy-unified-blue) | Omni fork (7-8 concurrent engines + Flutter app) |
| [colonelpanichacks/ouispy-detector](https://github.com/colonelpanichacks/ouispy-detector) | Standalone Detector firmware |
| [colonelpanichacks/ouispy-foxhunter](https://github.com/colonelpanichacks/ouispy-foxhunter) | Standalone Foxhunter firmware |
| [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you) | Standalone Flock-You firmware (`promiscious-dev` branch) |
| [colonelpanichacks/Sky-Spy](https://github.com/colonelpanichacks/Sky-Spy) | Standalone Sky Spy firmware |
| [colonelpanichacks/Oui-Spy-UniPwn](https://github.com/colonelpanichacks/Oui-Spy-UniPwn) | UniPwn (Unitree exploitation, authorized research) |
| [colonelpanichacks/Remote-ID-Spoofer](https://github.com/colonelpanichacks/Remote-ID-Spoofer) | Red Edition spoofer (illegal in most jurisdictions) |

### OUI Databases

| Source | Link |
|--------|------|
| Ringmast4r OUI Master Database (88K+) | [GitHub](https://github.com/Ringmast4r/OUI-Master-Database) |
| IEEE OUI Registry | [IEEE](https://standards.ieee.org/products-services/regauth/oui) |
| Wireshark manuf file | [GitLab](https://gitlab.com/wireshark/wireshark/raw/master/manuf) |
| Wireshark OUI Lookup Tool | [wireshark.org](https://www.wireshark.org/tools/oui-lookup.html) |
| macaddress.io | [macaddress.io](https://macaddress.io/database-download/csv) |
| nite-oui-collection (Flock research) | Included in Flock-You datasets folder |

### Hardware Stores

| Store | Link | What |
|-------|------|------|
| Colonel Panic's Store | [colonelpanic.tech](https://colonelpanic.tech/) | OUI-SPY boards, patches, badges |
| Colonel Panic's Tindie | Tindie | Same products, alternative storefront |
| Seeed Studio | [seeedstudio.com](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html) | XIAO ESP32-S3 |
| LILYGO Official | [lilygo.cc](https://lilygo.cc/products/t-display-s3) | T-Display S3 |
| Heltec | [heltec.org](https://heltec.org/project/wifi-kit32-v3/) | WiFi Kit 32 V3 |

### 3D Print Files

| Platform | Search |
|----------|--------|
| MakerWorld | "oui spy case" |
| Printables | "oui spy" or "ESP32 XIAO case" |

### Datasheets

| Component | Link |
|-----------|------|
| ESP32-S3 | [espressif.com](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) |
| XIAO ESP32-S3 | [Seeed Wiki](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/) |
| T-Display S3 | [LILYGO GitHub](https://github.com/Xinyuan-LilyGO/T-Display-S3) |
| SSD1306 OLED | [solomon-systech.com](https://www.solomon-systech.com/product/ssd1306/) |
| ST7789 TFT | [newhavendisplay.com](https://www.newhavendisplay.com/appnotes/datasheets/LCDs/ST7789V.pdf) |
| NimBLE-Arduino | [GitHub](https://github.com/h2zero/NimBLE-Arduino) |
| TFT_eSPI | [GitHub](https://github.com/Bodmer/TFT_eSPI) |
| Adafruit NeoPixel | [GitHub](https://github.com/adafruit/Adafruit_NeoPixel) |

### Build Dependencies

| Library | Version | PlatformIO Install |
|---------|---------|-------------------|
| NimBLE-Arduino | ^1.4.0 | `lib_deps = h2zero/NimBLE-Arduino` |
| ESP Async WebServer | ^3.0.6 | `lib_deps = ESP Async WebServer` |
| ArduinoJson | ^7.0.4 | `lib_deps = bblanchon/ArduinoJson` |
| Adafruit NeoPixel | ^1.12.0 | `lib_deps = adafruit/Adafruit NeoPixel` |
| TFT_eSPI | ^2.5.0 | `lib_deps = bodmer/TFT_eSPI` (for display builds) |
| Adafruit SSD1306 | ^2.5.7 | `lib_deps = adafruit/Adafruit SSD1306` (for OLED builds) |
| Adafruit GFX | ^1.11.5 | `lib_deps = adafruit/Adafruit GFX Library` (for OLED builds) |
| U8g2 | ^2.35.0 | `lib_deps = olikraus/U8g2` (alternative OLED driver) |
| TinyGPS++ | ^1.1.0 | `lib_deps = mikalhart/TinyGPSPlus` (for GPS builds) |

### Community & Videos

| Resource | Link |
|----------|------|
| OUI-Spy on Hackster.io | [hackster.io](https://www.hackster.io/colonelpanic/oui-spy-now-and-beyond-1f9c9a) |
| Colonel Panic's YouTube | Search "colonelpanichacks oui-spy" |
| Flock Detection video | [Watch](https://www.youtube.com/watch?v=W_F4rEaRduk) (also linked in Project 06) |
| Drone Detection video | [Watch](https://youtu.be/qK5cIhksoYw) (also linked in Project 06) |

---

## Related Projects in This Repo

| Project | Overlap | Notes |
|---------|---------|-------|
| [06 — Flock & Drone Detection](../06-flock-drone-detection/) | Flock-You mode, Sky Spy mode | Deep Flock legal analysis, all 31 OUIs, detection research |
| [08 — BLE Detection & Tracking](../08-ble-detection/) | Detector mode | BLE tracker detection concepts |
| [10 — Chasing Your Tail](../10-chasing-your-tail/) | Detector mode | AirTag/SmartTag/Tile detection |
| [01 — ESP32 Marauder](../01-esp32-marauder/) | WiFi scanning, OUI display | Marauder extracts vendor OUI in AP scans |
| [14 — Cyberdeck](../14-cyberdeck/) | All modes | OUI-Spy as a cyberdeck integration candidate |
