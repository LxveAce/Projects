# Chasing Your Tail NG -- Comprehensive Guide to BLE/Wi-Fi Surveillance Detection

## 1. Overview and Problem It Solves

**Chasing Your Tail NG** (CYT-NG) is an open-source, Python-based counter-surveillance tool that helps you determine if you are being physically followed. It was created by **Matt Edmondson**, a former 22-year U.S. federal agent (Department of Homeland Security), digital forensics expert, and certified SANS instructor.

**The problem:** There is a massive imbalance between tools designed to surveil people versus tools designed to help people detect surveillance. As Edmondson put it: "It was really kind of disheartening and depressing to look at the ratio of tools to spy on people versus tools to help you not get spied on."

**Origin story:** A colleague from another government agency needed help protecting a confidential informant connected to a terrorist organization. The handler was skilled at traditional counter-surveillance (driving techniques, route changes), but needed an "electronic supplement" to detect wireless devices belonging to a surveillance team. Finding no existing solutions, Edmondson built the first prototype in about a month. He later presented it at **Black Hat USA 2022**, where it was featured in Wired magazine.

**Repository:** [github.com/ArgeliusLabs/Chasing-Your-Tail-NG](https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG) -- 2.3k stars, 419 forks, MIT license.

**Real-world use cases:**

