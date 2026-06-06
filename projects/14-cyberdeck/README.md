# Project 14: The Cyberdeck -- All-In-One Portable Security Toolkit

> **Status:** Brainstorm / Concept Phase
> **Goal:** Integrate the Pi 5, ESP32 Marauder, Meshtastic, Pwnagotchi, Flock detection, BLE scanning, Chasing Your Tail, Kismet wardriving, and all associated hardware into a single portable, battery-powered cyberdeck case.

---

## Table of Contents

1. [Concept Overview](#1-concept-overview)
2. [Hardware Manifest -- What Goes Inside](#2-hardware-manifest----what-goes-inside)
3. [Form Factor Options](#3-form-factor-options)
4. [Internal Layout Design](#4-internal-layout-design)
5. [Power System](#5-power-system)
6. [Antenna Management](#6-antenna-management)
7. [Display Strategy](#7-display-strategy)
8. [Connectivity and Switching](#8-connectivity-and-switching)
9. [Cooling](#9-cooling)
10. [Modularity and Quick-Swap](#10-modularity-and-quick-swap)
11. [Software Integration](#11-software-integration)
12. [Bill of Materials (Case + New Parts)](#12-bill-of-materials)
13. [Build Phases](#13-build-phases)
14. [Inspiration and References](#14-inspiration-and-references)

---

## 1. Concept Overview

### What Is a Cyberdeck?

A cyberdeck is a custom-built, self-contained portable computer -- typically housed in a ruggedized case (Pelican, Apache, ammo can, or 3D-printed chassis) -- designed to be a grab-and-go workstation for a specific purpose. In this case: **wireless security research, surveillance detection, and mesh communications.**

### Design Philosophy

This cyberdeck is NOT just "a Pi in a box." It's a multi-tool that consolidates **every project in this repo** into a single portable rig that can:

- Run ESP32 Marauder for WiFi/BLE offensive testing
- Detect Flock ALPR surveillance cameras while driving
- Scan for BLE trackers (AirTags, Tiles, SmartTags) following you
- Operate a Meshtastic mesh node for off-grid comms
- Run Kismet wardriving with GPS logging
- Detect nearby drones via RemoteID
- All simultaneously, from one battery, with one display

### Core Principles

1. **Everything runs at once** -- not "swap this board to do that." Dedicated boards per function
2. **Field-portable** -- carries by handle, runs on battery for 4+ hours
3. **Antenna sanity** -- external SMA bulkheads, not a rat's nest of wires
4. **Modular bays** -- boards mount on removable plates so you can swap/upgrade
5. **One screen to rule them all** -- Pi 5 as the brain, 7" touchscreen as primary display, secondary status screens optional
6. **Stealth option** -- closed case looks like camera equipment, not a hacking rig

---

## 2. Hardware Manifest -- What Goes Inside

### From Your Current Inventory

| Component | Role in Cyberdeck | Notes |
|-----------|------------------|-------|
| **Raspberry Pi 5 8GB** | Main brain. Runs Kismet, controls ESP32s via serial, hosts web dashboards | Central compute, USB hub for adapters |
| **Lonely Binary ESP32 Gold #1** | ESP32 Marauder -- WiFi/BLE offensive toolkit | IPEX antenna -> SMA bulkhead |
| **Lonely Binary ESP32 Gold #2** | Flock camera detection (flock-you firmware) | IPEX antenna -> SMA bulkhead |
| **Lonely Binary ESP32 Gold #3** | BLE Detection / Chasing Your Tail scanner | IPEX antenna -> SMA bulkhead |
| **Heltec LoRa V3** | Meshtastic mesh node (915MHz) | IPEX -> SMA bulkhead (LoRa antenna) |
| **ESP32-WROOM-32 generic** | Drone RemoteID detection OR spare | Internal PCB antenna sufficient |
| **Hosyond 7" DSI Touchscreen** | Primary display | DSI ribbon to Pi 5 |
| **CYD 2.8" Touchscreen #1** | Secondary status display (Marauder GUI) | Standalone ESP32 display |
| **Panda PAU0F WiFi 6E adapter** | Kismet primary WiFi (monitor mode) | USB 3.0 to Pi 5 |
| **RT5370 WiFi dongle** | Kismet secondary 2.4GHz monitor | USB 2.0 to Pi 5 |
| **Rii K06 Mini Keyboard** | Input for the cyberdeck | Bluetooth, backlit |
| **DIYmall 2.4G antennas (2x)** | WiFi antennas for ESP32 boards | U.FL pigtails |
| **Bingfu dual-band antennas (2x)** | WiFi/BT antennas (2.4/5.8GHz) | RP-SMA |
| **915MHz LoRa antennas (2x)** | Meshtastic antenna | IPEX + SMA |
| **Boobrie RP-SMA to SMA adapters** | Antenna adapter chain | |
| **128GB Micro SD cards** | Pi 5 OS + Kismet data | |
| **32GB USB flash drives** | Data export | |
| **Fluke 17B+ Multimeter** | Build/debug tool (external) | |
| **Soldering iron + workstation** | Build tool (external) | |

### Pwnagotchi: Separate or Integrated?

**Recommendation: Keep Pwnagotchi separate.** The Pi Zero 2W + e-ink display + PiSugar battery is already a perfect pocket-sized unit. Integrating it into the cyberdeck adds complexity with minimal benefit -- Pwnagotchi is designed to be autonomous and pocket-carried.

The cyberdeck CAN have an internal "Pwnagotchi dock" -- a slot where you drop the assembled Pwnagotchi unit in for charging and data offload via USB, but it runs independently.

---

## 3. Form Factor Options

### Option A: Pelican 1200 Case (Recommended)

```
┌─────────────────────────────────────────┐
│          PELICAN 1200 (TOP VIEW)         │
│                                         │
│  External dims: 10.6" x 9.7" x 4.9"    │
│  Internal dims: 9.2" x 7.2" x 4.1"     │
│  Weight: 2.3 lbs empty                  │
│  Color: Black                           │
│  Price: ~$35-45                          │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   7" DSI DISPLAY (lid-mounted)   │  │
│  │   800x480 touchscreen            │  │
│  │   Hinged open = laptop mode      │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐  │
│  │  Pi 5   │ │ ESP32s  │ │ Battery  │  │
│  │  + USB  │ │ (x4-5)  │ │ + BMS    │  │
│  │  hub    │ │ on rail │ │          │  │
│  └─────────┘ └─────────┘ └──────────┘  │
│                                         │
│  ─── SMA BULKHEADS ON SIDE PANEL ───── │
│  [WiFi1] [WiFi2] [WiFi3] [LoRa] [BLE]  │
│                                         │
└─────────────────────────────────────────┘
```

**Pros:** Waterproof (IP67), crush-resistant, professional look (camera case), proven cyberdeck platform, easy to drill for SMA bulkheads, padded interior, pressure valve, lifetime warranty.

**Cons:** Limited vertical space (4.1" internal), tight fit for everything, need to cut foam precisely.

**Price:** ~$70-84 on Amazon

**Open-source reference:** Jake Simek's [Pelican-Deck](https://github.com/Jake-Simek/Pelican-Deck) -- full 3D-printable internal framework for a Pelican 1150, Kali Linux, water-resistant panel-mount I/O. Adaptable to the 1200.

### Option B: Pelican 1300 Case

```
Internal dims: 9.2" x 7.0" x 5.8"
```

**Same footprint as 1200 but 1.7" more vertical space.** Much easier to fit the Pi 5 + USB hub + battery stack. Recommended if vertical clearance is an issue.

**Price:** ~$85-100

**Reference build:** Jay Doscher's [Recovery Kit v2](https://doscher.com/recovery-kit-version-2/) uses this exact case with a Pi 5, 7" DSI, Drop Planck keyboard, Shargeek Storm 2 battery, and 5-port Ethernet switch. STL files available via membership.

### Option C: Apache 2800 (Harbor Freight)

```
Internal dims: 10.5" x 7.5" x 4.0"
```

**Budget Pelican clone.** Similar protection, slightly larger footprint, much cheaper.

**Pros:** $20-25, widely available, good enough protection.
**Cons:** Less robust latches, no pressure valve, not truly IP67.

### Option D: Pelican 1400 Case (Large Build)

```
Internal dims: 11.8" x 8.3" x 5.5"
```

**Roomiest option.** Enough space for everything with room to spare. Could include a full-size keyboard tray, larger battery, and dedicated Pwnagotchi dock.

**Pros:** Plenty of room, easy cable management, room for future expansion.
**Cons:** Bulkier, heavier, more expensive (~$80-110), less "grab and go."

### Option E: 3D-Printed Custom Chassis

Design a custom frame in Fusion 360 / OpenSCAD. Mount the Pi 5, ESP32 rail, display, and battery on a single 3D-printed skeleton that either stands alone or drops into any case.

**Pros:** Perfect fit, custom mounting for every component, can design snap-in bays.
**Cons:** Requires 3D printer access, longer build time, less ruggedized unless enclosed.

### Recommendation

**Start with the Pelican 1300** (~$50). It has the 1200 footprint but extra height that makes cable routing and component stacking much easier. You can always rebuild into a 3D-printed chassis later once you know exactly what fits.

---

## 4. Internal Layout Design

### Layer Architecture (Bottom to Top)

```
LAYER 1 (Bottom) -- Power
┌─────────────────────────────────────┐
│  [LiPo Battery Pack]  [BMS Board]  │
│  [USB-C PD Trigger]   [5V/3.3V     │
│                        Buck Conv.]  │
│  ─── Power distribution bus ─────  │
└─────────────────────────────────────┘

LAYER 2 (Middle) -- Compute
┌─────────────────────────────────────┐
│  ┌────────┐  ┌──────────────────┐  │
│  │  Pi 5  │  │   ESP32 Rail     │  │
│  │  8GB   │  │  ┌──┐┌──┐┌──┐   │  │
│  │        │  │  │M ││F ││B │   │  │
│  │ [USB]──┤  │  │a ││l ││L │   │  │
│  │ [DSI]──┤  │  │r ││o ││E │   │  │
│  │ [ETH]  │  │  │a ││c ││  │   │  │
│  │ [GPIO] │  │  │u ││k ││D │   │  │
│  └────────┘  │  │d ││  ││e │   │  │
│              │  └──┘└──┘└──┘   │  │
│  [USB Hub]   │  [Heltec] [Spare]│  │
│              └──────────────────┘  │
│  [Panda WiFi 6E]  [RT5370]        │
└─────────────────────────────────────┘

LAYER 3 (Top / Lid) -- Display + I/O
┌─────────────────────────────────────┐
│  ┌───────────────────────────────┐  │
│  │  Hosyond 7" DSI Touchscreen   │  │
│  │  (mounted in lid, hinges open) │  │
│  └───────────────────────────────┘  │
│                                     │
│  [CYD 2.8" status]  [Status LEDs]  │
│                                     │
│  ── SIDE PANEL (drilled) ────────  │
│  [SMA] [SMA] [SMA] [SMA] [SMA]    │
│  [USB-C IN] [USB-A OUT] [Switch]   │
└─────────────────────────────────────┘
```

### ESP32 Mounting Rail

All ESP32 boards mount on a **DIN rail** or custom 3D-printed rail inside the case:

```
ESP32 RAIL (top view)
┌──────────────────────────────────────────┐
│ [Lonely Binary #1]  [Lonely Binary #2]   │
│  Marauder             Flock Detection    │
│  ↓ U.FL pigtail       ↓ U.FL pigtail    │
│  → SMA Bulkhead #1    → SMA Bulkhead #2 │
│                                          │
│ [Lonely Binary #3]  [Heltec LoRa V3]    │
│  BLE/CYT Detection   Meshtastic         │
│  ↓ U.FL pigtail       ↓ IPEX cable      │
│  → SMA Bulkhead #3    → SMA Bulkhead #4 │
│                                          │
│ [WROOM-32 generic]  [CYD 2.8" display]  │
│  Drone RemoteID      Marauder touch GUI  │
│  (internal antenna)  (serial to Gold #1) │
└──────────────────────────────────────────┘
```

Each ESP32 connects to the Pi 5 via USB for serial communication and power. The Pi 5 can send commands, read scan data, and aggregate results from all boards simultaneously.

---

## 5. Power System

### Requirements

| Device | Voltage | Current (typical) | Current (peak) |
|--------|---------|-------------------|----------------|
| Pi 5 8GB | 5V | 800mA | 2.5A (under load) |
| ESP32 x4 | 5V (USB) | 100-180mA each | 300mA each (WiFi TX) |
| Heltec LoRa V3 | 5V (USB) | 80mA | 200mA (LoRa TX) |
| CYD 2.8" display | 5V (USB) | 150mA | 250mA |
| 7" DSI display | 5V (DSI) | 400mA | 500mA |
| Panda PAU0F WiFi | 5V (USB 3.0) | 400mA | 600mA |
| RT5370 WiFi | 5V (USB) | 150mA | 200mA |
| USB Hub | 5V | 50mA | 100mA |
| **TOTAL** | | **~2.7A** | **~5.0A** |

### Battery Sizing

At ~3A average draw:
- **4 hours runtime** = 3A x 4h = 12Ah at 5V = 60Wh
- **6 hours runtime** = 3A x 6h = 18Ah at 5V = 90Wh
- **8 hours runtime** = 3A x 8h = 24Ah at 5V = 120Wh

### Option A: Off-the-Shelf USB-C PD Power Bank (Simplest)

Use a high-capacity USB-C PD power bank that supports 5V/3A+ output:

| Power Bank | Capacity | Output | Est. Runtime | Price |
|-----------|----------|--------|-------------|-------|
| Anker 737 (24,000mAh) | 86.4Wh | 5V/3A USB-C + USB-A | ~5-6 hours | ~$80 |
| Baseus 20,000mAh PD | 72Wh | 5V/3A | ~4-5 hours | ~$35 |
| Anker 347 (25,600mAh) | 92Wh | 5V/3A | ~5-6 hours | ~$50 |

**Pros:** Zero build complexity, pass-through charging, built-in protection.
**Cons:** Bulky, can't customize form factor, some don't supply 5V/3A reliably.

### Option B: Custom LiPo Pack + BMS (Best for Custom Fit)

Build a battery pack that fits the case perfectly:

```
POWER SYSTEM DIAGRAM

[18650 LiPo Cells] ──→ [BMS Board] ──→ [5V Buck Converter] ──→ [USB Hub]
  3S2P or 4S2P          (protection,     (XL4015 or LM2596)     ↓
  ~11.1V or 14.8V        balancing)                          [Pi 5]
  6000-8000mAh                                               [ESP32s]
                                                             [Display]

  [USB-C PD Input] ──→ [TP4056 or IP5306 Charger] ──→ [LiPo Cells]
```

**Components:**
| Part | Purpose | Price |
|------|---------|-------|
| 18650 cells x6 (3S2P) | 11.1V, ~6000mAh (66Wh) | ~$20-30 |
| 3S BMS board (25A) | Cell protection + balancing | ~$5-8 |
| XL4015 5A buck converter | 11.1V → 5V/5A regulated | ~$5-8 |
| TP4056 or dedicated LiPo charger | USB-C charging input | ~$3-5 |
| 18650 cell holders | Physical mounting | ~$3-5 |
| Voltage display module | Battery level indicator | ~$2-3 |
| **Total** | | **~$40-55** |

**Pros:** Custom form factor, higher capacity, proper power distribution.
**Cons:** Requires soldering, LiPo safety knowledge, more complex build.

### Option C: PiSugar Pro / Pimoroni UPS (Pi-Specific)

- **PiSugar 3 Plus** (~$45) -- 5000mAh, mounts on Pi 5, UPS functionality, software battery monitoring
- **Pimoroni LiPo SHIM** (~$15) -- Thin LiPo power HAT for Pi
- **Waveshare UPS HAT (E)** (~$30-35) -- Four 21700 cells, USB-C PD 3.0 (40W bidirectional fast charge), 5V/6A output. Enough current for Pi 5 AND the ESP32 rail from one board
- **Waveshare UPS HAT (B)** (~$22) -- Dual 18650, 5V/5A, I2C battery fuel gauge

PiSugar and Pimoroni only power the Pi 5 itself. The Waveshare UPS HAT (E) is the standout -- 5V/6A output is enough for the entire cyberdeck from one board, with I2C monitoring and graceful shutdown signaling.

### Recommended Approach

**Hybrid: PD Power Bank + Powered USB Hub**

1. Large USB-C PD power bank (20,000-25,000mAh) mounted in the bottom layer
2. USB-C PD output → Pi 5 (direct, 5V/3A)
3. USB-A output → Powered USB hub (7-port) → all ESP32s, WiFi adapters
4. Pass-through charging via USB-C input on the case's side panel

This is the simplest approach with no custom battery wiring, and you can swap/upgrade the power bank later.

---

## 6. Antenna Management

### The Problem

You have 5+ devices that need antennas, all crammed into a metal (or plastic) case. Internal antennas will be shielded and interfere with each other. External antennas sticking out everywhere looks insane and snags on things.

### The Solution: SMA Bulkhead Panel

Drill 5-6 holes in one side of the case and install **SMA bulkhead connectors** (panel-mount). Each ESP32's U.FL pigtail routes internally to its dedicated bulkhead. Antennas screw on externally.

```
CASE SIDE PANEL (external view)

┌──────────────────────────────────────────┐
│                                          │
│  [SMA]  [SMA]  [SMA]  [SMA]  [SMA]     │
│   WiFi   WiFi   WiFi   LoRa   BLE      │
│   2.4G   2.4G   2.4G   915M   2.4G     │
│   MAR    FLOCK  KISM   MESH   BLE      │
│                                          │
│  [USB-C]  [USB-A]  [PWR SW]  [LED]     │
│   Charge   Data     ON/OFF   Status    │
│                                          │
└──────────────────────────────────────────┘
```

### Antenna Assignments

| Bulkhead # | Device | Antenna | Frequency |
|-----------|--------|---------|-----------|
| SMA 1 | Lonely Binary #1 (Marauder) | Bingfu 3dBi dual-band | 2.4/5.8 GHz |
| SMA 2 | Lonely Binary #2 (Flock) | DIYmall 3dBi | 2.4 GHz |
| SMA 3 | Panda PAU0F (Kismet) | Bingfu 3dBi dual-band | 2.4/5/6 GHz |
| SMA 4 | Heltec LoRa V3 (Meshtastic) | 915MHz LoRa 3dBi | 915 MHz |
| SMA 5 | Lonely Binary #3 (BLE) | DIYmall 3dBi | 2.4 GHz |

### Internal Routing

- U.FL pigtails from each ESP32 IPEX connector route to SMA bulkheads via the shortest path
- Keep pigtails away from power cables (EMI)
- Use adhesive cable clips to secure pigtail routing inside the case
- The Panda PAU0F has its own antenna -- use an SMA extension cable from the adapter to a bulkhead
- The RT5370 uses its internal antenna (secondary, short-range OK)

### Field Antenna Options

For normal carry: screw on short stubby antennas (3dBi) on all bulkheads.
For wardriving: swap the Kismet bulkhead antenna for a 9dBi magnetic-base roof-mount.
For directional work: swap Marauder bulkhead for a panel or Yagi antenna.

### Antenna Stow Mode

When the case is closed for transport, unscrew all external antennas and store them in a mesh pocket in the lid. The SMA bulkheads sit flush with the case wall.

---

## 7. Display Strategy

### Primary: Hosyond 7" DSI Touchscreen (In the Lid)

Mount the 7" display in the case lid using standoffs or a 3D-printed frame. When you open the case, it hinges up like a laptop screen.

```
OPEN POSITION (side view)

        ┌──────────────┐
        │   7" DSI     │  ← Lid (hinged open ~110°)
        │   Display    │
        └──────┬───────┘
               │ (DSI ribbon cable, routed through hinge gap)
┌──────────────┴──────────────┐
│   Pi 5 + ESP32s + Battery   │  ← Base
└─────────────────────────────┘
```

The DSI ribbon cable routes through the hinge area. Use a **FPC extension cable** (15-pin, 1mm pitch, 30cm) to give enough slack for the lid to open fully.

### Secondary: CYD 2.8" (Marauder Status)

The CYD runs Marauder's touch GUI independently. Mount it face-up in the base, visible when the lid is open. It shows:
- Current Marauder mode (scan/attack/sniff)
- Detected APs and stations
- Touch controls for Marauder without needing the Pi

### Optional: Small OLED Status Displays

Add 0.96" I2C OLED modules (~$3 each) connected to the Pi 5 GPIO for always-on status:
- Battery voltage / percentage
- Active tools running
- WiFi adapter status
- GPS lock status
- Meshtastic message count

### Software: Dashboard on the 7" Screen

The Pi 5 runs a custom dashboard (could be a web app on localhost) that aggregates:
- Kismet live network map
- ESP32 Marauder serial output
- Flock camera alerts (with GPS map)
- BLE tracker alerts
- Meshtastic messages
- Drone RemoteID detections
- System stats (CPU, RAM, battery, temps)

Options:
- **Grafana + InfluxDB** for real-time dashboards
- **Custom Python/Flask web app** for a tailored security dashboard
- **tmux split terminals** for the CLI purist approach

---

## 8. Connectivity and Switching

### USB Hub Architecture

```
Pi 5 USB 3.0 Port #1 ──→ Panda PAU0F WiFi 6E (Kismet primary)
Pi 5 USB 3.0 Port #2 ──→ Powered USB Hub (7-port)
                              ├── Lonely Binary #1 (Marauder) -- serial
                              ├── Lonely Binary #2 (Flock) -- serial
                              ├── Lonely Binary #3 (BLE) -- serial
                              ├── Heltec LoRa V3 (Meshtastic) -- serial
                              ├── ESP32-WROOM-32 (Drone) -- serial
                              ├── RT5370 WiFi (Kismet secondary)
                              └── USB flash drive (data export)
Pi 5 USB 2.0 Port #1 ──→ GPS module (UART over USB)
Pi 5 USB 2.0 Port #2 ──→ (spare / Pwnagotchi dock)
Pi 5 DSI Port ──→ 7" Touchscreen
Pi 5 Bluetooth ──→ Rii K06 Keyboard
```

### Powered USB Hub Selection

Need a compact, powered 7-port USB hub that can supply 500mA per port:

| Hub | Ports | Powered | Size | Price |
|-----|-------|---------|------|-------|
| Anker 7-Port USB 3.0 Hub | 7 | Yes (12V/3A adapter) | 6.8" x 1.8" | ~$30 |
| Sabrent 7-Port USB 3.0 | 7 | Yes (12V/3A) | 7.0" x 1.5" | ~$25 |
| Amazon Basics 7-Port | 7 | Yes | 6.5" x 2.0" | ~$20 |

**For internal mounting:** Strip the hub from its plastic enclosure and mount the bare PCB directly. Saves ~50% of the space.

**Embedded alternative:** Adafruit CH334F Mini 4-Port USB Hub Breakout (#5997, ~$5) -- a tiny 24x20mm PCB with 4 downstream ports via headers and USB-C upstream. Designed specifically for embedding inside enclosures. Chain two of them for 8 ports.

### Mode Switching

Not every tool needs to run simultaneously. Use a **physical toggle switch panel** or **software-controlled USB power switches** to enable/disable boards:

```
SWITCH PANEL (on case side or top)

[ALL ON]  [MARAUDER]  [FLOCK]  [BLE]  [MESH]  [KISMET]
  (o)       (o)         (o)     (o)     (o)      (o)
```

Options:
- **Physical toggle switches** in the USB power lines (~$5 for a pack)
- **USB switchable hub** (like Yepkit YKUSH) -- software-controlled per-port power
- **GPIO-controlled MOSFET switches** on the Pi 5 -- Python script controls which boards get power

---

## 9. Cooling

### The Problem

A sealed Pelican case with a Pi 5 + 5 ESP32s + a power bank will get HOT. The Pi 5 throttles at 85C.

### Solutions

**Option 1: Active Fan (Recommended)**

- Mount a 40mm Noctua fan (~$15) on the case wall with a filtered intake vent
- 3D-print a fan mount with dust filter mesh
- Drill intake holes on one side, exhaust holes on the opposite side
- Creates positive airflow across all components

```
AIRFLOW (top view)

[INTAKE]  ──→  Pi 5  ──→  ESP32s  ──→  [EXHAUST]
(filtered)    (heatsink)  (passive)    (drilled holes)
   FAN                                  
```

**Option 2: Heatsink + Thermal Pads Only (Passive)**

- Pi 5 aluminum heatsink case (like Argon NEO or Geekworm) -- ~$15
- Small adhesive heatsinks on each ESP32 module -- ~$5 for a pack
- Works if the case has some ventilation holes
- May not be enough for sustained full-load operation

**Option 3: Heat Pipe + External Heatsink**

- Run a copper heat pipe from the Pi 5 SoC to the case wall
- Case wall acts as a heatsink (Pelican cases are thick enough)
- No fan noise, no dust
- More complex build

### Recommendation

Go with **Option 1** (40mm fan) for the first build. A single quiet Noctua NF-A4x10 5V PWM fan provides enough airflow. Connect to Pi 5 GPIO for speed control via `fan_temp` overlay.

---

## 10. Modularity and Quick-Swap

### Removable Module Plates

Instead of permanently mounting everything, design **modular plates** that slide into the case:

```
PLATE SYSTEM

┌──────────────────────────────────┐
│  PLATE A: Pi 5 + USB Hub + Fan  │  ← Slides in from the left
│  (always installed)             │
├──────────────────────────────────┤
│  PLATE B: ESP32 Rail            │  ← Slides in from the right
│  (4-5 boards on standoffs)      │
├──────────────────────────────────┤
│  PLATE C: Battery               │  ← Bottom, velcro'd in
│  (swappable power banks)        │
└──────────────────────────────────┘
```

Each plate is a piece of acrylic or 3D-printed tray with standoffs. If you need to debug, upgrade, or reflash a board, pull the plate out.

### Quick-Connect Cables

- Use **magnetic USB-C cables** for ESP32 connections -- snap on/off without wear
- **JST-XH connectors** for internal power distribution -- keyed, snap-in
- **SMA quick-disconnect** at each bulkhead -- unscrew antennas for transport

### Pwnagotchi Dock

A dedicated slot in the case where the assembled Pwnagotchi (Pi Zero + e-ink + PiSugar) drops in:

```
PWNAGOTCHI DOCK (side view)

┌─────────────────┐
│   Main case     │
│                 │
│  ┌───────────┐  │
│  │ Pwnagotchi│  │  ← Drops into a 3D-printed cradle
│  │ Pi Zero   │  │     USB micro cable for charging + data
│  │ + e-ink   │  │     Pull out for pocket carry
│  └───────────┘  │
└─────────────────┘
```

---

## 11. Software Integration

### Operating System

**Kali Linux** on the Pi 5 -- it has Kismet, Bettercap, Wireshark, and most security tools pre-installed. Alternative: Raspberry Pi OS + manual tool install.

### ESP32 Serial Multiplexer

A Python service on the Pi 5 that manages serial connections to all ESP32 boards simultaneously:

```python
# Concept: Multi-ESP32 serial manager
# Each ESP32 appears as /dev/ttyUSBx
# Service reads from all, routes to dashboard

DEVICES = {
    '/dev/ttyUSB0': 'marauder',
    '/dev/ttyUSB1': 'flock',
    '/dev/ttyUSB2': 'ble_scanner',
    '/dev/ttyUSB3': 'meshtastic',
    '/dev/ttyUSB4': 'drone_id',
}
```

### Dashboard Candidates

| Dashboard | Pros | Cons |
|-----------|------|------|
| **Grafana + InfluxDB** | Beautiful, real-time, customizable | Heavy for Pi 5, complex setup |
| **Custom Flask/FastAPI app** | Lightweight, tailored to your tools | Need to build it |
| **Node-RED** | Visual flow programming, easy MQTT integration | Can be slow on Pi |
| **tmux + serial terminals** | Zero overhead, instant setup | Not pretty, hard to parse visually |
| **Cockpit** | Web-based system management, extensible | Not security-focused |

### Auto-Start Services

On boot, the cyberdeck should automatically:
1. Start Kismet in wardrive mode (if GPS lock acquired)
2. Open serial connections to all ESP32 boards
3. Start the Flock detection alert listener
4. Start the BLE tracker scanner
5. Connect to any nearby Meshtastic mesh
6. Launch the dashboard on the 7" display
7. Connect to the Rii K06 keyboard via Bluetooth

Use **systemd services** for each component with dependency ordering.

### GPS Integration

A USB GPS module (VK-162 or GlobalSat BU-353S4, ~$15-25) provides location data to:
- Kismet (wardrive logging with coordinates)
- Flock detection (map camera locations)
- Meshtastic (position sharing)
- BLE tracker (correlation with movement)

One GPS module, shared via `gpsd` daemon, feeds all tools.

---

## 12. Bill of Materials

### New Parts to Buy (Case + Mounting + Power)

| Item | Purpose | Est. Price |
|------|---------|-----------|
| Pelican 1300 Case (or 1200) | Enclosure | $85-100 |
| Powered USB 3.0 Hub (7-port) OR 2x Adafruit CH334F | Connect all devices | $10-30 |
| USB-C PD Power Bank (20,000-25,000mAh) OR Waveshare UPS HAT (E) + 4x 21700 cells | Battery | $35-60 |
| SMA bulkhead connectors x5 | Antenna panel mounts | $10-15 |
| U.FL to SMA pigtail cables x3 (extras) | Internal antenna routing | $8-12 |
| FPC DSI ribbon extension cable (30cm) | Display lid routing | $5-8 |
| 40mm Noctua NF-A4x10 5V fan | Cooling | $15 |
| M2.5/M3 standoff kit (brass) | Board mounting | $8-10 |
| USB GPS module (VK-162) | Location tracking | $15-25 |
| Toggle switches x6 | Power control per device | $5-8 |
| Panel-mount USB-C connector | External charge port | $5-8 |
| Panel-mount USB-A connector | External data port | $3-5 |
| Adhesive cable management clips | Internal routing | $5 |
| Pi 5 heatsink (aluminum) | Cooling | $10-15 |
| Small heatsinks for ESP32s (pack) | Cooling | $5-8 |
| 3D-printed parts (or acrylic sheets) | Mounting plates, fan mount, brackets | $10-20 (filament) |
| Wire, connectors, Kapton tape | Assembly | Already owned |
| **TOTAL NEW PARTS** | | **~$230-330** |

### Already Owned (Not Counted)

All compute, displays, antennas, keyboards, adapters, and storage from your existing inventory. Soldering iron and multimeter for the build.

### Total Project Cost

**Existing inventory:** ~$1,250-$1,450 (already purchased)
**New cyberdeck parts:** ~$230-330
**Grand total for complete cyberdeck:** ~$1,480-$1,780

---

## 13. Build Phases

### Phase 1: Layout and Mock-Up (Weekend 1)

- [ ] Buy Pelican case
- [ ] Lay out all components physically -- does everything fit?
- [ ] Mark drill points for SMA bulkheads, USB ports, fan, switches
- [ ] Decide on layer arrangement
- [ ] Order any missing parts (GPS module, USB hub, power bank, SMA bulkheads, standoffs)

### Phase 2: Case Prep (Weekend 2)

- [ ] Drill SMA bulkhead holes (use step drill bit for clean holes in plastic)
- [ ] Drill fan intake/exhaust holes
- [ ] Drill panel-mount USB-C and USB-A holes
- [ ] Install SMA bulkheads
- [ ] Install fan mount
- [ ] Install panel-mount USB connectors
- [ ] Install toggle switch panel

### Phase 3: Display Mount (Weekend 2-3)

- [ ] Mount 7" DSI display in lid using standoffs or 3D-printed frame
- [ ] Route DSI FPC extension cable through hinge gap
- [ ] Test display with Pi 5 before permanent mounting
- [ ] Optional: mount CYD 2.8" in base for Marauder status

### Phase 4: Power System (Weekend 3)

- [ ] Mount power bank in bottom layer (velcro or 3D-printed cradle)
- [ ] Wire USB-C input from panel-mount to power bank
- [ ] Wire power bank outputs to USB hub and Pi 5
- [ ] Test: does everything power on? Do voltage levels hold under load?
- [ ] Add voltage display module for battery monitoring

### Phase 5: Compute and ESP32 Rail (Weekend 3-4)

- [ ] Mount Pi 5 with heatsink on standoffs
- [ ] Mount USB hub (stripped from enclosure) adjacent to Pi 5
- [ ] Mount ESP32 boards on rail/plate with standoffs
- [ ] Route U.FL pigtails from each ESP32 to SMA bulkheads
- [ ] Connect all USB cables: ESP32s → hub, Panda WiFi → Pi 5 USB 3.0, GPS → Pi 5 USB 2.0
- [ ] Cable management: zip ties, adhesive clips, Kapton tape

### Phase 6: Software (Weekend 4-5)

- [ ] Install Kali Linux (or Pi OS) on Pi 5
- [ ] Install Kismet, Bettercap, Wireshark
- [ ] Configure gpsd for GPS module
- [ ] Flash all ESP32 boards with their respective firmware (Marauder, flock-you, BLE scanner, Meshtastic, drone RemoteID)
- [ ] Write systemd services for auto-start
- [ ] Build or configure dashboard
- [ ] Test serial communication with all ESP32 boards from Pi 5
- [ ] Configure Bluetooth keyboard pairing

### Phase 7: Integration Testing (Weekend 5)

- [ ] Full power-on test: everything runs simultaneously
- [ ] Battery runtime test: how long does it last?
- [ ] Heat test: monitor temps under sustained load
- [ ] Range test: do all antennas work through SMA bulkheads?
- [ ] Drive test: mount in car, test Flock detection + Kismet wardriving + GPS
- [ ] Walk test: carry case, test BLE tracker detection + Meshtastic

### Phase 8: Polish (Ongoing)

- [ ] Label all SMA bulkheads (WiFi/LoRa/BLE)
- [ ] Label all toggle switches
- [ ] Add status LEDs
- [ ] Print case stickers / labels
- [ ] Write operational guide (quick-start for field use)
- [ ] Optional: 3D-print a Pwnagotchi dock cradle

---

## 14. Inspiration and References

### Notable Cyberdeck Builds

| Build | Creator | Case | What's Inside | Link |
|-------|---------|------|---------------|------|
| **Recovery Kit v2** | Jay Doscher | Pelican 1300 | Pi 5, 7" DSI, Planck keyboard, Shargeek Storm 2, NVMe, Ethernet switch | [doscher.com](https://doscher.com/recovery-kit-version-2/) |
| **Pelican-Deck** | Jake Simek | Pelican 1150 | Pi 4, Kali, 3D-printed frame, panel-mount I/O, battery, 3x fans | [GitHub](https://github.com/Jake-Simek/Pelican-Deck) |
| **Pi Slate** | Carbon Computers | Custom | Pi 5, 5" 1920x720, RGB keyboard, 10,000mAh, Parrot OS | [carboncomputers.us](https://carboncomputers.us/products/pi-slate) |
| **HackberryPi CM5 9900** | Eclypsium | Aluminum | CM5 16GB, 720x720, BB keyboard, 5000mAh, Kali + NVMe | [eclypsium.com](https://eclypsium.com/blog/build-the-ultimate-cyberdeck-hackberry-pi/) |
| **CyberPi** | Community | 3D printed | Pi 5, modular frame, customizable | [Printables](https://www.printables.com/model/1162290) |
| **Kitchen Sink Deck** | Hackaday.io | Custom | Pi 4, HackRF, RTL-SDR, GPS, Sense HAT, solar panel | [Hackaday](https://hackaday.io/project/192237) |

### Communities

- **r/cyberdeck** -- 90,000+ members, build gallery, component discussions
- **Cyberdeck Cafe** -- [cyberdeck.cafe](https://cyberdeck.cafe/build) -- Build guides, component recs, showcase
- **Hackaday.io** -- Cyberdeck project category with build logs
- **Jay Doscher** -- [doscher.com](https://doscher.com/) -- Open-source cyberdeck designs, STL files
- **Printables / Thingiverse** -- Search "cyberdeck" for 3D-printable frames and mounts

### Design Files and Tools

- **Fusion 360** (free for personal use) -- 3D modeling for custom parts
- **OpenSCAD** -- Parametric 3D modeling (open source)
- **KiCad** -- If you want to design a custom power distribution PCB
- **FreeCAD** -- Open-source alternative to Fusion 360

### Key Videos

- Search YouTube: "Pelican case cyberdeck build 2025"
- Search YouTube: "Raspberry Pi 5 cyberdeck"
- Search YouTube: "ESP32 pentesting cyberdeck"
- Search YouTube: "Jay Doscher recovery kit build"

---

## Quick-Start Decision Matrix

| Question | Answer |
|----------|--------|
| **Case?** | Pelican 1300 (~$90) |
| **Display?** | 7" DSI in lid + CYD 2.8" for Marauder |
| **Battery?** | 20,000mAh USB-C PD power bank (~$40) |
| **Cooling?** | 40mm Noctua fan + Pi 5 heatsink |
| **Antennas?** | 5x SMA bulkheads, screw-on externals |
| **Software?** | Kali Linux + Kismet + custom dashboard |
| **Input?** | Rii K06 Bluetooth keyboard |
| **GPS?** | VK-162 USB module (~$15) |
| **New parts budget?** | ~$230-330 |
| **Build time?** | 5 weekends |

---

*This is a living document. Update as the build progresses.*
