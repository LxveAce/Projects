# Cyberdeck v2 — Full Re-Brainstorm, Capability-Maximized on the Real Owned Fleet

**Brain:** Raspberry Pi 5 (8GB). **Design rule applied:** every radio node runs the *single* firmware it is strongest at (one flash image per board — a board cannot run two firmwares at once), and the Pi 5 orchestrates and cross-routes them. Reliability/longevity-first, lawful-only (no operational jammer), per your standing guardrails.

This supersedes the 2026-06-07 wiring table in `integrations/README.md` in three ways the old plan got wrong or couldn't see yet:
- The 2× **Waveshare ESP32-C5** are now confirmed-real **dual-band 5GHz** nodes (Marauder/Bruce/GhostESP all flash and run on them) — they are the 5GHz backbone, not a "maybe."
- The 3× **BW16 (RTL8720DN)** you validated on **Vampire Deauther** are the **only** hardware in the fleet that does *5GHz active deauth* — a capability the C5 Marauder build does not match yet.
- The 3× **ESP32-S2U** unlock **native-USB BadUSB** (SuperWiFiDuck) — a keystroke-injection capability nothing else in the fleet has — and the **T-Display-S3** is the correct home for **Flock-You/OUI-Spy** (the WiFi-promiscuous ALPR catch needs an S3, not a classic ESP32).

---

## 1. Deck Architecture (one cohesive system)

```
                         ┌──────────────────────────────────────────────┐
                         │              RASPBERRY PI 5 (8GB) — BRAIN      │
                         │  Kali/Pi OS · Kismet server · gpsd · dashboard │
                         │  cyber-controller + headless-marauder-gui      │
                         └───────────────┬───────────────┬───────────────┘
        7" DSI dashboard ────────────────┘               │
                                                          │
        ┌───────────── POWERED USB 3.0 HUB (per-port switched) ─────────────┐
        │        │           │          │          │          │            │
   [Pi USB3]  [SW1]       [SW2..n]    [SW]       [SW]       [SW]         [SW]
   Panda      C5#1        C5#2        BW16×3     Gold×3 +   S2U          CYD×2 /
   PAU0F      5GHz        5GHz        5GHz       WROOM      BadUSB       T-Disp
   (Kismet)   Marauder    GhostESP    deauth     2.4GHz     (HID)        (handheld/
   always-on  /scan       wardrive    (serial)   nodes                   touch)
        │
   Heltec V3 (Meshtastic) ── own LoRa antenna, OLED, sometimes battery-detached as a field mesh node
```

**Two control planes:**
- **USB-serial control plane** — every ESP32/BW16 node enumerates at `/dev/ttyUSB*|ACM*` (115200 baud). The Pi drives them headless via your `headless-marauder-gui` `marauder_core` (Marauder CLI) and per-firmware serial CLIs (BW16 `AT+`, GhostESP/Bruce serial).
- **Network/IP control plane** — boards that expose their own web UI/AP (GhostESP web dashboard, Bruce web, SuperWiFiDuck web) are reachable from the Pi over a private wired/AP link; the Pi's dashboard iframes/links them. RayHunter (Orbic) is reached via **ADB port-forward** (`adb forward tcp:8080`).

**Data fusion on the Pi:** GPS from one USB puck is shared to *everything* via `gpsd`; Kismet ingests the Panda (+ optional remote-capture from a wardriving ESP); every node's loot/log lands in a single capture dir (you already built `capture.py` → `latest.json`/`aps.csv`/`stations.csv`) that the dashboard tails.

---

## 2. Board → Role assignment (each board → best firmware + why)

