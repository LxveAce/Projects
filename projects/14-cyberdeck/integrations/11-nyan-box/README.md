# NyanBOX — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all tools):** [projects/11-nyan-box](../../../11-nyan-box/)
> **Deck role:** Pre-built portable 2.4 GHz pentest toolkit — handheld companion
> **Status:** In Transit (ordered, awaiting delivery)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Device** | NyanBOX Complete Kit (jbohack/zr_crackiin) — pre-built, fully assembled |
| **Chip** | Its **own** ESP32-WROOM-32U (240 MHz) — *not* a board from the deck inventory |
| **Firmware** | Stock nyanBOX (ships pre-flashed); flash latest via web flasher on arrival |
| **Flash tool** | [nyandevices.com/flasher](https://nyandevices.com/flasher/) (Web Serial) |
| **Display** | Its **own** 0.96" OLED — standalone menu UI, no deck display assigned |
| **Antenna** | Its **own** 4× 2.4 GHz antennas — no deck SMA bulkhead assigned |
| **Power** | Onboard 2500 mAh LiPo; tops off from a deck USB port in the foam bay |
| **Deck mount** | Foam bay (grab-and-go) — **not** bolted into the chassis |

> **Why companion, not bolted in:** NyanBOX is a self-contained unit with its own ESP32,
> OLED, battery, and antennas. It is a handheld grab-and-go tool, so it **rides in a foam
> bay** and pulls out to use in-hand. It does **not** feed the Pi 5 and claims **no** deck
> board, SMA bulkhead, display, or toggle switch.

> **No inventory board needed:** unlike the Marauder/Flock/BLE Gold boards, NyanBOX brings
> its own everything. Nothing from the deck's ESP32 pool is allocated to it.

---

## What You Need (from the repo inventory)

- NyanBOX Complete Kit — fully assembled device + carrying case (In Transit)
- The kit's own 4× 2.4 GHz antennas (included in box)
- The kit's own USB-C cable (included)
- A Chromium browser (Chrome/Edge/Brave/Opera) for flashing — Firefox/Safari won't work
- CP210x USB-to-UART drivers on Windows ([silabs.com](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers))
- A free deck USB port for charging in the bay (see [power guide](../parts/power/))
- KOOTION 16 GB micro SD — optional, only if a firmware needs one ([INVENTORY](../../../../INVENTORY.md))

---

## Get It Running

### 1. Flash / Set up (on arrival)

1. Unbox, attach all **4 antennas** to the SMA connectors, charge via USB-C.
2. Flip the power switch ON — the OLED should show the nyanBOX boot screen.
3. (Windows) Install the **CP210x USB-to-UART** drivers from Silicon Labs, then reboot.
4. Turn the battery switch **OFF**, connect via USB-C, open **Chrome/Edge/Brave**.
5. Go to [nyandevices.com/flasher](https://nyandevices.com/flasher/) → **Install nyanBOX Firmware** → pick the COM port → wait for complete.
   - *Stuck?* Hold the **BOOT** button (top-right) when prompted; install CP210x if the port is missing.
6. First use: arrow buttons scroll menus, select/enter chooses a tool, back returns. Try **WiFi Scanner**, **BLE Scanner**, and **Spectrum Analyzer** to confirm it works.

> *Optional:* the community **nyanBEE** firmware (ck42x.com/nyanbee) roughly 2.5×'s the tool
> count and flashes the same way. You can switch back and forth freely. See the
> [full reference](../../../11-nyan-box/) for the trade-offs.

> *No deck flasher needed:* NyanBOX uses its own vendor flasher, not the deck's
> [ESP Terminator](../13-esp-terminator/) flow used for the Gold/WROOM boards.

### 2. Ride with the deck

- **Stowage:** NyanBOX lives in a **foam bay** cut into the deck — slide it in, no fasteners.
- **Charging:** plug its USB-C into a free deck USB port; the onboard 2500 mAh LiPo tops off in the bay. Power switch OFF while it charges idle.
- **No chassis wiring:** it does **not** connect to the Pi serial, does **not** share an SMA bulkhead, and does **not** use a toggle switch (SW1–SW7) — those stay free for the bolted-in boards.
- **Grab-and-go:** pull it out of the bay to use handheld; drop it back to recharge.

### 3. Verify

- In the bay: confirm the deck USB port is charging it (the LiPo indicator climbs with the power switch OFF).
- In-hand: flip the power switch ON, run **WiFi Scanner** — your own AP should appear; run **BLE Scanner** — nearby devices should list.
- Nothing on the deck (Pi, dashboard, other radios) should change state when NyanBOX is removed or reinserted — it is fully independent.

---

## Cyberdeck Compatibility Notes

- **USB/serial budget:** consumes **zero** Pi serial ports — it does not feed the Pi. It only borrows a deck USB port for *charging*, drawing nothing from the serial plumbing.
- **No bulkhead conflict:** uses its own 4 antennas; claims **no** SMA bulkhead (#1–#5 all stay assigned to the bolted-in radios).
- **No switch conflict:** not on the [power guide's](../parts/power/) toggle map (SW1–SW7) — it has its own power switch and battery.
- **Tool overlap with bolted-in radios:** NyanBOX duplicates a lot of the deck's 2.4 GHz coverage on purpose — it carries its own WiFi deauth/Evil Portal (vs [Marauder on Gold #1](../01-esp32-marauder/)), Flock + Drone RemoteID detection (vs [Flock on Gold #2](../06-flock-drone-detection/)), and AirTag/SmartTag/Tile + Flipper detection (vs [BLE/Chasing-Your-Tail on Gold #3](../08-ble-detection/)). That overlap is the point: it's the handheld backup that works when the deck is closed.
- **Battery:** all-day runtime off its LiPo; the deck USB is for top-ups, not a hard dependency.

## Standalone Mode

NyanBOX **is** standalone by default — it is a companion device, not a deck subsystem. Lift
it out of the foam bay and it runs entirely on its own ESP32, OLED, antennas, and battery
with full menu-driven access to every tool. The deck adds nothing but a charging port and a
place to stash it; remove it and the deck is unaffected, and remove the deck and NyanBOX is
unaffected.

## Source / Upstream

- Upstream firmware / source: [github.com/jbohack/nyanBOX](https://github.com/jbohack/nyanBOX)
- Official site / web flasher: [nyandevices.com](https://nyandevices.com/) · [nyandevices.com/flasher](https://nyandevices.com/flasher/)
- Full tool list, usage, nyanBEE option, legal notes: [projects/11-nyan-box](../../../11-nyan-box/)
