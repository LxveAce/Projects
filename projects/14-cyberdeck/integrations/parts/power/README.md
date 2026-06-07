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

## Source / Upstream

- Deck power design: [deck README §5 Power System](../../../README.md) and
  [§8 Connectivity & Switching](../../../README.md) (USB hub architecture, per-device
  switches, power-savings modes, power-distribution wiring diagram)
- Exact parts: [INVENTORY.md](../../../../../INVENTORY.md)
