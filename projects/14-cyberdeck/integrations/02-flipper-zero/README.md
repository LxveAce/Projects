# Flipper Zero — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/02-flipper-zero](../../../02-flipper-zero/)
> **Deck role:** Handheld sub-GHz / RFID / NFC / IR companion
> **Status:** Not yet purchased (~$170) — docks/charges via deck USB, not chassis-mounted

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Device** | Flipper Zero (STM32WB55RG, sub-GHz CC1101, NFC ST25R3916, 125 kHz RFID, IR, iButton) |
| **WiFi add-on** | **AWOK Dynamics Dual C5 Touch** (dual ESP32-C5-WROOM, 2.4/5 GHz, touchscreen, GNSS) |
| **Flipper firmware** | **Momentum** (`momentum-fw.dev/update`) after a 1–2 week stint on Official |
| **Add-on firmware** | Marauder/wardriving build via **ESP Terminator** (Chrome) or C5 Py Flasher |
| **SD card** | KOOTION 16 GB micro SD (FAT32) — from [INVENTORY](../../../../INVENTORY.md) |
| **Deck role** | Sub-GHz / RFID / NFC / IR — *not* WiFi/BLE (the deck's ESP32s own that) |
| **Mounting** | None — docks in a charge/USB bay, not bolted to the chassis |

> **Why sub-GHz/RFID/NFC/IR and not WiFi:** the deck's three Lonely Binary Gold boards
> already cover WiFi/BLE — [Marauder on Gold #1](../01-esp32-marauder/), Flock on Gold #2,
> BLE on Gold #3. The Flipper's unique value in the kit is the radios *nothing else in the
> deck has*: sub-GHz (315/433/868/915 MHz), 13.56 MHz NFC, 125 kHz RFID, IR, and iButton.

> **Why the Dual C5 Touch over a bare inventory ESP32:** standard ESP32 dev boards are
> **not pin-compatible** with the Flipper GPIO header. The AWOK board is purpose-built for
> the header and adds 5 GHz + GPS. It rides along only if/when you want Marauder-over-Flipper
> off-deck — on the deck, Gold #1 is still the primary WiFi tool.

---

## What You Need

- **Flipper Zero** (~$169) — from [flipper.net](https://flipper.net/products/flipper-zero) or an
  [authorized reseller](https://flipper.net/pages/resellers). Not Amazon/eBay (counterfeit/seizure risk).
- **AWOK Dynamics Dual C5 Touch** (~$170, frequently sold out) — only if you want WiFi-over-Flipper
- **KOOTION 16 GB micro SD** (FAT32) — already in [INVENTORY](../../../../INVENTORY.md)
- **USB-C data cable** — for qFlipper flashing and the deck dock (USB-C, 1A charge)
- **A PC with qFlipper** and Chrome/Edge (WebSerial) for the add-on flasher

---

## Get It Running

### 1. Flash / set up the Flipper

1. Insert the micro SD (chip side **up**) until it clicks.
2. Hold **BACK** 3 s to power on; set language and time zone (the dolphin guides you).
3. Install **qFlipper** (flipperzero.one/update), connect over USB-C, accept the update to the
   latest **Official** firmware. Do not disconnect mid-update.
4. Pair the **Flipper mobile app** over BLE (remote control, file transfer, wireless updates).
5. After 1–2 weeks on Official, switch to **Momentum**: open `momentum-fw.dev/update` in a
   browser, connect over USB, follow the web updater. Momentum removes the regional frequency
   lock, adds rolling-code TX, Subdriving (GPS-tagged sub-GHz), and 183+ apps.

### 2. (Optional) Flash the Dual C5 Touch add-on

1. Power **off** the Flipper.
2. Seat the Dual C5 Touch onto the GPIO header; press firmly.
3. Attach the two external 2.4/5 GHz antennas.
4. Flash WiFi firmware (board ships blank) via **ESP Terminator** (espterminator.com, Chrome) or
   **C5 Py Flasher** — pick the wardriving / offensive build per the
   [full guide](../../../02-flipper-zero/). Same web-flasher workflow as [Marauder](../01-esp32-marauder/).

### 3. Dock with the deck

- **No chassis mount.** The Flipper lives in a dock/charge bay, charging off the deck's
  powered USB ([power guide](../parts/power/)) over USB-C at up to 1A.
- **Pi 5 link:** connect the Flipper to the Pi 5 over USB for **qFlipper** or the **CLI** —
  file pulls (saved sub-GHz/NFC/RFID dumps), firmware updates, and scripting.
- **It runs on its own battery** (2100 mAh, ~28-day standby), so the deck only needs to top it up.

### 4. Verify

- Power on → main menu shows **Sub-GHz, 125 kHz RFID, NFC, Infrared, iButton, GPIO, Settings**.
- qFlipper on the Pi 5 detects the device and shows the SD file tree.
- (Add-on) Marauder/wardriving app on the Flipper lists nearby APs via the Dual C5 Touch.

---

## Cyberdeck Compatibility Notes

- **No board/antenna/switch slot.** Unlike Gold #1–#3, the Flipper is **not** in the
  [master wiring table](../README.md) — it owns no SW toggle and no SMA bulkhead. It docks via USB.
- **Radio coverage, no overlap:** sub-GHz (CC1101, up to 20 dBm), NFC (ST25R3916), 125 kHz RFID,
  IR (940 nm TX), and iButton are bands **no other deck board provides** — pure additive coverage.
- **WiFi/BLE is deliberately deferred** to the deck's ESP32s. The Dual C5 Touch is there only for
  off-deck WiFi work; on the deck, [Marauder on Gold #1](../01-esp32-marauder/) stays primary.
- **USB budget:** one USB-C run to the Pi 5 doubles as charge + data; nothing on the powered hub.
- **Stealth profile:** with no fixed RF tie-in, the Flipper can be pulled entirely for the deck's
  low-emission profiles — undock it and the deck's RF footprint is unchanged.

## Standalone Mode

The Flipper Zero is **inherently standalone** — it's a self-contained handheld with its own
screen, D-pad, battery, and SD card. Undock it from the deck and every function (sub-GHz, NFC,
RFID, IR, iButton, BadUSB) works in the hand with zero deck dependency. The deck is just a
charge dock and an occasional Pi 5 file/CLI bridge; pull it out and it loses nothing.

## Source / Upstream

- Momentum firmware: [momentum-fw.dev](https://momentum-fw.dev/) · [Next-Flip/Momentum-Firmware](https://github.com/Next-Flip/Momentum-Firmware)
- Add-on board: [AWOK Dynamics Dual C5 Touch](https://awokdynamics.com/products/dual-c5-touch)
- Full options, firmware comparison, legal notes, apps: [projects/02-flipper-zero](../../../02-flipper-zero/)