| # | Board (owned) | Chip | Role | Firmware (best fit) | Why this is its strongest job |
|---|---|---|---|---|---|
| 1 | **Raspberry Pi 5 8GB** | BCM2712 | **Brain / orchestrator** | Kali or Pi OS + Kismet + gpsd + cyber-controller + dashboard | Only device with the horsepower/USB3/DSI to run Kismet, fuse GPS, host the GUI, and command every node. |
| 2 | **Waveshare ESP32-C5 #1** | ESP32-C5 (dual-band WiFi6) | **5GHz attack/recon platform** | **Marauder (C5 build)** | C5 is the *only* fleet chip with native 5GHz; Marauder is the most-refined C5 firmware (scan/monitor/deauth/beacon/evil-twin on 2.4+5). Driven headless by your existing GUI. |
| 3 | **Waveshare ESP32-C5 #2** | ESP32-C5 | **Dual-band wardriving + Evil-Portal + skimmer/pineapple detect** | **GhostESP** | GhostESP's GPS-wardriving (WiGLE CSV), evil-portal, BLE/AirTag/skimmer/pineapple detection, and web dashboard make it the better *passive-mapping/captive* complement on the second 5GHz radio. |
| 4–6 | **BW16-Kit ×3** | RTL8720DN (2.4+5GHz) | **5GHz active deauth / dual-band disruption-test** | **Vampire Deauther** (validated) | The RTL8720DN is the fleet's only true *5GHz deauth* radio. AT+ CLI over serial = trivially Pi-orchestrated. 3 units = multi-channel/multi-band coverage or spares. (Black 22-pin PCB = the compatible version — yours.) |
| 7 | **Lonely Binary Gold #1** | Classic ESP32 (16MB, CH340) | **Primary 2.4GHz WiFi/BLE offensive tool** | **Marauder (ESP32/WROOM build)** | Your built/validated node. Classic ESP32 = rock-solid 2.4GHz Marauder (deauth, probe/PMKID, BLE spam, **built-in `sniffbt -t flock`**). |
| 8 | **Lonely Binary Gold #2** | Classic ESP32 | **Drone RemoteID + 2.4GHz scanner** | **Marauder** or Sky-Spy/RemoteID sniffer | Second 2.4GHz radio so #1 can attack while #2 passively scans/sniffs RemoteID without channel-fighting. |
| 9 | **Lonely Binary Gold #3** | Classic ESP32 | **BLE tracker / "Chasing Your Tail" detect** | **Bruce** (or Marauder BLE) | Bruce's BLE tooling + scan is a clean dedicated tail-detector (AirTag/Tile/SmartTag) on the deck's 3rd classic ESP32. |
| 10 | **ESP-WROOM-32** | Classic ESP32 | **Always-on BLE/2.4GHz beacon-anomaly monitor** | **Marauder** (headless) | Cheapest classic node → leave it as a persistent background sniffer feeding the dashboard; frees the Gold boards for active tasks. |
| 11–13 | **ESP32-S2U ×3** | ESP32-S2 (native USB, **no BLE**) | **BadUSB / keystroke-injection (HID)** | **SuperWiFiDuck** | S2's *native USB* = real USB-HID keyboard emulation over WiFi-managed DuckyScript — a capability **no other board in the fleet has**. (S2 has no Bluetooth, so it's wasted on BLE work; this is its killer app.) Spares/multi-payload. |
| 14 | **LILYGO T-Display-S3** | ESP32-S3 + 1.9" TFT | **Handheld Flock/OUI-Spy detector + detachable field tool** | **Flock-You / OUI-Spy** (primary); Bruce/GhostESP as alt | The Flock ALPR WiFi-promiscuous "receiver-address" catch is **documented to need an ESP32-S3** — the T-Display-S3 is the *right* chip + has a screen + LiPo for grab-and-go counter-surveillance. |
| 15 | **CYD #1 (2432S028R)** | Classic ESP32 + 2.8" touch | **Standalone touchscreen Marauder** | **Marauder (CYD build)** | Self-contained touch Marauder — usable on-deck or pulled out; no Pi needed. |
| 16 | **CYD #2 (2432S028R)** | Classic ESP32 + 2.8" touch | **Multi-protocol attack station (Sub-GHz/NFC/2.4 raw)** | **HaleHound-CYD** | HaleHound turns the CYD into a touch multitool and **breaks out CC1101 (Sub-GHz), NRF24L01+PA/LNA (2.4 raw/Mousejack), PN532 (NFC)** — your owned modules. Touch UI + SD loot + OTA. |
| 17 | **AITRIP 4" ST7796** | ESP32 + 4" touch | **Secondary touch panel / Bruce or HaleHound** | **Bruce** (good ST7796/TFT_eSPI support) | Bigger touch real-estate for a bench multitool or as the deck's local touch console; Bruce drives ST7796 well. |
| 18 | **Heltec LoRa V3** | ESP32-S3 + SX1262 | **Off-grid LoRa mesh (915MHz)** | **Meshtastic** (running) | The only LoRa radio; Meshtastic = off-grid comms/telemetry. One firmware per board, so it stays a dedicated mesh node (detach to deploy as a remote mesh point). |
| — | **Panda PAU0F** | MT7921 (WiFi6E) | **Kismet primary capture** | (Linux driver) | Pi-attached, monitor-mode 2.4/5/6GHz capture for Kismet — the deck's serious survey NIC. |
| — | **RT5370 / GPS puck** | Ralink / u-blox | Kismet secondary / shared GPS | gpsd | Second capture + the single GPS source fused to all tools. |
| — | **Pi Zero 2 W** | — | **FRIED — RMA/replace** | n/a | Was RaspyJack/Pwnagotchi host; dead. See shopping delta. |

