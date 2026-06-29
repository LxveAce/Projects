# Cyberdeck Integration: OUI-Spy — Passive Surveillance Detection

> **Source project:** [Project 17 — OUI-Spy](../../../17-oui-spy/)
> **Integrations index:** [integrations/](../README.md)
> **Board:** LILYGO T-Display S3 (ESP32-S3, built-in 1.9" TFT) — running OUI-SPY Unified Blue
> **Deck role:** Passive surveillance detector + RF direction-finding companion
> **Power:** Own USB / LiPo (companion — **not** chassis-wired, no hub switch / SMA slot)
> **Antenna:** ESP32-S3 internal (2.4 GHz WiFi/BLE) · optional 2.4 GHz Yagi for Foxhunter
> **Display:** Built-in 1.9" ST7789 color TFT (self-contained) + buzzer + NeoPixel

---

## What This Does in the Deck

OUI-Spy is the deck's **passive, receive-only surveillance detector**. It listens for the
wireless fingerprints of cameras, drones, and trackers and tells you what's watching *you* —
the inverse of the deck's offensive tools. It never transmits, deauths, or injects: it only
matches the **OUI** (manufacturer prefix) of MAC addresses it overhears against a watchlist.

Four modes, switched from a web menu at boot (no reflashing):

- **Detector** — multi-target BLE scanner (Flock, Ring, AirTag-class trackers, custom OUIs)
- **Foxhunter** — single-target RSSI direction-finding; beeps faster as you near the device
- **Flock-You** — Flock Safety / Raven ALPR camera detection (WiFi promiscuous + BLE)
- **Sky Spy** — FAA Remote ID drone detection (decodes ASTM F3411: serial, GPS, operator)

It runs as a **companion** like the [Flipper](../02-flipper-zero/) and
[ESP32-DIV](../15-esp32-div/): pocketable, battery-powered, used by hand — not bolted to the
chassis. That's deliberate — **Foxhunter direction-finding means you walk toward the signal**,
so it can't live inside a sealed case.

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Board** | **LILYGO T-Display S3** (ESP32-S3R8, 8 MB PSRAM, 16 MB flash) |
| **Why S3** | Full BLE 5.0 — required for Detector + Foxhunter. Classic ESP32 is WiFi-only |
| **Firmware** | **OUI-SPY Unified Blue** (all 4 modes, web boot selector) |
| **Display** | Built-in 1.9" ST7789 color TFT — no wiring, no Pi needed |
| **Alerts** | Passive piezo buzzer + WS2812B NeoPixel (wire to any free GPIO) |
| **Power** | Onboard JST 1.25 mm LiPo (500–1000 mAh) — charges over USB-C |
| **Antenna** | Internal PCB for general scanning; add a 2.4 GHz Yagi (10.5 dBi SMA) for Foxhunter |
| **Role** | Companion (handheld) — **no SMA bulkhead, no hub switch** assigned |

> **$0 start (fallback):** you can begin **WiFi-only** OUI scanning today on an owned classic
> ESP32 (Gold #3 or a spare CYD) with the standalone [`flock-you`](https://github.com/colonelpanichacks/flock-you)
> `promiscious-dev` firmware — Flock-You WiFi + Sky Spy promiscuous work fine. But the classic
> ESP32 lacks BLE 5.0, so **Detector and Foxhunter need the T-Display S3**. See
> [Project 17 §4](../../../17-oui-spy/#4-compatible-hardware----all-boards--displays) for the
> full board matrix.

---

## Why OUI-Spy When the Deck Already Detects Flock / BLE / Drones?

The deck's existing radios cover *offense* and broad scanning; OUI-Spy is the focused,
passive, **walk-around** detector that ties those threads together on one screenless-optional unit:

| Capability | Deck already has | OUI-Spy adds |
|------------|------------------|--------------|
| Flock ALPR cameras | [Gold #2 / WROOM-32 (Project 06)](../06-flock-drone-detection/) | Same OUI lists, **portable + BLE layer** |
| BLE tracker detection | [Gold #3 (Project 08)](../08-ble-detection/), [Chasing Your Tail (10)](../10-chasing-your-tail/) | Unified Detector with custom watchlists |
| Drone Remote ID | WROOM-32 (Project 06) | Full ASTM F3411 decode (GPS + operator) |
| **RF direction-finding** | ✗ | **Foxhunter** — physically locate a detected device |
| **All-in-one passive unit** | ✗ (spread across boards) | One ESP32-S3, four modes, no transmit |

It overlaps on purpose and is **passive-only** — keep the transmit-based forks
(Remote-ID-Spoofer "Red Edition", UniPwn) **off the deck**; see Legal below.

---

## What You Need

- LILYGO T-Display S3 (~$18–25) — built-in TFT + JST LiPo connector
- Passive piezo buzzer (3.3 V, through-hole) — ~$1–3
- 3.7 V LiPo, 500–1000 mAh, JST-SH 1.25 mm — ~$5–8
- 2× Dupont jumpers (buzzer to a free GPIO) — from the REXQualis kit (owned)
- USB-C **data** cable for flashing
- *Optional:* 2.4 GHz Yagi (10.5 dBi, SMA) for Foxhunter — ~$8–12

---

## Get It Running

### 1. Flash the firmware

Build Unified Blue for the S3 and flash over USB-C:

```bash
git clone https://github.com/colonelpanichacks/oui-spy-unified-blue.git
cd oui-spy-unified-blue
pip install platformio
pio run -t upload            # auto-detects the T-Display S3 port
# if it won't enter download mode: hold BOOT (GPIO0) → tap RST → release BOOT
```

esptool path (S3 — bootloader at `0x0`, not `0x1000`):
```bash
esptool.py --chip esp32s3 --baud 921600 write_flash \
  0x0 firmware/bootloader.bin \
  0x8000 firmware/partitions.bin \
  0xe000 firmware/boot_app0.bin \
  0x10000 firmware/oui-spy-unified-blue.bin
```

### 2. Wire the alert hardware

- Buzzer **(+)** → any free GPIO (e.g. GPIO43), buzzer **(–)** → GND.
- NeoPixel DIN → a free GPIO; VCC → 3.3 V, GND → GND. (Optional — the TFT already shows status.)
- Plug the LiPo into the JST 1.25 mm port (check silkscreen polarity) — charges over USB-C.

### 3. Verify

1. Power on — expect **4 ascending beeps** and the TFT to light up.
2. On your phone, join WiFi `oui-spy` / `ouispy123`, browse to `192.168.4.1`.
3. Pick **Detector** → it reboots → join `snoopuntothem` / `astheysnoopuntous` → the
   Detector page loads. NeoPixel breathing pink = scanning.
4. Hold **BOOT 2 s** any time to return to the mode selector.

---

## Cyberdeck Compatibility Notes

- **No chassis resources consumed** — companion device, so it takes **no SMA bulkhead and no
  hub switch** (it isn't in the [master wiring table](../README.md#the-master-wiring-decisions-quick-reference),
  same as the Flipper/ESP32-DIV/NyanBOX).
- **Pi dashboard (optional):** OUI-Spy emits JSON over serial at 115200 baud. If you dock it to
  a Pi USB port, the [dashboard](../parts/dashboard/) can tail Flock/drone detections alongside
  Kismet and Marauder. For Sky Spy, `mesh-mapper.py` plots drones on a map.
- **GPS:** uses the phone browser's geolocation in Flock mode — no draw on the deck's
  [shared VK-162 GPS](../parts/gps/).
- **Frequency:** 2.4 GHz only — no conflict with the deck's SMA radios.

## Standalone Mode

This is its natural state. Charge it, drop it in a pocket, walk. All four modes run with the
deck off and no Pi, laptop, or phone (the phone is only needed for first-time mode config and
Flock GPS). Foxhunter + a Yagi turns it into a handheld RF locator for a camera you've detected.

## Legal — passive only

OUI-Spy Blue is **receive-only**: it captures publicly broadcast WiFi management frames and BLE
advertisements (the ECPA "readily accessible to the general public" exception). It never
transmits. **Do not** put the transmit-based forks on the deck — **Remote-ID-Spoofer** (spoofs
FAA Remote ID, violates 14 CFR 89 / FCC) and **UniPwn** (robot exploitation, CFAA) are excluded,
mirroring the deck's [no-jammer rule](../16-bluejammer/). Full analysis in
[Project 17 §14](../../../17-oui-spy/#14-legal-considerations).

## Source / Upstream

- Unified Blue firmware: [colonelpanichacks/oui-spy-unified-blue](https://github.com/colonelpanichacks/oui-spy-unified-blue)
- Omni fork (7–8 concurrent engines + Flutter app): [lukeswitz/oui-spy-unified-blue](https://github.com/lukeswitz/oui-spy-unified-blue)
- WiFi-only fallback firmware: [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you) (`promiscious-dev`)
- Creator: colonelpanichacks · [colonelpanic.tech](https://colonelpanic.tech/)
- Full options, all boards, OUI databases, legal: [Project 17 — OUI-Spy](../../../17-oui-spy/)

---

*Decision-made guide for the cyberdeck build. See [Project 17](../../../17-oui-spy/) for the full research and all options.*
