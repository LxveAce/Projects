# Kismet Wardriving — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/07-kismet-wardriving](../../../07-kismet-wardriving/)
> **Deck role:** WiFi mapping / wardriving — passive recon, runs natively on the Pi 5
> **Status:** Ready to build (need GPS module)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Where it runs** | **Natively on the Pi 5** (Kali Linux) — no separate board |
| **Primary WiFi** | **Panda PAU0F** WiFi 6E (AXE3000, MT7921A) — monitor mode, 2.4/5/6 GHz |
| **Primary WiFi link** | **Pi 5 USB 3.0 port, direct** (needs full bandwidth, always on, no toggle) |
| **Secondary WiFi** | **RT5370** dongle — dedicated 2.4 GHz monitor, via hub → toggle **SW6** |
| **GPS** | Shared **VK-162** via `gpsd` (`gps=gpsd:host=localhost,port=2947`) |
| **Antenna** | Panda built-in → **SMA bulkhead #5** |
| **Control / aggregation** | Kismet **REST API** at `http://localhost:2501` → dashboard |

> **Why it runs on the Pi, not an ESP32:** Kismet is a full Linux capture stack — it needs
> real monitor-mode adapters and CPU for packet processing, database writes, and the web UI
> at once. The Pi 5 (Cortex-A76, 8 GB) handles all three simultaneously while feeding the deck.

> **Why the Panda goes direct to USB 3.0:** WiFi 6E capture across three bands saturates a hub
> port. The Panda gets a dedicated Pi 5 USB 3.0 line, **always on (no switch)** — only the
> RT5370 rides the powered hub behind a toggle.

---

## What You Need (from the repo inventory)

- Raspberry Pi 5 8GB — the deck [brain](../parts/pi5-brain/) (Kali, already flashed)
- **Panda PAU0F** AXE3000 WiFi 6E USB 3.0 adapter (primary monitor)
- **RT5370** USB WiFi dongle (secondary 2.4 GHz monitor)
- **VK-162** USB GPS — shared via the [GPS part guide](../parts/gps/) *(missing — to buy)*
- SMA extension → **SMA bulkhead #5** for the Panda antenna (see [antennas](../parts/antennas/))
- 128 GB micro SD (OS + `.kismet` DBs + WiGLE CSV export)
- See [INVENTORY.md](../../../../INVENTORY.md) for exact part lines

---

## Get It Running

### 1. Install & configure (on Kali)

```bash
sudo apt update && sudo apt install kismet gpsd gpsd-clients
sudo usermod -aG kismet $USER
sudo reboot          # group membership takes effect
```

Point `gpsd` at the VK-162 (full steps in the [GPS part guide](../parts/gps/)):

```bash
sudo nano /etc/default/gpsd
# DEVICES="/dev/ttyACM0"
# GPSD_OPTIONS="-n"
# USBAUTO="true"
sudo systemctl restart gpsd
```

Edit `/etc/kismet/kismet_site.conf` (survives package updates) for the deck's two adapters
plus the shared GPS:

```
source=wlan1:name=PandaWiFi6E
source=wlan2:name=RT5370_24GHz,band5ghz=false,band6ghz=false
gps=gpsd:host=localhost,port=2947
```

For 6 GHz on the Panda, set the regulatory domain first: `sudo iw reg set US`.

### 2. Wire it into the deck

- **Primary WiFi:** Panda PAU0F → **Pi 5 USB 3.0 port, direct** — *not* through the hub,
  *not* on a toggle. Always powered (full bandwidth for tri-band capture).
- **Secondary WiFi:** RT5370 → powered USB hub → inline **toggle SW6**.
- **Antenna:** Panda antenna → SMA extension → **SMA bulkhead #5**, antenna screwed on outside.
- **GPS:** VK-162 → Pi 5 USB (shared via `gpsd` — same feed Flock and Meshtastic read).
- **Display:** the 7" DSI shows the Kismet web UI / dashboard; no dedicated screen of its own.

### 3. Verify

```bash
cgps -s                          # wait for "3D Fix" (first lock can take 20+ min outdoors)
ip link show                     # confirm wlan1 (Panda) and wlan2 (RT5370) present
sudo kismet -t deck_$(date +%Y%m%d) --override wardrive -q -s
```

Then browse to `http://localhost:2501` (create the admin login on first use) — you should
see both data sources up, a live AP count, and GPS coordinates populating.

---

## Cyberdeck Compatibility Notes

- **USB budget:** Panda owns a **Pi 5 USB 3.0 port directly** (no hub, no switch); RT5370 takes
  one powered-hub port behind **SW6**; VK-162 shares GPS over `gpsd`.
- **Antenna:** owns bulkhead **#5** only — no conflict with the ESP32 radios (#1–#4).
- **GPS sharing:** the VK-162 feeds `gpsd`, so Kismet, [Flock](../06-flock-drone-detection/),
  and [Meshtastic](../04-meshtastic/) all read one GPS — see the [GPS part guide](../parts/gps/).
- **Dashboard:** Kismet's [REST API](http://localhost:2501) (kismet-rest Python client) feeds the
  deck [dashboard](../parts/dashboard/) — live AP count, new-network alerts, channel activity,
  GPS-tagged locations, station associations.
- **Power modes:** the Panda is **always on** (no toggle), so Kismet's primary radio stays live
  whenever the Pi is powered; only the secondary RT5370 can be cut via SW6 for low-draw profiles.
- **Passive by design:** Kismet never transmits — zero RF emission from the capture itself,
  fitting the deck's stealth profiles.

## Standalone Mode

Nothing here is deck-specific — Kismet runs on **any Kali box**. Plug the Panda (and optionally
the RT5370) and VK-162 into a laptop running Kali, repeat the install/config above, and launch
with `--override wardrive`. It's the same software stack; only the USB/antenna plumbing changes.
WiGLE CSV export and `.kismet` DBs come out identical whether on the deck or a bench laptop.

## Source / Upstream

- Upstream: [Kismet Wireless](https://www.kismetwireless.net/) · [Wardrive mode docs](https://www.kismetwireless.net/docs/readme/configuring/wardrive/)
- Full options, hardware tiers, WiGLE workflow, legal notes: [projects/07-kismet-wardriving](../../../07-kismet-wardriving/)
