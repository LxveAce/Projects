# Comprehensive Guide: Flock Camera Detection & Drone Detection

A complete technical reference covering DIY detection of Flock Safety ALPR surveillance cameras and drone detection using ESP32-based hardware, SDR, and acoustic methods.

---

## Table of Contents

- [Part 1 -- Flock Safety Camera Detection](#part-1----flock-safety-camera-detection)
  - [1.1 What Are Flock Safety Cameras?](#11-what-are-flock-safety-cameras)
  - [1.2 The Flock-You Project](#12-the-flock-you-project)
  - [1.3 Detection Methods (Three-Layer System)](#13-detection-methods-three-layer-system)
  - [1.4 The 31 Known Flock OUI Prefixes](#14-the-31-known-flock-oui-prefixes)
  - [1.5 Hardware Options](#15-hardware-options-cheapest-to-most-capable)
  - [1.6 Complete Build Guide (XIAO ESP32-S3)](#16-complete-build-guide-xiao-esp32-s3)
  - [1.7 Configuration Parameters](#17-configuration-parameters-maincpp)
  - [1.8 Alert Patterns](#18-alert-patterns)
  - [1.9 Data Storage and Architecture](#19-data-storage-and-architecture)
  - [1.10 Operating Modes](#110-operating-modes)
  - [1.11 Performance and Accuracy](#111-performance-and-accuracy)
  - [1.12 Related Projects and Community](#112-related-projects-and-community)
  - [1.13 Legal Analysis -- Flock Detection](#113-legal-analysis----flock-detection)
- [Part 2 -- Drone Detection](#part-2----drone-detection)
  - [2.1 Overview of Detection Methods](#21-how-drone-detection-works----overview-of-methods)
  - [2.2 FAA Remote ID Background](#22-faa-remote-id----background)
  - [2.3 Drone Mesh Mapper (Remote ID Detection)](#23-project-1-drone-mesh-mapper-remote-id-detection)
  - [2.4 Batear (Acoustic Drone Detection)](#24-project-2-batear-acoustic-drone-detection)
  - [2.5 RF Signal Analysis with SDR](#25-project-3-rf-signal-analysis-with-sdr)
  - [2.6 nRF24L01+ Multi-Antenna Detection](#26-project-4-nrf24l01-multi-antenna-detection)
  - [2.7 Recommended Drone Detection Build](#27-recommended-drone-detection-build-best-value)
  - [2.8 Legal Analysis -- Drone Detection](#28-legal-analysis----drone-detection)
  - [2.9 Comparison Table](#29-comparison-flock-detection-vs-drone-detection)
- [Sources](#sources)

---

## Part 1 -- Flock Safety Camera Detection

---

### 1.1 What Are Flock Safety Cameras?

Flock Safety is the largest vendor of Automated License Plate Reader (ALPR) systems in the United States. As of mid-2025, the company had deployed nearly 90,000 cameras across approximately 7,000 law enforcement networks nationwide.

**How they work:**

- Solar-powered, LTE-connected cameras install on poles in public areas (roads, intersections, neighborhood entrances)
- Run continuously, capturing every vehicle that enters the frame
- Onboard ALPR software reads license plate characters and tags each record with timestamp and GPS coordinates
- The system also tags vehicle color, body type, and visible features (roof racks, trailers, body damage)
- Data is uploaded to Flock's cloud, where law enforcement agencies can search and cross-reference across the entire national network
- Alerts fire automatically when a plate matches a stolen vehicle, wanted person, or AMBER alert

**What they do NOT do (per Flock's claims):** No video recording, no speed enforcement, no facial recognition, no personal identity data -- only plate, make, model, color, and vehicle features.

**Privacy concerns:** The [EFF](https://www.eff.org/deeplinks/2025/12/effs-investigations-expose-flock-safetys-surveillance-abuses-2025-review) and [ACLU](https://data.aclum.org/2025/10/07/flock-gives-law-enforcement-all-over-the-country-access-to-your-location/) have documented that Flock's system constitutes a nationwide mass-surveillance network. A Norfolk, Virginia court ruled in 2024 that collecting location data from Flock ALPRs is a Fourth Amendment search requiring a warrant. Flock also announced plans in 2025 to add "human distress" audio detection microphones, raising wiretap law questions.

**Physical appearance:** Flock cameras are small, solar-powered units mounted on utility poles. They often have a distinctive solar panel on top and a downward-facing camera housing.

---

### 1.2 The Flock-You Project

| | |
|---|---|
| **Repository** | [github.com/colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you) |
| **Documentation** | [virtuallyscott.github.io/flock-you](https://virtuallyscott.github.io/flock-you/) |
| **Stars** | 1,100+ |
| **Forks** | 145 |
| **Commits** | 57 |

Flock-You is open-source ESP32-S3 firmware that passively detects Flock Safety ALPR cameras (and other surveillance devices including Raven gunshot detectors, Penguin, and Pigvision systems) by monitoring their wireless emissions. The device is receive-only -- it never transmits or interferes with any system.

**How detection works:** Flock cameras use ESP32-based modules internally and constantly emit WiFi management frames (probe requests, beacons) and data frames. Each frame contains MAC addresses. The first 3 bytes of any MAC address form the OUI (Organizationally Unique Identifier), which identifies the hardware manufacturer. Flock-You maintains a curated list of 31 OUIs associated with Flock Safety deployments and listens for frames matching those signatures.

---

### 1.3 Detection Methods (Three-Layer System)

**Method 1 -- Wildcard Probe Signature (by DeFlockJoplin)**

Identifies 802.11 management frames where type=0, subtype=4 (Probe Request), the SSID Information Element has length 0 (wildcard/empty), and the transmitter MAC matches the known OUI list. This is the highest-confidence method. Field-tested in Joplin, MO: detected 11 of 12 known cameras with only 2 false positives.

**Method 2 -- Transmitter OUI Matching**

Checks the source MAC address (addr2) of every captured frame against the 31-OUI database. Generates `wifi_oui_addr2` detection events.

**Method 3 -- Receiver-Side Detection (by NitekryDPaul)**

Monitors the destination MAC address (addr1) in data frames, catching sleeping/idle cameras that appear as destinations without actively transmitting. Includes multicast filtering and randomized-MAC rejection to prevent false positives.

**Additional methods in full firmware:**

- BLE advertisement scanning
- SSID keyword matching ("flock")
- BLE device name matching
- BLE service UUID identification (for Raven gunshot detectors)

---

### 1.4 The 31 Known Flock OUI Prefixes

```
70:c9:4e   3c:91:80   d8:f3:bc   80:30:49   b8:35:32
14:5a:fc   74:4c:a1   08:3a:88   9c:2f:9d   c0:35:32
94:08:53   e4:aa:ea   f4:6a:dd   f8:a2:d6   24:b2:b9
00:f4:8d   d0:39:57   e8:d0:fc   e0:4f:43   b8:1e:a4
70:08:94   58:8e:81   ec:1b:bd   3c:71:bf   58:00:e3
90:35:ea   5c:93:a2   64:6e:69   48:27:ea   a4:cf:12
82:6b:f2
```

These are primarily Espressif (ESP32) OUIs. This means false positives can occur near ESP32 development boards, smart home devices, and other ESP32-based products.

---

### 1.5 Hardware Options (Cheapest to Most Capable)

#### Option A: DIY ESP32 Build ($5-12)

- **Board:** Any ESP32-WROOM or ESP32-S3 dev board
- **Buzzer:** KY-006 passive buzzer (optional)
- **Wiring:** Buzzer positive to GPIO 25, negative to GND; LED on GPIO 2 (often onboard)
- **Power:** USB cable
- **Assembly time:** 10-15 minutes, solderless breadboard

#### Option B: Seeed XIAO ESP32-S3 (~$8-13) -- RECOMMENDED

- **Board:** Seeed Studio XIAO ESP32-S3
- **Buzzer:** Piezo on GPIO 3
- **LED:** Onboard on GPIO 21 (active low)
- **Serial mirror:** GPIO 43 at 115200 baud
- **Power:** USB-C
- This is the primary target board for the flock-you firmware

#### Option C: M5 Atom Lite Pre-Flashed ($39.99)

- ESP32-PICO-D4 processor
- 5x5 RGB LED matrix
- USB-C powered
- Arrives pre-flashed, no setup needed
- Available from STS Collective (stscollective.com)

#### Option D: OUI-SPY Multi-Mode Board ($85)

- ESP32-S3 dual-core
- Switchable antenna (onboard ceramic OR external MMCX)
- Integrated PWM buzzer
- Four selectable firmware modes: Detector, Foxhunter, Flock-You, Sky Spy
- Mode selection via WiFi AP at 192.168.4.1
- Available from colonelpanic.tech

---

### 1.6 Complete Build Guide (XIAO ESP32-S3)

#### Step 1: Install PlatformIO

```bash
pip install platformio
```

Or install the PlatformIO extension in VS Code.

#### Step 2: Clone the Repository

```bash
git clone https://github.com/colonelpanichacks/flock-you.git
cd flock-you
git checkout promiscious-dev
```

The `promiscious-dev` branch contains the latest WiFi promiscuous mode firmware.

#### Step 3: Wire the Hardware

| Component | GPIO Pin | Function |
|-----------|----------|----------|
| Piezo buzzer (+) | GPIO 3 | Audio alert |
| Piezo buzzer (-) | GND | Ground |
| Onboard LED | GPIO 21 | Visual alert (active low, built-in) |
| Serial TX mirror | GPIO 43 | 115200 baud output (optional) |

For a minimal build, you only need the XIAO ESP32-S3 board itself -- the onboard LED provides visual feedback without any additional wiring.

#### Step 4: Compile and Flash

```bash
pio run                  # Compile
pio run -t upload        # Flash to device via USB
pio device monitor       # Open serial monitor
```

The firmware uses a custom partition table (`partitions.csv`) with 1.9 MB SPIFFS and 6 MB app partition. No external Arduino libraries needed beyond the ESP32 core.

#### Step 5: Verify Boot

On power-up, you should hear a Super Mario World 1-2 startup tune from the buzzer (confirms buzzer is working). The device immediately begins scanning.

#### Step 6 (Optional): Set Up Flask Dashboard

```bash
cd api
pip install -r requirements.txt
python flockyou.py
```

Access at `http://localhost:5000`. Provides real-time map visualization, detection logging, and data export (JSON, CSV, KML).

#### Step 7 (Optional): GPS Wardriving

- Connect a USB NMEA GPS puck to the host computer
- The Flask dashboard temporally correlates detections with GPS coordinates
- Alternatively, use browser geolocation on a mobile device running the Flask UI
- Export results as KML for Google Earth mapping

---

### 1.7 Configuration Parameters (main.cpp)

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `CHANNEL_MODE` | `CHANNEL_MODE_CUSTOM` | CUSTOM (1/6/11), FULL_HOP (1-11), or SINGLE |
| `CHANNEL_DWELL_MS` | 350 ms | Time spent on each channel before hopping |
| `RSSI_MIN` | -95 dBm | Minimum signal strength threshold |
| `ALERT_COOLDOWN_MS` | 5000 ms | Rate limit per-MAC alert emission |
| `CHECK_ADDR1` | 1 | Enable receiver-side detection |
| `CHECK_ADDR3` | 0 | BSSID fallback detection |
| `ENABLE_SSID_MATCH` | 0 | Keyword matching in SSIDs |
| `PROCESS_MGMT_FRAMES` | 1 | Analyze management frames |
| `PROCESS_DATA_FRAMES` | 1 | Analyze data frames |
| `MAX_DETECTIONS` | 200 | On-device detection table size |
| `AUTOSAVE_INTERVAL_MS` | 60000 ms | SPIFFS save interval |

---

### 1.8 Alert Patterns

| Event | Audio | Visual |
|-------|-------|--------|
| Boot | Super Mario 1-2 tune | LED flash |
| New detection | Two ascending beeps (2000 to 2800 Hz) | LED flash |
| Heartbeat (device still in range) | Bimodal beeps every 10 seconds | Periodic LED |
| Standalone boot (no USB) | Mario tune confirms operation | LED active |

---

### 1.9 Data Storage and Architecture

**Firmware architecture** uses a split design:

- **WiFi callback (IRAM, time-critical):** Runs in WiFi task context, performs fast OUI matching only, writes to a lock-free 32-entry ring buffer. No Serial calls or memory allocation here.
- **Main loop (application context):** Drains the alert queue, maintains detection table, manages SPIFFS persistence, emits JSON over USB CDC, triggers audio/LED.

**SPIFFS storage format:**

```json
Header: {"v":1,"count":N,"bytes":B,"crc":"0xXXXXXXXX"}
Payload: [{"mac":"...","method":"...","rssi":...,...},...]
```

CRC32 validation on boot with automatic recovery from temp file on corruption.

**JSON output over serial:**

```json
{
  "event": "detection",
  "detection_method": "wifi_oui_addr2",
  "protocol": "wifi_2_4ghz",
  "mac_address": "aa:bb:cc:dd:ee:ff",
  "oui": "aa:bb:cc",
  "device_name": "",
  "rssi": -62,
  "channel": 6,
  "frequency": 2437,
  "ssid": ""
}
```

---

### 1.10 Operating Modes

**Standalone (no USB connection):**

- Device boots, plays Mario tune, begins scanning
- Detections stored to SPIFFS
- LED flashes on each detection
- Previous session recoverable from `/prev_session.json`

**Connected (USB + Flask dashboard):**

- All standalone functionality continues
- Live JSON streaming to web dashboard
- GPS correlation if configured
- Real-time deduplication, mapping, and export
- Both modes run simultaneously

**BLE variant (main branch):**

- Detects Flock cameras via BLE advertisements
- Runs onboard WiFi AP
- Serves phone-facing dashboard at `192.168.4.1`

---

### 1.11 Performance and Accuracy

| Metric | Value |
|--------|-------|
| True positive rate | ~95% for confirmed Flock cameras in range |
| False positive rate | ~5-10% depending on environment |
| Detection range | 50-300 feet depending on obstacles and antenna |
| Common false positives | ESP32 dev boards, smart home devices, other surveillance cameras |

---

### 1.12 Related Projects and Community

- **[Trap Shooter](https://gainsec.com/2025/06/30/trap-shooter-tiny-flock-safety-sniffer-alarm/):** Alternative Flock sniffer firmware for the M5NanoC6 (ESP32-C6). Detects probe requests and SSIDs containing "flock." Extremely compact dongle form factor. Discovered that Flock devices use default hotspot passwords of "security."
- **[ESP32 Marauder - Flock Sniff](https://github.com/justcallmekoko/ESP32Marauder/wiki/Flock-Sniff):** Flock detection mode built into the popular ESP32 Marauder multi-tool firmware.
- **[flock-you-wifi-recon](https://github.com/0xXyc/flock-you-wifi-recon):** Fork focusing specifically on WiFi probe-based detection.
- **[Flock-You CYD](https://github.com/JarvisLatteier/Flock-You-CYD-2432S028R):** Port for the CYD-2432S028R (Cheap Yellow Display) boards with built-in screen.
- **[deflock.me](https://deflock.me):** Crowdsourced global map of ALPR camera locations.

**Vendor support:**

- Colonel Panic Tech: colonelpanic.tech (OUI-SPY, GPS modules, accessories)
- STS Collective: stscollective.com (M5 Atom Lite pre-flashed)
- M5Stack Official: shop.m5stack.com (bare hardware)

**Community platforms:**

- Reddit: r/privacy, r/privacytoolsIO
- Discord: Colonel Panic Tech server
- GitHub Issues: Technical support

---

### 1.13 Legal Analysis -- Flock Detection

**Why passive WiFi monitoring is legal in the US:**

- The device only receives publicly broadcast 802.11 frames -- it never transmits, connects, decrypts, or interferes
- Under the Electronic Communications Privacy Act (18 U.S.C. 2511), interception of unencrypted radio communications that are readily accessible to the general public is generally not prohibited
- Analogous to receiving any broadcast radio signal
- No court has held that passive reception of WiFi management frames constitutes wiretapping

**What is illegal:**

- Active jamming or interference with cameras (FCC violation, federal crime)
- Hacking into or accessing camera systems (CFAA violation)
- Physically destroying or tampering with cameras (vandalism, destruction of property)
- Some jurisdictions have stricter local wireless monitoring laws -- always check local regulations

**Ethical guidelines:**

- Use for personal surveillance awareness and privacy advocacy
- Contribute findings to community mapping (deflock.me)
- Do not trespass to confirm camera locations
- Do not use to facilitate illegal activity
- Be aware that GPS logs of your own movements could be subpoenaed

---

### 1.14 Troubleshooting

**No Detections Despite Known Camera:**

- Verify camera is powered and operational
- Move closer (expand detection range)
- Reorient antenna
- Update firmware to latest version
- Confirm device is actively scanning

**Excessive False Positives:**

- Reduce sensitivity settings
- Enable wildcard probe detection for higher confidence
- Physically verify detections
- Filter by signal strength
- Update OUI database

**Battery Drain:**

- Enable passive scan mode (intermittent vs. continuous)
- Set display timeout
- Disable GPS when mapping unnecessary
- Replace degraded Li-Po batteries

**GPS Lock Issues:**

- Move to position with clear sky visibility
- Ensure antenna properly connected (SMA)
- Expect 5-15 minutes for initial lock
- Move away from RF interference
- Verify GPS is enabled in settings

**RSSI Reference Values:**

| RSSI | Meaning |
|------|---------|
| -30 dBm | Extremely close |
| -50 dBm | Strong signal |
| -70 dBm | Weak but usable |
| -90 dBm | Edge of range |

---

## Part 2 -- Drone Detection

---

### 2.1 How Drone Detection Works -- Overview of Methods

There are four primary approaches to DIY drone detection, each with different hardware, cost, and capability profiles:

| Method | Hardware | Cost | Range | Detects |
|--------|----------|------|-------|---------|
| **Remote ID Reception** | ESP32-S3/C3 | $8-100 | 5-15 km | FAA-compliant drones broadcasting ID |
| **Acoustic Detection** | ESP32-S3 + MEMS mic | ~$15 | Short (50-200m) | Any drone with audible rotors |
| **RF Signal Analysis** | RTL-SDR + antenna | $30-300 | 1-10 km | Drones using specific RF protocols |
| **Multi-sensor nRF24** | ESP32 + nRF24L01+ modules | $30-60 | 100-500m | 2.4 GHz signal anomalies |

---

### 2.2 FAA Remote ID -- Background

As of March 2024, the FAA requires all drones operating in US airspace to broadcast Remote ID (14 CFR Part 89). This is effectively a "digital license plate" for drones.

**What Remote ID broadcasts:**

- Drone serial number or session ID
- Latitude, longitude, altitude of the drone
- Velocity and heading
- Latitude/longitude of the pilot (control station or takeoff location)
- Timestamp

**Broadcast methods:**

- WiFi (beacon frames, NAN -- Neighbor Awareness Networking)
- Bluetooth 4.0 Legacy and Bluetooth 5.0 Long Range

**Key fact for detection:** Remote ID broadcasts are unencrypted and can be received by anyone within range using compatible hardware or smartphone apps ([OpenDroneID](https://github.com/opendroneid/opendroneid-core-c), DroneScout). Receiving these broadcasts is completely legal -- the entire purpose of the system is public identification.

**Enforcement status:** As of 2025-2026, the FAA has transitioned to active enforcement. Local law enforcement can use Remote ID detection apps to identify non-compliant operators and report them to the FAA.

---

### 2.3 Project 1: Drone Mesh Mapper (Remote ID Detection)

| | |
|---|---|
| **Repository** | [github.com/colonelpanichacks/drone-mesh-mapper](https://github.com/colonelpanichacks/drone-mesh-mapper) |
| **Hackster.io** | [Mesh Mapper project page](https://www.hackster.io/colonelpanic/mesh-mapper-drone-remote-id-mapping-and-mesh-alerts-8e7c61) |
| **Creator** | Colonel Panic (same creator as Flock-You) |

This is the most capable open-source drone detection system available. It captures FAA Remote ID broadcasts over both WiFi and Bluetooth simultaneously using the ESP32-S3's dual-core architecture.

#### Hardware Options

**Option A: DIY Build ($8-25)**

- Seeed XIAO ESP32-S3 (~$8-13)
- USB-C cable
- Optional: upgraded 2.4 GHz antenna for extended range

**Option B: Mesh Build ($25-50)**

- XIAO ESP32-S3 (detector)
- Heltec LoRa 32 V3 (Meshtastic mesh radio)
- Wiring between the two boards (see below)

**Option C: Pre-built Kit ($100)**

- MeshDetect breakout board from Tindie ($15 board only, $100 assembled)
- Integrates XIAO ESP32-C3/S3 with Heltec LoRa module
- Pre-flashed and tested

#### Mesh Wiring (ESP32 to Meshtastic LoRa)

```
ESP32 Pin    Mesh Radio Pin    Function
TX1 (D4)  -> RX 19             Serial data
RX1 (D5)  -> TX 20             Serial data
3.3V      -> VCC               Power
GND       -> GND               Ground
```

#### Dual-Core Detection Architecture

- **Core 0:** WiFi promiscuous mode -- captures Remote ID data in beacon frames and NAN transmissions on channel 6
- **Core 1:** BLE scanning -- captures Remote ID in Bluetooth LE advertisements (BT 4.0 and 5.0)
- Both cores feed detected data into a unified JSON stream over USB serial at 115200 baud

#### Installation and Setup

**Flash firmware:**

```bash
git clone https://github.com/colonelpanichacks/drone-mesh-mapper.git
cd drone-mesh-mapper
# Open in PlatformIO, select remoteid_mesh_dualcore environment
pio run -t upload
```

**Start Flask dashboard:**

```bash
pip3 install Flask Flask-SocketIO pyserial requests urllib3
python3 mesh-mapper.py
```

Access at `http://localhost:5000`

**Raspberry Pi automated install:**

```bash
wget https://raw.githubusercontent.com/colonelpanichacks/drone-mesh-mapper/main/RPI/install_rpi.py
python3 install_rpi.py --branch main
```

#### Dashboard Features

- Real-time Google Maps-style interface with drone and pilot position markers
- Color-coded flight paths by device MAC
- Signal strength indicators
- FAA database integration (aircraft registration lookup with API caching)
- Multi-device support (up to 3 ESP32s simultaneously)
- Export: CSV, KML (Google Earth), GeoJSON, cumulative history
- Webhook support for external alerting systems
- Headless mode for dedicated server deployments

#### Command-Line Options

```
--headless          Run without web interface
--debug             Enable debug logging
--web-port PORT     Custom port (default: 5000)
--port-interval N   Monitor interval in seconds (default: 10)
--no-auto-start     Disable automatic port connection
```

#### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/detections` | GET | Current active drone detections |
| `/api/detections_history` | GET | Historical data (GeoJSON) |
| `/api/paths` | GET | Flight path visualization data |
| `/api/set_alias` | POST | Assign friendly device names |
| `/api/ports` | GET | Available serial ports |
| `/api/serial_status` | GET | ESP32 connection health |
| `/api/faa/<identifier>` | GET | FAA registration lookup |
| `/api/set_webhook_url` | POST | Configure webhook callbacks |
| `/download/csv` | GET | CSV export |
| `/download/kml` | GET | KML export |
| `/download/cumulative_detections.csv` | GET | Cumulative history export |

#### Performance

| Metric | Value |
|--------|-------|
| Detection range (urban) | 5 km |
| Detection range (open, good antenna) | 10-15 km |
| Detection latency | < 500 ms |
| Concurrent drones tracked | 50+ |
| Memory usage | < 100 MB |
| Storage per detection | ~1 KB |
| Throughput | 1,000+ detections/min |

#### Meshtastic Mesh Networking

Multiple ESP32 detection nodes can be deployed across a property or neighborhood. Each node shares detections over LoRa mesh (915 MHz in the US), creating overlapping coverage with no internet required between nodes. Alerts propagate through the mesh so a detection at one node triggers notifications at all nodes.

---

### 2.4 Project 2: Batear (Acoustic Drone Detection)

| | |
|---|---|
| **Repository** | [github.com/TN666/batear](https://github.com/TN666/batear) |
| **Website** | batear.io |
| **Stars** | 238 |
| **Version** | v2.2.0 |
| **License** | MIT, fiscally hosted as 501(c)(3) non-profit via Open Source Collective |

Batear takes a completely different approach -- it listens for the acoustic signature of drone rotors using MEMS microphones, inspired by WWII-era acoustic aircraft detection methods.

#### Hardware Components

**Wireless Deployment:**

| Component | Purpose |
|-----------|---------|
| Heltec WiFi LoRa 32 V3 or V4 | Detector/Gateway MCU |
| ICS-43434 MEMS microphone | High-precision acoustic sensor |
| SX1262 LoRa transceiver (915 MHz) | Encrypted mesh communication |
| SSD1306 OLED display | Gateway status display |

**Wired Deployment:**

| Component | Purpose |
|-----------|---------|
| LILYGO T-ETH-Lite S3 | Ethernet-connected detector |
| ICS-43434 MEMS microphone | Acoustic sensor |
| W5500 Ethernet controller | PoE/wired connectivity |

**Estimated cost:** ~$15 USD for a basic detector node

#### How It Works

1. The ICS-43434 MEMS microphone captures audio via I2S digital interface
2. An FFT harmonic detection algorithm (based on Goertzel filters) identifies frequency patterns characteristic of drone rotors
3. Different drones produce different rotor frequencies: small quadcopters spin at 4,000-6,000 RPM (67-100 Hz fundamental), larger craft lower
4. All processing runs locally on the ESP32 -- no cloud, no internet, no ongoing cost
5. On detection, the node transmits an AES-128-GCM encrypted 36-byte LoRa packet to the gateway
6. The gateway forwards alerts to Home Assistant via MQTT with automatic device discovery

#### Build and Flash

```bash
idf.py set-target esp32s3
idf.py build
idf.py flash monitor
```

Select build configuration via sdkconfig files: `sdkconfig.detector`, `sdkconfig.gateway`, `sdkconfig.wired_detector`

A browser-based web flasher (Chrome/Edge) is also available, eliminating the need for ESP-IDF toolchain installation.

#### Deployment Architecture

**Wireless mesh:** Multiple detector nodes transmit encrypted alerts via LoRa to a central gateway, which publishes to MQTT for Home Assistant automation (trigger lights, sirens, cameras, notifications).

**Wired/PoE:** Ethernet detectors publish directly to MQTT without a gateway -- suited for permanent installations with existing network infrastructure.

#### Tips for Better Detection

- Use a foam windscreen on the microphone to reduce wind-induced false positives
- Environmental calibration is recommended for each deployment location
- Multiple microphones can enable bearing triangulation (direction finding)
- Future plans include TensorFlow Lite / ESP32-NN machine learning models

---

### 2.5 Project 3: RF Signal Analysis with SDR

For detecting drones that are not Remote ID compliant (older models, modified/illegal drones, FPV racers), Software Defined Radio provides broader spectrum monitoring.

#### Hardware Options

| Device | Cost | Capability |
|--------|------|------------|
| RTL-SDR Blog V4 | ~$30 | 500 kHz - 1.7 GHz receive |
| Pluto SDR (Analog Devices) | $200-300 | Full duplex TX/RX, radar capable |
| AntSDR E200 | ~$300 | DJI DroneID protocol decoding |
| HackRF One | ~$300 | 1 MHz - 6 GHz receive/transmit |
| KerberosSDR (4-channel) | ~$150 | Direction finding / bearing |

#### Key Drone RF Frequencies

| Frequency | Usage |
|-----------|-------|
| 900 MHz | Long-range drone control/telemetry (Crossfire, ELRS 900) |
| 1.2 GHz | Analog video downlink (legacy FPV) |
| 2.4 GHz | WiFi control, FPV control (ELRS 2.4, DJI), Remote ID |
| 5.8 GHz | FPV video, DJI O3/O4 video |

#### Notable SDR Projects

- **GridDown:** Offline situational awareness platform using [RTL-SDR](https://www.rtl-sdr.com/tag/drone/) on Raspberry Pi 5 for ADS-B and Remote ID reception, plus 900 MHz control link detection
- **WarDragon:** Real-time drone tracking using Sniffle (BT sniffer) with SniffleToTAK for military-style TAK mapping
- **DJI DroneID Decoder:** AntSDR E200 firmware that decodes DJI's proprietary DroneID protocol, revealing drone and operator positions
- **KerberosSDR Tracking:** Four-channel coherent RTL-SDR array that determines drone bearing using radio direction-finding

---

### 2.6 Project 4: nRF24L01+ Multi-Antenna Detection

**Repository:** [github.com/RamiLup/HMI-Prototype-drone-detection-nRF24](https://github.com/RamiLup/HMI-Prototype-drone-detection-nRF24)

Uses three or more Nordic nRF24L01+ 2.4 GHz transceivers with directional (Yagi) and omnidirectional antennas connected to an ESP32. The system detects approaching drones by monitoring signal strength variations across antenna patterns. Includes an OLED display (I2C) and HMI interface.

---

### 2.7 Recommended Drone Detection Build (Best Value)

For a comprehensive setup covering most scenarios, combine Remote ID reception with acoustic detection:

**Tier 1 -- Remote ID Scanner ($13 total):**

1. Buy a Seeed XIAO ESP32-S3 (~$8-13)
2. Flash the drone-mesh-mapper firmware
3. Run the Flask dashboard on any computer
4. You now detect any FAA-compliant drone within 5-15 km

**Tier 2 -- Add Acoustic Detection ($15 more, ~$28 total):**

1. Buy a Heltec WiFi LoRa 32 V3 (~$12) and ICS-43434 mic (~$3)
2. Flash the Batear firmware
3. Integrate with Home Assistant via MQTT
4. You now also detect non-compliant drones by sound

**Tier 3 -- Add Mesh Networking ($15-50 more):**

1. Add a Heltec LoRa module to the Remote ID detector
2. Wire UART between ESP32-S3 and LoRa module
3. Deploy multiple nodes for full property coverage
4. All nodes share detections over LoRa mesh without internet

**Tier 4 -- Add SDR for full-spectrum awareness ($30+ more):**

1. Add an RTL-SDR Blog V4 dongle
2. Monitor 900 MHz / 2.4 GHz / 5.8 GHz drone control bands
3. Use with Raspberry Pi for continuous monitoring

---

### 2.8 Legal Analysis -- Drone Detection

**Receiving Remote ID broadcasts:**

Completely legal. The FAA designed Remote ID specifically to be received by the public. Unencrypted by design. Smartphone apps (OpenDroneID, DroneScout) are publicly available for this exact purpose. Law enforcement actively uses Remote ID receivers.

**Passive RF monitoring (SDR):**

Legal in the United States under the same principles as receiving any radio broadcast. The Communications Act of 1934 (47 U.S.C. 605) prohibits divulging intercepted communications to third parties, but passive reception for personal use is generally permitted. You cannot decrypt encrypted communications.

**Acoustic detection:**

No legal restrictions. Listening to sounds in the air is not regulated.

**What is illegal:**

- Jamming drone signals (federal crime under 47 U.S.C. 333, FCC enforcement)
- Shooting down drones (federal crime -- aircraft are protected under 18 U.S.C. 32)
- Spoofing GPS or Remote ID signals
- Using detection to facilitate interference with aircraft operations
- Only the federal government has authority to take counter-drone kinetic action (per the Preventing Emerging Threats Act)

**State and local variation:**

Some states have additional drone privacy laws. Detection and observation is universally legal, but what you do with that information may be subject to local regulations.

---

### 2.9 Comparison: Flock Detection vs. Drone Detection

| Aspect | Flock-You | Drone Mesh Mapper | Batear |
|--------|-----------|-------------------|--------|
| **Target** | ALPR surveillance cameras | FAA-compliant drones | Any drone (by sound) |
| **Method** | WiFi OUI matching | Remote ID (WiFi + BLE) | Acoustic FFT |
| **Primary board** | XIAO ESP32-S3 | XIAO ESP32-S3 | Heltec LoRa 32 V3 |
| **Cost** | $8-85 | $8-100 | ~$15 |
| **Range** | 50-300 ft | 5-15 km | 50-200 m |
| **Dashboard** | Flask (localhost:5000) | Flask (localhost:5000) | Home Assistant/MQTT |
| **Data export** | JSON, CSV, KML | CSV, KML, GeoJSON | MQTT events |
| **Mesh capable** | No (standalone) | Yes (Meshtastic LoRa) | Yes (LoRa) |
| **Legal** | Legal (passive receive) | Legal (public broadcast) | Legal (acoustic) |
| **Creator** | Colonel Panic | Colonel Panic | TN666 |
| **False positive risk** | Medium (other ESP32 devices) | Very low (Remote ID specific) | Medium (environmental noise) |

---

## Sources

- [colonelpanichacks/flock-you (GitHub)](https://github.com/colonelpanichacks/flock-you)
- [Flock You Documentation](https://virtuallyscott.github.io/flock-you/)
- [Flock-You Detection Project Guide (SimeonOnSecurity)](https://simeononsecurity.com/articles/flock-you-detection-project-counter-surveillance-hardware-guide-2026/)
- [Detecting Surveillance Cameras With The ESP32 (Hackaday)](https://hackaday.com/2025/09/26/detecting-surveillance-cameras-with-the-esp32/)
- [Trap Shooter - Flock Safety Sniffer (GainSec)](https://gainsec.com/2025/06/30/trap-shooter-tiny-flock-safety-sniffer-alarm/)
- [ESP32 Marauder Flock Sniff](https://github.com/justcallmekoko/ESP32Marauder/wiki/Flock-Sniff)
- [Mesh-Mapper Drone Remote ID (Hackster.io)](https://www.hackster.io/colonelpanic/mesh-mapper-drone-remote-id-mapping-and-mesh-alerts-8e7c61)
- [colonelpanichacks/drone-mesh-mapper (GitHub)](https://github.com/colonelpanichacks/drone-mesh-mapper)
- [Map Remote ID Drones with ESP32 and Meshtastic (CNX Software)](https://www.cnx-software.com/2025/06/05/map-remote-id-enabled-drones-with-esp32-c3-s3-and-meshtastic-lora-modules/)
- [Acoustic Drone Detection with ESP32 (Hackaday)](https://hackaday.com/2026/03/23/acoustic-drone-detection-on-the-cheap-with-esp32/)
- [TN666/batear (GitHub)](https://github.com/TN666/batear)
- [RTL-SDR Drone Detection Projects](https://www.rtl-sdr.com/tag/drone/)
- [nRF24 Drone Detection (GitHub)](https://github.com/RamiLup/HMI-Prototype-drone-detection-nRF24)
- [Open Drone ID Core C Library (GitHub)](https://github.com/opendroneid/opendroneid-core-c)
- [Flock Safety (Wikipedia)](https://en.wikipedia.org/wiki/Flock_Safety)
- [EFF Investigations of Flock Safety](https://www.eff.org/deeplinks/2025/12/effs-investigations-expose-flock-safetys-surveillance-abuses-2025-review)
- [ACLU on Flock Surveillance](https://data.aclum.org/2025/10/07/flock-gives-law-enforcement-all-over-the-country-access-to-your-location/)
- [Counter-Drone Technology 2026 Guide (Airsight)](https://www.airsight.com/blog/counter-drone-technology-2026-guide)
- [FAA Remote ID Rule for Drones 2026](https://www.droneasaservice.com/blog/faa-remote-id-rule-for-drones/)
- [Remote ID Compliance 2025 (Loyalty Drones)](https://loyaltydrones.com/remote-id-in-2025-navigating-drone-compliance-and-detection/)
- [Washington State Flock Camera Restrictions (MRSC)](https://mrsc.org/stay-informed/mrsc-insight/april-2026/restrictions-flock-cameras)
- [State Privacy Laws Restricting License Plate Readers (Stateline)](https://stateline.org/2026/01/08/worried-about-surveillance-states-enact-privacy-laws-and-restrict-license-plate-readers/)
- [Flock Camera: How They Work (Digital Policy Desk)](https://digitalpolicydesk.com/blog/flock-camera-how-flock-safety-license-plate-readers-actually)
- [Flock Safety LPR Product Page](https://www.flocksafety.com/products/license-plate-readers)
- [nyanBOX (GitHub)](https://github.com/jbohack/nyanBOX)
- [DroneRF Detection (GitHub)](https://github.com/Al-Sad/DroneRF)
