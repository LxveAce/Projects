# Security & Hardware Projects

A curated collection of cybersecurity, wireless, and hardware hacking projects -- from ESP32 tools to mesh networking to surveillance detection. Each project has its own folder with deep research, step-by-step build guides, and resource links. The flagship is a 14-device Pelican 1300 cyberdeck (Project 14) that consolidates the integrable projects into a single field-portable rig.

This is a self-taught, hobby-driven security-research and hardware portfolio. Everything here is documentation, research, and build notes -- not production software.

**General Resource Hub:** [BushidoUK/Open-source-tools-for-CTI](https://github.com/BushidoUK/Open-source-tools-for-CTI)

<!-- STATUS-ROADMAP:START -->
## Status & Roadmap

**Status:** Healthy public documentation/research portfolio — 19 projects plus the Project 14 cyberdeck, MIT-licensed, default branch `main`. No broken builds or crash-level defects; the focus is keeping the research and build notes accurate.

**In progress / known issues:**
- Reconciling the cyberdeck `UNIVERSAL-FLASHER.md` planning doc so it points at the already-shipped flasher lineage (the work it once planned now ships as the Cyber Controller app) instead of describing it as unbuilt.
- Correcting an ESP32 board-variant note (Lonely Binary "Gold" boards are classic ESP32, not ESP32-S3) so build steps reference the hardware-verified chip.
- Verifying the published downloads pages render working installer links end-to-end in a real browser.

**Roadmap:**
- Repoint the cyberdeck planning docs (`UNIVERSAL-FLASHER.md`, `FIRMWARE-REFERENCE.md`) to the shipped Cyber Controller / universal-flasher lineage so they inform rather than duplicate it.
- Add the missing `integrations/17-oui-spy` build guide (or document that OUI-Spy is folded into 18-halehound).
- Bump the embedded marauder README to the current upstream release and link readers to the maintained repo's Releases.
- Add lightweight CI (`python -m py_compile`) to guard the one vendored code snapshot.
<!-- STATUS-ROADMAP:END -->

---

## Project Directory

| # | Project | Status | Difficulty | Description |
|---|---------|--------|-----------|-------------|
| 01 | [ESP32 Marauder](projects/01-esp32-marauder/) | **Built** (CYD + headless + C5 dual-band) | Medium | WiFi/Bluetooth offensive & defensive toolkit on ESP32 — now with 2.4+5GHz dual-band via ESP32-C5 |
| 02 | [Flipper Zero + ESP32](projects/02-flipper-zero/) | Not Yet Purchased | Easy | Multi-tool for sub-GHz, RFID, NFC, IR + WiFi via ESP32 board |
| 03 | [Pwnagotchi](projects/03-pwnagotchi/) | Troubleshooting | Medium | AI-powered WiFi handshake capture tool on Pi Zero |
| 04 | [Meshtastic](projects/04-meshtastic/) | Troubleshooting | Easy-Medium | LoRa mesh networking for off-grid communications |
| 05 | [RayHunter](projects/05-rayhunter/) | Need Hardware | Easy | EFF's cell-site simulator (stingray) detector |
| 06 | [Flock & Drone Detection](projects/06-flock-drone-detection/) | Ready to Build | Medium | ALPR camera detection + RF drone detection |
| 07 | [Kismet Wardriving](projects/07-kismet-wardriving/) | Ready to Build | Medium | Wireless network detection, sniffing, and mapping |
| 08 | [BLE Detection & Tracking](projects/08-ble-detection/) | Ready to Build | Easy-Medium | Bluetooth tracker detection and presence monitoring |
| 09 | [Project Nomad](projects/09-project-nomad/) | Blocked (ARM) | Hard | Offline communications and media platform |
| 10 | [Chasing Your Tail](projects/10-chasing-your-tail/) | Ready to Build | Easy | Detect unwanted AirTag/Tile/SmartTag trackers |
| 11 | [NyanBOX](projects/11-nyan-box/) | In Transit | Easy | Pre-built portable pentesting toolkit |
| 12 | [USB Rubber Ducky](projects/12-usb-rubber-ducky/) | Not Yet Purchased | Easy | Keystroke injection tool (or DIY with ESP32) |
| 13 | [ESP Terminator](projects/13-esp-terminator/) | Ready to Use | Easy | Web-based ESP32 firmware flasher for multiple tools |
| 14 | [Cyberdeck](projects/14-cyberdeck/) | Brainstorm | Hard | All-in-one portable security rig — 14 devices, 12 switches, 7 SMA antennas (Pi 5 + ESP32-C5 dual-band + RayHunter + HaleHound + RaspyJack + Meshtastic + Kismet) |
| 15 | [ESP32-DIV](projects/15-esp32-div/) | Evaluating | Medium | Open-source ESP32-S3 multitool — Sub-GHz, IR, RFID/NFC, 2.4GHz (Flipper-class) |
| 16 | [BlueJammer-V2](projects/16-bluejammer/) | Reference only | -- | 2.4GHz RF jammer — cataloged for reference; deck uses the lawful **detector** instead |
| 17 | [OUI-Spy](projects/17-oui-spy/) | Ready to Build | Medium | Passive wireless surveillance detection — OUI-based device identification, Flock/drone/tracker scanning on ESP32-S3 |
| 18 | [HaleHound + IoT Recon](projects/18-halehound/) | Ready to Build | Medium | Multi-protocol attack toolkit on CYD — WiFi, BLE, SubGHz, NFC, IoT credential brute force (ESP32-DIV fork) |
| 19 | [RaspyJack](projects/19-raspyjack/) | Ready to Build | Easy-Medium | Portable network pentesting toolkit on Pi Zero 2W — 231+ payloads, wired attacks, WebUI (Shark Jack alternative) |

---

## Cyberdeck Classification

Every project falls into one of three categories relative to the [Cyberdeck build](projects/14-cyberdeck/) (Pelican 1300, 14 devices, 7 SMA bulkheads, 12 switches):

### Deck-Integrated (Board Mounted Inside)

| Project | Board | Role | Antenna |
|---------|-------|------|---------|
| 01 Marauder | Gold #1 + CYD #1 | 2.4GHz WiFi/BLE offensive | SMA 1 (5 dBi) |
| 06 Flock | Gold #2 | ALPR camera detection | SMA 2 (5 dBi) |
| 08/10 BLE+CYT | Gold #3 | BLE tracker + tail detection | SMA 3 (5 dBi) |
| 01 Marauder 5G | C5 #1 | Dual-band 2.4+5GHz attacks | SMA 4 (dual-band) |
| 07 Kismet 5G | C5 #2 | Dual-band scanning/wardriving | SMA 5 (dual-band) |
| 04 Meshtastic | Heltec V3 | LoRa 915MHz mesh comms | SMA 6 (4 dBi) |
| 06 Drone | WROOM-32 | RemoteID drone detection | Internal |
| 18 HaleHound | CYD #2 | IoT Recon + SubGHz + NFC | Internal |
| 19 RaspyJack | Pi Zero 2W | Wired network pentesting | Internal |
| 05 RayHunter | Orbic RC400L | IMSI catcher / stingray detector | Internal (cellular) |
| 07 Kismet | PAU0F + RT5370 | WiFi 6E wardriving | SMA 7 (tri-band) |
| Shared | VK-162 GPS | GPS for all tools via gpsd | Internal |

### Standalone (Separate Portable Device)

| Project | Why | Hardware |
|---------|-----|----------|
| 02 Flipper Zero | Pocket multi-tool, own screen/battery | Flipper Zero + AWOK C5 Touch |
| 03 Pwnagotchi | Autonomous AI, pocket carry | Pi Zero 2W + e-ink + PiSugar |
| 09 Project Nomad | x64 only (blocked on ARM) | LattePanda / x64 SBC |
| 11 NyanBOX | Pre-built sealed unit | NyanBOX kit ($220) |
| 12 USB Rubber Ducky | USB stick, physical access | Hak5 Ducky / DIY ESP32-S2 |

### Companion / Tool (Software or Reference)

| Project | Role |
|---------|------|
| 13 ESP Terminator | Web flasher for the deck's ESP32s |
| 15 ESP32-DIV | Superseded by HaleHound (Project 18) |
| 16 BlueJammer | Reference only — jamming is illegal; lawful detector side merged |
| 17 OUI-Spy | Detection merged into Flock + BLE firmware |

---

## Resources

| Resource | Description |
|----------|-------------|
| [OSINT / CTI](resources/osint/) | Open-source intelligence tools, techniques, and reference material |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| **Built** | Assembled, flashed, and working |
| Ready to Build | Have all or most parts needed |
| Ready to Start | Software-only, can begin immediately |
| Ready to Use | Web tool, no hardware needed |
| Troubleshooting | Built but has issues to resolve |
| In Transit | Hardware ordered, awaiting delivery |
| Blocked (ARM) | Hardware incompatibility preventing progress |
| Need Hardware | Missing key component(s) |
| Not Yet Purchased | Primary hardware not yet bought |

---

## Hardware Inventory

Full inventory of all purchased hardware with datasheets, drivers, and setup guides: **[INVENTORY.md](INVENTORY.md)**

### What I Have (curated core build hardware, ~$1,250-$1,450; see [INVENTORY.md](INVENTORY.md) for the full spend)

**Compute:**
- Raspberry Pi 5 8GB Starter Kit (CanaKit, 128GB SD)
- Raspberry Pi Zero 2 W Starter Kit (CanaKit, 32GB SD)
- ESP32 LoRa V3 Dev Board (Meshnology, SX1262 915MHz)
- ESP32 Gold Edition 3-Pack (Lonely Binary, IPEX antenna)
- ESP32-WROOM-32 Dev Board
- ESP32 GPIO Breakout Boards 5-Pack (AEDIKO)
- ESP32-C5 WiFi 6 Dev Boards x2 (Waveshare, **dual-band 2.4+5GHz**, IPEX antenna, cyberdeck Marauder C5)

**Displays:**
- 2.13" E-Ink HAT V4 (Waveshare, for Pwnagotchi)
- 5" HMI ESP32 Display (ELECROW CrowPanel, 800x480)
- 7" Touchscreen DSI x2 (Hosyond, for Pi)
- 5" Resistive TFT LCD (ELECROW, HDMI)
- 2.8" CYD Touchscreen 2-Pack (ESP32, ILI9341)
- 4.0" ESP32 Touchscreen (AITRIP, ST7796)

**Networking:**
- WiFi 6E USB Adapter (Panda PAU0F AXE3000, Kali-compatible)
- WiFi USB Dongle (RT5370, monitor mode capable)
- 915MHz LoRa Antennas 2-Pack
- WiFi/BT Antennas 2-Pack (Bingfu)
- 2.4G WiFi Antennas 2-Pack (DIYmall)
- SMA/RP-SMA Adapters 2-Pack

**Power:** PiSugar S 1200mAh (Pi Zero UPS), BreadVolt Power Supply

**Storage:** 128GB SD 6-Pack, 16GB SD 10-Pack, 32GB USB 10-Pack, SD card cases

**Tools:** Fluke 17B+ Multimeter, Soldering Pad, Kapton Tape, Component Kit, Breadboards, Pin Headers

**Input:** ProtoArc Foldable Keyboard, Rii K06 Mini Keyboard x2

---

## What I Still Need

| Item | For Project | Est. Price | Priority |
|------|-----------|-----------|----------|
| Flipper Zero | Flipper Zero | ~$170 | Medium |
| ESP32 WiFi Board (Dual C5 Touch) | Flipper Zero | ~$30-50 | Low (need Flipper first) |
| USB Rubber Ducky (Hak5) | Rubber Ducky | ~$80 | Low (can DIY) |
| Orbic Speed RC400L | RayHunter | ~$20-30 used | Medium |
| Lonely Binary ESP32 Gold (1 or 3-pack) | Cyberdeck Marauder (Gold #1 in use as standalone) | ~$12-36 | Medium |
| Foldable USB Solar Panel (20-28W) | Cyberdeck (solar charging) | ~$40-70 | Medium |
| GPS Module (USB or UART) | Kismet Wardriving | ~$15-25 | Medium |
| LattePanda Delta 3 (or x64 SBC) | Project Nomad | ~$200-300 | Low |
| Alfa AWUS036ACM (or similar) | Kismet (monitor mode) | ~$40-50 | Medium |
| ESP32-DIV board + RF shield (ESP32-S3, CC1101, 3x NRF24, IR) | ESP32-DIV | ~$40-70 DIY | Medium |
| NRF24L01+ PA/LNA module (+ 3.3V adapter/cap) | RF interference detect / Mousejack research / HaleHound | ~$8-12 | Low |
| CC1101 SubGHz Module (HW-863) | HaleHound SubGHz (replay, brute force, Tesla) | ~$5-8 | Medium |
| PN532 V3 NFC/RFID Module (SPI) | HaleHound NFC read/clone/brute | ~$5-8 | Medium |
| U.FL-to-SMA Pigtail Cables x2 | ESP32-C5 boards → SMA bulkhead (dual-band antennas) | ~$5-8 | **High** |
| Raspberry Pi Zero 2 WH | RaspyJack (dedicated, separate from Pwnagotchi) | ~$15-20 | Medium |
| Waveshare 1.44" LCD HAT | RaspyJack display (joystick + buttons) | ~$12-15 | Medium |
| USB OTG + USB-to-Ethernet Adapter | RaspyJack wired network attacks | ~$8-15 | Medium |
| LILYGO T-Display S3 (ESP32-S3, 1.9" TFT) | OUI-Spy (full BLE + WiFi, built-in screen) | ~$18-25 | **High** |
| Seeed XIAO ESP32-S3 (compact alt) | OUI-Spy (all modes, add external OLED) | ~$8-14 | Medium (alt to T-Display) |
| Passive Piezo Buzzer (3.3V, through-hole) | OUI-Spy (audio alerts) | ~$1-3 | High (with T-Display) |
| 3.7V LiPo Battery (500-1000mAh, JST 1.25mm) | OUI-Spy (portable power) | ~$5-8 | Medium |
| ~~Soldering Iron + Accessories~~ | ~~General~~ | -- | **Owned** |

---

## Projects I Can Start Right Now

### 1. OSINT (Software Only)
No hardware needed. Install tools and start practicing. See [OSINT resource guide](resources/osint/).

### 2. ESP32 Marauder
Have multiple ESP32 boards and CYD touchscreens. Flash via [ESP Terminator](https://espterminator.com) web flasher. See [project guide](projects/01-esp32-marauder/).

### 3. ESP Terminator (Web Flasher)
Already a web tool -- use it to flash Marauder, GhostESP, or Bruce firmware onto ESP32 boards. See [project guide](projects/13-esp-terminator/).

### 4. BLE Detection / Chasing Your Tail
ESP32 boards are ready. Flash BLE scanning firmware or build Chasing Your Tail NG. See [BLE guide](projects/08-ble-detection/) and [Chasing Your Tail guide](projects/10-chasing-your-tail/).

### 5. Flock / Drone Detection
ESP32 boards and WiFi antennas available. See [project guide](projects/06-flock-drone-detection/).

### 6. Kismet Wardriving
Pi 5, WiFi adapters, and storage ready. Need GPS module for full wardriving. See [project guide](projects/07-kismet-wardriving/).

### 7. OUI-Spy (WiFi-Only Quick Start)
Gold #3 or CYD #2 can run Flock-You WiFi promiscuous firmware today — no new hardware needed. For the full experience with BLE Detector, Foxhunter, and all modes, pick up a LILYGO T-Display S3 (~$20, built-in screen). See [project guide](projects/17-oui-spy/).

### 8. HaleHound + IoT Recon
CYD #2 can be flashed to HaleHound right now via [halehound.com](https://halehound.com/) web flasher. IoT Recon credential brute force works with just the CYD — no external modules needed. Add CC1101/NRF24/PN532 later for SubGHz/NFC. See [project guide](projects/18-halehound/).

### 9. ESP32-C5 Dual-Band Marauder
Both Waveshare ESP32-C5 boards are ready to flash with Marauder C5 firmware for 2.4+5GHz attacks. Use the [headless-marauder-gui](https://github.com/LxveAce/headless-marauder-gui) flasher with C5 target. Dual-band antennas via IPEX connector. See [Marauder C5 wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/ESP32%E2%80%90C5%E2%80%90DevKitC%E2%80%901).

---

## Projects Needing Troubleshooting

### Pwnagotchi -- Not Booting
- **Issue:** Display blank, not broadcasting on 2.4GHz (Marauder's sniffpwn detected nothing)
- **Hardware ruled out:** Fluke 17B+ confirmed proper voltage and continuity on all GPIO pins
- **Likely Cause:** Boot/image issue — Pi probably isn't running Pwnagotchi at all
- **Next Step:** Connect to PC via USB RNDIS, check if Pi responds to SSH at 10.0.0.2
- **Full debug plan:** [cyberdeck integration guide](projects/14-cyberdeck/integrations/03-pwnagotchi/)

### Meshtastic -- Node Not Detected via USB
- **Issue:** Computer doesn't detect node when plugged in
- **Likely Cause:** USB driver issue (CH340/CP2102) or charge-only cable
- **Action Items:** Install correct USB-serial driver, try a different USB cable, check Device Manager
- **Full troubleshooting guide:** [projects/04-meshtastic/](projects/04-meshtastic/)

### Project Nomad -- ARM Incompatibility
- **Issue:** Pi 5 (ARM) not supported; requires x64 architecture
- **Options:** Use LattePanda Delta 3 (x64), try QEMU/box64 emulation, or fork for ARM
- **Full analysis:** [projects/09-project-nomad/](projects/09-project-nomad/)

---

## Video References & Guides

### Project-Specific Videos
| Video | Project | Link |
|-------|---------|------|
| ESP32 Marauder Build Guide | ESP32 Marauder | [Watch](https://youtu.be/lcokJQMivwY) |
| ESP32 Marauder Deep Dive | ESP32 Marauder | [Watch](https://youtu.be/Co5FG3ivHhg) |
| Flock Camera Detection | Flock Detection | [Watch](https://www.youtube.com/watch?v=W_F4rEaRduk) |
| Drone Detection | Drone Detection | [Watch](https://youtu.be/qK5cIhksoYw) |
| Meshtastic for Dummies | Meshtastic | [Watch](https://youtu.be/igWP0O_VuUo) |
| OSINT Guide | OSINT | [Watch](https://www.youtube.com/watch?v=YKrXCmPp56k) |

### General / Unlabeled Videos
| Link | Notes |
|------|-------|
| [Video](https://youtu.be/km81ph7pZz8) | Security/hacking related |
| [Video](https://youtu.be/aZYvyy_R4jU) | Security/hacking related |
| [Video](https://youtu.be/XTnYVh7K6xQ) | Security/hacking related |
| [Video](https://youtu.be/EHW2XseuDDo) | Security/hacking related |
| [Video](https://youtu.be/uB0gr7Fh6lY) | Security/hacking related |
| [Video](https://youtu.be/cjXp3bBd2h8) | Security/hacking related |

### Instagram References
| Link |
|------|
| [Reel 1](https://www.instagram.com/reel/DZLDPGExR-1/) |
| [Reel 2](https://www.instagram.com/reel/DX4xKwSqEWJ/) |
| [Reel 3](https://www.instagram.com/reel/DYsfrtjJ608/) |

---

## Git Repositories

| Repository | Project | Link |
|-----------|---------|------|
| ESP32 Marauder | ESP32 Marauder | [justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder) |
| flock-you | Flock Detection | [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you) |
| USB Rubber Ducky Payloads | Rubber Ducky | [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads) |
| NyanBOX | NyanBOX | [jbohack/nyanBOX](https://github.com/jbohack/nyanBOX) |
| Haven MANET | Meshtastic | [buildwithparallel/haven-manet-ip-mesh-radio](https://github.com/buildwithparallel/haven-manet-ip-mesh-radio) |
| Meshtastic | Meshtastic | [meshtastic](https://github.com/meshtastic) |
| Project Nomad | Project Nomad | [Crosstalk-Solutions/project-nomad](https://github.com/Crosstalk-Solutions/project-nomad) |
| RayHunter | RayHunter | [EFForg/rayhunter](https://github.com/EFForg/rayhunter) |
| Chasing Your Tail NG | Chasing Your Tail | [ArgeliusLabs/Chasing-Your-Tail-NG](https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG) |
| Kismet | Kismet | [kismetwireless](https://github.com/kismetwireless) |
| Open Source CTI Tools | OSINT (Resource) | [BushidoUK/Open-source-tools-for-CTI](https://github.com/BushidoUK/Open-source-tools-for-CTI) |
| ESP32-DIV | ESP32-DIV | [cifertech/esp32-div](https://github.com/cifertech/esp32-div) |
| Headless Marauder GUI | Marauder / Cyberdeck | [LxveAce/headless-marauder-gui](https://github.com/LxveAce/headless-marauder-gui) |
| Mousejack (nRF24 research) | BlueJammer detector | [BastilleResearch/mousejack](https://github.com/BastilleResearch/mousejack) |
| OUI-Spy | OUI-Spy | [colonelpanichacks/oui-spy](https://github.com/colonelpanichacks/oui-spy) |
| OUI-Spy Unified Blue | OUI-Spy | [colonelpanichacks/oui-spy-unified-blue](https://github.com/colonelpanichacks/oui-spy-unified-blue) |
| OUI-Spy Omni (Luke Switzer) | OUI-Spy | [lukeswitz/oui-spy-unified-blue](https://github.com/lukeswitz/oui-spy-unified-blue) |
| OUI Master Database (88K+ OUIs) | OUI-Spy | [Ringmast4r/OUI-Master-Database](https://github.com/Ringmast4r/OUI-Master-Database) |
| HaleHound-CYD | HaleHound | [JesseCHale/HaleHound-CYD](https://github.com/JesseCHale/HaleHound-CYD) |
| ESP32 Marauder (C5 firmware) | Marauder (dual-band) | [justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder/wiki/ESP32%E2%80%90C5%E2%80%90DevKitC%E2%80%901) |
| RaspyJack | RaspyJack | [7h30th3r0n3/Raspyjack](https://github.com/7h30th3r0n3/Raspyjack) |
| RaspyJack Community Payloads | RaspyJack | [wickednull/raspyjack-payloads](https://github.com/wickednull/raspyjack-payloads) |
| GhostESP Revival (C5 support) | Dual-band alternative FW | [GhostESP](https://ghostesp.net/) |

---

## Project Ecosystem Map

```
                         ┌──────────────────────────┐
                         │   CYBERDECK (Pelican 1300) │
                         │  14 devices, 7 SMA, 12 SW │
                         └────────────┬─────────────┘
              ┌──────────────┬────────┼────────┬──────────────┐
              │              │        │        │              │
       ┌──────┴──────┐ ┌────┴────┐ ┌─┴──┐ ┌──┴─────┐ ┌──────┴──────┐
       │  WiFi/BLE   │ │  RECON  │ │MESH│ │WIRED   │ │SURVEILLANCE │
       │  OFFENSE    │ │         │ │COMM│ │ATTACKS │ │ DETECTION   │
       └──────┬──────┘ └────┬────┘ └─┬──┘ └──┬─────┘ └──────┬──────┘
       │ Gold#1 MAR  │ │ PAU0F    │ │Heltec│ │PiZero RJ│ │ Gold#2 FLK │
       │ C5#1 5G MAR │ │ RT5370   │ │LoRa  │ │HaleHound│ │ Gold#3 BLE │
       │ C5#2 5G SCN │ │ Kismet   │ │915MHz│ │IoT Rec  │ │ WROOM Drn  │
       └─────────────┘ └─────────┘ └──────┘ └─────────┘ │ CYT Tail   │
                                                         └────────────┘

       ┌──────────────────── STANDALONE ────────────────────────┐
       │                                                         │
       │  Flipper Zero (pocket)    Pwnagotchi (pocket AI)        │
       │  RayHunter (Orbic phone)  NyanBOX (pre-built)           │
       │  USB Rubber Ducky (USB)   Project Nomad (x64 blocked)   │
       └─────────────────────────────────────────────────────────┘

       ┌──────────────────── COMPANION ─────────────────────────┐
       │  ESP Terminator (flasher)  OSINT/CTI (software)         │
       │  ESP32-DIV (→ HaleHound)  BlueJammer (reference)        │
       │  OUI-Spy (→ Flock+BLE)                                  │
       └─────────────────────────────────────────────────────────┘
```

---

## Shared Hardware

Many projects share the same ESP32 boards, Raspberry Pi units, WiFi adapters, and accessories. Before starting a new project, check the [INVENTORY.md](INVENTORY.md) to see what you already have that can be reused.

**Key shared components:**
- **ESP32 boards** (Lonely Binary 3-pack, WROOM-32, AEDIKO breakouts) -> Marauder, BLE Detection, Flock Detection, Chasing Your Tail, OUI-Spy (WiFi-only modes)
- **ESP32-C5 boards** (Waveshare 2-pack) -> **Dual-band Marauder (2.4+5GHz)**, dual-band scanning/wardriving, IoT Recon
- **Raspberry Pi 5** -> Kismet, Project Nomad (if ARM solved), general server
- **Raspberry Pi Zero 2 W** -> Pwnagotchi, RaspyJack (need dedicated units)
- **Panda PAU0F WiFi 6E adapter** -> Kismet, general pentesting
- **SD cards & USB drives** -> All projects needing OS images or data storage
- **Fluke multimeter** -> Troubleshooting all electronics projects

---

## License

Released under the [MIT License](LICENSE). This repository is documentation, research, and build notes -- not production software or libraries.

---

## Disclaimer

These are **personal security-research and hardware projects shared for educational purposes.** Use any tools, firmware, or techniques referenced here **only** on systems, networks, and devices that you own or are explicitly authorized to test. Some techniques may be illegal to use against systems you do not own. You are solely responsible for complying with all applicable laws. Everything is provided **as-is, with no warranty** and **no liability** for misuse or damage. RF jamming and unauthorized interference are illegal in most jurisdictions -- this repo catalogs jammers for reference only and uses lawful detector firmware instead.

Security vulnerabilities or harmful/misleading guidance can be reported per the [security policy](SECURITY.md).

---

## Connect

- **Discord:** [discord.gg/lxveace](https://discord.gg/lxveace) -- questions, help, or to talk through this project
- **GitHub:** [@LxveAce](https://github.com/LxveAce)
- **Website:** [lxveace.com](https://lxveace.com)