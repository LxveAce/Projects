# Project 16: BlueJammer-V2 — (Reference Only / Not Operated)

> **Status:** Cataloged for reference — **NOT built or operated** (see Legal)
> **Upstream:** [EmenstaNougat/BlueJammer-V2](https://github.com/EmenstaNougat/BlueJammer-V2)
> **License:** "All Rights Reserved" (closed-source; pre-compiled binaries only)
> **What it is:** A 2.4 GHz (and 5 GHz-controller) **RF jammer**.

---

## 1. What it is

BlueJammer-V2 is a purpose-built **signal jammer**. It uses an **ESP32-WROOM-32U** driving
**1–4× NRF24L01+** modules (round-robin channel hopping) to flood 2.4 GHz, with an **Ai-Thinker
BW16 (RTL8720DN)** board hosting a 5 GHz web control panel and an SSD1306 OLED for local control.

Its modes are all jamming:

| Mode | Target | Channels |
|------|--------|----------|
| 1 | Bluetooth | 0–79 |
| 2 | BLE | 0–39 |
| 3 | Wi-Fi | 0–14 |
| 4 | RC / Drone | 0–125 |

There are **no scan/detect/analyze modes** — it only transmits noise. The firmware is
**closed-source ("All Rights Reserved")**, distributed as pre-built binaries via the author's site.

---

## 2. Why this project is reference-only

**Operating an RF jammer is illegal** and there is **no authorized-use exception** — unlike
deauth (a targeted, authorized WiFi pentest technique), broadband jamming is banned outright:

- **US:** 47 U.S.C. §333 + the FCC's blanket prohibition on **marketing, sale, and use** of jammers
  — including on your own property, even "just testing." Penalties are severe (large fines, seizure).
- **Drone/RC jamming** adds FAA / 18 U.S.C. §32 exposure; counter-drone jamming is reserved for
  specific federal agencies.
- A broadband 2.4 GHz jammer is an **indiscriminate denial-of-service** device — it would also take
  down your own deck's WiFi/BLE/GPS, neighbors, medical devices, etc.

So this repo entry exists to **document the project and its threat model**, not to build or run it.
It is also **closed-source**, so there's nothing to fork or integrate.

---

## 3. What we actually take from it — the lawful, defensive side

The valuable, on-brand capability the BlueJammer threat model points to is **detection**: knowing
when *you* (or a site you're assessing) are being jammed, and doing legitimate 2.4 GHz research with
the same nRF24 radio in **receive-only** mode. That's the cyberdeck integration:

- **2.4 GHz interference / jamming detection** — sweep nRF24 RSSI across channels to spot a raised
  noise floor / jamming / congestion. Extends the deck's existing **deauth detection**,
  **Drone RemoteID detection**, and **stingray detection** ([RayHunter](../05-rayhunter/)) posture.
- **nRF24 2.4 GHz research (RX)** — Mousejack-class wireless keyboard/mouse dongle discovery &
  sniffing, Crazyradio-style device enumeration — passive/lawful work the Marauder/ESP32 WiFi stack
  can't do.

See **[14-cyberdeck/integrations/16-bluejammer](../14-cyberdeck/integrations/16-bluejammer/)** —
the deck integrates the **detector**, never the jammer. (The deck already has 5 GHz visibility via
the Panda PAU0F + Kismet, so the BW16 board is largely redundant.)

---

## 4. Hardware (for the lawful detector, not the jammer)

- **NRF24L01+ (PA/LNA)** module ×1–2 + a 3.3 V adapter / decoupling cap — for RX interference
  detection and Mousejack/Crazyradio research.
- An ESP32 you already own drives it (no need for the WROOM-32U "jamming engine").

---

## 5. Resources

- Upstream (reference): https://github.com/EmenstaNougat/BlueJammer-V2
- Lawful counterpart in the deck: [RF interference detection + nRF24 research](../14-cyberdeck/integrations/16-bluejammer/)
- Related defensive tools already in the kit: [RayHunter](../05-rayhunter/), [Flock/Drone detection](../06-flock-drone-detection/), Marauder `sniffdeauth`.