**Firmware-per-board is a hard constraint** (single flash image). Where a board *could* run several firmwares (CYD, T-Display-S3, C5), the table picks the one that exploits a capability the rest of the fleet lacks, and lists the alternate so you can re-flash for a different op.

---

## 3. Unique-capability matrix (what each radio does that none other can)

| Capability | ONLY hardware in your fleet that does it | Notes / why unique |
|---|---|---|
| **5GHz active deauth** | **BW16 ×3 (RTL8720DN)** | C5 can *monitor/scan* 5GHz, but mature 5GHz *deauth* is the BW16/Vampire's job. Classic ESP32/S2/S3 are 2.4GHz-only. |
| **5GHz scan / monitor / WiFi6 recon** | **Waveshare C5 ×2** | Native dual-band WiFi6 SoC; runs full Marauder/GhostESP on 2.4+5. |
| **Native-USB BadUSB / HID keystroke injection** | **ESP32-S2U ×3** | S2's native USB stack → real keyboard emulation (SuperWiFiDuck). Classic ESP32/S3-on-these-boards can't match cleanly. |
| **LoRa / sub-GHz long-range mesh (915MHz)** | **Heltec V3 (SX1262)** | Only LoRa transceiver — off-grid comms + telemetry backhaul. |
| **CC1101 Sub-GHz (315/433/868/915) TX/RX + replay** | **CYD #2 (HaleHound) / ESP32-DIV path** | Garage/ISM capture-replay; your CC1101 2-pack + 315MHz + 915MHz whips. |
| **NFC/RFID 13.56MHz read/write/emulate** | **CYD #2 (HaleHound + PN532)** | Your PN532 V3 + S50 cards. |
| **Raw 2.4GHz NRF24 analyzer / Mousejack research** | **CYD #2 (HaleHound) or HaleHound/ESP32-DIV w/ NRF24+PA/LNA** | Wireless mouse/keyboard (Logitech/MS) recon; lawful research only. |
| **Flock/ALPR WiFi-promiscuous detection** | **T-Display-S3 (Flock-You/OUI-Spy)** | Receiver-address catch technique needs an **S3**; classic Gold is a weaker fit. |
| **IMSI-catcher / stingray detection (cellular)** | **Orbic RC400L (RayHunter)** *(to buy)* | Only cellular-aware device; ADB-forwarded to the Pi dashboard. |
| **WiFi 6E (6GHz) survey capture** | **Panda PAU0F + Kismet** | Only 6GHz-capable radio; Pi-side. |
| **Touchscreen standalone operation (no Pi)** | **CYD ×2, AITRIP 4", T-Display-S3** | Pull-and-go tools that survive a dead brain. |

**Overlap note (intentional redundancy):** classic-ESP32 2.4GHz Marauder exists on Gold ×3 + WROOM + CYD #1. That's deliberate — multiple 2.4GHz radios let you attack on one channel while passively sniffing on others (Marauder is single-channel at a time), and they're cheap spares.

---

## 4. Power / Antenna / Display / IO plan

### Power
- **Pi 5 (always-on):** USB-C PD bank (your Anker 347 plan) — Pi 5 wants a real 5V/5A PD source; do not starve it (USB3 + Panda + hub draw is significant).
- **Powered USB 3.0 hub with per-port switching:** every ESP/BW16/S2U/CYD hangs off switched ports so you energize only the radios an op needs (thermal + power + RF-hygiene). Keep Panda on an always-on port.
- **PiSugar:** keep for a *separate* battery-backed node (it lacks I2C SOC reporting — fine as a UPS, not for fuel-gauging). Reserve it for a detached field node, not the Pi 5 main rail.
- **T-Display-S3 + EEMB 1000mAh LiPo:** the grab-and-go Flock detector runs off its own LiPo so it leaves the deck fully functional.
- **Heltec V3:** runs off hub power on-deck; detachable with its own cell for remote mesh.

### Antenna (bulkhead plan — revised count)
Dedicated SMA bulkheads, U.FL→SMA pigtails (you have Rydocyee + Boobrie adapters):

