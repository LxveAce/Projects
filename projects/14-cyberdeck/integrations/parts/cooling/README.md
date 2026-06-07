# Cooling — 3-Layer Sealed System — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Full reference (all options):** [projects/14-cyberdeck — Section 9 Cooling](../../../README.md)
> **Deck role:** Cool a SEALED Pelican 1300 NF without breaking IP67
> **Status:** Ready to build (fans + heatsinks + vent in inventory)

---

## The Decision

A sealed Pelican 1300 with a Pi 5 + 5 ESP32s + power bank makes ~21W peak (~12W typical) of
heat. The Pi 5 throttles at **85C** — opening the case to vent it defeats IP67. So the deck
cools the internals **without breaching the seal**, using three layers. Target: **<70C** SoC.

| Question | Choice for the deck |
|----------|---------------------|
| **Layer 1 — wall fans** | 2× **Coolerguys CG4010M12-IP67** waterproof 40mm (intake one wall, exhaust opposite) |
| **Fan power** | **12V**, from the 5V→12V boost converter in the [power guide](../power/) |
| **Fan sealing** | Neoprene gasket + 3M marine silicone at each mount |
| **Layer 1b — circulator** | **Noctua NF-A4x10 5V** internal, blowing across the Pi 5 heatsink |
| **Circulator control** | PWM on **GPIO18**: `dtoverlay=gpio-fan,gpiopin=18,temp=55000` |
| **Layer 2 — conduction** | Pi 5 aluminum heatsink + thermal pads bridging to the case wall; adhesive heatsinks on each ESP32 |
| **Layer 3 — vent** | **Amphenol VENT-PS1** ePTFE membrane vent (IP69K) for pressure / condensation control |

> **Why all three:** sealed + no cooling hits ~75-90C and **throttles**. Sealed + fans +
> thermal pads + membrane vent holds the SoC at ~50-60C — well under the 85C throttle and
> below the <70C target — while keeping IP67 intact.

> **Critical:** the Coolerguys fans are **12V**. They run off the 5V→12V boost converter, not
> a hub port. The Noctua is **5V-native** and stays inside (it doesn't need to be waterproof).

---

## What You Need (from the repo inventory)

- 2× Coolerguys CG4010M12-IP67 waterproof fans (40×40×10mm, 12V, IP67, dual ball bearing)
- Noctua NF-A4x10 5V internal circulator fan
- 5V-to-12V DC boost converter (powers the IP67 fans — shared with the [power guide](../power/))
- Pi 5 aluminum heatsink (e.g. Geekworm H509)
- Thermalright thermal pads (120×120×3mm, 12.8 W/mK)
- Adhesive ESP32 heatsinks (9×9×5mm, 20-pack)
- Neoprene gasket sheet (12"×12") + 3M marine silicone
- Amphenol VENT-PS1 ePTFE membrane vent
- See [INVENTORY.md](../../../../../INVENTORY.md) for exact line items

---

## Get It Running

### 1. Mount the wall fans and seal them

1. Cut two **40mm** fan openings in opposite walls — intake low on one wall, exhaust high on
   the other (cross-ventilation). Drilling/cutout layout is in the [case-prep guide](../case-prep/).
2. Cut neoprene gaskets to the fan footprint; sandwich one between each fan and the case wall.
3. Bed each fan in **3M marine silicone**, screw down, and fillet the perimeter. This keeps
   IP67 at the cutout.
4. Orient airflow: one fan pulls air **in**, the opposite fan pushes it **out**.

### 2. Heatsinks and thermal pads (conduction to the case)

1. Bolt the **aluminum heatsink** directly to the Pi 5 SoC.
2. Bridge the Pi 5 heatsink to the nearest case wall with a **2-3mm thermal pad** so heat
   conducts into the chassis.
3. Stick an **adhesive heatsink** on each ESP32 module (and the Heltec LoRa V3).

### 3. Membrane vent (pressure / condensation)

1. Drill a small **6mm** hole on the top/bottom wall, away from the fans.
2. Install the **Amphenol VENT-PS1** ePTFE membrane vent. It lets gas/pressure equalize slowly
   during temperature swings — preventing seal stress and condensation — while staying IP69K.

### 4. Fan control and monitoring

**Noctua PWM (GPIO18):** add to `/boot/config.txt` so the circulator ramps with temperature
(ties into the [pi5-brain guide](../pi5-brain/) GPIO map — Pin 4 = +5V, Pin 9 = GND, Pin 12 = PWM):
```
dtoverlay=gpio-fan,gpiopin=18,temp=55000
```

**IP67 fans:** wire through a toggle/MOSFET on the Pi 5 GPIO — full speed when the case is
sealed, off when the lid is open.

**Thermal monitor** — add to `/etc/cron.d/thermal-monitor` on Kali:
```bash
#!/bin/bash
TEMP=$(vcgencmd measure_temp | grep -oP '[0-9.]+')
if (( $(echo "$TEMP > 78" | bc -l) )); then
    # Throttle warning — reduce workload or open lid
    echo "THERMAL WARNING: ${TEMP}C" | wall
fi
```

### 5. Verify (sealed thermal test)

Close the case, run all devices for **30 minutes**, and watch the SoC temp:
```bash
watch -n 2 vcgencmd measure_temp
```
Sealed + fans + pads + vent should settle around **~50-60C** (target <70C). If it climbs:
increase fan speed, add thermal pads, or add a second membrane vent.

---

## Cyberdeck Compatibility Notes

- **Power rail:** the IP67 fans are **12V** and draw from the 5V→12V boost converter documented
  in the [power guide](../power/) — they do **not** use a hub toggle port. The Noctua draws 5V
  from the Pi header.
- **Case prep:** the two 40mm fan cutouts, the 6mm vent hole, and their gasket/silicone sealing
  are part of the [case-prep guide](../case-prep/) drilling plan — do them together to keep IP67.
- **GPIO:** Noctua PWM speed control lives on **GPIO18 (Pin 12)**, +5V on Pin 4, GND on Pin 9 —
  see the [pi5-brain guide](../pi5-brain/) header map; no conflict with other subsystems.
- **Thermal budget:** ~12W of the ~21W peak is the loaded Pi 5; that component gets the
  heatsink + thermal pad + direct Noctua airflow, which is why it stays under the 85C throttle.

## Standalone Mode

N/A — cooling is a chassis-level subsystem, not a removable board. It exists only to keep the
sealed deck under throttle temps; there is nothing to run on a bench by itself. If you ever
operate the deck lid-open, the IP67 fans can be switched off (natural convection handles it).

## Source / Upstream

- Full design, thermal budget, expected temps, wiring: [projects/14-cyberdeck — Section 9 Cooling](../../../README.md)
- Coolerguys CG4010M12-IP67 fans, Noctua NF-A4x10, Amphenol VENT-PS1 — see [INVENTORY.md](../../../../../INVENTORY.md)
