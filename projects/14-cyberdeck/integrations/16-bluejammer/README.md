# RF Interference Detection + nRF24 Research — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference:** [projects/16-bluejammer](../../../16-bluejammer/)
> **Deck role:** The **lawful, defensive** side of the BlueJammer threat model
> **Status:** Optional add — needs one nRF24 module

---

## The Decision

The deck **does not carry a jammer** — operating one is illegal (see below). What it integrates
instead is the **blue-team counterpart**: detect when *you* are being jammed, and do passive 2.4 GHz
research, using an **nRF24L01+** radio in **receive-only** mode.

| Question | Choice for the deck |
|----------|---------------------|
| **Capability** | 2.4 GHz **interference / jamming detection** + nRF24 RX research (Mousejack / Crazyradio class) |
| **Hardware** | 1× **NRF24L01+ (PA/LNA)** on a spare ESP32 (a [Gold](../01-esp32-marauder/) or the WROOM-32), 3.3 V + decoupling cap |
| **Firmware** | An nRF24 **RX scanner** (channel RSSI sweep) and/or [Mousejack](https://github.com/BastilleResearch/mousejack) research firmware — **never the jammer** |
| **Power / data** | Hub → a toggle; serial to Pi 5 (115200) → dashboard alerts |
| **Explicitly excluded** | Any transmit/jamming mode — illegal to operate |

> **Note:** if you build the [ESP32-DIV](../15-esp32-div/), its **2.4 GHz Scanner** already gives you
> the interference view — this standalone nRF24 is for a *dedicated* always-on detector and for the
> Mousejack/Crazyradio research the deck otherwise can't do. The deck already sees 5 GHz via the
> Panda + Kismet, so no BW16 board is needed.

---

## What You Need

- **NRF24L01+ PA/LNA** module (+ a 3.3 V base adapter / 10 µF decoupling cap — these modules are
  power-noise sensitive).
- A spare ESP32 (own one already) with free SPI pins.
- 2.4 GHz antenna (the PA/LNA module is SMA — use a spare deck antenna).

---

## Get It Running

### 1. Wire the nRF24 to the ESP32 (SPI)
Typical mapping (the firmware defines exact pins — match it):

| nRF24 | ESP32 |
|-------|-------|
| VCC | 3.3 V (with decoupling cap / base board) |
| GND | GND |
| CE | GPIO4 |
| CSN | GPIO5 |
| SCK | GPIO18 |
| MOSI | GPIO23 |
| MISO | GPIO19 |
| IRQ | (optional) |

### 2. Flash a **receive** firmware (never the jammer)
- **Interference detector:** an nRF24 "2.4 GHz scanner" sketch sweeps all 126 channels reading the
  carrier-detect/RSSI bit — a sustained raised floor across many channels = jamming/heavy congestion.
- **Mousejack / Crazyradio research:** [BastilleResearch/mousejack](https://github.com/BastilleResearch/mousejack)
  + [nrf-research-firmware](https://github.com/BastilleResearch/nrf-research-firmware) to discover/sniff
  vulnerable wireless keyboard/mouse dongles (passive).

### 3. Wire into the deck
- Mount the ESP32 on the ESP32 plate; power via the [hub + a toggle](../parts/power/); 2.4 GHz antenna
  on a spare bulkhead ([antennas](../parts/antennas/)).
- Serial to the Pi 5; the [dashboard](../parts/dashboard/) raises an **alert when the 2.4 GHz noise
  floor spikes** — i.e. you're likely being jammed.

---

## Cyberdeck Compatibility Notes

- **Pure RX — lawful.** This extends the deck's existing detection posture: deauth detection
  (Marauder `sniffdeauth`), [Drone RemoteID detection](../06-flock-drone-detection/), and
  [stingray detection](../05-rayhunter/). "Know when you're being jammed" rounds it out.
- **No transmit, ever.** Do not flash or run BlueJammer or any jamming firmware on deck hardware —
  it's illegal (47 U.S.C. §333 / FCC) and would knock out the deck's own WiFi/BLE/GPS.
- **Overlap:** the [ESP32-DIV](../15-esp32-div/) 2.4 GHz Scanner covers the detection view too; this
  is the dedicated/always-on + Mousejack option.

## Standalone Mode

Runs on any ESP32 + nRF24 on a bench — a self-contained 2.4 GHz interference monitor / Mousejack
research rig, independent of the deck.

## Source / Upstream

- Threat model / reference: [projects/16-bluejammer](../../../16-bluejammer/) · [BlueJammer-V2](https://github.com/EmenstaNougat/BlueJammer-V2) (jammer — reference only)
- Research firmware: [Mousejack](https://github.com/BastilleResearch/mousejack), [nrf-research-firmware](https://github.com/BastilleResearch/nrf-research-firmware)
