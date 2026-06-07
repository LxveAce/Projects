# ESP32 Marauder — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/01-esp32-marauder](../../../01-esp32-marauder/)
> **Deck role:** Primary WiFi/BLE offensive tool
> **Status:** Ready to build (boards + display in inventory)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Board** | Lonely Binary ESP32 **Gold #1** |
| **Chip** | **ESP32-S3** (N16R8: 16 MB flash, 8 MB PSRAM) — *not* WROOM-32 |
| **Firmware** | ESP32 Marauder, the `_multiboardS3.bin` variant |
| **Flash tool** | [ESP Terminator](https://espterminator.com/) web flasher |
| **Display** | CYD 2.8" #1, as the standalone touch GUI |
| **Antenna** | IPEX → U.FL pigtail → **SMA bulkhead #1** ("MAR") → Bingfu 2.4/5.8 GHz |
| **Power** | Powered USB hub, gated by toggle **SW1** |

> **Why the Gold board over the CYD-as-brain:** the Gold has an IPEX/U.FL connector for a
> real external antenna (the CYD would need a soldered antenna mod). The CYD rides along as
> a screen only. One board, best range, no soldering.

> **Critical:** the Lonely Binary Gold is an **ESP32-S3**, so you must use the
> `_multiboardS3.bin` firmware. The generic "ESP32-WROOM" Marauder build will *not* boot
> correctly on it.

---

## What You Need (from the repo inventory)

- Lonely Binary ESP32 Gold #1 — from the [3-pack](../../../../INVENTORY.md)
- CYD 2.8" Touchscreen #1 (ESP32-2432S028R, ILI9341)
- U.FL/IPEX → SMA pigtail (15–20 cm) → SMA bulkhead #1
- Bingfu 2.4/5.8 GHz antenna (+ Boobrie RP-SMA→SMA adapter)
- 128 GB micro SD (optional — PCAP capture, Evil Portal HTML)
- USB-C **data** cable for flashing

---

## Get It Running

### 1. Flash the firmware

1. Open **Chrome or Edge** (WebSerial required — Firefox/Safari won't work).
2. Go to [espterminator.com](https://espterminator.com/).
3. Plug Gold #1 into your PC with a USB-C data cable.
4. Hold **BOOT**, click **Connect**, pick the COM port, release BOOT.
5. Select **ESP32 Marauder** → the **MultiBoard S3 / `_multiboardS3.bin`** target.
6. Click **Install** / **Flash** and wait for "complete," then press **RST**.

CLI alternative (same result):
```bash
pip install esptool
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x0 bootloader.bin \
  0x8000 esp32_marauder.ino.partitions.bin \
  0xe000 boot_app0.bin \
  0x10000 esp32_marauder_v1.12.1_multiboardS3.bin
```
(If it stalls at connect, hold BOOT during connect and drop to `--baud 115200`.)

### 2. Wire it into the deck

- **Mount:** Gold #1 on the ESP32 plate via M3 standoffs.
- **Antenna:** snap the U.FL pigtail straight down onto the Gold's IPEX socket (feel the
  click — never twist), route to **SMA bulkhead #1**, screw the antenna on outside.
  *U.FL is rated ~30 mating cycles — treat as semi-permanent.*
- **Display:** CYD #1 plugs into Gold #1 over serial; mount it face-up in the base.
- **Power:** USB from the powered hub → inline **toggle SW1** → Gold #1.
- **Data:** the same USB run carries serial to the Pi 5 (`/dev/ttyUSBx`, 115200 baud).
- **SD (optional):** FAT32, ≤32 GB, SanDisk recommended — enables `SavePCAP`.

### 3. Verify

```bash
screen /dev/ttyUSB0 115200      # then type:
scanap                          # should list nearby APs
stopscan
```
Or just power SW1 on with no Pi — the CYD should boot straight into the Marauder GUI.

---

## Cyberdeck Compatibility Notes

- **USB/serial budget:** consumes one powered-hub port; Pi reads it at `/dev/ttyUSBx`.
- **Dashboard:** the Pi 5 [dashboard](../parts/dashboard/) parses Marauder serial output and
  shows AP/station counts live. Command set: `scanap`, `scansta`, `attack -t deauth`,
  `sniffbt -t flock`, `stopscan`.
- **Overlap with Flock:** Marauder has a built-in `sniffbt -t flock`, so Gold #1 *can* do
  Flock detection too. The deck keeps [Flock on Gold #2](../06-flock-drone-detection/) for
  flexibility — but if you ever drop Gold #2, Marauder covers it.
- **Antenna:** owns bulkhead **#1** only — no conflict with the other radios.
- **Power modes:** SW1 fully cuts Marauder power for the "stealth" / low-draw profiles in the
  [power guide](../parts/power/) — zero RF emission when off.

## Standalone Mode

Flip **SW1** on with the Pi off and Marauder runs entirely on Gold #1 + CYD #1 — full touch
GUI, scans, attacks, PCAP to SD. Nothing about the deck wiring prevents pulling Gold #1 out
and running it on a bench; it's the same board either way.

## Source / Upstream

- Upstream firmware: [justcallmekoko/ESP32Marauder](https://github.com/justcallmekoko/ESP32Marauder)
- Full options, attack usage, legal notes: [projects/01-esp32-marauder](../../../01-esp32-marauder/)
