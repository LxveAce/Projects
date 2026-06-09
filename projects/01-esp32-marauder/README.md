# ESP32 Marauder

---

## Table of Contents

1. [Overview](#1-overview)
2. [Features -- Complete Tool List](#2-features----complete-tool-list)
3. [Compatible Hardware -- All Supported Boards](#3-compatible-hardware----all-supported-boards)
4. [Complete Parts List with Prices](#4-complete-parts-list-with-prices)
5. [Step-by-Step Build Guide](#5-step-by-step-build-guide)
6. [Firmware Flashing -- All Methods](#6-firmware-flashing----all-methods)
7. [Usage Guide for Each Feature](#7-usage-guide-for-each-feature)
8. [Troubleshooting](#8-troubleshooting)
9. [Legal Considerations](#9-legal-considerations)
10. [All Resource Links](#10-all-resource-links)
11. [Best-Fit Hardware from Your Inventory](#11-best-fit-hardware-from-your-inventory)
12. [Feature Brainstorm -- What Else Can This Do](#12-feature-brainstorm----what-else-can-this-do)
13. [Cyberdeck Integration](#13-cyberdeck-integration)

---

## 1. Overview

ESP32 Marauder is an open-source WiFi and Bluetooth security toolkit for ESP32 boards. Flash it onto a $10 dev board and you get a pocket-sized scanner, sniffer, and attack platform for wireless pentesting.

**Creator:** justcallmekoko ([GitHub](https://github.com/justcallmekoko)) · [justcallmekokollc.com](https://justcallmekokollc.com)

**Stats (June 2026):** 11,100+ stars, 1,300+ forks, 169 releases (latest v1.12.1). Codebase is 77.2% C++, 21.4% C.

---

## 2. Features -- Complete Tool List

### WiFi Scanning and Reconnaissance

- **Scan APs** -- Discovers and lists all nearby access points with SSID, BSSID, channel, signal strength, and encryption type
- **Station Sniff** -- Captures data from client devices (stations) connected to access points
- **Probe Request Sniff** -- Captures probe requests from nearby devices, revealing what networks they are searching for
- **Beacon Sniff** -- Captures beacon frames from nearby APs, showing network configurations
- **Signal Monitor** -- Real-time monitoring of WiFi signal strength for selected networks
- **Packet Monitor** -- Captures and displays all WiFi packets in real-time for comprehensive traffic analysis
- **Raw Capture** -- Captures all raw WiFi frames without filtering for offline analysis

### WiFi Attacks

- **Deauth Flood** -- Forges fake deauthentication packets to disconnect ALL clients from a targeted access point (broadcast)
- **Deauth Targeted** -- Sends deauth frames to specific client MAC addresses only, more surgical than flood
- **Beacon Spam List** -- Broadcasts fake WiFi network names from a user-generated SSID list
- **Beacon Spam Random** -- Transmits randomly-generated fake WiFi SSIDs
- **Rick Roll Beacon** -- Broadcasts song lyrics as fake WiFi network names
- **AP Clone Spam** -- Duplicates a real access point's configuration, creating multiple clones to confuse users
- **Probe Request Flood** -- Broadcasts probe requests with random SSIDs to confuse probe sniffers
- **Evil Portal** -- Spawns a rogue access point with a captive portal serving fake login pages; captures entered credentials. Supports custom HTML templates, SD card storage, and simultaneous deauth of the legitimate AP (EPDeauth setting)
- **EAPOL/PMKID Scan** -- Captures EAPOL and PMKID frames for WPA/WPA2 handshake cracking (compatible with hashcat/aircrack-ng)
- **ForcePMKID** -- Automatically sends deauth frames during PMKID sniffing to force handshake re-negotiation

### WiFi Detection

- **Deauth Sniff** -- Detects and captures deauthentication frames on the network (defensive)
- **Detect Pwnagotchi** -- Identifies nearby Pwnagotchi automated hacking devices

### Bluetooth / BLE Tools

- **Bluetooth Sniffer** -- Captures Bluetooth packets in vicinity for device identification and analysis
- **Sour Apple** -- Exploits an iOS 17 vulnerability to spam pop-ups on nearby Apple devices until crash
- **Swiftpair Spam** -- BLE attack generating 1,000+ fake pairing notifications per minute on Windows PCs
- **Samsung BLE Spam** -- Targets Samsung devices with repeated Bluetooth pairing notifications
- **Google BLE Spam** -- Targets Google Pixel devices with pairing notification spam
- **BLE Spam All** -- Executes all BLE spam attacks simultaneously
- **Detect Card Skimmers** -- Scans for Bluetooth devices matching known card skimmer signatures
- **AirTag / Tile Detection** -- Identifies nearby tracking devices

### Data and Logging

- **SavePCAP** -- Saves captured WiFi data to .pcap files on SD card (Wireshark-compatible)
- **Wardriving** -- GPS-aided WiFi mapping with signal strength logging
- **SD Card Logging** -- Persistent storage of all scan results and captures

### Settings and Utilities

- **Generate SSIDs** -- Creates SSID lists for beacon spam attacks
- **EnableLED** -- Toggles status indicator LED
- **ForceProbe** -- Auto-deauth during probe sniffing
- **OTA Updates** -- Over-the-air firmware updating
- **CLI Interface** -- Full serial command-line control for all features

---

## 3. Compatible Hardware -- All Supported Boards

### Official Marauder Hardware

| Board | Chip | Display | Key Features | Pros | Cons |
|-------|------|---------|-------------|------|------|
| Marauder v4 (Original) | ESP32 | 2.8" ILI9341 touch | SD card, optional GPS/battery/LED, BT | Full-featured original | Older design, larger |
| Marauder v6 / v6.1 | ESP32 | ILI9341 touch | GPS (v6.1), SD, battery, BT, CLI | Improved design, GPS added | Must match firmware to exact revision |
| Marauder v7 / v7.1 | ESP32 / ESP32-E | ILI9341 | Dual NRF24, tactile switch (no touch), BT, SD | NRF24 support, PSRAM on v7.1 | No touchscreen, button nav only |
| Marauder v8 | ESP32 | ILI9341 | Latest official, SMA antenna mount | Newest design, antenna upgradeable | Premium price |
| Marauder Mini | ESP32 | 1.44" ST7735 | 5-way joystick, onboard GPS, LiPo, external 2.4GHz antenna | Ultra-compact, self-contained | Small screen, joystick-only control |
| Marauder Kit | ESP32 (Huzzah32) | ILI9341 | DIY assembly, 3D-printed case | Cheapest official option, educational | Requires soldering, separate MCU purchase |
| Dev Board Pro | ESP32 | None (serial only) | Flipper addon, GPS expansion, SD | Flipper integration | No standalone display |
| BFFB | ESP32 | None | Flipper Zero integration, LED | Compact Flipper addon | Serial-only, no screen |

### Flipper Zero Integration Boards

| Board | Chip | Notes |
|-------|------|-------|
| Flipper Zero WiFi Dev Board | ESP32-S2 | PSRAM enabled, serial control via Flipper |
| Flipper Zero MultiBoard S3 | ESP32-S3 | Expandable platform, addon support |
| ESP32 Wemos D1 Mini Adapter | ESP32 | Budget Flipper WiFi addon |
| AWOK V2/V3 | ESP32 | Third-party Flipper boards, multiple USB color variants |
| FlipMods Ultra V3 (Sacred Labs) | ESP32-WROOM-32UE | 18-pin Flipper GPIO board, pre-loaded firmware |

### Cheap Yellow Display (CYD) Boards -- Best Budget Option

| Model | Size | Touch | Display Driver | Price |
|-------|------|-------|---------------|-------|
| ESP32-2432S028R | 2.8" | Resistive (XPT2046) | ILI9341 | ~$8-15 |
| ESP32-2432S028 (2USB) | 2.8" | Resistive | ILI9341 | ~$10-15 |
| ESP32-2432S024C | 2.4" | Capacitive (CST820) | ILI9341 | ~$10-15 |
| ESP32-2432S024R (Guition) | 2.4" | Resistive | ILI9341 | ~$8-12 |
| ESP32-2432S032C | 3.2" | Capacitive (GT911) | ST7789 | ~$12-18 |
| ESP32-2432S032R | 3.2" | Resistive | ST7789 | ~$10-15 |
| ESP32-3248S035C | 3.5" | Capacitive (GT911) | ST7796 | ~$15-20 |
| ESP32-3248S035R | 3.5" | Resistive | ST7796 | ~$12-18 |
| ESP32-1732S019 | 1.9" | None | ST7789 (S3) | ~$10-15 |

### Other Supported Platforms

| Board | Chip | Display | Notes |
|-------|------|---------|-------|
| M5StickC Plus / Plus 2 | ESP32 | ST7735 | Compact integrated platform |
| M5Cardputer | ESP32-S3 | ST7735 | Built-in keyboard, integrated platform |
| Rev Feather (ESP32-S2) | ESP32-S2 | ST7735 | Feather form factor, PSRAM, battery option |
| ESP32 LDDB / NodeMCU / Wemos | ESP32 | None | Dev/testing, serial only |
| ESP32-C5 DevKitC-1 | ESP32-C5 | None | 5GHz WiFi support, PSRAM |
| CYD Micro | ESP32 | ILI9341 | Display dev board variant |
| CYD GUITION | ESP32 | ILI9341 | GUITION display integration |

### Advanced / Third-Party Hardware

- **ESP32 Marauder Double Barrel 5G** -- Dual ESP32 chipsets + RTL8720DN for 5GHz deauth, GPS, Sub-GHz (433MHz), onboard battery. Works standalone or with Flipper Zero.
- **Apex 5 Module** -- ESP32-C5 + two Sub-GHz radios + nRF24 + GPS, five antenna ports. Flipper Zero addon.

---

## 4. Complete Parts List with Prices

### Option A: CYD Budget Build (Easiest, ~$15-30 total)

| Part | Price | Source |
|------|-------|--------|
| ESP32-2432S028R (2.8" CYD board) | $8-15 | AliExpress, Amazon, eBay |
| Micro USB data cable | $3-5 | Amazon |
| MicroSD card (4-32GB, SanDisk recommended) | $5-8 | Amazon |
| **TOTAL** | **~$16-28** | |

### Option B: CYD Build with GPS + Battery (~$50-80)

| Part | Price | Source |
|------|-------|--------|
| ESP32-2432S028R (2.8" CYD) | $8-15 | AliExpress, Amazon |
| NEO-6M GPS module with antenna | $8-12 | AliExpress, Amazon |
| 3.7V LiPo battery (500-1000mAh) with JST | $5-10 | Amazon, Adafruit |
| TP4056 USB-C charging module | $2-5 | AliExpress |
| MicroSD card (4-32GB, SanDisk) | $5-8 | Amazon |
| Dupont jumper wires (female-female) | $3-5 | Amazon |
| USB data cable | $3-5 | Amazon |
| 3D-printed case (optional) | $5-15 | Self-print or online service |
| **TOTAL** | **~$39-75** | |

### Option C: Official Marauder Kit (~$60-80)

| Part | Price | Source |
|------|-------|--------|
| ESP32 Marauder Kit PCB + enclosure | ~$40-50 | justcallmekokollc.com |
| Adafruit Huzzah32 ESP32 Feather | ~$20 | Adafruit |
| 3.7V LiPo battery with JST | $5-10 | Adafruit |
| **TOTAL** | **~$65-80** | |

### Option D: Pre-built / Pre-flashed (~$35-120)

| Product | Price | Source |
|---------|-------|--------|
| Pre-flashed CYD Marauder (2.8") | $35-60 | eBay, Tindie |
| Official Marauder hardware | $60-120+ | justcallmekokollc.com |
| CYD Battery+GPS Mod Kit | $52 | [Biscuit Shop](https://biscuitshop.us/products/esp32-marauder-battery-mod-kit), [Elecrow](https://www.elecrow.com/cyd-2-8-marauder-bruce-battery-gps-mod-diy-kit.html) |
| Flipper Zero addon boards | $25-60 | Various |

### Option E: Full DIY Custom Build (~$30-60)

| Part | Price | Source |
|------|-------|--------|
| ESP32 DevKitC / WROOM-32 dev board | $5-10 | AliExpress |
| 2.8" ILI9341 SPI TFT touchscreen | $8-12 | AliExpress |
| MicroSD card module | $2-3 | AliExpress |
| MicroSD card (4-32GB, SanDisk) | $5-8 | Amazon |
| NEO-6M GPS module (optional) | $8-12 | AliExpress |
| 3.7V LiPo + TP4056 charger (optional) | $5-10 | AliExpress |
| Breadboard + jumper wires | $5-8 | Amazon |
| External 2.4GHz SMA antenna (optional) | $3-8 | AliExpress |
| **TOTAL** | **~$30-60** | |

---

## 5. Step-by-Step Build Guide

### Build Path 1: CYD Board (Recommended for Beginners)

This is the simplest build -- the CYD (Cheap Yellow Display) already integrates the ESP32 + display + touchscreen + SD card slot on a single PCB. No soldering required.

**Step 1: Acquire Hardware**

- Purchase an ESP32-2432S028R (2.8" CYD) from AliExpress/Amazon (~$10-15)
- Get a MicroSD card (4-32GB, SanDisk brand strongly recommended, FAT32 formatted)
- Get a Micro USB data cable (not charge-only)

**Step 2: Install USB Drivers**

- Connect the CYD to your PC via USB
- Windows should auto-detect; if not, install CP2102 or CH340 drivers depending on your board variant
- Verify the board appears in Device Manager under "Ports (COM & LPT)"

**Step 3: Flash Firmware (Web Flasher Method -- Easiest)**

1. Open Google Chrome or Microsoft Edge (Firefox/Safari NOT supported)
2. Navigate to the CYD Marauder Web Flasher: https://marautech.github.io/ESP32-Cyd-Marauder-WebFlasher/
3. Hold the BOOT button on the CYD board
4. Click "Connect" in the web flasher and select the COM port
5. Select your exact board model (2.8" resistive, 2USB, etc.)
6. Select the latest firmware version
7. Click "Install" and wait for flashing to complete
8. When it says "To run the new firmware please reset your device," press the RST button or power cycle

**Step 4: Insert SD Card (Optional but Recommended)**

- Format a MicroSD card as FAT32 (must be 32GB or smaller)
- Insert into the CYD's card slot
- This enables PCAP saving, Evil Portal HTML storage, and log persistence

**Step 5: Power On and Use**

- Connect via USB or battery
- The Marauder touchscreen interface loads automatically
- Navigate menus by tapping the screen

### Build Path 2: ESP32 Dev Board + Separate TFT Display (DIY)

**Step 1: Gather Components**

- ESP32 DevKitC or WROOM-32 development board
- 2.8" ILI9341 SPI TFT touch display
- MicroSD card module (SPI)
- Jumper wires (female-to-female)
- Breadboard (for prototyping)

**Step 2: Wire the TFT Display to ESP32**

ILI9341 TFT to ESP32 connections:

| TFT Pin | ESP32 Pin | Function |
|---------|-----------|----------|
| VCC | 3.3V | Power |
| GND | GND | Ground |
| CS | GPIO 15 | Chip Select |
| RESET | GPIO 4 | Reset |
| DC/RS | GPIO 2 | Data/Command |
| SDI/MOSI | GPIO 23 | SPI Data In |
| SCK | GPIO 18 | SPI Clock |
| LED | 3.3V | Backlight |
| SDO/MISO | GPIO 19 | SPI Data Out |
| T_CLK | GPIO 18 | Touch Clock |
| T_CS | GPIO 21 | Touch Chip Select |
| T_DIN | GPIO 23 | Touch Data In |
| T_DO | GPIO 19 | Touch Data Out |
| T_IRQ | GPIO 15 | Touch Interrupt |

**Step 3: Wire the SD Card Module (Optional)**

| SD Module Pin | ESP32 Pin |
|--------------|-----------|
| VCC | 3.3V |
| GND | GND |
| MISO | GPIO 19 |
| MOSI | GPIO 23 |
| SCK | GPIO 18 |
| CS | GPIO 12 |

**Step 4: Wire GPS Module (Optional)**

| GPS Pin | ESP32 Pin |
|---------|-----------|
| VCC | 3.3V or VIN |
| GND | GND |
| TX | GPIO 16 (RX2) |
| RX | GPIO 17 (TX2) |

**Step 5: Flash Firmware**

- Use the [Spacehuhn Web Updater](https://esp.huhn.me/) or Arduino IDE (see [Section 6](#6-firmware-flashing----all-methods))

**Step 6: Verify and Test**

- Power on; the ILI9341 should display the Marauder boot screen
- Test touch calibration
- Verify SD card detection in settings

### Build Path 3: Official Marauder Kit

**Step 1: Unbox Kit**

- 1x Marauder Kit PCB with 3D-printed enclosure
- 4x M2.5 x 9mm hex screws
- Brass threaded inserts pre-installed

**Step 2: Prepare Huzzah32**

- Purchase [Adafruit Huzzah32](https://www.adafruit.com/product/3405) separately
- Solder the included header pins to the Huzzah32

**Step 3: Flash Firmware onto Huzzah32**

- Flash the `_kit.bin` firmware using [Spacehuhn Web Updater](https://esp.huhn.me/) before assembly

**Step 4: Assemble**

1. Insert Huzzah32 into the Kit PCB header sockets
2. Connect 3.7V LiPo battery to the Huzzah32's JST connector (power switch OFF first)
3. Secure battery inside enclosure with double-sided tape
4. Mount PCB to enclosure with the 4 screws, TFT facing outward

---

## 6. Firmware Flashing -- All Methods

### Method 1: Web Flasher (Easiest -- Recommended)

**For CYD boards:**

- URL: https://marautech.github.io/ESP32-Cyd-Marauder-WebFlasher/
- Browser: Chrome or Edge only
- Process: Connect > Select board > Select firmware > Install

**For Official Marauder hardware:**

- URL: https://esp.huhn.me/ (Spacehuhn Web Updater)
- Upload 4 files at specific memory addresses:
  - Bootloader at `0x1000` (or `0x0` for MultiBoard S3)
  - Partitions at `0x8000`
  - Boot App at `0xE000`
  - Firmware at `0x10000`

**For various boards:**

- [FZEE Flasher](https://fzeeflasher.com/)
- [ESP Terminator](https://espterminator.com/)

**Firmware Binary Selection by Hardware:**

| Hardware | Binary File |
|----------|-------------|
| v4 (Original) | `_old_hardware.bin` |
| v6 | `_new_hardware.bin` or `_v6.bin` |
| v6.1/v6.2 | `_v6_1.bin` |
| v7 | `_v7.bin` |
| v8 | `_v8.bin` |
| Kit | `_kit.bin` |
| Mini | `_mini.bin` |
| Mini v3 (C5) | `_mini_v3.bin` |
| Flipper Zero Dev Board | `_flipper.bin` |
| MultiBoard S3 | `_multiboardS3.bin` |
| LDDB/NodeMCU/Wemos | `_lddb.bin` |
| Dev Board Pro / BFFB | `_marauder_dev_board_pro.bin` |
| Rev Feather | `_rev_feather.bin` |
| CYD 2432S028(R) | `_cyd_2432S028.bin` |
| CYD 2432S028 2USB | `_cyd_2432S028_2usb.bin` |
| CYD Guition 2.4" | `_cyd_2432S024_guition.bin` |
| M5Cardputer | `_m5cardputer.bin` |
| ESP32-C5 DevKit | `_esp32c5_devkit.bin` |
| AWOK V2/V3 (white USB) | `_v6_1.bin` |
| AWOK V2 (orange USB) | `_flipper.bin` |
| AWOK V3 (orange USB) | `_marauder_dev_board_pro.bin` |

### Method 2: esptool.py (Command Line)

```bash
pip install esptool

esptool.py --chip esp32 --port COM3 --baud 115200 write_flash \
  0x1000 bootloader.bin \
  0x8000 partitions.bin \
  0xE000 boot_app0.bin \
  0x10000 esp32_marauder_vX.X.X_hardware.bin
```

Replace `COM3` with your actual port and select the correct firmware binary.

### Method 3: Arduino IDE (Build from Source)

1. Install Arduino IDE 2.x
2. Add ESP32 board support: File > Preferences > Additional Board Manager URLs:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Install "ESP32 by Espressif" from Board Manager
4. Install required libraries:
   - TFT_eSPI (configure User_Setup.h for your display)
   - lv_arduino (NOT "lvgl")
   - ESPAsyncWebServer
   - ArduinoJson
   - LinkedList
   - SwitchLib
5. Clone the ESP32Marauder repository
6. Open the `.ino` file in Arduino IDE
7. Select board: "ESP32 Dev Module" (or matching board)
8. Set partition scheme: "Minimal SPIFFS (Large APP)"
9. Set upload speed: 115200
10. Compile and upload

### Method 4: SD Card Update

- Place the firmware `.bin` file on the root of the SD card
- Use the device's built-in "Update Firmware" menu option
- Select the file and apply

### Method 5: OTA (Over-The-Air)

1. Flash MarauderOTA firmware first
2. Connect to the Marauder's WiFi AP
3. Navigate to the OTA web interface
4. Upload the new firmware binary

---

## 7. Usage Guide for Each Feature

### WiFi Scanning

**Scan Access Points:**

- Navigate: WiFi > Scan > Scan APs
- CLI: `scanap`
- The device scans all WiFi channels and lists discovered APs with SSID, BSSID, channel, RSSI, and encryption
- After scanning, select target APs for attacks using `select` or the touchscreen

**Scan Stations:**

- Navigate: WiFi > Sniffers > Station Sniff
- CLI: `sniffsta`
- Discovers client devices connected to APs

### Deauthentication Attacks

**Deauth Flood (all clients):**

1. Run `scanap` to discover APs
2. Select target(s): `select -a` (all) or tap specific APs
3. Navigate: WiFi > Attacks > Deauth Flood
4. CLI: `attack -t deauth`
5. All clients on the selected AP receive deauth frames and disconnect

**Deauth Targeted (specific clients):**

1. Run `scanap` then `sniffsta` to find specific clients
2. Select target stations
3. Navigate: WiFi > Attacks > Deauth Targeted
4. CLI: `attack -t deauth -c targeted`

### Beacon Spam

**From list:**

1. First generate SSIDs: WiFi > General > Generate SSIDs (or `ssid -g 50`)
2. Navigate: WiFi > Attacks > Beacon Spam List
3. CLI: `attack -t beacon -l`

**Random / Rick Roll:**

- Navigate: WiFi > Attacks > Beacon Spam Random or Rick Roll Beacon
- CLI: `attack -t beacon -r` or `attack -t beacon -rr`

**AP Clone:**

1. Scan APs first, select target
2. WiFi > Attacks > AP Clone Spam
3. Creates multiple copies of the selected AP's SSID

### Evil Portal

**Setup:**

1. Prepare SD card with `/index.html` file (download templates from [bigbrodude6119's GitHub repo](https://github.com/bigbrodude6119/flipper-zero-evil-portal) or create your own)
2. Optionally create `/ap.config.txt` with desired AP name (e.g., "Free_WiFi")
3. Insert SD card into device
4. Scan and select a target AP (optional, for SSID cloning)
5. Navigate: WiFi > Attacks > Evil Portal, or CLI: `evilportal -c start`
6. To use a specific HTML template: `evilportal -c start -w CoxWifi.html`
7. Enable EPDeauth setting to simultaneously deauth the legitimate AP
8. Monitor serial output / screen for captured credentials
9. Stop: tap screen or `stopscan`

### PMKID / Handshake Capture

1. Enable SavePCAP in settings (or CLI: `settings -s SavePCAP enable`)
2. Insert formatted SD card
3. Run: WiFi > Sniffers > EAPOL/PMKID Scan, or CLI: `sniffpmkid`
4. Optionally enable ForcePMKID to auto-deauth for faster capture
5. Captured PMKID/EAPOL data saves to `.pcap` file on SD card
6. Transfer `.pcap` to PC, open in Wireshark
7. Crack with hashcat:
   ```bash
   hashcat -m 22000 capture.pcap wordlist.txt
   ```

### Packet Monitor / Raw Capture

- Navigate: WiFi > Sniffers > Packet Monitor
- CLI: `sniffraw` for raw capture
- With SD card + SavePCAP enabled, all frames are saved as `.pcap`

### BLE Attacks

**Sour Apple (iOS crash):**

- Navigate: Bluetooth > Attacks > Sour Apple
- CLI: `bleattack -t sour_apple`
- Sends continuous BLE pop-ups to nearby Apple devices running iOS 17

**Swiftpair Spam (Windows):**

- Bluetooth > Attacks > Swiftpair Spam
- CLI: `bleattack -t swiftpair`
- Generates 1,000+ pairing notifications/minute on Windows devices

**Samsung / Google BLE Spam:**

- Same navigation pattern, select respective target
- CLI: `bleattack -t samsung` or `bleattack -t google`

**BLE Spam All:**

- Runs all BLE spam attacks simultaneously

### Bluetooth Scanning and Detection

**Card Skimmer Detection:**

- Bluetooth > Sniffers > Detect Card Skimmers
- Scans for BLE devices matching known skimmer signatures

**General BT Sniffing:**

- Bluetooth > Sniffers > Bluetooth Sniffer
- Captures and identifies nearby Bluetooth devices

### Wardriving (with GPS module)

1. Ensure GPS module is wired and functional
2. Insert SD card
3. Run AP scan -- GPS coordinates are logged alongside each discovered AP
4. Export data for mapping in tools like Wigle

---

## 8. Troubleshooting

### Flashing Problems

| Problem | Solution |
|---------|----------|
| Device not detected by PC | Install CP2102 or CH340 USB-UART drivers; try a different USB cable (must be data-capable, not charge-only) |
| Web flasher won't connect | Hold BOOT button, press RST, release RST (screen goes blank), then click Connect in the flasher |
| "Failed to connect" in esptool | Hold BOOT (GPIO0) while connecting; try lower baud rate (115200) |
| Flashing succeeds but no boot | Wrong firmware binary for your hardware; verify exact board model and re-flash correct binary |
| Browser not supported | Use Chrome or Edge only; Firefox and Safari lack WebSerial support |

### Display Problems

| Problem | Solution |
|---------|----------|
| White/blank screen after flash | Wrong firmware binary; or User_Setup.h not configured if building from source. Copy correct User_Setup.h into TFT_eSPI library folder |
| Black screen on startup | Rare firmware corruption; re-flash from scratch via Arduino IDE or web flasher |
| Touch not working / inverted | Wrong firmware revision for hardware version; older models need `_old_hardware.bin`, newer need `_new_hardware.bin` |
| Display flickers or artifacts | Check SPI wiring; verify 3.3V power stability |

### SD Card Problems

| Problem | Solution |
|---------|----------|
| SD card not detected | Must be 32GB or smaller; format as FAT32; use SanDisk brand (Samsung cards cause boot failures on some boards) |
| PCAPs not saving | Enable SavePCAP in settings; run `settings -r` to reset if needed; verify SD card is properly formatted |
| Device won't boot with SD inserted | Try a different brand/size SD card; some cards pull too much power at boot |

### Software / Compilation Errors

| Error | Solution |
|-------|----------|
| `multiple ieee80211_raw_frame_sanity_check` | Follow Arduino IDE setup steps exactly; check dependency configuration |
| LVGL compilation errors | Install "lv_arduino" library, NOT "lvgl" |
| LinkedList 'size' member missing | Install correct version of ESPAsyncWebServer per official guide |
| TFT_eSPI setTouch/getTouch errors | Copy User_Setup.h to TFT_eSPI library folder |

### OTA Update Problems

| Problem | Solution |
|---------|----------|
| Cannot connect to MarauderOTA AP | Change SSID and password in OTA code before uploading; refresh update page immediately after loading |
| Firmware reverts after power cycle | Follow MarauderOTA steps precisely (especially steps 5, 13, 16); try alternative flash method |

### General Tips

- Always update to firmware v0.9.15 or later before troubleshooting
- When in doubt, fully erase flash first:
  ```bash
  esptool.py --chip esp32 --port COM3 erase_flash
  ```
- Check [GitHub Issues](https://github.com/justcallmekoko/ESP32Marauder/issues) for your specific error before opening a new one

---

## 9. Legal Considerations

### Authorization is Mandatory

Using ESP32 Marauder against any network or device you do not own or have explicit written permission to test is **illegal** in virtually every jurisdiction.

**Applicable Laws:**

- **United States:** Computer Fraud and Abuse Act (CFAA), 18 U.S.C. 1030 -- unauthorized access to computer systems carries federal criminal penalties. FCC regulations prohibit intentional interference with licensed radio communications.
- **European Union:** EU Directive on Attacks Against Information Systems (2013/40/EU); individual country laws (e.g., UK Computer Misuse Act 1990).
- **Canada:** Criminal Code Section 342.1 (unauthorized use of computer).
- **General:** Most countries have laws criminalizing unauthorized network access, interception of communications, and denial-of-service attacks.

**What You CAN Do Legally:**

- Test your own personal networks and devices
- Conduct authorized penetration tests with written scope agreements
- Use in isolated lab environments with no third-party exposure
- Educational research on networks you control
- Defensive monitoring of your own infrastructure (deauth detection, rogue AP detection, skimmer scanning)

**What You CANNOT Do:**

- Deauth other people's networks without written authorization
- Capture credentials via Evil Portal on public or unauthorized networks
- Capture handshakes/PMKID from networks you don't own
- BLE spam public areas (can constitute harassment or disruption)
- Wardrive and publish results revealing private network locations (privacy concerns)
- Use beacon spam to impersonate legitimate businesses or services

**Best Practices for Authorized Testing:**

1. Obtain signed written authorization specifying exact scope, timeframe, and methods
2. Document everything -- timestamps, targets, methods used, results
3. Only test within the agreed scope
4. Report all findings to the authorizing party
5. Securely delete captured data after engagement completion
6. Never store captured credentials longer than necessary

**Consequences of Unauthorized Use:**

- Criminal prosecution (felony charges in many jurisdictions)
- Civil liability for damages
- Fines ranging from thousands to hundreds of thousands of dollars
- Imprisonment (up to 10+ years for serious CFAA violations)
- Permanent criminal record

---

## 10. All Resource Links

### Official Resources

- **GitHub Repository:** https://github.com/justcallmekoko/ESP32Marauder
- **Official Wiki:** https://github.com/justcallmekoko/ESP32Marauder/wiki
- **Getting Started:** https://github.com/justcallmekoko/ESP32Marauder/wiki/getting-started
- **Firmware Releases:** https://github.com/justcallmekoko/ESP32Marauder/releases
- **Update Firmware Guide:** https://github.com/justcallmekoko/ESP32Marauder/wiki/update-firmware
- **Official Store:** https://justcallmekokollc.com
- **FAQ:** https://github.com/justcallmekoko/ESP32Marauder/wiki/faq
- **Evil Portal Wiki:** https://github.com/justcallmekoko/ESP32Marauder/wiki/evilportal
- **Evil Portal Workflow:** https://github.com/justcallmekoko/ESP32Marauder/wiki/evil-portal-workflow
- **Attack Documentation:** https://github.com/justcallmekoko/ESP32Marauder/wiki/attack
- **WiFi Sniffers Wiki:** https://github.com/justcallmekoko/ESP32Marauder/wiki/wifi-sniffers
- **GPS Modification Guide:** https://github.com/justcallmekoko/ESP32Marauder/wiki/gps-modification
- **Marauder Versions:** https://github.com/justcallmekoko/ESP32Marauder/wiki/marauder-versions
- **Marauder Kit:** https://github.com/justcallmekoko/ESP32Marauder/wiki/esp32-marauder-kit
- **Marauder v8:** https://github.com/justcallmekoko/ESP32Marauder/wiki/Marauder-v8

### Web Flashers

- **Spacehuhn Web Updater:** https://esp.huhn.me/
- **CYD Marauder Web Flasher:** https://marautech.github.io/ESP32-Cyd-Marauder-WebFlasher/
- **FZEE Flasher:** https://fzeeflasher.com/
- **VoyagerRF Web Flasher:** https://kashmir54.github.io/voyagerrf/

### CYD (Cheap Yellow Display) Resources

- **CYD Marauder GitHub (Fr4nkFletcher):** https://github.com/Fr4nkFletcher/ESP32-Marauder-Cheap-Yellow-Display
- **CYD Pinout Reference:** https://randomnerdtutorials.com/esp32-cheap-yellow-display-cyd-pinout-esp32-2432s028r/
- **CYD Getting Started:** https://randomnerdtutorials.com/cheap-yellow-display-esp32-2432s028r/

### Build Guides and Tutorials

- **Targeted Tech Talk Build Guide:** https://www.targetedtechtalk.com/2025/07/20/esp32-marauder-build/
- **DevGodz DIY Guide:** https://devgodz.com/blog/build-your-own-esp32-marauder-a-diy-guide-1764802301
- **PWS Controls Step-by-Step:** https://pwscontrols.com/blog/build-your-own-esp32-marauder
- **Hackster.io DIY Project:** https://www.hackster.io/Electrodude/diy-esp32-marauder-wifi-testing-security-research-tool-e1a0dc
- **Deca's Foxhole CYD Guide:** https://decasfoxhole.wordpress.com/diy-esp32-marauder-with-cheap-yellow-display/
- **e1z0 DIY Guide (GitHub):** https://github.com/e1z0/ESP32Marauder-DIY/blob/master/guide/guide.md
- **Biscuit Shop Complete Tools Guide:** https://biscuitshop.us/blogs/how-to-guides/every-tool-esp32-marauder
- **Ultimate Guide (Deca's Foxhole):** https://decasfoxhole.wordpress.com/2025/11/15/ultimate-esp32-marauder-guide-wi-fi-bluetooth-hacking-tools-explained/

### Flipper Zero Integration

- **Flipper Community Wiki -- Installing Marauder:** https://flipper.wiki/tutorials/Marauder_guide/guide/
- **Flipper Lab App:** https://lab.flipper.net/apps/esp32_wifi_marauder
- **Flipper Marauder Portal Guide:** https://github.com/L-ubu/flipper-portals/blob/main/MARAUDER-GUIDE.md

### Third-Party Hardware

- **Double Barrel 5G (HoneyHoney):** https://github.com/HoneyHoneyTeam/ESP32-Marauder-Double-Barrel
- **Sacred Labs Ultra V3:** https://sacredlabstech.com/boards/ultra-v3/
- **DeepWiki Board Matrix:** https://deepwiki.com/justcallmekoko/ESP32Marauder/5.1-supported-boards-and-variants

### Parts and Purchase

- **Adafruit Huzzah32:** https://www.adafruit.com/product/3405
- **Amazon ESP32 Marauder Search:** https://www.amazon.com/esp32-marauder/s?k=esp32+marauder
- **eBay Listings:** https://www.ebay.com/shop/esp32-marauder
- **Biscuit Shop Battery+GPS Kit:** https://biscuitshop.us/products/esp32-marauder-battery-mod-kit
- **Elecrow CYD Upgrade Kit:** https://www.elecrow.com/cyd-2-8-marauder-bruce-battery-gps-mod-diy-kit.html
- **Tindie Listings:** https://www.tindie.com/products/ovvys/esp32-marauder-device/

### Video Guides

- **Build Your Own Wi-Fi Hacking Tool (ESP32 Marauder):** https://youtu.be/lcokJQMivwY
- **ESP32 Marauder Guide:** https://youtu.be/Co5FG3ivHhg

### Tools and Utilities

- **Wireshark (PCAP analysis):** https://www.wireshark.org/
- **hashcat (password cracking):** https://hashcat.net/hashcat/
- **aircrack-ng:** https://www.aircrack-ng.org/
- **esptool.py:** https://github.com/espressif/esptool
- **ArduinoPcap Library:** https://github.com/spacehuhn/ArduinoPcap

---

## 11. Best-Fit Hardware from Your Inventory

### Recommended Build

| Component | Assignment | Why |
|-----------|-----------|-----|
| **Board** | Lonely Binary ESP32 Gold Edition #1 | IPEX/U.FL antenna connector for external antenna. Best WiFi range of all boards in inventory. CH340 USB well-supported for flashing |
| **Display** | ESP32 2.8" CYD Touchscreen #1 (Sunton, ILI9341) | Marauder has native CYD support with full touch GUI. Compact and field-portable. Can run standalone OR pair with the Gold board as serial display |
| **Antenna** | DIYmall 2.4G WiFi Antenna #1 + U.FL pigtail cable | Connects directly to the Lonely Binary IPEX connector. 3dBi omnidirectional for broad area scanning |
| **Storage** | 128GB Micro SD Card (Lerdisk U3/A1/V30) #1 | For PCAP capture during extended scanning sessions |
| **Prototyping** | AEDIKO ESP32 GPIO Breakout Board #1 | Useful during initial flashing and development |

### External Antenna Setup

Your Lonely Binary ESP32 Gold Edition has a built-in IPEX/U.FL connector -- **no soldering required**.

**Connection chain:**
```
Lonely Binary ESP32 [IPEX socket]
    │
    ▼
DIYmall U.FL Pigtail Cable (14cm, 1.13mm coax)
    │
    ▼
SMA Female end of pigtail
    │
    ▼
Boobrie RP-SMA to SMA Adapter (if using Bingfu antenna)
    │
    ▼
Bingfu 2.4/5.8GHz RP-SMA Antenna (3dBi dual-band)
```

**Steps:**
1. Locate the small gold IPEX connector on the Lonely Binary board (near the ESP32 module RF section)
2. Align the DIYmall U.FL connector directly over it
3. Press straight down firmly until you hear/feel a click
4. Route the pigtail away from the board (5mm+ bend radius)
5. Connect antenna to the SMA end (use Boobrie adapter if connecting RP-SMA Bingfu antenna)

**Important:** U.FL connectors are rated for ~30 mating cycles. Treat as semi-permanent. Cable loss at 14cm is ~0.3dB -- negligible.

### Antenna Upgrades for Extended Range

| Antenna Type | Gain | Best For | Est. Price |
|-------------|------|----------|-----------|
| Your DIYmall 3dBi omni | 3dBi | General scanning, indoor | Already owned |
| 5dBi omnidirectional RP-SMA | 5dBi | Balanced range/coverage outdoors | ~$8-12 |
| 9dBi magnetic-base omni | 9dBi | Vehicle wardriving (roof mount) | ~$12-18 |
| Directional panel (60-90°) | 8-14dBi | Targeted building scanning | ~$15-25 |
| Yagi directional (30-45°) | 12-18dBi | Long-range point-to-point | ~$20-35 |

### Upgrade Recommendations

| Component | Upgrade To | Price | Improvement |
|-----------|-----------|-------|-------------|
| Board | Lonely Binary ESP32-S3 IPEX (16MB flash, 8MB PSRAM) | ~$15 | More memory for larger captures, dual USB-C, same IPEX connector |
| Board | Marauder Mini (official hardware) | ~$45-65 | Purpose-built: 1.44" screen, GPS, LiPo battery, IPEX antenna, SD slot |
| Board | Double Barrel 5G (C5 V2) | ~$80-120 | Dual Marauder systems, ESP32-C5 for 5GHz WiFi, GPS, Sub-GHz, 4 antennas |
| Display | Marauder v7/v8 touchscreen | ~$60-90 | Full-featured touchscreen Marauder with GPS and battery |
| Antenna | 9dBi magnetic-base omni | ~$12-18 | 3x range improvement for wardriving |

### CYD Antenna Modification (Optional)

If running Marauder on the CYD standalone (without the Lonely Binary board), you can add an external antenna:

**Method (Direct pigtail solder -- Fr4nkFletcher guide):**
1. Cut U.FL connector off a pigtail cable, exposing ~5mm of center conductor and shield
2. Tin both wires with solder
3. Solder center conductor to the CYD ESP32 module's antenna feed point
4. Solder shield to nearby ground pad
5. Connect RP-SMA antenna to the other end

**Difficulty:** Intermediate. Requires soldering iron, flux, magnification. See [Fr4nkFletcher AntennaMod guide](https://github.com/Fr4nkFletcher/ESP32-Marauder-Cheap-Yellow-Display/blob/master/AntennaMod.md) and [YouTube tutorial](https://www.youtube.com/watch?v=CFhwLVzeMFA).

**Recommendation:** Use the Lonely Binary Gold board as the main processor with CYD as display instead -- avoids the mod entirely and gives better range.

---

## 12. Feature Brainstorm -- What Else Can This Do

- **Dual-band attack coordination** -- Run a Gold board on 2.4GHz and an ESP32-C5 on 5GHz simultaneously, covering both bands during scans and deauths from a single operator station
- **Automated PMKID farm** -- Script a scan-deauth-capture-save loop via serial CLI on the Pi 5 that continuously cycles through discovered APs, captures PMKID/EAPOL, and auto-exports to hashcat-ready format
- **Evil Portal template library** -- Build a collection of cloned captive portal pages (hotel WiFi, airline WiFi, corporate guest networks) stored on SD card, selectable per engagement
- **Wireshark-ready PCAP export pipeline** -- Write a Pi 5 script that pulls PCAPs from the SD card via serial, timestamps and organizes them by target SSID, and opens them directly in Wireshark or tshark for immediate analysis
- **Custom SD card directory structure** -- Create organized folders on the SD card (e.g., `/captures/pmkid/`, `/captures/handshakes/`, `/evil-portal/templates/`, `/logs/wardrive/`) so captures from different sessions stay separated and searchable
- **Marauder CLI automation scripts** -- Write Python scripts on the Pi 5 that send serial commands to automate common workflows: scan all APs, select by RSSI threshold, run targeted deauth for N seconds, stop and save
- **Signal strength heatmapping** -- Combine wardriving GPS data with RSSI readings to generate WiFi signal heatmaps of a target area using tools like Wigle or custom matplotlib plots
- **Channel utilization analyzer** -- Scan all 14 channels and log packet counts per channel over time, producing a channel congestion report to identify the quietest channels for your own use or the busiest for target-rich scanning
- **Rogue AP detection mode** -- Run Marauder in continuous scan mode to detect new or unexpected APs appearing on your own network, alerting via the Pi 5 dashboard when an unknown BSSID shows up
- **Multi-board coordinated scanning** -- Use a Gold board for 2.4GHz AP scanning and a C5 for 5GHz scanning simultaneously, merging results on the Pi 5 into a single unified target list
- **BLE tracker sweep** -- Periodically scan for AirTags, Tiles, and unknown BLE beacons in your vicinity, logging MAC addresses and timestamps to detect persistent trackers following your location
- **Deauth detection alarm** -- Run the Deauth Sniff feature continuously as a defensive IDS, triggering an audible or visual alert on the CYD screen when someone is deauthing your own network

---

## 13. Cyberdeck Integration

> See [Project 14: Cyberdeck](../14-cyberdeck/) for the full build plan.

### Role in the Cyberdeck

ESP32 Marauder is the **primary WiFi/BLE offensive tool** in the cyberdeck. It runs on Lonely Binary Gold #1 with the CYD 2.8" as its dedicated touchscreen interface.

### Physical Setup

- **Board:** Lonely Binary Gold #1, mounted on the ESP32 rail via M3 standoffs
- **Display:** CYD 2.8" mounted face-up in the base, connected via serial to the Gold board
- **Antenna:** IPEX → U.FL pigtail → SMA bulkhead #1 (labeled "MAR") → external 2.4GHz antenna
- **Power:** USB from the powered hub (toggle switch #1 controls power)
- **Data:** USB serial to Pi 5 via hub — Pi reads scan results and forwards to the dashboard

### Serial Communication with Pi 5

Marauder supports serial commands at **115200 baud**. The Pi 5 connects via `/dev/ttyUSBx` and can:

- Send commands: `scanap`, `scansta`, `stopscan`, `attack -t deauth`, etc.
- Read scan output: AP lists, station lists, PMKID captures
- The cyberdeck dashboard parses this output in real time

### Firmware

Flash via [ESP Terminator](https://espterminator.com) web flasher or [Marauder OTA](https://github.com/justcallmekoko/ESP32Marauder/wiki/update-firmware). Select the **ESP32-WROOM** variant for the Lonely Binary Gold.

### Standalone vs Integrated

| Mode | How |
|------|-----|
| **Standalone** | CYD touchscreen provides full Marauder GUI. No Pi needed. Toggle on Marauder switch only |
| **Integrated** | Pi 5 sends serial commands and aggregates results into the cyberdeck dashboard alongside all other tools |
