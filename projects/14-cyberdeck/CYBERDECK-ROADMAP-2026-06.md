# Cyberdeck Re-Refinement Roadmap — June 2026 (inventory-anchored)

*The "clear line forward" — every mini-project mapped to the hardware that actually arrived, in
build order, so you can start. Anchored to **Cyber Controller v1.1.0** + the June 2026 parts haul.
Companion to `CYBERDECK-V2-ARCHITECTURE.md` (board→role), `BUILD-GUIDE-STEP-BY-STEP.md` (assembly),
`FIRMWARE-DEVICE-SPECIALTIES.md` (per-firmware fit), and `VISION-ROADMAP.md` (the why).*

Status legend: ✅ have it · 🟡 partial / verify qty · ⏳ still shipping · 🔌 needs assembly/flash

---

## 1. Inventory snapshot (reconciled from order screenshots, June 2026)

> Quantities from screenshots may be off by one — treat as a checklist to confirm, not gospel.

### Compute / SBC core
- ✅ **Raspberry Pi 5 (CanaKit Starter Kit, 8GB)** + a 2nd **Pi 5 8GB w/ Active Case** — the starter kit should include the **official 27 W USB-C PSU** (critical for Pi 5) + active cooler.
- ✅ **PiSugar S 1200 mAh UPS** (Pwnagotchi power module, Pi Zero class)
- ✅ **Cable Matters USB→Ethernet adapter** · ✅ JSAUX Micro-HDMI→HDMI (Pi 5)

