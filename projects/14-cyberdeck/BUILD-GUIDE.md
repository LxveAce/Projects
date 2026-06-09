# Cyberdeck Build Guide -- Complete Step-by-Step

> **Project:** [14 -- The Cyberdeck](README.md)
> **Case:** Pelican 1300 NF (No Foam)
> **Devices:** 14 active boards/modules
> **Switches:** 12 SPST toggles with waterproof boot caps
> **SMA Bulkheads:** 7 panel-mount antenna ports
> **Displays:** 5 total (7" DSI + 2x CYD 2.8" + 2.42" OLED + Heltec built-in)
> **Battery:** Anker 347 25,600mAh USB-C PD
> **OS:** Kali Linux (Pi 5 ARM)

This guide covers the full build from raw components to a sealed, tested cyberdeck. It is
split into two major parts:

- **Part 1** -- flash, configure, and bench-test every individual component before it goes
  into the case. Nothing gets mounted until it is proven working on a desk.
- **Part 2** -- physically assemble the cyberdeck: drill the case, mount the hardware,
  wire everything together, integrate the software, and run acceptance tests.

**Read the entire guide before starting.** Several steps have 24-hour cure times or
firmware prerequisites that block later work if skipped.

---

## Table of Contents

### Part 1: Individual Component Builds
1. [Pi 5 Brain Setup](#1-pi-5-brain-setup)
2. [ESP32 Marauder -- Gold #1 + CYD #1](#2-esp32-marauder----gold-1--cyd-1)
3. [ESP32 Marauder Dual-Band -- C5 #1](#3-esp32-marauder-dual-band----c5-1)
4. [ESP32-C5 #2 -- Dual-Band Scanner](#4-esp32-c5-2----dual-band-scanner)
5. [Flock Detection -- Gold #2](#5-flock-detection----gold-2)
6. [BLE Scanner / Chasing Your Tail -- Gold #3](#6-ble-scanner--chasing-your-tail----gold-3)
7. [Meshtastic -- Heltec LoRa V3](#7-meshtastic----heltec-lora-v3)
8. [HaleHound -- CYD #2](#8-halehound----cyd-2)
9. [Drone RemoteID -- WROOM-32](#9-drone-remoteid----wroom-32)
10. [RaspyJack -- Pi Zero 2W](#10-raspyjack----pi-zero-2w)
11. [RayHunter -- Orbic RC400L](#11-rayhunter----orbic-rc400l)
12. [Pwnagotchi -- Standalone Pocket Device](#12-pwnagotchi----standalone-pocket-device)

### Part 2: Cyberdeck Assembly
- [Phase 1: Case Preparation](#phase-1-case-preparation)
- [Phase 2: Waterproofing](#phase-2-waterproofing)
- [Phase 3: Mounting Plates](#phase-3-mounting-plates)
- [Phase 4: Compute Layer](#phase-4-compute-layer)
- [Phase 5: ESP32 Rail](#phase-5-esp32-rail)
- [Phase 6: Displays](#phase-6-displays)
- [Phase 7: Software Integration](#phase-7-software-integration)
- [Phase 8: Integration Testing](#phase-8-integration-testing)
- [Phase 9: Finishing](#phase-9-finishing)

### Appendix
- [A: Master Wiring Table](#appendix-a-master-wiring-table)
- [B: USB Device Rules (udev)](#appendix-b-usb-device-rules-udev)
- [C: Systemd Service Templates](#appendix-c-systemd-service-templates)
- [D: Troubleshooting](#appendix-d-troubleshooting)

---

# PART 1: Individual Component Builds

Flash and test each device standalone on a workbench before any of it goes into the
Pelican case. Every component must be proven working independently. If something fails
inside the sealed deck, diagnosing it is ten times harder.

**Tools needed for Part 1:**
- A desktop/laptop with USB ports (Windows, Linux, or macOS)
- USB-C and micro-USB data cables (not charge-only -- verify data lines)
- SD card reader
- Arduino IDE (for BLE scanner firmware)
- Chrome or Edge browser (for WebSerial-based flashers)
- Python 3.10+ with pip
- `esptool` installed: `pip install esptool`
- Soldering iron (only needed for optional mods)

---

## 1. Pi 5 Brain Setup

**Board:** Raspberry Pi 5 8GB (CanaKit kit)
**OS:** Kali Linux ARM
**Boot media:** 128GB micro SD card
**Role:** Central brain -- runs Kismet, controls all ESP32s via serial, hosts the Flask
dashboard, aggregates GPS

### 1.1 Flash Kali Linux to SD Card

1. Download the Kali Linux ARM image for Raspberry Pi 5 from
   [kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm). Select the
   **Raspberry Pi 5** image (`.img.xz` file, approximately 3-4 GB compressed).
2. Insert the 128GB micro SD card into your PC's card reader.
3. Open **Raspberry Pi Imager** (download from
   [raspberrypi.com/software](https://www.raspberrypi.com/software/) if not installed).
4. Click **Choose OS** > **Use custom** > select the downloaded Kali `.img.xz` file.
5. Click **Choose Storage** > select the 128GB SD card. Double-check the drive letter --
   this operation erases all data on the selected device.
6. Click **Write**. Wait for the write and verification to complete (10-20 minutes
   depending on card speed).
7. Eject the SD card safely.

### 1.2 First Boot and Initial Configuration

1. Insert the flashed SD card into the Pi 5.
2. Connect the Pi 5 to a monitor (HDMI or the Hosyond 7" DSI display) and a USB keyboard.
3. Connect power via USB-C (the CanaKit PSU or any 5V/5A USB-C PD supply).
4. The Pi 5 will boot into Kali Linux. Default credentials:
   - Username: `kali`
   - Password: `kali`
5. **Change the default password immediately:**
   ```bash
   passwd
   ```
6. Set hostname:
   ```bash
   sudo hostnamectl set-hostname cyberdeck
   ```
7. Connect to WiFi for updates (use the Pi 5's built-in WiFi temporarily):
   ```bash
   sudo nmcli dev wifi connect "YOUR_SSID" password "YOUR_PASSWORD"
   ```

### 1.3 System Update and Core Packages

1. Full system update:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   ```
   This may take 15-30 minutes on first run. Reboot after if a kernel update was applied:
   ```bash
   sudo reboot
   ```

2. Install core system packages:
   ```bash
   sudo apt install -y \
     kismet \
     python3-pip \
     python3-flask \
     python3-venv \
     adb \
     gpsd \
     gpsd-clients \
     screen \
     git \
     esptool \
     i2c-tools \
     chromium \
     onboard \
     tmux \
     nmap \
     wireshark \
     aircrack-ng \
     bettercap
   ```

3. Install Python packages (use a venv or `--break-system-packages` on modern Kali):
   ```bash
   pip install --break-system-packages \
     flask \
     flask-socketio \
     pyserial \
     meshtastic \
     gps3 \
     kismet-rest \
     luma.oled \
     Pillow \
     psutil
   ```

4. Enable SSH for remote access:
   ```bash
   sudo systemctl enable --now ssh
   ```

5. Enable I2C bus (needed for the 2.42" OLED later):
   ```bash
   sudo raspi-config
   ```
   Navigate: **Interface Options** > **I2C** > **Enable**. Exit and reboot.

### 1.4 Configure GPS (gpsd)

1. Plug the VK-162 USB GPS module into the Pi 5.
2. Identify the device:
   ```bash
   ls /dev/ttyACM*
   ```
   Expected output: `/dev/ttyACM0`

3. Edit the gpsd configuration:
   ```bash
   sudo nano /etc/default/gpsd
   ```
   Set these values:
   ```
   START_DAEMON="true"
   DEVICES="/dev/ttyACM0"
   GPSD_OPTIONS="-n"
   USBAUTO="true"
   ```

4. Enable and start gpsd:
   ```bash
   sudo systemctl enable gpsd
   sudo systemctl start gpsd
   ```

5. Verify GPS fix (take the Pi near a window or outdoors):
   ```bash
   cgps -s
   ```
   Expected output: latitude, longitude, altitude, and satellite count should populate
   within 30-120 seconds of getting a sky view. If the fields stay empty indoors, that is
   normal -- GPS requires line-of-sight to satellites.

6. Test the Python GPS library:
   ```bash
   python3 -c "
   from gps3 import gps3
   gps_socket = gps3.GPSDSocket()
   data_stream = gps3.DataStream()
   gps_socket.connect()
   gps_socket.watch()
   for new_data in gps_socket:
       if new_data:
           data_stream.unpack(new_data)
           print('Lat:', data_stream.TPV['lat'], 'Lon:', data_stream.TPV['lon'])
           break
   "
   ```

### 1.5 Verify Pi 5 Bench Test

Run these checks before continuing:

| Check | Command | Expected |
|-------|---------|----------|
| OS version | `cat /etc/os-release` | Kali Linux |
| Python 3 | `python3 --version` | 3.11+ |
| esptool | `esptool.py version` | 4.x |
| Kismet | `kismet --version` | Version string printed |
| gpsd running | `systemctl status gpsd` | active (running) |
| I2C enabled | `i2cdetect -y 1` | Grid printed (no devices yet) |
| SSH | `systemctl status ssh` | active (running) |
| Serial tools | `screen --version` | Version string |

---

## 2. ESP32 Marauder -- Gold #1 + CYD #1

**Board:** Lonely Binary ESP32 Gold #1 (ESP32-S3, IPEX antenna connector)
**Display:** CYD 2.8" Touchscreen #1 (plugs into Gold #1 for touchscreen Marauder GUI)
**Firmware:** ESP32 Marauder v1.12.1+ (MultiBoard S3 variant)
**Deck role:** Primary 2.4GHz WiFi/BLE offensive toolkit with touchscreen control
**SMA port:** SMA #1

### 2.1 Download Firmware Files

1. Go to the Marauder releases page:
   [github.com/justcallmekoko/ESP32Marauder/releases](https://github.com/justcallmekoko/ESP32Marauder/releases)
2. Download these four files from the latest release (v1.12.1 or newer):
   - `esp32_marauder.ino.bootloader.bin`
   - `esp32_marauder.ino.partitions.bin`
   - `boot_app0.bin`
   - `esp32_marauder_v1_12_1_multiboardS3.bin` (the main application binary)
3. Save all four files to the same folder on your PC.

### 2.2 Flash via esptool (CLI Method)

1. Connect Gold #1 to your PC with a USB-C **data** cable.
2. Identify the COM port:
   - **Windows:** Open Device Manager > Ports (COM & LPT). Look for "USB Serial" or
     "CH340" or "CP210x". Note the COM number (e.g., COM3).
   - **Linux:** `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`
   - **macOS:** `ls /dev/cu.usbserial-*`
3. If the board is not recognized, hold the **BOOT** button while plugging in the USB cable,
   then release BOOT after 2 seconds. This forces bootloader mode.
4. Flash the firmware (replace `COM3` with your actual port):

   **Windows:**
   ```
   esptool.py --chip esp32s3 --port COM3 --baud 921600 ^
     write_flash ^
     0x0 esp32_marauder.ino.bootloader.bin ^
     0x8000 esp32_marauder.ino.partitions.bin ^
     0xe000 boot_app0.bin ^
     0x10000 esp32_marauder_v1_12_1_multiboardS3.bin
   ```

   **Linux/macOS:**
   ```bash
   esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 921600 \
     write_flash \
     0x0 esp32_marauder.ino.bootloader.bin \
     0x8000 esp32_marauder.ino.partitions.bin \
     0xe000 boot_app0.bin \
     0x10000 esp32_marauder_v1_12_1_multiboardS3.bin
   ```

5. Expected output during flash:
   ```
   esptool.py v4.x
   Serial port COM3
   Connecting...
   Chip is ESP32-S3
   ...
   Writing at 0x00010000... (100 %)
   Hash of data verified.
   Leaving...
   Hard resetting via RTS pin...
   ```
6. If the flash stalls at "Connecting...", hold BOOT, press and release RST, then release
   BOOT. The board should enter bootloader mode.

### 2.3 Alternative: Flash via Web (ESP Terminator)

1. Open Chrome or Edge (must support WebSerial).
2. Navigate to [espterminator.com](https://espterminator.com/).
3. Connect Gold #1 via USB-C data cable.
4. Select the device/port when prompted.
5. Choose **ESP32 Marauder** > **MultiBoard S3** > latest version.
6. Click **Flash**. Wait for completion (do not disconnect mid-flash).
7. Press RST on the board after flash completes.

### 2.4 Connect CYD #1 to Gold #1

The CYD 2.8" touchscreen #1 connects to Gold #1 via serial for the Marauder touchscreen GUI:

1. Connect the CYD to Gold #1 using a short USB cable (CYD acts as the display, Gold #1
   runs the firmware and does the RF work).
2. Power on both boards.
3. The CYD should display the Marauder main menu with touch-selectable options:
   - WiFi
   - Bluetooth
   - Device
   - Reboot

### 2.5 Test Marauder Standalone

1. Test via serial (connect Gold #1 to PC):
   ```bash
   screen /dev/ttyUSB0 115200
   ```
   (Windows: use PuTTY at 115200 baud on the correct COM port)

2. Run a WiFi access point scan:
   ```
   scanap
   ```
   Expected output: a list of nearby WiFi access points with SSID, BSSID, channel, and RSSI.

3. Stop the scan:
   ```
   stopscan
   ```

4. Test Flock detection mode (this confirms Gold #1 can be a Flock fallback):
   ```
   sniffbt -t flock
   ```
   Expected output: "Sniffing for Flock..." -- it will print detections if any Flock ALPR
   cameras with known OUIs are within 2.4GHz range.

5. Stop:
   ```
   stopscan
   ```

6. If using the CYD touchscreen, tap through **WiFi** > **Scan APs** on the touchscreen
   and verify results display.

### 2.6 Verify Antenna Connector

1. Locate the IPEX/U.FL connector on Gold #1 (small gold pad near the "ANT" label).
2. Take a U.FL-to-SMA pigtail cable (15-20cm).
3. Align the U.FL connector directly over the IPEX socket.
4. Press straight down firmly until you feel/hear a click. **Do not twist or wiggle.**
5. Connect a 2.4GHz antenna to the SMA end of the pigtail.
6. Re-run `scanap` and compare RSSI values -- they should be noticeably stronger (higher,
   less negative) with the external antenna vs the PCB trace antenna.
7. Disconnect the pigtail gently by pulling straight up with fingernails under the
   connector edge. U.FL connectors are rated for approximately 30 mating cycles -- treat
   as semi-permanent once installed in the deck.

---

## 3. ESP32 Marauder Dual-Band -- C5 #1

**Board:** Waveshare ESP32-C5 #1
**Firmware:** ESP32 Marauder (C5 dual-band variant)
**Deck role:** Dual-band Marauder (2.4GHz + 5GHz WiFi 6) -- headless, Pi 5 controlled
**SMA port:** SMA #4

The ESP32-C5 is the dual-band backbone of the cyberdeck. It supports both 2.4GHz and 5GHz
WiFi 6, bringing 5GHz packet injection, deauth, beacon spam, and scanning that the classic
ESP32 Gold boards cannot do.

### 3.1 Download C5 Firmware

1. Check the Marauder releases page for a C5-specific build:
   [github.com/justcallmekoko/ESP32Marauder/releases](https://github.com/justcallmekoko/ESP32Marauder/releases)
2. Look for a file named like `esp32_marauder_v*_esp32c5_devkitc.bin` or `_v8.bin`.
3. If a dedicated C5 build is not yet available in the main release, check the
   development branch or community forks that have ported Marauder to the C5 platform.

### 3.2 Flash the C5 Board

1. Connect C5 #1 to your PC with a USB-C data cable.
2. Put the board into bootloader mode: hold **BOOT**, press and release **RST**, then
   release **BOOT** after 2 seconds.
3. Identify the port (same as Section 2.2).
4. Flash:

   **Windows:**
   ```
   esptool.py --chip esp32c5 --port COM3 --baud 921600 ^
     write_flash 0x10000 esp32_marauder_esp32c5_devkitc.bin
   ```

   **Linux:**
   ```bash
   esptool.py --chip esp32c5 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x10000 esp32_marauder_esp32c5_devkitc.bin
   ```

   If the flash fails at 921600 baud, drop to 115200:
   ```bash
   esptool.py --chip esp32c5 --port /dev/ttyUSB0 --baud 115200 \
     write_flash 0x10000 esp32_marauder_esp32c5_devkitc.bin
   ```

5. Press RST after flash completes.

### 3.3 Test Headless Serial Control

This board runs headless (no display). It is controlled from the Pi 5 via serial:

1. Open a serial connection:
   ```bash
   screen /dev/ttyUSB0 115200
   ```

2. Run a scan on 2.4GHz:
   ```
   scanap
   ```
   Verify access points appear.

3. Switch to 5GHz scanning (if the firmware supports band selection):
   ```
   channel -s 36
   scanap
   ```
   You should see 5GHz networks that the classic ESP32 boards cannot detect.

4. Stop:
   ```
   stopscan
   ```

### 3.4 Attach Dual-Band Antenna

1. Snap the U.FL pigtail onto the C5's IPEX connector (press straight down, feel the click).
2. Connect a **Bingfu dual-band antenna** (2.4/5.8GHz) to the SMA end.
3. Re-scan and compare RSSI values between bands.
4. If the antenna is RP-SMA, use a Boobrie RP-SMA-to-SMA adapter between the pigtail and
   the antenna.

---

## 4. ESP32-C5 #2 -- Dual-Band Scanner

**Board:** Waveshare ESP32-C5 #2
**Firmware:** GhostESP or Marauder scanner build
**Deck role:** Dual-band passive scanning/wardriving (2.4GHz + 5GHz)
**SMA port:** SMA #5

### 4.1 Flash Firmware

**Option A -- GhostESP (recommended for passive scanning + Wireshark streaming):**

1. Download GhostESP from
   [github.com/GhostESP-Revival/GhostESP/releases](https://github.com/GhostESP-Revival/GhostESP/releases).
2. Select the ESP32-C5 DevKitC variant binary.
3. Flash:
   ```bash
   esptool.py --chip esp32c5 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x10000 ghostesp_esp32c5_devkitc.bin
   ```

**Option B -- Marauder (same firmware family as C5 #1):**

Follow the same process as [Section 3](#3-esp32-marauder-dual-band----c5-1), flashing the
same C5 Marauder build. This gives you two independent Marauder instances -- one for
attacks (C5 #1) and one for passive monitoring (C5 #2).

### 4.2 Test 5GHz Scanning

1. Serial in:
   ```bash
   screen /dev/ttyUSB0 115200
   ```
2. For GhostESP, trigger a scan (commands vary by version -- check GhostESP documentation).
3. For Marauder, use `scanap` and verify both 2.4GHz and 5GHz networks appear.
4. Verify antenna works with the Bingfu dual-band antenna attached.

---

## 5. Flock Detection -- Gold #2

**Board:** Lonely Binary ESP32 Gold #2 (classic ESP32, **not** S3)
**Firmware:** Marauder Flock mode (primary) or Flock-You dedicated firmware (alternative)
**Deck role:** Dedicated Flock ALPR camera detection -- passive, always listening
**SMA port:** SMA #2

### 5.1 Determine Gold Board Chip Variant

**Critical:** The Lonely Binary Gold boards ship in two variants. You must determine which
chip is in Gold #2 before flashing:

1. Connect Gold #2 and run:
   ```bash
   esptool.py --port /dev/ttyUSB0 chip_id
   ```
2. Check the output:
   - `Chip is ESP32-S3` -- use the MultiBoard S3 Marauder firmware (same as Gold #1).
   - `Chip is ESP32` (WROOM) -- use the standard ESP32 (WROOM) Marauder firmware.

### 5.2 Flash Marauder for Flock Mode (Primary Path)

Flash Marauder onto Gold #2 (same process as [Section 2.2](#22-flash-via-esptool-cli-method),
using the correct chip variant). Then activate the dedicated Flock detection mode over serial.

After flashing, connect via serial and start Flock scanning:
```bash
screen /dev/ttyUSB0 115200
```
```
sniffbt -t flock
```

Expected output when a Flock ALPR camera is in range:
```
[FLOCK] MAC: AA:BB:CC:DD:EE:FF RSSI: -65 OUI: Flock Safety
```

For GPS-tagged logging (requires gpsd):
```
Flock Wardrive
```

### 5.3 Alternative: Flash Flock-You Dedicated Firmware

If you want a purpose-built Flock scanner instead of Marauder:

1. Clone the repository:
   ```bash
   git clone https://github.com/colonelpanichacks/flock-you.git
   cd flock-you
   ```

2. Install PlatformIO:
   ```bash
   pip install platformio
   ```

3. **Verify the build target matches your chip.** Open `platformio.ini` and check the
   `[env]` sections. You need an environment that targets classic ESP32 (if your Gold is
   WROOM) or ESP32-S3 (if your Gold is S3).

4. Build and flash:
   ```bash
   pio run -e <your_env> --target upload
   ```
   Replace `<your_env>` with the correct PlatformIO environment name for your chip.

5. If using the compiled binary approach:
   ```bash
   pio run -e <your_env>
   # Binary will be in .pio/build/<your_env>/firmware.bin
   esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x10000 .pio/build/<your_env>/firmware.bin
   ```

### 5.4 Test Flock Detection

1. Open serial:
   ```bash
   screen /dev/ttyUSB0 115200
   ```
2. The board should continuously scan for Flock OUI MAC addresses on 2.4GHz.
3. Flock cameras use ~31 known OUIs. You will not see detections unless you are physically
   near a Flock ALPR camera (typically mounted on poles in parking lots, intersections, or
   HOA neighborhoods).
4. To verify the scanner is working, confirm serial output shows scanning activity (even if
   no Flock devices are detected).

---

## 6. BLE Scanner / Chasing Your Tail -- Gold #3

**Board:** Lonely Binary ESP32 Gold #3 (classic ESP32 or S3)
**Firmware:** ESP32 AirTag Scanner or Chasing Your Tail NG (combined BLE tracker detection)
**Deck role:** Detect BLE trackers (AirTags, Tiles, SmartTags) and persistent BLE followers
**SMA port:** SMA #3

**Important:** Gold #3 is a shared board. It runs BLE device detection AND Chasing Your Tail
tracker detection from the same firmware. Flash once to cover both functions.

### 6.1 Flash ESP32 AirTag Scanner

1. Install **Arduino IDE** from [arduino.cc/en/software](https://www.arduino.cc/en/software).

2. Add ESP32 board support:
   - Open Arduino IDE.
   - Go to **File** > **Preferences**.
   - In "Additional Boards Manager URLs", add:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to **Tools** > **Board** > **Boards Manager**.
   - Search "esp32" and install **"esp32 by Espressif Systems"**.

3. Clone or download the scanner:
   ```bash
   git clone https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner.git
   ```

4. Open the `.ino` sketch file in Arduino IDE.

5. Configure the board:
   - **Tools** > **Board**: select **"ESP32 Dev Module"** (for classic ESP32) or
     **"ESP32S3 Dev Module"** (for S3 variant). Run `esptool.py chip_id` if unsure.
   - **Tools** > **Port**: select the COM port of Gold #3.
   - **Tools** > **Upload Speed**: 921600.

6. Click **Upload**. If it stalls at "Connecting...", hold **BOOT** during upload.

7. After upload completes, open **Tools** > **Serial Monitor** at 115200 baud.

### 6.2 Test BLE Detection

1. Open serial at 115200 baud.
2. Walk a phone, AirTag, Tile, or any BLE device near the board.
3. Expected output (one line per detected device):
   ```
   MAC: AA:BB:CC:DD:EE:FF  RSSI: -52  Name: "AirTag"  Manufacturer: Apple
   MAC: 11:22:33:44:55:66  RSSI: -71  Name: ""         Manufacturer: Samsung
   ```
4. Verify:
   - Known devices appear (your phone, smartwatch, etc.).
   - RSSI values change as you move the device closer/farther.
   - The scanner runs continuously without crashing.

### 6.3 Alternative: Chasing Your Tail NG

If you want purpose-built tail detection (detects BLE devices that follow you over time):

1. Clone:
   ```bash
   git clone https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG.git
   ```
2. Open in Arduino IDE, select the correct board, and upload.
3. This firmware specifically flags BLE devices that persist across multiple scan cycles,
   indicating they may be tracking your movement.

### 6.4 Attach External Antenna

Same process as [Section 2.6](#26-verify-antenna-connector):
1. Snap U.FL pigtail onto Gold #3's IPEX socket (press straight down, click).
2. Attach 2.4GHz antenna to SMA end.
3. BLE shares the 2.4GHz radio -- the external antenna gives approximately +10 dB
   reception improvement over the PCB trace, critical for spotting low-power trackers
   at distance.

---

## 7. Meshtastic -- Heltec LoRa V3

**Board:** Heltec WiFi LoRa 32 V3 (ESP32-S3 + SX1262 LoRa radio + 0.96" OLED)
**Firmware:** Meshtastic, latest stable release
**Deck role:** Off-grid 915MHz encrypted mesh communications
**SMA port:** SMA #6

**CRITICAL WARNING:** Attach the 915MHz antenna BEFORE powering on or transmitting.
Keying the SX1262 LoRa radio with no antenna connected can permanently destroy the radio
chip. This is not a theoretical risk -- it is a common cause of dead Heltec boards.

### 7.1 Flash Meshtastic via Web Flasher (Easiest)

1. Connect the 915MHz antenna to the Heltec V3's IPEX connector first. If you do not have
   the final antenna ready, at minimum connect any 915MHz antenna or a 50-ohm dummy load.
2. Connect the Heltec V3 to your PC with a USB-C **data** cable.
3. Open **Chrome** or **Edge** (WebSerial required -- Firefox and Safari do not support it).
4. Navigate to [flasher.meshtastic.org](https://flasher.meshtastic.org/).
5. Select device: **"Heltec WiFi LoRa 32 V3"**.
6. Select version: **Latest Stable**.
7. Select flash type: **"Full Erase and Install"** (recommended for a fresh board).
8. Click **Flash**. Do not disconnect during the flash process.
9. Wait for the "Flash complete" confirmation.

### 7.2 Alternative: Flash via esptool (CLI)

1. Download the Meshtastic firmware for Heltec V3 from
   [github.com/meshtastic/firmware/releases](https://github.com/meshtastic/firmware/releases).
2. Look for `firmware-heltec-v3-X.X.XX.bin` (or similar naming).
3. Flash:
   ```bash
   esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x0 firmware-heltec-v3-X.X.XX.bin
   ```

### 7.3 Configure Region and Node

The LoRa radio will not transmit until the region is set. This is a legal requirement --
different countries use different frequencies.

1. Install the Meshtastic Python CLI:
   ```bash
   pip install meshtastic
   ```

2. Set region to US (915MHz):
   ```bash
   meshtastic --port /dev/ttyUSB0 --set lora.region US
   ```

3. Set your node name:
   ```bash
   meshtastic --port /dev/ttyUSB0 --set-owner "CYBERDECK"
   ```

4. View node info to confirm configuration:
   ```bash
   meshtastic --port /dev/ttyUSB0 --info
   ```
   Expected output includes:
   ```
   Owner: CYBERDECK
   Region: US
   Modem Preset: LONG_FAST
   ...
   ```

### 7.4 Test Meshtastic Standalone

1. The onboard 0.96" OLED should display the Meshtastic boot screen, then the node
   status screen showing:
   - Node name
   - Channel info
   - Number of nodes in mesh (will show 1 if you are the only node)
   - GPS coordinates (if GPS is connected)
   - Battery level

2. Test sending a message (requires a second Meshtastic node to receive):
   ```bash
   meshtastic --port /dev/ttyUSB0 --sendtext "Cyberdeck online"
   ```

3. Test via BLE: pair your phone (Android or iOS) with the Meshtastic app. The default
   BLE pairing PIN is **123456**. Change it after pairing:
   ```bash
   meshtastic --port /dev/ttyUSB0 --set security.bluetooth_logging_enabled false
   ```

### 7.5 Troubleshooting: Node Not Detected Over USB

If the board powers (OLED lights up) but the PC does not detect a serial device:

1. **Swap the USB cable.** The #1 cause is a charge-only cable. Use a verified data cable.
2. **Install the USB-serial driver.** The Heltec V3 uses a CH340 or CP2102 bridge:
   - CH340: download from [wch.cn/downloads/CH341SER_ZIP.html](https://www.wch.cn/downloads/CH341SER_ZIP.html)
   - CP210x: download from [silabs.com/developers/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
3. **Force bootloader mode:** hold **BOOT** while plugging in the USB cable, then re-flash.
4. After driver install, reboot your PC and try again.

---

## 8. HaleHound -- CYD #2

**Board:** CYD 2.8" Touchscreen #2 (ESP32-2432S028R)
**Firmware:** HaleHound-CYD
**Deck role:** Multi-protocol attack station + IoT Recon credential harvester
**Display:** Built-in 2.8" touchscreen (self-contained, no Pi needed for basic operation)

HaleHound is an ESP32-DIV fork that adds IoT Recon -- automated LAN scanning with
credential brute force for IoT devices. It also supports WiFi attacks, BLE attacks, and
optionally SubGHz (CC1101) and NFC (PN532) with add-on modules.

### 8.1 Flash HaleHound

**Method A -- Web Flasher (easiest):**

1. Open Chrome or Edge.
2. Navigate to [halehound.com](https://halehound.com/).
3. Connect CYD #2 via USB.
4. Select **"ESP32-2432S028R (2.8" CYD)"**.
5. Click **Flash**. Takes approximately 60 seconds.
6. After flash, press RST on the board.

**Method B -- esptool (CLI):**

1. Download `HaleHound-CYD-FULL.bin` from the HaleHound releases page:
   [github.com/JesseCHale/HaleHound-CYD/releases](https://github.com/JesseCHale/HaleHound-CYD/releases)
2. Flash at address 0x0:
   ```bash
   esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x0 HaleHound-CYD-FULL.bin
   ```
3. If flash stalls, hold BOOT during connect, or drop baud to 115200.

### 8.2 First Boot and Setup

1. After flashing, the CYD should display the HaleHound boot screen and main menu
   on its 2.8" touchscreen.
2. Insert a micro SD card (16GB+) into the CYD's SD slot for loot/credential storage.
3. Navigate the touchscreen menu. Key capabilities:
   - **IoT Recon** -- connect to a WiFi network, scan for IoT devices, brute-force
     default credentials
   - **WiFi** -- deauth, beacon spam, evil portal (GARMR), karma
   - **BLE** -- Cinder, Spoofer, Predator, Lunatic Fringe (tracker detection)
   - **Settings** -- WiFi config, SD card management

### 8.3 Test IoT Recon Mode

1. From the main menu, tap **IoT Recon**.
2. Select **Scan WiFi** -- the board will find nearby WiFi networks.
3. Select your test network and enter the password.
4. The board connects, scans the LAN for devices, and attempts default credential
   brute force against discovered IoT devices (cameras, printers, routers, smart plugs).
5. Results display on screen and save to the SD card.

**Legal notice:** Only use IoT Recon on networks you own or have explicit written
authorization to test.

### 8.4 Verify

| Check | How | Expected |
|-------|-----|----------|
| Boot | Power via USB | HaleHound menu on touchscreen |
| Touch input | Tap menu items | Menus navigate correctly |
| WiFi scan | IoT Recon > Scan WiFi | Nearby networks listed |
| SD card | Settings > SD Info | Card detected, free space shown |
| BLE | BLE menu > Scan | Nearby BLE devices listed |

---

## 9. Drone RemoteID -- WROOM-32

**Board:** ESP32-WROOM-32 generic dev board
**Firmware:** Sky-Spy (Drone RemoteID scanner)
**Deck role:** Detect FAA RemoteID broadcasts from nearby drones
**Antenna:** Internal PCB antenna (no SMA needed -- RemoteID range is generous)

### 9.1 Flash Sky-Spy

1. Clone the Sky-Spy repository:
   ```bash
   git clone https://github.com/colonelpanichacks/Sky-Spy.git
   cd Sky-Spy
   ```

2. Install PlatformIO if not already installed:
   ```bash
   pip install platformio
   ```

3. Check `platformio.ini` for the correct environment. Look for an `env` targeting
   ESP32-WROOM-32 or ESP32 Dev Module.

4. Build and upload:
   ```bash
   pio run -e esp32dev --target upload
   ```
   (Replace `esp32dev` with the correct environment name if different.)

5. If using the pre-compiled binary approach:
   ```bash
   pio run -e esp32dev
   esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
     write_flash 0x10000 .pio/build/esp32dev/firmware.bin
   ```

### 9.2 Alternative: Flash via Arduino IDE

1. Open Sky-Spy sketch in Arduino IDE.
2. Board: **"ESP32 Dev Module"**.
3. Upload Speed: 921600.
4. Click Upload.

### 9.3 Test Drone Detection

1. Open serial:
   ```bash
   screen /dev/ttyUSB0 115200
   ```
2. Expected output format when a RemoteID-compliant drone is detected:
   ```json
   {"mac":"AA:BB:CC:DD:EE:FF","rssi":-45,"drone_lat":37.7749,"drone_lon":-122.4194,"altitude":120,"speed":5.2,"pilot_lat":37.7740,"pilot_lon":-122.4180}
   ```
3. If no drones are nearby, the serial output should still show the scanner is running
   (periodic status messages or empty scan cycles).
4. To bench-test without a real drone, verify the firmware boots correctly and the serial
   output format matches the expected JSON structure.

---

## 10. RaspyJack -- Pi Zero 2W

**Board:** Raspberry Pi Zero 2 WH (dedicated -- separate from Pwnagotchi Pi Zero)
**Firmware:** RaspyJack OS image
**Deck role:** Wired network pentesting (Responder, ARP MITM, DNS spoofing, Nmap)
**Display:** Waveshare 1.44" LCD HAT (128x128, ST7735S, with joystick + 3 buttons)

RaspyJack fills the one gap no ESP32 board covers: wired Ethernet attacks. It plugs into a
network switch or router via USB-to-Ethernet adapter and runs Responder, ARP MITM, DNS
spoofing, and 231+ payload scripts.

### 10.1 Flash RaspyJack OS Image

1. Download the latest RaspyJack image from
   [github.com/7h30th3r0n3/Raspyjack/releases](https://github.com/7h30th3r0n3/Raspyjack/releases).
2. Write the image to a micro SD card (16GB+) using Raspberry Pi Imager or balenaEtcher:
   - **Raspberry Pi Imager**: Choose OS > Use custom > select the RaspyJack `.img` file.
   - **balenaEtcher**: Select image > select drive > Flash.
3. Insert the SD card into the Pi Zero 2W.

### 10.2 Attach Hardware

1. Mount the **Waveshare 1.44" LCD HAT** onto the Pi Zero 2W's GPIO header. The HAT has
   a 40-pin connector that plugs directly onto the Pi Zero's GPIO pins.
2. Connect a **USB OTG adapter** (micro-USB to USB-A) to the Pi Zero's USB data port.
3. Plug the **USB-to-Ethernet adapter** (AX88772 or similar) into the OTG adapter.

### 10.3 First Boot

1. Power the Pi Zero 2W via its micro-USB power port (any 5V/2A source).
2. RaspyJack boots automatically. The 1.44" LCD HAT should display the RaspyJack menu
   within 30-60 seconds.
3. Use the joystick and buttons on the HAT to navigate the menu:
   - Payloads
   - Settings
   - Network Info
   - Reboot / Shutdown

### 10.4 Test Wired Attack Capabilities

1. Connect an Ethernet cable from the USB-to-Ethernet adapter to a test network
   (your own lab network).
2. From the LCD menu, select **Payloads** > **Responder**.
3. Responder should start and begin listening for LLMNR/NBT-NS/MDNS queries.
4. From another machine on the same network, try to access a non-existent share
   (e.g., `\\fakeshare`) -- Responder should capture the credential hash.
5. Check the loot folder for captured hashes.

### 10.5 Test WebUI

1. From your PC or the Pi 5, connect to RaspyJack's WiFi AP (check the LCD for SSID
   and password) or use USB networking.
2. Open `http://raspyjack.local` (or the IP shown on the LCD) in a browser.
3. Verify the WebUI loads with:
   - Payload browser
   - Code editor
   - Loot viewer
   - Remote control

**Legal notice:** Only use RaspyJack on networks you own or have explicit written
authorization to test.

---

## 11. RayHunter -- Orbic RC400L

**Board:** Orbic Speed RC400L mobile hotspot
**Firmware:** EFF RayHunter (IMSI catcher / stingray detector)
**Deck role:** Detect fake cell towers (IMSI catchers / stingrays)

RayHunter runs entirely on the Orbic's own hardware. The Pi 5 cannot run RayHunter because
it has no cellular baseband modem. The Orbic is a self-contained detector -- the cyberdeck
just carries it and keeps it charged.

### 11.1 Acquire the Orbic

Purchase an Orbic Speed **RC400L** (also sold as Kajeet RC400L). Available used/renewed on
eBay or Amazon for approximately $20-30. This specific model is required because it has an
exposed Qualcomm `/dev/diag` interface that RayHunter needs.

### 11.2 Note the Admin Password

- **Verizon units:** the WiFi password printed on the device label IS the admin password.
- **Kajeet/Smartspot units:** default admin password is `$m@rt$p0tc0nf!g`.
- Write this password down -- you will need it for the installer.

### 11.3 Install RayHunter

1. Download the latest RayHunter release from
   [github.com/EFForg/rayhunter/releases](https://github.com/EFForg/rayhunter/releases).
2. Unzip the release archive.
3. Connect the Orbic to your PC via USB (power it on first, let it fully boot).
4. Run the installer:
   ```bash
   ./installer orbic --admin-password 'YOUR_ADMIN_PASSWORD'
   ```
   For Kajeet units:
   ```bash
   ./installer orbic --admin-password '$m@rt$p0tc0nf!g'
   ```
   If the network install method fails, use USB:
   ```bash
   ./installer orbic-usb
   ```
5. The installer will:
   - Root the device
   - Deploy the RayHunter daemon
   - Configure autostart so RayHunter launches on every boot

### 11.4 Apply Autoboot Mod (Optional but Recommended)

The autoboot mod patches the Orbic's aboot partition so it powers on automatically when
USB power is applied -- no need to press the power button. This means the Orbic starts
with the cyberdeck.

**WARNING:** This modifies the device's bootloader partition. Proceed carefully.

1. Get shell access:
   ```bash
   ./installer util orbic-shell
   ```
   Or:
   ```bash
   adb shell
   /bin/rootshell
   ```

2. The patch target is the aboot partition. Find the byte sequence `03 02 00 0a 20`.
   Change the last byte from `0x20` to `0xFF`.

3. This modification is documented in the RayHunter project's community notes. Refer to
   the latest guidance at [efforg.github.io/rayhunter](https://efforg.github.io/rayhunter/)
   for the exact procedure and safety warnings.

### 11.5 Insert a SIM Card

RayHunter requires a SIM card to connect to the cellular network and monitor for IMSI
catchers:

1. Use any **deactivated SIM card** -- no active service plan is needed.
2. Insert the SIM into the Orbic's SIM slot.
3. The Orbic's internal battery must remain installed -- it will not boot without it.
   USB power keeps the battery charged.

### 11.6 Verify RayHunter

1. Power on the Orbic.
2. Wait 30-60 seconds for it to fully boot and start RayHunter.
3. Join the Orbic's WiFi network (check the device label for SSID and password).
4. Open a browser and navigate to:
   ```
   http://192.168.1.1:8080
   ```
5. The RayHunter dashboard should display:
   - Status line: **green** = no suspicious activity detected.
   - If the status shows **red**, a possible IMSI catcher has been detected.
6. Test the API endpoint:
   ```bash
   curl http://192.168.1.1:8080/api/analysis
   ```
   Expected output: JSON containing analysis results and threat level.

---

## 12. Pwnagotchi -- Standalone Pocket Device

**Board:** Raspberry Pi Zero 2W (separate unit from RaspyJack)
**Firmware:** Jayofelony fork v2.9.5.4
**Status:** Standalone pocket device -- does NOT go inside the cyberdeck

The Pwnagotchi is an autonomous AI-driven WiFi handshake capture device. It stays outside
the deck as a pocket-carry companion because:
- It is designed for long autonomous walks (6+ hours on a PiSugar battery).
- Integrating it into the deck adds complexity with minimal benefit.
- It has its own e-ink display and personality.

### 12.1 Flash Pwnagotchi Image

1. Download the jayofelony fork image:
   [github.com/jayofelern/pwnagotchi/releases](https://github.com/jayofelern/pwnagotchi/releases)
   Look for the latest v2.9.5.4 (or newer) image file.
2. Flash to a micro SD card (16GB+) using Raspberry Pi Imager or balenaEtcher.
3. After flashing, mount the SD card's boot partition on your PC.

### 12.2 Configure Before First Boot

1. Edit the configuration file at `/boot/config.toml` (or `/boot/config.yml` depending
   on the fork version):
   ```toml
   main.name = "pwnagotchi"
   main.lang = "en"
   main.whitelist = ["YOUR_HOME_SSID"]

   ui.display.enabled = true
   ui.display.type = "waveshare_3"
   ui.web.enabled = true
   ui.web.address = "0.0.0.0"
   ui.web.username = "changeme"
   ui.web.password = "changeme"
   ```
2. Set your home network SSID in the whitelist to prevent the Pwnagotchi from capturing
   your own handshakes.

### 12.3 First Boot

1. Insert the SD card into the Pi Zero 2W.
2. Attach the e-ink display HAT.
3. Power via micro-USB or PiSugar battery.
4. First boot takes 5-10 minutes as the Pwnagotchi initializes.
5. The e-ink display will show the Pwnagotchi face and status.

### 12.4 Verify

1. The Pwnagotchi should begin capturing WPA handshakes automatically in "auto" mode.
2. Connect via USB networking to `http://10.0.0.2:8080` for the web interface.
3. Captured handshakes are stored in `/root/handshakes/`.

---

# PART 2: Cyberdeck Assembly

All components from Part 1 are now flashed, tested, and verified working individually.
This part covers the physical build: drilling the case, mounting hardware, wiring
everything together, integrating the software, and running acceptance tests.

**Required tools for Part 2:**
- Cordless drill with step drill bit (4-20mm Unibit)
- Deburring tool or fine sandpaper (120-220 grit)
- Acrylic scoring tool + steel ruler
- Bench clamp or vise
- Soldering iron + solder (for power switch wiring)
- Wire strippers
- Heat shrink tubing + heat gun (or electrical tape)
- Phillips and flathead screwdrivers (M2.5, M3)
- Needle-nose pliers
- Multimeter (Fluke 17B+ from inventory)
- Marker (fine-tip Sharpie)
- Painter's tape
- Center punch
- Safety glasses

**Estimated build time:** 4-5 weekends (spaced across 9 phases)

---

## Phase 1: Case Preparation

**Goal:** Mark and drill every penetration point in the Pelican 1300 NF case.

### 1.1 Prepare the Case

1. Unbox the Pelican 1300 NF. Inspect for manufacturing defects. The NF (No Foam) version
   ships empty -- no pick-and-pluck foam to remove.
2. Clean the interior with a damp cloth. Remove any dust or debris.
3. Open the case fully. Familiarize yourself with the hinge, latches, O-ring groove, and
   the internal ribs molded into the walls.
4. Place painter's tape over every area you plan to drill. This serves two purposes:
   - Provides a surface you can mark with a fine-tip marker.
   - Reduces the chance of the drill bit skipping on smooth polycarbonate.

### 1.2 Mark Drill Points -- Right Wall (SMA Bulkheads + Exhaust Fan)

The right wall (when looking at the case from the front/latch side) holds the antenna
bulkheads and exhaust fan.

1. Measure and mark **7 evenly spaced points** for SMA bulkheads along the upper portion
   of the right wall:
   - Start approximately 1" from the hinge edge.
   - Space each bulkhead center approximately 1" apart.
   - Keep all points in a straight horizontal line, approximately 1.5" from the top edge.
   - Bulkhead holes: **7/16" (11mm)** diameter for standard SMA panel-mount connectors.
   - Label each mark: SMA1 (Gold #1, 2.4G), SMA2 (Gold #2, Flock), SMA3 (Gold #3, BLE),
     SMA4 (C5 #1, Dual), SMA5 (C5 #2, Dual), SMA6 (Heltec, 915M), SMA7 (PAU0F, 6E).

2. Mark **1 x 40mm fan cutout** on the lower portion of the right wall:
   - Center the fan template (40x40mm square) in the lower-right area, at least 1" from
     any edge or rib.
   - Mark the four corner mounting holes (M3 screws) and the central circular opening
     (approximately 38mm diameter).

3. Center-punch every mark lightly so the drill bit does not wander.

### 1.3 Mark Drill Points -- Left Wall (Intake Fan + Membrane Vent)

1. Mark **1 x 40mm fan cutout** on the left wall, positioned opposite the exhaust fan
   on the right wall:
   - Same height and general position as the exhaust fan.
   - This creates cross-ventilation: intake (left) to exhaust (right).

2. Mark **1 x 6mm hole** for the Amphenol VENT-PS1 membrane vent:
   - Position on the lower portion of the left wall, below the fan and at least 2" away.
   - The vent is M12x1.5 threaded and requires a 12mm hole.

### 1.4 Mark Drill Points -- Front Panel (Switches + USB + RJ45)

The front panel (latch side, visible when carrying the case) holds all toggle switches
and panel-mount connectors.

1. Mark **12 toggle switch holes** in a horizontal row:
   - Start approximately 1" from the left edge.
   - Space each switch center approximately 3/4" (19mm) apart.
   - Hole diameter: **1/2" (12mm)** for standard SPST mini toggle thread.
   - Label each: SW1 (MAR), SW2 (FLK), SW3 (BLE), SW4 (5GM), SW5 (5GS), SW6 (MSH),
     SW7 (DRN), SW8 (IOT), SW9 (NET), SW10 (KS2), SW11 (GPS), SW12 (RAY).

2. Below the switch row, mark:
   - **1 x USB-C panel-mount hole** (for charging -- connects to Anker 347 input).
     Hole size per the specific panel-mount connector spec (typically 12-16mm).
   - **1 x USB-A panel-mount hole** (for data export -- connects to Pi 5 USB 2.0).
     Hole size per connector spec.
   - **1 x RJ45 panel-mount hole** (for RaspyJack wired Ethernet pass-through).
     Typically 22-24mm for a standard RJ45 bulkhead.

### 1.5 Drill All Holes

**Safety:** Wear safety glasses. Polycarbonate shards are sharp.

1. Set the drill to **low RPM** (300-500 RPM). Polycarbonate melts at high speed, creating
   ragged edges and potentially cracking the case. Let the bit do the cutting -- do not
   force it.

2. For the SMA bulkhead holes (11mm) and toggle switch holes (12mm):
   - Use the step drill bit. Start at the smallest step and step up to the target diameter.
   - Pause between steps to let the material cool.
   - Check the fit with the actual component after each step -- you can always drill
     larger, but never smaller.

3. For the fan cutouts (40mm circular):
   - Option A: Use a 40mm hole saw (cleanest result).
   - Option B: Drill a pilot hole, then use a Dremel with a cutting wheel to cut the
     circular opening. File smooth.
   - Option C: Drill many small holes around the 40mm circle perimeter, then punch out
     the center and file smooth.
   - Drill the four corner M3 mounting holes for fan screws.

4. For the USB-C, USB-A, and RJ45 panel-mount holes:
   - Step drill to the required diameter per each connector's spec sheet.

5. For the membrane vent (12mm):
   - Step drill to 12mm.

### 1.6 Deburr All Holes

1. Use a deburring tool or fine sandpaper (120-220 grit) on every hole, inside and out.
2. A clean, round, burr-free edge is critical:
   - O-rings and gaskets need a smooth surface to seal properly.
   - Sealant fills gaps better on smooth edges.
   - Sharp burrs can cut cables routed near the holes.
3. After deburring, wipe all holes with a damp cloth to remove dust/shavings.
4. Remove all painter's tape.

---

## Phase 2: Waterproofing

**Goal:** Install all panel-mount components with IP67/IP68 sealing and marine sealant.
Every penetration must be sealed before any electronics go into the case.

**Critical:** The sealant requires a **24-hour cure time** before water exposure or
before closing the lid. Plan accordingly -- do Phase 2 on Day 1 and Phase 3+ on Day 2.

### 2.1 Install IP67 SMA Bulkheads

1. For each of the 7 SMA bulkhead holes:
   - Apply a thin ring of **3M Marine Grade Silicone Sealant** around the hole on the
     **inside** of the case wall.
   - Insert the SMA bulkhead connector from the **outside**, pushing the threaded shaft
     through the hole.
   - Ensure the O-ring (included with IP67 bulkheads) is seated between the connector
     flange and the case wall.
   - From the inside, apply another ring of sealant around the connector shaft.
   - Thread the locknut onto the shaft from the inside. Hand-tighten, then add
     approximately 1/4 turn with a wrench. The sealant should squeeze into any gaps.
   - Wipe excess sealant with a damp cloth.
2. Label each bulkhead on the outside with a marker or label tape:
   SMA1, SMA2, SMA3, SMA4, SMA5, SMA6, SMA7.

### 2.2 Install IP67 Fans

1. **Exhaust fan (right wall):**
   - Cut a neoprene gasket to match the fan's 40mm footprint. Use the fan as a template.
   - Apply sealant around the fan cutout.
   - Place the neoprene gasket over the cutout.
   - Mount the Coolerguys CG4010M12-IP67 fan over the gasket with the airflow direction
     pointing **outward** (exhaust). The fan label/sticker side typically faces the
     direction of airflow.
   - Secure with M3 screws through the corner mounting holes.
   - Apply sealant around each screw head and the fan perimeter.

2. **Intake fan (left wall):**
   - Same process, but mount with airflow direction pointing **inward** (intake).
   - The airflow path should be: intake (left) -> across components -> exhaust (right).

### 2.3 Install Membrane Vent

1. Apply sealant around the 12mm vent hole on the left wall.
2. Thread the **Amphenol VENT-PS1** into the hole (M12x1.5 threads).
3. Tighten firmly. Apply sealant around the flange.
4. The ePTFE membrane allows slow air exchange for pressure equalization but blocks water
   and dust (IP69K rated).

### 2.4 Install Toggle Switches

1. For each of the 12 toggle switch holes:
   - Thread the SPST mini toggle switch through the hole from the inside.
   - Apply sealant around the hole on the outside.
   - Thread the nut from the outside. Tighten firmly.
   - Press on the **waterproof boot cap** over the toggle.
2. Label each switch below it: SW1/MAR, SW2/FLK, SW3/BLE, SW4/5GM, SW5/5GS, SW6/MSH,
   SW7/DRN, SW8/IOT, SW9/NET, SW10/KS2, SW11/GPS, SW12/RAY.

### 2.5 Install Panel-Mount Connectors

1. **USB-C (charge port):**
   - Install the IP65 panel-mount USB-C connector with sealant.
   - Internal cable routes to the Anker 347 power bank's USB-C input.

2. **USB-A (data export):**
   - Install the IP67 panel-mount USB-A connector with sealant.
   - Internal cable routes to Pi 5 USB 2.0 port.

3. **RJ45 (RaspyJack Ethernet):**
   - Install the panel-mount RJ45 connector with sealant.
   - Internal cable routes to RaspyJack's USB-to-Ethernet adapter.

### 2.6 Final Sealant Pass

1. Inspect every penetration point from both inside and outside.
2. Apply additional sealant to any gaps, cracks, or areas where the sealant bead is thin.
3. Pay special attention to:
   - The area around fan mounting screws.
   - The edges of toggle switch nuts.
   - The USB and RJ45 connector flanges.
4. Wipe all excess sealant with a damp cloth.

### 2.7 Cure

1. Leave the case **open** in a well-ventilated area.
2. Wait a **full 24 hours** for the silicone sealant to cure.
3. Do not install any electronics or close the lid during the cure period.
4. After 24 hours, gently press on each sealed component -- it should be firmly set with
   no movement.

---

## Phase 3: Mounting Plates

**Goal:** Fabricate and install the acrylic mounting plates that hold all components.

### 3.1 Cut the Base Plate

1. Mark the acrylic sheet: **8.5" x 6.5"** (for Pi 5 + USB hub + power bank + Orbic).
2. Score the cut line:
   - Place the steel ruler along the marked line.
   - Run the acrylic scoring tool along the ruler 10-15 times, pressing firmly.
   - Each pass deepens the score groove.
3. Snap the sheet:
   - Align the score line with the edge of the workbench.
   - Clamp the acrylic to the bench so the waste side hangs off.
   - Press down firmly on the overhanging portion -- it should snap cleanly along the
     score line.
4. Sand the cut edge smooth with fine sandpaper.

### 3.2 Cut the ESP32 Plate

1. From the remaining acrylic, mark and score: **6" x 4"** (for all ESP32 boards).
2. Score and snap using the same technique.
3. Sand the cut edge smooth.

### 3.3 Drill Mounting Holes

1. **Base plate mounting holes:**
   - Place the Pi 5 on the base plate and mark its 4 mounting holes with a marker.
   - Place the USB hub PCB (stripped from enclosure) and mark its mounting holes.
   - Mark 2-4 holes for Velcro/strap anchor points (for the power bank and Orbic).
   - Drill all marked holes with a **2.5mm or 3mm drill bit at low RPM** (high speed
     cracks acrylic). Go slow.

2. **ESP32 plate mounting holes:**
   - Lay out all ESP32 boards (3x Gold, 2x C5, 1x Heltec, 1x WROOM-32, 2x CYD) on
     the plate.
   - Leave approximately 1/2" (12mm) between boards for cable routing and airflow.
   - Mark M2.5 mounting holes for each board's standoff positions.
   - Drill all holes with a 2.5mm bit at low RPM.

### 3.4 Install Brass Standoffs

1. Thread **M2.5 brass standoffs** (from the 420-piece kit) into every drilled hole.
2. Base plate standoff height: 6-8mm (lifts boards off the plate for airflow).
3. ESP32 plate standoff height: 6-8mm.
4. Secure each standoff with a nut on the underside of the plate.

### 3.5 Test Fit

1. Place the base plate into the case. It should rest on the internal ribs molded into
   the case walls, approximately level. If it rocks, add foam strips under the plate
   edges for stability.
2. Place the ESP32 plate next to or stacked above the base plate.
3. Dry-fit a board on each plate to confirm the standoff spacing is correct and the screws
   thread in smoothly.
4. Confirm both plates fit within the case dimensions with clearance for cable routing
   along the edges.

---

## Phase 4: Compute Layer

**Goal:** Mount the Pi 5, USB hub, power bank, and Orbic on the base plate. Verify power.

### 4.1 Mount the Pi 5

1. Attach the **Geekworm H509 aluminum heatsink** to the Pi 5's SoC. Follow the
   heatsink's included instructions -- typically thermal paste or a thermal pad goes between
   the SoC and the heatsink, then mounting clips or screws secure it.
2. Place the Pi 5 on the base plate, aligning its mounting holes with the brass standoffs.
3. Secure with M2.5 screws through the Pi 5's mounting holes into the standoffs.
4. Confirm the Pi 5 is firmly mounted with no flex or wobble.

### 4.2 Mount the USB Hub

1. Strip the USB hub from its plastic enclosure to save space:
   - Remove screws from the hub casing.
   - Extract the bare PCB.
   - The PCB is approximately 50% smaller than the enclosed hub.
2. Mount the hub PCB on the base plate adjacent to the Pi 5 using standoffs.
3. If using two chained Adafruit CH334F 4-port breakouts instead of a single hub:
   - Mount both breakouts side by side.
   - Connect their upstream USB-C ports in a daisy chain.

### 4.3 Mount the Power Bank

1. Place the **Anker 347 (25,600mAh)** power bank in the base plate area.
2. Secure with **industrial-strength Velcro strips** (adhesive-backed) on the bottom of
   the power bank and the base plate. Press firmly for 30 seconds.
3. Alternatively, cut a foam block to cradle the power bank snugly.
4. Position the power bank so its USB-C and USB-A ports face toward the Pi 5 and hub.

### 4.4 Mount the Orbic RC400L

1. Place the Orbic near the case wall for best cellular signal reception.
2. Secure with Velcro strips.
3. Route a short USB cable from a hub port (through toggle SW12) to the Orbic's USB-C port.

### 4.5 Connect Power and Boot Test

1. Connect a **USB-C PD cable** from the Anker 347's USB-C output to the Pi 5's USB-C
   power input. The Anker 347 supports 30W USB-C PD output -- more than sufficient for
   the Pi 5's 25W requirement.
2. Connect a **USB-A cable** from the Anker 347's USB-A output to the USB hub's upstream
   port.
3. Press the power button on the Anker 347.
4. The Pi 5 should boot Kali Linux within 30 seconds.
5. Verify the USB hub enumerates:
   ```bash
   lsusb
   ```
   You should see the hub listed and any devices already connected.
6. Verify power delivery is stable:
   ```bash
   vcgencmd get_throttled
   ```
   Output `throttled=0x0` means no undervoltage detected. Any other value indicates a
   power issue.

---

## Phase 5: ESP32 Rail

**Goal:** Mount all ESP32 boards on the ESP32 plate, connect antennas to SMA bulkheads,
wire USB cables through toggle switches to the hub.

### 5.1 Mount ESP32 Boards

Mount each board on the ESP32 plate using M2.5 screws into the brass standoffs:

| Board | Position on Plate | Notes |
|-------|-------------------|-------|
| Gold #1 (Marauder) | Top left | Adjacent to CYD #1 |
| Gold #2 (Flock) | Top center | |
| Gold #3 (BLE/CYT) | Top right | |
| C5 #1 (Dual-band Marauder) | Middle left | |
| C5 #2 (Dual-band Scanner) | Middle right | |
| Heltec LoRa V3 (Meshtastic) | Bottom left | OLED faces up |
| WROOM-32 (Drone RemoteID) | Bottom right | |

Alternatively, use **DIN rail mounting:**
1. Cut a 35mm DIN rail segment to approximately 7" length.
2. Mount the DIN rail horizontally on the ESP32 plate with screws.
3. Attach DIN rail PCB clips to each ESP32 board and clip onto the rail.

### 5.2 Mount CYD Touchscreens

1. **CYD #1 (Marauder):** Mount on the ESP32 plate facing upward. Connect via USB to
   Gold #1 for the Marauder touchscreen GUI.
2. **CYD #2 (HaleHound):** Mount on the ESP32 plate facing upward. This is a standalone
   unit running its own firmware.

### 5.3 Connect U.FL Pigtails to SMA Bulkheads

For each board with an IPEX connector, connect a U.FL-to-SMA pigtail:

| Board | IPEX Connector | Pigtail Routes To | Antenna Type |
|-------|----------------|-------------------|--------------|
| Gold #1 | IPEX near "ANT" | SMA #1 | 2.4GHz omni |
| Gold #2 | IPEX near "ANT" | SMA #2 | 2.4GHz omni |
| Gold #3 | IPEX near "ANT" | SMA #3 | 2.4GHz omni |
| C5 #1 | IPEX connector | SMA #4 | Bingfu dual-band 2.4/5.8GHz |
| C5 #2 | IPEX connector | SMA #5 | Bingfu dual-band 2.4/5.8GHz |
| Heltec V3 | IPEX for SX1262 | SMA #6 | 915MHz LoRa |

For each connection:
1. Align the U.FL connector directly over the board's IPEX socket.
2. Press **straight down** firmly until you feel/hear a click. Do not twist.
3. Route the pigtail cable away from the board (maintain 5mm+ minimum bend radius).
4. Route each pigtail to its assigned SMA bulkhead using the shortest clean path.
5. Screw the SMA end of each pigtail onto the interior side of its SMA bulkhead.
6. Keep pigtails away from power cables to minimize EMI interference.
7. Secure pigtail routing with adhesive cable clips along the plate edges.

**Panda PAU0F (SMA #7):** The PAU0F has its own antenna. Use an SMA extension cable
from the adapter to SMA bulkhead #7. Connect the PAU0F directly to Pi 5 USB 3.0 #1 (not
through the hub -- Kismet needs full USB 3.0 bandwidth).

**WROOM-32 and CYDs:** No external antenna needed -- they use internal PCB antennas.

### 5.4 Wire USB Cables Through Toggle Switches

Each toggle switch controls the 5V power line of one device. The switch is wired
**inline** on the USB cable's 5V wire (red wire), while the ground (black), data+
(green), and data- (white) wires pass through unbroken.

**For each device (SW1 through SW12):**

1. Cut a USB cable at the midpoint.
2. Strip the outer insulation to expose the 4 internal wires: red (5V), black (GND),
   green (D+), white (D-).
3. Cut only the **red (5V) wire.**
4. Strip 5mm of insulation from each end of the cut red wire.
5. Solder one end to the center terminal of the toggle switch.
6. Solder the other end to one of the outer terminals.
7. Apply heat shrink tubing over each solder joint.
8. Leave the black, green, and white wires intact and uncut.
9. Secure the spliced area with additional heat shrink or electrical tape.

**Wiring diagram per switch:**
```
USB Hub Port ----[RED]--[cut]--[SW toggle]--[RED continues]---- Device
                 [BLK]--------- passes through unbroken --------
                 [GRN]--------- passes through unbroken --------
                 [WHT]--------- passes through unbroken --------
```

**Switch assignments:**

| Switch | Device | Hub Port |
|--------|--------|----------|
| SW1 | Gold #1 (Marauder 2.4G) | Hub 1 |
| SW2 | Gold #2 (Flock) | Hub 2 |
| SW3 | Gold #3 (BLE/CYT) | Hub 3 |
| SW4 | C5 #1 (Dual-band Marauder) | Hub 4 |
| SW5 | C5 #2 (Dual-band Scanner) | Hub 5 |
| SW6 | Heltec LoRa V3 (Meshtastic) | Hub 6 |
| SW7 | WROOM-32 (Drone RemoteID) | Hub 7 |
| SW8 | CYD #2 (HaleHound) | Hub 8 |
| SW9 | Pi Zero 2W (RaspyJack) | Hub 9 |
| SW10 | RT5370 (Kismet secondary) | Hub 10 |
| SW11 | VK-162 GPS | Hub 11 |
| SW12 | Orbic RC400L (RayHunter) | Hub 12 (charge only) |

**Always-on (no switch):** Pi 5 + Panda PAU0F are connected directly to Pi 5 USB 3.0
ports, bypassing the hub and switches entirely.

### 5.5 Wire the 12V Fan Boost Converter

The IP67 fans are 12V. The Anker 347 outputs 5V. Bridge with the DROK boost converter:

1. Connect the input of the 5V-to-12V boost converter to a USB-A cable from the
   Anker 347 (cut the USB-A cable, solder red/black to the boost converter input).
2. Connect the output of the boost converter to the two IP67 fans in parallel.
3. Verify output voltage with a multimeter: should read 12.0V (+/- 0.5V).
4. Mount the boost converter on the base plate with double-sided foam tape.

### 5.6 Cable Management

1. Use **adhesive cable clips** (from the 30-pack) along the edges of both plates.
2. Route USB cables in bundles of 2-3, secured with small zip ties every 2".
3. Keep USB data cables away from the U.FL pigtails (minimize EMI coupling).
4. Keep power cables (boost converter, fan wires) separated from signal cables.
5. Leave enough slack in each cable for the plates to be removed from the case without
   disconnecting anything.

---

## Phase 6: Displays

**Goal:** Mount all displays and verify visual output from every source.

### 6.1 Mount the 7" DSI Display in the Lid

1. Position the Hosyond 7" DSI touchscreen centered in the Pelican 1300 lid.
2. Mark the 4 mounting tab positions on the lid interior.
3. Attach **aluminum L-brackets** to the lid:
   - Use short M3 bolts through the L-brackets into the lid.
   - **Do not drill through the lid** -- use short standoffs with adhesive backing on
     the lid interior, or drill only partially into the lid material.
   - Breaking through the lid compromises the seal.
4. Screw the 7" display to the L-brackets using M3 screws.
5. Verify the display is secure and does not rattle.

### 6.2 Route the DSI Ribbon Cable

1. Connect the **22-pin to 15-pin DSI adapter** to the display's 22-pin connector.
2. Connect a **30cm DSI FPC extension cable** (15-pin, 1mm pitch) from the adapter.
3. Route the ribbon cable through the hinge gap between the lid and base.
4. Secure the ribbon cable with **Kapton tape** along the hinge area to prevent pinching
   when the lid opens and closes.
5. Connect the other end of the ribbon cable to the Pi 5's DSI port.
6. **Test:** open and close the lid 10 times slowly, checking that the ribbon cable
   moves freely without binding, kinking, or pinching.

### 6.3 Mount the Noctua Fan in the Lid

1. Mount the **Noctua NF-A4x10 5V** fan on the lid interior, near the display but not
   blocking the screen.
2. Position it to blow air across the display and down into the base for internal
   circulation.
3. Wire the fan:
   - **+5V** to Pi 5 GPIO pin 4 (5V power).
   - **GND** to Pi 5 GPIO pin 9 (ground).
   - **PWM** (if 4-pin fan) to Pi 5 GPIO 18 (pin 12) for temperature-based speed control.
4. Secure fan wires with adhesive cable clips along the lid interior.

### 6.4 Mount the 2.42" SSD1309 OLED

1. Mount the OLED module on the edge of the base plate or ESP32 plate, angled for
   visibility when the lid is open.
2. Wire to the Pi 5 GPIO:
   - **VCC** to pin 1 (3.3V).
   - **GND** to pin 14 (ground).
   - **SDA** to GPIO2 (pin 3).
   - **SCL** to GPIO3 (pin 5).
3. Use short Dupont jumper wires for the connection.
4. Verify I2C detection:
   ```bash
   i2cdetect -y 1
   ```
   The OLED should appear at address **0x3C** (or 0x3D depending on the module).

### 6.5 Mount CYD Touchscreens

1. **CYD #1** is already connected to Gold #1 from [Section 5.2](#52-mount-cyd-touchscreens).
   Position it face-up on the ESP32 plate for touch access.
2. **CYD #2** (HaleHound) is standalone -- position it face-up adjacent to CYD #1.

### 6.6 Test All Displays

Power on the deck and verify every display:

| Display | Expected Output |
|---------|----------------|
| 7" DSI | Kali Linux desktop or console |
| CYD #1 | Marauder touchscreen menu |
| CYD #2 | HaleHound touchscreen menu |
| 2.42" OLED | Nothing yet (software not written -- will show vitals in Phase 7) |
| Heltec OLED | Meshtastic node status |

---

## Phase 7: Software Integration

**Goal:** Configure all software services, udev rules, the Flask dashboard, OLED monitor,
and Chromium kiosk mode on the Pi 5.

### 7.1 Configure Serial Device Rules (udev)

By default, Linux assigns `/dev/ttyUSB0`, `/dev/ttyUSB1`, etc. in the order devices
enumerate. This is not deterministic -- the same board could be ttyUSB0 one boot and
ttyUSB3 the next. Fix this with udev rules that assign stable symlinks.

1. Plug in each device one at a time and note its USB attributes:
   ```bash
   udevadm info -a -n /dev/ttyUSB0 | grep -E '{idVendor}|{idProduct}|{serial}'
   ```

2. Create the udev rules file:
   ```bash
   sudo nano /etc/udev/rules.d/99-cyberdeck.rules
   ```

3. Add a rule for each device (adjust vendor/product/serial to match your hardware):
   ```
   # Gold #1 - Marauder 2.4GHz
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", ATTRS{serial}=="XXXXXXXX", SYMLINK+="marauder24"

   # Gold #2 - Flock Detection
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", ATTRS{serial}=="YYYYYYYY", SYMLINK+="flock"

   # Gold #3 - BLE Scanner
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", ATTRS{serial}=="ZZZZZZZZ", SYMLINK+="ble_scanner"

   # C5 #1 - Dual-band Marauder
   SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", ATTRS{serial}=="C5_1_SER", SYMLINK+="marauder5g"

   # C5 #2 - Dual-band Scanner
   SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", ATTRS{serial}=="C5_2_SER", SYMLINK+="scanner5g"

   # Heltec LoRa V3 - Meshtastic
   SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="meshtastic"

   # WROOM-32 - Drone RemoteID
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", ATTRS{serial}=="WROOM_SER", SYMLINK+="drone_rid"

   # CYD #2 - HaleHound
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", ATTRS{serial}=="CYD2_SER", SYMLINK+="halehound"

   # VK-162 GPS
   SUBSYSTEM=="tty", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a7", SYMLINK+="gps"
   ```

   **Note:** If multiple devices share the same vendor/product IDs (common with CH340
   chips), you must differentiate by the `ATTRS{serial}` field, or by the physical USB
   port path using `KERNELS`.

   Alternative -- differentiate by USB port path:
   ```
   SUBSYSTEM=="tty", KERNELS=="1-1.2:1.0", SYMLINK+="marauder24"
   SUBSYSTEM=="tty", KERNELS=="1-1.3:1.0", SYMLINK+="flock"
   ```
   This approach requires that each device always plugs into the same physical hub port.

4. Reload udev rules:
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

5. Verify symlinks exist:
   ```bash
   ls -la /dev/marauder24 /dev/flock /dev/ble_scanner /dev/meshtastic /dev/drone_rid /dev/gps
   ```

### 7.2 Configure gpsd

Update gpsd to use the stable symlink:

```bash
sudo nano /etc/default/gpsd
```
```
DEVICES="/dev/gps"
GPSD_OPTIONS="-n"
```
```bash
sudo systemctl restart gpsd
```

Verify:
```bash
cgps -s
```

### 7.3 Configure Kismet

1. Add the current user to the kismet group:
   ```bash
   sudo usermod -aG kismet kali
   ```

2. Edit Kismet configuration:
   ```bash
   sudo nano /etc/kismet/kismet.conf
   ```
   Add/modify:
   ```
   source=wlan1:type=linuxwifi
   gps=gpsd:host=localhost,port=2947
   ```
   (`wlan1` is typically the Panda PAU0F interface. Verify with `iwconfig`.)

3. Set the Panda PAU0F to monitor mode:
   ```bash
   sudo ip link set wlan1 down
   sudo iw wlan1 set monitor none
   sudo ip link set wlan1 up
   ```

4. Test Kismet:
   ```bash
   kismet
   ```
   Open `http://localhost:2501` in Chromium. Verify networks are being captured.

### 7.4 Set Up ADB Port Forwarding for RayHunter

If you want to access RayHunter's web UI from the Pi 5 instead of joining the Orbic's
WiFi separately:

1. Connect the Orbic to a hub port via USB.
2. Verify ADB sees the device:
   ```bash
   adb devices
   ```
   Expected: the Orbic's serial number listed as "device".
3. Forward the port:
   ```bash
   adb forward tcp:8080 tcp:8080
   ```
4. Access RayHunter at `http://localhost:8080` from the Pi 5.

Create a systemd service for automatic forwarding (see [Appendix C](#appendix-c-systemd-service-templates)).

### 7.5 Build the Flask Dashboard

Create the cyberdeck dashboard that aggregates all device feeds:

1. Create the project directory:
   ```bash
   mkdir -p ~/cyberdeck-dashboard
   cd ~/cyberdeck-dashboard
   ```

2. Create the main application file `app.py`:
   ```python
   from flask import Flask, render_template
   from flask_socketio import SocketIO
   import serial
   import threading
   import json
   import subprocess
   from gps3 import gps3
   import psutil

   app = Flask(__name__)
   socketio = SocketIO(app)

   # Serial device paths (using udev symlinks)
   DEVICES = {
       'marauder24': '/dev/marauder24',
       'flock': '/dev/flock',
       'ble_scanner': '/dev/ble_scanner',
       'marauder5g': '/dev/marauder5g',
       'scanner5g': '/dev/scanner5g',
       'meshtastic': '/dev/meshtastic',
       'drone_rid': '/dev/drone_rid',
       'halehound': '/dev/halehound',
   }

   def serial_reader(name, port, baud=115200):
       """Read serial data from a device and emit via WebSocket."""
       try:
           ser = serial.Serial(port, baud, timeout=1)
           while True:
               line = ser.readline().decode('utf-8', errors='ignore').strip()
               if line:
                   socketio.emit(f'serial_{name}', {'data': line})
       except Exception as e:
           socketio.emit(f'serial_{name}', {'data': f'ERROR: {str(e)}'})

   def gps_reader():
       """Read GPS data from gpsd and emit via WebSocket."""
       gps_socket = gps3.GPSDSocket()
       data_stream = gps3.DataStream()
       gps_socket.connect()
       gps_socket.watch()
       for new_data in gps_socket:
           if new_data:
               data_stream.unpack(new_data)
               socketio.emit('gps', {
                   'lat': str(data_stream.TPV['lat']),
                   'lon': str(data_stream.TPV['lon']),
                   'speed': str(data_stream.TPV['speed']),
                   'alt': str(data_stream.TPV['alt']),
               })

   def system_monitor():
       """Read system stats and emit via WebSocket."""
       import time
       while True:
           cpu_temp = float(subprocess.check_output(
               ['vcgencmd', 'measure_temp']
           ).decode().split('=')[1].split("'")[0])
           socketio.emit('system', {
               'cpu_temp': cpu_temp,
               'cpu_percent': psutil.cpu_percent(),
               'ram_percent': psutil.virtual_memory().percent,
           })
           time.sleep(2)

   @app.route('/')
   def index():
       return render_template('index.html')

   if __name__ == '__main__':
       # Start serial readers for each connected device
       for name, port in DEVICES.items():
           t = threading.Thread(target=serial_reader, args=(name, port), daemon=True)
           t.start()

       # Start GPS reader
       threading.Thread(target=gps_reader, daemon=True).start()

       # Start system monitor
       threading.Thread(target=system_monitor, daemon=True).start()

       socketio.run(app, host='0.0.0.0', port=5000)
   ```

3. Create the template directory and `templates/index.html`:
   ```bash
   mkdir -p ~/cyberdeck-dashboard/templates
   ```
   Build an HTML page with tabs for each subsystem: WiFi, BLE, Mesh, Flock, Drone,
   RayHunter, System. Use Socket.IO on the client side to receive real-time updates.
   The dashboard runs at 800x480 resolution for the 7" touchscreen.

4. Test the dashboard:
   ```bash
   cd ~/cyberdeck-dashboard
   python3 app.py
   ```
   Open `http://localhost:5000` in Chromium on the Pi 5.

### 7.6 Configure Chromium Kiosk Mode

Set up the 7" DSI display to boot directly into the dashboard:

1. Create an autostart entry:
   ```bash
   mkdir -p ~/.config/autostart
   nano ~/.config/autostart/cyberdeck-dashboard.desktop
   ```
   ```ini
   [Desktop Entry]
   Type=Application
   Name=Cyberdeck Dashboard
   Exec=chromium --kiosk --no-first-run --disable-restore-session-state http://localhost:5000
   X-GNOME-Autostart-enabled=true
   ```

2. Disable screen blanking:
   ```bash
   sudo nano /etc/lightdm/lightdm.conf
   ```
   Under `[Seat:*]`, add:
   ```
   xserver-command=X -s 0 -dpms
   ```

### 7.7 Write the OLED Temperature Monitor

Create a Python script that displays system vitals on the 2.42" SSD1309 OLED:

```bash
nano ~/cyberdeck-dashboard/temp_monitor.py
```

```python
#!/usr/bin/env python3
"""Cyberdeck OLED System Monitor -- 2.42" SSD1309 (128x64, I2C)."""

import time
import subprocess
import psutil
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1309
from luma.core.render import canvas
from PIL import ImageFont

# Initialize I2C OLED at address 0x3C
serial_interface = i2c(port=1, address=0x3C)
device = ssd1309(serial_interface, width=128, height=64)

# Use default font (or specify a TTF path for larger text)
font = ImageFont.load_default()

def get_cpu_temp():
    """Read Pi 5 CPU temperature."""
    result = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
    return float(result.split('=')[1].split("'")[0])

def get_active_tools():
    """Check which cyberdeck tools are running."""
    tools = []
    for proc in psutil.process_iter(['name']):
        name = proc.info['name'].lower()
        if 'kismet' in name:
            tools.append('KIS')
        if 'flask' in name or 'python3' in name:
            tools.append('DSH')
        if 'gpsd' in name:
            tools.append('GPS')
    return tools

while True:
    cpu_temp = get_cpu_temp()
    cpu_pct = psutil.cpu_percent(interval=0.5)
    ram_pct = psutil.virtual_memory().percent
    tools = get_active_tools()

    with canvas(device) as draw:
        draw.text((0, 0), f"CPU: {cpu_temp:.1f}C  {cpu_pct:.0f}%", font=font, fill="white")
        draw.text((0, 12), f"RAM: {ram_pct:.0f}%", font=font, fill="white")
        draw.text((0, 24), f"Tools: {' '.join(tools)}", font=font, fill="white")

        # Throttle warning
        throttled = subprocess.check_output(['vcgencmd', 'get_throttled']).decode().strip()
        if throttled != "throttled=0x0":
            draw.text((0, 48), "! THROTTLED !", font=font, fill="white")
        else:
            draw.text((0, 48), "Status: OK", font=font, fill="white")

    time.sleep(2)
```

Make it executable:
```bash
chmod +x ~/cyberdeck-dashboard/temp_monitor.py
```

Test it:
```bash
python3 ~/cyberdeck-dashboard/temp_monitor.py
```
The OLED should display CPU temp, CPU usage, RAM usage, and active tools.

### 7.8 Create Systemd Services for Auto-Start

Create services so everything starts automatically on boot, in the correct order:

1. **gpsd** -- already enabled from Section 1.4.

2. **Kismet:**
   ```bash
   sudo nano /etc/systemd/system/cyberdeck-kismet.service
   ```
   ```ini
   [Unit]
   Description=Kismet Wardriving
   After=network.target gpsd.service
   Wants=gpsd.service

   [Service]
   Type=simple
   User=kali
   ExecStart=/usr/bin/kismet --no-ncurses
   Restart=on-failure
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. **Flask Dashboard:**
   ```bash
   sudo nano /etc/systemd/system/cyberdeck-dashboard.service
   ```
   ```ini
   [Unit]
   Description=Cyberdeck Flask Dashboard
   After=network.target gpsd.service

   [Service]
   Type=simple
   User=kali
   WorkingDirectory=/home/kali/cyberdeck-dashboard
   ExecStart=/usr/bin/python3 /home/kali/cyberdeck-dashboard/app.py
   Restart=on-failure
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

4. **OLED Monitor:**
   ```bash
   sudo nano /etc/systemd/system/cyberdeck-oled.service
   ```
   ```ini
   [Unit]
   Description=Cyberdeck OLED System Monitor
   After=multi-user.target

   [Service]
   Type=simple
   User=kali
   ExecStart=/usr/bin/python3 /home/kali/cyberdeck-dashboard/temp_monitor.py
   Restart=on-failure
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

5. **ADB Port Forward (RayHunter):**
   ```bash
   sudo nano /etc/systemd/system/cyberdeck-rayhunter.service
   ```
   ```ini
   [Unit]
   Description=RayHunter ADB Port Forward
   After=multi-user.target

   [Service]
   Type=simple
   User=kali
   ExecStart=/usr/bin/adb forward tcp:8080 tcp:8080
   Restart=on-failure
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

6. Enable all services:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable cyberdeck-kismet
   sudo systemctl enable cyberdeck-dashboard
   sudo systemctl enable cyberdeck-oled
   sudo systemctl enable cyberdeck-rayhunter
   ```

7. Add the Noctua fan PWM control to `/boot/config.txt`:
   ```bash
   sudo nano /boot/config.txt
   ```
   Add:
   ```
   dtoverlay=gpio-fan,gpiopin=18,temp=55000
   ```
   This activates the fan when the CPU exceeds 55C.

8. Reboot and verify all services start:
   ```bash
   sudo reboot
   ```
   After reboot:
   ```bash
   sudo systemctl status cyberdeck-kismet
   sudo systemctl status cyberdeck-dashboard
   sudo systemctl status cyberdeck-oled
   sudo systemctl status cyberdeck-rayhunter
   ```
   All should show `active (running)`.

---

## Phase 8: Integration Testing

**Goal:** Verify the complete cyberdeck works as a system. Test power, thermal,
functionality, and weatherproofing.

### 8.1 Full Power-On Test

1. Close all toggle switches to OFF.
2. Power on the Anker 347.
3. Verify Pi 5 boots and the 7" DSI displays Kali desktop.
4. Verify the dashboard auto-launches in Chromium.
5. Verify the OLED displays system vitals.
6. Turn on switches **one at a time** in order (SW1 through SW12):
   - After each switch, wait 5 seconds and verify the device appears in `lsusb` and
     the corresponding serial symlink exists in `/dev/`.
   - Check for any USB errors in `dmesg | tail -20`.
7. With all 12 switches on, verify all 14 devices are operational simultaneously:
   ```bash
   ls -la /dev/marauder24 /dev/flock /dev/ble_scanner /dev/marauder5g /dev/scanner5g /dev/meshtastic /dev/drone_rid /dev/halehound /dev/gps
   lsusb
   ```

### 8.2 Sealed Thermal Test

1. Close the Pelican 1300 lid with all devices running.
2. Monitor the OLED and dashboard for CPU temperature.
3. Run for **30 continuous minutes** with all devices active.
4. Targets:
   - Pi 5 CPU temperature: **below 70C**
   - No throttling (`vcgencmd get_throttled` returns `0x0`)
   - Case exterior should feel warm but not hot to the touch
5. If temps exceed 70C:
   - Increase fan voltage (check boost converter output).
   - Add thermal pads between the Pi 5 heatsink and the nearest case wall.
   - Consider adding a second membrane vent.
   - Reduce simultaneous device count (turn off unused switches).
6. Re-test after any thermal modifications.

### 8.3 Battery Runtime Test

1. Fully charge the Anker 347 (all LEDs solid).
2. Power on the cyberdeck with all 12 switches active (maximum draw).
3. Start a timer.
4. Run until the Pi 5 shuts down from low power.
5. Record the total runtime.
6. Target: **3-4 hours at full load.** The Anker 347 at 92Wh with approximately 4A
   average draw should deliver approximately 4-5 hours.
7. Repeat the test with a "wardriving only" profile (SW10 + SW11 only) to establish
   the low-power runtime baseline.

### 8.4 Antenna Range Tests

Test each antenna/radio frequency band for expected range:

| Antenna | Test | Method | Expected Range |
|---------|------|--------|---------------|
| SMA 1-3 (2.4GHz) | WiFi AP scan | Walk away from a known AP, note RSSI at distance | 400-600m open field with 5dBi |
| SMA 4-5 (dual-band) | 5GHz AP scan | Same as above on a 5GHz network | 150-300m with 5dBi |
| SMA 6 (915MHz LoRa) | Meshtastic range | Walk/drive with a second node, note max range | 2-5km suburban, 10km+ LOS |
| SMA 7 (WiFi 6E) | Kismet 6GHz scan | Scan for 6GHz networks | Depends on environment |

### 8.5 Drive Test

1. Mount the cyberdeck in a vehicle (passenger seat or secured in footwell).
2. Screw on all antennas.
3. Power on with the driving profile:
   - SW2 (Flock): ON -- watch for ALPR cameras
   - SW10 (Kismet secondary): ON -- wardriving
   - SW11 (GPS): ON -- location logging
   - SW6 (Meshtastic): ON -- mesh comms
4. Drive a known route (20-30 minutes) through areas with Flock cameras if possible.
5. After the drive:
   - Check Kismet logs for captured networks.
   - Check Flock serial output for any ALPR detections.
   - Verify GPS track was logged.
   - Export Kismet data to WiGLE-compatible CSV if desired.

### 8.6 Walk Test

1. Carry the cyberdeck by the handle.
2. Enable the walking profile:
   - SW3 (BLE): ON -- scan for trackers
   - SW6 (Meshtastic): ON -- mesh comms
   - SW12 (RayHunter): charging -- check Orbic periodically
3. Walk through a crowded area (mall, downtown) for 15-20 minutes.
4. After the walk:
   - Check BLE scanner output for detected trackers.
   - Check for any persistent MAC addresses that appeared throughout the walk (possible tail).
   - Check Meshtastic for nearby nodes.
   - Check RayHunter dashboard for any alerts.

### 8.7 Water Resistance Spray Test

1. Close all SMA dust caps onto the bulkheads.
2. Close the Pelican lid and engage all latches.
3. **Do not power on the deck during this test.**
4. Using a garden hose with a spray nozzle, spray the case from all angles for
   30 seconds per side, focusing on:
   - SMA bulkheads
   - Toggle switches
   - Fan openings
   - USB-C and USB-A panel mounts
   - The membrane vent
5. Open the case and inspect every penetration point for water ingress.
6. If any water entered:
   - Identify the failed seal.
   - Dry the interior completely.
   - Reapply marine sealant to the failed point.
   - Cure 24 hours.
   - Retest.

---

## Phase 9: Finishing

**Goal:** Label everything, add protective accessories, and create a quick-start reference.

### 9.1 Label All SMA Bulkheads

Use a label maker (Brother P-Touch or similar) or permanent marker:

| Bulkhead | Label |
|----------|-------|
| SMA 1 | WIFI 2.4 / MAR |
| SMA 2 | WIFI 2.4 / FLK |
| SMA 3 | BLE / CYT |
| SMA 4 | DUAL / 5G-M |
| SMA 5 | DUAL / 5G-S |
| SMA 6 | LORA / 915M |
| SMA 7 | WIFI 6E / KIS |

### 9.2 Label All Toggle Switches

Label below each switch:

| Switch | Label |
|--------|-------|
| SW1 | MAR |
| SW2 | FLK |
| SW3 | BLE |
| SW4 | 5GM |
| SW5 | 5GS |
| SW6 | MSH |
| SW7 | DRN |
| SW8 | IOT |
| SW9 | NET |
| SW10 | KS2 |
| SW11 | GPS |
| SW12 | RAY |

### 9.3 Apply Anti-Slip Rubber Feet

1. Apply adhesive rubber feet to the bottom of the Pelican 1300 case (4 corners).
2. This prevents the case from sliding on smooth surfaces during operation.

### 9.4 Install SMA Dust Caps

1. Screw **gold-plated SMA dust caps** onto all 7 SMA bulkheads.
2. These protect the SMA connectors during transport (when antennas are removed and stored).
3. Dust caps also help maintain the waterproof seal when antennas are not attached.

### 9.5 Write Quick-Start Card

Create a laminated reference card that fits inside the Pelican lid pocket:

```
CYBERDECK QUICK-START
=====================
1. Open case, attach antennas to SMA 1-7
2. Press Anker 347 power button (side)
3. Wait 30s for Pi 5 boot
4. Dashboard auto-loads on 7" screen
5. Toggle switches for desired profile:

PROFILES:
  Full Scan:  ALL switches ON
  Wardriving: SW10 + SW11
  Surveillance Detect: SW2 + SW3 + SW11
  Stealth:    ALL switches OFF (Pi + PAU0F only)
  IoT Recon:  SW8 + SW9
  Mesh Only:  SW6

SHUTDOWN:
  sudo shutdown -h now (or close lid and hold Anker button 3s)

PASSWORDS:
  Kali: [your password]
  Kismet: http://localhost:2501
  Dashboard: http://localhost:5000
  RayHunter: http://192.168.1.1:8080 (Orbic WiFi)
```

Print on cardstock and laminate with self-adhesive laminating sheets.

---

# Appendices

## Appendix A: Master Wiring Table

| Board / Device | Deck Slot | Power Source | Switch | SMA Port | Antenna | Display | Serial Path |
|----------------|-----------|-------------|--------|----------|---------|---------|-------------|
| Pi 5 8GB | Brain | Anker 347 USB-C PD | Always on | -- | -- | 7" DSI | -- |
| Panda PAU0F | Kismet primary | Pi 5 USB 3.0 #1 | Always on | SMA #7 | Built-in / SMA ext | -- | -- |
| Gold #1 | Marauder 2.4GHz | Hub -> SW1 | SW1 | SMA #1 | DIYmall 2.4G | CYD #1 | /dev/marauder24 |
| Gold #2 | Flock detection | Hub -> SW2 | SW2 | SMA #2 | DIYmall 2.4G | -- | /dev/flock |
| Gold #3 | BLE + CYT | Hub -> SW3 | SW3 | SMA #3 | DIYmall 2.4G | -- | /dev/ble_scanner |
| C5 #1 | Dual-band Marauder | Hub -> SW4 | SW4 | SMA #4 | Bingfu dual-band | -- | /dev/marauder5g |
| C5 #2 | Dual-band Scanner | Hub -> SW5 | SW5 | SMA #5 | Bingfu dual-band | -- | /dev/scanner5g |
| Heltec V3 | Meshtastic | Hub -> SW6 | SW6 | SMA #6 | 915MHz LoRa | OLED 0.96" | /dev/meshtastic |
| WROOM-32 | Drone RemoteID | Hub -> SW7 | SW7 | Internal | PCB trace | -- | /dev/drone_rid |
| CYD #2 | HaleHound | Hub -> SW8 | SW8 | Internal | PCB trace | 2.8" touch | /dev/halehound |
| Pi Zero 2W | RaspyJack | Hub -> SW9 | SW9 | Internal | -- | 1.44" LCD HAT | USB gadget |
| RT5370 | Kismet secondary | Hub -> SW10 | SW10 | Internal | Built-in | -- | -- |
| VK-162 | GPS | Hub -> SW11 | SW11 | Internal | Built-in | -- | /dev/gps |
| Orbic RC400L | RayHunter | Hub -> SW12 | SW12 | Internal | Cellular | -- | ADB |

## Appendix B: USB Device Rules (udev)

Complete udev rules file for stable serial device naming. Save to
`/etc/udev/rules.d/99-cyberdeck.rules`:

```
# Cyberdeck Serial Device Rules
# Reload after editing: sudo udevadm control --reload-rules && sudo udevadm trigger

# To find attributes for a new device:
# udevadm info -a -n /dev/ttyUSB0 | grep -E '{idVendor}|{idProduct}|{serial}'

# If multiple CH340 devices share VID:PID, differentiate by USB port path:
# udevadm info -a -n /dev/ttyUSB0 | grep KERNELS
# Use KERNELS=="1-1.2:1.0" etc. to match physical port position

# ESP32 Gold boards (CH340 bridge, VID:PID 1a86:7523)
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.1:1.0", SYMLINK+="marauder24", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.2:1.0", SYMLINK+="flock", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.3:1.0", SYMLINK+="ble_scanner", MODE="0666"

# ESP32-C5 boards (native USB, VID:PID 303a:1001)
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", KERNELS=="1-1.4:1.0", SYMLINK+="marauder5g", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", KERNELS=="1-1.5:1.0", SYMLINK+="scanner5g", MODE="0666"

# Heltec LoRa V3 (CP2102/CH340 bridge)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="meshtastic", MODE="0666"

# WROOM-32 Drone RemoteID
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.6:1.0", SYMLINK+="drone_rid", MODE="0666"

# CYD #2 HaleHound
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.7:1.0", SYMLINK+="halehound", MODE="0666"

# VK-162 GPS (u-blox)
SUBSYSTEM=="tty", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a7", SYMLINK+="gps", MODE="0666"
```

**Note:** The `KERNELS` values above are placeholders. You must determine your actual USB
port paths by plugging each device into its designated hub port and running
`udevadm info -a -n /dev/ttyUSBx | grep KERNELS`.

## Appendix C: Systemd Service Templates

All service files are located in `/etc/systemd/system/`. After creating or modifying any
service file:

```bash
sudo systemctl daemon-reload
sudo systemctl enable <service-name>
sudo systemctl start <service-name>
sudo systemctl status <service-name>
```

### Boot Order (dependency chain)

```
gpsd (system)
  |
  +-> cyberdeck-kismet (depends on gpsd)
  +-> cyberdeck-dashboard (depends on gpsd)
  +-> cyberdeck-oled (no deps)
  +-> cyberdeck-rayhunter (no deps)
```

### cyberdeck-kismet.service

```ini
[Unit]
Description=Cyberdeck Kismet Wardriving
After=network.target gpsd.service
Wants=gpsd.service

[Service]
Type=simple
User=kali
ExecStart=/usr/bin/kismet --no-ncurses
Restart=on-failure
RestartSec=5
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

### cyberdeck-dashboard.service

```ini
[Unit]
Description=Cyberdeck Flask Dashboard
After=network.target gpsd.service
Wants=gpsd.service

[Service]
Type=simple
User=kali
WorkingDirectory=/home/kali/cyberdeck-dashboard
ExecStart=/usr/bin/python3 /home/kali/cyberdeck-dashboard/app.py
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### cyberdeck-oled.service

```ini
[Unit]
Description=Cyberdeck OLED System Monitor (2.42" SSD1309)
After=multi-user.target

[Service]
Type=simple
User=kali
ExecStart=/usr/bin/python3 /home/kali/cyberdeck-dashboard/temp_monitor.py
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### cyberdeck-rayhunter.service

```ini
[Unit]
Description=RayHunter ADB Port Forward (Orbic RC400L)
After=multi-user.target

[Service]
Type=oneshot
RemainAfterExit=yes
User=kali
ExecStart=/usr/bin/adb forward tcp:8080 tcp:8080
ExecStop=/usr/bin/adb forward --remove tcp:8080

[Install]
WantedBy=multi-user.target
```

## Appendix D: Troubleshooting

### Serial device not appearing

| Symptom | Cause | Fix |
|---------|-------|-----|
| No `/dev/ttyUSB*` at all | Charge-only USB cable | Swap to a verified data cable |
| Device in `lsusb` but no tty | Missing CH340/CP210x driver | Install driver, reboot |
| Wrong symlink assignment | udev rule mismatch | Re-check KERNELS path, reload rules |
| ttyUSB numbers change between boots | No udev rules | Create udev rules (Appendix B) |
| "Permission denied" on serial | User not in dialout group | `sudo usermod -aG dialout kali` |

### Flash failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Failed to connect" during esptool | Board not in bootloader | Hold BOOT, press RST, release BOOT |
| Flash starts but fails mid-write | Baud rate too high | Drop to `--baud 115200` |
| Flash completes but board won't boot | Wrong firmware variant | Verify chip with `esptool.py chip_id`, use matching bin |
| "Invalid head of packet" | Corrupted download | Re-download firmware, verify checksum |

### Thermal issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pi 5 throttling (> 80C) | Inadequate cooling | Add thermal pads, increase fan speed, open lid |
| Case exterior very hot | Heat not being exhausted | Check fan direction (intake vs exhaust), clear obstructions |
| Condensation inside case | Sealed too tightly | Install or check membrane vent, run fans to circulate |

### Power issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pi 5 shows lightning bolt icon | Undervoltage (< 4.7V) | Use USB-C PD cable (not USB-A to C), check Anker charge level |
| Devices randomly disconnecting | Hub underpowered | Use powered hub, check hub power supply |
| Short battery life | Too many devices active | Use power profiles (switch off unused devices) |
| Boost converter output wrong | Potentiometer misadjusted | Measure with multimeter, adjust to 12.0V |

### Meshtastic not detected

| Symptom | Cause | Fix |
|---------|-------|-----|
| Board powers (OLED on) but no serial | Charge-only cable | Swap cable |
| No serial device in `/dev/` | Missing CH340 driver | Install CH341SER or CP210x driver |
| "No Meshtastic device found" in CLI | Wrong port | Check `ls /dev/ttyUSB*`, specify correct port |
| Region not set | LoRa won't TX without region | `meshtastic --set lora.region US` |

### RayHunter issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Installer fails | Wrong admin password | Check device label, try default Kajeet password |
| Web UI not accessible | Wrong network | Join Orbic's WiFi, not your home WiFi |
| ADB not seeing device | USB connection issue | Try different cable, check `adb devices` |
| No SIM error | SIM not inserted or not seated | Reinsert SIM card, any deactivated SIM works |

---

*This is a living document. Update as the build progresses, parts change, or firmware
versions are updated. Refer to the [main cyberdeck README](README.md) for design
rationale and the [integrations index](integrations/README.md) for per-subsystem guides.*
