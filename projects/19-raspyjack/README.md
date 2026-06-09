# Project 19: RaspyJack — Portable Network Pentesting Toolkit

> **Status:** Ready to Build (need Waveshare LCD HAT)
> **Difficulty:** Easy-Medium
> **Hardware:** Raspberry Pi Zero 2 W + Waveshare 1.44" LCD HAT
> **Repository:** [7h30th3r0n3/Raspyjack](https://github.com/7h30th3r0n3/Raspyjack)
> **Current Version:** v1.0.6+ (active development)
> **License:** MIT
> **Stars:** 1,000+ on GitHub

---

## Overview

RaspyJack is an open-source, portable network security toolkit built on the Raspberry Pi Zero 2W. It's a DIY alternative to the Hak5 Shark Jack (~$100) for roughly ~$40, with far more capabilities — **231+ payloads across 13 categories**, a built-in WebUI with payload IDE, and the ability to run any Linux tool (Nmap, Responder, aircrack-ng, Scapy, etc.) since it runs full Raspberry Pi OS.

The key differentiator from ESP32-based tools: **RaspyJack runs full Linux.** It's not constrained to firmware-level capabilities. Any tool you can install on Debian/Raspbian runs on RaspyJack.

### RaspyJack vs ESP32 Marauder vs Hak5 Shark Jack

| Feature | RaspyJack | ESP32 Marauder | Hak5 Shark Jack |
|---------|-----------|----------------|-----------------|
| **Hardware** | Pi Zero 2W (~$15-20) | ESP32 (~$12-15) | Custom ($100+) |
| **OS** | Full Linux | ESP32 firmware | Embedded Linux |
| **WiFi attacks** | Yes (external USB adapter) | Yes (native, 2.4GHz) | No |
| **Wired network** | Yes (primary strength) | No | Yes (primary) |
| **Bluetooth** | Yes (scanning, MITM, spam) | Yes (scanning, spam) | No |
| **Custom payloads** | Python/Bash scripts | Limited | Bash scripts |
| **Web UI** | Full dashboard + IDE | Basic | None |
| **Display** | 1.44" LCD + joystick | Varies | LED indicators |
| **Full Linux tools** | Yes (Nmap, Responder, etc.) | No | Partially |

---

## Capabilities (231+ Payloads)

### Reconnaissance
- Nmap scanning with Discord webhook integration
- Shodan integration
- OSINT tools
- Access point/client statistics
- Norse recon suite
- Flock ALPR detection

### WiFi Attacks (Requires External USB Adapter)
- Deauthentication attacks
- Evil twin AP deployment
- Beacon flood / Chaos SSID flooding
- Handshake hunting with auto-upload
- CIW Zeroclick WiFi attacks
- SSID injection
- Wardriving

### Wired Network Attacks
- ARP MITM (man-in-the-middle)
- DNS spoofing
- Stealth bridge MITM with live protocol statistics
- Silent bridge for dual Ethernet

### Credential Capture
- Responder integration (LLMNR/NBT-NS/MDNS poisoning)
- ARP MITM credential harvesting
- DNS spoofing for credential capture
- Automated handshake hunting + hash harvesting

### Evil Portal
- 84 captive portal templates
- Full lifecycle management

### Bluetooth
- Bluetooth scanning
- Bluetooth MITM
- Beacon flood
- Audio injection
- BLE spam

### Shells & C2
- Reverse shell generation
- Discord C2 (command & control)
- HTTPS stealth shells
- DuckyScript generator

### Exfiltration
- HTTP, DNS, BLE, Discord, SMB, FTP, USB, Dropbox methods

### Other Tools
- Ragnar port (vulnerability scanning)
- BadUSB detector
- SMB probe
- CCTV/RTSP viewer with digital zoom
- WebUI dashboard with remote control
- Full Payload IDE (in-browser code editor)
- Tailscale integration for remote access
- Loot browser with filtering and export
- Game Boy emulator with ROM browser

---

## Hardware Requirements

### Minimum Build (~$40)

| Component | Source | Cost | Notes |
|-----------|--------|------|-------|
| Raspberry Pi Zero 2 WH | INVENTORY: Pi Zero 2 W Starter Kit | $0 (owned) | Quad-core, 512MB RAM, headers pre-soldered |
| Waveshare 1.44" LCD HAT | **Need to purchase** | ~$12-15 | ST7735S, 128x128, joystick + 3 buttons, SPI |
| MicroSD card 16GB+ | INVENTORY: 16GB or 128GB cards | $0 (owned) | For OS + payloads + loot |
| USB OTG adapter + USB-to-Ethernet | **Need to purchase** | ~$5-10 | For wired network attacks |

### Recommended Additions

| Component | Purpose | Cost | Notes |
|-----------|---------|------|-------|
| PiSugar S battery | Portable power | INVENTORY (owned) | Currently assigned to Pwnagotchi |
| USB WiFi dongle (monitor mode) | Wireless attacks | INVENTORY: RT5370 (owned) | Or Alfa AWUS036ACH for dual-band |
| Compact case | Protection | ~$5-10 | Optional, 3D printed or off-shelf |

### Hardware Conflict: Pi Zero 2W Allocation

The Pi Zero 2 W is currently assigned to Pwnagotchi (Project 03). Options:
1. **Buy a second Pi Zero 2 W** (~$15-20) — keeps both projects independent
2. **Repurpose** — flash RaspyJack over Pwnagotchi (Pwnagotchi is currently in troubleshooting)
3. **Dual-boot SD swap** — keep both OS images, swap SD cards as needed

**Recommendation:** Buy a second Pi Zero 2 WH. They're cheap and both projects benefit from dedicated hardware. Alternatively, since Pwnagotchi is stuck in troubleshooting, RaspyJack could take over the Pi Zero until Pwnagotchi is resolved.

---

## Setup

### Step 1: Flash the Image

1. Download latest RaspyJack image from [releases](https://github.com/7h30th3r0n3/Raspyjack/releases)
2. Flash to SD card with Raspberry Pi Imager or balenaEtcher
3. Insert SD into Pi Zero 2 W

### Step 2: Hardware Assembly

1. Attach Waveshare 1.44" LCD HAT to Pi Zero GPIO header
2. Connect USB OTG adapter to Pi Zero micro-USB port
3. Plug in USB-to-Ethernet adapter (for wired attacks)
4. Optionally attach PiSugar S for portable battery power

### Step 3: First Boot

1. Power on — RaspyJack boots directly to the LCD menu
2. Navigate with joystick and buttons
3. Select payloads from the touchscreen menu
4. Results display on LCD and log to SD card

### Step 4: WebUI Access

1. Connect to RaspyJack's WiFi AP (created on boot)
2. Navigate to WebUI in browser
3. Full dashboard: payload browser, IDE, loot viewer, remote control
4. Optional: enable Tailscale for remote access over the internet

---

## Cyberdeck Integration

RaspyJack in the cyberdeck fills a role NO other device covers: **wired network attacks.** The ESP32 boards handle WiFi/BLE/RF, but none can plug into an Ethernet port and run ARP MITM, Responder, or DNS spoofing.

**Deck role:** Wired network pentesting + Linux-based reconnaissance
**Board:** Pi Zero 2 W (dedicated unit, separate from Pwnagotchi)
**Power:** USB from powered hub or PiSugar battery
**Display:** Waveshare 1.44" LCD HAT (self-contained)
**Network:** USB-to-Ethernet adapter for wired attacks, USB WiFi for wireless
**Control:** Joystick/buttons on LCD HAT, or remote via WebUI from Pi 5

**Docking concept:** Like Pwnagotchi, RaspyJack sits in a dock inside the cyberdeck case. It operates independently but can be controlled from the Pi 5's dashboard via WebUI over the internal network.

See [cyberdeck integration guide](../14-cyberdeck/integrations/19-raspyjack/) for deck-specific setup.

---

## Community

- **Main repo:** [7h30th3r0n3/Raspyjack](https://github.com/7h30th3r0n3/Raspyjack)
- **Community payloads:** [wickednull/raspyjack-payloads](https://github.com/wickednull/raspyjack-payloads)
- **Build guide (YouTube):** [Complete RaspyJack Guide](https://www.youtube.com/watch?v=YacMgTcv3wY)
- **Cardputer Zero port:** M5Stack Cardputer Zero alternative (Pi CM0-based, has keyboard + screen + battery)

---

## Limitations

- **No WiFi attacks without external USB adapter** — onboard Broadcom chip cannot do monitor mode
- **512MB RAM** — limits concurrent tool usage vs a full Pi 5
- **Pi Zero 2W power** — adequate for payloads but slower than Pi 4/5 for heavy scanning
- **Wired attacks require physical Ethernet connection** — need to be plugged into the target network
- **LCD HAT consumes GPIO** — limits expansion options while attached

---

## Feature Brainstorm — What Else Can This Do

- **Responder credential capture** — deploy Responder on a wired connection to poison LLMNR/NBT-NS/MDNS and capture NTLMv2 hashes from Windows hosts on the target network during authorized pentests
- **ARP MITM for traffic interception** — run arpspoof + mitmproxy to intercept and inspect plaintext traffic between hosts on the same subnet; log credentials, cookies, and API keys for the engagement report
- **DNS spoofing for social engineering assessments** — redirect DNS queries to a controlled evil portal running on RaspyJack to test employee awareness against phishing during an authorized red team exercise
- **Nmap automated discovery with Discord webhook alerts** — schedule periodic Nmap scans of a target subnet and push new-host alerts to a Discord channel via webhook for real-time asset discovery monitoring
- **Scapy custom packet crafting** — write Python scripts using Scapy to craft and send custom protocol packets for testing firewall rules, IDS evasion, or protocol-level fuzzing on authorized networks
- **WebUI payload IDE for custom scripts** — use the built-in browser-based code editor to write, test, and deploy custom Python/Bash attack payloads without needing SSH or a separate dev environment
- **Bluetooth MITM via built-in BLE** — leverage the Pi Zero 2W's onboard Bluetooth to intercept BLE GATT communications between a peripheral and its app, testing for insecure pairing or plaintext attribute writes
- **WiFi attacks with external USB adapter** — add a monitor-mode-capable USB WiFi dongle (RT5370 from inventory) to run deauth, evil twin, and handshake capture attacks alongside wired pentesting
- **Community payload contributions** — submit custom payloads to [wickednull/raspyjack-payloads](https://github.com/wickednull/raspyjack-payloads) and pull new community payloads to expand the 231+ payload library
- **SSH tunnel back to cyberdeck Pi 5** — establish a reverse SSH tunnel from RaspyJack to the cyberdeck's Pi 5 so you can control the device remotely from the deck's dashboard while it is plugged into a distant switch
- **Drop box deployment** — configure RaspyJack as a covert "drop box" left on an authorized target network: auto-connect via Ethernet, run Responder + Nmap on a cron schedule, exfiltrate loot via Tailscale or Discord C2, and retrieve the device later

---

## Resources

| Resource | Link |
|----------|------|
| GitHub repo | [7h30th3r0n3/Raspyjack](https://github.com/7h30th3r0n3/Raspyjack) |
| Releases | [GitHub Releases](https://github.com/7h30th3r0n3/Raspyjack/releases) |
| Wiki | [GitHub Wiki](https://github.com/7h30th3r0n3/Raspyjack/wiki) |
| Community payloads | [wickednull/raspyjack-payloads](https://github.com/wickednull/raspyjack-payloads) |
| Hackster.io coverage | [RaspyJack Low-Cost Shark Jack Alternative](https://www.hackster.io/news/the-raspyjack-is-a-low-cost-alternative-to-the-hak5-shark-jack-built-from-a-raspberry-pi-zero-2w-cde02bdfc943) |
| Geeky Gadgets guide | [RaspyJack Features & Setup](https://www.geeky-gadgets.com/raspyjack-dns-spoofing-tools/) |
| Build video | [How to Build a RaspyJack](https://www.youtube.com/watch?v=WHJHB-T4IsI) |
