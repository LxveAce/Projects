# Case Prep — Pelican 1300 NF Chassis (Drill / Seal / Mount)

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Full reference (all options):** [projects/14-cyberdeck README §3, §10, Phases 2–3](../../../README.md)
> **Deck role:** The bare chassis — every penetration and mounting plate the other parts depend on
> **Status:** First physical build step (do this before any board goes in)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Case** | Pelican **1300 NF** (No Foam), IP67 |
| **Why this case** | 1200 footprint + 1.7" more height (internal 9.2 x 7.0 x 5.8") — fits the Pi 5 + hub + power bank stack with room to route cable |
| **Drilling** | Step drill bit on polymer, slow (no heat), deburr every hole |
| **Penetrations** | 5× SMA bulkhead · 2× 40 mm fan · 7× toggle switch · 1× panel-mount USB-C · 1× membrane vent |
| **Waterproofing** | IP67 bulkheads + **3M Marine Grade Silicone** around every penetration, cure 24 h |
| **Mounting (no 3D printer)** | 3 mm acrylic plates, score-and-snap, on brass standoffs; DIN rail for ESP32s; L-brackets for lid display |
| **Foam** | NF case = empty; pick-and-pluck **only** for the battery bay |

> **Why NF (No Foam) over a foam-filled 1300:** the deck mounts everything on rigid plates,
> not in foam. Buying the NF version skips paying for pick-and-pluck you'd rip out anyway —
> a small block of foam for the battery cradle is all that's wanted, and foam **insulates
> heat**, so it never goes near the Pi 5 or ESP32 rail.

> **Critical:** every hole breaks the IP67 seal. The rating is only restored by IP67-rated
> bulkheads/fans/vent **plus** marine silicone at each penetration — and only after a full
> **24-hour cure**. Don't water-test or seal the lid on uncured sealant.

---

## What You Need

