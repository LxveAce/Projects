# VK-162 USB GPS — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Full reference (wardriving GPS options):** [projects/07-kismet-wardriving](../../07-kismet-wardriving/)
> **Deck role:** One shared GPS feed for every tool, via a single `gpsd` daemon
> **Status:** Still need (~$15)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Module** | **VK-162 USB GPS** (u-blox 7, G-Mouse puck) |
| **Why** | Native `cdc_acm` Linux driver — appears as `/dev/ttyACM0`, no config needed |
| **Connection** | Pi 5 **USB 2.0** port (via hub or direct) |
| **Power** | Gated by toggle **SW7** ("GPS") |
| **Daemon** | **one** `gpsd` on the Pi 5, serving `localhost:2947` |
| **Consumers** | Kismet, Meshtastic, the dashboard, and Flock/BLE timestamping — all read the same socket |

> **Why one shared daemon:** the deck has four things that want location (Kismet, Meshtastic,
> the dashboard, Flock/BLE logging). Instead of each fighting over the serial device, **only
> `gpsd` opens `/dev/ttyACM0`** and every tool connects to it over `localhost:2947`. One GPS,
> one driver, four readers — no contention.

---

## What You Need (from the repo inventory)

- VK-162 USB GPS Module — ~$15, still to order ([INVENTORY.md](../../../../../INVENTORY.md))
- One free Pi 5 **USB 2.0** port (USB 2.0 #1 in the [wiring map](../../../README.md))
- Toggle **SW7** inline on the USB power run
- Clear sky view at the mount point (dashboard/roof, not buried inside the case)

---

## Get It Running

### 1. Install gpsd

```bash
sudo apt install gpsd gpsd-clients
sudo systemctl enable gpsd
```

### 2. Plug in and find the device

Connect the VK-162 to a Pi 5 USB 2.0 port (SW7 on). The u-blox 7 enumerates with the kernel
`cdc_acm` driver — confirm it shows up:

```bash
ls /dev/ttyACM*      # expect /dev/ttyACM0
```

### 3. Configure gpsd

Edit `/etc/default/gpsd`:

```
DEVICES="/dev/ttyACM0"
GPSD_OPTIONS="-n"
```

(`-n` tells `gpsd` to poll the GPS even before a client connects, so a fix is ready at boot.)
Then restart it:

```bash
sudo systemctl restart gpsd
```

### 4. Point each tool at it

Every consumer reads `gpsd` at **`localhost:2947`** — nothing else touches the serial device:

- **Kismet:** add `gps=gpsd:host=localhost,port=2947` to `kismet.conf`.
- **Meshtastic:** position sharing via the `meshtastic-python` API.
- **Dashboard:** the `gpsd` Python client (`gps3`) for live coordinates.
- **Flock / BLE:** GPS timestamps pulled from the dashboard backend.

### 5. Verify lock

```bash
cgps          # live fix table — wait for "3D FIX"
# or:
gpsmon        # raw satellite / NMEA monitor
```

> **First lock is slow.** A cold start needs to download almanac data — **20+ minutes outdoors**
> the first time, then 1–3 minutes on later cold starts. Get it under open sky for the first fix.

---

## Cyberdeck Compatibility Notes

- **One GPS, shared by all:** the daemon is the only thing holding `/dev/ttyACM0`. Kismet,
  Meshtastic, the [dashboard](../dashboard/), and Flock/BLE all read `localhost:2947` — no
  device contention, one fix shared everywhere.
- **Kismet:** the [wardriving guide](../../07-kismet-wardriving/) uses the same `gpsd` line; in
  wardrive mode Kismet only logs once it has a lock, so SW7 must be on first.
- **Meshtastic:** the [mesh node](../../04-meshtastic/) gets position from this feed via
  `meshtastic-python` rather than a second on-board GPS.
- **Dashboard:** shows the live `GPS: lat, lon` + satellite/lock status tile from the `gpsd`
  Python client.
- **USB/power budget:** consumes one Pi 5 USB 2.0 port; **SW7** fully cuts GPS power for the
  low-draw profiles (e.g. it's off in "Stealth / passive" and only on for Wardriving / Full scan).
- **No antenna bulkhead:** the VK-162 has an internal patch antenna — it owns no SMA, so no
  conflict with the five RF bulkheads.

## Standalone Mode

The VK-162 is just a plain USB GPS. Plug it into **any** Linux box, `apt install gpsd
gpsd-clients`, point `/etc/default/gpsd` at `/dev/ttyACM0`, and it serves NMEA fixes on
`localhost:2947` for anything that speaks `gpsd` — Kismet, GPSD-aware loggers, `cgps`,
QGIS, etc. Nothing about the deck wiring is required; pull it out and it works on a laptop.

## Source / Upstream

- GPS module choices, fix-time notes, chipsets: [projects/07-kismet-wardriving](../../07-kismet-wardriving/)
- `gpsd` project: [gpsd.gitlab.io/gpsd](https://gpsd.gitlab.io/gpsd/)
- Full deck GPS integration spec: [Project 14 README, §11](../../../README.md)
