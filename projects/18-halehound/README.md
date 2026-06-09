# Project 18: HaleHound — ESP32 CYD Multi-Protocol Attack Toolkit

> **Status:** Ready to Build
> **Difficulty:** Medium
> **Hardware:** ESP32 2.8" CYD Touchscreen (already in inventory)
> **Repository:** [JesseCHale/HaleHound-CYD](https://github.com/JesseCHale/HaleHound-CYD)
> **Website:** [halehound.com](https://halehound.com/)
> **Current Version:** v3.5.5 (April 2026)
> **License:** Open source (community-driven)

---

## Overview

HaleHound-CYD is a multi-protocol offensive security toolkit for the ESP32 "Cheap Yellow Display" platform. It consolidates **40+ attack modules** across WiFi, Bluetooth, SubGHz (CC1101), 2.4GHz (NRF24), NFC/RFID (PN532), and GPS into a $7-15 touchscreen dev board with a full touch-driven UI.

Based on the [ESP32-DIV](https://github.com/cifertech/esp32-div) project (Project 15 in this repo), HaleHound adds a polished CYD-native interface, additional attack modules, and the **IoT Recon** automated credential harvesting suite.

### What Makes This Different from Marauder

| | HaleHound | ESP32 Marauder |
|---|---|---|
| **Primary focus** | Multi-protocol attacks (WiFi + BLE + SubGHz + NFC + IR) | WiFi/BLE attacks |
| **Display** | CYD touchscreen native (built-in) | CYD, TFT, or headless |
| **SubGHz** | Yes (CC1101 — replay, brute force, Tesla charge port) | No |
| **NFC/RFID** | Yes (PN532 — scan, read, clone, brute force) | No |
| **IoT Recon** | Yes (automated LAN scan + credential brute force) | No |
| **Defensive tools** | WiFi Guardian, SubGHz Sentinel, Stalkerware Detect | Limited |
| **2.4GHz radio** | NRF24 (MouseJack, sniffer, spectrum analyzer) | No |

### Relationship to ESP32-DIV (Project 15)

HaleHound is a fork/derivative of ESP32-DIV by cifertech. It uses the same hardware platform (ESP32 + CC1101 + NRF24 + PN532) but targets the CYD form factor specifically. If you build HaleHound, you do NOT also need to build ESP32-DIV separately — HaleHound includes all DIV capabilities plus additional modules.

---

## IoT Recon — The Key Module

IoT Recon is an automated LAN attack suite added in HaleHound v3.2.0. This is the reason this project was added to the repo.

### What It Does

1. Connects to a target WiFi network via on-screen keyboard
2. Performs a full subnet scan to discover all devices on the LAN
3. Fingerprints discovered services: **HTTP, RTSP, Telnet, MQTT, Modbus, XMEye, SSH, FTP**
4. Brute forces credentials using **40+ built-in default password combinations**
5. Supports custom credential lists via `/creds.txt` on SD card
6. Stores all harvested credentials to the SD card loot directory

### Technical Details

- Dual-core execution: networking on Core 0, UI rendering on Core 1 (no screen freeze during scans)
- Targets IoT devices, cameras (RTSP/XMEye), industrial controllers (Modbus), message brokers (MQTT)
- Only requires the base CYD board — no external radio modules needed (uses ESP32 built-in WiFi)

---

## Hardware Requirements

### Base Build (Required — Already in Inventory)

| Component | Source | Cost | Notes |
|-----------|--------|------|-------|
| ESP32 2.8" CYD Touchscreen | INVENTORY: CYD #2 | $0 (owned) | ESP32-2432S028R, ILI9341, 240x320 |
| Micro SD card | INVENTORY: 16GB or 128GB | $0 (owned) | For loot storage + custom creds |

### External Radio Modules (Optional — Expand Capabilities)

| Module | Enables | Cost | Notes |
|--------|---------|------|-------|
| CC1101 (HW-863 or E07-433M20S) | SubGHz 300-928 MHz (replay, brute force, Tesla charge port) | ~$3-8 | SPI wiring to CYD GPIO |
| NRF24L01+PA+LNA | 2.4 GHz sniffer, MouseJack keystroke injection, spectrum analyzer | ~$3-5 | SPI wiring, shared bus with CC1101 |
| PN532 V3 (SPI mode) | NFC/RFID scan, read, clone, brute force | ~$5-8 | SPI mode required (NOT I2C) |
| GT-U7 or NEO-6M GPS | Wardriving, location tagging | ~$5-10 | UART to CYD RX/TX |
| Independent 3.3V buck converter | Brownout prevention for PA modules | ~$2-3 | Required if using Ebyte PA variant CC1101 |

**Total for full build with all modules: ~$25-40 on top of existing CYD**

---

## Full Module List (v3.5.5)

### WiFi (Built-in, no extra hardware)
- Packet Monitor
- Beacon Spammer
- WiFi Deauther
- Probe Sniffer
- WiFi Scanner
- Captive Portal (GARMR)
- Station Scanner
- Auth Flood
- **IoT Recon** (automated LAN scan + credential brute force)
- EAPOL Capture (WPA handshakes + PMKID)
- Karma Attack
- Wardriving (with GPS module)

### Bluetooth (Built-in)
- BLE Cinder
- BLE Spoofer
- BLE Beacon
- BLE Predator (GATT reconnaissance + honeypot)
- WhisperPair (CVE-2025-36911)
- Airoha RACE (CVE-2025-20700/20701/20702 — targets Sony, Marshall, JBL, Jabra)
- Lunatic Fringe (AirTag/SmartTag/Tile/Chipolo/FMDN tracker detection + Phantom Flood + AirTag Replay)

### SubGHz (Requires CC1101)
- Replay Attack
- Brute Force
- SubGHz Scorch
- Spectrum Analyzer
- Saved Profile
- Tesla Charge Port Opener (315 MHz US / 433.92 MHz EU)
- .Sub File Reader (Flipper Zero format support)

### 2.4GHz Radio (Requires NRF24)
- Scanner
- Spectrum Analyzer
- NRF Sniffer
- MouseJack Keystroke Injection
- WLAN Ember
- Proto Kill

### NFC/RFID (Requires PN532)
- Card Scanner
- Card Reader
- Card Clone
- Key Brute Force
- Card Emulate

### Defensive / Blue Team
- WiFi Guardian (rogue AP detection)
- SubGHz Sentinel (rogue signal detection)
- 2.4GHz Watchdog
- Full Spectrum Monitoring
- Stalkerware Detect

### Operational Security
- VALHALLA Protocol (liability disclaimer gates all offensive modules)
- PIN Lock
- Blue Team Mode (persists across reboots)
- Loot Browser (SD card with filtering and export)

### TX Power
- WiFi: +20.5 dBm
- NRF24: +20 dBm
- CC1101: +12 dBm stock / +20 dBm with PA
- BLE: +9 dBm

---

## Flashing

### Method 1: Web Flasher (Recommended)
1. Go to [halehound.com](https://halehound.com/)
2. Select your CYD board variant (2.8" or 3.5")
3. Connect CYD via USB, click Flash
4. Done — no IDE, no compile

### Method 2: Arduino IDE
1. Install Arduino IDE + ESP32 board support
2. Clone [HaleHound-CYD repo](https://github.com/JesseCHale/HaleHound-CYD)
3. Open project, select board "ESP32 Dev Module"
4. Flash at 921600 baud

### Method 3: OTA Update from SD Card
1. Download latest `.bin` from [releases](https://github.com/JesseCHale/HaleHound-CYD/releases)
2. Copy to SD card root
3. Boot CYD with SD inserted → firmware updates automatically

---

## Wiring Guide (External Modules)

### CC1101 to CYD (SPI)

| CC1101 Pin | CYD GPIO |
|-----------|----------|
| VCC | 3.3V |
| GND | GND |
| CSN | GPIO 15 |
| SCK | GPIO 14 |
| MOSI | GPIO 13 |
| MISO | GPIO 12 |
| GDO0 | GPIO 2 |
| GDO2 | GPIO 4 |

### NRF24L01+PA+LNA to CYD (SPI)

| NRF24 Pin | CYD GPIO |
|-----------|----------|
| VCC | 3.3V (external buck if PA+LNA variant) |
| GND | GND |
| CSN | GPIO 5 |
| CE | GPIO 26 |
| SCK | GPIO 18 |
| MOSI | GPIO 23 |
| MISO | GPIO 19 |

### PN532 to CYD (SPI)

| PN532 Pin | CYD GPIO |
|-----------|----------|
| VCC | 3.3V |
| GND | GND |
| SS | GPIO 27 |
| SCK | Shared with NRF24 (GPIO 18) |
| MOSI | Shared with NRF24 (GPIO 23) |
| MISO | Shared with NRF24 (GPIO 19) |

---

## Cyberdeck Integration

HaleHound on CYD #2 becomes a standalone multi-protocol attack station inside the deck. It does NOT require the Pi 5 — it operates independently with its own touchscreen.

**Deck role:** Multi-protocol attack station (WiFi/BLE/SubGHz/NFC) + IoT Recon credential harvester
**Board:** CYD #2
**Power:** USB from powered hub, switched via toggle
**Display:** Built-in 2.8" touchscreen (self-contained)
**Storage:** Micro SD for loot, captures, custom cred lists

See [cyberdeck integration guide](../14-cyberdeck/integrations/18-halehound/) for deck-specific wiring and placement.

---

## Limitations

- **2.4GHz WiFi only** — classic ESP32 chip, no 5GHz support (use ESP32-C5 boards for dual-band)
- **Single radio** — cannot do WiFi and SubGHz simultaneously (time-shared)
- **Fork of ESP32-DIV** — attribution dispute exists (Issue #116 on ESP32-DIV repo)
- **No WPA3 support** — ESP32 hardware limitation
- **CYD-specific** — requires the ESP32-2432S028 board variant, not a generic ESP32

---

## Feature Brainstorm — What Else Can This Do

- **IoT Recon credential harvesting on home lab** — connect to your own network and run IoT Recon against cameras, routers, smart plugs, and NAS devices to audit how many still use default credentials; export the loot report as a remediation checklist
- **CC1101 SubGHz replay attacks** — capture and replay garage door openers, gate remotes, and car key fobs (authorized targets only) to demonstrate SubGHz vulnerabilities during physical security assessments
- **Tesla charge port opener** — replay the 315 MHz (US) / 433.92 MHz (EU) signal to pop a Tesla charge port door as a controlled SubGHz demo; pairs with the CC1101 module already in the wiring guide
- **PN532 NFC badge cloning for access control audits** — read and clone 13.56 MHz MIFARE / NTAG badges on authorized facilities; log UIDs and key sectors for audit documentation
- **WiFi Guardian defensive monitoring** — deploy HaleHound in Blue Team Mode as a rogue AP detector on your home or lab network, alerting when unknown access points appear
- **SubGHz Sentinel for nearby transmissions** — use the CC1101 spectrum analyzer to passively monitor 315/433/868/915 MHz bands and detect unexpected SubGHz activity (e.g., unknown remotes, jammers, or IoT devices)
- **Stalkerware Detect for hidden devices** — scan for hidden cameras, microphones, and BLE-emitting surveillance devices in hotel rooms, Airbnbs, or meeting rooms using the built-in Stalkerware Detect module
- **Custom credential wordlists for IoT** — expand IoT Recon's default 40-credential list with vendor-specific defaults (Hikvision, Dahua, Ubiquiti, TP-Link) via `/creds.txt` on SD card for deeper coverage
- **BLE spam resilience testing** — use BLE Cinder and BLE Spoofer to test how your own devices (phones, headphones, smartwatches) handle malformed BLE advertisements and connection floods
- **MouseJack keystroke injection via NRF24** — test wireless keyboards in your environment for the MouseJack vulnerability using the NRF24 module; inject a benign test string to prove exploitability on authorized hardware
- **Marauder + IoT Recon combo workflow** — use Marauder to deauth a target off their AP, capture the handshake, then pivot to HaleHound's IoT Recon to scan the network for devices with default credentials once connected

---

## Resources

| Resource | Link |
|----------|------|
| GitHub repo | [JesseCHale/HaleHound-CYD](https://github.com/JesseCHale/HaleHound-CYD) |
| Website | [halehound.com](https://halehound.com/) |
| Releases | [GitHub Releases](https://github.com/JesseCHale/HaleHound-CYD/releases) |
| Base project | [cifertech/ESP32-DIV](https://github.com/cifertech/esp32-div) |
| CYD pinout reference | [RandomNerdTutorials](https://randomnerdtutorials.com/esp32-cheap-yellow-display-cyd-pinout-esp32-2432s028r/) |
| CYD community docs | [witnessmenow/ESP32-Cheap-Yellow-Display](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display) |
| Build video | [Best DIY Hacking Gadget of 2026](https://www.youtube.com/watch?v=r_qS7qlY9eM) |
