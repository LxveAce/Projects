# Kismet Wireless Network Detector and Wardriving -- Comprehensive Guide

---

## Table of Contents

1. [Overview and Capabilities](#1-overview-and-capabilities)
2. [Hardware](#2-hardware)
3. [Installation Guide](#3-installation-guide)
4. [Wardriving Rig Parts List](#4-wardriving-rig-parts-list)
5. [Setup and Configuration](#5-setup-and-configuration)
6. [Usage -- Running a Wardrive](#6-usage----running-a-wardrive)
7. [Data Analysis and WiGLE Mapping](#7-data-analysis-and-wigle-mapping)
8. [Legal Considerations](#8-legal-considerations)
9. [Best Practices](#9-best-practices)
10. [Sources](#sources)

---

## 1. Overview and Capabilities

**Kismet** is an open-source wireless network detector, sniffer, Wireless Intrusion Detection System (WIDS), and wardriving tool. Originally created in 2001, it has evolved into one of the most powerful passive wireless reconnaissance platforms available.

### What Kismet Does

- **Passive network detection** -- Kismet operates entirely passively, never transmitting packets. It places wireless adapters into monitor mode and captures raw 802.11 frames, leaving zero trace of reconnaissance activity.
- **Multi-protocol support** -- Wi-Fi (2.4 GHz, 5 GHz, 6 GHz/Wi-Fi 6E), Bluetooth, Bluetooth Low Energy (BLE), Zigbee, RF sensors, ADSB airplane beacons, power meters, water meters, and nRF-based wireless keyboards.
- **Distributed architecture** -- Remote capture sensors can stream data over TCP sockets or websockets back to a central Kismet server, enabling multi-location deployments.
- **Unified logging** -- The `.kismet` database format (built on SQLite3) combines packets, device records, GPS coordinates, and runtime data into a single file.
- **REST API** -- A full REST-based API allows scripting, automation, and integration with other tools.
- **Web UI** -- A modern dark-mode web interface accessible at `http://localhost:2501` for real-time monitoring.
- **Wardrive mode** -- A dedicated configuration overlay optimized for mobile AP scanning with direct WiGLE CSV export.

### Supported Platforms

| Platform | Notes |
|----------|-------|
| Linux | Primary platform, best hardware support |
| macOS | Native Airport card support |
| Windows | Via remote capture using WSL (Windows Subsystem for Linux) |

### Latest Version

The most recent major release is **2025-09-R1**, which includes numerous bugfixes, UI improvements, performance optimizations, and 6 GHz channel support enhancements.

---

## 2. Hardware

### WiFi Adapters with Monitor Mode Support

The adapter is the most critical component. You need chipsets with proper Linux kernel support for monitor mode and packet injection. Here are the recommended options as of 2026:

#### Tier 1 -- Highly Recommended

| Adapter | Chipset | Bands | Notes |
|---------|---------|-------|-------|
| **Alfa AWUS036AXML** | MediaTek MT7921AUN | 2.4/5/6 GHz | The only reliable WiFi 6E adapter for wardriving. Active monitor mode works with kernel 6.12+. Required for 6 GHz scanning. ~$50 |
| **Alfa AWUS036ACH** | Realtek RTL8812AU | 2.4/5 GHz | Dual-band AC adapter. Kali 2026.1 (kernel 6.14) mainlines the driver -- plug and play. ~$35 |
| **Alfa AWUS036NHA** | Atheros AR9271 | 2.4 GHz | The classic pentesting adapter. Works out of the box on every Linux distribution. Rock-solid reliability. ~$25 |

#### Tier 2 -- Good Options

| Adapter | Chipset | Bands | Notes |
|---------|---------|-------|-------|
| **Alfa AWUS036ACM** | MediaTek MT7612U | 2.4/5 GHz | 802.11ac, well-supported in Linux kernel. ~$40 |
| **Panda PAU09** | Realtek RTL8814AU | 2.4/5 GHz | Dual-band with dual antennas. Requires out-of-kernel driver. ~$20 |

#### Chipsets to Avoid

- **Realtek RTL8832BU and RTL8852AU** -- Incomplete Linux monitor mode support as of mid-2026.
- **Broadcom (Raspberry Pi onboard WiFi)** -- Only works with nexmon patches; default drivers do not support monitor mode. Use an external USB adapter instead.
- **ath10k-based cards** -- Generate floods of spurious packets in monitor mode.
- **Most out-of-kernel drivers** -- Generally incompatible or unreliable with Kismet.

#### Multi-Adapter Strategy

For serious wardriving, run multiple adapters simultaneously:

- **Adapter 1**: Alfa AWUS036NHA locked to 2.4 GHz channels 1, 6, 11
- **Adapter 2**: Alfa AWUS036ACH or ACM hopping 5 GHz channels
- **Adapter 3**: Alfa AWUS036AXML dedicated to 6 GHz (if doing WiFi 6E)

### GPS Modules

GPS is essential for geolocating discovered networks. The GPS feeds coordinates to Kismet via `gpsd`.

| GPS Module | Interface | Chipset | Notes |
|------------|-----------|---------|-------|
| **VK-162 USB GPS Dongle** | USB | u-blox 7 | Best choice. Native `cdc_acm` Linux driver, no configuration needed. Multi-GNSS support. ~$12-15 on Amazon |
| **VFan UG-353** | USB | u-blox 7 | Same u-blox 7 firmware as VK-162. Excellent gpsd compatibility. ~$15 |
| **GlobalSat BU-353-S4** | USB | SiRF Star IV | Long-established option but being phased out. Some reported Linux compatibility issues. ~$30 |
| **Adafruit Ultimate GPS (PA1616S)** | Serial/UART | MediaTek MT3339 | Best for Raspberry Pi GPIO connection. 10 Hz update rate. ~$30 |
| **BN-220** | Serial/UART | u-blox M8N | Compact, multi-GNSS, great for Pi builds. ~$15 |

**Important**: GPS modules need to download almanac data and lock onto satellites before first use. This initial lock can take 20+ minutes outdoors. Subsequent cold starts are faster (1-3 minutes).

### Raspberry Pi

| Model | Suitability | Notes |
|-------|-------------|-------|
| **Raspberry Pi 5** | Excellent | Fastest Pi, best for running Kismet with multiple adapters. USB 3.0 ports. ~$80 |
| **Raspberry Pi 4 (4GB+)** | Great | Most popular choice. Adequate for 2-3 adapters. ~$55 |
| **Raspberry Pi 3B+** | Adequate | Works but slower. Fine for single-adapter setups. ~$35 |
| **Raspberry Pi Zero 2 W** | Minimal | Ultra-compact but limited USB (needs hub). Good for single-adapter stealth builds. ~$15 |

---

## 3. Installation Guide

### Option A: Kali Linux (Recommended for Laptops)

Kismet is in the Kali repos by default:

```bash
sudo apt update && sudo apt install kismet
```

For the latest version from the official Kismet repository:

```bash
# Install GPG key
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key --quiet \
  | gpg --dearmor | sudo tee /usr/share/keyrings/kismet-archive-keyring.gpg >/dev/null

# Add repository
echo 'deb [signed-by=/usr/share/keyrings/kismet-archive-keyring.gpg] https://www.kismetwireless.net/repos/apt/release/kali kali main' \
  | sudo tee /etc/apt/sources.list.d/kismet.list >/dev/null

# Install
sudo apt update && sudo apt install kismet
```

### Option B: Debian Bookworm / Trixie

```bash
# GPG key (same as above)
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key --quiet \
  | gpg --dearmor | sudo tee /usr/share/keyrings/kismet-archive-keyring.gpg >/dev/null

# Add repository (substitute 'bookworm' or 'trixie')
echo 'deb [signed-by=/usr/share/keyrings/kismet-archive-keyring.gpg] https://www.kismetwireless.net/repos/apt/release/bookworm bookworm main' \
  | sudo tee /etc/apt/sources.list.d/kismet.list >/dev/null

sudo apt update && sudo apt install kismet
```

### Option C: Ubuntu (20.04 / 22.04 / 24.04 / 25.04)

Same process -- substitute the codename (`focal`, `jammy`, `noble`, or `plucky`) in the repository URL:

```bash
# Example for Ubuntu 24.04 Noble
echo 'deb [signed-by=/usr/share/keyrings/kismet-archive-keyring.gpg] https://www.kismetwireless.net/repos/apt/release/noble noble main' \
  | sudo tee /etc/apt/sources.list.d/kismet.list >/dev/null
```

### Option D: Raspberry Pi OS (Bookworm 64-bit)

```bash
# Same GPG key step, then:
echo 'deb [signed-by=/usr/share/keyrings/kismet-archive-keyring.gpg] https://www.kismetwireless.net/repos/apt/release/bookworm bookworm main' \
  | sudo tee /etc/apt/sources.list.d/kismet.list >/dev/null

sudo apt update && sudo apt install kismet
```

### Post-Installation (All Distributions)

```bash
# Allow suid-root capture helpers (answer Yes when prompted during install)
# Add your user to the kismet group
sudo usermod -aG kismet $USER

# Reboot for group membership to take effect
sudo reboot
```

### Install GPS Daemon

```bash
sudo apt install gpsd gpsd-clients
```

### Signing Key Note (February 2026)

The Kismet GPG signing key was refreshed with SHA256 signatures in February 2026. If you have an older keyring, remove and re-download:

```bash
sudo rm /usr/share/keyrings/kismet-archive-keyring.gpg
wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key --quiet \
  | gpg --dearmor | sudo tee /usr/share/keyrings/kismet-archive-keyring.gpg >/dev/null
```

### Optional Capture Packages

```bash
# Bluetooth capture
sudo apt install kismet-capture-linux-bluetooth

# nRF Mousejack capture
sudo apt install kismet-capture-nrf-mousejack

# RTL-SDR based captures (ADS-B, AMR meters, 433MHz sensors)
sudo apt install python-kismetcapturertl433 python-kismetcapturertladsb python-kismetcapturertlamr

# Zigbee capture
sudo apt install python-kismetcapturefreaklabszigbee

# Log analysis tools
sudo apt install kismet-logtools
```

---

## 4. Wardriving Rig Parts List

### Budget Build (~$100-130)

| Component | Product | Approx. Price |
|-----------|---------|---------------|
| Computer | Raspberry Pi 4 (4GB) | $55 |
| WiFi Adapter | Alfa AWUS036NHA (2.4 GHz) | $25 |
| GPS | VK-162 USB GPS Dongle | $12 |
| Storage | 32GB microSD (Class 10/A2) | $8 |
| Power | 10,000 mAh USB-C power bank (3A output) | $15 |
| Case | Generic Pi 4 case | $8 |
| **Total** | | **~$123** |

### Mid-Range Build (~$200-250)

| Component | Product | Approx. Price |
|-----------|---------|---------------|
| Computer | Raspberry Pi 5 (4GB) | $60 |
| WiFi Adapter 1 | Alfa AWUS036NHA (2.4 GHz) | $25 |
| WiFi Adapter 2 | Alfa AWUS036ACH (2.4/5 GHz) | $35 |
| GPS | VK-162 USB GPS Dongle | $12 |
| Storage | 64GB microSD (A2) | $10 |
| Power | 20,000 mAh USB-C PD power bank | $25 |
| USB Hub | Powered USB 3.0 4-port hub | $15 |
| Case | Pelican-style waterproof case | $20 |
| Display (optional) | 3.5" SPI LCD or OLED | $15 |
| Misc | USB cables, velcro, zip ties | $10 |
| **Total** | | **~$227** |

### Full Coverage Build (~$350-400)

| Component | Product | Approx. Price |
|-----------|---------|---------------|
| Computer | Raspberry Pi 5 (8GB) | $80 |
| WiFi Adapter 1 | Alfa AWUS036NHA (2.4 GHz) | $25 |
| WiFi Adapter 2 | Alfa AWUS036ACM (2.4/5 GHz) | $40 |
| WiFi Adapter 3 | Alfa AWUS036AXML (6 GHz) | $50 |
| GPS | VK-162 USB GPS Dongle | $12 |
| Storage | 128GB microSD (A2) | $15 |
| Power | 26,800 mAh USB-C PD power bank | $35 |
| USB Hub | Powered USB 3.0 7-port hub | $20 |
| Case | Pelican 1150 or similar | $30 |
| Display | HyperPixel 4.0 (800x480 touch) | $35 |
| Antenna upgrades | Alfa 9dBi directional antennas | $25 |
| Misc | Suction cup mount, cables, velcro | $15 |
| **Total** | | **~$382** |

### Laptop-Based Alternative

If you already have a laptop, the minimum additional cost is just:

- Alfa AWUS036ACH (~$35) + VK-162 GPS (~$12) = **~$47**
- Run Kali Linux from a persistent USB boot drive so you don't modify your host OS.

---

## 5. Setup and Configuration

### 5.1 GPS Configuration

#### USB GPS (VK-162 or similar)

```bash
# Plug in GPS, identify device
dmesg | grep tty
# Look for /dev/ttyACM0 or /dev/ttyUSB0

# Configure gpsd
sudo nano /etc/default/gpsd
```

Set these values:

```
START_DAEMON="true"
DEVICES="/dev/ttyACM0"
GPSD_OPTIONS="-n"
USBAUTO="true"
```

```bash
# Restart gpsd
sudo systemctl restart gpsd

# Test GPS lock (take the GPS near a window or outside)
cgps -s
# Wait for "3D Fix" -- can take 20+ minutes on first use
# Alternative: gpsmon -n
```

#### Serial GPS on Raspberry Pi (GPIO)

Wire the GPS module:

- GPS TX to RPi GPIO 15 (pin 10)
- GPS RX to RPi GPIO 14 (pin 8)
- GPS VCC to 3.3V
- GPS GND to GND

```bash
# Disable serial console
sudo raspi-config
# Navigate: Interface Options > Serial Port
# Login shell over serial: No
# Hardware serial enabled: Yes

# Edit gpsd config
sudo nano /etc/default/gpsd
```

Set `DEVICES="/dev/ttyS0"` and restart as above.

### 5.2 Kismet Configuration

The main configuration file is at `/etc/kismet/kismet.conf`. Override settings in `/etc/kismet/kismet_site.conf` (recommended -- survives package updates).

#### Define WiFi Sources

```bash
sudo nano /etc/kismet/kismet_site.conf
```

```
# Single adapter, all bands
source=wlan1:name=wardriver

# Multiple adapters with band assignments
source=wlan1:name=24ghz,band5ghz=false,band6ghz=false
source=wlan2:name=5ghz,band24ghz=false,band6ghz=false
source=wlan3:name=6ghz,band24ghz=false,band5ghz=false

# Specific channel list (optimized for high-density areas)
source=wlan1:name=primary,channels="1,6,11,36,40,44,48,149,153,157,161,165"

# 6 GHz source (requires regulatory domain set first)
source=wlan3:name=6e,band24ghz=false,band5ghz=false,band6ghz=true,channel=1w6e
```

#### Set Regulatory Domain (Required for 6 GHz)

```bash
sudo iw reg set US    # Replace US with your country code
```

#### Key Configuration Options

```
# GPS source (usually auto-detected via gpsd)
gps=gpsd:host=localhost,port=2947

# Log directory
log_prefix=/home/pi/kismet/logs

# Channel hopping speed (default is fine for most setups)
channel_hop_speed=5/sec

# Disable HT/VHT channels for wardrive efficiency
# (APs only beacon on primary channels)
source=wlan1:name=driver,ht_channels=false,vht_channels=false

# Filter to management frames only (reduces CPU dramatically)
source=wlan1:name=driver,filter_mgmt=true
```

### 5.3 Wardrive Mode Configuration

Kismet ships with a wardrive overlay (`kismet_wardrive.conf`) that automatically:

- Enables WiGLE CSV logging
- Disables HT/VHT channel scanning (APs only beacon on primary channels)
- Applies BPF filters restricting capture to management frames and EAPOL
- Disables non-AP device tracking
- Disables fingerprinting, IE tag retention, and EAPOL capture
- Turns off channel history and datasource logging
- Minimizes memory and CPU usage

No manual editing needed -- just launch with the `--override wardrive` flag (see Section 6).

### 5.4 Auto-Start on Boot (Raspberry Pi)

Create the startup script:

```bash
nano ~/start_kismet.sh
```

```bash
#!/bin/bash
sleep 30  # Wait for USB devices and GPS to initialize

USER_HOME="/home/pi"
KISMET_DIR="${USER_HOME}/kismet/logs"
mkdir -p "${KISMET_DIR}"
cd "${KISMET_DIR}"

KISMET_COMMAND="kismet -t wardrive_$(date +%Y%m%d) --override wardrive -q -s"
$KISMET_COMMAND

# Auto-restart if Kismet crashes
while true; do
    sleep 60
    if ! curl -Is http://localhost:2501 | grep -q "200 OK"; then
        $KISMET_COMMAND
    fi
done
```

```bash
chmod +x ~/start_kismet.sh

# Add to crontab
crontab -e
# Add this line:
@reboot /home/pi/start_kismet.sh
```

### 5.5 Optional: RaspAP for Remote Management

Install RaspAP to create a WiFi access point on the Pi for SSH/web access from your phone:

```bash
curl -sL https://install.raspap.com | bash
```

Default SSID: `raspi-webgui`, password: `ChangeMe`. Web login: admin/secret. Change all defaults immediately.

---

## 6. Usage -- Running a Wardrive

### 6.1 Pre-Drive Checklist

1. GPS has satellite lock (check with `cgps -s` -- must show "3D Fix")
2. WiFi adapter(s) are recognized (`iwconfig` or `ip link show`)
3. Power bank is charged
4. Sufficient storage space on SD card
5. Date/time is correct on the Pi (`timedatectl`)

### 6.2 Launch Kismet in Wardrive Mode

```bash
# Basic wardrive launch
sudo kismet --override wardrive

# With a named session
sudo kismet -t my_city_wardrive --override wardrive

# Quiet/headless mode (no console output)
sudo kismet -t wardrive_$(date +%Y%m%d) --override wardrive -q -s

# Specify log directory
sudo kismet -t wardrive --override wardrive --log-prefix /home/pi/kismet/logs
```

### 6.3 Monitor via Web UI

From any device on the same network, open a browser to:

```
http://<device-ip>:2501
```

First-time access requires creating an admin username/password. The web UI shows:

- Real-time device count
- GPS coordinates and map
- Channel activity
- Data source status
- Signal strength indicators

### 6.4 During the Drive

- **Speed**: 15-30 mph (25-50 km/h) is ideal. Faster speeds miss more APs.
- **Route**: Drive systematically through neighborhoods, commercial districts, and industrial areas. Cover all streets rather than just main roads.
- **Duration**: A typical urban wardrive session is 1-4 hours.
- **Antenna placement**: Mount the GPS on the dashboard or roof. Keep WiFi adapters elevated (suction cup window mount works well).
- **Power management**: A 20,000 mAh bank runs a Pi 4 + 2 adapters + GPS for approximately 6-8 hours.

### 6.5 Stop Kismet

```bash
# Graceful shutdown (via web UI or):
kill -TERM $(pidof kismet)

# Or press Ctrl+C if running in foreground
```

Kismet writes final data to the log files on clean shutdown.

---

## 7. Data Analysis and WiGLE Mapping

### 7.1 Output Files

Wardrive mode produces two types of log files:

| File | Format | Purpose |
|------|--------|---------|
| `*.kismet` | SQLite3 database | Full device/packet/GPS data (if not in pure wardrive mode) |
| `*.wiglecsv` | CSV text | WiGLE-compatible format for direct upload |

### 7.2 Converting Kismet Databases to WiGLE CSV

If you ran Kismet in normal mode (not `--override wardrive`):

```bash
kismetdb_to_wiglecsv --in session.kismet --out session.wiglecsv
```

### 7.3 Upload to WiGLE

1. Create an account at [https://wigle.net](https://wigle.net)
2. Go to [https://wigle.net/uploads](https://wigle.net/uploads)
3. Upload your `.wiglecsv` file
4. WiGLE processes the data and adds it to the global map
5. View your statistics and contributions on your profile

WiGLE accepts data from many tools: Kismet, NetStumbler, inSSIDer, MacStumbler, WiFi-Where, WiGLE WiFi Wardriving (Android app), and others.

### 7.4 WiGLE Android App

For casual wardriving without a full rig, install **WiGLE WiFi Wardriving** from Google Play. It uses your phone's WiFi and GPS to scan and upload directly. Great for walking or biking.

### 7.5 Local Analysis

#### Query the Kismet Database Directly

```bash
# Open the database
sqlite3 session.kismet

# Count unique APs
SELECT COUNT(DISTINCT devmac) FROM devices WHERE type='Wi-Fi AP';

# List open networks
SELECT devmac, device FROM devices WHERE type='Wi-Fi AP' AND device LIKE '%Open%';

# Export to CSV
.mode csv
.output my_networks.csv
SELECT * FROM devices WHERE type='Wi-Fi AP';
.quit
```

#### Generate KML for Google Earth

```bash
kismetdb_to_kml --in session.kismet --out session.kml
```

Open the `.kml` file in Google Earth to visualize network locations on a 3D map.

### 7.6 WiGLE API

For programmatic access to the WiGLE database:

```bash
# Example: search for networks near coordinates
curl -H "Authorization: Basic <your_encoded_token>" \
  "https://api.wigle.net/api/v2/network/search?latrange1=40.7&latrange2=40.8&longrange1=-74.0&longrange2=-73.9"
```

Register at WiGLE and generate API tokens from your account settings.

---

## 8. Legal Considerations

### United States Federal Law

**Wardriving itself is not explicitly illegal under US federal law.** Simply scanning for and logging the presence of wireless networks is a passive activity analogous to listening to radio broadcasts. The FCC permits detection of radio frequency signals in the unlicensed Wi-Fi spectrum.

### Where It Becomes Illegal

The legal line is crossed when passive scanning transitions to active exploitation:

| Activity | Legal Status | Relevant Law |
|----------|-------------|--------------|
| Passively detecting Wi-Fi networks | **Legal** | No prohibition on receiving RF signals |
| Logging SSIDs, BSSIDs, encryption types | **Legal** | Publicly broadcast information |
| Recording GPS coordinates of APs | **Legal** | No expectation of privacy for RF emissions |
| Uploading data to WiGLE | **Legal** | Aggregating publicly available data |
| Connecting to an open network without authorization | **Gray area / potentially illegal** | Computer Fraud and Abuse Act (CFAA) |
| Attempting to crack WPA/WEP passwords | **Illegal** | CFAA -- unauthorized access attempt |
| Intercepting network traffic content | **Illegal** | Wiretap Act (18 U.S.C. 2511) |
| Exploiting discovered networks | **Illegal** | CFAA (18 U.S.C. 1030) |

### The Computer Fraud and Abuse Act (CFAA)

The CFAA (18 U.S.C. 1030) prohibits "unauthorized access" to computer systems and networks. Key points:

- Scanning is not access.
- Connecting to a network you are not authorized to use may constitute unauthorized access.
- Penalties range from fines to imprisonment depending on the nature of the offense.

### State Laws

Some states have additional computer crime laws that may be more restrictive than federal law. Research your specific state's statutes. For example, some states criminalize "unauthorized access to a computer network" broadly enough that connecting to an open network without explicit permission could be prosecuted.

### International Considerations

Laws vary significantly by country. Some jurisdictions (e.g., Germany, parts of the EU) have stricter regulations on wireless scanning. Research local laws before wardriving internationally.

### Best Practices for Legal Protection

1. **Never connect to any network you discover.** Kismet is purely passive -- keep it that way.
2. **Never attempt to capture, crack, or decrypt passwords or traffic.**
3. **Do not wardrive on private property** (military bases, government facilities, corporate campuses) without explicit permission.
4. **Be prepared to explain what you are doing** if approached by law enforcement. Having Kismet's passive nature and your WiGLE profile ready to show can help.
5. **Keep your activities strictly passive** -- scan, log, drive on.

---

## 9. Best Practices

### Hardware

- **Use quality USB extension cables** or a powered USB hub. Cheap cables cause disconnections and data corruption.
- **Mount the GPS with a clear sky view.** Dashboard or roof-mounted via suction cup. GPS inside a backpack or glove box gets poor fixes.
- **Heat management**: In hot weather, ensure the Pi has ventilation. Thermal throttling degrades performance. A case with a fan is worth the extra few dollars.
- **Label your adapters** if using multiples. Use Kismet's `name=` parameter to give each source a meaningful identifier.

### Software

- **Always use `--override wardrive` mode** unless you specifically need full packet capture. It dramatically reduces CPU, memory, and storage usage.
- **Disable HT/VHT channels** in wardrive mode (done automatically by the overlay). APs only beacon on primary 20 MHz channels, so scanning HT40/HT80 wastes time.
- **Use BPF filtering** (`filter_mgmt=true`) to capture only management frames. This reduces CPU usage by 50-80%.
- **Set the correct regulatory domain** (`sudo iw reg set US`) before scanning, especially for 6 GHz access.
- **Update Kismet regularly.** The project is actively developed with frequent bugfixes.

### Operational

- **Drive slowly** (15-30 mph). Channel hopping at speed means you may miss APs if moving too fast.
- **Plan systematic routes.** Use Google Maps to plan coverage grids. Avoid driving the same streets repeatedly.
- **Wardrive at different times.** Some APs (mobile hotspots, event venues) are only active at certain times.
- **Back up your data** after every session. Copy `.kismet` and `.wiglecsv` files off the SD card.
- **Monitor GPS lock** before starting. No GPS = no location data = useless wardrive data.

### Data Management

- **Upload to WiGLE regularly.** The community benefits from fresh data, and you get statistics and rankings.
- **Keep raw `.kismet` files** if you want to do deeper analysis later. The WiGLE CSV is a subset.
- **Use descriptive session names** (`-t downtown_2026_06_06`) so you can identify sessions later.
- **Rotate logs** on long wardrives to prevent single files from growing too large.

### Security of Your Own Rig

- **Change default credentials** on RaspAP, Kismet web UI, and SSH.
- **Use SSH key authentication** instead of passwords.
- **Do not expose Kismet's web UI to the internet.** Bind it to localhost or your local network only.
- **Encrypt your SD card** if you are concerned about the data on it.
- **If using RaspAP**, change the default SSID to something inconspicuous and use a strong WPA2 password.

---

## Sources

- [Kismet Wireless Official Site](https://www.kismetwireless.net/)
- [Kismet Wardrive Mode Documentation](https://www.kismetwireless.net/docs/readme/configuring/wardrive/)
- [Kismet Linux WiFi Data Sources](https://www.kismetwireless.net/docs/readme/datasources/wifi-linux/)
- [Kismet Packages / Installation](https://www.kismetwireless.net/packages/)
- [Wardriving Introduction and Kismet 6 GHz -- STACKTITAN](https://rift.stacktitan.com/wardriving-6e-kismet/)
- [Automated Raspberry Pi Wardriving Rig Setup Guide (GitHub Gist)](https://gist.github.com/lukeswitz/435be3ff6607a5c8a53c58e2adc4a222)
- [Raspberry Pi Wardriving Setup -- designer2k2.at](https://www.designer2k2.at/en/mods/elektronik/156-raspberry-pi-wardriving-setup)
- [Felix Kohlhas -- My Wardriving Setup](https://felixkohlhas.com/projects/wardriving/)
- [Th4ntis -- Wardriving Guide](https://cybersec.th4ntis.com/guides-and-how-tos/wardriving)
- [Th4ntis -- RPi Wardriving](https://th4ntis.com/guide/2024/03/06/RPi-Wardriving.html)
- [Best WiFi Adapters for Kali Linux 2026 -- Kennyvn](https://kennyvn.com/best-wireless-adapters-kali-linux/)
- [I Mapped 2.98 Million WiFi Networks -- ringmast4r](https://ringmast4r.substack.com/p/i-mapped-298-million-wifi-networks)
- [Best GPS Modules for Wardriving -- ringmast4r](https://ringmast4r.org/html-roladex/GPS-Comparison)
- [WiGLE: Wireless Network Mapping](https://wigle.net/)
- [WiGLE Tools and Downloads](https://wigle.net/tools)
- [WiGLE Uploads](https://wigle.net/uploads)
- [Kali Linux -- Kismet Tool Page](https://www.kali.org/tools/kismet/)
- [Wardriving Legal Definition -- USLegal](https://definitions.uslegal.com/w/wardriving/)
- [Wardriving Legal Implications -- US Legal Forms](https://legal-resources.uslegalforms.com/w/wardriving)
- [Norton -- What is Wardriving](https://us.norton.com/blog/hacking/wardriving-what-it-is-and-how-to-help-protect-your-network)
- [Wardriving -- Wikipedia](https://en.wikipedia.org/wiki/Wardriving)

---

## 11. Best-Fit Hardware from Your Inventory

### Recommended Build

| Component | Assignment | Why |
|-----------|-----------|-----|
| **Board** | CanaKit Raspberry Pi 5 8GB (with 128GB SD) | Most powerful SBC in inventory. Quad-core Cortex-A76 + 8GB RAM handles real-time packet processing, database writes, and web UI simultaneously. Better USB bandwidth for multiple WiFi adapters |
| **Primary WiFi** | Panda PAU0F AXE3000 WiFi 6E USB 3.0 Adapter | Most capable WiFi adapter in inventory. MT7921A chipset, Kali-compatible. Supports 2.4/5/6 GHz with monitor mode |
| **Secondary WiFi** | RT5370 USB WiFi Dongle | Dedicated 2.4GHz monitor mode adapter for parallel channel hopping |
| **Display** | Hosyond 7" DSI Touchscreen IPS #1 | Dedicated Kismet dashboard. DSI ribbon cable (no HDMI port consumed). IPS for good car-mount viewing angles. Touch for Kismet web UI |
| **Keyboard** | Rii K06 Mini Bluetooth Keyboard #2 | Dedicated to wardriving field kit. Compact for car use. Backlit for nighttime operation |
| **Adapter** | JSAUX Micro HDMI to HDMI Adapter #1 | For Pi 5 HDMI output during setup (DSI handles daily use) |
| **Storage** | 128GB Micro SD (from CanaKit kit) + 32GB USB 3.0 flash drive | SD for OS + kismetdb files. USB for exporting data |
| **Field keyboard** | ProtoArc XK01 TP Foldable Keyboard | Available for extended SSH sessions and config editing |

### Pinout Reference (Raspberry Pi 5)

The Pi 5 uses the standard 40-pin GPIO header (same pinout as Pi 4/3/Zero):

| Function | BCM GPIO | Physical Pin |
|----------|----------|-------------|
| I2C1 SDA | GPIO 2 | Pin 3 |
| I2C1 SCL | GPIO 3 | Pin 5 |
| SPI0 MOSI | GPIO 10 | Pin 19 |
| SPI0 MISO | GPIO 9 | Pin 21 |
| SPI0 SCLK | GPIO 11 | Pin 23 |
| SPI0 CE0 | GPIO 8 | Pin 24 |
| UART TXD | GPIO 14 | Pin 8 |
| UART RXD | GPIO 15 | Pin 10 |

**Interactive pinout:** [pinout.xyz](https://pinout.xyz/) | **Pi 5 docs:** [raspberrypi.com/documentation](https://www.raspberrypi.com/documentation/)

### Missing Components

| Item | Est. Price | Priority |
|------|-----------|----------|
| **GPS Module** (VK-162 or GlobalSat BU-353S4) | ~$15-25 | **High** -- required for geolocation tagging |
| USB-C PD power bank (high capacity) | ~$25-40 | Medium -- for mobile wardriving |

### Upgrade Recommendations

| Component | Upgrade To | Price | Improvement |
|-----------|-----------|-------|-------------|
| WiFi | Alfa AWUS036AXML (WiFi 6E, tri-band) | ~$50-70 | Better 6 GHz support, faster capture rate, better Linux driver support |
| GPS | GlobalSat BU-353S4 | ~$30 | Faster fix time, better sensitivity than budget modules |
| Antenna | 9dBi magnetic-base omni for Panda adapter | ~$12-18 | Extended scan range from vehicle roof |
| Case | Argon NEO 5 with fan | ~$25 | Active cooling prevents thermal throttling during long wardrives |

---

## 12. Cyberdeck Integration

> See [Project 14: Cyberdeck](../14-cyberdeck/) for the full build plan.

### Role in the Cyberdeck

Kismet is the **primary wardriving and wireless reconnaissance tool**, running directly on the Pi 5 (not on an ESP32). It uses the Panda PAU0F and RT5370 WiFi adapters in monitor mode to passively capture all wireless traffic.

### Physical Setup

- **Compute:** Runs on the Pi 5 itself (Kali Linux, pre-installed)
- **Primary WiFi:** Panda PAU0F WiFi 6E → Pi 5 USB 3.0 port #1 (direct, not through hub — needs full bandwidth)
- **Secondary WiFi:** RT5370 → powered USB hub (2.4GHz dedicated monitor)
- **Antenna:** Panda PAU0F antenna → SMA bulkhead #3 (labeled "KISM") via SMA extension cable
- **GPS:** USB GPS module (VK-162) → Pi 5 USB 2.0, shared via `gpsd` daemon
- **Display:** 7" DSI touchscreen shows Kismet web UI at `http://localhost:2501`

### Software Setup on Kali

```bash
sudo apt install kismet gpsd gpsd-clients
sudo usermod -aG kismet $USER
```

Configure `/etc/kismet/kismet.conf`:
```
source=wlan1:name=PandaWiFi6E
source=wlan2:name=RT5370_24GHz
gps=gpsd:host=localhost,port=2947
```

### Dashboard Integration

Kismet exposes a **REST API** at `http://localhost:2501`. The cyberdeck dashboard queries this API to display:
- Live AP count and new network alerts
- Channel activity heatmap
- GPS-tagged network locations
- Client/station associations

### Data Flow

```
Panda PAU0F ──→ Pi 5 (Kismet) ──→ .kismet SQLite DB ──→ WiGLE CSV export
RT5370 ────────→ Pi 5 (Kismet)     └──→ REST API ──→ Cyberdeck Dashboard
USB GPS ───────→ gpsd ─────────────→ Kismet + Dashboard + Flock + Meshtastic
```

All tools share the single GPS feed via `gpsd`.
