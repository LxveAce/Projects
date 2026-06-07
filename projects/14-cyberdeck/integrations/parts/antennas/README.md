# Antennas & SMA Bulkhead Panel — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Full reference (all options):** [projects/14-cyberdeck — §6 Antenna Management](../../../README.md#6-antenna-management)
> **Deck role:** External RF I/O — one sealed bulkhead panel feeds every radio
> **Status:** Ready to build (bulkheads, pigtails, antennas in inventory)

---

## The Decision

One side wall gets **five IP67 waterproof SMA bulkheads** (O-ring sealed), each fed by a
U.FL/IPEX → SMA pigtail from the board that owns it. Antennas screw on outside; internal-PCB
boards (WROOM-32, CYDs) get **no** bulkhead.

| Bulkhead | Board / device | Antenna | Frequency |
|----------|----------------|---------|-----------|
| **SMA #1** | Lonely Binary Gold #1 — [Marauder](../../01-esp32-marauder/) | Bingfu dual-band | 2.4/5.8 GHz |
| **SMA #2** | Lonely Binary Gold #2 — [Flock](../../06-flock-drone-detection/) | DIYmall 2.4G | 2.4 GHz |
| **SMA #3** | Lonely Binary Gold #3 — [BLE](../../08-ble-detection/) | DIYmall 2.4G | 2.4 GHz |
| **SMA #4** | Heltec LoRa V3 — [Meshtastic](../../04-meshtastic/) | 915 MHz LoRa | 915 MHz |
| **SMA #5** | Panda PAU0F — [Kismet](../../07-kismet-wardriving/) | built-in (SMA extension) | 2.4/5/6 GHz |

> **Why IP67 bulkheads:** every hole in the Pelican breaks the IP67 seal. O-ring-sealed
> waterproof bulkheads seal the hole *by design* — no sealant required for the connection
> itself — and a bead of marine silicone makes it belt-and-suspenders.

> **No bulkhead for:** the **WROOM-32** (drone RemoteID — PCB trace antenna only, no IPEX)
> and both **CYD 2.8"** screens (PCB antenna, serial-only, no WiFi scanning). Adding external
> antennas to those would require soldering a U.FL feed point — not done.

---

## What You Need (from the repo inventory)

- 5× IP67 waterproof SMA bulkhead connectors, O-ring sealed (e.g. Exgoofit 5-pack)
- 5× U.FL/IPEX → SMA pigtail, 15–20 cm (one per board above)
- Bingfu 2.4/5.8 GHz antenna (Gold #1) + Boobrie RP-SMA→SMA adapter
- 2× DIYmall 2.4 GHz antenna (Gold #2, Gold #3)
- 915 MHz LoRa antenna (Heltec V3)
- SMA extension cable for the Panda PAU0F → SMA #5
- 3M Marine Grade Silicone Sealant (clear) — for the seal-and-suspenders pass
- SMA dust caps (~10-pack) — stow mode
- Adhesive cable clips — internal pigtail routing
- *(Drilling tools live in the [case-prep guide](../case-prep/) — step drill bit, deburring tool)*

---

## Get It Running

### 1. Drill + seal the bulkheads

1. On one side wall, mark **five** evenly spaced holes for the bulkheads (see [case-prep](../case-prep/)).
2. Drill each with a **step drill bit** (clean round holes in polycarbonate), then **deburr**.
3. Apply a ring of marine silicone around the hole on the **inside** of the case.
4. Insert each IP67 bulkhead from outside, push through, add a ring of silicone on the outer flange.
5. Tighten the nut firmly — the O-ring + sealant squeeze into any gaps. Wipe excess, cure 24 h.

### 2. Snap on the U.FL pigtails

For each Gold board and the Heltec V3 (the WROOM-32 and CYDs are skipped — PCB antenna only):

1. Locate the small gold **IPEX socket** on the board (near the "ANT" label / RF section).
2. Align the pigtail's **U.FL** connector directly over the socket.
3. Press **straight down** until you feel/hear a **CLICK**. **Never twist** — vertical only.
4. U.FL is rated for **~30 mating cycles** — treat as semi-permanent.

```
[board] ──IPEX(snap)──→ [U.FL pigtail 15-20cm] ──SMA──→ [IP67 bulkhead] ──→ [antenna]
```

### 3. Route to the bulkheads

- Run each pigtail by the **shortest path** to its assigned bulkhead; keep a 5 mm+ bend radius.
- Keep pigtails **away from power cables** (EMI); secure with adhesive cable clips.
- **Panda PAU0F:** it has its own antenna — run an **SMA extension cable** from the Panda to
  **bulkhead #5** (no U.FL snap on this one).
- Screw each external antenna onto its bulkhead outside (Bingfu uses the RP-SMA→SMA adapter).

### 4. Stow mode

- For transport, **unscrew all external antennas** and store them in the lid mesh pocket.
- Screw an **SMA dust cap** onto each bulkhead — protects the connector and keeps the seal flush.

### 5. Verify

- Tug-test each U.FL: it should hold without popping off (but don't yank — 30-cycle limit).
- Power each radio via its switch and confirm range improves vs. no antenna (e.g. Marauder
  `scanap` from the [Marauder guide](../../01-esp32-marauder/) should see more/farther APs).
- After silicone cure, the closed case with dust caps on should hold its IP67 seal.

---

## Cyberdeck Compatibility Notes

- **Bulkhead ownership (no collisions):**
  - **#1** → [Gold #1 / Marauder](../../01-esp32-marauder/) (2.4/5.8 GHz)
  - **#2** → [Gold #2 / Flock](../../06-flock-drone-detection/) (2.4 GHz)
  - **#3** → [Gold #3 / BLE](../../08-ble-detection/) (2.4 GHz)
  - **#4** → [Heltec V3 / Meshtastic](../../04-meshtastic/) (915 MHz LoRa)
  - **#5** → [Panda PAU0F / Kismet](../../07-kismet-wardriving/) (SMA extension)
- **No bulkhead consumers:** WROOM-32 (drone RemoteID) and both CYDs ride on PCB antennas —
  they cost zero bulkheads, so the panel stays at five.
- **Drilling + sealing:** all hole work and the IP67 seal strategy are shared with the
  [case-prep guide](../case-prep/); cooling fans and the membrane vent use the same marine
  silicone discipline.
- **Cable loss** at 15 cm is ~0.3 dB — negligible. Don't run longer than ~20 cm pigtails.
- **Field swaps:** because every radio terminates at an SMA bulkhead, you can swap a stubby
  for a 9 dBi mag-mount (wardriving) or a panel/Yagi (directional) without opening the case.

## Standalone Mode

**N/A** — the bulkhead panel is chassis infrastructure, not a board. It has no standalone
function of its own; it simply gives each board's radio a sealed external antenna. Pull any
board out of the deck and it reverts to its own onboard IPEX (snap the antenna straight to the
board) — see that board's guide for its standalone notes.

## Source / Upstream

- Full antenna design, routing, and waterproofing rationale: [projects/14-cyberdeck — §6 Antenna Management](../../../README.md#6-antenna-management)
- Antenna/adapter parts: [INVENTORY.md](../../../../../INVENTORY.md)
- Drilling + sealing the panel: [parts/case-prep](../case-prep/)
