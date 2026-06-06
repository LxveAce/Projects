# Claude Session Transfer Notes

**Last updated:** 2026-06-06
**Project:** `C:\Users\mmrla\Projects` (Security & Hardware Projects Repo)
**GitHub:** https://github.com/LxveAce/Projects (private)

---

## What Was Done This Session

### Cyberdeck Brainstorm (`projects/14-cyberdeck/README.md`)

Major rewrite of the cyberdeck brainstorm document. All sections updated:

1. **Case:** Pelican 1300 selected (~$85-100). Price updated, references added.
2. **Antenna Connections:** Full U.FL/IPEX guide added — step-by-step for each board. Waterproofing with IP67 SMA bulkheads + 3M Marine Silicone + dust caps.
3. **Displays:** 5 total — 7" DSI primary, 2x CYD 2.8" (Marauder + Flock/Drone), 2.42" SSD1309 OLED (system vitals), Heltec built-in OLED.
4. **Connectivity/Switching:** 7x SPST toggle switches with waterproof boot caps for per-device power control. USB hub architecture documented.
5. **Input:** Wired USB keyboard (Perixx PERIBOARD-409U) — BLE stealth, no Bluetooth advertising.
6. **Cooling:** 3-layer IP67-sealed system — 2x Coolerguys IP67 waterproof 40mm fans (intake/exhaust in walls), Noctua NF-A4x10 internal circulator, Amphenol VENT-PS1 membrane vent, thermal pads. Runs sealed.
7. **Mounting:** No 3D printer — acrylic plates (score and snap), DIN rail brackets, aluminum L-brackets, pick-and-pluck foam.
8. **Software Integration:** GPIO pin mapping (3-4 pins used, 22+ free, NO expander needed). USB port budget. Flask + SocketIO dashboard with UI layout. Serial protocols for all ESP32s. Firmware flashing guide for all 5 boards. GPS via gpsd.
9. **BOM:** Split into "Already Purchased" (17 items) and "Need to Get" (27 items) with Amazon links and descriptions. Total new parts: ~$340-420.
10. **Visual Diagrams:** 7 ASCII renderings — top-down base, lid interior, right wall (SMA + exhaust), left wall (intake + vent), front panel (switches), cross-section (airflow), antenna connection detail, wiring/power distribution.
11. **Build Phases:** Expanded to 9 phases with waterproofing, sealant curing, sealed thermal testing.
12. **Decision Matrix:** Updated with all new choices.

### Project Integration Sections Added

These project READMEs got new "Cyberdeck Integration" sections:

- `01-esp32-marauder/README.md` — Section 12: serial commands, flash instructions, standalone vs integrated
- `04-meshtastic/README.md` — Section 13: Heltec V3 on ESP32 rail, meshtastic-python API
- `06-flock-drone-detection/README.md` — Flock on Gold #2, Drone on WROOM-32, Marauder built-in Flock discovery
- `07-kismet-wardriving/README.md` — Section 12: Pi 5 native, Kismet REST API, GPS sharing
- `08-ble-detection/README.md` — Section 11: Gold #3, merged with Chasing Your Tail
- `10-chasing-your-tail/README.md` — Merges with BLE on Gold #3, GPS correlation

### Root README Updated

- `README.md` — Added row 14 (Cyberdeck) to project table

---

## Critical Discoveries

1. **Lonely Binary ESP32 Gold is ESP32-S3** (N16R8: 16MB Flash, 8MB PSRAM), NOT ESP32-WROOM-32. All firmware selections must use `_multiboardS3.bin` variants.

2. **Marauder has built-in Flock Sniff** — serial command `sniffbt -t flock`. Could potentially consolidate Gold #2 (dedicated Flock board) since Marauder on Gold #1 can do Flock detection. Current design keeps them separate for flexibility.

3. **Pi 5 DSI uses 22-pin connector** (not 15-pin like Pi 4). The Hosyond 7" display needs a 22-to-15 pin adapter cable.

---

## What's Left / Future Work

- **Dashboard app:** Build the actual Flask + SocketIO dashboard (architecture is designed, not coded yet)
- **Temperature monitoring script:** Write `temp_monitor.py` for the 2.42" OLED (code pattern in README)
- **systemd services:** Write auto-start service files for all components
- **Physical build:** Follow the 9-phase build plan
- **Repo refinement:** General polish of all 13 project READMEs (some still have standalone-only framing)
- **INVENTORY.md updates:** Quantity corrections, pinout images, best-fit hardware recs, antenna solutions (from memory file `projects-repo-updates.md`)

---

## Constraints / User Preferences

- **No Pwnagotchi** in the cyberdeck — kept separate
- **No 3D printer** — use acrylic, DIN rail, foam, L-brackets instead
- **No Bluetooth keyboard** — wired only (BLE stealth concern)
- **No Claude co-author** in git commits
- **Do NOT modify** `C:\Users\mmrla\Downloads\Barcode Label Gen` (original copy)
- **Anker 347** confirmed as the power bank
- **Pelican 1300** confirmed as the case

---

## Files Modified This Session

```
projects/14-cyberdeck/README.md          (major rewrite — all sections)
projects/01-esp32-marauder/README.md     (added cyberdeck integration section)
projects/04-meshtastic/README.md         (added cyberdeck integration section)
projects/06-flock-drone-detection/README.md (added cyberdeck integration section)
projects/07-kismet-wardriving/README.md  (added cyberdeck integration section)
projects/08-ble-detection/README.md      (added cyberdeck integration section)
projects/10-chasing-your-tail/README.md  (added cyberdeck integration section)
README.md                               (added cyberdeck row to project table)
CLAUDE-TRANSFER.md                       (this file)
```
