# NyanBOX

## Table of Contents

1. [Overview](#1-overview)
2. [Hardware Specs](#2-hardware-specs)
3. [All Included Tools (Stock Firmware)](#3-all-included-tools-stock-firmware)
4. [Setup Guide](#4-setup-guide)
5. [Tool Usage Guides](#5-tool-usage-guides)
6. [Customization](#6-customization)
7. [Integration with Other Tools](#7-integration-with-other-tools)
8. [Use Cases](#8-use-cases)
9. [Legal Considerations](#9-legal-considerations)
10. [Quick Reference Links](#10-quick-reference-links)
11. [When Your Device Arrives -- TL;DR Checklist](#11-when-your-device-arrives----tldr-checklist)

---

## 1. Overview

NyanBOX is a pocket-sized 2.4 GHz wireless security toolkit built on ESP32 architecture, created by developers **jbohack** and **zr_crackiin**. It is described as "a Swiss Army knife for the entire 2.4 GHz spectrum" -- covering WiFi, Bluetooth, BLE, and RF protocols through a fully menu-driven interface that requires zero coding or command-line knowledge.

The device scans, analyzes, and spoofs RF, Wi-Fi, and BLE protocols entirely from its onboard OLED interface. It is positioned as an educational and security research tool for authorized penetration testing, wireless auditing, and personal awareness (such as detecting tracking devices or credit card skimmers).

| Detail | Value |
|---|---|
| **Creators** | jbohack & zr_crackiin (Nyan Devices) |
| **Official site** | [nyandevices.com](https://nyandevices.com/) |
| **Shop** | [shop.nyandevices.com](https://shop.nyandevices.com/products/nyanbox) |
| **Codebase origin** | Fork of cifertech/nRFBox, heavily extended |
| **Language breakdown** | C++ (86.6%), C (12.1%), Python (1.3%) |
| **Price** | $220 USD (Complete Kit) |

---

## 2. Hardware Specs

| Component | Specification |
|---|---|
| **Processor** | ESP32 WROOM-32U, dual-core, 240 MHz |
| **WiFi** | 802.11 b/g/n (2.4 GHz) |
| **Bluetooth** | BLE 4.2 |
| **RF Modules** | 3x NRF24 GTmini modules |
| **Antennas** | 4x 2.4 GHz optimized antennas |
| **Display** | 0.96" OLED, 128x64 pixels |
| **Battery** | 2500 mAh rechargeable LiPo |
| **Runtime** | Full day under typical use |
| **Data/Charge** | USB-C |
| **Debug Interface** | UART |
| **Enclosure** | Protective carrying case included |
| **Variants** | Multicolor or Black case |

### What's in the Complete Kit Box

- Fully assembled nyanBOX device
- Protective carrying case
- Integrated battery (pre-installed)
- 4x 2.4 GHz antennas
- USB-C cable
- Pre-flashed with latest firmware (can be updated via web flasher)

---

## 3. All Included Tools (Stock Firmware)

### WiFi Toolkit (11 tools)

| Tool | Function |
|---|---|
| **WiFi Scanner** | Detects nearby access points with full client detection; view connected clients per network, signal strength, and packet activity |
| **Channel Analyzer** | Visualizes WiFi channel utilization across the 2.4 GHz band |
| **Camera Detector** | Scans for wireless IP cameras across 20+ brands |
| **Camera Deauther** | Disconnects detected wireless cameras from their networks (authorized testing only) |
| **WiFi Deauther** | Sends deauthentication frames to test network resilience |
| **Deauth Scanner** | Detects ongoing deauthentication attacks on nearby networks |
| **Packet Monitor** | Real-time monitoring of 802.11 packet traffic |
| **Beacon Spam** | Broadcasts fake WiFi access point beacons (for testing SSID filtering) |
| **Evil Portal** | Creates captive portals with realistic templates (Google, Facebook, Apple ID, Microsoft, Xfinity); auto-scans nearby networks for SSID spoofing |
| **Pineapple Detector** | Detects Hak5 WiFi Pineapple rogue access points |
| **Pwnagotchi Spam** | Spams Pwnagotchi-style handshake requests |

### Bluetooth / BLE Toolkit (17 tools)

| Tool | Function |
|---|---|
| **BLE Scanner** | Discovers all nearby BLE-advertising devices |
| **BLE Inspector** | Decodes raw BLE advertising packets: service UUIDs, manufacturer data, TX power, flags, raw payloads |
| **nyanBOX Detector** | Discovers other nyanBOX devices nearby; shows level, version, signal strength |
| **Flipper Scanner** | Detects nearby Flipper Zero devices |
| **Axon Detector** | Detects Axon body cameras |
| **Meshtastic Detector** | Finds Meshtastic mesh networking devices |
| **MeshCore Detector** | Finds MeshCore devices |
| **Skimmer Detector** | Detects HC-03, HC-05, and HC-06 Bluetooth modules commonly embedded in credit card skimming devices (gas pumps, ATMs) |
| **AirTag Detector** | Scans for nearby Apple AirTag devices (counter-stalking) |
| **AirTag Spoofer** | Clones and rebroadcasts detected AirTag BLE advertisements; supports selective or bulk spoofing |
| **SmartTag Detector** | Detects Samsung SmartTag trackers |
| **Tile Detector** | Detects Tile Bluetooth trackers |
| **RayBan Detector** | Detects Ray-Ban Meta smart glasses |
| **BLE Spammer** | Floods the BLE advertising space with spam packets |
| **Swift Pair** | Triggers Windows Swift Pair pairing notifications on nearby PCs |
| **Sour Apple** | Triggers persistent pairing popups on Apple devices (iOS/macOS) |
| **Sour Droid** | Triggers persistent pairing popups on Android devices |
| **BLE Spoofer** | Spoofs BLE device advertisements |

### RF / Signal Tools (6 tools)

| Tool | Function |
|---|---|
| **Drone Detector** | Detects drones broadcasting RemoteID via WiFi and BLE; displays drone ID, GPS location, altitude, speed, operator info, flight status; includes locate mode with real-time RSSI meter |
| **Drone Spoofer** | Spoofs drone RemoteID broadcasts |
| **Flock Detector** | Detects multiple drone swarm patterns |
| **Device Scout** | General-purpose 2.4 GHz device discovery |
| **2.4 GHz Scanner** | Scans the full 2.4 GHz spectrum for active signals |
| **Spectrum Analyzer** | Visual spectrum analysis across the 2.4 GHz band |

### System Features

| Feature | Description |
|---|---|
| **RPG Leveling System** | Tracks usage with XP; 9 ranks to progress through; different XP rates for scanning, attacks, and utilities; data persists via EEPROM |
| **Device Lock** | Arrow-key sequence password to lock the device |

---

## 4. Setup Guide

### Step 1: Unboxing and Physical Setup

1. Remove nyanBOX from the protective case
2. Attach all 4x 2.4 GHz antennas to the SMA connectors
3. Flip the power switch to ON (the battery comes pre-charged, but top it off via USB-C)
4. The OLED display should light up with the nyanBOX boot screen

### Step 2: Install USB Drivers (if needed)

- **Windows:** You may need to install the **CP210x USB-to-UART Bridge** drivers from Silicon Labs
  - Download from: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
  - Install, then reboot
- **macOS / Linux:** Drivers are typically built-in; no action needed

### Step 3: Update Firmware via Web Flasher

1. Turn the battery switch **OFF** on the nyanBOX
2. Connect nyanBOX to your PC via USB-C
3. Open a **Chromium-based browser** (Chrome, Edge, Brave, Opera) -- Safari and Firefox do NOT support Web Serial API
4. Navigate to **https://nyandevices.com/flasher/**
5. Click "Install nyanBOX Firmware"
6. Select the correct COM/serial port when prompted
7. Wait for the flash to complete

**Troubleshooting:**

- **Port not appearing:** Install the CP210x drivers above, then unplug/replug
- **Flash fails:** Hold the **BOOT button** (top-right button on device) when the flasher indicates, keep holding until it says to release
- **Still stuck:** Join the Discord for help: https://discord.gg/J5A3zDC2y8

### Step 4: Navigate the Interface

- Use the **arrow buttons** to scroll through menus
- Press the **select/enter button** to choose a tool
- Press **back** to return to the previous menu
- The interface is entirely menu-driven -- no typing or CLI needed

### Step 5: First Run Checklist

1. Navigate to the WiFi Scanner and verify it detects your own access point
2. Try the BLE Scanner to see nearby Bluetooth devices
3. Check the Spectrum Analyzer to see 2.4 GHz activity around you
4. Note your level and rank in the RPG system

---

## 5. Tool Usage Guides

### WiFi Reconnaissance

**WiFi Scanner:**
Navigate to WiFi > Scanner. The device will scan all 2.4 GHz channels and list discovered access points with SSID, BSSID, channel, signal strength (RSSI), and encryption type. Select any AP to see its connected clients. Use this for network mapping during authorized assessments.

**Channel Analyzer:**
Navigate to WiFi > Channel Analyzer. Displays a real-time bar graph of signal density per channel (1-13). Useful for identifying congestion and finding clear channels for your own networks.

**Packet Monitor:**
Navigate to WiFi > Packet Monitor. Shows real-time packet counts and types flowing on the selected channel. Useful for understanding traffic patterns and detecting anomalies.

### Evil Portal (Credential Capture Testing)

Navigate to WiFi > Evil Portal. Select a template (Google, Facebook, Apple ID, Microsoft, Xfinity). The device creates a rogue access point with a captive portal that mimics the selected login page. When a test subject connects and enters credentials, they are logged on the device.

**Only use this on networks/devices you own or have written authorization to test.**

### WiFi Deauthentication Testing

Navigate to WiFi > WiFi Deauther. First scan for APs, select the target AP (must be one you own or have authorization to test), then initiate. The device sends 802.11 deauthentication frames, disconnecting clients. Use this to test whether your network's management frame protection (802.11w/PMF) is working.

### BLE Reconnaissance

**BLE Scanner:**
Navigate to BLE > Scanner. Lists all BLE-advertising devices within range with name, MAC address, RSSI, and advertisement type.

**BLE Inspector:**
Navigate to BLE > Inspector. Select a discovered device to decode its raw advertisement payload: service UUIDs, manufacturer-specific data, TX power level, and flags.

### Tracker Detection (Counter-Surveillance)

**AirTag Detector:**
Navigate to BLE > AirTag Detector. The device scans for Apple's proprietary BLE advertisements used by AirTags. If someone has planted an AirTag on your person, vehicle, or belongings, this will find it -- even if you don't have an iPhone.

**SmartTag / Tile / RayBan Detectors:**
Same workflow. Each detector is tuned to the specific BLE advertising format of its respective tracker brand.

### Skimmer Detection

Navigate to BLE > Skimmer Detector. The device scans for HC-03, HC-05, and HC-06 Bluetooth serial modules. These cheap modules are commonly wired into card skimmers at gas pumps and ATMs to wirelessly exfiltrate stolen card data. If you detect one of these modules at a gas pump, do not use that pump and report it.

### Drone Detection

Navigate to RF > Drone Detector. The device listens for RemoteID broadcasts (mandatory in many jurisdictions since 2023) over both WiFi and BLE. Detected drones show: serial number, GPS coordinates, altitude, speed, heading, operator location, and flight status. Use the **Locate Mode** to track a drone's direction via real-time RSSI signal strength metering.

### BLE Disruption Testing

**Sour Apple / Sour Droid / Swift Pair:**
These tools send crafted BLE pairing requests that trigger persistent popup notifications on Apple, Android, and Windows devices respectively. Useful for testing whether your devices are vulnerable to BLE notification spam.

**Only test on your own devices.**

### Spectrum Analysis

Navigate to RF > Spectrum Analyzer. Provides a real-time visual waterfall/graph of all 2.4 GHz energy. Useful for identifying interference sources, locating hidden transmitters, and characterizing the RF environment.

---

## 6. Customization

### Alternative Firmware: nyanBEE Community Edition

**nyanBEE** (by CK42X) is a free community firmware that sits on top of the nyanBOX hardware and dramatically extends its capabilities. Current version: v2.0.12.

**Installation:** Flash via browser at https://www.ck42x.com/nyanbee (same Web Serial process as stock firmware). Verify SHA-256 hash before flashing.

**What nyanBEE adds beyond stock (85 total menu entries vs stock ~34):**

| Category | Added Capabilities |
|---|---|
| **WiFi** | WPA Handshake/PMKID capture, Evil Twin attacks, 19 Evil Portal templates (vs stock 5), Deauth Guardian (defensive), Traffic/Packet/Probe loggers, Wardriving mode, Hidden network reveal, Rogue AP detection, WiFi Graffiti |
| **BLE** | HoneyBLE lab modes, BLE MITM, Tracker Sweep (all trackers at once), AIO Find Mode (counter-surveillance) |
| **RF/NRF24** | MouseJack (wireless keyboard/mouse injection), Replay Attack, Stinger (targeted jamming), Morse beacon |
| **Workflow** | Mission Mode (Recon/Red Team/Blue Team presets), Session logging, Engagement reports (HTML/JSON export), Achievement gallery |
| **SIGINT** | HiveMind dashboard (phone-accessible spectrum stats), SigWatch (tag and compare signal signatures across locations), Anomaly Watch |
| **Games** | 9 arcade titles (Snake, Signal Wars, HivePet, etc.) |
| **Platform** | OTA updates, Bee Level System (separate from stock RPG) |

**Switching between firmwares:** You can freely flash back and forth between stock nyanBOX and nyanBEE. Just use the respective web flasher for each.

### Hardware Mods

- The ESP32 WROOM-32U uses an external antenna connector (U.FL/IPEX to SMA), so you can attach higher-gain directional antennas for extended range
- UART pins are exposed for serial debugging and custom firmware development
- The source code is C++/C, so developers can fork the GitHub repo and add custom tools

---

## 7. Integration with Other Tools

### With Flipper Zero

NyanBOX and Flipper Zero are complementary, not competitive:

- **Flipper Zero** excels at: Sub-GHz (garage doors, key fobs), NFC/RFID, infrared, BadUSB, GPIO
- **NyanBOX** excels at: 2.4 GHz spectrum (WiFi, BLE, NRF24 protocols)
- NyanBOX includes a **Flipper Scanner** that detects nearby Flipper Zero devices
- Together they cover the full wireless spectrum from sub-1 GHz through 2.4 GHz

### With Pwnagotchi

- NyanBOX includes a **Pwnagotchi Detector** to find nearby Pwnagotchi devices
- Also has **Pwnagotchi Spam** for testing
- nyanBEE firmware adds WPA handshake capture, overlapping with Pwnagotchi's core function

### With Hak5 WiFi Pineapple

- NyanBOX's **Pineapple Detector** identifies rogue Pineapple access points
- The Evil Portal feature provides similar (though lighter-weight) captive portal capabilities
- NyanBOX is more portable; Pineapple is more powerful for sustained engagements

### With Wireshark / Network Analysis

- NyanBOX's Packet Monitor and WiFi Scanner provide on-device recon
- nyanBEE's handshake capture files can be exported and cracked with hashcat/aircrack-ng on a full PC
- Use nyanBOX for field recon, then process captures on your workstation

### With Meshtastic / MeshCore

- Built-in detectors for both Meshtastic and MeshCore mesh networking devices
- Useful for mapping mesh network deployments during physical security assessments

### With Kali Linux / Parrot OS

- NyanBOX handles standalone field recon where a laptop would be conspicuous
- Captured data (especially with nyanBEE's engagement reports in HTML/JSON) can be imported into your pentesting workstation for further analysis

---

## 8. Use Cases

### Authorized Penetration Testing

- WiFi network auditing (deauth resilience, rogue AP detection, client enumeration)
- BLE device discovery and attack surface mapping
- Evil Portal credential capture testing (social engineering assessment)
- Wireless camera security auditing

### Physical Security Assessments

- Sweep a facility for unauthorized wireless cameras
- Detect rogue access points and WiFi Pineapples
- Map all wireless devices in a target environment
- Drone surveillance detection and tracking
- Detect body cameras (Axon) and smart glasses (Ray-Ban Meta)

### Personal Security and Counter-Surveillance

- **Anti-stalking:** Detect AirTags, SmartTags, and Tile trackers planted on your person, vehicle, or belongings
- **ATM/gas pump safety:** Scan for credit card skimmer Bluetooth modules before inserting your card
- **Drone awareness:** Know when drones are operating near your location
- **Hidden camera detection:** Sweep hotel rooms, Airbnbs, changing rooms for wireless cameras

### Red Team Operations

- Portable, inconspicuous form factor for field work
- No laptop required for initial wireless recon
- Evil Portal for social engineering tests
- BLE disruption testing (Sour Apple/Droid/Swift Pair)
- Drone spoofing for testing drone detection systems
- nyanBEE adds MouseJack for wireless keyboard injection attacks

### Blue Team / Defensive

- Detect deauthentication attacks in progress (Deauth Scanner)
- Detect rogue APs and Pineapples on your network
- Monitor for unauthorized BLE devices in secure areas
- nyanBEE's Deauth Guardian mode for active defense
- Continuous spectrum monitoring for anomalous signals

### Education and Research

- Learn 802.11 protocol fundamentals hands-on
- Understand BLE advertising and pairing mechanisms
- Visualize the 2.4 GHz spectrum in real-time
- Study wireless attack and defense techniques in a controlled lab

### Wardriving (nyanBEE firmware)

- Map WiFi access points while moving through an area
- Log SSIDs, BSSIDs, encryption types, signal strength, and GPS coordinates
- Build coverage maps of wireless infrastructure

---

## 9. Legal Considerations

### Device Ownership

NyanBOX is **legal to own** in most jurisdictions. It is a general-purpose ESP32 development platform with radio modules. Possessing the device is not illegal.

### Usage Restrictions (Critical)

The legality depends entirely on **how you use it**.

**Generally Legal (most jurisdictions):**

- Passive scanning and spectrum analysis
- Detecting trackers on your own property/person (AirTags, SmartTags, Tiles)
- Scanning for skimmers at gas pumps/ATMs
- Testing your own WiFi networks and devices
- Educational use in a controlled lab environment
- Drone detection (passive listening for RemoteID)

**Requires Authorization (written permission mandatory):**

- WiFi deauthentication on any network you do not own
- Evil Portal deployment on any network
- Any form of credential capture
- BLE spoofing/spamming targeting other people's devices
- Drone spoofing
- MouseJack attacks (nyanBEE)
- Any penetration testing on third-party infrastructure

**Potentially Illegal (jurisdiction-dependent):**

- Deauthentication attacks are illegal in the US under the Computer Fraud and Abuse Act (CFAA) and FCC regulations (intentional interference with radio communications) when performed without authorization
- Evil Portal credential capture without authorization = wire fraud and/or identity theft
- AirTag spoofing could implicate you in stalking-related offenses if misused
- Drone spoofing may violate FAA regulations and federal aviation law
- Jamming (nyanBEE's Stinger) is illegal under FCC Part 15 in the US and similar regulations internationally -- even on your own property
- BLE spam attacks (Sour Apple/Droid) targeting strangers' devices may constitute harassment or unauthorized access

### Key Regulations by Region

| Region | Key Laws |
|---|---|
| **USA** | CFAA (18 U.S.C. 1030), FCC Part 15 (47 CFR 15), Wiretap Act, state computer crime statutes |
| **EU** | GDPR (data capture), Computer Misuse regulations per member state, Radio Equipment Directive |
| **UK** | Computer Misuse Act 1990, Wireless Telegraphy Act 2006 |
| **Canada** | Criminal Code s.342.1, Radiocommunication Act |
| **Australia** | Radiocommunications Act 1992, Criminal Code Act 1995 |

### Best Practices

1. **Always** obtain written authorization before testing any network or device you do not own
2. **Never** use jamming features outside a Faraday cage or shielded lab
3. **Document** your scope and authorization for every engagement
4. Keep a copy of your authorization letter/contract on your person during field work
5. Understand that "educational purposes" is not a legal defense if you cause harm or access unauthorized systems
6. The nyanBOX manufacturers state the device is "intended solely for educational, research, testing, and personal development purposes" -- this is a liability disclaimer, not legal protection for you

---

## 10. Quick Reference Links

| Resource | URL |
|---|---|
| **Official Website** | https://nyandevices.com/ |
| **Purchase** | https://shop.nyandevices.com/products/nyanbox |
| **GitHub (source)** | https://github.com/jbohack/nyanBOX |
| **Web Flasher (stock firmware)** | https://nyandevices.com/flasher/ |
| **nyanBEE Community Firmware** | https://www.ck42x.com/nyanbee |
| **Discord Community** | https://discord.gg/J5A3zDC2y8 |
| **CP210x USB Drivers** | https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers |
| **Setup Video Tutorial** | https://www.youtube.com/watch?v=hJjEluLOBXg |
| **Firmware Overview Video** | https://www.youtube.com/watch?v=MSSw1mUMdss |
| **Frank's World Review** | https://www.franksworld.com/2025/11/24/why-nyanbox-is-the-hacking-tool-everyones-talking-about/ |

---

## 11. When Your Device Arrives -- TL;DR Checklist

1. Unbox, attach all 4 antennas, charge via USB-C
2. Install CP210x drivers on your Windows PC ([silabs.com](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers))
3. Flash latest firmware: [nyandevices.com/flasher](https://nyandevices.com/flasher/) (Chrome/Edge only)
4. Consider flashing nyanBEE for 2.5x more tools: [ck42x.com/nyanbee](https://www.ck42x.com/nyanbee)
5. Join the [Discord](https://discord.gg/J5A3zDC2y8) for community support and firmware update notifications
6. Start with passive tools first (WiFi Scanner, BLE Scanner, Spectrum Analyzer) to learn the interface
7. Only use active/offensive tools on your own equipment or with written authorization

---

## Standalone Build Guide

Pre-built 2.4GHz wireless security toolkit -- arrives ready to use.

1. Purchase NyanBOX kit (~$220, includes board + antennas + case)
2. Unbox and connect USB-C power
3. NyanBOX boots into its own menu system -- no flashing needed
4. Connect external antenna for better range (RP-SMA port on board)
5. Use standalone for WiFi scanning, deauth testing, beacon spam
6. Compare results with ESP32 Marauder for cross-validation
7. Good as a backup/redundant scanner if primary Marauder boards fail

> **Note:** NyanBOX is largely redundant with the cyberdeck's 3 Gold + 2 C5 boards.

---

## Feature Brainstorm -- What Else Can This Do

- **MouseJack wireless keyboard injection** -- Flash the nyanBEE community firmware to unlock NRF24-based MouseJack attacks. The NyanBOX's three NRF24 GTmini modules can sniff and inject keystrokes into unencrypted wireless keyboards and mice during authorized physical security assessments.
- **Spectrum analysis for finding hidden wireless devices** -- Use the built-in Spectrum Analyzer to sweep rooms, offices, or vehicles for unexpected 2.4 GHz transmitters (hidden cameras, rogue APs, planted bugs) that would not appear in a standard WiFi scan.
- **BLE proximity monitoring with tracker sweep** -- Run the AirTag, SmartTag, and Tile detectors in sequence (or nyanBEE's Tracker Sweep for all at once) as a portable counter-surveillance sweep tool when entering a new vehicle, hotel room, or meeting space.
- **WiFi channel congestion analysis for site surveys** -- Use the Channel Analyzer during wireless site assessments to identify which 2.4 GHz channels are overloaded, recommending optimal channel assignments for the target network.
- **Cross-validation scan results with ESP32 Marauder** -- Run the same WiFi/BLE reconnaissance with both NyanBOX and your Marauder-flashed ESP32 boards to compare detection results, validating scan completeness and identifying any devices one tool misses.
- **NRF24 sniffer mode for custom protocol analysis** -- Use the NRF24 modules to sniff non-WiFi, non-Bluetooth 2.4 GHz protocols (baby monitors, wireless sensors, proprietary IoT devices) for security research on custom RF implementations.
- **Custom SSID lists for targeted beacon spam testing** -- Create curated SSID lists mimicking specific target environments (corporate networks, government SSIDs) for authorized Evil Twin and beacon spam testing during red team engagements.
- **Portable RF survey tool for physical site assessments** -- Combine the WiFi Scanner, BLE Scanner, Spectrum Analyzer, and Drone Detector into a single walk-through survey workflow, documenting the complete 2.4 GHz RF environment of a facility in one pass.
- **Deauth detection for defensive monitoring** -- Deploy the Deauth Scanner in continuous mode on your home or office network to alert you when someone is actively running deauthentication attacks against your infrastructure.
- **Pwnagotchi and Pineapple detection for blue team sweeps** -- Use the built-in Pwnagotchi and Pineapple detectors during physical security patrols to identify if any unauthorized offensive tools are operating within your facility.

---

## 12. Best-Fit Hardware from Your Inventory

### Status: In Transit -- Pre-Built Kit

NyanBOX arrives as a self-contained unit. **No board from your inventory needs to be allocated.** The kit includes its own ESP32, antennas, and OLED display.

### From Your Inventory (Optional Accessories)

| Component | Use |
|-----------|-----|
| KOOTION 16GB Micro SD Card | If the kit requires one |
| USB power bank | Extended portable operation |
