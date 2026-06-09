# Cyberdeck Integration: HaleHound + IoT Recon

> **Source project:** [Project 18 — HaleHound](../../../18-halehound/)
> **Board:** ESP32 2.8" CYD Touchscreen #2
> **Deck role:** Multi-protocol attack station + IoT Recon credential harvester
> **Power:** Hub → switch SW8
> **Antenna:** Internal PCB (2.4GHz ESP32 built-in)
> **Display:** Built-in 2.8" touchscreen (self-contained)

---

## What This Does in the Deck

HaleHound on CYD #2 is a **standalone multi-protocol attack station** that does NOT require the Pi 5. It has its own touchscreen, its own menus, and operates independently. You tap through attacks on its screen.

**Key capabilities in the deck:**
- **IoT Recon** — connect to a WiFi network and brute-force credentials on every IoT device on the LAN
- **WiFi deauth/beacon/karma** — same category as Marauder but on a separate board
- **BLE attacks** — Cinder, Spoofer, Predator, Lunatic Fringe (tracker detection)
- **SubGHz** (with CC1101) — replay attacks, brute force, Tesla charge port opener
- **NFC/RFID** (with PN532) — card read/clone/brute force
- **Defensive** — WiFi Guardian, Stalkerware Detect

### Why Not Just Use Marauder?

Marauder focuses on WiFi/BLE. HaleHound adds SubGHz, NFC, IR, and most importantly **IoT Recon** — automated LAN scanning with credential brute force that Marauder doesn't have. They're complementary, not redundant:

| Task | Use Marauder (Gold #1 / C5) | Use HaleHound (CYD #2) |
|------|----------------------------|------------------------|
| WiFi deauth | ✓ | ✓ |
| 5GHz attacks | ✓ (C5 boards only) | ✗ |
| BLE spam/detect | ✓ | ✓ |
| IoT Recon (LAN brute) | ✗ | **✓** |
| SubGHz replay | ✗ | ✓ (CC1101) |
| NFC clone | ✗ | ✓ (PN532) |
| PCAP capture | ✓ | ✗ |
| Evil portal | ✓ | ✓ (GARMR) |

---

## Hardware Assignment

| Component | Source | Notes |
|-----------|--------|-------|
| CYD 2.8" Touchscreen #2 | INVENTORY | Reflash from stock to HaleHound |
| Micro SD card (16GB+) | INVENTORY | Loot storage + custom creds |
| CC1101 module | **Purchase** (~$5) | Optional: SubGHz capability |
| NRF24L01+PA+LNA | **Purchase** (~$5) | Optional: 2.4GHz radio attacks |
| PN532 V3 (SPI mode) | **Purchase** (~$7) | Optional: NFC/RFID |

### CYD #2 Reassignment

CYD #2 was previously shared between Flock display and general use. With this change:
- **CYD #1:** Stays as Marauder touchscreen (standalone, Gold #1)
- **CYD #2:** Reflashed to HaleHound (standalone, multi-protocol)
- Flock display role moves to the Pi 5 dashboard (Flask UI on 7" DSI)

---

## Flashing for the Deck

1. Connect CYD #2 via USB
2. Go to [halehound.com](https://halehound.com/)
3. Select "ESP32-2432S028R (2.8" CYD)"
4. Flash via web — takes ~60 seconds
5. Insert micro SD card for loot storage
6. Boot — HaleHound touchscreen menu appears

---

## Standalone Mode

Pull CYD #2 out of the deck → plug into any USB power source → full HaleHound toolkit on its own screen. No Pi, no laptop, no phone needed. Pocket-sized attack station.

---

## Deck Placement

CYD #2 mounts vertically on the side panel or DIN rail inside the Pelican case. Its 2.8" screen faces up/out for touch access. USB cable runs to the powered hub for power (and optionally to Pi 5 for serial monitoring).

---

*Decision-made guide for the cyberdeck build. See [Project 18](../../../18-halehound/) for the full research and all options.*