| Bulkhead | Feeds | Band | Antenna |
|---|---|---|---|
| SMA1 | Gold #1 (Marauder) | 2.4GHz | 2.4 whip (DIYmall) |
| SMA2 | Gold #2 (RemoteID/scan) | 2.4GHz | 2.4 whip |
| SMA3 | Gold #3 (BLE/tail) | 2.4GHz | 2.4 whip |
| SMA4 | **C5 #1** | **dual 2.4/5** | Bingfu dual-band |
| SMA5 | **C5 #2** | **dual 2.4/5** | Bingfu dual-band |
| SMA6 | **BW16 (primary)** | **dual 2.4/5** | dual-band (Bingfu/RP-SMA via adapter) |
| SMA7 | Heltec (LoRa) | 915MHz | 915 LoRa whip |
| SMA8 | Panda PAU0F | 2.4/5/6 | its own dual-element (often best left on the dongle near a case wall) |
| (internal) | CYD #2 HaleHound radios | CC1101 315/433/915 + NRF24 RP-SMA | 315/915 whips + NRF24 duck (mount to bulkheads if you want external) |

BW16 ×3: only 1–2 need external bulkheads; the others can run internal PCB-antenna for bench/spare. **Note the RP-SMA vs SMA polarity** — your Boobrie RP-SMA↔SMA adapters resolve the NRF24/deauther-duck mismatches.

### Display
- **Pi 5 → 7" Hosyond DSI** (needs the **22-pin→15-pin** adapter cable — Pi 5 DSI is 22-pin) = main dashboard, Chromium kiosk.
- **CYD #1** = standalone Marauder touch; **CYD #2** = HaleHound touch; **AITRIP 4"** = bench/Bruce console; **T-Display-S3** = handheld Flock detector; **Heltec OLED** = mesh status. **1.3" OLEDs (×5)** = per-rail/temperature status readouts on the Pi (your `temp_monitor.py` plan).

### IO / serial plumbing
- All ESP/BW16/S2U at **115200** over USB → `/dev/ttyUSB*`/`ACM*`. CH340 (Gold), CP2102 (S2U/Heltec), native-USB (S2/S3) all enumerate on Linux automatically.
- **Pin udev rules** to give each board a stable symlink (e.g., `/dev/marauder24`, `/dev/c5-1`, `/dev/bw16-1`) so the dashboard/`marauder_core` binds the right node every boot regardless of plug order. (Multiple CH340s share VID:PID — use `ATTRS{serial}` or USB-port path.)

---

## 5. Data / control topology (how nodes talk to the Pi + each other)

