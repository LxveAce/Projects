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

When the case is closed for transport, unscrew all external antennas and store them in a mesh pocket in the lid. The SMA bulkheads sit flush with the case wall. Screw on SMA dust caps (~$3 for a 10-pack) to protect the connectors and maintain the seal.

### How to Connect Antennas to Each Board

#### Lonely Binary ESP32 Gold (x3) — IPEX Connector (No Soldering)

The Gold boards have a built-in IPEX/U.FL connector near the ESP32 module's RF section. This is a snap-on connector — no soldering required.

```
STEP-BY-STEP:

1. Locate the small gold IPEX socket on the board (near "ANT" label)
2. Take a U.FL-to-SMA pigtail cable (15-20cm)
3. Align the U.FL connector DIRECTLY over the IPEX socket
4. Press STRAIGHT DOWN firmly until you hear/feel a CLICK
5. Do NOT wiggle or twist — press vertically only
6. Route the pigtail cable away from the board (maintain 5mm+ bend radius)
7. The SMA end of the pigtail connects to the SMA bulkhead on the case wall

CONNECTION CHAIN:

[ESP32 board] ──IPEX──→ [U.FL pigtail cable, 15cm] ──SMA──→ [SMA bulkhead] ──→ [external antenna]
                snap-on                                panel-mount          screw-on
```

**Important notes:**
- U.FL connectors are rated for **~30 mating cycles**. Treat as semi-permanent — don't connect/disconnect repeatedly
- Cable loss at 15cm is ~0.3dB — negligible
- If the board has BOTH a PCB trace antenna AND an IPEX connector, there may be a tiny **0-ohm resistor** that selects between them. The Lonely Binary Gold comes configured for IPEX by default
- Use the smallest U.FL connector you can find — some cheap ones are slightly oversized and won't snap properly

#### Heltec LoRa V3 — IPEX Connector (No Soldering)

Same process as the Lonely Binary boards. The Heltec V3 has an IPEX connector for the SX1262 LoRa antenna (915MHz). The WiFi antenna uses the PCB trace (no external option without soldering).

```
[Heltec V3] ──IPEX──→ [U.FL pigtail] ──SMA──→ [SMA bulkhead #4] ──→ [915MHz LoRa antenna]
```

#### ESP32-WROOM-32 (Generic) — PCB Antenna Only

The generic WROOM-32 dev board has **no IPEX connector** — it uses a PCB trace antenna only. For drone RemoteID detection (short range, ~50-100m), the internal PCB antenna is sufficient. No modification needed.

If you later want to add an external antenna, you would need to **solder a U.FL connector** to the antenna feed point on the ESP32 module — this is an advanced modification requiring soldering experience, flux, and magnification.

#### CYD 2.8" Touchscreens — PCB Antenna Only

The CYD boards also use PCB antennas with no IPEX connector. Since they're mounted inside the case and only need short-range communication (serial to the Gold boards via USB), the internal antenna is not a concern — they don't do WiFi scanning.

### Waterproofing the Antenna Panel

Every hole drilled in the Pelican 1300 compromises the IP67 seal. Here's how to maintain water resistance:

**Option 1: IP67-Rated Waterproof SMA Bulkheads (Best)**
- Buy SMA bulkheads with built-in O-ring gaskets and waterproof threading
- These seal the hole by design — no additional sealant needed for the SMA connections
- Exgoofit waterproof SMA bulkheads (~$12 for 5-pack)

**Option 2: Standard SMA Bulkheads + Marine Sealant**
- Apply **3M Marine Grade Silicone Sealant** (clear, ~$8) around each bulkhead hole before tightening the nut
- Also seal around toggle switches, USB panel-mount connectors, and membrane vents
- Let cure 24 hours before exposing to water

**Option 3: Belt and Suspenders**
- Use waterproof bulkheads AND apply marine sealant around them
- Add a thin bead of **butyl rubber tape** (~$5) under each panel-mount component's flange before tightening

**Sealant application:**
1. Drill the hole (use a step drill bit for clean, round holes in polycarbonate)
2. Deburr the hole edges with a deburring tool or fine sandpaper
3. Apply a ring of marine silicone around the hole on the INSIDE of the case
4. Insert the bulkhead connector from outside, push through
5. Apply another ring of sealant on the outside flange
6. Tighten the nut firmly — sealant squeezes into any gaps
7. Wipe excess sealant with a damp cloth
8. Let cure 24 hours

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

### Secondary: CYD 2.8" #1 (Marauder Touchscreen)

The CYD runs Marauder's full touch GUI independently — no Pi needed for basic Marauder operations. Mount face-up in the base, visible when the lid is open.

- Touch controls for scan/attack/sniff modes
- Live AP and station lists
- Connected to Lonely Binary Gold #1 via serial

### Tertiary: CYD 2.8" #2 (Flock/Drone Alert Display)

Second CYD mounted next to the first, running a simple alert dashboard for Flock camera detection and drone RemoteID alerts.

- Connected to Lonely Binary Gold #2 via serial
- Displays OUI match alerts, signal strength, estimated distance
- Red screen flash on Flock camera detection

### Status Display: 2.42" OLED (System Vitals)

A **2.42" SSD1309 OLED** (128x64, I2C) connected to the Pi 5 GPIO provides always-on system status — much more readable than a 0.96" module:

- Battery voltage / percentage
- Active tools running (Kismet, Marauder, Flock, BLE, Mesh)
- WiFi adapter status (monitor mode active?)
- GPS lock status + satellite count
- Meshtastic message count / last message
- Pi 5 CPU temperature + throttle warning
- Internal case temperature (via ESP32 + DHT22 sensor, optional)

Mount this on the edge of the compute plate, angled for visibility when the lid is open.

### Display Summary

| Display | Size | Role | Connected To |
|---------|------|------|-------------|
| Hosyond 7" DSI | 7.0" | Primary dashboard, Kismet web UI, full OS | Pi 5 DSI port |
| CYD 2.8" #1 | 2.8" | Marauder touch GUI | Lonely Binary Gold #1 (serial) |
| CYD 2.8" #2 | 2.8" | Flock/Drone alert display | Lonely Binary Gold #2 (serial) |
| SSD1309 OLED | 2.42" | System vitals (battery, temp, status) | Pi 5 GPIO I2C |
| Heltec built-in OLED | 0.96" | Meshtastic status (built into the board) | Heltec LoRa V3 onboard |

**Total: 5 displays.** Every interactive component has its own visual output.

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
Pi 5 USB 2.0 Port #2 ──→ Wired USB mini keyboard (BLE stealth)
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

### Per-Device Power Switches

Every component gets its own **SPST mini toggle switch** in the USB 5V power line. When a switch is OFF, that device draws **zero power** — completely dead, no standby drain.

```
SWITCH PANEL (mounted on case side panel)

 [MAIN]  [MAR]  [FLOCK]  [BLE]  [MESH]  [DRONE]  [KISM]
  (o)     (o)     (o)     (o)     (o)      (o)      (o)

   ↑       ↑       ↑       ↑       ↑        ↑        ↑
  Pi 5   Gold    Gold    Gold   Heltec  WROOM-32  RT5370
  +Hub    #1      #2      #3    LoRa              2.4GHz
```

**7 switches total.** Each wired inline on the USB 5V line between the hub port and the device.

**Wiring per switch:**
```
USB Hub Port ──→ [5V wire cut] ──→ [SPST Toggle] ──→ [5V wire continues] ──→ Device
                  GND wire passes through unbroken
```

Use **SPST mini toggle switches with waterproof boot caps** (Twidec 10-pack, ~$10) for dust/water resistance on the panel.

**Power savings by mode:**

