# RayHunter — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/05-rayhunter](../../../05-rayhunter/)
> **Deck role:** Stingray / IMSI-catcher detector (companion device)
> **Status:** Need hardware (buy an Orbic RC400L, ~$20-30 used)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Device** | Orbic Speed **RC400L** mobile hotspot (also sold as Kajeet RC400L) |
| **Why this device** | Qualcomm modem + exposed `/dev/diag` — RayHunter's hard requirement |
| **Firmware** | EFF **RayHunter** ([EFForg/rayhunter](https://github.com/EFForg/rayhunter)), runs *on the Orbic* |
| **Where it runs** | **On the Orbic itself** — *not* on the Pi 5 |
| **Deck slot** | Companion: rides in a foam bay, charges off deck USB |
| **Install tool** | EFF `installer` script (rootshell/adb), run once from your PC |
| **Checked via** | Its own web UI at **http://192.168.1.1:8080** (over its WiFi or USB) |
| **Power** | Deck USB charge port — it runs on its **own battery** (18-22 hr) |

> **Why it lives on the Orbic, not the Pi:** RayHunter reads raw cellular control-plane
> traffic through the Qualcomm modem's `/dev/diag` interface. The Pi 5 has no cellular
> baseband, so it physically *cannot* run RayHunter. The Orbic is a self-contained
> detector — the deck just carries it and tops up its battery.

> **Critical:** there is **no Pi-side daemon and no serial link**. The deck does not
> integrate RayHunter over USB/serial like the ESP32s. It is a standalone gadget that
> happens to ride along; you check it on its own web page.

---

## What You Need (from the repo inventory)

- Orbic Speed **RC400L** hotspot (used/renewed, ~$20-30) — **not yet owned**, must buy
- USB cable for flashing (data-capable) — used once, from your PC
- A WiFi-capable device (phone/laptop/Pi) to reach its web UI at `192.168.1.1:8080`
- A deck USB charge port + short USB cable to keep it topped up (see [parts/power](../parts/power/))
- A foam bay cut into the Pelican layout to hold the Orbic

> Nothing else from the [INVENTORY](../../../../INVENTORY.md) substitutes — no ESP32,
> antenna, or display in the kit has a cellular modem, so the Orbic is mandatory hardware.

---

## Get It Running

### 1. Acquire & flash (one-time, off the deck)

1. **Buy** an Orbic RC400L (eBay / Amazon renewed, ~$20-30). Kajeet RC400L is identical hardware.
2. **Note the admin password:**
   - Verizon units: the WiFi password printed on the device *is* the admin password.
   - Kajeet/Smartspot units: default is `$m@rt$p0tc0nf!g`.
3. **Download** the latest release from
   [github.com/EFForg/rayhunter/releases](https://github.com/EFForg/rayhunter/releases) and unzip.
4. **Run the installer** from your PC (network method, recommended):
   ```bash
   ./installer orbic --admin-password 'mypassword'
   ```
   (Kajeet: use `--admin-password '$m@rt$p0tc0nf!g'`. If network install fails:
   `./installer orbic-usb`.) The installer roots the device, deploys the daemon, and
   sets it to autostart.
5. **Confirm the web UI:** join the Orbic's WiFi, browse to **http://192.168.1.1:8080**,
   and you should see the RayHunter dashboard.

> Shell access if you need to debug: `./installer util orbic-shell` (or `adb shell` →
> `/bin/rootshell` on older builds). See the [full reference](../../../05-rayhunter/)
> for heuristics, alert handling, and legal context.

### 2. Ride with the deck

- **Mount:** drop the Orbic into its foam bay. No standoffs, no antenna, no serial wiring.
- **Charge:** run a short USB cable from a deck charge port to the Orbic. It runs on its
  **internal battery** (18-22 hr) — the deck port just keeps it from draining on long ops.
  No toggle switch is assigned to it; it's a charge-only tap.
- **No data link:** it does **not** report to the Pi dashboard. RayHunter starts
  automatically on power-up and runs fully on the Orbic.

### 3. Verify

1. Power the Orbic on — RayHunter autostarts.
2. From the Pi (or a phone), join the Orbic's WiFi and open **http://192.168.1.1:8080**.
3. Read the status line: **green** = no suspicious activity, **red** = possible IMSI catcher.
4. On a red alert, note location/time and download the logs from the web UI for analysis.

---

## Cyberdeck Compatibility Notes

- **No USB/serial budget:** unlike the ESP32s, RayHunter consumes **no** Pi serial port
  and **no** powered-hub toggle. It only taps a USB charge port.
- **Antenna:** none of the deck's five SMA bulkheads — the Orbic uses its internal
  cellular antenna. Zero conflict with Marauder/Flock/Meshtastic/Kismet radios.
- **Power:** charge-only off the deck ([power guide](../parts/power/)); not gated by any
  of the SW1-SW7 switches, so it keeps running even in low-draw "stealth" profiles.
- **Dashboard:** **not** wired into the Pi 5 dashboard. Checked on its own web UI.
- **RF footprint:** it transmits as a normal LTE hotspot (cellular + its WiFi AP). If you
  want true RF silence, power the Orbic off — there is no switch to gate it from the deck.

## Standalone Mode

The Orbic is **always** standalone — that's the whole design. Pull it from the foam bay,
pocket it, and it runs on its own battery for 18+ hours with no deck attached. The deck
adds nothing to its function except a charge tap and a place to carry it. Check it the
same way anywhere: join its WiFi, open `192.168.1.1:8080`.

## Source / Upstream

- Upstream firmware: [EFForg/rayhunter](https://github.com/EFForg/rayhunter) (GPL-3.0)
- Official docs: [efforg.github.io/rayhunter](https://efforg.github.io/rayhunter/)
- Full options, heuristics, legal notes, device list: [projects/05-rayhunter](../../../05-rayhunter/)
