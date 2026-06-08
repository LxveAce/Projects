# Power System — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Source reference (all options):** [deck README §5 Power](../../../README.md) · [§8 Connectivity & Switching](../../../README.md)
> **Deck role:** Single-battery power distribution + per-device switching for the whole rig
> **Status:** Ready to build (power bank, hub, and switches in inventory)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Battery** | **Anker 347** power bank (25,600mAh, 30W) |
| **Pi 5 feed** | Anker **USB-C PD → Pi 5 directly** — always on, no switch |
| **Everything-else feed** | Anker **USB-A → powered 7-port USB hub** |
| **Hub** | Powered 7-port USB hub, **enclosure stripped, bare PCB mounted internally** |
| **Per-device switching** | **7× SPST mini toggle** switches, inline on each 5V hub-to-device run |
| **Switch hardware** | Twidec SPST mini toggles **with waterproof boot caps** |
| **12V rail** | **5V→12V boost converter** for the two IP67 cooling fans |
| **Always-on (no switch)** | **Pi 5** (USB-C PD) and **Panda PAU0F** (Pi USB 3.0 direct) |

> **Why one power bank, not a custom LiPo pack:** zero battery wiring, built-in protection,
> pass-through charging, and it can be swapped/upgraded later. The Anker's USB-C PD port
> alone carries the Pi 5; its USB-A port runs the hub that powers everything else.

> **Why a stripped powered hub, not the Pi's own ports:** the deck has 7 switched devices.
> A powered hub supplies a clean 500mA/port and keeps the Pi's USB 3.0 #1 free and at full
> bandwidth for the always-on Panda (Kismet primary). Strip the plastic enclosure and mount
> the bare PCB to reclaim ~50% of the space.

---

## What You Need (from the repo inventory)

- **Anker 347** power bank — 25,600mAh, 30W (USB-C PD + USB-A)
- **Powered 7-port USB hub** (strip the enclosure, mount the bare PCB)
- **7× SPST mini toggle switches** with **waterproof boot caps** (Twidec)
- **5V→12V DC boost converter** (feeds the two IP67 fans — see [cooling](../cooling/))
- USB-C **PD** cable (Anker → Pi 5) + panel-mount USB-C for case-side charging
- Hookup wire for the inline switch splices (the 5V leg only)
- Full part list: [INVENTORY.md](../../../../../INVENTORY.md)

---

## Get It Running

### 1. Battery + hub

1. Mount the **Anker 347** in the bottom layer (foam-plucked bay).
2. **USB-C PD out → Pi 5** directly. This rail is **always on** — no switch in the path.
   (See [pi5-brain](../pi5-brain/) for the Pi side.)
3. **USB-A out → powered USB hub upstream.** The hub's own upstream data also runs to the
   Pi's **USB 3.0 #2** so the Pi sees every device.
4. The hub's 7 downstream ports feed: 5× ESP32 boards, the RT5370, and a USB flash drive.
5. Panel-mount a **USB-C IN** on the case wall for pass-through charging.

> **Always on, no switch:** Pi 5 (USB-C PD) and the **Panda PAU0F** (wired to Pi USB 3.0 #1
> direct, not the hub). Kismet is the primary tool and needs full USB 3.0 bandwidth.

### 2. Wire the 7 switches

Every switched device gets one **SPST mini toggle** inline on its **5V** line between the hub
port and the device. **Cut and splice only the 5V wire — GND passes through unbroken.**

```
Hub Port ──→ [5V wire cut] ──→ [SPST Toggle] ──→ [5V continues] ──→ Device
              GND wire passes through unbroken
```

| Switch | Device | Notes |
|--------|--------|-------|
| **SW1** | Gold #1 — Marauder | see [01-esp32-marauder](../../01-esp32-marauder/) |
| **SW2** | Gold #2 — Flock | |
| **SW3** | Gold #3 — BLE / Chasing Your Tail | |
| **SW4** | Heltec LoRa V3 — Meshtastic | |
| **SW5** | WROOM-32 — Drone RemoteID | |
| **SW6** | RT5370 — Kismet secondary | |
| **SW7** | VK-162 — GPS | |