| Mode | Switches ON | Est. Draw | Use Case |
|------|------------|-----------|----------|
| Full scan | All 7 | ~3A | All tools simultaneously |
| Wardriving only | MAIN + KISM | ~1.5A | Kismet + GPS, everything else off |
| Surveillance detect | MAIN + FLOCK + BLE | ~1.2A | Driving, detecting cameras + trackers |
| Mesh comms only | MAIN + MESH | ~0.9A | Off-grid messaging |
| Stealth (passive) | MAIN only | ~0.8A | Pi 5 only, no ESP32 RF emissions |

**Note:** The Panda PAU0F WiFi 6E adapter connects directly to Pi 5 USB 3.0 (not through the hub), so it's always powered when the Pi is on. This is intentional — Kismet is the primary tool and needs full USB 3.0 bandwidth.

---

## 9. Cooling (Sealed Operation)

### The Problem

A sealed Pelican 1300 with a Pi 5 + 5 ESP32s + a power bank generates ~15-25W of heat. The Pi 5 throttles at 85C. Opening the case defeats the IP67 water/dust resistance. We need to **cool the internals without breaching the case seal.**

### Solution: Hybrid Sealed Cooling System

The approach combines three strategies: **internal air circulation**, **conductive heat transfer to the case walls**, and **membrane venting for extreme scenarios**.

#### Layer 1: IP67 Waterproof Fans (Active Venting Without Breaking Seal)

Use **Coolerguys CG4010M12-IP67** waterproof fans (40x40x10mm, IP67 rated) mounted in the case wall. These are designed for outdoor/marine electronics — they maintain the IP67 waterproof rating while providing real airflow through the case.

Mount **two fans on opposite walls**: one intake (low), one exhaust (high). Seal each mounting hole with neoprene gasket material and marine silicone.

```
CROSS-VENTILATION (top view, case sealed)

┌──────────────────────────────────────┐
│                                      │
│  [IP67 FAN #1]                       │
│  INTAKE (low)                        │
│     ↓ cool air enters                │
│  [Pi 5 + heatsink] → [ESP32 rail]   │
│     ↓ warm air flows across →        │
│                         [IP67 FAN #2]│
│                         EXHAUST (hi) │
│                                      │
└──────────────────────────────────────┘
```

**Coolerguys CG4010M12-IP67 specs:** 40x40x10mm, 12V DC, IP67 rated (submersible to 1m for 30 min), dual ball bearing (67,000 hour lifespan). ~$13-15 each.

**Note:** These are 12V fans. Power options:
- Anker 347 has a USB-A 5V output — use a 5V-to-12V DC boost converter (~$5) to step up
- Or use 5V-native Noctua NF-A4x10 internally as a supplemental circulator alongside the IP67 fans

#### Layer 1b: Internal Circulation Fan (Supplemental)

In addition to the IP67 wall fans, mount a **Noctua NF-A4x10 5V** internally on the mounting plate, blowing directly across the Pi 5 heatsink. This ensures the hottest component always has moving air, even if external conditions limit the IP67 fans' effectiveness.

The Noctua stays inside — it doesn't need to be waterproof.

#### Layer 2: Conductive Heat Transfer

- **Pi 5 aluminum heatsink** (~$10-15) bolted directly to the SoC
- **Thermal silicone pads** (2-3mm thick, ~$5) bridging from the Pi 5 heatsink to the nearest case wall or to a copper/aluminum heat spreader plate
- **Adhesive heatsinks** on each ESP32 module (~$5 for a pack of 20)
- **Copper heat spreader plate** (optional): a thin copper sheet (~$8) mounted to the inside bottom of the case, thermal-padded to the Pi 5 and ESP32s. Heat conducts through the copper to the entire case floor

```
HEAT TRANSFER (side view cross-section)

     ┌─ case wall (polycarbonate, 3-4mm) ─┐
     │                                      │
     │  ┌─ thermal pad (2mm) ─┐            │
     │  │                      │            │
     │  │  [Pi 5 heatsink]    │            │
     │  │  [Pi 5 SoC]         │            │
     │  │                      │            │
     │  └──────────────────────┘            │
     │                                      │
     │  copper heat spreader plate          │
     │  (thermal-padded to case floor)      │
     └──────────────────────────────────────┘
      ↓ heat dissipates through case exterior
```

#### Layer 3: Membrane Pressure Equalization Vent

Add an **Amphenol LTW VENT-PS1** ePTFE membrane vent (~$2-4 from DigiKey). This handles pressure equalization when the fans are OFF (prevents the case from pressurizing/depressurizing with temperature swings, which stresses seals and causes condensation).

- M12x1.5 threaded, requires a 12mm hole
- IP69K rated — blocks water and dust completely
- Allows slow air/gas exchange to prevent condensation inside the case
- Install on the top of the case, away from the fan locations

```
MEMBRANE VENT (cross-section)

[Outside]  ← ePTFE membrane (blocks water, passes air) →  [Inside]
               ┌───────────────┐
rain/dust ──X──│  Amphenol     │──→ pressure equalization
               │  VENT-PS1     │    + condensation prevention
               └───────────────┘
         IP69K rated, prevents seal stress
```

#### Thermal Budget Analysis

| Component | Heat Output | Cooling Method |
|-----------|-----------|---------------|
| Pi 5 (loaded) | ~12W peak | Aluminum heatsink + thermal pad to case wall + fan |
| ESP32 x4 (WiFi TX) | ~1.2W each, ~5W total | Adhesive heatsinks + internal airflow |
| Heltec LoRa V3 | ~1W (LoRa TX) | Adhesive heatsink |
| CYD 2.8" display | ~0.5W | Passive (low heat) |
| 7" DSI display | ~2W | In lid, natural convection |
| USB hub + misc | ~1W | Passive |
| **Total** | **~21W peak, ~12W typical** | |

#### Expected Temperatures (Sealed, 25C Ambient)

| Scenario | Est. Internal Temp | Pi 5 SoC Temp | Status |
|----------|-------------------|--------------|--------|
| Lid open, fan on | +5-10C above ambient | ~45-55C | No throttling |
| Lid closed, fan on, thermal pads | +15-20C above ambient | ~55-65C | No throttling |
| Lid closed, fan on, thermal pads + membrane vents | +10-15C above ambient | ~50-60C | No throttling |
| Lid closed, NO fan, NO thermal pads | +25-35C above ambient | ~75-90C | WILL THROTTLE |

#### Recommendation

**Use all three layers.** The system maintains IP67 waterproofing while keeping the Pi 5 well below throttle temps even during sustained closed-lid operation.

| Part | Price |
|------|-------|
| Coolerguys CG4010M12-IP67 fans x2 (intake + exhaust) | ~$26-30 |
| Noctua NF-A4x10 5V (internal circulator) | ~$15 |
| 5V-to-12V DC boost converter (for IP67 fans) | ~$5 |
| Pi 5 aluminum heatsink | ~$10-15 |
| Thermalright thermal pads (120x120x3mm) | ~$10-15 |
| Adhesive ESP32 heatsinks (pack) | ~$5-8 |
| Neoprene gasket sheet (for fan mounts) | ~$8-12 |
| Amphenol VENT-PS1 membrane vent | ~$3-4 |
| **Total cooling system** | **~$80-100** |

**Noctua PWM control:** Connect to Pi 5 GPIO 18 (hardware PWM) for temperature-based speed control via the `fan_temp` dtoverlay in `/boot/config.txt`:
```
dtoverlay=gpio-fan,gpiopin=18,temp=55000
```

**IP67 fan control:** Wire to a toggle switch or MOSFET on the Pi 5 GPIO for on/off control. Run at full speed when case is sealed, off when lid is open.

#### Temperature Monitoring Script