**Serial-controlled nodes (Pi is master):**
- **Marauder nodes (C5 #1, Gold ×3, WROOM, CYD)** → your `headless-marauder-gui`/`marauder_core` CLI catalog (70-cmd) over serial; live AP/Station tables + `capture.py` logging.
- **BW16 ×3** → `AT+SCAN` / `AT+DEAUTHIDX=` / `AT+BEACONRANDOM=` / `AT+STOP` over serial. Add a thin BW16 panel to the dashboard (mirror the Marauder pattern).
- **GhostESP (C5 #2)** → serial CLI **and** its own web dashboard/AP (wardrive control, WiGLE export). Pi pulls the WiGLE CSV into the shared loot dir.
- **SuperWiFiDuck (S2U)** → WiFi web UI for DuckyScript; Pi links it from the dashboard and stores payloads.

**Network/IP nodes:**
- **RayHunter (Orbic)** → ADB over USB-C; Pi does `adb forward tcp:8080`, polls `/api/analysis` every ~5s → red/yellow/green stingray tile.
- **Meshtastic (Heltec)** → Meshtastic API/serial; Pi can bridge mesh text + push GPS/alerts out over LoRa as an off-grid backhaul.

**Cross-routing / fusion (the "cohesive deck" payoff):**
- **One GPS, all tools:** `gpsd` feeds Kismet, GhostESP wardrive (via Pi-tagged logs), and timestamps every node's capture.
- **Kismet as the aggregator:** Panda is the primary monitor source; a wardriving ESP can feed Kismet via **remote-capture** for a second vantage (set a unique `uuid=` per remote source — Kismet requirement).
- **Unified loot bus:** every node's output normalizes into the Pi capture dir → dashboard tails `latest.json`; correlate (e.g., a Flock OUI hit from T-Display-S3 + a Kismet AP fix + a GPS point = one geolocated detection).
- **Mesh exfil/alerting:** dashboard alerts (stingray/Flock/skimmer) can be pushed to the Meshtastic node for off-grid notification.

---

## 6. Prioritized shopping delta (specific to closing real gaps)

**Tier 1 — needed to make the deck whole / unblock validated capabilities**
1. **USB GPS puck (u-blox VK-162 or similar)** — you have *none*; Kismet wardriving + all geo-tagging depends on it. (~$15–18)
2. **Pi 5 DSI 22-pin→15-pin adapter cable** — the 7" Hosyond won't connect to Pi 5 without it. (~$5–8)
3. **Powered USB 3.0 hub with per-port switches** — the backbone of the switched power plan. (~$20–35)
4. **Pi 5 5V/5A USB-C PD source** (if Anker 347 can't sustain 5A) — undervolt = USB dropouts under Panda+hub load. (~$25–45)
5. **SMA bulkheads (×8) + U.FL→SMA pigtails** + a couple more **RP-SMA↔SMA adapters** for NRF24/BW16-duck polarity. (~$20–30)

**Tier 2 — adds unique capability you don't yet have**
6. **Orbic Speed RC400L + a dead SIM** → RayHunter IMSI/stingray detection (the *only* cellular-threat capability). (~$75 + ~$1)
7. **Replace the fried Pi Zero 2 W** if you still want RaspyJack (wired LAN attacks) / a docked Pwnagotchi — both are dead without it. (~$15–20 board)
8. **Heltec V4 case** (already owned per inventory) — confirm it fits V3; otherwise grab a V3 case for the detachable mesh node.

**Tier 3 — nice-to-have / future**
9. **CC1101 + NRF24 + PN532 wiring harness/perfboard** for CYD #2 HaleHound (you own the modules — just need clean breakout to the CYD pins).
10. **A second dual-band antenna or two** if you externalize more than one BW16.
11. **Pelican 1300 + foam / DIN-rail / L-brackets** for the chassis build (no 3D printer, per your constraint).

**Explicitly NOT buying / excluded:**
- **No operational RF jammer** (BlueJammer) — illegal (47 U.S.C. §333), no research exemption; the deck keeps the *lawful detector* side only.
- **No Project Nomad on the Pi 5** — it needs x64 (LattePanda); stays a companion, not chassis-core.
- You already own enough classic-ESP32 2.4GHz radios — don't buy more Golds; spares are spares.

---

## Sources (fact-checked against upstream)
- Marauder supported chips / C5 build / 2.4-only classic+S2: [DeepWiki — ESP32Marauder Supported Boards](https://deepwiki.com/justcallmekoko/ESP32Marauder/5.1-supported-boards-and-variants), [justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder)
- C5 dual-band 5GHz reality + Marauder/Bruce/GhostESP on Waveshare C5: [CNX — Apex 5 ESP32-C5 Marauder](https://www.cnx-software.com/2026/02/11/esp32-marauder-5g-apex-5-module-for-flipper-zero-combines-esp32-c5-two-sub-ghz-radios-nrf24-and-gps/), [Waveshare ESP32-C5 docs](https://docs.waveshare.com/ESP32-C5-WIFI6-KIT), [Flash Bruce on Waveshare C5 (YouTube)](https://www.youtube.com/watch?v=QIyJSpAXHEU), [Espressif ESP32-C5](https://www.espressif.com/en/products/socs/esp32-c5)
- Bruce supported boards (CYD/S3/C5): [BruceDevices/firmware](https://github.com/BruceDevices/firmware), [bruce.computer](https://bruce.computer/)
- GhostESP features/boards (wardrive, evil-portal, skimmer/pineapple/AirTag detect, C5/S3): [ghostesp.net](https://ghostesp.net/), [GhostESP supported boards](https://ghostesp.net/boards), [GhostESP-Revival/GhostESP](https://github.com/GhostESP-Revival/GhostESP)
- BW16 Vampire Deauther (2.4+5GHz deauth, AT+ serial, black 22-pin PCB): [vampel.github.io Vampire Deauther flasher](https://vampel.github.io/), [WiFiX-DualBand-Deauther](https://github.com/EmenstaNougat/WiFiX-DualBand-Deauther)
- ESP32-DIV / HaleHound chip + modules (S3, CC1101/NRF24/PN532): [cifertech/ESP32-DIV](https://github.com/cifertech/esp32-div), [JesseCHale/HaleHound-CYD](https://github.com/JesseCHale/HaleHound-CYD)
- ESP32-S2 native-USB BadUSB: [SuperWiFiDuck](https://github.com/wasdwasd0105/SuperWiFiDuck)
- Flock-You needs ESP32-S3 (WiFi-promiscuous ALPR catch): [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you), [0xXyc/flock-you-wifi-recon](https://github.com/0xXyc/flock-you-wifi-recon)
- Kismet remote-capture / multi-source UUID / gpsd: [Kismet Datasources](https://www.kismetwireless.net/docs/readme/datasources/datasources/), [Kismet Remote Capture](https://www.kismetwireless.net/docs/readme/remotecap/remotecap/)
- NRF24 Mousejack research: [Bastille MouseJack background via RogueMaster NRF24 docs](https://github.com/RogueMaster/flipperzero-firmware-wPlugins/blob/420/documentation/NRF24.md)