- Pelican **1300 NF** case (IP67)
- 3 mm clear acrylic sheet (~$5–8) — yields both plates
- Acrylic scoring tool (~$5), steel ruler, marker, bench clamp
- **Step drill bit** (e.g. 4–20 mm Unibit) + cordless drill, low RPM
- Deburring tool or fine sandpaper
- M2.5 brass standoffs + screws (base + ESP32 plates)
- 35 mm DIN rail segment (~7" cut) + PCB support clips — *optional ESP32 mount*
- Aluminum **L-brackets** (pack, ~$3–5) + M3 bolts — for the lid display
- **3M Marine Grade Silicone Sealant** (clear, ~$8)
- IP67 SMA bulkheads with O-rings ×5 *(consumed by the [antennas guide](../antennas/))*
- IP67 40 mm fans + neoprene gasket *(consumed by the [cooling guide](../cooling/))*
- SPST toggle switches with waterproof boot caps ×7 *(consumed by the [power guide](../power/))*
- Panel-mount USB-C pass-through (1)
- Amphenol VENT-PS1 ePTFE membrane vent (1)
- Small foam block for the battery bay (pick-and-pluck offcut or craft foam)

---

## Get It Running

### 1. Mark and drill all holes

Remove any foam first (NF case ships empty). Mark, then drill — measure twice.

| Penetration | Count | Location | Tool |
|-------------|-------|----------|------|
| SMA bulkhead | 5 | Right wall, evenly spaced | Step drill to bulkhead OD |
| 40 mm fan cutout | 2 | Left wall (intake) + right wall (exhaust) | Step drill + file to square |
| Toggle switch | 7 | Front panel, in a row | Step drill to switch thread |
| Panel-mount USB-C | 1 | Front panel | Step drill to connector |
| Membrane vent | 1 | Bottom/top wall, away from fans | 6 mm hole (VENT-PS1) |

1. Mark every hole with a marker; centre-punch lightly so the bit doesn't wander.
2. Drill with the **step drill at low RPM** — let the bit cut, don't force it. Polymer melts
   if you run hot, so pause to let it cool.
3. **Deburr** every hole inside and out with the deburring tool or fine sandpaper — a clean,
   round, burr-free edge is what lets the O-rings and sealant seat properly.

### 2. Install and seal every penetration (then cure 24 h)

1. Seat the **IP67 SMA bulkheads** with their O-rings — hand-tighten plus ~1/4 turn with a wrench.
2. Mount the **IP67 fans** with neoprene gaskets (intake left, exhaust right).
3. Fit the **7 toggle switches** with their waterproof boot caps.
4. Fit the **panel-mount USB-C** pass-through.
5. Fit the **Amphenol VENT-PS1** membrane vent in its 6 mm hole.
6. Run a ring of **3M Marine Grade Silicone** around **every** penetration — bead on the
   inside, push the part through, bead on the outside flange, tighten so sealant squeezes
   into the gaps. Wipe excess with a damp cloth.
7. **Let it cure a full 24 hours** before any water exposure or before closing the lid on it.

### 3. Cut the acrylic plates (score-and-snap)

Two plates, both from the one 3 mm sheet:

- **Base plate** — ~**8.5" × 6.5"** (Pi 5 + USB hub + power bank)
- **ESP32 plate** — ~**6" × 4"** (all ESP32 boards)

1. Mark the cut line with ruler and marker.
2. Score 10+ passes along the line with the scoring tool.
3. Clamp to the table edge at the score line.
4. Snap downward — clean break.
5. Drill M2.5 / M3 mounting holes at **low RPM** (high speed cracks acrylic); mark hole
   positions off the actual component/standoff footprints.

### 4. Mount rails and brackets

- **Base + ESP32 plates:** fit **brass standoffs** into the drilled holes — boards bolt to
  these, lifting them off the plate for airflow.
- **ESP32 rail (optional):** mount the **35 mm DIN rail** segment and clip the ESP32s on via
  DIN clips/breakouts instead of (or alongside) standoffs.
- **Lid display:** bolt **aluminum L-brackets** into the lid with M3, screw the 7" display to
  the brackets, and leave the hinge gap clear for the DSI ribbon. Use short standoffs /
  adhesive backing so you **don't drill through** the lid and break its seal.
- **Battery bay:** drop the small foam block in the bottom layer and pluck a snug cavity for
  the power bank. Foam here only — never under heat-producing boards.

### 5. Verify fit

- Test-fit both plates: they should rest on the case's internal ribs or on foam strips, level
  and not rocking.
- Dry-fit a board on each plate to confirm standoff/DIN spacing before final assembly.
- Confirm every bulkhead, switch, fan, USB-C, and the vent is solid and square in its hole.
- After the 24 h cure, the chassis is ready for the compute layer and the part guides below.

---

## Cyberdeck Compatibility Notes

This guide *produces the holes and plates the other part guides consume.* It owns the chassis;
they own what goes in it.

- **[Antennas](../antennas/):** claims the **5× SMA bulkhead** holes drilled here; routes each
  ESP32's U.FL pigtail to its bulkhead. Bulkhead-to-radio assignments live in that guide.
- **[Cooling](../cooling/):** claims the **2× 40 mm fan cutouts** + the **membrane vent** hole;
  this guide just cuts and gasket-seals them. Fan power/PWM wiring is in the cooling guide.
- **[Power / switches](../power/):** claims the **7× toggle-switch** holes + the panel-mount
  USB-C; switch-to-device mapping (SW1–SW7) is in the power guide.
- **[Displays](../displays/):** mounts the 7" DSI to the **lid L-brackets** installed here, and
  the CYD/OLED panels to the acrylic plates.
- **Plate budget:** base plate carries Pi 5 + hub + power bank; ESP32 plate carries the radio
  rail. Boards from every other guide bolt to these two plates (or the DIN rail).
- **Seal discipline:** any guide that adds a *new* penetration later must re-seal with marine
  silicone and re-cure 24 h, or the IP67 rating is lost.

## Standalone Mode

**N/A.** This is the chassis-prep step, not a runnable subsystem — there's no board or
firmware to run on its own. The "standalone" payoff is structural: a sealed, drilled, plated
Pelican 1300 that every other part guide drops into. It is a hard dependency for the
[antennas](../antennas/), [cooling](../cooling/), [power](../power/), and [displays](../displays/)
guides — do this first.

## Source / Upstream

- Case + mounting decisions: [Project 14 README — §3 Form Factor, §10 Modularity, Build Phases 2–3](../../../README.md)
- Exact parts: [INVENTORY.md](../../../../../INVENTORY.md)
- Reference builds: Jay Doscher [Recovery Kit v2](https://doscher.com/recovery-kit-version-2/) (Pelican 1300) · Jake Simek [Pelican-Deck](https://github.com/Jake-Simek/Pelican-Deck)