Add to `/etc/cron.d/thermal-monitor` on Kali:
```bash
#!/bin/bash
TEMP=$(vcgencmd measure_temp | grep -oP '[0-9.]+')
if (( $(echo "$TEMP > 78" | bc -l) )); then
    # Throttle warning — reduce workload or open lid
    echo "THERMAL WARNING: ${TEMP}C" | wall
fi
```

---

## 10. Modularity and Quick-Swap

### Mounting Without a 3D Printer

No 3D printer needed. All mounting uses **off-the-shelf materials**: acrylic sheets, DIN rail, brass standoffs, and the Pelican's own pick-and-pluck foam.

#### Option A: Acrylic Mounting Plates (Recommended)

Buy a clear acrylic sheet (3mm thick, ~$5-8) and cut to fit the Pelican 1300 interior (~9" x 7"). Tools needed: acrylic scoring tool (~$5), ruler, drill with M3 bits.

```
PLATE SYSTEM (no 3D printing)

┌──────────────────────────────────┐
│  PLATE A: Acrylic (3mm)         │  ← Pi 5 + USB Hub + fan on standoffs
│  Cut to 9" x 7"                │     Drill M3 holes for standoffs
│  (sits on foam risers)          │
├──────────────────────────────────┤
│  PLATE B: Acrylic or perforated │  ← ESP32 rail (standoffs or DIN rail)
│  board (sits beside Plate A)    │
├──────────────────────────────────┤
│  BOTTOM: Pick-and-pluck foam    │  ← Battery bay (power bank sits in foam)
│  (custom-plucked cavity)        │
└──────────────────────────────────┘
```

**How to cut acrylic at home:**
1. Mark cut line with ruler and marker
2. Score 10+ times with acrylic scoring tool along the line
3. Clamp to table edge at score line
4. Snap downward — clean break
5. Drill mounting holes with standard drill bits (use low RPM to avoid cracking)

#### Option B: DIN Rail ESP32 Mount