### ESP32 / microcontroller fleet
- ✅ ESP-WROOM-32 dev boards (multipack) · ✅ 3-pack **Lonely Binary ESP32 Gold** · ✅ 5-pack ESP32 (CP2102, ext. antenna) · ✅ KEDIKU 5-pack ESP32+OLED
- ✅ 3-pack **Lonely Binary ESP32-S2 mini** · ✅ **LILYGO T-Display-S3** · ✅ ELEGOO ESP32 480×480 touch · ✅ **ESP32-C5** (dual-band WiFi-6)
- ✅ **3× BW16 / RTL8720DB** (DC Buying) · ✅ **Heltec LoRa V3** (Meshtastic) + Heltec V4 case
- ✅ **Elecrow Emensta PCBs** (order #301544): ESP32-RF, ESP32-RF_Ebyte, **WiFiX DIY-PCB**, **C3Mini-RF**

### Radios / sensors
- ✅ **nRF24L01+ modules — plenty** (HiLetGo + Hosyond 6-pack w/ antenna + Elecrow) → covers BlueJammer's "up to 4"
- ⏳ **2× CC1101** (315/433/868/915 MHz + SMA) — **arriving ~June 23–30** → the sub-GHz radio for **FreqFoxRF**
- ✅ **PN532 NFC/RFID module** (HiLetgo)
- ✅ **OLEDs** — Hosyond 3× 1.3" SH1106 128×64 (BlueJammer/FreqFox display)

### Displays
- ✅ Pi: **7" DSI 800×480 capacitive** (Hosyond) · **5" Elecrow resistive 800×480** · **1.44" SPI HAT w/ joystick** (RaspyJack) · **2.13" e-ink HAT**
- ✅ ESP: 2.8" CYD (ESP-WROOM-32 240×320) · 4" ILI9488 · 4" ST7796 · T-Display-S3

### Antennas / RF accessories
- ✅ **Panda PAU0F AXE3000 tri-band USB WiFi** → **monitor-mode/Kismet on the Pi** (fills the Kali-Pi5 "no Nexmon" gap!) · ✅ extra USB WiFi dongle
- ✅ U.FL/SMA: DIYmall 2.4G U.FL · Meshtastic long-range (U.FL) · Bingfu short · Eightwood RP-SMA 3-pack · Boobrie RP-SMA · **Rydocyee U.FL→SMA pigtails**

### Network / IMSI
- ✅ **Orbic Speed RC400L 4G LTE hotspot** → **RayHunter** IMSI-catcher detector target

### Power / storage / tools
- ✅ EEMB LiPo ×2 · SunFounder BreadVolt PSU · ✅ 128 GB µSD multipack + KIOXION 10× 16 GB + INLAND USB drives + SD cases
- ✅ **Fluke 17B+ DMM** · soldering pad · Kapton tape · header/jumper kits · ELEGOO breadboards · **ALLECIN cap kit (has the 10 µF BlueJammer brownout caps)** · buzzer
- ✅ Input: **ProtoArc foldable keyboard+touchpad** · **Rii K06 mini BT keyboard (IR learning)**

**Bottom line:** the deck is ~95% sourced. The only project-critical part still in transit is the **CC1101 (FreqFoxRF), ~Jun 23–30.** Everything else can be built now.

---

## 2. The deck itself (the chassis the projects plug into)

- **Brain:** Pi 5 (8 GB) running **Kali** (see §4) — orchestration + Kismet + RayHunter host + Cyber Controller.
- **Screen:** 7" DSI (primary) or 5" Elecrow; 1.44"/2.13" HATs for dedicated node readouts.
- **Input:** ProtoArc foldable (full) / Rii K06 (one-hand).
- **Radio bay:** the ESP/BW16 fleet on a powered USB hub, each pinned to its best firmware; Panda tri-band for the Pi's own WiFi attacks.
- **Power:** 27 W PSU bench-side now; LiPo + UPS for the portable build later.
- **Second Pi 5** = spare / dedicated Kismet or RayHunter host if you want to split roles.

---

## 3. Per-project roadmap (build order within each)

| Project | Hardware (status) | Firmware / role | CC support | Start here |
|---|---|---|---|---|
| **Marauder / GhostESP / Bruce / DIV / HaleHound** | ESP32 fleet ✅ | WiFi/BLE recon, the core ESP arsenal | ✅ v1.1.0 (HW-validated) | Flash from CC; already proven. Pin each spare board to one firmware. |
| **BW16 Vampire / WiFiX dual-band deauther** | 3× BW16 ✅, WiFiX PCB ✅ | 2.4+5 GHz deauth/recon | ✅ rtl8720 backend | Flash Vampire (have) → flash **WiFiX** for true dual-band. Lab-only label. |
| **Meshtastic** | Heltec V3 ✅ + antennas | LoRa mesh comms | ✅ + CLI configured | Done — already region-set + talking. Add 2nd node for a real mesh. |
| **BlueJammer-V2** ⚠️lab-only | ESP32 ✅ + 3–4× nRF24 ✅ + OLED ✅ + 10 µF caps ✅ + BW16 ✅ | 2.4 GHz RF study (illegal to operate) | **to add** (2 profiles) | §5 — parts are all here. CC flashes + reads telemetry only; never keys TX. |
| **FreqFoxRF** 🦊 | CC1101 ⏳(Jun 23–30) + ESP32-C3 + OLED ✅ | **sub-GHz** capture/replay (Flipper-like) | new profile (after parts) | Best non-jammer add. Build the moment the CC1101 lands. |
| **ModuLoRa** | ESP32 ✅ + REYAX RYLR998 (need) | long-range LoRa telemetry/mesh | optional profile | Order the RYLR998 if you want it; low priority vs. Meshtastic. |
| **RayHunter** | **Orbic RC400L ✅** | IMSI-catcher detector | ✅ ADB backend | Flash from CC (ADB). You have the exact target device. |
| **Pwnagotchi** | Pi Zero (need a Zero 2 W) + PiSugar ✅ | WiFi handshake harvester | ✅ SD-image | Needs a Pi Zero 2 W (the old one's fried). PiSugar/UPS ready. |
| **RaspyJack** | Pi + **1.44" HAT ✅** | Pi-based pentest UI | ✅ SD-image | Image a spare µSD; the joystick HAT is the intended UI. |
| **NFC/RFID** | **PN532 ✅** | 13.56 MHz read/clone | via HaleHound/host | Wire PN532 to an ESP or the Pi; pairs with the HaleHound NFC events. |

---

## 4. Pi 5 → Kali (the core) — NOW UNBLOCKED

You have the **Pi 5 + 27 W PSU + a USB→Ethernet adapter**, so the reliable path is clear:

1. **Install Raspberry Pi Imager** (Windows). Choose OS → **Kali Linux** (it's in the list; auto-verifies the `kali-linux-2026.x-raspberry-pi-arm64.img.xz`). Choose Storage → the **SD (E:)** → Write. **Decline** the "OS customization" prompt — *Kali ignores it.*
2. Re-insert the SD; on the small boot partition I'll have you create an **empty file named `ssh`** (no `.txt` — turn on "show file extensions" first).
3. **Networking = Ethernet** (you have the adapter): plug Pi → router. No WiFi creds needed.
4. Boot on the **27 W PSU**, wait ~2 min, then `ssh kali@kali.local` (or find its IP in your router's DHCP list). Login **kali / kali** → **change it immediately** (`passwd`).
5. Monitor-mode WiFi on the Pi = the **Panda PAU0F** (the internal Pi 5 WiFi has no Nexmon under Kali).

If `kali.local` won't resolve, fall back to the router's client list or `nmap -sn`. EEPROM bootloader update only if it refuses to boot the SD (Imager → Misc utility images → Pi 5 bootloader).

---

## 5. BlueJammer-V2 → Cyber Controller (parts in hand)

Two boards, both already match CC backends:
- **ESP32-WROOM-32U** (jamming engine, ≤4× nRF24L01+, OLED) → **esptool**, offsets `0x1000 / 0x8000 / 0x10000`, **no boot_app0**.
- **BW16/RTL8720DN** (5 GHz web UI + UART master) → **existing rtl8720 backend**, same km0/km4/image2 bundle.

**CC work:** add `bluejammer-esp32` + `bluejammer-bw16` FirmwareProfiles (fetch bins from the v0.2 GitHub Release at flash time — closed-source, don't vendor — and **SHA-256-pin** them), JSON profiles, an optional info-only parser, and the **`illegal-tx` lab-only label**. **CC never operates the transmitter** — it flashes + reads telemetry only; the device's only TX triggers are its own button + web UI. Build the hardware per the repo wiring (NRF1–4 on fixed pins, **10 µF cap per module VCC/GND** — you have the cap kit). Hardware: ESP32 ✅, BW16 ✅, nRF24 ✅, OLED ✅, caps ✅ → **nothing blocking.**

---

## 6. Build phases (suggested order)

1. **Pi core up** — flash Kali, SSH in, install CC + Kismet (Panda adapter). *(Now.)*
2. **ESP arsenal** — pin each spare board to one firmware via CC; confirm the dual-board cross-comm/broadcast. *(Now.)*
3. **BlueJammer-V2** — add CC profiles + assemble the board (lab study). *(Now — code + build.)*
4. **RayHunter** — flash the Orbic. *(Now.)*
5. **FreqFoxRF** — build when the CC1101 arrives (~Jun 23–30).
6. **RaspyJack / Pwnagotchi** — image spare µSDs (Pwnagotchi needs a Pi Zero 2 W).
7. **Chassis + power + portable** — displays, keyboard, LiPo/UPS, antenna bulkheads.
8. **Then:** websites + branding refresh (purple LxveAce / green CC), per the Emensta-inspired revamp.

---

## 7. Still to acquire (small gaps)

- **Pi Zero 2 W** (for Pwnagotchi — the old one is fried) · **REYAX RYLR998** (only if doing ModuLoRa) · a **WROOM-32U** specifically if you want the exact BlueJammer board (any classic ESP32 works for study).
- Confirm the **27 W PSU** came with the CanaKit (Pi 5 power is the #1 gotcha).
- Chassis (Pelican 1300 per the prior plan) + toggle switches + SMA bulkheads for the final enclosure.