When a switch is **OFF that device draws zero power** — completely dead, no standby drain and
(for the radios) zero RF emission. Use the **waterproof boot caps** so the panel keeps the
case's water/dust resistance.

### 3. Power modes

Pick a mode by which switches you flip. (Pi 5 + Panda are always on, so they're the floor.)

| Mode | Switches ON | Est. Draw | Use Case |
|------|------------|-----------|----------|
| **Full scan** | All 7 | ~3A | All tools simultaneously |
| **Wardriving only** | MAIN + KISM | ~1.5A | Kismet + GPS, everything else off |
| **Surveillance detect** | MAIN + FLOCK + BLE | ~1.2A | Driving — detect cameras + trackers |
| **Mesh comms only** | MAIN + MESH | ~0.9A | Off-grid messaging |
| **Stealth (passive)** | MAIN only | ~0.8A | Pi 5 only, no ESP32 RF emissions |

("MAIN" = Pi 5 + hub, always live; the named radios are their SW above.)

### 4. 12V rail (cooling fans)

The two IP67 cooling fans are **12V**. Feed a **5V→12V boost converter** from a spare hub /
USB-A 5V tap; its 12V output runs both fans. Details and fan wiring live in
[cooling](../cooling/).

### 5. Verify

```bash
lsusb            # every switched-ON device should enumerate; flip a switch and re-run
vcgencmd get_throttled   # 0x0 = Pi 5 getting clean, sufficient power (no under-volt flag)
```
Flip each SW1–SW7 on/off and confirm the matching device appears/disappears in `lsusb`.
Confirm Pi 5 and Panda stay present regardless of any switch.

---

## Cyberdeck Compatibility Notes

- **Two rails from one bank:** USB-C PD carries the Pi 5; USB-A carries the hub (everything
  else). Don't move the Pi onto the hub — it needs the dedicated PD feed.
- **Switch map is fixed:** SW1–SW7 match the [master wiring table](../../README.md). Every
  integration guide references its own switch by this number — don't renumber.
- **Panda is unswitchable by design:** wired direct to Pi USB 3.0 #1, always on with the Pi.
- **GND is shared:** switches break only the 5V leg; never cut GND or devices won't enumerate.
- **12V is downstream of 5V:** the cooling fans depend on this rail via the boost converter —
  see [cooling](../cooling/).
- **Stealth profile:** "MAIN only" cuts all ESP32 power, so the deck emits no ESP32 RF — the
  low-draw, RF-quiet profile referenced across the radio guides.

## Standalone Mode

Not applicable as a standalone tool — this subsystem **is** the power for the rig. It produces
no scan data of its own; it just delivers a clean 5V (and a 12V fan rail) to the Pi 5, the
hub, and the switched devices. Pull the Anker 347 and it's an ordinary USB-C PD power bank.

---

## Solar Charging (brainstorm)

The Anker 347 supports pass-through charging — a solar panel can feed the battery while the deck runs. The panel-mount USB-C on the case wall is the entry point. Here's the breakdown of what makes sense.

### The math

The deck's power draw depends on what's running:

| Mode | Draw | To charge at this rate, you need |
|------|------|----------------------------------|
| Stealth (Pi 5 only) | ~4W | Panel > 4W to gain charge |
| Wardriving | ~7.5W | Panel > 7.5W to gain charge |
| Full scan (everything on) | ~15W | Panel > 15W to gain charge |
| Deck off (just charging the Anker) | 0W | Any panel works |

A 20W-rated panel produces roughly 12-15W in direct sun (panel rating is lab conditions). So a 20W foldable can sustain wardriving mode in good sunlight, and charge the battery with the deck off. A 5W lid-mount panel realistically produces ~3W — not enough to run anything, but it can slowly top up a parked deck.

The Anker 347's USB-C input accepts up to ~18W. Anything above that is wasted, so there's no reason to go past a 30W panel (real-world output maxes out the Anker's input).

### Option A: Foldable panel (recommended — the one that actually matters)

A 20-30W USB foldable panel. Deploy it when you're stationary, plug into the case USB-C port, fold up and carry when moving.

**Why this is the move:**
- 12-18W real output — enough to charge the Anker from empty in ~8-10 hours of sun, or sustain the deck in low-power modes indefinitely
- No case modifications beyond the already-planned USB-C panel mount
- Can angle toward the sun (huge efficiency gain vs. flat-mounted)
- Folds to roughly book-sized, weighs ~1-2 lbs
- $40-70

**Options:**
- BigBlue 28W (~$55) — 3× USB-A, SunPower cells, proven outdoor. Need a USB-A to USB-C cable for the Anker.
- Nekteck 28W (~$50) — 2× USB-A, SunPower, similar to BigBlue.
- Anker 625 24W (~$85) — USB-C output, charges the Anker 347 natively over PD. Cleaner but pricier.
- Generic 20-25W USB-C panels on Amazon (~$30-45) — hit or miss on quality, but cheap.

**Use case:** Set up at a park bench, campsite, rooftop, car dashboard. Panel sits in the sun, cable runs to the deck. Deck runs in wardriving or surveillance mode. Solar sustains the battery — you run all day.

### Option B: Lid-mounted panel (cool factor — trickle only)

A small rigid or flexible panel attached to the outside of the Pelican 1300 lid. Charges whenever the case is in sunlight, even closed.

**The reality:** The Pelican 1300 lid is ~10.7" × 9.8", but after the handle, latches, and edges, you have maybe 7" × 8" of flat surface. That fits a 5W panel at best. Real-world output: ~3W. To charge the Anker 347 from empty at 3W would take **40+ hours of direct sun**. This is maintenance/trickle charging, not real power.

**Still worth it if:** you leave the deck in a car, on a windowsill, or outdoors between sessions. The battery stays topped without thinking about it. It's the "leave it and forget it" option.

**How to mount without killing IP67:**
- Adhesive or industrial velcro on the lid exterior (no drill holes = no sealing issues)
- Route the cable through an IP67 cable gland on the case wall (same as the antenna bulkheads)
- Or run the cable to the existing panel-mount USB-C port (external routing, no penetration)

**Panels that fit:**
- Generic 5V 5W mini solar panel (~$10-15, ~7" × 5") — wire to a small USB charge board inside
- Voltaic 3.5W or 6W panels (~$30-50) — designed for tactical/outdoor, USB output built in, rugged ETFE coating

### Option C: Both (the full setup)

A small panel on the lid for passive trickle + a foldable for active charging. Best of both, and they share the same USB-C input on the case.

- **Lid panel (5W):** keeps the battery alive between sessions without any effort — leave the case by a window or in the car
- **Foldable (20-28W):** deploy when you need real power in the field

Total cost: ~$60-100 for both.

### Option D: Backpack/MOLLE strap panel

A foldable panel with MOLLE straps or carabiners on the back of a backpack. Cable runs down to the deck while walking.

**Pros:** Charges on the move. **Cons:** Inconsistent angle (you're turning, shading changes), lower output than stationary, cable management is annoying. Better than nothing but worse than just stopping and deploying a foldable properly.

### What I'd do

**Start with a 20-28W foldable panel** (BigBlue or Nekteck, ~$50). That's the one that actually extends your runtime. If you like the concept, add a cheap 5W lid panel later for passive trickle. The foldable is the real workhorse; the lid panel is a nice-to-have.

| Item | Est. Price | Priority |
|------|-----------|----------|
| Foldable USB solar panel (20-28W) | ~$40-70 | High — this is the one that matters |
| Small rigid/flex panel for lid (5W) | ~$10-30 | Low — cool but trickle only |
| IP67 cable gland (if routing lid panel internally) | ~$5 | Only if doing lid mount |

---

## Source / Upstream

- Deck power design: [deck README §5 Power System](../../../README.md) and
  [§8 Connectivity & Switching](../../../README.md) (USB hub architecture, per-device
  switches, power-savings modes, power-distribution wiring diagram)
- Exact parts: [INVENTORY.md](../../../../../INVENTORY.md)