Mount a short DIN rail segment (35mm standard, cut to ~7") inside the case. ESP32 boards attach via DIN rail clips or DIN-mount terminal breakout boards.

- DIN Rail Mount Breakout for ESP32-DevKitC (~$10 each) — all-in-one: screw terminal + DIN clip + board holder
- Generic DIN rail PCB support clips (~$5 for 10-pack)

#### Option C: Pick-and-Pluck Foam Bays

The Pelican 1300 comes with pick-and-pluck foam. Pluck out custom-shaped bays for each component. Best for:
- Battery (power bank sits snugly in a foam cavity)
- Components that don't generate significant heat
- Quick grab-and-go organization

**Not recommended** for the Pi 5 or ESP32s — foam insulates heat.

#### Display in the Lid

Mount the 7" DSI display in the Pelican 1300 lid using **aluminum L-brackets** ($3-5 for a pack) and M3 standoffs:

1. Position display centered in the lid
2. Mark 4 mounting holes through the display's mounting tabs
3. Drill pilot holes in the lid (do NOT drill through — use short standoffs and adhesive backing)
4. Attach L-brackets to the lid with M3 bolts, display screws to the brackets
5. Route DSI ribbon cable through the hinge gap

### Quick-Connect Cables

- Use **magnetic USB-C cables** for ESP32 connections -- snap on/off without wear
- **JST-XH connectors** for internal power distribution -- keyed, snap-in
- **SMA quick-disconnect** at each bulkhead -- unscrew antennas for transport

### Input: Wired USB Keyboard (BLE Stealth)

**Why wired?** A Bluetooth keyboard advertises on BLE channels. If you're running BLE scanning/detection tools, your own keyboard shows up as a persistent BLE device — and anyone else running BLE scanners nearby will detect your keyboard. A wired USB keyboard emits zero RF.

**Options:**

| Keyboard | Size | Connection | Backlit | Notes | Price |
|----------|------|-----------|---------|-------|-------|
| Perixx PERIBOARD-409U | 12.4" x 5.8" | USB wired | No | Compact, proven Linux compat. Too wide to fit inside case — stows on top or in lid | ~$20 |
| Perixx PERIBOARD-426 | ~12.6" x ~4" | USB wired | No | Ultra-thin (14mm), scissor keys. Same width issue | ~$25 |
| Generic 8" USB mini keyboard | ~8" x 4" | USB wired | Varies | Fits inside the case. Search "mini USB keyboard 8 inch" | ~$10-15 |

The keyboard lives outside the case during operation — open the lid, plug in the keyboard, use the 7" touchscreen as display. When done, unplug and stow.

**Alternative:** The 7" DSI is a **touchscreen**. For quick tasks, use the on-screen keyboard (`onboard` package on Kali: `sudo apt install onboard`). Reserve the physical keyboard for extended typing sessions.

---

## 11. Software Integration

### Operating System

**Kali Linux** on the Pi 5 -- Kismet, Bettercap, Wireshark, and 600+ security tools pre-installed. Flash to SD card via Kali ARM images.

### Pi 5 GPIO Pin Mapping

Only **3-4 GPIO pins** are used. Everything else connects via USB.

| Phys Pin | BCM GPIO | Assignment | Device |
|----------|----------|-----------|--------|
| 1 | -- (3.3V) | Power | 2.42" OLED VCC |
| 2 | -- (5V) | Power | DSI Touchscreen |
| 3 | GPIO2 | I2C1 SDA | 2.42" OLED SDA |
| 4 | -- (5V) | Power | Noctua Fan +5V |
| 5 | GPIO3 | I2C1 SCL | 2.42" OLED SCL |
| 6 | -- (GND) | Ground | DSI Touchscreen |
| 9 | -- (GND) | Ground | Noctua Fan GND |
| 12 | GPIO18 | PWM0 | Noctua Fan PWM speed control |
| 14 | -- (GND) | Ground | OLED GND |
| 7-40 (rest) | Various | **Available** | 22-23 GPIO pins free |

**No GPIO expander needed.** 22+ pins remain free for future expansion (sensors, LEDs, buzzer, etc.).

**No conflicts:** The DSI touchscreen uses a separate I2C bus through the DSI connector — it does not share I2C1 with the OLED. All ESP32 boards, WiFi adapters, and GPS connect via USB only.

### USB Port Budget

| Port | Device | Type |
|------|--------|------|
| Pi 5 USB 3.0 #1 | Panda PAU0F WiFi 6E (Kismet) | Direct — needs full bandwidth |
| Pi 5 USB 3.0 #2 | Powered USB Hub → 7 devices below | Hub upstream |
| Hub Port 1 | Lonely Binary Gold #1 (Marauder) | Serial |
| Hub Port 2 | Lonely Binary Gold #2 (Flock/BLE) | Serial |
| Hub Port 3 | Lonely Binary Gold #3 (BLE/CYT) | Serial |
| Hub Port 4 | Heltec LoRa V3 (Meshtastic) | Serial |
| Hub Port 5 | ESP32-WROOM-32 (Drone RemoteID) | Serial |
| Hub Port 6 | RT5370 WiFi (Kismet secondary) | Monitor mode |
| Hub Port 7 | USB flash drive (data export) | Storage |
| Pi 5 USB 2.0 #1 | VK-162 USB GPS module | UART/GPS |
| Pi 5 USB 2.0 #2 | Wired USB keyboard (when plugged in) | HID |

### Dashboard: Flask + SocketIO (Recommended)

A custom **Python Flask + SocketIO** web app running in Chromium kiosk mode on the 7" touchscreen. This is the best fit because:

1. Single Python codebase handles serial I/O AND serves the UI
2. Real-time WebSocket push updates all device panels instantly
3. HTML/CSS gives full control over 800x480 touch-friendly layout
4. Can embed maps (Leaflet.js), charts (Chart.js), and send commands back to ESP32s
5. Lightweight — no Electron bloat, runs smoothly on Pi 5

**Layout (800x480 tabbed interface):**

```
┌──────────────────────────────────────────────────────┐
│ [Overview] [WiFi/Marauder] [BLE/Flock] [Mesh] [Sys] │  ← 5 tabs, 160x48px each
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Marauder│ │ Flock  │ │  BLE   │ │  Mesh  │       │
│  │  🟢   │ │  🟢   │ │  🟢   │ │  🟢   │       │  ← Status cards
│  │ 42 APs │ │ 0 cams │ │ 7 devs │ │ 3 nodes│       │     200x120px each
│  └────────┘ └────────┘ └────────┘ └────────┘       │
│  ┌────────┐ ┌────────┐ ┌──────────────────────┐    │
│  │ Drone  │ │Kismet  │ │  GPS: 37.77, -122.41 │    │
│  │  🟢   │ │  🟢   │ │  Battery: 78%        │    │
│  │ 0 UAVs │ │ 156 AP │ │  CPU: 62°C  RAM: 43%│    │
│  └────────┘ └────────┘ └──────────────────────┘    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Existing open-source starting points:**
- [ESP32 Marauder Web GUI](https://github.com/Pranav-V-20/ESP32-Marauder-Web-GUI) — browser-based Marauder control via Web Serial
- [python-kismet-rest](https://github.com/kismetwireless/python-kismet-rest) — official Kismet REST API wrapper
- [meshtastic-python](https://github.com/meshtastic/python) — official Meshtastic Python SDK

### Serial Communication Protocols

All ESP32 devices communicate at **115200 baud** over USB serial.

| Device | Protocol | Key Commands / Output |
|--------|----------|----------------------|
| **Marauder** | ASCII CLI | `scanap`, `scansta`, `attack -t deauth`, `sniffbt -t flock`, `stopscan` |
| **Flock** | Built into Marauder | `sniffbt -t flock` — detects Flock OUI, `Flock Wardrive` for GPS-tagged logging |
| **BLE Scanner** | ASCII serial | Outputs MAC, RSSI, device name, manufacturer data per detected device |
| **Meshtastic** | Binary protobuf | Use `meshtastic-python` SDK: `interface.sendText()`, `showNodes()`, `getMyNodeInfo()` |
| **Drone RemoteID** | JSON serial | `{"mac":"...","rssi":-45,"drone_lat":37.77,"drone_long":-122.41,"altitude":120}` |
| **Kismet** | REST API | `http://localhost:2501` — Python client: `kismet-rest` package |

**Important discovery:** Marauder has **built-in Flock Sniff** and **Flock Wardrive** features. This means you can run Flock detection on the SAME ESP32 running Marauder — potentially freeing up Gold #2 for a dedicated BLE scanner or spare. The serial command is `sniffbt -t flock`.

### Firmware Flashing Guide

| Board | Firmware | Flash Method | Firmware File |
|-------|----------|-------------|---------------|
| Lonely Binary Gold #1 | ESP32 Marauder | [ESP Terminator](https://espterminator.com/) or esptool | `_multiboardS3.bin` (ESP32-S3) |
| Lonely Binary Gold #2 | Marauder (Flock mode) OR [flock-you](https://github.com/colonelpanichacks/flock-you) | ESP Terminator / PlatformIO | Same S3 variant |
| Lonely Binary Gold #3 | [ESP32-AirTag-Scanner](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner) | Arduino IDE | Select "ESP32S3 Dev Module" |
| Heltec LoRa V3 | Meshtastic | [flasher.meshtastic.org](https://flasher.meshtastic.org/) | Select "Heltec V3" |
| ESP32-WROOM-32 | [Sky-Spy](https://github.com/colonelpanichacks/Sky-Spy) (Drone RemoteID) | PlatformIO | `pio run -e seeed_xiao_esp32s3 --target upload` |

**Note:** The Lonely Binary Gold is an **ESP32-S3** (not WROOM-32). Use S3-specific firmware variants.

**Marauder flashing via esptool (CLI):**
```bash
pip install esptool
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x0 bootloader.bin \
  0x8000 esp32_marauder.ino.partitions.bin \
  0xe000 boot_app0.bin \
  0x10000 esp32_marauder_v1.12.1_multiboardS3.bin
```

**Meshtastic flashing (MUST attach antenna first):**
1. Connect Heltec V3 via USB-C (data cable, not charge-only)
2. Open [flasher.meshtastic.org](https://flasher.meshtastic.org/) in Chrome/Edge
3. Select "Heltec WiFi LoRa 32 V3" → Latest Stable → Flash
4. Configure region: `meshtastic --port /dev/ttyUSB0 --set lora.region US`

### Auto-Start Services

On boot, the cyberdeck should automatically:
1. Start `gpsd` daemon for GPS feed
2. Start Kismet in wardrive mode (if GPS lock acquired)
3. Open serial connections to all ESP32 boards
4. Start the Flock detection listener
5. Start the BLE tracker scanner
6. Connect to the Meshtastic mesh
7. Launch the dashboard in Chromium kiosk mode on the 7" display

Use **systemd services** for each component with dependency ordering.

### GPS Integration

The **VK-162 USB GPS module** provides location data to ALL tools through a single `gpsd` daemon:

```bash
sudo apt install gpsd gpsd-clients
sudo systemctl enable gpsd
```

Configure `/etc/default/gpsd`:
```
DEVICES="/dev/ttyACM0"
GPSD_OPTIONS="-n"
```

All tools connect to `gpsd` at `localhost:2947`:
- **Kismet:** `gps=gpsd:host=localhost,port=2947` in `kismet.conf`
- **Meshtastic:** Position sharing via the `meshtastic-python` API
- **Dashboard:** `gpsd` Python client library for real-time coordinates
- **Flock/BLE:** GPS timestamps from the dashboard backend

---

## 12. Bill of Materials

### Already Purchased (Reference Links)

| # | Item | Description | Link |
|---|------|-------------|------|
| 1 | CanaKit Pi 5 8GB Starter Kit | Pi 5, case, PSU, 128GB SD, heatsink | [Amazon](https://www.amazon.com/CanaKit-Raspberry-Starter-Kit-PRO/dp/B0CRSNCJ6Y) |
| 2 | Lonely Binary ESP32 Gold 3-Pack | 3x ESP32 with IPEX antenna connectors | [Amazon](https://www.amazon.com/ESP32-External-IPEX-Antenna-MicroPython/dp/B0FRXZD6VC) |
| 3 | Heltec LoRa V3 ESP32 (SX1262) | ESP32-S3 + LoRa 915MHz + 0.96" OLED | [Amazon](https://www.amazon.com/Heltec-Development-863-870MHz-ESP32-S3FN8-902-928MHz/dp/B0D1H1FN9Y) |
| 4 | ESP32-WROOM-32 Dev Board | Dual-core 240MHz WiFi+BT, 30-pin | [Amazon](https://www.amazon.com/ESP-WROOM-32-Development-Microcontroller-Integrated-Compatible/dp/B08D5ZD528) |
| 5 | Hosyond 7" DSI Touchscreen x2 | 800x480 IPS capacitive, driver-free | [Amazon](https://www.amazon.com/Hosyond-Touchscreen-Compatible-Capacitive-Driver-Free/dp/B0D3QB7X4Z) |
| 6 | CYD 2.8" ESP32 Touchscreen 2-Pack | ESP32-2432S028R, ILI9341, 240x320 | [Amazon](https://www.amazon.com/MELIFE-Display-ESP32-2432S028R-Dual-core-Development/dp/B0DDPY97JC) |
| 7 | AITRIP 4.0" ESP32 Touchscreen | ST7796, 320x480, ESP32 Type-C | [Amazon](https://www.amazon.com/AITRIP-Touchscreen-Display-320x480-Compatible/dp/B0GGB5W5XK) |
| 8 | Panda PAU0F WiFi 6E USB Adapter | AXE3000, tri-band, USB 3.0, Kali-ready | [Amazon](https://www.amazon.com/Panda-Wireless%C2%AE-PAU0F-AXE3000-Adapter/dp/B0D972VY9B) |
| 9 | RT5370 WiFi USB Dongle | 150Mbps 2.4GHz, monitor mode capable | [Amazon](https://www.amazon.com/Wireless-Adapter-150Mbps-Set-Top-Raspberry/dp/B01KWQAQ00) |
| 10 | Rii K06 Mini Keyboard x2 | Backlit, BT + 2.4G (keep for non-cyberdeck use) | [Amazon](https://www.amazon.com/Rii-Bluetooth-Keyboard-Lightweight-Compatible/dp/B0BML42L6X) |
| 11 | DIYmall 2.4G WiFi Antennas 2-Pack | 3dBi gain with U.FL to SMA pigtail | [Amazon](https://www.amazon.com/Diymall-Antenna-Antennas-Arduino-ESP-072pcs/dp/B00ZBJNO9O) |
| 12 | Bingfu Dual-Band Antennas 2-Pack | 2.4/5/5.8GHz 3dBi MIMO RP-SMA | [Amazon](https://www.amazon.com/Bingfu-Rosewill-Gigabyte-Wireless-Security/dp/B082SHKT3Q) |
| 13 | 915MHz LoRa Antennas 2-Pack | 5dBi omni SMA + IPEX cable | [Amazon](https://www.amazon.com/915MHz-Antenna-Indoor-Connector-Meshtastic/dp/B0DY7KSYTV) |
| 14 | Boobrie RP-SMA to SMA Adapters | 4-pack gender changer kit, gold plated | [Amazon](https://www.amazon.com/BOOBRIE-Connector-Adapter-Coaxial-Antenna/dp/B09R9YFJL4) |
| 15 | AEDIKO ESP32 GPIO Breakout 5-Pack | 30-pin expansion boards, Type-C | [Amazon](https://www.amazon.com/AEDIKO-ESP32-WROOM-32-Development-Interface-Expansion/dp/B0D2HNT8ZR) |
| 16 | Fluke 17B+ Multimeter | Build/debug tool (external) | [Amazon](https://www.amazon.com/Fluke-Applications-Measurements-Capacitance-Temperature/dp/B0779621KZ) |
| 17 | Anker 347 Power Bank | 25,600mAh USB-C PD + USB-A output | [Amazon](https://www.amazon.com/Anker-600mAh-Portable-Charger-PowerCore/dp/B0DP4RYZV5) |

### Need to Get (Shopping List)

| # | Item | Description | Est. Price | Link |
|---|------|-------------|-----------|------|
| 1 | Pelican 1300 Case NF (No Foam) | IP67, 10.7"x9.8"x6.9", black | ~$85-100 | [Amazon](https://www.amazon.com/Pelican-1300-Foam-Black-1300NF/dp/B0009PCU7C) |
| 2 | IP67 Waterproof SMA Bulkheads x5 | Panel-mount, O-ring sealed, antenna pass-through | ~$12-15 | [Amazon](https://www.amazon.com/exgoofit-Waterproof-Bulkhead-Connetor-Antennas/dp/B0D66Y7C6J) |
| 3 | U.FL/IPEX to SMA Pigtails x5 | 15-20cm, connect ESP32 IPEX to bulkheads | ~$8-10 | [Amazon](https://www.amazon.com/HiLetgo-Wireless-Antenna-Extension-NRF24L01/dp/B01HXU1PKS) |
| 4 | Pi 5 DSI Cable (22-pin to 15-pin) | Adapter for Pi 5 to Hosyond display | ~$8 | [Amazon](https://www.amazon.com/TUOPUONE-Official-Flexible-Compatible-Raspberry/dp/B0CNQ4Q2SL) |
| 5 | DSI FPC Extension Cable 30cm | 15-pin 1mm pitch, routes through hinge | ~$5-8 | [Amazon](https://www.amazon.com/Cables-Ribbon-Flexible-Raspberry-Extension/dp/B0891TPPXH) |
| 6 | Coolerguys IP67 40mm Fans x2 | Waterproof intake/exhaust, maintains seal | ~$26-30 | [Amazon](https://www.amazon.com/Coolerguys-40x40x10mm-CG4010M12-IP67-Waterproof-Exterior/dp/B09YWDT4MD) |
| 7 | Noctua NF-A4x10 5V Fan | Internal circulator, ultra-quiet | ~$15 | [Amazon](https://www.amazon.com/Noctua-Cooling-Bearing-NF-A4X10-FLX-5V/dp/B00NEMGCIA) |
| 8 | 5V-to-12V DC Boost Converter | Powers 12V IP67 fans from USB 5V | ~$5 | Search "5V to 12V boost converter USB" |
| 9 | VK-162 USB GPS Module | GPS for Kismet + Flock + Meshtastic | ~$15 | [Amazon](https://www.amazon.com/VK-162-G-Mouse-External-Navigation-Raspberry/dp/B01EROIUEW) |
| 10 | M2.5/M3 Brass Standoff Kit 420pc | Board mounting hardware | ~$10 | [Amazon](https://www.amazon.com/HanTof-Standoff-Assortment-Motherboard-Raspberry/dp/B07CK7L2W6) |
| 11 | IP65 Panel-Mount USB-C | Waterproof bulkhead, charge port | ~$10-12 | [Amazon](https://www.amazon.com/HangTon-Waterproof-Connector-Extension-Pass-Through/dp/B0CDPSGBNL) |
| 12 | IP67 Panel-Mount USB-A | Waterproof bulkhead, data export port | ~$10-12 | [Amazon](https://www.amazon.com/PENGLIN-Waterproof-Connector-Bulkhead-Extension/dp/B09VNS64HM) |
| 13 | Twidec Toggle Switches w/ Caps x10 | SPST, waterproof boot caps, per-device | ~$10 | [Amazon](https://www.amazon.com/Twidec-Toggle-Miniature-Switches-Waterproof/dp/B08CX6P86W) |
| 14 | 3M Marine Grade Silicone Sealant | Clear, waterproof seal for all holes | ~$8-12 | [Amazon](https://www.amazon.com/3M-08019-Marine-Silicone-Sealant/dp/B000H8W9V8) |
| 15 | Amphenol VENT-PS1 Membrane Vent | IP69K pressure equalization, ePTFE | ~$3-4 | [DigiKey](https://www.digikey.com/en/products/detail/amphenol-ltw/VENT-PS1YBK-N8001/7898285) |
| 16 | Geekworm H509 Pi 5 Heatsink | Passive aluminum, low-profile | ~$10-15 | [Amazon](https://www.amazon.com/Geekworm-Aluminum-Heatsink-H509-Raspberry/dp/B0DDTL52Q6) |
| 17 | Adhesive ESP32 Heatsinks 20-pack | 9x9x5mm with 3M thermal tape | ~$5-8 | [Amazon](https://www.amazon.com/Easycargo-Heatsink-conductive-Regulators-8-8mmx8-8mmx5mm/dp/B079FQ22LK) |
| 18 | Thermalright Thermal Pads 120x120x3mm | 12.8 W/mK, heat bridge to case wall | ~$10-15 | [Amazon](https://www.amazon.com/Thermalright-120x120x3mm-Resistance-High-Temperature-Non-Conductive/dp/B08ZN7CN9K) |
| 19 | Neoprene Gasket Sheet 12"x12" | Custom gaskets for fan mounts | ~$8-12 | Search "neoprene gasket sheet 12x12" |
| 20 | 2.42" SSD1309 OLED (I2C) | System status display, 128x64 | ~$10-12 | [Amazon](https://www.amazon.com/HiLetgo-SSD1309-128x64-Display-Optional/dp/B0CFF5SD1T) |
| 21 | Perixx PERIBOARD-409U Wired Mini KB | USB-only input, BLE stealth | ~$20 | [Amazon](https://www.amazon.com/Perixx-PERIBOARD-409U-Mini-Keyboard-12-40x5-79x0-79/dp/B007LQKFG0) |
| 22 | GL850G 4-Port USB Hub Module | Embedded hub breakout for internal use | ~$10-12 | [Amazon](https://www.amazon.com/Port-Module-Genesys-Logic-GL850G/dp/B0BWNG3Z3Y) |
| 23 | Adhesive Cable Clips 30-pack | Adjustable, internal cable routing | ~$5 | [Amazon](https://www.amazon.com/Viaky-Adhesive-Backed-Adjustable-Management/dp/B01M6U9Q9C) |
| 24 | Clear Acrylic Sheet 12"x12" (3mm) | Mounting plates — cut to fit case | ~$8-10 | Search "acrylic sheet 12x12 3mm clear" |
| 25 | DIN Rail ESP32 Mount Breakout | Screw terminal + DIN clip for ESP32s | ~$10 ea | [Amazon](https://www.amazon.com/Mount-Terminal-Breakout-Module-ESP32-DevKitC/dp/B08LGQ2H72) |
| 26 | Aluminum L-Brackets (pack) | Display mounting in lid, no 3D printing | ~$5 | Search "aluminum L bracket small pack" |
| 27 | SMA Dust Caps 10-pack | Protect bulkheads when antennas stowed | ~$3 | Search "SMA dust cap 10 pack" |
| | **TOTAL NEW PARTS** | | **~$340-420** | |

### Total Project Cost

**Existing inventory:** ~$1,250-$1,450 (already purchased)
**New cyberdeck parts:** ~$340-420
**Grand total for complete cyberdeck:** ~$1,590-$1,870

---

## 12.5 Visual Build Diagrams

### Top-Down View (Lid Open, Looking Into Base)

```
┌─────────────────────────────────────────────────────────────┐
│  PELICAN 1300 - TOP DOWN (BASE)    9.17" x 7.0" x 6.15"    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    HINGE SIDE                       │    │
│  │  ┌───────────┐ ─ ─ ─ DSI ribbon runs through ─ ─ ─ │    │
│  │  │           │                                      │    │
│  │  │  Pi 5     │  ┌──────────┐   ┌──────────────┐    │    │
│  │  │  + heat-  │  │ USB Hub  │   │  Anker 347   │    │    │
│  │  │  sink     │  │ (7-port) │   │  40K Power   │    │    │
│  │  │           │  │          │   │  Bank         │    │    │
│  │  │  [GPIO]───┤  │ P1 P2 P3│   │              │    │    │
│  │  │  I2C+PWM  │  │ P4 P5 P6│   │  USB-C PD    │    │    │
│  │  └───────────┘  │ P7      │   │  ──→ Pi 5    │    │    │
│  │       │         └──────────┘   └──────────────┘    │    │
│  │       │              │                              │    │
│  │  ─ ─ ┼── ACRYLIC BASE PLATE (8.5" x 6.5") ──── ─ ─│    │
│  │       │              │                              │    │
│  │  ┌────┴────┐  ┌──────┴─────┐  ┌───────────────┐    │    │
│  │  │ Noctua  │  │  ESP32     │  │  VK-162 GPS   │    │    │
│  │  │ Fan     │  │  PLATE     │  └───────────────┘    │    │
│  │  │ (circ.) │  │            │                       │    │
│  │  └─────────┘  │ ┌──┐┌──┐  │  ┌─────────┐         │    │
│  │               │ │G1││G2│  │  │ WROOM-32│         │    │
│  │               │ └──┘└──┘  │  │ (Drone) │         │    │
│  │               │ ┌──┐┌──┐  │  └─────────┘         │    │
│  │               │ │G3││H3│  │                       │    │
│  │               │ └──┘└──┘  │  ┌─────────┐         │    │
│  │               └───────────┘  │ RT5370  │         │    │
│  │                              │ WiFi #2 │         │    │
│  │                              └─────────┘         │    │
│  │                    LATCH SIDE                     │    │
│  └───────────────────────────────────────────────────┘    │
│                                                           │
│  G1 = Lonely Binary Gold #1 (Marauder)                    │
│  G2 = Lonely Binary Gold #2 (Flock/BLE)                   │
│  G3 = Lonely Binary Gold #3 (BLE Scanner/CYT)             │
│  H3 = Heltec WiFi LoRa V3 (Meshtastic)                   │
└───────────────────────────────────────────────────────────┘
```

### Lid Interior (7" Display Mounted)

```
┌─────────────────────────────────────────────────────────┐
│  PELICAN 1300 - LID INTERIOR (viewed from inside)       │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                  HINGE EDGE                     │    │
│  │                                                 │    │
│  │   ┌─────────────────────────────────────┐       │    │
│  │   │                                     │       │    │
│  │   │     7" Hosyond DSI Touchscreen      │       │    │
│  │   │          800 x 480 px               │       │    │
│  │   │                                     │       │    │
│  │   │     ┌─────────────────────────┐     │       │    │
│  │   │     │   Flask Dashboard UI    │     │       │    │
│  │   │     │  [WiFi][BLE][Mesh][Sys] │     │       │    │
│  │   │     └─────────────────────────┘     │       │    │
│  │   │                                     │       │    │
│  │   └──────────────┬──────────────────────┘       │    │
│  │                  │ DSI ribbon (22→15 pin)       │    │
│  │   ┌──────┐       │                              │    │
│  │   │Noctua│       │  ┌─────────────────┐         │    │
│  │   │A4x10 │       │  │ 2.42" SSD1309   │         │    │
│  │   │(circ)│       │  │ OLED            │         │    │
│  │   └──────┘       │  │ CPU/RAM/Temps   │         │    │
│  │                  │  └─────────────────┘         │    │
│  │              L-brackets (aluminum)              │    │
│  │                  LATCH EDGE                     │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Display mounted via 4x aluminum L-brackets + M3 screws │
│  OLED wired to Pi 5 GPIO2 (SDA) + GPIO3 (SCL)          │
└─────────────────────────────────────────────────────────┘
```

### Right Side Wall (SMA Bulkheads + Exhaust Fan)

```
┌───────────────────────────────────────────────────────┐
│  RIGHT WALL - EXTERNAL VIEW                           │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │                                                 │  │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  │  │
│  │  │SMA 1│  │SMA 2│  │SMA 3│  │SMA 4│  │SMA 5│  │  │
│  │  │WiFi │  │WiFi/│  │ BLE │  │LoRa │  │Panda│  │  │
│  │  │2.4G │  │ BLE │  │     │  │915M │  │WiFi │  │  │
│  │  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  │  │
│  │     │        │        │        │        │      │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │         IP67 WATERPROOF SEAL             │  │  │
│  │  │  (O-rings + 3M Marine Silicone Sealant)  │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  │                                                 │  │
│  │           ┌────────────────┐                    │  │
│  │           │  ████████████  │                    │  │
│  │           │  █ EXHAUST  █  │                    │  │
│  │           │  █  FAN     █  │  Coolerguys        │  │
│  │           │  █ CG4010M  █  │  40mm IP67         │  │
│  │           │  █ 12-IP67  █  │  12V Waterproof    │  │
│  │           │  ████████████  │                    │  │
│  │           └────────────────┘                    │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
│  INTERNAL: U.FL pigtails snap onto ESP32 IPEX          │
│  connectors, route to SMA bulkheads                    │
└───────────────────────────────────────────────────────┘
```

### Left Side Wall (Intake Fan)

```
┌───────────────────────────────────────────────────────┐
│  LEFT WALL - EXTERNAL VIEW                            │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │                                                 │  │
│  │           ┌────────────────┐                    │  │
│  │           │  ████████████  │                    │  │
│  │           │  █ INTAKE   █  │                    │  │
│  │           │  █  FAN     █  │  Coolerguys        │  │
│  │           │  █ CG4010M  █  │  40mm IP67         │  │
│  │           │  █ 12-IP67  █  │  12V Waterproof    │  │
│  │           │  ████████████  │                    │  │
│  │           └────────────────┘                    │  │
│  │                                                 │  │
│  │                                                 │  │
│  │           ○ Amphenol VENT-PS1                   │  │
│  │             Membrane Vent                       │  │
│  │             (pressure equalization)             │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
│  Airflow: INTAKE (left) → across components →         │
│           EXHAUST (right) + Noctua internal circ.      │
└───────────────────────────────────────────────────────┘
```

### Front Panel (Switches + USB-C)

```
┌───────────────────────────────────────────────────────┐
│  FRONT PANEL - LATCH SIDE (EXTERNAL VIEW)             │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │                                                 │  │
│  │  POWER SWITCHES (SPST + waterproof boot caps)   │  │
│  │                                                 │  │
│  │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐   │  │
│  │  │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │ │ 7 │   │  │
│  │  │MAR│ │FLK│ │BLE│ │MSH│ │DRN│ │KS2│ │GPS│   │  │
│  │  └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘   │  │
│  │    │     │     │     │     │     │     │       │  │
│  │  Each switch inline with USB power to device    │  │
│  │                                                 │  │
│  │         ┌──────────┐                            │  │
│  │         │  USB-C   │  Panel-mount               │  │
│  │         │ CHARGE   │  charging port             │  │
│  │         └──────────┘  → Anker 347 input         │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
│  1=Marauder  2=Flock  3=BLE Scanner  4=Meshtastic    │
│  5=Drone ID  6=Kismet WiFi #2  7=GPS Module          │
│  Pi 5 + primary WiFi always on (powered directly)     │
└───────────────────────────────────────────────────────┘
```

### Cross-Section View (Side Cut — Airflow Path)

```
┌───────────────────────────────────────────────────────┐
│  CROSS-SECTION (side view, lid open 90°)              │
│                                                       │
│         ┌──────── LID ────────┐                       │
│         │  ┌───────────────┐  │                       │
│         │  │ 7" DSI Screen │  │                       │
│         │  └───────────────┘  │                       │
│         │  Noctua A4x10 ↻    │  ← internal air circ  │
│         │  2.42" OLED        │                        │
│         └────────────────────┘                        │
│              ║ DSI ribbon                             │
│  ┌───────────╨───────────────────────┐                │
│  │ ← INTAKE      BASE        EXHAUST → │             │
│  │   IP67 fan                 IP67 fan  │             │
│  │                                      │             │
│  │   ┌─────┐  ┌──────┐  ┌──────────┐   │             │
│  │   │     │  │ Pi 5 │  │  Anker   │   │  ← Layer 1  │
│  │   │     │  │ + HS │  │  347     │   │    (base     │
│  │   │COOL │  └──────┘  │  40K     │   │     plate)   │
│  │   │ AIR │  ┌──────┐  └──────────┘   │             │
│  │   │ → → │  │ USB  │                 │             │
│  │   │     │  │ Hub  │  ┌───┐┌───┐     │  ← Layer 2  │
│  │   │     │  └──────┘  │G1 ││G2 │     │    (ESP32    │
│  │   │     │            └───┘└───┘     │     plate)   │
│  │   │     │  ┌──────┐  ┌───┐┌───┐     │             │
│  │   │     │  │ GPS  │  │G3 ││H3 │ HOT │             │
│  │   │     │  └──────┘  └───┘└───┘  →  │             │
│  │   └─────┘                           │             │
│  │   ○ Membrane vent (bottom wall)     │             │
│  └─────────────────────────────────────┘              │
│                                                       │
│  Thermal path: heatsinks → air → IP67 fans → outside  │
│  Membrane vent equalizes pressure during temp changes  │
└───────────────────────────────────────────────────────┘
```

### U.FL/IPEX to SMA Bulkhead Connection Detail

```
┌───────────────────────────────────────────────────────┐
│  ANTENNA CONNECTION DETAIL                            │
│                                                       │
│  ESP32 Board              Case Wall           Outside │
│  ┌─────────┐                │                        │
│  │         │  U.FL pigtail  │  SMA bulkhead          │
│  │  ┌───┐  │  ~~~~~~~~~~~  ┌┴┐  ════╗               │
│  │  │IPX│──┤──── coax ────│O│──║  ║──► Antenna      │
│  │  └───┘  │              └┬┘  ════╝               │
│  │         │    6" cable    │                        │
│  └─────────┘                │                        │
│                             │                        │
│  Step 1: Align IPEX         │  Step 3: Thread SMA    │
│  connector over board       │  through drilled hole   │
│  pad (gold circle)          │  + O-ring gasket        │
│                             │                        │
│  Step 2: Press straight     │  Step 4: Tighten nut    │
│  down — feel/hear click     │  from inside + sealant  │
│  (DO NOT twist or slide)    │                        │
│                             │  Step 5: Screw on       │
│  ⚠ Max 30 mating cycles    │  external antenna       │
│    per IPEX connector       │                        │
└───────────────────────────────────────────────────────┘
```

### Wiring Diagram (Power Distribution)

```
┌───────────────────────────────────────────────────────────┐
│  POWER DISTRIBUTION                                       │
│                                                           │
│  ┌──────────────┐                                         │
│  │  Anker 347   │                                         │
│  │  40,000mAh   │                                         │
│  │              │                                         │
│  │  USB-C PD ───┼──► Pi 5 (5V/5A, 25W) ──► ALWAYS ON     │
│  │  30W output  │                                         │
│  │              │                                         │
│  │  USB-A #1 ───┼──► Powered USB Hub                      │
│  │  22.5W       │       │                                 │
│  │              │       ├──► SW1 ──► Gold #1 (Marauder)   │
│  │  USB-A #2 ───┼──►    ├──► SW2 ──► Gold #2 (Flock)     │
│  │  (spare)     │       ├──► SW3 ──► Gold #3 (BLE)        │
│  │              │       ├──► SW4 ──► Heltec V3 (Mesh)     │
│  │  USB-C IN ◄──┼───── Panel-mount USB-C (charging)       │
│  └──────────────┘       ├──► SW5 ──► WROOM-32 (Drone)     │
│                         ├──► SW6 ──► RT5370 (Kismet #2)   │
│  Pi 5 USB Ports:        └──► SW7 ──► VK-162 GPS           │
│  ├─ USB 3.0 #1 ──► Panda PAU0F (direct, full bandwidth)  │
│  ├─ USB 3.0 #2 ──► Powered USB Hub (upstream)            │
│  ├─ USB 2.0 #1 ──► VK-162 GPS (via hub or direct)        │
│  └─ USB 2.0 #2 ──► Wired USB Keyboard                    │
│                                                           │
│  SW1-SW7 = SPST toggle switches with waterproof boots     │
│  Pi 5 + Panda WiFi are always on (no switch)              │
│                                                           │
│  12V rail (from buck converter or USB-to-12V):            │
│  └──► 2x Coolerguys IP67 fans (intake + exhaust)          │
│                                                           │
│  5V from Pi 5 GPIO:                                       │
│  └──► Noctua A4x10 fan (Pin 4, PWM on GPIO18)             │
│  └──► 2.42" OLED (Pin 1: 3.3V, I2C on GPIO2/3)            │
└───────────────────────────────────────────────────────────┘
```

---

## 13. Build Phases

### Phase 1: Planning and Procurement (Week 1)

- [ ] Order Pelican 1300 case and all "Need to Get" parts from BOM
- [ ] Print this README as a reference sheet
- [ ] While waiting for parts: flash Kali Linux to SD card, install `esptool`, `meshtastic`, `gpsd`
- [ ] Flash all ESP32 boards with firmware (Marauder `_multiboardS3.bin`, Meshtastic, etc.)
- [ ] Test each ESP32 board individually on a desk — confirm serial comms work

### Phase 2: Case Prep and Waterproofing (Weekend 1)

- [ ] Remove pick-and-pluck foam from Pelican 1300
- [ ] Mark drill points: 5x SMA bulkhead holes (right wall), 2x 40mm fan cutouts (left + right wall), 7x toggle switch holes (front panel), 1x panel-mount USB-C hole
- [ ] Drill all holes with step drill bit (go slow on polymer — no heat buildup)
- [ ] Install IP67 SMA bulkheads with O-rings — hand-tighten plus 1/4 turn with wrench
- [ ] Install IP67 Coolerguys fans (intake left wall, exhaust right wall) with gaskets
- [ ] Apply 3M Marine Grade Silicone Sealant around every penetration point
- [ ] Install Amphenol VENT-PS1 membrane vent (bottom wall, small 6mm hole)
- [ ] Install 7x SPST toggle switches with waterproof boot caps
- [ ] **Let sealant cure 24 hours before continuing**

### Phase 3: Acrylic Plate Fabrication (Weekend 1-2)

- [ ] Score and snap 3mm acrylic sheet into two plates:
  - Base plate: 8.5" x 6.5" (Pi 5 + USB hub + power bank)
  - ESP32 plate: 6" x 4" (all ESP32 boards)
- [ ] Drill mounting holes with 3mm bit (mark from component standoffs)
- [ ] Mount M2.5 brass standoffs to both plates
- [ ] Test-fit plates in case — should rest on internal ribs or foam strips

### Phase 4: Compute Layer Assembly (Weekend 2)

- [ ] Mount Pi 5 (with aluminum heatsink) on base plate standoffs
- [ ] Mount powered USB hub (stripped from enclosure) adjacent to Pi 5
- [ ] Mount Anker 347 power bank on base plate with velcro strips
- [ ] Connect: USB-C PD from power bank → Pi 5, USB-A from power bank → hub
- [ ] Test power-on: Pi 5 boots Kali, hub enumerates

### Phase 5: ESP32 Rail and Antennas (Weekend 2-3)

- [ ] Mount all ESP32 boards on ESP32 plate using DIN rail brackets or direct standoffs
- [ ] Connect U.FL/IPEX pigtails from each ESP32 to SMA bulkheads:
  - Gold #1 → SMA #1 (WiFi 2.4GHz)
  - Gold #2 → SMA #2 (WiFi/BLE)
  - Gold #3 → SMA #3 (BLE)
  - Heltec LoRa V3 → SMA #4 (915MHz LoRa)
  - WROOM-32 → Internal PCB antenna (no SMA needed)
- [ ] Route USB cables from each ESP32 to hub ports
- [ ] Connect Panda PAU0F directly to Pi 5 USB 3.0 #1 (needs full bandwidth)
- [ ] Wire power switches: each toggle switch inline with each ESP32's USB power line
- [ ] Cable management: zip ties every 2", adhesive clips along plate edges

### Phase 6: Displays (Weekend 3)

- [ ] Mount 7" DSI display in lid using aluminum L-brackets and M3 screws
- [ ] Route DSI ribbon cable (22-to-15 pin adapter) through hinge gap, secure with Kapton tape
- [ ] Mount Noctua NF-A4x10 fan on lid faceplate (internal circulation), wire PWM to GPIO18
- [ ] Mount CYD 2.8" #1 (Marauder) on ESP32 plate — plugs directly into Gold #1
- [ ] Mount CYD 2.8" #2 (Flock/Drone) — plugs directly into Gold #2
- [ ] Mount 2.42" SSD1309 OLED on front panel or lid edge, wire I2C to Pi 5 GPIO2/GPIO3
- [ ] Test all displays power on and show output

### Phase 7: Software Integration (Weekend 3-4)

- [ ] Verify Kali Linux is up to date: `sudo apt update && sudo apt full-upgrade`
- [ ] Install Kismet: `sudo apt install kismet`
- [ ] Install Python packages: `pip install flask flask-socketio pyserial meshtastic kismet-rest gps3`
- [ ] Configure `gpsd` for VK-162 GPS module
- [ ] Test serial communication with each ESP32: `screen /dev/ttyUSB0 115200`
- [ ] Write systemd services for auto-start (gpsd → kismet → dashboard)
- [ ] Build Flask + SocketIO dashboard app
- [ ] Configure Chromium kiosk mode: `chromium-browser --kiosk http://localhost:5000`
- [ ] Write `temp_monitor.py` for OLED system vitals display
- [ ] Test all services start on boot

### Phase 8: Sealed Integration Testing (Weekend 4)

- [ ] Full power-on test: all 7 switches ON, all devices running simultaneously
- [ ] **Sealed thermal test:** close case, run all devices for 30 minutes, monitor temps via OLED
  - Target: Pi 5 CPU < 70°C, case interior < 45°C
  - If too hot: increase fan speed, add thermal pads, or add second membrane vent
- [ ] Battery runtime test: full load until shutdown — target 3-4 hours
- [ ] Antenna range test: WiFi scan from 50ft, LoRa from 1+ mile, BLE from 30ft
- [ ] Drive test: Flock detection + Kismet wardriving + GPS logging
- [ ] Walk test: BLE tracker detection + Meshtastic mesh
- [ ] Water resistance test: spray case with hose (SMA side) for 30 seconds, check interior

### Phase 9: Polish (Ongoing)

- [ ] Label all SMA bulkheads with Brother P-Touch labels (WiFi/BLE/LoRa)
- [ ] Label all toggle switches (Marauder/Flock/BLE/Mesh/Drone/Kismet-2/GPS)
- [ ] Apply anti-slip rubber feet to case bottom
- [ ] Screw on SMA dust caps for transport
- [ ] Write field operations quick-start card (laminated, inside lid pocket)
- [ ] Optional: custom laser-engraved Pelican nameplate

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
| **Case?** | Pelican 1300 (~$85-100) |
| **Displays?** | 5 total: 7" DSI + 2x CYD 2.8" + 2.42" OLED + Heltec built-in |
| **Battery?** | Anker 347 Power Bank 40K (40,000mAh, 30W USB-C PD) |
| **Cooling?** | 3-layer sealed: 2x IP67 Coolerguys + Noctua internal + membrane vent |
| **Waterproofing?** | IP67 SMA bulkheads + 3M Marine Silicone + Amphenol VENT-PS1 |
| **Antennas?** | 5x SMA bulkheads, screw-on externals, U.FL pigtails |
| **Mounting?** | 3mm acrylic plates + DIN rail brackets (no 3D printer) |
| **Power switches?** | 7x SPST toggles with waterproof boot caps |
| **Software?** | Kali Linux + Kismet + Flask/SocketIO dashboard |
| **Input?** | Perixx PERIBOARD-409U wired USB (BLE stealth) |
| **GPS?** | VK-162 USB module via gpsd |
| **GPIO used?** | 3-4 of 26 pins (no expander needed) |
| **New parts budget?** | ~$340-420 |
| **Build time?** | 4-5 weekends (9 phases) |

---

*This is a living document. Update as the build progresses.*
