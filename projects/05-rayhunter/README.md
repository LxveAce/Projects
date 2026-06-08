# RayHunter

## Table of Contents

1. [Overview](#1-overview)
2. [How IMSI Catchers Work](#2-how-imsi-catchers-work)
3. [Hardware Requirements](#3-hardware-requirements)
4. [Step-by-Step Setup](#4-step-by-step-setup)
5. [Usage and Interpreting Results](#5-usage-and-interpreting-results)
6. [Detection Heuristics and Limitations](#6-detection-heuristics-and-limitations)
7. [Legal Context](#7-legal-context)
8. [Alternative Tools](#8-alternative-tools)
9. [Resources](#9-resources)

---

## 1. Overview

**RayHunter** is a free, open-source tool developed by the **Electronic Frontier Foundation (EFF)** that detects IMSI catchers -- also known as **cell-site simulators (CSS)** or **Stingrays**. Written primarily in Rust (94.2% of the codebase), it runs on affordable mobile hotspot hardware (as cheap as ~$20) and intercepts/analyzes the control-plane traffic between the hotspot's cellular modem and nearby cell towers, looking for telltale signs of surveillance devices.

### Why EFF Built It

Very little is publicly known about how commercial cell-site simulators actually work. Law enforcement agencies in the US and abroad use them, but their deployment is shrouded in secrecy -- police have dropped criminal cases rather than disclose Stingray use in court. EFF built RayHunter to:

- Determine conclusively whether CSS are used to surveil constitutionally protected activity (protests, journalism, etc.)
- Collect empirical network traffic data about what CSS exploits actually look like on the wire
- Map CSS usage globally, especially in countries lacking free speech protections
- Improve threat modeling and inform policy advocacy
- Give ordinary people a low-cost way to detect potential surveillance

The project launched publicly in **March 2025**. As of June 2026, it has 5,300+ GitHub stars, 430+ forks, 32 releases (current: v0.11.2), and active community development.

| | |
|---|---|
| **Repository** | https://github.com/EFForg/rayhunter |
| **Documentation** | https://efforg.github.io/rayhunter/ |
| **License** | GPL-3.0 |

---

## 2. How IMSI Catchers Work

### What They Are

IMSI catchers are devices that impersonate legitimate cellular base stations (cell towers). They exploit fundamental design flaws in cellular protocols -- particularly the fact that phones are designed to always connect to the tower with the strongest signal, and that in older protocols (2G/GSM), the phone authenticates itself to the network but the network does not authenticate itself to the phone.

### Two Categories

**Active Cell-Site Simulators (Stingrays):**

- Broadcast signals stronger than legitimate towers, or manipulate broadcast parameters to appear more attractive
- Force nearby phones to disconnect from real towers and connect to the simulator
- Once connected, extract the phone's IMSI (International Mobile Subscriber Identity -- the unique identifier tied to the SIM card) and IMEI (hardware serial number)
- Can collect data from up to 10,000 phones simultaneously within range
- Advanced models can intercept communications when forcing connections down to 2G

**Passive IMSI Catchers:**

- Do not transmit signals
- Passively capture cellular transmissions from the airwaves (like an FM radio)
- Decode/decrypt captured signals to extract identifiers and track devices
- Much harder to detect since they emit no radio energy

### Attack Categories

1. **IMSI/IMEI Harvesting** -- During connection negotiation, the CSS sends an Identity Request. The phone automatically transmits its IMSI. This is the most basic and universal capability.

2. **Location Tracking:**
   - *Passive presence testing:* Monitoring unencrypted paging messages to see which phones are in an area
   - *Semi-passive testing:* Triggering calls/messages to correlate temporary identifiers with targets
   - *Active tracking:* Using connected phones to report signal strength from neighboring towers, enabling trilateration; newer phones may transmit GPS coordinates

3. **Communication Interception** -- Only reliably possible on 2G/GSM networks where encryption is weak (A5/1 cipher) or can be disabled entirely. Requires man-in-the-middle positioning. Can capture call metadata, unencrypted SMS, and website visits.

4. **Service Downgrade Attacks** -- The CSS forces LTE/4G-capable phones to fall back to 2G/GSM by sending TAU Reject messages or broadcasting fake System Information Blocks that prioritize 2G/3G frequencies. Once on 2G, the phone is vulnerable to interception.

5. **Denial of Service** -- Jamming frequencies or sending rejection codes that force phones into non-functional states, disrupting communications within a ~500m radius (including 911 calls).

### Protocol Vulnerabilities by Generation

| Generation | Key Vulnerability |
|---|---|
| **2G/GSM** | No mutual authentication. Network does not prove identity to phone. Weak/disableable encryption (A5/1). Full interception possible. |
| **3G/UMTS** | Mutual authentication added, but attackers can exploit "nearest neighbor" lists, broadcast on higher-priority frequencies, or force downgrade to 2G. |
| **4G/LTE** | Stronger security, but System Information Blocks (SIB) are unencrypted and unauthenticated -- can be spoofed to trigger downgrade. IMSI still transmitted before encryption is established in certain handover scenarios. |
| **5G** | Encrypts the IMSI (now called SUPI) using SUCI, but implementation varies. Early 5G NSA (Non-Standalone) still relies on 4G core and inherits vulnerabilities. |

### Who Uses Them

- **US Federal:** FBI, DEA, NSA, Secret Service, ICE, US Marshals, all military branches
- **US State/Local:** At least 75 agencies across 27+ states
- **International:** Used by governments worldwide, including in authoritarian regimes
- **Manufacturers:** Harris Corporation (Stingray, Hailstorm, KingFish), Boeing/Digital Receiver Technology ("Dirtboxes"), Septier, Gamma Group, Rohde & Schwarz, and others

---

## 3. Hardware Requirements

### Core Compatibility Requirement

RayHunter requires a device that:

- Runs a **Qualcomm modem**
- Exposes the **`/dev/diag`** diagnostic interface (Qualcomm's DIAG protocol)

This interface gives RayHunter access to raw cellular control-plane messages that are normally hidden from applications.

### Recommended Devices (Extensively Tested)

| Device | Region | Notes |
|---|---|---|
| **Orbic RC400L** | Americas | Primary development device. Also sold as Kajeet RC400L. ~$15-30 on secondary markets. 18-22 hr battery. 94/100 score. 97% 2G downgrade detection accuracy. |
| **TP-Link M7350** | Europe, Africa, Middle East | Also works in Americas but usually more expensive. 12-15 hr battery. 91/100 score. Excellent global band compatibility. SD card support. |

### Confirmed Working Devices

| Device | Region |
|---|---|
| **Kajeet RC400L** | Americas (identical hardware to Orbic) |
| **TP-Link M7310** | Europe, Africa, Middle East |
| **Wingtech CT2MHS01** | Americas |
| **T-Mobile TMOHS1** | Americas |
| **PinePhone / PinePhone Pro** | Global |
| **FY UZ801** | Asia, Europe |
| **Moxee Hotspot** | Americas |

### Practical Recommendations

- **High-risk professionals (journalists, activists):** Orbic RC400L for maximum reliability and battery life
- **International travelers:** TP-Link M7350 for global band coverage
- **Budget-conscious / training:** TP-Link M7310 as minimum viable option
- **Extended field operations:** Orbic/Kajeet for 18+ hour battery life

### What You Also Need

- A computer (Mac, Linux, or Windows) for initial installation
- USB cable for flashing the device
- WiFi-capable device (phone, laptop) to access RayHunter's web interface after setup

---

## 4. Step-by-Step Setup

### Prerequisites

- Download the latest RayHunter release from https://github.com/EFForg/rayhunter/releases
- Unzip the release files
- Have your hotspot device and a USB cable ready

### Installation on Orbic RC400L (Primary Device)

**Step 1: Obtain the device**

Purchase an Orbic RC400L (or Kajeet RC400L). Available on eBay, Amazon secondary market, and other sources for approximately $15-30.

**Step 2: Note your admin password**

- Verizon units: The WiFi password displayed on the device is also the admin password
- Kajeet/Smartspot units: Default password is `$m@rt$p0tc0nf!g`
- If needed, reset by pressing the button under the back case until the unit restarts

**Step 3: Download and extract RayHunter**

Download the latest release from the GitHub releases page and unzip.

**Step 4: Run the installer**

Standard network-based installation (recommended):

```bash
./installer orbic --admin-password 'mypassword'
```

For Kajeet devices:

```bash
./installer orbic --admin-password '$m@rt$p0tc0nf!g'
```

Optional parameters if defaults don't match:

```bash
--admin-username 'myusername'
--admin-ip 'mydeviceip'
```

Alternative USB method (not recommended, use only if network method fails):

```bash
./installer orbic-usb
```

There is also a GUI-based installer (`installer-gui`) for less technical users.

**Step 5: Access the RayHunter interface**

1. Connect to the Orbic's WiFi network from your phone or laptop
2. Open a browser and navigate to: **http://192.168.1.1:8080**
3. You should see the RayHunter dashboard

**Step 6: Verify operation**

- The interface displays a colored indicator line
- **Green** = normal, no suspicious activity detected
- **Red** = suspicious activity detected -- potential IMSI catcher

### Shell Access (Advanced)

For debugging or advanced configuration:

```bash
./installer util orbic-shell
```

Or for older versions:

```bash
adb shell
/bin/rootshell   # for elevated privileges
```

### Platform Notes

- Mac and Linux are fully supported for installation
- Windows support exists but may require additional setup (ADB drivers)
- The installer handles rooting the device, deploying the RayHunter daemon, and configuring autostart

---

## 5. Usage and Interpreting Results

### Day-to-Day Operation

1. **Power on** the Orbic hotspot -- RayHunter starts automatically
2. **Carry it with you** -- it fits in a pocket and runs on battery for 18+ hours
3. The device's screen or LED indicator shows status (green = safe, red = alert)
4. For detailed information, connect to the device's WiFi and visit **http://192.168.1.1:8080**

### Web Interface Features

- **Real-time status:** Current detection state (safe vs. alert)
- **Log viewer:** Browse captured cellular control-plane events
- **Alert history:** Review past detections with timestamps
- **Log download:** Export PCAP/log files for expert analysis or submission to EFF
- **Analyzer configuration:** Enable/disable individual heuristics

### Interpreting Alerts

**Green status (no detection):** The analyzers have not flagged any suspicious behavior from nearby towers. Note: this does NOT guarantee no IMSI catcher is present -- passive catchers and sophisticated devices may evade detection.

**Red status (alert):** One or more heuristics triggered. This means anomalous cellular behavior was observed. It does NOT definitively confirm an IMSI catcher -- false positives can occur from:

- Legitimate tower maintenance or reconfiguration
- Carrier network testing equipment
- Crossing tracking/location area boundaries
- Flying (landing near airports after prolonged disconnection)
- Unusual but legitimate tower configurations

**What to do when you get an alert:**

1. Note your location, time, and what you were doing (protest, near government building, etc.)
2. Download the log files from the web interface
3. Consider submitting logs to EFF for analysis
4. If you see repeated alerts in the same location over multiple visits, that is more significant than a single transient alert

### Contributing Data to EFF

EFF actively seeks log data to map CSS deployment worldwide. You can export logs from the web interface and submit them through EFF's community channels (Mattermost).

---

## 6. Detection Heuristics and Limitations

### Detection Heuristics (7 Active Analyzers)

#### 1. IMSI Requested (v3) -- Core Detection

Flags when a base station requests your IMSI/IMEI in suspicious circumstances.

- Specifically watches for the pattern: connect to tower -> identity request -> NO authentication -> disconnect
- Legitimate IMSI requests happen during power-on, roaming, SIM swap, or area changes -- these are filtered out
- **Known false positive:** Aircraft landing scenarios

**Normal circumstances for IMSI/IMEI requests:**
- Initial network attachment after device power-on
- TMSI/GUTI expiration
- Network transitions (roaming, SIM swaps)
- Tracking/Location Area changes
- Core network reboots

**Additional alert triggers:**
- Identity requested after successful authentication
- Identity requested without preceding tower connection
- Identity requested without subsequent authentication
- Repetitive identity sends under non-suspicious conditions (diagnostic alerts)

#### 2. Connection Release/Redirect 2G Downgrade -- High Priority

Detects when a tower releases your connection and redirects you to a 2G base station.

- A real carrier has no reason to ask a 4G-capable device to reconnect using 2G
- Any 2G downgrade redirect triggers a high-priority alert

#### 3. LTE SIB6/7 Downgrade (v2) -- Protocol Manipulation

Detects fake System Information Block broadcasts that prioritize 2G/3G frequencies over 4G.

- SIB messages are unencrypted and unauthenticated, making them forgeable
- SIB6 alerts (CDMA2000) are rare; SIB7 (GSM/EDGE) false positives reduced in v2
- A well-behaved tower always advertises 4G neighbors at higher priority than 2G/3G

#### 4. Null Cipher - RRC Layer -- Encryption Disabled

Alerts when a cell suggests EEA0 (null cipher / no encryption) for the radio layer.

- Normal only in lab/testing environments
- IMSI catchers use null ciphers to avoid setting up secure communication

#### 5. NAS Null Cipher -- Critical Severity

Alerts when a security mode command suggests no encryption after successful authentication.

- This **should never happen at all** under normal conditions
- Indicates either an IMSI catcher with telecom/government cooperation, an SS7 attack, or severe misconfiguration
- Potential causes include SS7 attacks accessing HLR key material, IMSI catchers with government/telecom cooperation, or rare misconfiguration where encryption is restricted

#### 6. Incomplete SIB -- Tower Validation

Flags when SIB1 messages lack timing info for the minimum expected additional SIBs (SIB3, 4, 5).

- Fake stations often broadcast minimal system information (SIB1 + one additional only)
- Alone suggests misconfiguration; combined with IMSI Requested, **strongly suggests malicious activity**

#### 7. Diagnostic Information -- Informational

Logs connection/disconnection events for tower analysis.

- Used for baseline building; alerts are informational only
- Ignored until low/medium/high severity alerts appear

#### 8. Test Analyzer -- Development/Verification Only

Alerts on every new tower (SIB1 broadcasts) to verify RayHunter is working.

- Intentionally generates high alert volume for verification purposes
- **Disabled during normal operation** due to noise levels

### Limitations

**Fundamental constraints:**

- **No ground truth:** Without a known IMSI catcher to test against, detection accuracy cannot be formally validated. There is no way to confirm that silence means safety.
- **Passive catchers are invisible:** RayHunter can only detect active cell-site simulators that interact with the device. Purely passive listeners that just capture radio signals cannot be detected by any phone-based tool.
- **Sophisticated evasion:** Well-funded adversaries may use CSS that mimic legitimate tower behavior closely enough to evade heuristic detection.
- **5G limitations:** Current heuristics focus on 2G/3G/4G. 5G-specific attacks are an active area of research.
- **False positives:** Legitimate network events (maintenance, reconfiguration, carrier testing, area transitions) can trigger alerts. A single alert should not cause panic.
- **False negatives:** An IMSI catcher that does not use the specific attack patterns RayHunter checks for will not be detected.
- **Device dependency:** Only works on devices with Qualcomm modems exposing `/dev/diag`. Cannot run on ordinary smartphones.
- **Geographic coverage:** Band compatibility varies by region. The Orbic RC400L is optimized for US LTE bands; international users need region-appropriate devices.

---

## 7. Legal Context

### Running RayHunter

The EFF states: *"We believe running this program does not currently violate any laws or regulations in the United States."* However, they disclaim liability and advise non-US users to consult local legal counsel. RayHunter is a passive monitoring tool that only analyzes signals your own device receives -- it does not transmit, jam, or interfere with any communications.

### Legal Status of IMSI Catchers in the US

**Federal policy (not binding law):**

- In 2015, the DOJ issued a policy requiring federal agencies to obtain a **warrant** before using CSS, except in emergencies or national security cases
- This is DOJ internal policy, not statute, and does not bind state/local law enforcement
- The government's official position has been that CSS use falls under pen register authority (lower standard than a warrant), per *Smith v. Maryland*

**State laws requiring warrants:**

- California (CalECPA)
- Washington
- Virginia
- Utah
- Minnesota
- Illinois
- Most other states have NO specific CSS legislation

**Proposed federal legislation:**

- The **Cell-Site Simulator Warrant Act** (introduced 2021 by Senators Wyden and Daines) would require probable cause warrants for all federal, state, and local CSS use. As of 2026, it remains stalled in committee.

**Government secrecy practices:**

- Police routinely withhold CSS use from courts and defense attorneys
- Officers have "recreated" evidence through parallel construction to hide surveillance methods
- Prosecutors have dropped cases rather than disclose CSS use
- Non-disclosure agreements with manufacturers (particularly Harris Corporation) restrict transparency
- The FBI has instructed local police to attribute CSS evidence to "confidential sources"

**Constitutional concerns:**

- CSS constitute **general searches** -- they sweep up data from thousands of non-target phones
- This potentially violates Fourth Amendment requirements to "particularly describe" the place to be searched
- CSS disrupt 911 calls within their operating radius, creating public safety hazards
- Disproportionate deployment in low-income communities and communities of color has been documented (Baltimore)

---

## 8. Alternative Tools

### Phone-Based Apps

| Tool | Platform | Status | Notes |
|---|---|---|---|
| **SnoopSnitch** | Android (rooted, Qualcomm) | Maintained | Analyzes network traffic, alerts on suspicious tower behavior. Requires root and Qualcomm chipset. |
| **AIMSICD** (Android IMSI-Catcher Detector) | Android | Abandoned (last update ~2016) | Detected quick tower changes, 2G downgrades. No longer maintained. |
| **Cell Spy Catcher** | Android | Active | Logs suspicious events, exports CSV. Works across GSM/UMTS/CDMA/LTE. Commercial app. |
| **Darshak** | Android | Research project | Academic tool for analyzing control-plane messages. |
| **AntiSpy** (Croatian Telecom) | Android/iOS | Active | Uses radio signal analysis. Telecom-backed. |

### Hardware-Based Tools

| Tool | Hardware | Notes |
|---|---|---|
| **Crocodile Hunter** (EFF) | Software-Defined Radio + Raspberry Pi/Linux | EFF's earlier project. Scans for fake 4G base stations using SDR. More complex setup than RayHunter. Requires dedicated hardware (~$200+). |
| **SeaGlass** (Univ. of Washington) | Custom sensor arrays deployed in vehicles | City-scale detection research project. Deployed across Seattle. Not consumer-available. |
| **SITCH** (Ash Wilson) | Raspberry Pi + SDR | Sensor for Insecure Telephone Communication on your Honeypot. Network-based approach. |

### Enterprise/Commercial Solutions

| Tool | Notes |
|---|---|
| **FirstPoint Mobile Guard** | Commercial cellular security platform |
| **Bastille Networks** | Enterprise RF threat detection |
| **Pwnie Express** | Enterprise wireless threat detection (includes CSS detection) |
| **ESD America CryptoPhone** | Hardened Android phone with built-in CSS detection (~$3,500) |
| **Cape** | Privacy-focused mobile carrier with built-in IMSI catcher resistance |

### Why RayHunter Stands Out

- **Cost:** ~$20 for hardware vs. hundreds or thousands for alternatives
- **Ease of use:** Simple installer, web-based interface, no rooting of personal phone required
- **Independence:** Runs on a separate device, not your personal phone
- **Open source:** Fully auditable code under GPL-3.0
- **Active development:** EFF-backed with monthly updates and new heuristics
- **Community:** Active contributor base, 430+ forks, Mattermost discussion channel
- **Data contribution:** Supports EFF's global mapping effort

---

## 9. Resources

### Official

- **GitHub Repository:** https://github.com/EFForg/rayhunter
- **Official Documentation/Book:** https://efforg.github.io/rayhunter/
- **Supported Devices:** https://efforg.github.io/rayhunter/supported-devices.html
- **Orbic Setup Guide:** https://efforg.github.io/rayhunter/orbic.html
- **Heuristics Documentation:** https://efforg.github.io/rayhunter/heuristics.html
- **EFF Launch Blog Post:** https://www.eff.org/deeplinks/2025/03/meet-rayhunter-new-open-source-tool-eff-detect-cellular-spying
- **EFF IMSI Catcher Whitepaper:** https://www.eff.org/wp/gotta-catch-em-all-understanding-how-imsi-catchers-exploit-cell-networks
- **EFF Street Level Surveillance -- CSS:** https://sls.eff.org/technologies/cell-site-simulators-imsi-catchers
- **Releases:** https://github.com/EFForg/rayhunter/releases

### Community Guides and Tutorials

- **LinuxConfig Tutorial:** https://linuxconfig.org/rayhunter-tutorial-convert-a-verizon-orbic-speed-rc400l-into-a-stingray-detector
- **SimeonOnSecurity Flashing Guide:** https://simeononsecurity.com/articles/how-to-flash-rayhunter-devices-complete-guide/
- **SimeonOnSecurity Device Comparison:** https://simeononsecurity.com/articles/rayhunter-device-comparison-2026-complete-review/
- **Ringmast4r EFF Rayhunter Guide:** https://ringmast4r.org/html-roladex/EFF-Rayhunter
- **Chris Reynolds Blog:** https://ecto-1a.github.io/rayhunter/
- **xtonyx Installation Guide:** https://xtonyx.org/posts/2025/08/14/rayhunter-on-orbic/
- **jtriley Analysis:** https://jtriley.substack.com/p/the-rayhunter
- **Hackers Arise SDR/Rayhunter:** https://hackers-arise.com/sdr-signals-intelligence-for-hackers-discover-rayhunter-an-open-source-tool-by-eff-for-detecting-cellular-spying/

### Video Tutorials

- **Side of Burritos -- Setup Guide:** https://www.youtube.com/watch?v=UXp77zJkLN4
- **Building the EFF IMSI Catcher Detector:** https://www.youtube.com/watch?v=SbSYSNuAetI
- **Rayhunter $20 Stingray Detector Full Demo:** https://www.youtube.com/watch?v=K7fupbkdLMs

### Background and Legal Resources

- **IMSI Catcher Wikipedia:** https://en.wikipedia.org/wiki/IMSI-catcher
- **Stingray Use in US Law Enforcement (Wikipedia):** https://en.wikipedia.org/wiki/Stingray_use_in_United_States_law_enforcement
- **Georgetown Law -- Stingray and Fourth Amendment:** https://www.law.georgetown.edu/american-criminal-law-review/wp-content/uploads/sites/15/2023/02/53-0-McCullough-stingray-searches-and-the-fourth-amendment-implications-of-modern-cellular-surveillance.pdf
- **POGO -- Cell-Site Simulator Warrant Act:** https://www.pogo.org/fact-sheets/issue-brief-the-cell-site-simulator-warrant-act
- **SeaGlass Project (UW):** https://seaglass.cs.washington.edu/
- **Enea -- IMSI Catchers Around the World:** https://www.enea.com/insights/adaptive-mobile-imsi-catchers/

### Where to Buy Hardware

- **Orbic RC400L:** eBay, Amazon secondary market, Tindie (pre-flashed units available from STS Collective at https://www.tindie.com/products/stscollective/new-rayhunter-imsi-catcher-stingray-detector/)
- **TP-Link M7350:** Standard retail channels (Amazon, electronics retailers)

### Community

- **Mattermost:** Referenced in official docs for discussion and log submission
- **GitHub Issues:** https://github.com/EFForg/rayhunter/issues

---

## 10. Best-Fit Hardware from Your Inventory

### Status: Not Ready -- Need Orbic Phone

RayHunter requires a specific Orbic RC400L (or RC2200L) phone with a Qualcomm modem for baseband diagnostic access. **No board in your current inventory can substitute** -- it needs the cellular modem hardware.

### What to Buy

| Item | Price | Where |
|------|-------|-------|
| Orbic Speed RC400L (used/renewed) | ~$20-50 | [eBay](https://www.ebay.com/p/24051840599), [Amazon (renewed)](https://www.amazon.com/RC400L-Carrier-Unlocked-Hotspot-Renewed/dp/B0F55YKZP9), [Walmart](https://www.walmart.com/ip/Orbic-Speed-Mobile-Hotspot-for-Verizon-RC400L-Used/5384207634) |
| Pre-flashed RayHunter unit | ~$50-70 | [Tindie (STS Collective)](https://www.tindie.com/products/stscollective/new-rayhunter-imsi-catcher-stingray-detector/) |

Once obtained: root the phone, flash RayHunter via ADB, and access the web UI from another device. No keyboard, display, antenna, or storage from your inventory is needed.
