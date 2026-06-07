# Chasing Your Tail (NG) — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/10-chasing-your-tail](../../../10-chasing-your-tail/)
> **Deck role:** Tail detection — flags AirTag/Tile/SmartTag/devices that follow you over time
> **Status:** Ready to build (shares Gold #3 + GPS, both in inventory)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Software** | [ArgeliusLabs/Chasing-Your-Tail-NG](https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG) (CYT-NG, MIT) |
| **Where it runs** | Pi 5 brain — correlation logic only, **no dedicated board** |
| **BLE source** | Lonely Binary **Gold #3** — the *same* board as [BLE Detection](../08-ble-detection/) |
| **GPS source** | VK-162 USB GPS, shared via `gpsd` ([gps part](../parts/gps/)) |
| **Antenna** | Shares **SMA bulkhead #3** with BLE Detection — no new antenna |
| **Power** | Gold #3 gated by toggle **SW3** (shared); Pi 5 always on |
| **Display** | Cyberdeck [dashboard](../parts/dashboard/) on the 7" DSI — no own screen |

> **Why no separate board:** CYT-NG's job is *correlation* — "have I seen this BLE/Wi-Fi
> signature before, somewhere else, a while ago?" It doesn't need its own radio. It rides on
> the BLE stream **Gold #3 already produces** for [BLE Detection](../08-ble-detection/), adds
> GPS from `gpsd`, and runs the temporal-persistence scoring on the Pi 5. One board, two tools.

> **This guide does NOT cover flashing Gold #3.** The board flash, antenna, and SW3/SMA #3
> wiring all live in the [BLE Detection guide](../08-ble-detection/). Do that first, then come
> back here for the Pi-side setup.

---

## What You Need (from the repo inventory)

- **Gold #3 already flashed and wired** per the [BLE Detection guide](../08-ble-detection/) — this is the prerequisite
- Pi 5 8GB brain (already the deck's brain — [pi5-brain part](../parts/pi5-brain/))
- VK-162 USB GPS on **SW7**, served over `gpsd` — see [gps part](../parts/gps/)
- 7" DSI display for the [dashboard](../parts/dashboard/) (already in the deck)
- No new board, no new antenna, no new SMA bulkhead — see [INVENTORY.md](../../../../INVENTORY.md)

---

## Get It Running

### 1. Flash & wire Gold #3 — see the BLE guide

Follow **[08 — BLE Detection](../08-ble-detection/)** end to end: flash Gold #3, snap on its
U.FL pigtail to **SMA bulkhead #3**, mount it, and gate power through **SW3**. When the BLE
side is scanning and reaching the Pi over serial, the radio half of Chasing Your Tail is done.
Everything below runs on the **Pi 5**.

### 2. Install CYT-NG on the Pi 5

```bash
git clone https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG.git
cd Chasing-Your-Tail-NG
pip3 install -r requirements.txt
```

Run the security migration **first** (sets up encrypted credential storage):

```bash
python3 migrate_credentials.py
```

### 3. Wire in the GPS dependency

CYT-NG correlates *device sightings across locations*, so GPS is not optional on the deck —
it's what turns "seen twice" into "followed me across town."

1. Confirm the VK-162 is up on **SW7** and `gpsd` is serving it (per the [gps part](../parts/gps/)):

```bash
cgps          # should show a live fix (lat/lon, sats)
```

2. Point CYT-NG at the deck's data sources by editing `config.json`:

- **BLE/Kismet DB path** → the SQLite the deck's BLE capture writes (Gold #3's stream feeds Kismet on the Pi)
- **GPS** → leave on auto-extract so it pulls coordinates from the live `gpsd`/Kismet feed
- Time windows: keep defaults (5 / 10 / 15 / 20 min sliding windows)
- WiGLE API key — optional, for SSID geolocation only

### 4. Verify

```bash
# baseline your own + nearby stationary devices into the ignore list first
python3 cyt_gui.py        # use "Create ignore list" — sit still 2-3 min

# then, while moving, run the correlation
python3 surveillance_analyzer.py
```

A device that shows a high **persistence score** (0.6–1.0) across multiple time windows
*and* multiple GPS points is the deck telling you something is tailing you. Quick smoke test
with no movement needed:

```bash
python3 surveillance_analyzer.py --demo   # canned Phoenix coords, proves the pipeline runs
```

---

## Cyberdeck Compatibility Notes

- **No radio of its own:** CYT-NG is pure Pi-side software. It consumes Gold #3's BLE stream
  (the same data [BLE Detection](../08-ble-detection/) uses) plus `gpsd` — zero extra RF, zero
  extra USB ports, zero new antenna.
- **Shared with BLE Detection:** Gold #3 / **SW3** / **SMA #3** are owned by the
  [BLE guide](../08-ble-detection/). Flip SW3 off and *both* tools go dark together — they are
  one board. There is no independent power switch for Chasing Your Tail.
- **GPS is the hard dependency:** without a `gpsd` fix you get device persistence but no
  location correlation, which is the whole point. Keep **SW7** (GPS) on when using CYT.
- **Dashboard:** persistence alerts surface on the Pi 5 [dashboard](../parts/dashboard/)
  alongside BLE counts; KML output can be opened later in Google Earth for the route map.
- **It does not ID trackers by protocol:** like upstream, it flags *any* BLE/Wi-Fi device that
  persistently follows you — it does not decode Apple FindMy / SmartTag / Tile specifically.
  For protocol-level AirTag ID, pair with AirGuard on a phone (see source guide).

## Standalone Mode

Out of the deck, CYT-NG is just the upstream project: a Raspberry Pi running Kismet + a
monitor-mode Wi-Fi adapter + a USB GPS, with the Python correlation engine on top. The deck
simply pre-supplies all three — Gold #3's BLE feed, the Pi 5, and the shared VK-162 GPS — so
nothing is soldered in or deck-specific. Pull the Pi (or just the repo + a GPS dongle) and it
runs anywhere. See the [full source guide](../../../10-chasing-your-tail/) for the from-scratch
standalone build (Kismet install, Wi-Fi adapter monitor mode, GUI usage).

## Source / Upstream

- Upstream software: [ArgeliusLabs/Chasing-Your-Tail-NG](https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG) (Matt Edmondson, MIT)
- Full write-up, usage, limitations, alternatives: [projects/10-chasing-your-tail](../../../10-chasing-your-tail/)
- Shared board flash + antenna/power: [BLE Detection integration](../08-ble-detection/)