- Confidential informant protection (original purpose)
- Hospital staff safety (ER workers receiving death threats)
- Search and rescue (detecting lost persons' broadcasting devices)
- Force protection (government agencies incorporating tool logic into procedures)
- Personal safety for stalking victims, journalists, activists

---

## 2. How It Works Technically

CYT-NG uses **passive wireless monitoring** to detect when the same device(s) persistently appear near you as you move through different locations. The core insight: even sophisticated surveillance teams carry phones and other wireless devices that constantly emit identifiable signals.

### Detection Method: Temporal Persistence Analysis

Rather than simple location-based tracking, the system uses **overlapping time windows**:

| Window | Timeframe |
|--------|-----------|
| Recent | 0-5 minutes ago |
| Medium | 5-10 minutes ago |
| Old | 10-15 minutes ago |
| Oldest | 15-20 minutes ago |

The system asks: "Do I see a device right now that I also saw 5 minutes ago, 10 minutes ago, and 15 minutes ago?" If you are driving from place to place and the same device signatures persist across multiple windows, that is a strong indicator of surveillance.

### Data Flow Pipeline

1. **Kismet** (open-source wireless sniffer) captures Wi-Fi and Bluetooth frames into SQLite databases
2. CYT-NG queries the Kismet database every **60 seconds**
3. The system maintains sliding time windows and filters probe requests
4. Device reappearances are logged and scored
5. **Persistence scores** (0.0 to 1.0 scale) are calculated using weighted algorithms that evaluate:
   - Temporal persistence across windows
   - Location correlation across multiple GPS points
   - Probe request pattern analysis
   - Timing anomalies (work hours vs. off-hours patterns)
6. Alerts are generated; reports and KML files are produced

### How It Defeats MAC Randomization

Modern phones randomize their MAC addresses, but CYT-NG does not rely solely on MACs. It analyzes **Wi-Fi probe requests** -- the SSIDs (network names) a device broadcasts when searching for known networks. The *set of SSIDs* a device probes for acts as a fingerprint. Unique network names (like a home router's custom SSID, a corporate network name, etc.) create identifiable signatures even when MAC addresses rotate.

### GPS Integration

- Automatic coordinate extraction from Kismet's Bluetooth GPS data
- Device-to-location correlation in real time
- **Location clustering** with a 100-meter threshold
- KML file generation for Google Earth visualization with color-coded persistence markers and device tracking paths

---

## 3. What It Detects

CYT-NG detects **any wireless device that broadcasts signals**:

**Primary detection targets:**

- **Smartphones** (iOS and Android) -- via Wi-Fi probe requests and Bluetooth broadcasts
- **Laptops and tablets** -- same mechanism
- **Bluetooth devices** -- anything broadcasting BLE or classic Bluetooth identifiers
- **Drones** -- Edmondson notes drones using "long range Bluetooth" are detectable "a kilometer out"
- **TPMS sensors** -- Tire Pressure Monitoring Systems (via software-defined radio integration)

**BLE Tracker Detection (AirTags, Tile, SmartTag):**

CYT-NG can detect **any Bluetooth-broadcasting device that Kismet can see**, which includes:

- **Apple AirTags** (including AirTag 2 with U2 chip released January 2026)
- **Samsung SmartTags**
- **Tile trackers**
- **Any other BLE beacon or tracker**

However, it is important to understand the distinction: CYT-NG detects these devices as part of its general Bluetooth scanning via Kismet. It does **not** have AirTag-specific identification logic (like decoding Apple's FindMy rotating keys). It sees them as Bluetooth devices that persist near you. For dedicated AirTag/SmartTag identification with anti-stalking alerts, see the Alternatives section below.

---

## 4. Hardware Requirements

**Total cost: Under $100** (often effectively free if you already own a Raspberry Pi)

| Component | Purpose | Estimated Cost |
|-----------|---------|---------------|
| **Raspberry Pi** (Model 2, 3, 4, 5, or Zero) | Main computer | $35-$75 |
| **Wi-Fi adapter with monitor mode** (Alpha or Panda brand recommended) | Passive wireless capture | $20-$30 |
| **USB GPS receiver** | Location tracking | ~$10 |
| **Portable battery/charger** | Power supply | $10-$20 (if not owned) |
| **Small LCD touchscreen** (optional) | Display alerts in the field | $20-$30 |
| **Small waterproof case** (Pelican-style) | Housing | $10-$20 (if not owned) |
| **Bluetooth GPS** (optional) | Higher-accuracy GPS | ~$50 |

**Software requirements:**

- Linux-based OS (Raspberry Pi OS recommended)
- Python 3.6+
- Kismet wireless packet capture tool
- Wi-Fi adapter driver supporting monitor mode

As Edmondson quipped: "How many Raspberry Pis do you have laying around your house doing absolutely nothing?"

---

## 5. Build Guide -- Step by Step

### Step 1: Prepare the Raspberry Pi

1. Flash **Raspberry Pi OS** (Lite or Desktop) onto a microSD card
2. Boot the Pi, connect to the internet, and update:

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Kismet

Kismet is the core wireless capture engine. Install from the Kismet repository for the latest version:

```bash
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | sudo apt-key add -
echo "deb https://www.kismetwireless.net/repos/apt/release/$(lsb_release -cs) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/kismet.list
sudo apt update
sudo apt install kismet -y
```

> **Note:** Compiling Kismet from source on a Raspberry Pi is very slow (potentially hours). Using the package repository is strongly recommended.

### Step 3: Set Up the Wi-Fi Adapter

1. Plug in the external Wi-Fi adapter (Alpha/Panda with monitor mode support)
2. Verify it is detected:

```bash
iwconfig
# or
ip link
```

3. Put it into monitor mode:

```bash
sudo airmon-ng start wlan1
```

Replace `wlan1` with your adapter's interface name.

### Step 4: Connect GPS

1. Plug in USB GPS receiver
2. Install gpsd:

```bash
sudo apt install gpsd gpsd-clients -y
```

3. Configure gpsd to use the GPS device
4. Verify GPS lock:

```bash
cgps
# or
gpsmon
```

### Step 5: Clone and Install CYT-NG

```bash
git clone https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG.git
cd Chasing-Your-Tail-NG
pip3 install -r requirements.txt
```

### Step 6: Security Migration (CRITICAL -- Do This First)

```bash
python3 migrate_credentials.py
```

This sets up encrypted credential storage for API keys and eliminates legacy plaintext storage.

### Step 7: Configure

Edit `config.json` to set:

- Kismet database path patterns
- Log and ignore list directories
- Time window durations (defaults: 5/10/15/20 minutes)
- Geographic search boundaries
- WiGLE API key (optional, for SSID geolocation)

### Step 8: Assemble the Hardware

1. Mount the Pi, battery, Wi-Fi adapter, and GPS in the case
2. Connect the touchscreen (if using)
3. Route cables neatly; ensure airflow for the Pi

---

## 6. Software Setup

### Core Components

| File | Purpose |
|------|---------|
| `chasing_your_tail.py` | Core real-time monitoring engine |
| `cyt_gui.py` | Enhanced Tkinter GUI with surveillance analysis |
| `surveillance_analyzer.py` | GPS surveillance detection orchestrator |
| `surveillance_detector.py` | Persistence detection engine |
| `gps_tracker.py` | Location clustering and KML generation |
| `probe_analyzer.py` | Post-processing with WiGLE integration |
| `start_kismet_clean.sh` | Primary Kismet startup script (the ONLY working startup script) |
| `migrate_credentials.py` | Security credential migration (run first!) |
| `config.json` | Central configuration file |

### Security Modules

| File | Purpose |
|------|---------|
| `secure_database.py` | SQL injection prevention via parameterized queries |
| `secure_credentials.py` | Encrypted API key management |
| `secure_ignore_loader.py` | Safe ignore list loading (replaces dangerous `exec()` calls) |
| `input_validation.py` | Input sanitization utilities |

### Output Directories

- `./surveillance_reports/` -- Markdown and HTML surveillance reports
- `./kml_files/` -- Google Earth visualization files
- `./logs/` -- Core monitoring logs
- `./analysis_logs/` -- Surveillance analysis logs
- `./reports/` -- Probe analysis reports
- `./ignore_lists/` -- MAC and SSID filter lists (JSON format)

### Optional: WiGLE API Integration

WiGLE is a crowdsourced database of wireless networks with GPS coordinates. By adding a WiGLE API key to your encrypted credentials, CYT-NG can geolocate SSIDs found in probe requests to map where surveillance devices have connected to networks. Note: WiGLE API calls consume credits.

### Optional: Pandoc (for HTML Reports)

Install Pandoc to convert Markdown reports to HTML:

```bash
sudo apt install pandoc
```

---

## 7. Usage Guide

### Initial Setup: Create an Ignore List

Before moving, sit at your starting location for 2-3 minutes with everything running. The system will capture your own devices, neighbors' devices, and stationary nearby devices. These are saved to the ignore list so they do not trigger false alerts when you start moving.

### Starting the System

**Option A: GUI Mode (Recommended)**

```bash
python3 cyt_gui.py
```

The GUI provides large, touchscreen-friendly buttons:

- Create/delete ignore list
- Check system status
- Start surveillance detection mode
- Surveillance Analysis button with GPS-correlated persistence detection
- Analyze Logs button for historical probe data

**Option B: Command Line**

```bash
# Start Kismet first (use the working startup script)
./start_kismet_clean.sh

# Start core monitoring
python3 chasing_your_tail.py
```

### Surveillance Analysis Commands

```bash
# Standard detection (auto-extracts GPS from Kismet)
python3 surveillance_analyzer.py

# Demo mode (uses Phoenix, AZ coordinates for testing)
python3 surveillance_analyzer.py --demo

# Analyze a specific Kismet database
python3 surveillance_analyzer.py --kismet-db /path/to/database.kismet

# Focus on stalking detection with high persistence threshold
python3 surveillance_analyzer.py --stalking-only --min-persistence 0.8

# Export results as JSON
python3 surveillance_analyzer.py --output-json results.json

# Use external GPS data
python3 surveillance_analyzer.py --gps-file coordinates.json
```

### Post-Analysis Commands

```bash
# Analyze collected data from past 14 days (default)
python3 probe_analyzer.py

# Analyze specific duration
python3 probe_analyzer.py --days 7

# Analyze all available logs
python3 probe_analyzer.py --all-logs

# Include WiGLE geolocation data
python3 probe_analyzer.py --wigle
```

### Interpreting Results

| Persistence Score | Level | Meaning |
|-------------------|-------|---------|
| 0.0 - 0.3 | Low | Device appeared briefly |
| 0.3 - 0.6 | Moderate | Worth noting, could be coincidence (same commute route, etc.) |
| 0.6 - 0.8 | High | Device has been near you across multiple time windows and/or locations |
| 0.8 - 1.0 | Critical | Strong indicator of surveillance; same device seen persistently across locations and extended time |

KML files can be opened in Google Earth to visualize device tracking paths with color-coded markers based on persistence levels.

---

## 8. Limitations

1. **Not a BLE tracker identifier:** CYT-NG sees Bluetooth devices generically. It does not decode Apple FindMy protocols, Samsung SmartTag protocols, or Tile protocols. It cannot tell you "this is an AirTag" specifically -- only that a Bluetooth device has been persistently near you.

2. **False positives:** Devices appearing persistent might belong to commuters on the same route, people stuck in the same traffic, or neighbors with overlapping schedules. The tool generates "actionable leads," not definitive proof.

3. **Sophisticated adversaries:** A surveillance team using Faraday bags, burner devices with no saved Wi-Fi networks, or entirely passive equipment could evade detection. However, in practice, even trained teams carry personal devices.

4. **Linux only:** The system requires a Linux-based OS. It does not run natively on Windows or macOS.

5. **Monitor-mode Wi-Fi adapter required:** Not all Wi-Fi adapters support monitor mode. You need a specific compatible adapter (Alpha or Panda brand recommended).

6. **Large dataset performance:** Analyzing large historical Kismet databases can be slow, especially on lower-powered Raspberry Pi models.

7. **WiGLE API costs:** The WiGLE integration consumes API credits per request.

8. **MAC randomization edge cases:** While CYT-NG's SSID-based fingerprinting mitigates MAC randomization, devices that probe for zero SSIDs (increasingly common on modern iOS/Android) are harder to fingerprint.

9. **Requires movement:** The tool is designed for mobile use. Sitting stationary defeats the purpose -- you need to move through multiple locations to see if devices follow you.

10. **Raspberry Pi 5 compatibility:** The author has noted ongoing work to update for full Raspberry Pi 5 support.

---

## 9. Privacy and Legal Context

### Legal Disclaimer (from the repository)

> "This tool is intended for legitimate security research, network administration, and personal safety purposes. Users are responsible for complying with all applicable laws and regulations."

### Privacy Considerations

**Defensive use:** CYT-NG passively monitors publicly broadcast wireless signals. It does not transmit, jam, or interfere with any signals. Wi-Fi probe requests and Bluetooth advertisements are broadcast openly by devices. In most jurisdictions, passively receiving publicly broadcast radio signals is legal.

**Ethical tension:** The tool normalizes passive collection of device signatures from all nearby individuals, not just suspected surveillance operatives. Everyone in your vicinity has their device signatures logged.

**Democratization argument:** Edmondson's position is that defensive value for vulnerable populations (stalking victims, informants, journalists, activists) outweighs the potential for misuse. Counter-surveillance capabilities were previously available only to state actors and well-funded organizations.

### The Broader Tracker Stalking Problem

The rise of cheap BLE trackers (AirTags at $29, Tile, SmartTag) has created a new category of stalking threat. Apple, Google, and Samsung have responded with:

- **Apple:** Automatic "AirTag Found Moving With You" alerts on iPhones
- **Google/Apple joint standard:** "Detecting Unwanted Location Trackers" (DULT) specification, implemented in Android and iOS
- **Samsung:** SmartTags emit sound when separated from owner for extended periods

These built-in protections are useful but have gaps: detection delays can be hours or days, cross-platform detection was historically poor (Android users could not detect AirTags easily until DULT), and sophisticated attackers can modify tracker firmware to disable anti-stalking features.

---

## 10. Alternatives

### Software Alternatives (Phone Apps)

| Tool | Platform | What It Detects | Open Source? |
|------|----------|----------------|-------------|
| [AirGuard](https://github.com/seemoo-lab/AirGuard) | Android, [iOS](https://github.com/seemoo-lab/AirGuard-iOS) | AirTags, Samsung SmartTags, Tile, Google Find My, Chipolo | Yes (TU Darmstadt) |
| Apple Tracker Detect | Android | AirTags only | No |
| Built-in iOS alerts | iOS | AirTags, DULT-compliant trackers | No |
| Built-in Android alerts | Android | AirTags, SmartTags, DULT-compliant trackers | No |

**AirGuard** is the most capable open-source alternative for pure BLE tracker detection. Developed by the Secure Mobile Networking Lab at TU Darmstadt, it scans in the background, saves all detected trackers locally (no data leaves your device), and alerts you when the same tracker appears at 3+ different locations. It can play sound on detected AirTags to help locate them physically.

### Hardware/DIY Alternatives

| Tool | Hardware | What It Does |
|------|----------|-------------|
| [ESP32 BLETracker](https://github.com/shogunxam/ESP32_BLETracker) | ESP32 | Tracks BLE devices, reports via MQTT to Home Assistant |
| [Blecker](https://github.com/redakker/blecker) | ESP32 | BLE presence detection for smart home via MQTT |
| [BLE-Scanner](https://github.com/gromeck/BLE-Scanner) | ESP32 | BLE scanning with MQTT reporting, web frontend |
| [nRFBox](https://www.hackster.io/CiferTech/esp32-powered-tool-to-scan-jam-spoof-ble-wi-fi-nrfbox-96b516) | ESP32 | Scan, analyze BLE/Wi-Fi/2.4GHz (note: jamming/spoofing features may be illegal) |
| [OpenHaystack](https://github.com/seemoo-lab/openhaystack) | Various | Build your own FindMy-compatible trackers (offensive, not defensive) |

### How CYT-NG Compares

CYT-NG occupies a unique niche: it is the only open-source tool that combines **Wi-Fi probe request analysis + Bluetooth monitoring + GPS correlation + temporal persistence scoring** into a mobile counter-surveillance platform. Phone apps like AirGuard are better for detecting *specific commercial BLE trackers* (AirTags, SmartTags). CYT-NG is better for detecting *human surveillance teams* carrying any wireless device.

**Best combined approach:** Run CYT-NG on a Raspberry Pi in your bag/car for broad wireless surveillance detection, AND run AirGuard on your phone for dedicated BLE tracker identification. The two tools are complementary, not competing.

---

## Sources

- [ArgeliusLabs/Chasing-Your-Tail-NG - GitHub](https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG)
- [The Return of "Chasing Your Tail" - Argelius Labs Blog](https://www.argeliuslabs.com/the-return-of-chasing-your-tail-a-tool-born-from-real-need/)
- [Chasing Your Tail: Anti-Stalking Digital Tracker - Raspberry Pi Magazine](https://magazine.raspberrypi.com/articles/chasing-your-tail-anti-stalking-digital-tracker)
- [How to Track the People Tracking YOU - David Bombal](https://davidbombal.com/how-to-track-the-people-tracking-you/)
- [How to Track the People Tracking YOU: A Deep Study - Paul Flores](https://paulfloreswriter.wordpress.com/2026/04/03/how-to-track-the-people-tracking-you-a-deep-study-of-surveillance-detection-using-open-source-tools/)
- [Anti-Tracking Tool Tells You If You're Being Followed - Malwarebytes](https://www.malwarebytes.com/blog/news/2022/08/someone-made-an-anti-tracking-tool-that-alerts-you-if-youre-being-tailed)
- [Black Hat USA 2022 Presentation PDF](https://i.blackhat.com/USA-22/Thursday/US-22-Edmondson-Chasing-Your-Tail.pdf)
- [AirGuard - GitHub (Android)](https://github.com/seemoo-lab/AirGuard)
- [AirGuard iOS - GitHub](https://github.com/seemoo-lab/AirGuard-iOS)
- [AirGuard on F-Droid](https://f-droid.org/packages/de.seemoo.at_tracking_detection/)
- [ESP32 BLETracker - GitHub](https://github.com/shogunxam/ESP32_BLETracker)
- [nRFBox - Hackster.io](https://www.hackster.io/CiferTech/esp32-powered-tool-to-scan-jam-spoof-ble-wi-fi-nrfbox-96b516)
