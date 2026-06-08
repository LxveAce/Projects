# Security & Hardware Projects

A curated collection of cybersecurity, wireless, and hardware hacking projects -- from ESP32 tools to mesh networking to surveillance detection. Each project has its own folder with deep research, step-by-step build guides, and resource links.

**General Resource Hub:** [BushidoUK/Open-source-tools-for-CTI](https://github.com/BushidoUK/Open-source-tools-for-CTI)

---

## Project Directory

| # | Project | Status | Difficulty | Description |
|---|---------|--------|-----------|-------------|
| 01 | [ESP32 Marauder](projects/01-esp32-marauder/) | **Built** (CYD + headless) | Medium | WiFi/Bluetooth offensive & defensive toolkit on ESP32 |
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
| 14 | [Cyberdeck](projects/14-cyberdeck/) | Brainstorm | Hard | All-in-one portable security rig (Pi 5 + ESP32s + Meshtastic + Kismet) |
| 15 | [ESP32-DIV](projects/15-esp32-div/) | Evaluating | Medium | Open-source ESP32-S3 multitool — Sub-GHz, IR, RFID/NFC, 2.4GHz (Flipper-class) |
| 16 | [BlueJammer-V2](projects/16-bluejammer/) | Reference only | -- | 2.4GHz RF jammer — cataloged for reference; deck uses the lawful **detector** instead |

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

### What I Have (37 items + extras, ~$1,250-$1,450 total)

**Compute:**
- Raspberry Pi 5 8GB Starter Kit (CanaKit, 128GB SD)
- Raspberry Pi Zero 2 W Starter Kit (CanaKit, 32GB SD)
- ESP32 LoRa V3 Dev Board (Meshnology, SX1262 915MHz)
- ESP32 Gold Edition 3-Pack (Lonely Binary, IPEX antenna)
- ESP32-WROOM-32 Dev Board
- ESP32 GPIO Breakout Boards 5-Pack (AEDIKO)
- ESP32-C5 WiFi 6 Dev Boards x2 (Waveshare, dual-band)

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
| GPS Module (USB or UART) | Kismet Wardriving | ~$15-25 | Medium |
| LattePanda Delta 3 (or x64 SBC) | Project Nomad | ~$200-300 | Low |
| Alfa AWUS036ACM (or similar) | Kismet (monitor mode) | ~$40-50 | Medium |
| ESP32-DIV board + RF shield (ESP32-S3, CC1101, 3x NRF24, IR) | ESP32-DIV | ~$40-70 DIY | Medium |
| NRF24L01+ PA/LNA module (+ 3.3V adapter/cap) | RF interference detect / Mousejack research | ~$8-12 | Low |
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

---

## Project Ecosystem Map

```
                    ┌─────────────────────────────────────────┐
                    │          SECURITY TOOLKIT               │
                    └─────────────────────────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
    ┌──────┴──────┐           ┌───────┴───────┐          ┌──────┴──────┐
    │   WIRELESS  │           │  SURVEILLANCE │          │  OFFENSIVE  │
    │   DEFENSE   │           │  DETECTION    │          │   TOOLS     │
    └──────┬──────┘           └───────┬───────┘          └──────┬──────┘
           │                          │                          │
    ┌──────┴──────┐           ┌───────┴───────┐          ┌──────┴──────┐
    │ RayHunter   │           │ Flock Detect  │          │ Marauder    │
    │ Kismet      │           │ Drone Detect  │          │ Flipper     │
    │ Meshtastic  │           │ Chasing Tail  │          │ NyanBOX     │
    │ BLE Detect  │           │ BLE Tracking  │          │ Rubber Ducky│
    └─────────────┘           └───────────────┘          │ Pwnagotchi  │
                                                         └─────────────┘
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
    ┌──────┴──────┐           ┌───────┴───────┐          ┌──────┴──────┐
    │    COMMS    │           │ INTELLIGENCE  │          │   PLATFORM  │
    └──────┬──────┘           └───────┬───────┘          └──────┬──────┘
    │ Meshtastic  │           │ OSINT / CTI   │          │ Proj Nomad  │
    │ Proj Nomad  │           │ Kismet Data   │          │ ESP Terminal│
    └─────────────┘           └───────────────┘          └─────────────┘
```

---

## Shared Hardware

Many projects share the same ESP32 boards, Raspberry Pi units, WiFi adapters, and accessories. Before starting a new project, check the [INVENTORY.md](INVENTORY.md) to see what you already have that can be reused.

**Key shared components:**
- **ESP32 boards** (Lonely Binary 3-pack, WROOM-32, AEDIKO breakouts) -> Marauder, BLE Detection, Flock Detection, Chasing Your Tail
- **Raspberry Pi 5** -> Kismet, Project Nomad (if ARM solved), general server
- **Raspberry Pi Zero 2 W** -> Pwnagotchi
- **Panda PAU0F WiFi 6E adapter** -> Kismet, general pentesting
- **SD cards & USB drives** -> All projects needing OS images or data storage
- **Fluke multimeter** -> Troubleshooting all electronics projects
