# Cyberdeck Firmware Reference

Master firmware reference for all devices and software across the cyberdeck project ecosystem. Covers ESP32-family firmwares, Raspberry Pi images, Flipper Zero custom firmware, and companion software tools.

Last updated: 2026-06-09

---

## Quick-Reference Summary

| # | Firmware | Version | Board(s) | Flash Method | GitHub Repo |
|---|----------|---------|----------|--------------|-------------|
| 1 | ESP32 Marauder | v1.12.1 | ESP32, ESP32-S3, ESP32-C5, CYD | esptool / Web Flasher | [justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder) |
| 2 | GhostESP | VA1.4.8 | ESP32/S3/C5/C6, CYD, GhostBoard, M5 Cardputer | Web Serial / esptool | [Spooks4576/Ghost_ESP](https://github.com/Spooks4576/Ghost_ESP) |
| 3 | Bruce | 1.15 | M5 Cardputer, StickC, T-Deck, T-Embed, CYD, Awok, Nesso, CYD-C5 | Web Flasher / esptool | [BruceDevices/firmware](https://github.com/BruceDevices/firmware) |
| 4 | HaleHound-CYD | v3.5.5 | CYD 2.8", NM-RF-Hat, QDtech, 3.5" Cap | ESP Web Flasher / esptool | [JesseCHale/HaleHound-CYD](https://github.com/JesseCHale/HaleHound-CYD) |
| 5 | Meshtastic | v2.7.22 | Heltec WiFi LoRa 32 V3 + 50 others | Web Flasher / esptool | [meshtastic/firmware](https://github.com/meshtastic/firmware) |
| 6 | Pwnagotchi (jayofelony) | v2.9.5.4 | Pi Zero 2W | SD card image | [jayofelony/pwnagotchi](https://github.com/jayofelony/pwnagotchi) |
| 7 | Flock-You | rolling | XIAO ESP32-S3, ESP32 classic | PlatformIO / Arduino IDE | [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you) |
| 8 | OUI-Spy Unified Blue | rolling | LILYGO T-Display S3, XIAO ESP32-S3 | PlatformIO | [colonelpanichacks/oui-spy-unified-blue](https://github.com/colonelpanichacks/oui-spy-unified-blue) |
| 9 | Sky-Spy | rolling | ESP32-S3, ESP32-C6 | PlatformIO / Arduino IDE | [colonelpanichacks/Sky-Spy](https://github.com/colonelpanichacks/Sky-Spy) |
| 10 | ESP32-DIV | v1.5.3 | ESP32-S3 | Arduino IDE / esptool | [cifertech/ESP32-DIV](https://github.com/cifertech/ESP32-DIV) |
| 11 | RaspyJack | v1.0.6 | Pi Zero 2W + Waveshare 1.44" LCD HAT | SD card + install script | [7h30th3r0n3/Raspyjack](https://github.com/7h30th3r0n3/Raspyjack) |
| 12 | RayHunter | v0.11.2 | Orbic RC400L | Installer script (WiFi/ADB) | [EFForg/rayhunter](https://github.com/EFForg/rayhunter) |
| 13 | Chasing Your Tail NG | rolling | Any Linux host (software) | pip / clone | [ArgeliusLabs/Chasing-Your-Tail-NG](https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG) |
| 14 | ESP32 AirTag Scanner | rolling | ESP32/S3, CYD | Arduino IDE | [MatthewKuKanich/ESP32-AirTag-Scanner](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner) |
| 15a | Flipper Momentum | MNTM-012 | Flipper Zero (f7) | qFlipper / Web Updater | [Next-Flip/Momentum-Firmware](https://github.com/Next-Flip/Momentum-Firmware) |
| 15b | Flipper Unleashed | unlshd-089 | Flipper Zero (f7) | qFlipper | [DarkFlippers/unleashed-firmware](https://github.com/DarkFlippers/unleashed-firmware) |
| 16 | Kismet | 2025-09-R1 | Any Linux host (software) | apt / compile from source | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) |

---

## Detailed Firmware Entries

---

### 1. ESP32 Marauder

- **Version:** v1.12.1
- **GitHub:** https://github.com/justcallmekoko/ESP32Marauder
- **Supported Boards:**
  - ESP32 classic (WROOM/DevKit)
  - ESP32-S3: v6, v6.1, v7, MultiBoardS3, Lonely Binary Gold
  - ESP32-C5: v8 (dual-band 2.4/5 GHz)
  - CYD: community forks only (Fr4nkFletcher, Tony7466)
- **Flash Method:** esptool.py or Marauder Web Flasher
- **Binary Naming:** `esp32_marauder_v{X}_{Y}_{Z}_{DATE}_{BOARD}.bin`
- **Download:** https://github.com/justcallmekoko/ESP32Marauder/releases
- **Flash Command (esptool):**
  ```
  esptool.py --chip esp32 --port COM# --baud 115200 write_flash 0x0 esp32_marauder_v{version}_{board}.bin
  ```
- **CYD Fork (Fr4nkFletcher):** https://github.com/Fr4nkFletworker/ESP32-Marauder-Cheap-Yellow-Display
- **CYD Fork (Tony7466):** https://github.com/Tony7466/ESP32Marauder
- **Notes:** The primary WiFi/BLE offensive tool in the ecosystem. Gold boards refer to the classic ESP32, NOT S3 variants.

---

### 2. GhostESP

- **Version:** VA1.4.8
- **GitHub:** https://github.com/Spooks4576/Ghost_ESP
- **Revival Fork:** https://github.com/GhostESP-Revival
- **Supported Boards:**
  - ESP32 classic, ESP32-S3, ESP32-C5, ESP32-C6
  - CYD (Cheap Yellow Display)
  - GhostBoard (dedicated hardware)
  - M5 Cardputer
- **Flash Method:** Web Serial at https://flasher.ghostesp.net or esptool.py
- **Binary Files:** Board-specific set of three files:
  - `bootloader.bin`
  - `partitions.bin`
  - `GhostESP.bin`
- **Download:** https://github.com/Spooks4576/Ghost_ESP/releases
- **Flash Command (esptool):**
  ```
  esptool.py --chip esp32s3 --port COM# --baud 460800 write_flash \
    0x0 bootloader.bin \
    0x8000 partitions.bin \
    0x10000 GhostESP.bin
  ```
- **Notes:** Multi-protocol offensive tool. The Revival fork maintains community patches when upstream is inactive.

---

### 3. Bruce

- **Version:** 1.15
- **GitHub:** https://github.com/BruceDevices/firmware
- **Supported Boards:**
  - M5 Cardputer
  - M5 StickC / StickC Plus
  - LILYGO T-Deck
  - LILYGO T-Embed
  - CYD variants (2.8", 3.5", capacitive)
  - Awok
  - Arduino Nesso
  - CYD-C5 (ESP32-C5 based)
- **Flash Method:** Web Flasher at https://bruce.computer/flasher or esptool.py
- **Binary Naming:** `Bruce-{device}.bin`
- **Download:** https://github.com/BruceDevices/firmware/releases
- **Flash Command (esptool):**
  ```
  esptool.py --chip esp32s3 --port COM# --baud 921600 write_flash 0x0 Bruce-{device}.bin
  ```
- **Notes:** All-in-one offensive firmware. Supports WiFi, BLE, IR, RFID, SubGHz (with CC1101), BadUSB, and more depending on hardware.

---

### 4. HaleHound-CYD

- **Version:** v3.5.5
- **GitHub:** https://github.com/JesseCHale/HaleHound-CYD
- **Supported Boards:**
  - CYD 2.8" (ESP32-2432S028)
  - NM-RF-Hat
  - QDtech variants
  - 3.5" Capacitive
- **Flash Method:** ESP Web Flasher or esptool.py at address `0x0`
- **Binary Naming:** `HaleHound-CYD-FULL.bin` (merged binary, flash at 0x0) or board-specific binaries
- **Download:** https://github.com/JesseCHale/HaleHound-CYD/releases
- **Flash Command (esptool):**
  ```
  esptool.py --chip esp32 --port COM# --baud 460800 write_flash 0x0 HaleHound-CYD-FULL.bin
  ```
- **Notes:** Merged binary simplifies flashing -- single file at 0x0, no separate bootloader/partition files needed.

---

### 5. Meshtastic

- **Version:** v2.7.22
- **GitHub:** https://github.com/meshtastic/firmware
- **Supported Boards:**
  - Heltec WiFi LoRa 32 V3 (primary in this project)
  - 50+ other boards (T-Beam, T-Echo, RAK, Station G2, etc.)
- **Flash Method:** Web Flasher at https://flasher.meshtastic.org or esptool.py
- **Binary Naming:** `firmware-heltec-wsl-v3-{version}.bin`
- **Download:** https://github.com/meshtastic/firmware/releases
- **Flash Command (esptool):**
  ```
  esptool.py --chip esp32s3 --port COM# --baud 921600 write_flash 0x0 firmware-heltec-wsl-v3-{version}.bin
  ```
- **Notes:** LoRa mesh networking firmware. Used in the cyberdeck for off-grid encrypted comms. Configure via Meshtastic app (Android/iOS/desktop) or CLI.

---

### 6. Pwnagotchi (jayofelony fork)

- **Version:** v2.9.5.4
- **GitHub:** https://github.com/jayofelony/pwnagotchi
- **Recommended Fork:** jayofelony (actively maintained, recommended over original)
- **Supported Boards:** Raspberry Pi Zero 2W
- **Flash Method:** SD card image (.img.xz)
- **Binary Naming:** `pwnagotchi-{version}-arm64.img.xz`
- **Download:** https://github.com/jayofelony/pwnagotchi/releases
- **Flash Steps:**
  1. Download `pwnagotchi-{version}-arm64.img.xz`
  2. Flash to microSD with balenaEtcher, Raspberry Pi Imager, or `dd`
  3. Insert SD card into Pi Zero 2W and boot
  4. Access via USB RNDIS (172.0.0.1:8080) or Bluetooth
- **Notes:** AI-powered WiFi handshake capture. The jayofelony fork is the community-recommended version with active development and Pi Zero 2W support.

---

### 7. Flock-You

- **Version:** rolling (no versioned releases)
- **GitHub:** https://github.com/colonelpanichacks/flock-you
- **Supported Boards:**
  - XIAO ESP32-S3 (primary)
  - ESP32 classic (community forks)
- **Flash Method:** PlatformIO or Arduino IDE (compile from source, no prebuilt binaries)
- **Download:** Clone repo and compile
- **Flash Steps:**
  1. Clone: `git clone https://github.com/colonelpanichacks/flock-you.git`
  2. Open in PlatformIO or Arduino IDE
  3. Select board (XIAO ESP32-S3)
  4. Compile and upload
- **Notes:** BLE device spoofing / flooding tool. Source-only distribution -- requires local compilation.

---

### 8. OUI-Spy Unified Blue

- **Version:** rolling (no versioned releases)
- **GitHub:** https://github.com/colonelpanichacks/oui-spy-unified-blue
- **Supported Boards:**
  - LILYGO T-Display S3
  - XIAO ESP32-S3
- **Flash Method:** PlatformIO (source only)
- **5 Operational Modes:**
  1. Detector -- passive BLE scanning
  2. FlockYou -- BLE spoofing/flooding
  3. Foxhunter -- signal direction finding
  4. SkySpy -- drone/UAV detection
  5. Wardrive -- WiFi mapping with GPS
- **OUI Database:** 42 Flock OUI prefixes for device identification
- **Flash Steps:**
  1. Clone: `git clone https://github.com/colonelpanichacks/oui-spy-unified-blue.git`
  2. Open in PlatformIO
  3. Select target board
  4. Compile and upload
- **Notes:** Unified multi-tool combining five separate reconnaissance functions into a single firmware.

---

### 9. Sky-Spy

- **Version:** rolling (no versioned releases)
- **GitHub:** https://github.com/colonelpanichacks/Sky-Spy
- **Supported Boards:**
  - ESP32-S3
  - ESP32-C6
- **Flash Method:** PlatformIO or Arduino IDE (source only)
- **Serial Output:** JSON via serial at 115200 baud
- **Flash Steps:**
  1. Clone: `git clone https://github.com/colonelpanichacks/Sky-Spy.git`
  2. Open in PlatformIO or Arduino IDE
  3. Select board
  4. Compile and upload
- **Notes:** Drone/UAV detection via WiFi and BLE signature analysis. Outputs structured JSON for integration with other tools.

---

### 10. ESP32-DIV

- **Version:** v1.5.3
- **GitHub:** https://github.com/cifertech/ESP32-DIV
- **Supported Boards:** ESP32-S3
- **Flash Method:** Arduino IDE or esptool.py
- **Binary Naming:** `ESP32-DIV-{version}.bin`
- **Download:** https://github.com/cifertech/ESP32-DIV/releases
- **Capabilities:** WiFi, BLE, 2.4 GHz, SubGHz, IR, RFID/NFC, GPS
- **Flash Command (esptool):**
  ```
  esptool.py --chip esp32s3 --port COM# --baud 460800 write_flash 0x0 ESP32-DIV-{version}.bin
  ```
- **Notes:** Multi-protocol all-in-one device. Covers seven signal domains in a single firmware. Requires matching hardware peripherals (CC1101, PN532, GPS module, IR LED) for full functionality.

---

### 11. RaspyJack

- **Version:** v1.0.6
- **GitHub:** https://github.com/7h30th3r0n3/Raspyjack
- **Supported Boards:** Raspberry Pi Zero 2W + Waveshare 1.44" LCD HAT
- **Flash Method:** SD card image + install script
- **Payload Count:** 233 payloads across 13 categories
- **Flash Steps:**
  1. Flash Raspberry Pi OS Lite to microSD
  2. Boot Pi Zero 2W and SSH in
  3. Clone: `git clone https://github.com/7h30th3r0n3/Raspyjack.git`
  4. Run: `cd Raspyjack && ./install_raspyjack.sh`
  5. Reboot
- **Notes:** USB HID attack platform (Rubber Ducky equivalent). The Waveshare 1.44" LCD HAT provides a menu interface for selecting payloads without needing an external display.

---

### 12. RayHunter

- **Version:** v0.11.2
- **GitHub:** https://github.com/EFForg/rayhunter
- **Supported Boards:** Orbic RC400L (mobile hotspot)
- **Flash Method:** Installer script via WiFi or ADB
- **Web UI:** http://192.168.1.1:8080
- **Flash Commands:**
  - **Via WiFi:**
    ```
    ./installer orbic --admin-password 'password'
    ```
  - **Via ADB (USB):**
    ```
    ./installer orbic-usb
    ```
- **Download:** https://github.com/EFForg/rayhunter/releases
- **Notes:** IMSI catcher / cell-site simulator detector by the Electronic Frontier Foundation. Runs on the Orbic RC400L hotspot's onboard Qualcomm modem. Access the web UI over the hotspot's WiFi.

---

### 13. Chasing Your Tail NG

- **Version:** rolling
- **GitHub:** https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG
- **Type:** Software (Python), not firmware
- **Runs On:** Any Linux host
- **Install:**
  ```
  git clone https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG.git
  cd Chasing-Your-Tail-NG
  pip install -r requirements.txt
  ```
- **Integrations:**
  - Kismet (real-time probe capture)
  - WiGLE (geographic correlation)
- **Notes:** WiFi probe request analyzer. Correlates device probe requests with known network databases to map device owner travel patterns. Not firmware -- runs as a Python application on the host system.

---

### 14. ESP32 AirTag Scanner

- **Version:** rolling
- **GitHub:** https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner
- **CYD Fork:** https://github.com/hevnsnt/CYD_ESP32-AirTag-Scanner
- **Related Tool:** Pigtail -- https://github.com/benbaker76/Pigtail (stalker scoring algorithm)
- **Supported Boards:**
  - ESP32 classic
  - ESP32-S3
  - CYD (via hevnsnt fork)
- **Flash Method:** Arduino IDE (compile from source)
- **Flash Steps:**
  1. Clone: `git clone https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner.git`
  2. Open in Arduino IDE
  3. Install ESP32 board package and BLE library
  4. Select board and upload
- **Notes:** Detects nearby Apple AirTags and compatible Find My trackers via BLE. The CYD fork adds touchscreen display support. Pigtail extends detection with a stalker scoring system for threat assessment.

---

### 15a. Flipper Zero -- Momentum Firmware

- **Version:** MNTM-012
- **GitHub:** https://github.com/Next-Flip/Momentum-Firmware
- **Supported Boards:** Flipper Zero (f7)
- **Flash Method:** qFlipper desktop app or Web Updater at https://momentum-fw.dev/update
- **Binary Naming:** `flipper-z-f7-update-mntm-{NNN}.tgz`
- **Download:** https://github.com/Next-Flip/Momentum-Firmware/releases
- **Flash Steps (qFlipper):**
  1. Download `.tgz` release
  2. Connect Flipper via USB
  3. Open qFlipper
  4. Drag `.tgz` onto qFlipper window or use "Install from file"
- **Notes:** Successor to Xtreme firmware (discontinued). Momentum is the actively maintained continuation. Do NOT use Xtreme -- it is no longer updated.

### 15b. Flipper Zero -- Unleashed Firmware

- **Version:** unlshd-089
- **GitHub:** https://github.com/DarkFlippers/unleashed-firmware
- **Supported Boards:** Flipper Zero (f7)
- **Flash Method:** qFlipper desktop app
- **Binary Naming:** `flipper-z-f7-update-unlshd-{NNN}e.tgz`
- **Download:** https://github.com/DarkFlippers/unleashed-firmware/releases
- **Flash Steps (qFlipper):**
  1. Download `.tgz` release
  2. Connect Flipper via USB
  3. Open qFlipper
  4. Drag `.tgz` onto qFlipper window or use "Install from file"
- **Notes:** Long-standing alternative custom firmware. Focuses on removing regional restrictions and adding community apps. The trailing `e` in the binary name indicates the "extra apps" bundle.

---

### 16. Kismet

- **Version:** 2025-09-R1
- **GitHub:** https://github.com/kismetwireless/kismet
- **Type:** Software, not firmware
- **Runs On:** Any Linux host (Debian/Ubuntu, Kali, Raspberry Pi OS)
- **Install (apt):**
  ```
  sudo apt install kismet
  ```
- **Install (from source):**
  ```
  git clone https://github.com/kismetwireless/kismet.git
  cd kismet
  ./configure
  make -j$(nproc)
  sudo make install
  ```
- **Web UI:** http://localhost:2501
- **Notes:** Wireless network detector, sniffer, and IDS. Supports WiFi, Bluetooth, BTLE, Zigbee, and more. Used as the backend capture engine for Chasing Your Tail NG and general wardriving. Not firmware -- runs as a service on the host system.

---

## Flash Method Categories

| # | Method | Tools | Used By |
|---|--------|-------|---------|
| 1 | esptool.py | `pip install esptool` | Marauder, GhostESP, Bruce, HaleHound, Meshtastic, ESP32-DIV |
| 2 | Web Serial API (browser) | Chrome/Edge (WebSerial) | Marauder, GhostESP, Bruce, HaleHound, Meshtastic |
| 3 | SD card image | balenaEtcher, Raspberry Pi Imager, `dd` | Pwnagotchi, RaspyJack |
| 4 | ADB / installer script | ADB, shell script | RayHunter |
| 5 | Arduino IDE / PlatformIO | Arduino IDE, PlatformIO CLI/VS Code | Flock-You, OUI-Spy, Sky-Spy, AirTag Scanner |
| 6 | qFlipper / .tgz package | qFlipper desktop app | Momentum, Unleashed |
| 7 | Package manager / source | apt, make | Kismet |

### esptool.py Quick Reference

Install:
```
pip install esptool
```

Common flags:
```
--chip          Target chip (esp32, esp32s3, esp32c5, esp32c6)
--port          Serial port (COM# on Windows, /dev/ttyUSB# or /dev/ttyACM# on Linux)
--baud          Baud rate (115200, 460800, 921600)
write_flash     Write binary to flash at specified address
erase_flash     Erase entire flash (useful before re-flashing)
```

Erase before flashing (recommended for clean installs):
```
esptool.py --chip esp32 --port COM# erase_flash
```

---

## Discontinued Firmware

| Firmware | Status | Successor |
|----------|--------|-----------|
| Xtreme (Flipper Zero) | Discontinued | Momentum (MNTM-012) |

Do NOT install Xtreme firmware. It is no longer maintained. Use Momentum instead.
