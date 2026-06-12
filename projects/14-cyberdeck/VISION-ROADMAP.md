# Cyberdeck + Cyber Controller — Vision & Forward Roadmap

*A synthesis/"squash-all" document tying the orchestration software, the hardware build, and the
firmware fleet into one direction. Companion to `CYBERDECK-V2-ARCHITECTURE.md` (the hardware),
`BUILD-GUIDE-STEP-BY-STEP.md` (the build), and `FIRMWARE-DEVICE-SPECIALTIES.md` (the per-firmware
fit). Written to be honest about what exists today vs. what is planned — claims here are grounded in
shipped, tested code, not aspiration.*

Last updated: 2026-06-12 · Anchored to **Cyber Controller v1.1.0** (released).

---

## 1. North Star

**One operator, one screen, every radio.** A portable security-hardware deck where a heterogeneous
fleet of cheap RF boards (ESP32 classic/S2/S3/C5/C6, Realtek BW16, Flipper, LoRa, Pi-class SBCs)
behaves like a single instrument. The operator expresses **intent** — *find APs*, *map BLE*, *sweep
sub-GHz*, *capture handshakes* — and the system fans that intent out to whatever hardware is plugged
in, each running its strongest native firmware, with results converging into one shared picture.

The software that makes this real is **Cyber Controller (CyberC)**; the body it lives in is the
**cyberdeck**; the muscle is the **firmware fleet**. This doc is about how the three converge.

---

## 2. Where we actually are (v1.1.0, honest baseline)

What works **today**, validated this cycle on real hardware:

- **Flash engine, 19 firmware profiles, 5 backends** (`esptool`, `qFlipper`, ADB, SD-image,
  `rtl8720`). New this release: GhostESP `.zip` bundles, Meshtastic per-chip zips, and a full
  **BW16/RTL8720DN (Realtek AmebaD)** backend — the first non-ESP32 radio brought in first-class.
  Supply-chain integrity: SHA-256 pinning on the third-party BW16 bundle, allowlisted SSRF-safe
  downloads, path-traversal-safe extraction, TOCTOU-safe suicide flashing.
- **Unified Action Broadcast** — the North Star in embryo. One verb → every connected radio fires
  it in its own command; results merge into the Target Pool. *Live-proven:* "Find APs" hit a BW16
  (`AT+SCAN`, dual-band) and a GhostESP (`scanap`, 94 APs) simultaneously.
- **A genuinely hardened web + desktop remote.** A full 10-finding security audit is **closed**:
  durable hash-chained audit trail, strict CSP (nonce, no `unsafe-inline`), session-fixation
  defenses, Windows NTFS ACLs on secrets, no silent dev-server on LAN. This is the difference
  between a demo and something you'd actually run on a deck that drives attack hardware.
- **A real fleet on the bench:** classic ESP32 (Marauder/GhostESP/Bruce/DIV-legacy), BW16 Vampire
  (dual-band deauth/recon), Meshtastic Heltec V3 (LoRa mesh, configured + talking).

What is **not** here yet: the Raspberry Pi core (hardware not yet connected), the physical deck
chassis, and the appearance-affecting small-screen UI adaptations (deferred, owner-decision).

---

## 3. The three pillars

### Pillar A — Cyber Controller (the orchestration brain)
The intent layer. Its job is to make N dissimilar radios feel like one. The architecture that gets
us there is already seeded: a verb registry (`BROADCAST_CAPABILITIES`), per-protocol command maps,
a convergent `TargetPool`, and an `AutoRouter` for cross-device reactions (one board sees a target →
another board acts). The trajectory is **more verbs, more protocols, smarter convergence** — not a
rewrite.

### Pillar B — The cyberdeck (the body)
A Pi-class brain + a powered USB fabric + a multi-variant ESP32/BW16 radio fleet + displays + power +
antennas, each board pinned to the firmware it's best at (see `FIRMWARE-DEVICE-SPECIALTIES.md`). The
deck is what turns "a pile of dev boards on a desk" into a field instrument. `CYBERDECK-V2-
ARCHITECTURE.md` already maps board→role; the build guide phases the physical assembly.

