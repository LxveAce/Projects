# Flipper Zero -- Comprehensive Guide

> Last updated: June 2026

---

## Table of Contents

1. [Overview and Built-In Capabilities](#1-overview-and-built-in-capabilities)
2. [ESP32 Add-On: AWOK Dynamics Dual C5 Touch](#2-esp32-add-on-awok-dynamics-dual-c5-touch)
3. [Custom Firmware Comparison](#3-custom-firmware-comparison)
4. [Complete Setup from Unboxing](#4-complete-setup-from-unboxing)
5. [Must-Have Apps](#5-must-have-apps)
6. [Legal Considerations](#6-legal-considerations)
7. [Pricing and Where to Buy](#7-pricing-and-where-to-buy)
8. [Sources](#sources)

---

## 1. Overview and Built-In Capabilities

### What Is Flipper Zero?

Flipper Zero is a portable, open-source multi-tool designed for interaction with access control systems, radio protocols, hardware, and digital interfaces. Created by Alex Kulagin and Pavel Zhovner in 2019, it launched via Kickstarter in August 2020, raising $4.8 million. The device features a pixel-art dolphin virtual pet that evolves as you use the device's features -- the more you explore, the happier your dolphin becomes.

The firmware runs on FreeRTOS, written primarily in C/C++, with the architecture split into FuriCore (scheduler/multithreading), FuriHal (hardware abstraction), and modular services/applications. The hardware design is open-source under GPL (schematics published; PCB layouts remain proprietary).

### Hardware Specifications

| Specification | Detail |
|---|---|
| **MCU** | STM32WB55RG (dual-core ARM) |
| **Application Processor** | ARM Cortex-M4, 32-bit, 64 MHz |
| **Radio Processor** | ARM Cortex-M0+, 32-bit, 32 MHz |
| **Flash Memory** | 1024 KB (shared between cores) |
| **SRAM** | 256 KB (shared between cores) |
| **Display** | 1.4" monochrome LCD, 128x64 px, ST7567 controller (SPI) |
| **Battery** | 2100 mAh LiPo, up to 28 days standby |
| **Dimensions** | 100.3 x 40.1 x 25.6 mm (3.95 x 1.58 x 1.01 in) |
| **Weight** | 102 g (3.6 oz) |
| **Materials** | PC, ABS, PMMA |
| **USB** | Type-C, USB 2.0, 12 Mbps, 1A max charging |
| **MicroSD** | Up to 256 GB (2-32 GB recommended), SPI, ~5 Mbps R/W |
| **GPIO** | 13 I/O pins, 2.54mm connectors, 3.3V CMOS, 5V tolerant, 20 mA/pin |
| **Buzzer** | 100-2500 Hz, 87 dB |
| **Vibration Motor** | 30N force, 13,500 RPM |
| **Operating Temp** | 0-40C (32-104F) |
| **Controls** | 5-position D-pad + back button |

### Hardware Architecture (4 PCB Modules)

1. **Main Board** -- STM32WB55 processor, Sub-GHz radio (CC1101), Bluetooth antenna, LCD, GPIO pins, USB-C port
2. **Infrared/iButton PCB** -- IR receiver, three IR LEDs, buzzer, iButton connector
3. **NFC PCB** -- ST25R3916 NFC chip + 125 kHz RFID circuitry
4. **Antenna PCB** -- Dual passive coil antennas (13.56 MHz + 125 kHz)

### Built-In Capabilities (All 8 Radios/Interfaces)

#### Sub-GHz Radio

- **Transceiver:** Texas Instruments CC1101
- **TX Power:** Up to 20 dBm
- **Frequency Bands:** 315, 433, 868, 915 MHz (300-928 MHz range)
- **What it does:** Reads, records, and retransmits radio signals from devices like garage door openers, car key fobs (static codes only), wireless doorbells, weather stations, remote-controlled outlets, and smart home sensors
- **What it cannot do:** Cannot break rolling codes out of the box (modern garage doors and cars use rolling codes that change with every press). Official firmware blocks restricted frequencies and unsafe transmissions
- **Protocols:** AM, FM, OOK modulation; supports dozens of protocols including Princeton, CAME, Nice, Chamberlain, Linear, and many more

#### NFC (13.56 MHz)

- **Transceiver:** ST25R3916
- **Frequency:** 13.56 MHz
- **Standards:** ISO 14443A/B, NXP MIFARE (Classic, Ultralight, DESFire), FeliCa, HID iClass
- **What it does:** Reads NFC cards and tags, emulates NFC cards, writes data to blank NFC tags, analyzes NFC data formats. Useful for backing up transit cards, access badges, and experimenting with NFC automation
- **What it cannot do:** Cannot clone cards with strong encryption (e.g., MIFARE DESFire EV2/EV3 with diversified keys, bank cards with EMV)

#### RFID (125 kHz)

- **Frequency:** 125 kHz (Low Frequency)
- **Modulation:** AM, OOK
- **Coding:** ASK, PSK
- **What it does:** Reads, saves, and emulates older LF access cards and tags (EM4100, HID Prox, Indala, AWID, Viking, Paradox, etc.)
- **What it cannot do:** Cannot read/clone higher-security HF cards via this module (that is NFC territory). Limited to passive 125 kHz tags

#### Infrared (IR)

- **RX:** 950 nm (+/- 100 nm), 38 kHz carrier
- **TX:** 940 nm, 0-2 MHz carrier, 300 mW power
- **What it does:** Acts as a universal remote control. Comes with a large built-in database of IR codes for TVs, AC units, projectors, soundbars, set-top boxes, and more. Can learn and record new IR signals from existing remotes. 2026 firmware update expanded the IR library significantly
- **What it cannot do:** Line-of-sight only; limited range (~10-15 meters depending on conditions)

#### iButton (1-Wire)

- **Protocols:** Dallas DS1990A, Cyfral, Metakom
- **What it does:** Reads and emulates 1-Wire contact keys commonly used in apartment intercoms and older access control systems (common in Eastern Europe and Russia)
- **Connector:** Built into the bottom edge of the device

#### GPIO (General Purpose I/O)

- **Pins:** 13 I/O pins on external 2.54mm header
- **Logic:** 3.3V CMOS, 5V tolerant inputs, 20 mA per pin
- **What it does:** Connects to external hardware -- expansion boards (WiFi dev board, ESP32 modules), electronic components, UART serial consoles, SPI/I2C devices. Enables hardware hacking, debugging, and interfacing with microcontrollers
- **Expansion modules connect here:** WiFi boards, SubGHz range extenders, video game module, etc.

#### USB (Type-C)

- **Standard:** USB 2.0, 12 Mbps
- **What it does:** Charges the device (1A max), firmware flashing via qFlipper desktop app, file transfer to/from microSD, BadUSB attacks (HID keyboard/mouse emulation using DuckyScript), U2F second-factor authentication hardware key
- **BadUSB:** Emulates a keyboard to execute pre-written DuckyScript payloads on connected computers -- used legitimately for penetration testing and automating tasks

#### Bluetooth Low Energy (BLE)

- **Version:** 5.4
- **TX Power:** 4 dBm max
- **RX Sensitivity:** -96 dBm
- **Data Rate:** 2 Mbps
- **What it does:** Connects to the Flipper mobile app (iOS/Android) for remote control, file transfer, firmware updates, and real-time diagnostics. Scans for nearby BLE devices, shows identifiers, signal strength, and broadcasting patterns
- **Mobile app features (2026):** Real-time diagnostics, device management, file browsing, firmware updates, remote trigger

---

## 2. ESP32 Add-On: AWOK Dynamics Dual C5 Touch

### Overview

The Dual C5 Touch is an advanced WiFi/BLE expansion board made by AWOK Dynamics that plugs into the Flipper Zero's GPIO header, adding dual-band WiFi capabilities, a touchscreen interface, and GPS -- all in one module. It is purpose-built for WiFi wardriving and network auditing.

### Specifications

| Specification | Detail |
|---|---|
| **Price** | $170.00 USD (awokdynamics.com) / ~EUR 160 (Lab401, EU) |
| **Availability** | Frequently sold out; restocks announced via Discord/Email/Instagram |
| **Processor** | Dual ESP32-C5-WROOM chips on a single board |
| **WiFi** | Dual-band 2.4 GHz + 5 GHz |
| **Antennas** | Two external 2.4/5 GHz antennas included |
| **GPS** | Dual-band L1/L5 GNSS, 4 constellations, Airoha 3335 LNA chip |
| **GPS Antenna** | Internal ceramic antenna (pre-installed) |
| **Display** | Touchscreen (controlled by one ESP32) |
| **Case** | Clear injection-molded plastic, optional SMA antenna mount hole |
| **RTC** | Real-time clock with coin-cell battery for rapid GPS startup |
| **Configuration** | DIP switch for engagement customization |

### How It Works

- **ESP32 #1:** Controls the touchscreen UI, runs wardriving/scanning operations
- **ESP32 #2:** Accessible via CLI or GPIO pins for parallel tasks. Both chips can communicate with the GPS module simultaneously
- Connects to Flipper Zero via the GPIO header pins
- No firmware pre-installed -- user must flash firmware

### WiFi Capabilities

- **AP Scanning:** Detect and enumerate nearby WiFi networks (SSIDs, encryption type, channel, signal strength)
- **Station Monitoring:** Track connected client devices
- **Beacon Operations:** Custom SSID broadcasting, probe request sniffing
- **Deauthentication:** Send deauth frames for authorized penetration testing
- **Evil Portal:** Create captive portal pages for social engineering assessments
- **Evil Twin Detection:** Detect WiFi Pineapples and rogue access points
- **WiFi Capture:** Log probe requests, beacon frames, deauth packets, raw 802.11 data
- **Wardriving:** GPS-timestamped network mapping, compatible with WiGLE.net uploads
- **Pineapple Detection:** Identify WiFi Pineapples and Evil Twin attacks on your network
- **Web Interface:** Built-in browser-based UI for settings management

### BLE Capabilities

- BLE device scanning with specialized modes (AirTags, Flipper Zeros, generic BLE)
- Packet capture and traffic analysis
- Device spoofing/spam functionality
- GPS-stamped BLE wardriving and device mapping

### Installation

1. Power off your Flipper Zero
2. Align the Dual C5 Touch board with the GPIO header pins on top of the Flipper
3. Press down firmly to seat the board
4. Attach the two external 2.4/5 GHz antennas
5. Flash firmware using one of these methods:
   - **C5 Py Flasher** (Python-based flashing tool)
   - **ESP Terminator** (espterminator.com -- browser-based flasher via Google Chrome)
   - **Biscuit firmware** via the orange port
   - **KOKOs firmware** for alternative functionality
6. If the touchscreen scrolls randomly, loosen the back screws slightly; check case interior for molding imperfections

### Firmware Options for the Dual C5 Touch

- **General wardriving firmware** -- optimized for classical WiFi/BLE collection
- **Passive assessment firmware** -- data collection only, no transmission
- **Offensive engagement firmware** -- Evil Portal, deauth, Evil Twin capabilities
- STL files available for custom 3D-printed cases

### What's In the Box

- 1x Dual C5 Touch PCB
- 1x Clear case with optional SMA antenna mount hole
- 2x External 2.4/5 GHz antennas
- 1x Internal ceramic GPS antenna (pre-installed)
- 1x GPIO protective cover

**Note:** The Dual C5 Touch is designed for network monitoring and educational/experimental purposes. It is receive-focused by design (not a high-power transmitter). AWOK also sells the simpler ESP32 v5 board for those who do not need the touchscreen or dual-chip architecture.

---

## 3. Custom Firmware Comparison

### Quick Summary Table

| Feature | Official (OFW) | Momentum | Unleashed | RogueMaster |
|---|---|---|---|---|
| **Status** | Active, stable | Active, stable | Active, stable | Active |
| **Base** | Stock | OFW + Unleashed features | OFW fork | Unleashed + former Xtreme |
| **Regional Frequency Lock** | YES (locked) | REMOVED | REMOVED | REMOVED |
| **Rolling Code Support** | No | Yes (TX capable) | Yes | Yes |
| **UI Customization** | Minimal | Extensive (8 menu styles, asset packs, RGB) | Minimal | Moderate |
| **BLE Spam Tools** | No | Yes | Yes | Yes |
| **BadUSB/BadKB** | Basic DuckyScript | Enhanced + Find My BadKB | Enhanced | Enhanced + complex patterns |
| **Preinstalled Apps** | ~30 | 183+ | ~50+ | ~100+ |
| **SubGHz Protocols** | Standard set | Extended (weather, POCSAG, TPMS) | Extended | Extended |
| **NFC Enhancements** | Standard | Type 4 (NDEF), EMV | Enhanced | Enhanced |
| **GPS/Subdriving** | No | Yes | No | No |
| **Update Method** | qFlipper / mobile app | Web updater + qFlipper | Manual .dfu flash | Manual flash |
| **Signed Updates** | Yes | Yes (OTA via qFlipper) | No rollback protection | No |
| **Community Size** | Largest (official) | Large, growing fast | Large, established | Medium |

### Xtreme Firmware (DISCONTINUED)

Xtreme firmware ceased development on November 19, 2024. The same core developers went on to create Momentum. Users still on Xtreme should migrate to Momentum (direct successor) or Unleashed.

### Detailed Breakdown

#### Official Firmware (OFW)

- **Best for:** Absolute beginners, first 1-2 weeks of ownership, users who want guaranteed stability
- **Pros:** Most stable, officially supported, automatic updates via qFlipper and mobile app, access to the official App Hub (lab.flipper.net), no risk of bricking, FCC/regulatory compliant
- **Cons:** Regional frequency restrictions enforced, no rolling code support, limited advanced features, fewer preinstalled apps
- **Update frequency:** Regular official releases

#### Momentum Firmware (Recommended for Most Users)

- **Best for:** Users who want the best balance of features, stability, and customization
- **Unique features:**
  - Asset Packs: Install custom animations, icons, and fonts without recompiling firmware
  - 8 main menu styles + Control Center with quick toggles
  - FindMy tracking (auto-enabled at startup)
  - Subdriving (GPS-tagged SubGHz signal mapping)
  - Enhanced JavaScript support (USBDisk, Storage, GUI, BLE, SubGHz modules)
  - Boot lock + reset on failed PIN attempts
  - RGB backlight modes including rainbow customization
  - Device spoofing (name, MAC, serial)
  - Momentum Settings app for comprehensive configuration
  - 183+ preinstalled external apps
- **Current stable:** mntm-012 (December 31, 2025), with frequent dev builds (latest June 2, 2026)
- **Install:** momentum-fw.dev/update (web-based updater)
- **GitHub:** github.com/Next-Flip/Momentum-Firmware

#### Unleashed Firmware

- **Best for:** RF-focused penetration testers, users who want minimal UI changes with maximum functional improvements
- **Unique features:**
  - Regional restriction removal for all frequency bands
  - Rolling code protocol support for dynamic security systems
  - Enhanced battery life optimization and faster BLE connections
  - Community plugins: frequency analyzers, RFID fuzzers
  - Minimal interface changes from stock (feels familiar)
- **Cons:** Manual .dfu flashing required, no rollback protection, fewer UI customization options
- **Install:** Manual flash via qFlipper with .dfu file from GitHub releases

#### RogueMaster Firmware

- **Best for:** Power users who want everything combined, tinkerers
- **Unique features:**
  - Merges best features from Unleashed + former Xtreme
  - DUMB Mode for simplified interface
  - Custom animations and extensive visual customization
  - Strong BadUSB enhancements with complex attack patterns
- **Cons:** Less stable than Momentum or Unleashed, larger firmware size, may have more bugs

### Firmware Recommendation Flow

1. **Just unboxed?** -- Start with Official for 1-2 weeks to learn the basics
2. **Want more features + customization?** -- Switch to Momentum
3. **Focused on RF pentesting?** -- Consider Unleashed
4. **Want to tinker with everything?** -- Try RogueMaster
5. **Currently on Xtreme?** -- Migrate to Momentum immediately (same developers)

---

## 4. Complete Setup from Unboxing

### What's In the Box

- 1x Flipper Zero device
- 1x USB-C to USB-A cable
- Documentation card
- Sticker

### You Will Also Need (Not Included)

- MicroSD card (4-32 GB recommended, FAT32 formatted)
- Computer with qFlipper installed (for firmware management)
- Flipper mobile app (iOS/Android) for BLE connectivity

### Step-by-Step Setup

**Step 1: Insert MicroSD Card**

- Open the microSD slot on the left side of the device
- Insert the card with the chip side facing UP
- Push until it clicks into place

**Step 2: Power On**

- Hold the BACK button for 3 seconds to power on
- The dolphin pet will appear and guide you through initial setup
- Select your language and time zone

**Step 3: Update Firmware**

- Download and install qFlipper on your computer (flipperzero.one/update)
- Connect Flipper Zero via USB-C cable
- qFlipper will detect the device and prompt you to update to the latest official firmware
- Click "Update" and wait for the process to complete (do NOT disconnect during update)

**Step 4: Install Flipper Mobile App**

- Download "Flipper Mobile App" from iOS App Store or Google Play
- Open the app and pair with your Flipper via Bluetooth
- This enables remote control, file transfer, and wireless firmware updates

**Step 5: Explore the Menus**

- Use the D-pad to navigate; center button to select; back button to go back
- Main sections: Sub-GHz, 125 kHz RFID, NFC, Infrared, iButton, BadUSB, GPIO, Settings
- The dolphin pet levels up as you use different features

**Step 6 (Optional): Install Custom Firmware**

- If switching to Momentum: visit momentum-fw.dev/update in a browser, connect Flipper via USB, follow web updater prompts
- If switching to Unleashed: download .dfu from GitHub releases, flash via qFlipper's "Install from file" option

**Step 7 (Optional): Install Dual C5 Touch ESP32 Board**

- Power off the Flipper
- Seat the board onto the GPIO header
- Attach external antennas
- Flash ESP32 firmware via C5 Py Flasher or espterminator.com (Chrome browser)

---

## 5. Must-Have Apps

### Utility / Core

- **Infrared Remote** -- Universal remote with massive 2026-expanded IR database. Control TVs, ACs, projectors, soundbars
- **Sub-GHz Scanner** -- Detect and analyze nearby Sub-GHz devices (doorbells, sensors, smart home equipment)
- **NFC Tools / RFID Explorer** -- Read, write, and emulate NFC/RFID tags with improved 2026 card compatibility
- **File Browser** -- Manage saved signals, backups, scripts on the microSD card (2026 version has better navigation)
- **BadUSB** -- Run DuckyScript payloads for authorized penetration testing and automation

### Network / WiFi (Requires ESP32 Board)

- **WiFi Marauder** -- WiFi scanning, deauth, packet capture (classic ESP32 firmware)
- **Evil Portal** -- Captive portal for social engineering assessments
- **Wardriving apps** -- GPS-tagged network mapping with WiGLE.net export

### Learning / Exploration

- **Bluetooth Signal Finder** -- Discover nearby BLE devices, analyze signal strength patterns
- **Smart Meter Monitor** -- Educational tool for understanding smart home wireless activity
- **Spectrum Analyzer** -- Visualize radio frequency activity across Sub-GHz bands

### Fun / Entertainment

- **Flipper Music Player** -- Play melodies through the internal buzzer
- **Games** -- Tetris, Snake, 2048, Doom, and many more via the App Hub
- **Script Runner** -- Run simple automations and repeated task sequences

### Where to Find Apps

- **Official App Hub:** lab.flipper.net/apps (for official firmware)
- **Momentum:** 183+ apps preinstalled; additional apps via the built-in app manager
- **GitHub:** github.com/djsime1/awesome-flipperzero (curated community list)

---

## 6. Legal Considerations

### General Principle

**Legality depends on USE, not possession.** No country currently bans mere ownership of a Flipper Zero. The device itself is FCC certified and CE marked. What matters is what you do with it.

### United States

- **Legal to own:** Yes, fully legal to purchase and possess
- **Applicable laws:**
  - **Computer Fraud and Abuse Act (CFAA):** Unauthorized access to computer systems is a federal felony
  - **Electronic Communications Privacy Act (ECPA):** Intercepting electronic communications without authorization is illegal
  - **FCC Regulations:** Transmitting on restricted frequencies, interfering with licensed radio services, or jamming signals violates FCC rules (fines up to $100,000+ and imprisonment)
  - **State laws:** Many states have their own computer crime and wireless interference statutes
- **Customs issues:** US CBP seized ~15,000 units in late 2022 (eventually released). Importing from unofficial channels can result in delays or seizure
- **Amazon:** Banned sales in April 2023, calling it a "card skimming device" (overblown characterization)

### What Is Legal To Do

- Test and experiment with your own devices and systems
- Read/emulate your own access cards, garage remotes, NFC tags
- Use as a universal IR remote for your own electronics
- Professional penetration testing with explicit written authorization and defined scope
- Educational demonstrations on authorized equipment
- U2F hardware security key functionality
- BadUSB testing on your own computers
- Scan and analyze RF spectrum (passive listening is generally legal)

### What Is Illegal To Do

- Clone someone else's access badge or garage remote without authorization
- Deauthenticate WiFi networks you do not own or have permission to test
- Transmit on emergency service frequencies
- Jam or interfere with any radio communications
- Run BadUSB payloads on someone else's computer without authorization
- Use for unauthorized access to any system you do not own
- Skim or clone payment cards (even attempting this is a felony)
- BLE spam attacks in public spaces (can disrupt medical devices -- an insulin pump controller crash was documented at Midwest FurFest 2023)

### International Notes

| Country/Region | Status |
|---|---|
| **Canada** | Legal. Government initially proposed a ban (Feb 2024) in response to auto theft concerns, but reversed course (March 2024) to restrict illegitimate uses only |
| **Brazil** | Anatel has seized shipments citing criminal use potential; EFF criticized seizures |
| **UK** | Legal to own. One device confiscated at Gatwick Airport (Sept 2023) by security |
| **EU (Germany, France, etc.)** | Legal for personal use; unauthorized signal replication or network interference prohibited |
| **Japan** | Legal with MIC Type Approval requirements; precise radio frequency transmission rules |
| **India** | Legal with adherence to telecom regulations |
| **China** | Strict laws around signal devices, especially for commercial/public use |

### Notable Incidents

- **Late 2022:** US Customs seized ~15,000 units; devices were eventually released
- **April 2023:** Amazon banned sales, labeling it a "card skimming device"
- **August 2023:** South Dakota Fusion Centre issued bulletin warning about potential extremist use against power grid infrastructure. No concrete evidence of actual plots was documented. Flipper CEO Pavel Zhovner countered that modern systems are not vulnerable
- **September 2023:** Gatwick Airport security confiscated a device from a passenger; handed to Sussex Police
- **September 2023 (Midwest FurFest):** BLE spam attacks disrupted Square payment readers and caused an insulin pump controller crash. A "Wall of Flippers" Python detection tool was subsequently created
- **February 2024:** Canada announced intention to ban the device due to auto theft concerns
- **March 2024:** Canada reversed course, opting to restrict illegitimate uses rather than implement outright ban

### Bottom Line

**The golden rule: Only interact with systems you OWN or have EXPLICIT WRITTEN PERMISSION to test.** If you follow this rule, you will stay legal everywhere.

---

## 7. Pricing and Where to Buy

### Flipper Zero Device

| Retailer | Price | Notes |
|---|---|---|
| **Flipper Official (flipper.net)** | ~$169 USD | Most reliable source; ships to US, UK, EU, and select countries |
| **Hacker Warehouse (US)** | $210 USD | Same-day processing, US-based support |
| **Lab401 (EU, Belgium)** | EUR 190 (~$207) | VAT-inclusive, DHL Express 2-4 days EU-wide |
| **Micro Center (US, in-store)** | ~$170-200 | 30 stores across the US; walk-in purchase |
| **Joom (Japan)** | JPY 27,800 (~$185) | Sole authorized channel for Japan; MIC compliant |

### AWOK Dynamics Dual C5 Touch (ESP32 Board)

| Retailer | Price | Notes |
|---|---|---|
| **AWOK Dynamics (awokdynamics.com)** | $170 USD | Frequently sold out; restock alerts via Discord |
| **Lab401 (EU)** | EUR 160 | Dual Touch v3 variant; in stock more frequently |

### Total Cost Estimate

- **Flipper Zero only:** $169-210 USD
- **Flipper Zero + Dual C5 Touch + MicroSD card:** ~$350-400 USD
- **MicroSD card (32 GB):** ~$8-15 USD

### Where NOT to Buy

- **Amazon:** Flipper Zero is restricted/banned on Amazon. Third-party listings are often overpriced, counterfeit, or used
- **eBay/AliExpress/Wish:** High risk of counterfeits or tampered devices
- **Unauthorized resellers:** May result in customs seizure; no warranty support

### Official Retailer Finder

Visit flipper.net/pages/resellers and select your country for a complete list of authorized sellers in your region.

---

## Sources

- [Flipper Zero Official Product Page](https://flipper.net/products/flipper-zero)
- [Flipper Zero Technical Specs (Official Docs)](https://docs.flipper.net/zero/development/hardware/tech-specs)
- [Flipper Zero - Wikipedia](https://en.wikipedia.org/wiki/Flipper_Zero)
- [AWOK Dynamics Dual C5 Touch](https://awokdynamics.com/products/dual-c5-touch)
- [AWOK Dual Touch v3 - Lab401](https://lab401.com/products/awok-dual-touch-v3)
- [Momentum Firmware Official Site](https://momentum-fw.dev/)
- [Momentum Firmware GitHub](https://github.com/Next-Flip/Momentum-Firmware)
- [Awesome Flipper Firmware Comparison](https://awesome-flipper.com/firmware/)
- [Flipper Zero Firmware for Pentesting - Spartans Security](https://www.spartanssec.com/post/flipper-zero-choosing-the-best-firmware-for-pentesting)
- [Flipper Zero Step-by-Step Guide 2026 - Serverman](https://www.serverman.co.uk/hardware/flipper-zero/flipper-zero-step-by-step-guide/)
- [What Can the Flipper Zero Do - Serverman](https://www.serverman.co.uk/hardware/flipper-zero/what-can-the-flipper-zero-do/)
- [Flipper Zero App Hub 2026 - Serverman](https://www.serverman.co.uk/everything-hardware/everything-flipper-zero/flipper-zero-app/)
- [Flipper Zero Tutorial 2026 - StationX](https://www.stationx.net/flipper-zero-tutorial/)
- [Flipper Zero Legal Guide - Unleashed](https://flipperzerounleashed.com/flipper-zero-legal-guide/)
- [Flipper Zero Real Uses and Legal Limits - NextTechWorld](https://nexttechworld.com/rf-security/flipper-zero-real-capabilities-legal-use-guide/)
- [Flipper Zero Official Resellers](https://flipper.net/pages/resellers)
- [Where to Buy Flipper Zero - Support](https://support.flipper.net/hc/en-us/articles/17912880572189-Where-to-buy)
- [Awesome Flipper Zero GitHub](https://github.com/djsime1/awesome-flipperzero)
- [Flipper Zero Apps - Official Docs](https://docs.flipper.net/zero/apps)
- [Flipper Lab App Store](https://lab.flipper.net/apps)
