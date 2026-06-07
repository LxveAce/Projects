# Displays — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Source (full strategy):** deck README [Section 7 — Display Strategy](../../../README.md)
> **Deck role:** All visual output — one primary touchscreen + four dedicated status screens
> **Status:** Ready to build (all 5 displays in inventory)

---

## The Decision

Five displays, each tied to the subsystem it serves. Nothing shares a screen by accident —
every interactive board has its own output.

| Display | Size / Type | Role | Connection |
|---------|-------------|------|------------|
| **Hosyond 7" DSI** | 7.0" 800×480 touch | Primary dashboard, Kismet web UI, full Kali desktop | Pi 5 **DSI port** (in the lid) |
| **CYD 2.8" #1** | 2.8" ILI9341 touch | Standalone Marauder (touch GUI) | Its *own* onboard ESP32 (USB power) |
| **CYD 2.8" #2** | 2.8" ILI9341 touch | Flock / Drone alert screen | Its *own* onboard ESP32 (USB power) |
| **SSD1309 OLED** | 2.42" 128×64, I2C | System vitals (battery, temp, GPS, tool status) | Pi 5 **GPIO I2C1** (SDA/SCL) |
| **Heltec built-in OLED** | 0.96" | Meshtastic status | **Onboard** Heltec LoRa V3 (no wiring) |

> **Why the 7" goes in the lid:** mounted in the Pelican 1300 lid, it hinges open like a
> laptop screen. The Pi 5 drives it over DSI (not HDMI), freeing the HDMI ports and keeping
> the cable run short and clean through the hinge.

> **Critical — Pi 5 DSI is 22-pin:** the Hosyond's stock ribbon is the older 15-pin Pi
> connector. You **must** use a **22-pin → 15-pin DSI adapter cable** (Pi 5 side) plus a
> **30cm 15-pin FPC extension** to reach through the hinge. Without the adapter the display
> will not link up on a Pi 5.

---

## What You Need (from the repo inventory)

- Hosyond 7" DSI Touchscreen, 800×480 — [INVENTORY.md](../../../../../INVENTORY.md)
- Pi 5 DSI Cable, **22-pin → 15-pin** adapter (~$8)
- DSI **FPC Extension Cable, 30cm** (15-pin, 1mm pitch) — routes through the hinge (~$5–8)
- CYD 2.8" Touchscreen #1 (ESP32-2432S028R, ILI9341) — Marauder GUI
- CYD 2.8" Touchscreen #2 (ESP32-2432S028R, ILI9341) — Flock/Drone alerts
- 2.42" SSD1309 OLED, 128×64, **I2C** (4-pin: VCC/GND/SDA/SCL)
- Heltec LoRa V3 — 0.96" OLED is built onto the board (nothing to buy)
- Aluminum **L-brackets** (~$3–5/pack) + **M3 standoffs/bolts** for the lid mount
- Kapton tape for securing the DSI ribbon through the hinge

