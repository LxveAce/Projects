# Pwnagotchi — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/03-pwnagotchi](../../../03-pwnagotchi/)
> **Deck role:** Docked companion — drops into a charge/offload bay, runs autonomously
> **Status:** Troubleshooting (e-ink + HDMI blank — see Verify; likely GPIO solder, test/reflow)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Board** | CanaKit Raspberry Pi **Zero 2 W** |
| **Image** | **jayofelony fork** (v2.9.x+ — the only one that supports the Zero 2 W) |
| **Display** | Waveshare **2.13" e-Paper HAT V4** (250x122, SPI) |
| **Battery** | **PiSugar S** 1200 mAh UPS (mounts underneath) |
| **WiFi** | RT5370 USB dongle (onboard WiFi can't do monitor-mode injection) |
| **Integration** | **DOCK only** — Pwnagotchi is *not* on the deck's board set |
| **Dock power/data** | Foam bay → USB to Pi 5 (charge + handshake offload) |

> **Why docked, not integrated:** the Zero 2 W + e-ink + PiSugar is already a perfect
> pocket-sized autonomous unit. Bolting it onto the main board set adds complexity for no
> gain — Pwnagotchi is *designed* to wander on battery and hunt handshakes on its own. The
> deck explicitly **excludes it from the board plate set** ([deck README](../../README.md)).
> Instead the deck gives it a home: a pick-and-pluck **foam bay** where the assembled unit
> drops in to charge and dump captures over USB, then comes back out to roam.

> **Critical:** use the **jayofelony** image, not the original evilsocket one — the Zero 2 W
> is only supported on the fork. And the display is a **V4**, so `ui.display.type` must be
> `waveshare_4` (some images need `waveshare213inb_v4`). The wrong value = blank screen.

---

## What You Need (from the repo inventory)

- CanaKit Raspberry Pi Zero 2 W (with 32 GB SD from the kit)
- Waveshare 2.13" E-Ink HAT **V4** (250x122, SPI) — plugs onto the 40-pin GPIO header
- PiSugar S 1200 mAh UPS (note: PiSugar S lacks I2C — no software battery readout)
- RT5370 WiFi USB dongle (proven Pwnagotchi monitor-mode + injection on 2.4 GHz)
- KOOTION 16 GB micro SD (Class 10) — plenty for the image; save 128 GB cards elsewhere
- Rii K06 Mini Bluetooth Keyboard #1 — dedicated to this rig for headless SSH/terminal
- JSAUX Micro-HDMI→HDMI adapter #2 — for boot output during setup/debug
- Fluke 17B+ multimeter — for GPIO solder-joint continuity
- USB **data** micro-USB cable for first boot / dock offload

> See [INVENTORY.md](../../../../INVENTORY.md) for the exact items.

---

## Get It Running

### 1. Build & flash

1. Download the **jayofelony** image (`.img.xz`): https://github.com/jayofelony/pwnagotchi/releases (v2.9.x+).
2. Flash to the micro SD with [Balena Etcher](https://etcher.balena.io) or Raspberry Pi Imager (~5 min).
   - **Do NOT** use Pi Imager's username/password/WiFi customization — the image handles that itself.
3. On the SD card's `boot` partition, create `config.toml`:

```toml
main.name = "pwnagotchi"
main.lang = "en"
main.whitelist = [ "YourHomeNetwork", "AA:BB:CC:DD:EE:FF" ]

ui.display.enabled = true
ui.display.type = "waveshare_4"   # V4 — try "waveshare213inb_v4" if blank
ui.display.color = "black"
ui.display.rotation = 180
ui.fps = 0                         # 0 = refresh on change only (required for e-ink)

main.plugins.grid.enabled = true
main.plugins.grid.report = true
```

4. Seat the Waveshare V4 HAT fully onto all 40 pins. Plug the RT5370 dongle into the data USB port (via OTG adapter).
5. **First boot:** insert SD, power via the **DATA** micro-USB port, wait **3–10 min** untouched (RSA key generation — interrupting it corrupts the install). Green LED activity = good; solid red only = problem.

### 2. Dock with the deck

The Pwnagotchi assembles and runs as a standalone unit, then **docks** into the deck:

- **Bay:** a pick-and-pluck **foam cavity** in the [Pelican 1300](../../README.md) holds the assembled
  unit. Foam is fine here — the Zero 2 W + e-ink are low-heat (unlike the Pi 5 / ESP32s, which
  must stay on the acrylic plates).
- **Charge + offload:** a USB run from the deck's **Pi 5 spare USB port** ([wiring map](../../README.md))
  feeds the dock. Plugged in, the Pwnagotchi drops to **MANU mode** (idle) so you can SSH in and
  pull captures; unplugged, it returns to **AUTO mode** and hunts on its own.
- **Power:** the dock USB both tops up the PiSugar S and powers MANU-mode offload — no separate
  brick in the field. See the [power guide](../parts/power/) for hub/port budget.
- **It is NOT a board on the deck:** no plate, no SMA bulkhead, no toggle switch is assigned to it.
  It owns nothing on the [master wiring table](../README.md) — by design.

### 3. Verify

> **STATUS (current):** Not working — display blank AND not broadcasting. GPIO hardware is
> **ruled out** (Fluke 17B+ confirmed proper voltage and continuity on all pins). Marauder's
> "Detect Pwnagotchi" also sees nothing — meaning the Pi likely isn't booting into AUTO mode
> at all (or isn't booting period). This points to a boot/image problem, not just display.
> Next step: connect to a PC over USB, check if the Pi even responds to ping/SSH.

### Debug plan (connect to PC)

GPIO hardware is cleared — Fluke confirmed good voltage and continuity on all pins. More importantly, Marauder's "Detect Pwnagotchi" (`sniffpwn`) didn't pick up any beacon — in AUTO mode, Pwnagotchi actively broadcasts on 2.4GHz, so this means the Pi probably isn't running Pwnagotchi at all. **Step 1 (SSH check) is critical** — if the Pi doesn't respond, the image may be corrupt or the SD card may have an issue.

**Step 1 — Check if the Pi is alive:**
```
# Plug into PC via the DATA micro-USB port (not POWER port)
# On Windows: install RNDIS driver if needed, set USB Ethernet adapter to:
#   IP: 10.0.0.1   Subnet: 255.255.255.0   Gateway: (blank)
# On Linux: gadget appears as usb0, set it to 10.0.0.1/24

ping 10.0.0.2
ssh pi@10.0.0.2          # default password: raspberry
```
- **If SSH works** → Pi boots, problem is display config. Go to step 2.
- **If ping fails** → check:
  - Green activity LED blinking? (No blink = bad SD image or power)
  - Right USB port? (DATA, not POWER)
  - Data cable? (Charge-only cables won't enumerate the gadget)
  - Try re-flashing a fresh jayofelony image

**Step 2 — Check config (the usual suspect):**
```bash
cat /etc/pwnagotchi/config.toml | grep -i display
# ui.display.type MUST be "waveshare_4" or "waveshare213inb_v4"
# ui.display.enabled MUST be true
# ui.fps MUST be 0

grep spi /boot/config.txt
# Must have: dtparam=spi=on
```
Wrong `display.type` is the #1 cause of blank screens. The V4 display is picky about this — try both `waveshare_4` and `waveshare213inb_v4` if one doesn't work.

**Step 3 — Check the Pwnagotchi logs:**
```bash
sudo journalctl -u pwnagotchi --no-pager | tail -50
# Look for display/SPI errors, Python tracebacks, plugin crashes
# Also check:
sudo cat /var/log/pwnagotchi.log | tail -50
```
The logs often show exactly what's wrong — a bad import, a display driver error, a plugin crashing at startup.

**Step 4 — Test with dummy display (isolate the display):**
```bash
sudo nano /etc/pwnagotchi/config.toml
# Change: ui.display.type = "dummydisplay"
sudo systemctl restart pwnagotchi
```
Open `http://10.0.0.2:8080` in a browser. If the web UI shows the Pwnagotchi face → software is fine, display or its driver is the problem. If the web UI is also broken → something is wrong with the Pwnagotchi install itself.

**Step 5 — Fresh flash (if nothing else works):**
1. Re-flash a clean jayofelony image onto the SD card
2. Write a minimal `config.toml` with just display settings (no plugins, no extras)
3. Boot with display seated, wait the full 3-10 min (first boot generates RSA keys)
4. If still blank after fresh flash with known-good config → the display itself may be dead. Try swapping it if you have another e-ink HAT.

Captures verify without a display: `ls -lh /home/pi/handshakes/` over SSH, or the web UI.

---

## Cyberdeck Compatibility Notes

- **Not on the board set:** owns no acrylic plate, no SMA bulkhead, and no toggle switch
  (SW1–SW7 are all spoken for elsewhere). It is a **drop-in dock occupant**, full stop.
- **USB/serial budget:** consumes only the **Pi 5 spare USB port** while docked — no powered-hub
  port, unlike the ESP32 boards.
- **Detect Pwnagotchi (Marauder):** the deck's [ESP32 Marauder](../01-esp32-marauder/) on Gold #1
  has a **"Detect Pwnagotchi"** function — so the deck can *see* its own (or anyone's) Pwnagotchi
  beacon on 2.4 GHz. Handy to confirm the docked unit is alive/AUTO without SSH.
- **Antenna:** uses its own RT5370 dongle on 2.4 GHz — independent of the deck's SMA bulkheads,
  so no RF/antenna conflict with Marauder/Flock/BLE.
- **Heat:** safe in foam (low-power Zero 2 W); keep it out of the [cooling](../parts/cooling/) loop
  that serves the Pi 5 and ESP32 plates.

## Standalone Mode

This is the **default** mode — the deck dock is the optional part. Pull the unit from the bay,
power the PiSugar S, and it runs **fully autonomous** (AUTO/AI mode) in your pocket, hunting
WPA handshakes on the RT5370 and showing its face on the e-ink. Nothing about docking changes
the build; the dock only adds charge + offload convenience. Bring it back to the deck to top up
and dump captures to the Pi 5 over USB.

## Source / Upstream

- Recommended image: [jayofelony/pwnagotchi](https://github.com/jayofelony/pwnagotchi) (Zero 2 W support, v2.9.x+)
- Community hub: [pwnagotchi.org](https://pwnagotchi.org/getting-started/index.html)
- Full hardware list, soldering guide, deep troubleshooting, plugins: [projects/03-pwnagotchi](../../../03-pwnagotchi/)
