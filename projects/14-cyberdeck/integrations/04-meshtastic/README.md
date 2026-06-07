# Meshtastic — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/04-meshtastic](../../../04-meshtastic/)
> **Deck role:** Off-grid encrypted mesh node (915 MHz LoRa)
> **Status:** Troubleshooting — node not detected over USB (driver / cable). See [Verify](#3-verify) for the fix.

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Board** | Heltec LoRa V3 |
| **Chip** | **ESP32-S3 + SX1262** (915 MHz LoRa, onboard 0.96" OLED) |
| **Firmware** | Meshtastic, latest stable |
| **Flash tool** | [flasher.meshtastic.org](https://flasher.meshtastic.org/) — pick **"Heltec WiFi LoRa 32 V3"** |
| **Region** | **US** (915 MHz) — mandatory before the radio transmits |
| **Display** | onboard 0.96" OLED (no extra screen) |
| **Antenna** | IPEX → pigtail → **SMA bulkhead #4** ("MESH") → 915 MHz LoRa antenna |
| **Power** | Powered USB hub, gated by toggle **SW4** |
| **Control** | Pi 5 over serial (115200) via the `meshtastic` Python SDK |

> **Why the Heltec V3:** it's the only LoRa board in the inventory, purpose-built for Meshtastic
> with first-class firmware support, an SX1262 radio, and a built-in OLED — so it shows node
> status standalone with no extra display wired into the deck.

> **Critical:** **attach the 915 MHz antenna to SMA bulkhead #4 BEFORE powering on / transmitting.**
> Keying the LoRa radio with no antenna can permanently damage the SX1262 chip.

> **Band:** 915 MHz LoRa does **not** overlap the 2.4/5.8 GHz radios — Meshtastic can transmit
> at the same time as every other tool with zero cross-talk.

---

## What You Need (from the repo inventory)

- Heltec LoRa V3 (Meshnology N30, ESP32-S3 + SX1262, 915 MHz) — from the [INVENTORY](../../../../INVENTORY.md)
- 915 MHz LoRa antenna 3 dBi #1 + IPEX pigtail → SMA bulkhead #4
- Boobrie RP-SMA→SMA adapter #1 (if mating a larger base-station antenna)
- USB-C **data** cable for flashing (not charge-only)
- Chrome or Edge (WebSerial required for the web flasher)

---

## Get It Running

### 1. Flash the firmware

1. Open **Chrome or Edge** (WebSerial — Firefox/Safari won't work).
2. Go to [flasher.meshtastic.org](https://flasher.meshtastic.org/).
3. Plug the Heltec V3 into your PC with a USB-C **data** cable.
4. Select device **"Heltec WiFi LoRa 32 V3"**, latest **stable**.
5. For a fresh board choose **"Full Erase and Install"**; click Flash and wait for "complete" — don't disconnect mid-flash.

Then set the region (mandatory — the radio will not transmit until it's set):
```bash
meshtastic --port /dev/ttyUSB0 --set lora.region US
```
(Install the SDK first with `pip install meshtastic`.)

### 2. Wire it into the deck

- **Mount:** Heltec V3 on the ESP32 rail via M3 standoffs.
- **Antenna:** snap the IPEX pigtail straight down onto the Heltec's socket (feel the click —
  never twist), route to **SMA bulkhead #4** ("MESH"), screw the 915 MHz antenna on outside.
  **Antenna must be attached before SW4 powers the board.**
- **Power:** USB from the powered hub → inline **toggle SW4** → Heltec V3.
- **Data:** the same USB run carries serial to the Pi 5 (`/dev/ttyUSB0`, 115200 baud).
- **Display:** onboard 0.96" OLED — nothing else to wire.

### 3. Verify

```bash
pip install meshtastic
meshtastic --port /dev/ttyUSB0 --info     # should print node + LoRa config
```
The onboard OLED should also show the node screen once powered via SW4.

> **Current status — node not detected over USB.** The board powers (OLED lights) but the Pi
> doesn't enumerate it as a serial device. The two known causes, in order:
>
> 1. **Charge-only cable** (the #1 cause). Swap in a known **data** cable and re-test.
> 2. **Missing USB-serial driver.** The Heltec V3 uses a **CH340 / CP2102** bridge — install
>    the matching driver ([WCH CH341SER](https://www.wch.cn/downloads/CH341SER_ZIP.html) or
>    [Silicon Labs CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)),
>    then reboot. If it still won't enumerate, hold **BOOT** while plugging in to force
>    bootloader mode, then re-flash.
>
> Full diagnostic flow: [Section 3 of the source guide](../../../04-meshtastic/#3-troubleshooting----node-not-detected-via-usb).

---

## Cyberdeck Compatibility Notes

- **USB/serial budget:** consumes one powered-hub port; Pi reads it at `/dev/ttyUSB0` (115200).
- **Band isolation:** owns **915 MHz** only — completely separate from the 2.4/5.8 GHz radios,
  so no RF conflict and it can transmit concurrently with everything else.
- **Antenna:** owns bulkhead **#4** only — no conflict with the other radios.
- **GPS:** shares the deck's [USB GPS](../parts/gps/) so the node can broadcast position into the
  mesh (set position from the Pi via the SDK rather than adding a GPS module to the Heltec).
- **Dashboard:** the Pi 5 [dashboard](../parts/dashboard/) can read the node list, signal reports,
  and incoming messages via the `meshtastic` SDK and surface them live.
- **Power modes:** SW4 fully cuts Meshtastic power for the "stealth" / low-draw profiles — zero
  915 MHz emission when off.

## Standalone Mode

Flip **SW4** on with the Pi off and the Heltec V3 runs Meshtastic entirely on its own — onboard
OLED for status, BLE pairing to the Meshtastic phone app (Android/iOS) for config and messaging
(headless PIN default **123456** — change it). Pull the board out of the deck and it's the same
node on a bench. Nothing about the deck wiring is required for it to mesh.

## Source / Upstream

- Upstream / flasher: [meshtastic.org](https://meshtastic.org/) · [flasher.meshtastic.org](https://flasher.meshtastic.org/)
- Full options, hardware list, channels/encryption, range, troubleshooting: [projects/04-meshtastic](../../../04-meshtastic/)