The two CYDs are flashed/configured as part of their own subsystem guides — see the
[Marauder guide](../../01-esp32-marauder/) (CYD #1) and the
[Flock/Drone guide](../../06-flock-drone-detection/) (CYD #2).

---

## Get It Running

### 1. Mount and route the 7" DSI (in the lid)

1. Position the display **centered in the Pelican 1300 lid**.
2. Mark the 4 mounting holes through the display's mounting tabs.
3. Drill **pilot holes only** — do **not** drill through the lid. Use short standoffs +
   adhesive backing to keep the IP67 seal intact.
4. Attach **aluminum L-brackets** to the lid with **M3 bolts**; screw the display to the brackets.
5. Plug the **22→15 pin DSI adapter** into the Pi 5 DSI connector, chain the **30cm FPC
   extension**, then route the ribbon **through the hinge gap** to the lid. Secure with Kapton tape.
6. Power and touch are carried per the [pi5-brain](../pi5-brain/) GPIO map (5V on pin 2/4, GND on pin 6).

### 2. CYD #1 and CYD #2 (standalone boards, base-mounted)

- **Each CYD is a complete ESP32 board with its own screen** — *not* a dumb display wired to a
  Gold board. It runs its own firmware off its own USB power. (You already flash these as their
  own devices — that's why the CYD ships with an ESP32 onboard.)
- Mount both CYDs **face-up in the base**, visible when the lid is open.
- **CYD #1** runs **Marauder standalone** — power it over USB and it boots into the touch GUI
  (scan/attack/sniff modes, live AP/station lists). Nothing connects it to Gold #1.
- **CYD #2** runs its own **Flock/Drone alert firmware** (e.g. Marauder with `sniffbt -t flock`,
  or a custom alert sketch). If you want it to *mirror* Gold #2's output rather than sniff on its
  own, run a UART wire between the two boards — otherwise let CYD #2 detect by itself.
- No flashing here: each CYD is set up in its parent subsystem guide (linked above).

### 3. Wire the 2.42" OLED (I2C to the Pi 5)

The SSD1309 is a 4-wire I2C device on the Pi 5's **I2C1** bus (matches the
[pi5-brain](../pi5-brain/) GPIO map):

| OLED pin | Pi 5 phys pin | BCM |
|----------|---------------|-----|
| VCC | Pin 1 (3.3V) | — |
| GND | Pin 14 (GND) | — |
| SDA | Pin 3 | **GPIO2 (I2C1 SDA)** |
| SCL | Pin 5 | **GPIO3 (I2C1 SCL)** |

Mount it on the edge of the compute plate, **angled for visibility** when the lid is open.
It shows battery %, active tools (Kismet/Marauder/Flock/BLE/Mesh), monitor-mode status,
GPS lock + satellite count, last Meshtastic message, and Pi 5 CPU temp / throttle warning.

### 4. Verify each lights up

```bash
# 7" DSI — should show the Kali desktop on boot. If blank, recheck the 22→15 adapter.
# OLED — confirm it's on the I2C bus (expect address 0x3C or 0x3D):
sudo apt install -y i2c-tools
i2cdetect -y 1
```
- **CYD #1:** power it over USB — it boots into the Marauder touch GUI on its own.
- **CYD #2:** power it over USB — it boots into its Flock/Drone alert screen on its own.
- **Heltec OLED:** powers up with the board (SW4) and shows Meshtastic status — no wiring.

---

## Cyberdeck Compatibility Notes

- **7" DSI is the only Pi-driven graphical screen** — it runs the
  [dashboard](../dashboard/) (Flask + SocketIO in Chromium kiosk) that aggregates Kismet,
  Marauder serial, Flock/BLE/drone alerts, Meshtastic, and system stats.
- **GPIO budget:** the OLED uses **I2C1 (GPIO2/GPIO3) only**. The DSI touchscreen runs its
  touch over a **separate I2C bus inside the DSI connector** — no clash with the OLED. See
  the [pi5-brain](../pi5-brain/) guide for the full pin map.
- **Which subsystem each screen belongs to:** CYD #1 = the standalone
  [Marauder](../../01-esp32-marauder/) touchscreen; CYD #2 = the
  [Flock & Drone](../../06-flock-drone-detection/) alert screen; 7" DSI + 2.42" OLED ← the
  [Pi 5](../pi5-brain/); 0.96" OLED ← Heltec LoRa V3 itself.
- **USB cost:** each CYD is its own ESP32 board, so it needs its **own powered-hub port** for
  power — it is not free-riding on a Gold board's link. The OLED is GPIO and the 7" is DSI.
- **Power gating:** give each CYD its own inline toggle on its hub port (the OLED/7" live on the
  always-on Pi 5; the Heltec OLED follows SW4 with its board).

## Standalone Mode

Each CYD is a self-contained ESP32 + screen, so it works with the Pi off (and without any Gold
board). Power CYD #1 and it runs the full Marauder touch GUI on its own; power CYD #2 and it
runs the Flock/Drone alert screen on its own. The Heltec's 0.96" OLED shows Meshtastic status
standalone the same way. Only the 7" DSI and the 2.42" OLED require the Pi 5 — they're the
brain's screens (and the 7" is where a *headless* Gold board's output actually shows up, via the
[dashboard](../dashboard/)).

## Source / Upstream

- Deck display strategy (the 5-display plan, roles, connections): deck README
  [Section 7](../../../README.md)
- Lid mounting (L-brackets + M3, hinge routing): deck README Section 10, "Display in the Lid"
- GPIO / OLED I2C pinout: deck README Section 11
- Exact parts and links: [INVENTORY.md](../../../../../INVENTORY.md)
