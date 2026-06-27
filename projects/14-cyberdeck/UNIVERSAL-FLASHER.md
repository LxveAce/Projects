# Universal Flasher — Architecture & Roadmap

> **SHIPPED.** This concept shipped as **[LxveAce/universal-flasher](https://github.com/LxveAce/universal-flasher)** (v1.3.x)
> and was subsequently folded into the flagship **[LxveAce/cyber-controller](https://github.com/LxveAce/cyber-controller)**
> ([cybercontroller.org](https://cybercontroller.org)), which is now the maintained home for cyberdeck
> flashing and device management. This document is retained as the original architecture and roadmap
> notes; for current downloads and docs, see cyber-controller.

> **Built on:** [Headless Marauder GUI](https://github.com/LxveAce/headless-marauder-gui) scaffold

---

## 1. What This Is

A single desktop application that can flash, configure, and control **every device in the cyberdeck** — and any standalone build from this project collection. One app replaces:

- ESP Terminator (web flasher)
- Arduino IDE (for BLE/Flock/OUI-Spy firmware)
- PlatformIO (for Sky-Spy, OUI-Spy builds)
- Meshtastic Web Flasher
- qFlipper (Flipper Zero firmware)
- Raspberry Pi Imager (for Pwnagotchi/RaspyJack SD images)
- ADB manual commands (for RayHunter on Orbic)
- esptool CLI (for raw ESP32 flashing)

**One app. Every board. Every firmware. Download, run, plug in, flash.**

---

## 2. Why Build This

The cyberdeck has **13 devices** running **10+ different firmwares**. Right now, flashing each one requires a different tool, different workflow, different documentation. If a board dies in the field, you need to remember which flasher, which firmware variant, which partition table, which baud rate.

The universal flasher eliminates that. It knows every board, every firmware, every flash procedure. Select your device from a dropdown, pick the firmware, click FLASH.

---

## 3. What Already Exists (The Scaffold)

The [Headless Marauder GUI v1.3.0](https://github.com/LxveAce/headless-marauder-gui) already provides:

| Feature | Status |
|---------|--------|
| 4 UI frontends (PyQt5, Tkinter, Textual TUI, Flask browser) | Built |
| Multi-firmware flasher (Marauder, ESP32-DIV, Bruce) | Built |
| Auto chip detection (ESP32, S2, S3, C3, C5) | Built |
| esptool integration (app-only or full flash + erase) | Built |
| Suicide build flashing with SHA256 verification | Built |
| Firmware download with HTTPS allowlist | Built |
| Serial control (70+ Marauder commands) | Built |
| Live AP/Station tables, CSV/JSON export | Built |
| Standalone exe builds (Windows, Linux x64, ARM64) | Built |
| Mock mode for testing without hardware | Built |

**What needs to be added:**

| Feature | Effort |
|---------|--------|
| HaleHound-CYD firmware support | Low (esptool, same as Marauder) |
| GhostESP firmware support | Low (esptool, add board profiles) |
| Flock-You firmware support | Low (esptool/PlatformIO build) |
| OUI-Spy Unified Blue firmware support | Low (esptool/PlatformIO) |
| Sky-Spy (Drone RemoteID) firmware support | Low (esptool) |
| BLE Scanner / AirTag Scanner firmware | Low (esptool) |
| Chasing Your Tail NG firmware | Low (esptool) |
| Meshtastic firmware support | Medium (different partition layout) |
| Pwnagotchi SD image writer | Medium (new subsystem — dd/Win32DiskImager) |
| RaspyJack SD image writer | Medium (same subsystem as Pwnagotchi) |
| RayHunter ADB installer | Medium (new subsystem — ADB commands) |
| Flipper Zero firmware support | Hard (qFlipper protocol, different USB) |
| Per-device serial controller profiles | Medium (HaleHound commands differ from Marauder) |
| Device auto-identification (which firmware is running?) | Medium |

---

## 4. Architecture

### 4.1 Core Modules

```
universal-flasher/
├── core/
│   ├── flasher/
│   │   ├── esptool_backend.py      # ESP32 flashing (existing, extended)
│   │   ├── sd_image_backend.py     # Pi SD card imaging (NEW)
│   │   ├── adb_backend.py          # ADB-based installation (NEW)
│   │   └── flipper_backend.py      # Flipper Zero flashing (NEW, future)
│   ├── serial/
│   │   ├── marauder_controller.py  # Marauder commands (existing)
│   │   ├── halehound_controller.py # HaleHound commands (NEW)
│   │   ├── meshtastic_controller.py # Meshtastic serial (NEW)
│   │   └── generic_controller.py   # Raw serial for other firmware
│   ├── firmware/
│   │   ├── registry.py             # Firmware database (versions, URLs, board maps)
│   │   ├── downloader.py           # HTTPS firmware fetcher (existing, extended)
│   │   └── profiles/               # Per-firmware JSON profiles
│   │       ├── marauder.json
│   │       ├── marauder_c5.json
│   │       ├── ghostesp.json
│   │       ├── bruce.json
│   │       ├── halehound.json
│   │       ├── meshtastic.json
│   │       ├── flock_you.json
│   │       ├── oui_spy.json
│   │       ├── sky_spy.json
│   │       ├── ble_scanner.json
│   │       ├── cyt_ng.json
│   │       ├── pwnagotchi.json
│   │       ├── raspyjack.json
│   │       └── rayhunter.json
│   └── detection/
│       ├── chip_detect.py          # ESP32 chip type detection (existing)
│       ├── device_identify.py      # Identify running firmware via serial (NEW)
│       └── usb_detect.py           # Detect connected device type (NEW)
├── ui/
│   ├── qt/                         # PyQt5 GUI (existing, extended)
│   ├── tk/                         # Tkinter GUI (existing, extended)
│   ├── tui/                        # Textual TUI (existing, extended)
│   └── web/                        # Flask browser UI (existing, extended)
├── data/
│   └── firmware_registry.json      # Master firmware database
└── builds/
    └── ...                         # PyInstaller specs for standalone exe
```

### 4.2 Firmware Profile Schema

Each firmware gets a JSON profile that tells the flasher everything it needs:

```json
{
  "id": "marauder",
  "name": "ESP32 Marauder",
  "version": "1.12.1",
  "repo": "justcallmekoko/ESP32Marauder",
  "website": "https://github.com/justcallmekoko/ESP32Marauder",
  "flash_method": "esptool",
  "supported_chips": ["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c5"],
  "board_variants": {
    "multiboardS3": {
      "name": "Multiboard S3 (CYD, S3 devkits, etc. — NOT the classic-ESP32 Gold board)",
      "chip": "esp32s3",
      "files": {
        "bootloader": "esp32_marauder.ino.bootloader.bin",
        "partitions": "esp32_marauder.ino.partitions.bin",
        "boot_app0": "boot_app0.bin",
        "app": "esp32_marauder_v{version}_multiboardS3.bin"
      },
      "offsets": {
        "bootloader": "0x0",
        "partitions": "0x8000",
        "boot_app0": "0xe000",
        "app": "0x10000"
      },
      "baud": 921600
    },
    "esp32c5_devkitc": {
      "name": "ESP32-C5 DevKitC (Waveshare, dual-band)",
      "chip": "esp32c5",
      "files": {
        "app": "esp32_marauder_v{version}_esp32c5_devkitc.bin"
      },
      "offsets": {
        "app": "0x10000"
      },
      "baud": 921600
    }
  },
  "download_url_pattern": "https://github.com/justcallmekoko/ESP32Marauder/releases/download/v{version}/{filename}",
  "serial_controller": "marauder",
  "serial_baud": 115200,
  "has_suicide_build": true,
  "notes": "Gold boards are CLASSIC ESP32 (WROOM, CH340 USB-serial) — hardware-verified: esptool reports Device: ESP32, and the _multiboardS3.bin fails preflight on them. Flash the classic-ESP32 (WROOM) Marauder build, not the S3 build. C5 boards support 2.4+5GHz dual-band."
}
```

### 4.3 Flash Methods

| Method | Devices | How It Works |
|--------|---------|-------------|
| **esptool** | All ESP32 variants | Existing. esptool.py writes firmware bins at specific offsets. Chip auto-detection, baud negotiation, verify. |
| **SD Image** | Pwnagotchi, RaspyJack | NEW. Download .img.xz, decompress, write to SD card (dd on Linux, Win32DiskImager API on Windows). Show progress bar, verify hash. |
| **ADB** | RayHunter (Orbic) | NEW. Run `adb push` + `adb shell` commands to install RayHunter binary on the Orbic RC400L. Requires ADB drivers. |
| **qFlipper** | Flipper Zero | FUTURE. Flipper's USB DFU protocol. Complex — may just launch qFlipper externally. |

### 4.4 Device Auto-Detection Flow

```
USB device connected
    │
    ├── VID:PID matches ESP32 USB-serial chip?
    │   ├── CH340/CH341 (1a86:7523) → ESP32 classic / Gold / WROOM
    │   ├── CP2102 (10c4:ea60) → Heltec LoRa V3 / some ESP32s
    │   ├── ESP32-S2/S3 native USB (303a:1001) → ESP32-S3 boards
    │   └── ESP32-C5 native USB (303a:1001) → C5 boards
    │   │
    │   └── Run esptool chip_id → identify exact chip
    │       └── Show compatible firmware list for that chip
    │
    ├── VID:PID matches Qualcomm diagnostic? → Orbic / RayHunter
    │   └── Run adb devices → confirm connection
    │       └── Show RayHunter install option
    │
    ├── VID:PID matches Flipper Zero? → Flipper
    │   └── Show Flipper firmware options
    │
    └── SD card reader detected?
        └── Show Pi image options (Pwnagotchi, RaspyJack)
```

---

## 5. Firmware Registry (All Supported Firmware)

### ESP32-Based (esptool flash method)

| Firmware | Latest | Boards | Repo | Flash Tool |
|----------|--------|--------|------|------------|
| ESP32 Marauder | v1.12.1 | Gold (classic ESP32 / WROOM, CH340), CYD, C5, S3, Cardputer | justcallmekoko/ESP32Marauder | esptool |
| GhostESP | v1.9.10 | S3, C5, XIAO, DevKitC | GhostESP-Revival/GhostESP | esptool |
| Bruce | v1.15 | S3, CYD, C5, Cardputer, many more | BruceDevices/firmware | esptool |
| HaleHound-CYD | v3.5.5 | CYD 2.8" (ESP32-2432S028R) | JesseCHale/HaleHound-CYD | esptool |
| Meshtastic | latest stable | Heltec LoRa V3, T-Beam, XIAO | meshtastic/firmware | esptool |
| Flock-You | promiscuous-dev | ESP32 Gold, XIAO S3 | colonelpanichacks/flock-you | PlatformIO → bin → esptool |
| OUI-Spy Unified Blue | latest | ESP32-S3 (T-Display, XIAO) | colonelpanichacks/oui-spy-unified-blue | PlatformIO → bin → esptool |
| Sky-Spy (Drone RemoteID) | latest | ESP32-S3, WROOM-32 | colonelpanichacks/Sky-Spy | PlatformIO → bin → esptool |
| ESP32 AirTag Scanner | latest | ESP32-S3 | MatthewKuKanich/ESP32-AirTag-Scanner | Arduino → bin → esptool |
| Chasing Your Tail NG | latest | ESP32 | ArgeliusLabs/Chasing-Your-Tail-NG | Arduino → bin → esptool |
| ESP32-DIV | latest | ESP32-S3 + CC1101/NRF24 | cifertech/esp32-div | Arduino → bin → esptool |

### Pi-Based (SD image flash method)

| Firmware | Latest | Board | Repo | Flash Tool |
|----------|--------|-------|------|------------|
| Pwnagotchi | latest | Pi Zero 2W | jayofelern/pwnagotchi | SD image write |
| RaspyJack | v1.0.6 | Pi Zero 2W | 7h30th3r0n3/Raspyjack | SD image write |
| Kali Linux ARM | 2026.x | Pi 5 | kali.org | SD image write |

### Other (specialized flash methods)

| Firmware | Latest | Device | Repo | Flash Tool |
|----------|--------|--------|------|------------|
| RayHunter | latest | Orbic RC400L | EFForg/rayhunter | ADB push + install |
| Flipper Momentum | latest | Flipper Zero | Next-Flip/Momentum-Firmware | qFlipper (external) |

---

## 6. UI Changes

### New "Device" Tab (replaces single firmware selector)

```
┌─────────────────────────────────────────────────────────┐
│  UNIVERSAL FLASHER                                       │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Flasher  │ Control  │ Monitor  │ Devices  │ Guide       │
├──────────┴──────────┴──────────┴──────────┴─────────────┤
│                                                          │
│  Connected: COM3 — ESP32-S3 (Lonely Binary Gold)         │
│                                                          │
│  ┌─ Device ─────────┐  ┌─ Firmware ──────────────────┐  │
│  │ ESP32-S3 (Gold)  ▼│  │ ESP32 Marauder v1.12.1    ▼│  │
│  └──────────────────┘  │ GhostESP v1.9.10            │  │
│                         │ Bruce v1.15                  │  │
│  ┌─ Flash Mode ─────┐  │ Flock-You (promiscuous-dev)  │  │
│  │ Full Flash       ▼│  │ BLE AirTag Scanner           │  │
│  └──────────────────┘  │ Chasing Your Tail NG          │  │
│                         └─────────────────────────────┘  │
│  [ ] Suicide Build (Marauder only)                       │
│  [ ] Erase flash first                                   │
│                                                          │
│  [  DETECT CHIP  ]     [  FLASH  ]     [  ERASE  ]      │
│                                                          │
│  Status: Ready                                           │
│  ████████████████░░░░░░░░░░░░░░░░ 45%                   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### New "Devices" Dashboard Tab

```
┌──────────────────────────────────────────────────────────┐
│  CYBERDECK DEVICES                                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Gold #1     │  │ Gold #2     │  │ Gold #3     │     │
│  │ Marauder    │  │ Flock-You   │  │ BLE Scanner │     │
│  │ v1.12.1     │  │ prom-dev    │  │ latest      │     │
│  │ ● Online    │  │ ● Online    │  │ ○ Offline   │     │
│  │ [Control]   │  │ [Control]   │  │ [Flash]     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ C5 #1       │  │ C5 #2       │  │ Heltec V3   │     │
│  │ Marauder 5G │  │ GhostESP    │  │ Meshtastic  │     │
│  │ v1.12.1     │  │ v1.9.10     │  │ 2.5.x       │     │
│  │ ● Online    │  │ ● Online    │  │ ● Online    │     │
│  │ [Control]   │  │ [Control]   │  │ [Messages]  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ CYD #2      │  │ Pi Zero     │  │ Orbic       │     │
│  │ HaleHound   │  │ RaspyJack   │  │ RayHunter   │     │
│  │ v3.5.5      │  │ v1.0.6      │  │ latest      │     │
│  │ ● Online    │  │ ○ Offline   │  │ ● Online    │     │
│  │ [Control]   │  │ [Flash SD]  │  │ [Dashboard] │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  [Flash All Outdated]  [Refresh]  [Export Config]        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 7. Implementation Phases

### Phase 1: Extend ESP32 Flasher (2-3 days)

Add firmware profiles for all ESP32-based firmware. The esptool backend already works — this is mostly adding JSON profiles and download URLs:

- [ ] HaleHound-CYD profile + download
- [ ] GhostESP profile + download
- [ ] Flock-You profile (pre-compiled bins or PlatformIO build)
- [ ] OUI-Spy Unified Blue profile
- [ ] Sky-Spy profile
- [ ] BLE AirTag Scanner profile
- [ ] Chasing Your Tail NG profile
- [ ] Meshtastic profile (different partition layout)
- [ ] Firmware version checking (compare installed vs latest)

### Phase 2: SD Image Writer (1-2 days)

New subsystem for Pi-based devices:

- [ ] Image download + decompression (.img.xz, .img.gz, .zip)
- [ ] SD card detection and selection
- [ ] Block-level write with progress bar
- [ ] Hash verification after write
- [ ] Pwnagotchi image profile
- [ ] RaspyJack image profile
- [ ] Kali ARM image profile

### Phase 3: ADB Backend (1 day)

New subsystem for Orbic/Android devices:

- [ ] ADB device detection
- [ ] ADB push + shell command execution
- [ ] RayHunter binary download and install
- [ ] RayHunter status check (is it running?)
- [ ] Web UI port forwarding via ADB

### Phase 4: Device Dashboard (2-3 days)

The "Devices" tab that shows all connected cyberdeck devices:

- [ ] Multi-port serial enumeration
- [ ] Device identification (what firmware is each port running?)
- [ ] Per-device control panels
- [ ] Status indicators (online/offline/outdated)
- [ ] One-click "Flash All Outdated" button

### Phase 5: Rename & New Repo (1 day)

- [x] Fork headless-marauder-gui to new repo (shipped as LxveAce/universal-flasher)
- [x] Update all branding, README, PyInstaller specs
- [x] Keep headless-marauder-gui as the Marauder-focused release
- [x] New repo becomes the full cyberdeck management tool (folded into LxveAce/cyber-controller — cybercontroller.org)

---

## 8. Technical Constraints

- **Python-only** — must stay Python for cross-platform exe builds (PyInstaller)
- **No cloud** — all firmware downloads are direct from GitHub Releases, no intermediary
- **Offline mode** — cache firmware binaries locally for field re-flashing without internet
- **HTTPS-only** — existing security hardening (host allowlist, path traversal protection) extends to all new download sources
- **Single exe** — the standalone binary must include esptool, ADB client, and SD imaging tools
- **ARM64 support** — must run on the cyberdeck's own Pi 5 (Kali ARM64)

---

*This was the original planning document. The tool shipped as LxveAce/universal-flasher (v1.3.x) and is now maintained as part of LxveAce/cyber-controller (cybercontroller.org).*
