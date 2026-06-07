# Flock & Drone Detection — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/06-flock-drone-detection](../../../06-flock-drone-detection/)
> **Deck role:** ALPR camera detection (Flock) + drone RemoteID detection — both passive, always listening
> **Status:** Ready to build (boards + display in inventory)

---

This subsystem covers **two detectors on two boards** that share one screen:

- **FLOCK** — detects Flock Safety ALPR cameras by their WiFi emissions, on **Gold #2 (classic ESP32)**.
- **DRONE** — detects FAA RemoteID broadcasts, on a separate **ESP32-WROOM-32**.

Both are receive-only (they never transmit), both feed serial alerts to the Pi 5, and both surface on **CYD #2**.

---

## The Decision

| Question | Flock detector | Drone detector |
|----------|----------------|----------------|
| **Board** | Lonely Binary ESP32 **Gold #2** | **ESP32-WROOM-32** (generic) |
| **Chip** | Classic ESP32 (CH340, *not* S3) | ESP32-WROOM-32 |
| **Detects** | Flock ALPR cameras (31 known OUIs) | FAA RemoteID drones (WiFi + BLE) |
| **Firmware** | Marauder Flock mode `sniffbt -t flock` (confirmed on classic ESP32) — or [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you) if its build targets classic ESP32 | [colonelpanichacks/Sky-Spy](https://github.com/colonelpanichacks) |
| **Antenna** | IPEX → U.FL → **SMA bulkhead #2** ("FLOCK", 2.4 GHz) | Internal PCB antenna (no SMA) |
| **Power** | Hub → toggle **SW2** | Hub → toggle **SW5** |
| **Display** | CYD #2 (shared) | CYD #2 (shared) |
| **Serial** | USB to Pi 5, 115200 baud | USB to Pi 5, 115200 baud |

> **Why a dedicated Gold #2 for Flock when Marauder already has it:** the [Marauder on Gold #1](../01-esp32-marauder/) can run `sniffbt -t flock`, so Flock detection overlaps. The deck keeps Gold #2 dedicated to Flock so it can scan continuously and passively *while* Gold #1 is busy with WiFi/BLE attacks. If you ever drop Gold #2, Marauder covers Flock as a fallback.

> **Why the WROOM-32 has no SMA:** RemoteID broadcasts are strong and the detection range is generous; the WROOM-32's internal PCB antenna is sufficient, so it needs no bulkhead — keeping bulkhead #2 free for Flock alone.

---

## What You Need (from the repo inventory)

- Lonely Binary ESP32 Gold #2 — from the [3-pack](../../../../INVENTORY.md) (Flock)
- ESP32-WROOM-32 generic dev board (Drone)
- CYD 2.8" Touchscreen #2 (ESP32-2432S028R, ILI9341) — shared by both
- U.FL/IPEX → SMA pigtail (15–20 cm) → SMA bulkhead #2 ("FLOCK")
- 2.4 GHz antenna for bulkhead #2 (omni preferred for 360° coverage)
- USB-C / USB **data** cable for flashing each board

---

## Get It Running

### Flock board (Gold #2)

#### 1. Flash the firmware

Gold #2 is a **classic ESP32**, so the confirmed path is the **standard ESP32 (WROOM) Marauder
build**, then turn Flock detection on over serial:

1. Open **Chrome or Edge** and use [ESP Terminator](../13-esp-terminator/) (espterminator.com).
2. Plug Gold #2 in with a USB-C data cable; hold **BOOT**, connect, release.
3. Flash the **standard ESP32 (WROOM)** Marauder target (same as [Gold #1](../01-esp32-marauder/) — *not* MultiBoard S3).
4. Press **RST**, then run Flock detection over serial: `sniffbt -t flock` (and `Flock Wardrive` for GPS-tagged logging).

**Alternative — dedicated flock-you firmware:** [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you)
is a purpose-built Flock scanner, but **confirm its PlatformIO env targets classic ESP32** before
flashing this board (several of its envs are ESP32-S3, which won't run on the Gold):
```bash
git clone https://github.com/colonelpanichacks/flock-you.git
cd flock-you
# select/verify a classic-ESP32 build env, then:
pio run -t upload
```

#### 2. Wire it into the deck

- **Mount:** Gold #2 on the ESP32 plate via M3 standoffs.
- **Antenna:** snap the U.FL pigtail straight down onto the IPEX socket (feel the click — never twist), route to **SMA bulkhead #2** ("FLOCK"), screw the 2.4 GHz antenna on outside. *U.FL is ~30 mating cycles — treat as semi-permanent.*
- **Power:** USB from the powered hub → inline **toggle SW2** → Gold #2.
- **Data:** the same USB run carries serial to the Pi 5 (`/dev/ttyUSBx`, 115200 baud).
- **Display:** shares CYD #2 with the drone detector (see [displays part](../parts/displays/)).

### Drone board (WROOM-32)

#### 1. Flash the firmware

1. Open **Chrome or Edge**, plug the WROOM-32 in over USB.
2. Flash [Sky-Spy](https://github.com/colonelpanichacks) (colonelpanichacks) — its RemoteID scanner captures WiFi beacon/NAN and BLE advertisements that carry RemoteID.
3. Hold **BOOT** during connect if it stalls; drop to `--baud 115200` if needed.
4. Wait for "complete," press **EN/RST**.

#### 2. Wire it into the deck

- **Mount:** WROOM-32 on the ESP32 rail via M3 standoffs.
- **Antenna:** none to wire — it uses the internal PCB antenna.
- **Power:** USB from the powered hub → inline **toggle SW5** → WROOM-32.
- **Data:** USB serial to the Pi 5 (`/dev/ttyUSBx`, 115200 baud).
- **Display:** shares CYD #2 with the Flock detector.

### Verify

```bash
screen /dev/ttyUSB0 115200      # Flock board: should stream detection JSON when a Flock OUI is in range
screen /dev/ttyUSB1 115200      # Drone board: should stream RemoteID events when a compliant drone is up
```
Or power SW2 / SW5 on and watch alerts land on **CYD #2** and in the Pi 5 [dashboard](../parts/dashboard/).

---

## Cyberdeck Compatibility Notes

- **USB/serial budget:** consumes two powered-hub ports (SW2 + SW5); Pi reads each at its own `/dev/ttyUSBx`.
- **Dashboard:** the Pi 5 [dashboard](../parts/dashboard/) parses both serial streams. Flock alerts show camera MAC / OUI / RSSI; drone alerts show RemoteID with drone + pilot position. The Pi maps detections to GPS from the shared `gpsd` feed.
- **Shared display:** CYD #2 is shared by both detectors — the dashboard multiplexes Flock and drone alerts onto the one screen.
- **Overlap with Marauder:** [Gold #1 / Marauder](../01-esp32-marauder/) can also do Flock via `sniffbt -t flock`. Gold #2 stays dedicated to Flock for flexibility; Marauder is the fallback if Gold #2 is removed.
- **Antenna:** Flock owns bulkhead **#2** only. Drone uses no bulkhead. No RF conflict with the other radios.
- **Power modes:** SW2 and SW5 independently cut each detector for the low-draw profiles in the [power guide](../parts/power/) — zero RF emission when off (both are receive-only regardless).

## Standalone Mode

Flip **SW2** (and/or **SW5**) on with the Pi off and each board runs on its own — flock-you logs detections to onboard SPIFFS and beeps/flashes on each hit; Sky-Spy keeps scanning RemoteID. Pull either board out and it works on a bench unchanged; it's the same board either way.

## Source / Upstream

- Flock firmware: [colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you)
- Drone firmware: [colonelpanichacks/Sky-Spy](https://github.com/colonelpanichacks)
- Full options, detection methods, legal notes: [projects/06-flock-drone-detection](../../../06-flock-drone-detection/)
