# BLE (Bluetooth Low Energy) Detection and Tracking -- Comprehensive Guide

---

## Table of Contents

1. [Overview: BLE Scanning, Protocols, and Advertising](#1-overview-ble-scanning-protocols-and-advertising)
2. [Methods: Detection and Tracking Approaches](#2-methods-detection-and-tracking-approaches)
3. [Hardware Requirements](#3-hardware-requirements)
4. [Setup Guides](#4-setup-guides)
5. [Tracker Detection (AirTags, Tile, SmartTags)](#5-tracker-detection-airtags-tile-smarttags)
6. [Privacy Applications](#6-privacy-applications)
7. [Legal Considerations](#7-legal-considerations)
8. [Summary: Method Comparison](#8-summary-method-comparison)
9. [Sources](#9-sources)

---

## 1. Overview: BLE Scanning, Protocols, and Advertising

### What Is BLE?

Bluetooth Low Energy (BLE), introduced in the Bluetooth 4.0 specification, is a wireless protocol designed for short-range communication with minimal power consumption. Unlike Classic Bluetooth (used for audio streaming, file transfer), BLE is optimized for periodic, small data bursts -- making it ideal for beacons, sensors, trackers, and presence detection.

### The BLE Advertising Mechanism

BLE operates in the 2.4 GHz ISM band and divides it into 40 channels (0-39). Three of these channels are dedicated exclusively to advertising:

| Channel | Frequency | Position |
|---------|-----------|----------|
| 37 | 2402 MHz | Start of band |
| 38 | 2426 MHz | Mid-band (between Wi-Fi channels 1 and 6) |
| 39 | 2480 MHz | End of band |

These three channels are deliberately spaced across the spectrum to minimize interference from Wi-Fi, Classic Bluetooth, and other 2.4 GHz devices. When a BLE device advertises, it transmits the same packet sequentially across all three channels, increasing the probability that at least one packet is successfully received by a scanner.

### Advertising Packet Structure

Each BLE advertising packet is a Protocol Data Unit (PDU) containing:

- **Preamble**: 1 byte synchronization pattern
- **Access Address**: 4 bytes (always `0x8E89BED6` for advertising)
- **Header**: PDU type (`ADV_IND`, `ADV_DIRECT_IND`, `ADV_NONCONN_IND`, `ADV_SCAN_IND`, `SCAN_REQ`, `SCAN_RSP`) and length
- **Advertiser Address**: 6-byte MAC address (public or random)
- **Payload**: Up to 31 bytes of advertising data (extended to 255 bytes in BLE 5.0)
- **CRC**: 3-byte integrity check

Common payload fields include device name, service UUIDs, TX power level, and manufacturer-specific data (used by iBeacon, Eddystone, AirTag, etc.).

### Advertising Intervals

Configurable from 20 ms to 10.24 seconds. Shorter intervals improve discoverability but increase power draw; longer intervals conserve battery but delay detection. AirTags, for example, advertise approximately every 2 seconds.

### Scanning Modes

- **Passive scanning**: The scanner listens for advertising packets without transmitting anything. Completely silent/undetectable.
- **Active scanning**: After receiving an advertising packet, the scanner sends a `SCAN_REQ` to the advertiser, which responds with a `SCAN_RSP` containing additional data. This reveals the scanner's presence.

### Key BLE Beacon Standards

- **iBeacon** (Apple): Uses manufacturer-specific data with Apple's company ID (`0x004C`), followed by UUID (16 bytes), Major (2 bytes), Minor (2 bytes), and TX Power (1 byte).
- **Eddystone** (Google): Supports multiple frame types -- Eddystone-UID (namespace + instance ID), Eddystone-URL (broadcasts a URL), and Eddystone-TLM (telemetry data).
- **AltBeacon**: Open-source alternative with similar structure to iBeacon.

### RSSI (Received Signal Strength Indicator)

RSSI is measured in dBm (typically -30 to -100 dBm for BLE). Key characteristics:

- Closer devices yield higher (less negative) RSSI values (e.g., -30 dBm = very close)
- Farther devices yield lower (more negative) RSSI values (e.g., -90 dBm = far away)
- RSSI is inherently noisy due to multipath reflection, body absorption, wall attenuation, and antenna orientation
- With proper calibration and smoothing algorithms (Kalman filter, running average), room-level accuracy of 95%+ is achievable

---

## 2. Methods: Detection and Tracking Approaches

### Method A: ESP32 BLE Scanning (DIY)

The ESP32 is a low-cost (~$5-15) microcontroller with built-in Wi-Fi and BLE support. It can be programmed via Arduino IDE or ESP-IDF to continuously scan for BLE advertising packets.

**How it works**: The ESP32 performs passive or active BLE scans, collecting MAC addresses, device names, RSSI values, and manufacturer data from all nearby BLE devices. Results can be logged locally, sent via MQTT to a server, or integrated with Home Assistant.

**Capabilities**:

- Detect any device broadcasting BLE advertisements
- Filter by MAC address, UUID, device name, or manufacturer ID
- Calculate approximate distance from RSSI + TX power calibration
- Identify specific device types (AirTags, Tiles, SmartTags, fitness trackers, phones)
- Run continuously on USB power or battery

**Supported ESP32 variants for BLE**:

| Variant | BLE Support | Notes |
|---------|-------------|-------|
| ESP32 (original) | BLE 4.2 | Widely available |
| ESP32-C3 | BLE 5.0 | Recommended for cost/simplicity |
| ESP32-S3 | BLE 5.0 | Improved range |
| ESP32-C6 | BLE 5.0 | Also supports 802.15.4 (Thread/Zigbee) |
| ESP32-S2 | None | Wi-Fi only -- not suitable |
| ESP32-P4 | None | Not suitable |

### Method B: BLEShark Nano

The BLEShark Nano by InfiShark Tech is a purpose-built, pocket-sized wireless security research multi-tool powered by the Seeed Studio XIAO ESP32-C3.

**What sets it apart**: Unlike a bare ESP32 dev board, the BLEShark Nano is a finished product with a 3D-printed case, 0.66" OLED display, three tactile buttons, 500mAh battery (6-12 hours active use), and USB-C charging. It ships with 30+ pre-built tools and receives OTA firmware updates.

**Key capabilities**:

- BLE device scanning and detection (AirTags, SmartTags, Tile, and all other BLE advertisers)
- BLE Spam (crafted packets that trigger popups on iOS, Windows, Android, Samsung)
- Wi-Fi AP Spam (beacon flooding)
- Wi-Fi Deauth attacks (2.4 GHz deauthentication frame injection)
- Bad-BT (wireless HID injection via BLE keyboard emulation, similar to USB Rubber Ducky)
- IR blaster (TV/AC/LED/fan control)
- Built-in games (Flappy Bird, Pong, Space Invaders)

**Price**: $39.99 USD (silicone case $12.99 extra). Available from [infishark.com](https://infishark.com/products/bleshark-nano) and [Tindie](https://www.tindie.com/products/infishark/bleshark-nano-prototype/).

### Method C: nRF Sniffer for Bluetooth LE

The nRF Sniffer, developed by Nordic Semiconductor, is the gold standard for deep BLE packet analysis. Unlike the ESP32 methods which primarily scan advertising data, the nRF Sniffer can capture full BLE traffic including connection setup, data exchange, and encrypted packets.

**How it works**: Firmware is flashed onto a Nordic development board or dongle, which then feeds raw BLE packets into Wireshark via an extcap plugin. Wireshark provides full protocol dissection and filtering.

**Capabilities**:

- Capture advertising packets on channels 37, 38, 39
- Follow and capture connected BLE sessions (data channels 0-36)
- Full packet dissection (headers, PDU types, ATT/GATT operations, SMP pairing)
- RSSI filtering (e.g., `rssi >= -70` to only capture nearby devices)
- CRC validation with color-coded corrupt packet highlighting
- Export captures as PCAP files for offline analysis
- Channel hopping across all 40 BLE channels

### Method D: Home Assistant ESPresense

ESPresense is open-source firmware that transforms ESP32 boards into room-level BLE presence detectors integrated with Home Assistant via MQTT.

**How it works**: Multiple ESP32 nodes (one per room) continuously scan for BLE advertisements. Each node measures RSSI for tracked devices and publishes to MQTT. Home Assistant compares RSSI readings across all nodes to determine which room a device is in.

**Alternative: Bermuda BLE Trilateration**

Bermuda is a newer Home Assistant custom integration that achieves similar room presence detection but with key differences:

| Feature | ESPresense | Bermuda |
|---------|-----------|---------|
| Firmware | Custom ESPresense firmware | Standard ESPHome (Bluetooth proxy) |
| Dedicated hardware | Yes (ESP32 must run only ESPresense) | No (ESP32 can run other ESPHome tasks) |
| Setup complexity | Higher (coordinate mapping, calibration) | Lower (simpler configuration) |
| MQTT required | Yes | No (uses HA native Bluetooth proxies) |
| 3D mapping | Yes (with floor plan) | No (nearest-node only) |
| iPhone tracking | Works but inconsistent | Reported as very reliable |
| Update speed | ~5-10 seconds | Under 10 seconds |

---

## 3. Hardware Requirements

### Method A: ESP32 BLE Scanner (DIY)

| Component | Options | Approx. Cost |
|-----------|---------|-------------|
| ESP32 board | ESP32 DevKit v1, ESP32-C3 Super Mini, ESP32-S3 DevKitC | $3-15 |
| USB cable | Micro-USB or USB-C (depends on board) | $2-5 |
| Power supply | USB power bank (for portable use) or USB wall adapter | $5-15 |
| Optional: OLED display | SSD1306 0.96" I2C | $3-5 |
| Optional: Case | 3D-printed enclosure | $0-10 |

**Total: $3-50 depending on accessories**

### Method B: BLEShark Nano

| Component | Cost |
|-----------|------|
| BLEShark Nano device | $39.99 |
| Silicone protective case (optional) | $12.99 |

**Specifications**:

- MCU: Seeed Studio XIAO ESP32-C3
- Display: 0.66" monochrome OLED
- Battery: 500mAh LiPo (6-12 hours active)
- Charging: USB-C
- Connectivity: BLE 5.0, Wi-Fi 2.4 GHz, IR
- Interface: 3 tactile buttons
- Firmware updates: OTA (automatic)

**Total: $40-53**

### Method C: nRF Sniffer

| Component | Options | Approx. Cost |
|-----------|---------|-------------|
| nRF52840 Dongle | Nordic nRF52840 Dongle (PCA10059) | $10 |
| Alternative: nRF52840 DK | Nordic nRF52840 Development Kit (PCA10056) | $45 |
| Alternative: MakerDiary nRF52840 MDK USB Dongle | Third-party compatible dongle | $20 |
| Alternative: Adafruit nRF52840 Express | Adafruit Feather board | $25 |
| Computer | Windows/macOS/Linux with USB port | (existing) |

**Software (free)**:

- Wireshark (v2.4.6 or later, v4.x recommended)
- nRF Sniffer firmware (from Nordic)
- nRF Connect for Desktop or nrfutil (for flashing)
- Python 3.x with pyserial

**Total: $10-45 for hardware**

### Method D: ESPresense / Bermuda

| Component | Quantity | Approx. Cost |
|-----------|----------|-------------|
| ESP32 boards (one per room) | 3-8 typical | $3-15 each |
| USB cables + wall adapters | 1 per board | $5-8 each |
| MQTT broker (Mosquitto) | 1 instance (ESPresense only) | Free (software) |
| Home Assistant instance | 1 | Free (on existing hardware) |
| BLE beacons/tags for tracking | 1 per person/asset | $5-25 each (Tile, iBeacon) |
| Optional: Raspberry Pi (for HA) | 1 | $35-75 |

**Total: $25-200+ depending on scale**

---

## 4. Setup Guides

### Setup A: ESP32 BLE Scanner (Arduino IDE)

#### Step 1: Install Arduino IDE and ESP32 Board Support

1. Download Arduino IDE from [arduino.cc](https://www.arduino.cc/)
2. Go to **File > Preferences > Additional Board Manager URLs**
3. Add: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
4. Go to **Tools > Board > Board Manager**, search "esp32", install "esp32 by Espressif Systems"

#### Step 2: Select Board and Port

1. Connect ESP32 via USB
2. **Tools > Board** > select your variant (e.g., "ESP32 Dev Module" or "ESP32C3 Dev Module")
3. **Tools > Port** > select the COM port

#### Step 3: Basic BLE Scanner Code

```cpp
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

BLEScan* pBLEScan;
int scanTime = 5; // seconds

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
        Serial.printf("Device: %s", advertisedDevice.getAddress().toString().c_str());
        if (advertisedDevice.haveName()) {
            Serial.printf(" | Name: %s", advertisedDevice.getName().c_str());
        }
        Serial.printf(" | RSSI: %d dBm", advertisedDevice.getRSSI());
        if (advertisedDevice.haveManufacturerData()) {
            String mfData = advertisedDevice.getManufacturerData();
            // Apple manufacturer ID = 0x004C
            if (mfData.length() >= 2 && (uint8_t)mfData[0] == 0x4C && (uint8_t)mfData[1] == 0x00) {
                Serial.print(" | [APPLE DEVICE]");
            }
        }
        Serial.println();
    }
};

void setup() {
    Serial.begin(115200);
    Serial.println("Starting BLE Scanner...");
    BLEDevice::init("");
    pBLEScan = BLEDevice::getScan();
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setActiveScan(true);  // Active scan gets more data
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);
}

void loop() {
    Serial.println("\n--- Scan Start ---");
    BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
    Serial.printf("Devices found: %d\n", foundDevices.getCount());
    pBLEScan->clearResults();
    delay(2000);
}
```

#### Step 4: Upload and Monitor

1. Click **Upload** (arrow button)
2. Open **Serial Monitor** (Tools > Serial Monitor) at 115200 baud
3. Watch BLE devices appear with MAC addresses, names, and RSSI values

#### Step 5: Advanced -- MQTT Integration

For Home Assistant integration, add WiFi + PubSubClient libraries and publish scan results to an MQTT topic. The open-source project [BLE-Scanner](https://github.com/gromeck/BLE-Scanner) on GitHub provides a complete implementation.

---

### Setup B: BLEShark Nano

#### Step 1: Unbox and Charge

1. Charge via USB-C until full
2. Power on using the button

#### Step 2: Navigate the Interface

- The 0.66" OLED displays menus navigated with three buttons (up, down, select)
- Main menu categories: BLE Tools, Wi-Fi Tools, IR Tools, Games, Settings

#### Step 3: BLE Scanning

1. Navigate to **BLE Tools > BLE Scan**
2. The device scans all three advertising channels
3. Detected devices display with MAC address, name (if available), and RSSI
4. Identify tracker types by manufacturer data (Apple `0x4C` for AirTags, Samsung for SmartTags)

#### Step 4: Firmware Updates

- The BLEShark Nano receives OTA updates automatically when connected to Wi-Fi
- New features and tools are added through firmware updates

#### Step 5: Safety Reminder

- BLE Spam, Wi-Fi Deauth, and Bad-BT features are for **authorized penetration testing only**
- Unauthorized use of deauth attacks violates FCC regulations and computer fraud laws

---

### Setup C: nRF Sniffer for Bluetooth LE

#### Step 1: Install Prerequisites

1. Install [Wireshark v4.x](https://www.wireshark.org/) from wireshark.org
2. Install [Python 3.x](https://www.python.org/) from python.org
3. Install [nRF Connect for Desktop](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-Desktop) from nordicsemi.com (or use nrfutil CLI)

#### Step 2: Flash Sniffer Firmware

1. Download the nRF Sniffer for Bluetooth LE package from Nordic's website
2. For nRF52840 Dongle:
   - Put dongle in DFU mode (press the RESET button while plugging in; LED pulses red)
   - Use nRF Connect Programmer to flash the sniffer firmware hex file
3. For nRF52840 DK:
   - Connect via USB and use nrfjprog:
     ```
     nrfjprog --program sniffer_firmware.hex --chiperase --verify
     ```

#### Step 3: Install Wireshark Plugin

1. Navigate to the extracted sniffer package folder
2. Run:
   ```
   pip3 install -r extcap/requirements.txt
   ```
3. Copy the extcap files to Wireshark's extcap folder:
   - **Windows**: `C:\Program Files\Wireshark\extcap\`
   - **macOS**: `/Applications/Wireshark.app/Contents/MacOS/extcap/`
   - **Linux**: `/usr/lib/x86_64-linux-gnu/wireshark/extcap/`
4. Copy the `Profile_nRF_Sniffer_Bluetooth_LE` folder to Wireshark's profiles directory

#### Step 4: Start Capturing

1. Open Wireshark
2. Select the "nRF Sniffer for Bluetooth LE" interface from the capture interface list
3. Select the Wireshark profile: **Edit > Configuration Profiles > "Profile_nRF_Sniffer_Bluetooth_LE"**
4. Click **Start Capture** (green shark fin)

#### Step 5: Filtering and Analysis

**Capture-level RSSI filter**:
```
rssi >= -70
```
(Only captures nearby devices)

**Display filters**:

| Filter | Purpose |
|--------|---------|
| `btle.advertising_header` | All advertising packets |
| `btle.advertising_address == aa:bb:cc:dd:ee:ff` | Specific device by MAC |
| `btcommon.eir_ad.entry.company_id == 0x004c` | iBeacon / Apple packets |
| `btle.advertising_header.pdu_type == 0x05` | Connection requests |

**Following a connection**: Click on a device in the device list toolbar, then the sniffer will follow that device into its connected session on data channels.

**CRC highlighting**: Go to **View > Coloring Rules** to color bad-CRC packets red.

---

### Setup D: ESPresense

#### Step 1: Flash ESPresense Firmware

1. Go to [espresense.com/firmware](https://espresense.com/firmware) in a Chrome/Edge browser (Web Serial required)
2. Connect your ESP32 via USB
3. Select your board type from the dropdown
4. Click "Install ESPresense" and follow the web-based flashing wizard

#### Step 2: Configure Wi-Fi and MQTT

1. After flashing, the ESP32 creates an AP named "ESPresense-XXXXXX"
2. Connect to it from your phone/laptop
3. A captive portal opens -- enter:
   - Wi-Fi SSID and password
   - MQTT broker IP address (your Home Assistant or Mosquitto server)
   - MQTT username and password
   - Room name (e.g., "living_room", "bedroom", "office")
4. Save and the ESP32 reboots, connecting to your network

#### Step 3: Set Up MQTT Broker (if not already running)

1. Install Mosquitto add-on in Home Assistant (**Settings > Add-ons > Mosquitto Broker**)
2. Configure a username/password
3. Start the add-on

#### Step 4: Home Assistant Integration

1. ESPresense uses MQTT auto-discovery -- devices appear automatically in HA
2. Go to **Settings > Devices & Services > MQTT** to see discovered ESPresense nodes
3. Each tracked BLE device creates a `device_tracker` entity with `home`/`not_home` state and a `room` attribute

#### Step 5: Deploy Multiple Nodes

1. Flash and configure one ESP32 per room you want to track
2. Ensure slight RSSI coverage overlap between adjacent rooms
3. Place nodes at chest height, away from metal objects and microwave ovens
4. Avoid placing directly behind furniture or inside cabinets

#### Step 6: Calibrate

1. Access the ESPresense web interface at `http://espresense-XXXXXX.local`
2. Adjust absorption factor (how much walls/obstacles attenuate signal)
3. Walk through rooms with your tracked device to verify correct room assignment

#### Alternative: Bermuda BLE Setup

1. Flash ESP32s with standard ESPHome firmware, enabling `bluetooth_proxy`
2. Install Bermuda via HACS (Home Assistant Community Store)
3. Bermuda automatically discovers BLE proxies and tracked devices
4. Configure area assignments in the Bermuda integration settings
5. No MQTT broker required -- uses native Home Assistant Bluetooth proxy infrastructure

---

## 5. Tracker Detection (AirTags, Tile, SmartTags)

### How BLE Trackers Work

All consumer BLE trackers share the same fundamental mechanism:

1. The tracker broadcasts BLE advertising packets at regular intervals
2. Nearby phones (belonging to anyone) receive these packets and relay the tracker's encrypted location to a cloud service
3. The tracker owner queries the cloud service to see the last-known location

| Tracker | Manufacturer Data Prefix | Network | Advertising Interval | Battery |
|---------|-------------------------|---------|---------------------|---------|
| Apple AirTag | `0x4C00` (Apple) | Find My (billions of Apple devices) | ~2 seconds | CR2032, ~1 year |
| Samsung SmartTag2 | Samsung BLE ID | SmartThings Find (Samsung Galaxy devices) | ~2 seconds | CR2032, ~500 days |
| Tile (various) | Tile company ID | Tile Network (Tile app users) | ~2-8 seconds | Varies by model |
| Chipolo ONE Spot | `0x4C00` (Apple Find My) | Find My (Apple network) | ~2 seconds | CR2032, ~1 year |

### Detecting Unknown Trackers with ESP32

Several open-source projects enable ESP32-based tracker detection:

**[AirTagTag](https://github.com/7ENSOR/AirTagTag)**:
- Scans for Apple manufacturer data (`0x4C`)
- Identifies AirTags specifically by payload structure
- Hosts a captive portal showing detected devices with RSSI/distance
- Dynamic trend analysis shows if a tracker is following you

**[CYD ESP32 AirTag Scanner](https://github.com/hevnsnt/CYD_ESP32-AirTag-Scanner)**:
- Runs on ESP32 with a CYD (Cheap Yellow Display) touchscreen
- Detects AirTags, Samsung SmartTags, and Tile trackers
- Displays MAC addresses and payloads without needing a phone

**[AirFlag](https://github.com/bennettjustin/AirFlag)**:
- Focuses on detecting AirTags in "disconnected" or "lost" modes (the states used for stalking)
- Scans for 30 seconds every 2.5 minutes to conserve power
- Ideal for continuous monitoring

### Built-in Phone Detection

**Apple (iOS 17.5+)**: Automatic alerts for unknown AirTags, SmartTags, Tile trackers, and any DULT-compatible tracker traveling with you. Shows "[Item] Found Moving With You" notification.

**Android (6.0+, updated 2024)**: Google rolled out the DULT standard in partnership with Apple. Android sends "Tracker traveling with you" alerts for unknown compatible trackers detected over time.

**Samsung (SmartThings app)**: "Unknown Tag Search" feature scans for unknown SmartTags nearby.

### The DULT Standard (Detecting Unwanted Location Trackers)

In May 2024, [Apple and Google jointly launched](https://thehackernews.com/2024/05/apple-and-google-launch-cross-platform.html) the cross-platform DULT specification:

- Works on iOS 17.5+ and Android 6.0+
- Provides automatic alerts when any compatible tracker travels with you
- Allows users to play a sound on the unknown tracker, view its identifier, and get disabling instructions
- Being further developed with the IETF (Internet Engineering Task Force)
- Tracker manufacturers can adopt the standard for cross-platform detection compatibility

### Identifying Tracker Types via BLE Scan

When scanning with an ESP32 or nRF Sniffer, trackers can be identified by:

- **Apple AirTag**: Manufacturer data starting with `0x4C 0x00`, followed by Apple's Find My payload type
- **Samsung SmartTag**: Samsung-specific BLE service UUIDs
- **Tile**: Tile-specific service UUID (`0xFEED` or `0xFEEC` depending on model)
- **Generic Find My devices** (Chipolo, etc.): Same Apple manufacturer prefix as AirTags

### Detection Limitations

- AirTags rotate their BLE MAC address every ~15 minutes, making long-term tracking by MAC alone difficult
- Researchers have demonstrated ESP32-based "stealth AirTag clones" that bypass Apple's anti-stalking protections by mimicking the address rotation pattern
- Tile trackers require the Tile app with "Scan and Secure" manually activated -- no automatic detection without DULT

---

## 6. Privacy Applications

### Defensive / Personal Privacy

1. **Stalker tracker detection**: Use an ESP32 scanner or BLEShark Nano to sweep your vehicle, bags, and personal spaces for unknown BLE trackers. Projects like AirTagTag provide continuous monitoring.

2. **Home presence automation**: ESPresense/Bermuda enable smart home automations (lights, HVAC, security) based on which room you're in, all processed locally -- no cloud dependency, no data leaving your network.

3. **BLE environment auditing**: Use the nRF Sniffer to analyze what BLE devices are broadcasting in your home, office, or vehicle. Identify unexpected transmitters (smart TVs, appliances, or planted devices).

4. **RF silence verification**: After removing a suspected tracker, use continuous BLE scanning to verify no devices are still broadcasting in your vicinity.

### Security Research

1. **Penetration testing**: The BLEShark Nano and ESP32 tools enable authorized testing of BLE-enabled devices (smart locks, medical devices, IoT sensors) to identify vulnerabilities.

2. **Protocol analysis**: The nRF Sniffer + Wireshark combination allows full dissection of BLE communications, including pairing procedures, GATT service enumeration, and data exchange.

3. **Replay and fuzzing**: Captured BLE packets can be analyzed to understand proprietary protocols and test device resilience.

### Asset Tracking (Legitimate)

1. **Equipment tracking**: Place BLE beacons on tools, equipment, or inventory. ESP32 scanners in fixed locations report which assets are in which area.

2. **Pet/child safety**: BLE tags on pets or children's backpacks, with ESP32 nodes providing localized alerts when they leave a defined area.

3. **Fleet management**: BLE beacons in vehicles detected by fixed ESP32 scanners at facility entrances/exits.

### Privacy Risks to Be Aware Of

- **MAC address tracking**: Static BLE MAC addresses allow passive tracking of individuals carrying BLE devices. Modern devices use MAC randomization, but implementation varies.
- **Fingerprinting**: Even with MAC randomization, BLE devices can be fingerprinted by their advertising payload patterns, timing characteristics, and PHY-layer RF signatures.
- **Retail tracking**: Some retailers use BLE beacons and scanners to track customer movement through stores.
- **Government surveillance**: Passive BLE scanning infrastructure could theoretically track populations. China has deployed Bluetooth-based tracking in some contexts.

---

## 7. Legal Considerations

### United States

**Federal level**:

- **FCC Part 15**: All BLE devices must comply. Wi-Fi deauthentication attacks (as available on BLEShark Nano) are illegal under FCC rules -- they constitute intentional interference with authorized radio communications.
- **Computer Fraud and Abuse Act (CFAA)**: Unauthorized access to or interference with computer systems (including BLE-connected devices) can be a federal crime.
- **Wiretap Act (18 U.S.C. 2511)**: Intercepting electronic communications without consent may violate federal wiretap laws. BLE advertising packets are generally considered "public" broadcasts, but capturing connected/encrypted sessions is a gray area.
- **No specific federal BLE tracking law**: As of 2025-2026, there is no comprehensive federal law specifically addressing BLE tracker misuse, though several bills have been proposed.

**State level**:

- Multiple states (including California, Illinois, Texas, New York) have enacted or proposed laws specifically criminalizing the use of tracking devices (including AirTags) for stalking.
- California's CCPA/CPRA and similar state privacy laws may apply to commercial BLE tracking of consumers.
- Some states classify placing a tracker on someone's vehicle without consent as a criminal offense (not just a civil one).

### Passive Scanning (Receiving Advertising Packets)

Passively receiving BLE advertising packets that are broadcast publicly is generally considered legal in the United States. These are unencrypted broadcasts on public radio frequencies. This is analogous to listening to unencrypted radio transmissions.

### Active Interference and Attacks

- **Wi-Fi Deauth**: Illegal under FCC rules. Penalties include fines up to $100,000+ and equipment seizure.
- **BLE Spam/Injection**: Legal gray area. Sending unsolicited BLE packets that cause notifications on victim devices could constitute harassment or unauthorized access depending on jurisdiction.
- **Jamming**: Intentional radio frequency jamming is a federal crime.

### Authorized Penetration Testing

- Must have explicit written authorization from the device/network owner
- Scope must be clearly defined
- Standard industry frameworks (PTES, OWASP) should be followed
- Bug bounty programs provide legal safe harbor for some types of testing

### International Considerations

- **EU GDPR**: BLE MAC addresses are considered personal data. Tracking individuals via BLE without consent or legal basis violates GDPR.
- **UK**: Similar to GDPR post-Brexit via UK GDPR and Data Protection Act 2018.
- **Canada**: PIPEDA governs commercial BLE tracking.

### Best Practices for Legal Compliance

1. Only scan/capture BLE traffic on networks and devices you own or have explicit authorization to test
2. Never use deauth, jamming, or injection capabilities without written authorization
3. Do not track individuals without their knowledge and consent
4. Treat captured BLE data (especially MAC addresses) as potentially personal data
5. Follow responsible disclosure if you discover vulnerabilities
6. Check local and state laws -- they vary significantly

---

## 8. Summary: Method Comparison

| Criterion | ESP32 DIY | BLEShark Nano | nRF Sniffer | ESPresense/Bermuda |
|-----------|-----------|---------------|-------------|-------------------|
| Cost | $3-15 | $40 | $10-45 | $25-200 |
| Skill level | Intermediate | Beginner | Advanced | Intermediate |
| Best for | Custom scanning, MQTT integration | Portable security testing | Deep packet analysis | Home automation presence |
| Packet depth | Advertising data only | Advertising data only | Full protocol stack | Advertising RSSI only |
| Portability | Medium (needs power bank) | High (built-in battery) | Low (needs laptop) | Fixed installation |
| Tracker detection | Yes (with code) | Yes (built-in) | Yes (with filters) | Yes (as side benefit) |
| Home Assistant | Via MQTT or ESPHome | No | No | Native integration |
| Legal risk | Low (passive scanning) | Medium (includes attack tools) | Low (passive capture) | Low (passive scanning) |

---

## 9. Sources

- [ESP32 BLE Beacon Scanner Explained (2026)](https://esp32.co.uk/esp32-ble-beacon-scanner-explained-2026/)
- [ESP32-Powered Presence Sensor Using Bluetooth](https://www.xda-developers.com/built-esp32-powered-presence-sensor-bluetooth/)
- [Turn ESP32 Into a BLE Beacon Scanner for Presence Detection](https://omarghader.github.io/esp32-ble-beacon-scanner-presence-detection-home-assistant/)
- [BLE-Based Proximity Control Using ESP32](https://circuitdigest.com/microcontroller-projects/ble-based-proximity-control-using-esp32)
- [BLE Asset Tracking with ESP32: A Complete Guide](https://medium.com/engineering-iot/ble-asset-tracking-with-esp32-a-comprehensive-guide-2a3f439b45c4)
- [BLEShark Nano: ESP32-Based Multi-tool (Hackaday)](https://hackaday.io/project/199277-bleshark-nano-esp32-based-multi-tool-for-hackers)
- [BLEShark Nano Product Page (InfiShark)](https://infishark.com/products/bleshark-nano)
- [BLEShark Nano (Hackster.io)](https://www.hackster.io/news/infishark-s-bleshark-nano-is-a-pocket-friendly-espressif-esp32-powered-bluetooth-and-wi-fi-tool-ba6e4d5b8d79)
- [BLEShark GitHub](https://github.com/grdashark/BLEShark)
- [nRF Sniffer for Bluetooth LE: Complete Technical Guide](https://novelbits.io/bluetooth-sniffer-series-part-2/)
- [Setting up nRF Sniffer (Nordic Developer Academy)](https://academy.nordicsemi.com/courses/bluetooth-low-energy-fundamentals/lessons/lesson-6-bluetooth-le-sniffer/topic/nrf-sniffer-for-bluetooth-le/)
- [nRF Sniffer Product Page (Nordic Semiconductor)](https://www.nordicsemi.com/Products/Development-tools/nRF-Sniffer-for-Bluetooth-LE)
- [Master BLE Sniffing: nRF52840 USB Dongle & Wireshark](https://novelbits.io/nordic-ble-sniffer-guide-using-nrf52840-wireshark/)
- [BLE Sniffer with nRF52840 (Adafruit)](https://learn.adafruit.com/ble-sniffer-with-nrf52840/working-with-wireshark)
- [BLE Tracker Stalking: Real Cases (InfiShark)](https://infishark.com/blogs/learn/ble-tracker-stalking-real-cases-and-the-response)
- [AirTag Tracking Detection (AllAboutCookies)](https://allaboutcookies.org/is-airtag-tracking-you)
- [Apple and Google DULT Anti-Tracking (The Hacker News)](https://thehackernews.com/2024/05/apple-and-google-launch-cross-platform.html)
- [Apple and Google 2025 Tracking Protection Landscape](https://wysleap.com/blog/apple-google-2025-tracking-protections)
- [DULT Standard (Talk Android)](https://www.talkandroid.com/466690-apple-google-dult/)
- [ESPresense Quick Start](https://espresense.com/quick-start/)
- [Room-Level Presence with BLE Beacons in Home Assistant](https://esp32.co.uk/room-level-presence-with-ble-beacons-in-home-assistant-esp32-bluetooth-proxy-guide/)
- [ESPresense with Home Assistant (Newerest Space)](https://newerest.space/mastering-espresence-room-presence-home-assistant/)
- [ESPHome + Bermuda BLE (Derek Seaman)](https://www.derekseaman.com/2025/12/home-assistant-track-whos-in-each-room-with-esphome-bermuda-ble.html)
- [Bermuda BLE Trilateration (Home Automation Guy)](https://www.homeautomationguy.io/blog/room-location-detection-with-bermuda-and-home-assistant-8f94b)
- [Replacing ESPresense with Bermuda (Zorruno)](https://zorruno.com/2024/replacing-espresense-with-bermuda-for-ble-tracking/)
- [Bermuda GitHub](https://github.com/agittins/bermuda)
- [BLE Advertising Primer (Argenox)](https://argenox.com/library/bluetooth-low-energy/ble-advertising-primer/)
- [How BLE Advertisements Work (NovelBits)](https://novelbits.io/bluetooth-low-energy-advertisements-part-1/)
- [BLE Advertising and Connections Explained (Tinkimo)](https://tinkimo.com/ble-advertising-and-connections-explained/)
- [ESP32 BLE on Arduino IDE (Random Nerd Tutorials)](https://randomnerdtutorials.com/esp32-bluetooth-low-energy-ble-arduino-ide/)
- [ESPHome BLE Presence Sensor](https://esphome.io/components/binary_sensor/ble_presence/)
- [ESPHome BLE RSSI Sensor](https://esphome.io/components/sensor/ble_rssi/)
- [BLE Security & Privacy 2025 Guide (Argenox)](https://argenox.com/blog/bluetooth-low-energy-ble-security-privacy-a-2025-guide/)
- [EFF: Standards for Bluetooth-Enabled Trackers](https://www.eff.org/deeplinks/2023/08/industry-discussion-about-standards-bluetooth-enabled-physical-trackers-finally)
- [AirTagTag ESP32 AirTag Detector (GitHub)](https://github.com/7ENSOR/AirTagTag)
- [CYD ESP32 AirTag Scanner (GitHub)](https://github.com/hevnsnt/CYD_ESP32-AirTag-Scanner)
- [AirFlag AirTag Detector (GitHub)](https://github.com/bennettjustin/AirFlag)
- [BLE-Scanner MQTT (GitHub)](https://github.com/gromeck/BLE-Scanner)

---

## 10. Best-Fit Hardware from Your Inventory

### Recommended Build

| Component | Assignment | Why |
|-----------|-----------|-----|
| **Board** | Lonely Binary ESP32 Gold Edition #3 | IPEX antenna connector extends BLE reception range. BLE operates on 2.4GHz alongside WiFi, so the same external antenna improves BLE scanning. Ideal for detecting hidden BLE devices (ATM skimmers, rogue beacons) |
| **Display** | AITRIP 4.0" ESP32 Touchscreen (ST7796, 320x480) | Larger screen provides more room for BLE device lists with MAC addresses, RSSI, device names, manufacturer data. Leaves both CYD screens for Marauder and Flock |
| **Antenna** | Bingfu WiFi/BT Antenna #2 (2.4/5.8GHz, RP-SMA) via Boobrie adapter + U.FL pigtail | Specifically rated for Bluetooth frequencies. Better gain than DIYmall for BLE scanning |
| **Storage** | KOOTION 16GB Micro SD Card | BLE scan data is small (MAC + RSSI + name per device). 16GB is plenty |
| **Prototyping** | AEDIKO ESP32 GPIO Breakout Board #3 | For adding status LEDs or buzzer for alert-on-detection mode |

### External Antenna for BLE Range

BLE and WiFi share the same 2.4GHz antenna on ESP32. Tests show **+10dB average improvement** with external antenna vs PCB trace antenna, extending reliable BLE detection to 15+ meters with 70% improved signal stability.

**Connection:** Same as Marauder antenna chain -- Lonely Binary IPEX socket -> U.FL pigtail -> Boobrie adapter -> Bingfu RP-SMA antenna.

### Pinout Reference (ESP32-WROOM-32 / Lonely Binary Gold)

| Function | GPIO | Notes |
|----------|------|-------|
| SPI MOSI | GPIO 23 | For external display |
| SPI MISO | GPIO 19 | |
| SPI SCK | GPIO 18 | |
| SPI CS | GPIO 5 | |
| I2C SDA | GPIO 21 | For sensors |
| I2C SCL | GPIO 22 | |
| UART TX | GPIO 1 | Serial output |
| UART RX | GPIO 3 | Serial input |
| ADC (signal strength) | GPIO 34-39 | Input-only pins, no pullup |
| Buzzer/LED | GPIO 2, 4, 15 | Output for alerts |

**Full pinout:** [RandomNerdTutorials ESP32 Pinout](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)

### Upgrade Recommendations

| Component | Upgrade To | Price | Improvement |
|-----------|-----------|-------|-------------|
| Board | Lonely Binary ESP32-S3 IPEX | ~$15 | BLE 5.0 support (extended range, coded PHY), 16MB flash, 8MB PSRAM |
| Antenna | 5dBi 2.4GHz RP-SMA omni | ~$8-12 | Better BLE detection range without losing 360-degree coverage |
| Add-on | Passive buzzer module | ~$3-5 | Audible alert when suspicious BLE device detected (skimmer, rogue tracker) |
