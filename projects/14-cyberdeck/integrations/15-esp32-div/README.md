# ESP32-DIV — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference:** [projects/15-esp32-div](../../../15-esp32-div/)
> **Deck role:** Handheld multitool companion — fills the deck's **Sub-GHz / IR / RFID-NFC / 2.4 GHz-raw** gaps
> **Status:** Evaluating / to build (MIT, open hardware)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **What it adds** | CC1101 **Sub-GHz**, **IR** (replay + universal remote), **RFID/NFC** read/clone, **2.4 GHz NRF24 spectrum scan**, deauth detector |
| **Form** | A **companion** (its own ESP32-S3 + touchscreen + battery) — rides in a foam bay, charges off deck USB. *Not* chassis-wired. |
| **Pi link** | Optional USB for log/profile offload (saved Sub-GHz/IR/RFID profiles live on its microSD) |
| **What we DON'T use** | Its jam modes (BLE Jammer, Protokill, Sub-GHz Jammer, RFID jam) — illegal to operate |
| **Overlap** | Covers the same ground as [Flipper Zero](../02-flipper-zero/) — pick one as your Sub-GHz/RFID/IR tool |

> **Why a companion, not a wired board:** like the Flipper, ESP32-DIV is a self-contained handheld
> with its own screen and battery. It doesn't need to bolt into the chassis — it just needs a bay and
> a charge port. Its value is the **bands the deck's ESP32s can't reach**: Sub-GHz (CC1101), IR, and
> RFID/NFC, plus a raw 2.4 GHz (NRF24) analyzer.

> **ESP32-DIV or Flipper?** They overlap heavily (Sub-GHz/RFID/NFC/IR). If you build ESP32-DIV you may
> not need the Flipper for those bands — ESP32-DIV is the open-source DIY route and adds the NRF24
> 2.4 GHz analyzer the Flipper lacks. The Flipper is more polished/closed. Don't buy both for the same job.

---

## What You Need

- An **ESP32-DIV** (build the open-hardware main board + RF shield, or buy a made one).
- microSD (FAT32) for captures / saved profiles / wardrive logs.
- Antennas for the CC1101 (Sub-GHz band of interest) and NRF24s.
- USB-C **data** cable (flashing + optional offload).

---

## Get It Running

### 1. Flash / set up
1. Build or obtain the board + shield (Gerbers/BOM upstream).
2. Flash firmware from the [repo](https://github.com/cifertech/esp32-div) release, or build from source
   (ESP32-S3 target), or use the device's **microSD "Update Firmware"**. Same flashing pattern as the
   rest of the kit — see [ESP Terminator](../13-esp-terminator/).
3. Insert the microSD; attach antennas.

### 2. Use it for the gaps (lawful features)
- **Sub-GHz (CC1101):** scan / replay / saved profiles for **your own** 315/433/868/915 MHz remotes.
- **IR:** universal remote + replay.
- **RFID/NFC:** read / clone / dump **your own** cards.
- **2.4 GHz Scanner:** raw NRF24 spectrum/airtime view — spot congestion/interference (complements the
  [interference detector](../16-bluejammer/)).
- **Deauth Detector:** defensive — same role as Marauder `sniffdeauth`.

### 3. Ride with the deck
- Foam bay + charge from the [powered USB](../parts/power/).
- Pull saved Sub-GHz/IR/RFID profiles off its microSD (or over USB) into your case notes / logs.

---

## Cyberdeck Compatibility Notes

- **No chassis slot / SMA / switch** — it's a self-powered handheld, not in the [master wiring table](../README.md).
- **Fills real gaps:** the deck's offensive radios are WiFi/BLE only (Marauder) + LoRa (Meshtastic);
  ESP32-DIV is what brings **Sub-GHz, IR, RFID/NFC** and a **raw 2.4 GHz analyzer**.
- **Overlaps:** WiFi/BLE attack features duplicate [Marauder](../01-esp32-marauder/) — use Marauder on
  the deck for those; use ESP32-DIV for the other bands. Sub-GHz/RFID/IR overlap the [Flipper](../02-flipper-zero/).
- **Jam modes excluded** — illegal to operate; don't use them (see [project 16](../16-bluejammer/) legal note).

## Standalone Mode

Fully standalone — its own ESP32-S3, touchscreen, and battery. Pull it from the deck and it's a
complete handheld multitool; the deck is just a charge bay + profile-offload point.

## Source / Upstream

- [cifertech/esp32-div](https://github.com/cifertech/esp32-div) (MIT) · [cifertech.net](https://cifertech.net)
- Full project notes: [projects/15-esp32-div](../../../15-esp32-div/)