### Pillar C — The firmware fleet (the muscle)
Marauder / GhostESP / Bruce / ESP32-DIV / HaleHound / BW16 Vampire / Meshtastic / Flock-You /
OUI-Spy / Sky-Spy / AirTag / Minigotchi / Flipper (Momentum/Unleashed) / RayHunter / Pwnagotchi /
RaspyJack / Kali-ARM. Each is a specialist; CyberC is the conductor. Capabilities are **labeled and
gated, never removed** — the deck's value is breadth, and lawful-use posture is enforced by warnings
and confirmations, not by crippling the hardware.

---

## 4. Roadmap by horizon

### Horizon 1 — "The deck powers on" (next)
- **Bring up the Pi as the core.** Put CyberC on the Pi, drive the radio fleet from it over the USB
  fabric, talk to an ESP-with-display on the Pi's USB. End state: Kali on the Pi. *(Blocked only on
  the Pi being connected.)*
- **Small-screen UI pass** (the deferred, appearance-affecting `ui-optimization.md` items): touch
  sizing, lower the 900×600 minimum for 800×480 panels, lazy tab construction. Needs the owner's
  call on auto-detect vs. a settings toggle vs. kiosk/fullscreen.
- **Broadcast v2:** more verbs (sub-GHz sweep, NFC, NRF24, handshake-capture-all, mesh-relay), a
  per-verb live result panel, and a STOP-ALL that's instant across every port.

### Horizon 2 — "The deck is an instrument"
- **Cross-comm playbooks:** chain intents into reactive missions (scan → on-new-AP → targeted
  capture on a second radio → log), building on the existing `AutoRouter`.
- **HaleHound 5-domain monitor** surfaced as a first-class live view (WiFi/BLE/SubGHz/NFC/NRF24),
  feeding all event types into the Target Pool.
- **Field hardening:** the audit trail and ACL work already done becomes the foundation for an
  on-deck forensic log; consider an append-only export + integrity check on shutdown.

### Horizon 3 — "The deck defends and documents itself"
- **Duress / anti-forensic layer** (the Suicide-Marauder / Guardian work) integrated as an opt-in
  owner-only boot gate on selected nodes, host-side provisioned from CyberC's Tools dialog.
- **Self-auditing UI:** ship the security posture (CSP, ACLs, audit trail) as a visible "deck
  health" surface, plus a periodic self-scan of the deck's own web remote.
- **Public surfaces** kept honest and current: cybercontroller.org / esp32marauder.com reflect the
  real, shipped capability set (reconciled against the actual profile count and versions, as the
  fact-check pass did for the README).

---

## 5. Operating principles (carried from how this was built)

1. **Reliability/lawfulness first.** Capabilities are retained but labeled; broadband jamming stays
   excluded (47 U.S.C. §333 / FCC). Dangerous RF is framed as authorized-lab-only.
2. **Security before features, features before polish.** v1.1.0 shipped the full audit *before* the
   optimization pass landed — that order is deliberate and should hold.
3. **Verify on hardware; double-check the data.** Versions/repos were re-checked against upstream
   before being written down; firmware paths are validated on real boards before being claimed.
4. **Small, tested, self-merged PRs.** Every change ships green with a regression test; the history
   stays readable.
5. **Breadth is the product.** The deck wins by running *everything* well, orchestrated simply.

---

## 6. Open decisions for the owner

- **Pi connection + role split:** is the Pi the sole brain, or a brain + a dedicated Kismet/Panda
  host? How does it attach (LAN / USB-ether gadget / direct)?
- **Small-screen strategy:** auto-detect-and-adapt vs. settings toggle vs. kiosk fullscreen on the
  7" panel.
- **Which nodes get the duress/anti-forensic gate** (Horizon 3) — and the C2/T2 eFuse-before-burn
  decision already logged in the Suicide-Marauder notes.
- **Marauder "Lonely Binary Gold" chip identity** (classic vs S3) — still unresolved in the docs;
  affects flash offsets for those three owned boards.

---

*This is a living document. As horizons land, fold the result back into the architecture + build
guide and bump the anchor version at the top.*
