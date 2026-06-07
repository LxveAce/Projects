# BLE Detection — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/08-ble-detection](../../../08-ble-detection/)
> **Deck role:** Bluetooth tracker / device detection (background sweep)
> **Status:** Ready to build (board in inventory)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Board** | Lonely Binary ESP32 **Gold #3** — *shared with [Chasing Your Tail](../10-chasing-your-tail/)* |
| **Chip** | **Classic ESP32** (WROOM-class, CH340, BLE 4.2 — *not* an S3) |
| **Firmware** | [MatthewKuKanich/ESP32-AirTag-Scanner](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner) (compile for classic ESP32) |
| **Flash tool** | Arduino IDE, board target **"ESP32 Dev Module"** |
| **Antenna** | IPEX → U.FL pigtail → **SMA bulkhead #3** (2.4 GHz) |
| **Power** | Powered USB hub, gated by toggle **SW3** |
| **Display** | None — output goes to the Pi 5 dashboard |

> **Critical — this board is SHARED.** Gold #3 runs BLE device detection **and**
> [Chasing Your Tail](../10-chasing-your-tail/) tail detection. Same chip, same
> antenna, same switch (SW3), same serial link. Read both guides together; flash
> the firmware that covers both before final mounting so you don't pull the board
> twice.

> **Why the Gold board:** it has an IPEX/U.FL connector for a real external antenna. BLE
> shares the 2.4 GHz radio with WiFi, so the same external antenna that helps Marauder also
> extends BLE reception (+~10 dB vs the PCB trace) for spotting low-power trackers across a
> room. (BLE 4.2 on the classic ESP32 is plenty for scanning tracker advertisements.)

---

## What You Need (from the repo inventory)

- Lonely Binary ESP32 Gold #3 — from the [3-pack](../../../../INVENTORY.md) *(shared with Chasing Your Tail)*
- U.FL/IPEX → SMA pigtail (15–20 cm) → SMA bulkhead #3
- 2.4 GHz antenna on bulkhead #3 (Bingfu/DIYmall + RP-SMA→SMA adapter as needed)
- USB-C **data** cable for flashing
- Arduino IDE with ESP32 board support installed

---

## Get It Running

### 1. Flash the firmware

1. Install **Arduino IDE** and the ESP32 board support package
   (Board Manager URL: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`,
   then install "esp32 by Espressif Systems").
2. Clone or download [MatthewKuKanich/ESP32-AirTag-Scanner](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner) and open its sketch.
3. Plug Gold #3 into your PC with a USB-C data cable.
4. **Tools > Board** → select **"ESP32 Dev Module"** (classic ESP32 — *not* the S3 variant).
5. **Tools > Port** → select the COM port.
6. Click **Upload**; if it stalls at connect, hold **BOOT** during connect.

> Building the **shared** Gold #3? Merge in the Chasing Your Tail logic now — see
> [10-chasing-your-tail](../10-chasing-your-tail/) — so one flash covers BLE
> detection and tail detection.

### 2. Wire it into the deck

- **Mount:** Gold #3 on the ESP32 plate via M3 standoffs.
- **Antenna:** snap the U.FL pigtail straight down onto the Gold's IPEX socket (feel the
  click — never twist), route to **SMA bulkhead #3**, screw the 2.4 GHz antenna on outside.
  *U.FL is rated ~30 mating cycles — treat as semi-permanent.*
- **Power:** USB from the powered hub → inline **toggle SW3** → Gold #3.
- **Data:** the same USB run carries serial to the Pi 5 (`/dev/ttyUSBx`, 115200 baud).
- **Display:** none — Gold #3 is headless; all output lands on the Pi 5 dashboard.

### 3. Verify

```bash
screen /dev/ttyUSB0 115200      # detected devices stream as lines
```
Each detected device prints **MAC, RSSI, device name, and manufacturer data**. Walk a
phone or a known AirTag/Tile past the deck and confirm new lines appear. If using the
dashboard, the live BLE device list should populate within a few seconds.

---

## Cyberdeck Compatibility Notes

- **Shared board (the big one):** Gold #3 is **also** the [Chasing Your Tail](../10-chasing-your-tail/)
  board. BLE detection and tail detection run from the **same** chip, antenna (SMA #3),
  switch (SW3), and serial link — they are not two separate radios. Coordinate firmware
  so both functions ship together; flipping SW3 powers/cuts **both**.
- **USB/serial budget:** consumes one powered-hub port; Pi reads it at `/dev/ttyUSBx` (115200 baud).
- **Dashboard:** the Pi 5 [dashboard](../parts/dashboard/) parses the serial stream and shows a
  live list of detected devices — **MAC, RSSI, device name, manufacturer data** — and can flag
  devices that persist across scans (possible trackers).
- **Antenna:** owns bulkhead **#3** only (2.4 GHz) — no conflict with Marauder (#1) or Flock (#2).
- **Power modes:** SW3 fully cuts Gold #3 for the "stealth" / low-draw profiles in the
  [power guide](../parts/power/) — zero RF emission when off (disables BLE + tail detection).

## Standalone Mode

Flip **SW3** on with the Pi off and Gold #3 keeps scanning on its own — it just has no
screen, so to read output you connect a serial monitor (115200 baud) instead of the
dashboard. The board is headless either way; nothing about the deck wiring stops you from
pulling Gold #3 out and running it on a bench.

## Source / Upstream

- Upstream firmware: [MatthewKuKanich/ESP32-AirTag-Scanner](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner)
- Shared-board companion: [Chasing Your Tail (project 10)](../10-chasing-your-tail/)
- Full options, BLE background, tracker/legal notes: [projects/08-ble-detection](../../../08-ble-detection/)
