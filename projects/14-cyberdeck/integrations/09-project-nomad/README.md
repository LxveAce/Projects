# Project Nomad — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/09-project-nomad](../../../09-project-nomad/)
> **Deck role:** Offline knowledge/AI/media server — **companion module, not on the Pi 5**
> **Status:** BLOCKED — needs x64 hardware the deck does not yet have

---

## The Blocker (read this first)

Project N.O.M.A.D. (Node for Offline Media, Archives, and Data) is **x86-64 only**. Its
Docker images are published only for `linux/amd64`, and the installer assumes NVIDIA GPU
passthrough — there is **no ARM path** in upstream. The deck's brain is a **Pi 5 (ARM64)**,
so NOMAD **cannot run on the deck's Pi 5.** This is not a tuning problem; the containers
will not pull on ARM.

There is no honest "flash it and go" here. NOMAD joins the deck only once you add a
**separate x64 single-board computer** as a companion module.

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Runs on the Pi 5?** | **No** — Pi 5 is ARM64, NOMAD is amd64-only |
| **Chosen path** | **Separate x64 SBC** as a companion — **LattePanda 3 Delta** (~$200-300) |
| **Status of that board** | On the **"still need"** list — not yet purchased |
| **OS** | Ubuntu Desktop 24.04 LTS on NVMe |
| **Install** | Upstream `install_nomad.sh` (standard amd64 install) |
| **Deck link** | Local Wi-Fi / Ethernet only — browse NOMAD from the Pi 5's 7" screen |
| **Fallback only** | RPi ARM fork, or QEMU emulation — *not* the chosen route |

> **Why LattePanda 3 Delta and not "make the Pi 5 work":** the Delta is x86-64, runs Ubuntu
> + Docker natively, and takes the **standard install with zero porting**. It is the same
> companion-module pattern the deck already uses for [RayHunter](../05-rayhunter/) and
> [NyanBOX](../11-nyan-box/) — a dedicated device that rides along, not another load on the Pi.

> **Why not the fallbacks:** the community ARM fork ([eglische/project-nomad-rpi](https://github.com/eglische/project-nomad-rpi))
> works on a Pi 5 but is unofficial and AI is minimal; QEMU emulation runs amd64 images on
> ARM but is **5-8x slower** and unusable for LLM inference. Keep both as last resorts.

---

## What You Need

**Not in inventory yet** — this whole module is forward-looking.

- **x64 SBC** — LattePanda 3 Delta (~$200-300, *still-need list*). Intel N5105, 8 GB RAM,
  64 GB eMMC + M.2 NVMe slot
- **NVMe SSD** — 512 GB-1 TB for the OS and offline content (Wikipedia w/ images alone ≈ 100 GB)
- **Ubuntu Desktop 24.04 LTS** — flashed to USB to install onto the SBC
- **12V power** — the Delta is 10W TDP; off the deck's [power rail](../parts/power/) or its own brick
- From inventory, **reserved for when the board arrives** ([INVENTORY.md](../../../../INVENTORY.md)):
  - Hosyond 7" DSI #2 *(or ELECROW 5" HDMI)* — local screen if you want it self-contained
  - ProtoArc XK01 foldable BT keyboard — for direct workstation use
  - 32 GB USB 3.0 flash drive — Ubuntu installer media

---

## Get It Running

This stays **conditional on acquiring x64 hardware.** Nothing below runs on the Pi 5.

### 1. Acquire x64 hardware

1. Buy a **LattePanda 3 Delta** (or any small x86-64 mini PC / SBC).
2. Add a **512 GB-1 TB NVMe SSD** for OS + content.
3. This is the gating step — until the board is in hand, the rest does not apply.

### 2. Install (standard amd64 path)

1. Flash **Ubuntu Desktop 24.04 LTS** to USB, install it to the NVMe, set BIOS to boot NVMe.
2. Update, then run the upstream installer:
   ```bash
   sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
   curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/main/install/install_nomad.sh -o install_nomad.sh
   sudo bash install_nomad.sh
   ```
3. Open the Command Center at `http://localhost:8080` (or `http://<sbc-ip>:8080`).
4. Use the Easy Setup wizard to pick apps (Kiwix, Kolibri, maps, AI) and content tiers,
   then **download everything while online**.
5. Disconnect — NOMAD then runs fully offline.

> Fallback only, if you refuse to buy x64 hardware: the [RPi ARM fork](https://github.com/eglische/project-nomad-rpi)
> installs on the Pi 5 directly. Treat it as unsupported and expect minimal AI.

### 3. Ride with the deck

NOMAD has **no serial/USB tie-in** to the deck — it's a network service, not an ESP32 radio.

- **Link:** put the SBC and the Pi 5 on the same LAN (Ethernet, or have the SBC run a
  `hostapd`/NetworkManager Wi-Fi hotspot the deck joins).
- **Use it:** open the Pi 5's [dashboard](../parts/dashboard/) / Chromium kiosk and browse to
  `http://<sbc-ip>:8080`. The deck's 7" screen is your NOMAD client.
- **Power:** the Delta can hang off the deck's [power system](../parts/power/) (12V) or run on
  its own battery/brick as a true grab-and-go companion.
- **No bulkhead/switch slot** is consumed on the deck — NOMAD owns none of SW1-SW7 or SMA #1-#5.

---

## Cyberdeck Compatibility Notes

- **Architecture is the hard wall:** Pi 5 = ARM64, NOMAD = amd64-only. There is no wiring or
  config trick that changes this — it needs its own x64 silicon.
- **Zero radio/serial budget:** unlike every ESP32 guide here, NOMAD doesn't touch the
  115200-baud serial bus, the powered hub switches, or any SMA bulkhead. It's purely IP.
- **Relation to Meshtastic:** NOMAD is a knowledge/AI server, **not** a comms platform — it
  does **not** integrate [Meshtastic](../04-meshtastic/) today. They're complementary: Meshtastic
  carries messages off-grid, NOMAD holds the offline library/AI. You could run a Meshtastic
  node on the same x64 box, but they'd be independent services.
- **Power draw:** an always-on extra SBC is a real budget hit for the deck's "stealth"/low-draw
  profiles — plan to power it only when you actually need the library.

## Standalone Mode

NOMAD is **standalone by nature** — it was designed as a self-contained box, so "deck
integration" is really just pointing the deck's browser at it. With its own screen
(Hosyond 7" / ELECROW 5") and the ProtoArc keyboard, the LattePanda is a complete offline
knowledge workstation with no Pi 5 involved at all. Pull it off the deck and it loses nothing.

## Source / Upstream

- Upstream: [Crosstalk-Solutions/project-nomad](https://github.com/Crosstalk-Solutions/project-nomad)
- Community ARM fork (fallback): [eglische/project-nomad-rpi](https://github.com/eglische/project-nomad-rpi)
- Full options, x64 rationale, LattePanda specs, forking guide: [projects/09-project-nomad](../../../09-project-nomad/)
