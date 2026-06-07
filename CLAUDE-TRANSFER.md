# Claude Session Transfer Notes

**Last updated:** 2026-06-07
**Project:** `C:\Users\mmrla\Projects` (Security & Hardware Projects Repo)
**GitHub:** https://github.com/LxveAce/Projects (private)

---

## What Was Done This Session (2026-06-07)

### Cyberdeck Integration Guides — `projects/14-cyberdeck/integrations/`

Built a whole new `integrations/` tree under the cyberdeck that re-frames **every project
and every hardware subsystem** specifically for the deck build. Each guide is **decision-made**
(only the choice that was made for the deck — not the option-dumps the original project READMEs
carry) and **standalone-compatible** (every guide has a "Standalone Mode" section). Tone is a
short build-sheet: flash it, wire it, verify it.

**Structure chosen (with the user): `integrations/` subfolders, all 13 projects + 8 parts.**

```
projects/14-cyberdeck/
  README.md                         (UNTOUCHED — the master brainstorm)
  integrations/
    README.md                       (index + master wiring/decisions table)
    01-esp32-marauder/README.md     (EXEMPLAR — sets the template/style)
    02-flipper-zero/README.md
    03-pwnagotchi/README.md
    04-meshtastic/README.md
    05-rayhunter/README.md
    06-flock-drone-detection/README.md
    07-kismet-wardriving/README.md
    08-ble-detection/README.md
    09-project-nomad/README.md
    10-chasing-your-tail/README.md
    11-nyan-box/README.md
    12-usb-rubber-ducky/README.md
    13-esp-terminator/README.md
    parts/
      pi5-brain/README.md
      power/README.md
      cooling/README.md
      antennas/README.md
      displays/README.md
      gps/README.md
      case-prep/README.md
      dashboard/README.md
```

Each guide follows the exemplar's sections: header block → **The Decision** table → What You
Need → **Get It Running** (Flash/Build → Wire into deck → Verify) → Cyberdeck Compatibility
Notes → **Standalone Mode** → Source / Upstream. All cross-links are relative and verified to
resolve.

### Master wiring decisions (now pinned in `integrations/README.md`)

| Board / device | Slot | Power | Antenna | Display |
|---|---|---|---|---|
| Pi 5 | Brain | Anker 347 USB-C PD (always on) | — | 7" DSI |
| Gold #1 | Marauder | SW1 | SMA #1 | CYD #1 |
| Gold #2 | Flock | SW2 | SMA #2 | CYD #2 |
| Gold #3 | BLE + Chasing Your Tail | SW3 | SMA #3 | — |
| Heltec V3 | Meshtastic | SW4 | SMA #4 | onboard OLED |
| WROOM-32 | Drone RemoteID | SW5 | internal PCB | CYD #2 (shared) |
| Panda PAU0F | Kismet primary | Pi USB 3.0 (always on) | SMA #5 | — |
| RT5370 | Kismet secondary | SW6 | internal | — |
| VK-162 GPS | Shared GPS | SW7 | internal | — |

### Notable per-guide decisions made

- **Flipper Zero:** Flipper + **AWOK Dynamics Dual C5 Touch** WiFi add-on, **Momentum** firmware;
  docks/charges via deck USB, owns no SMA/switch (sub-GHz/RFID/NFC/IR is its unique value).
- **USB Rubber Ducky:** DIY path = **ESP32-S2 Mini + SuperWiFiDuck**; Hak5 listed only as upgrade.
- **Companions (not chassis-mounted):** RayHunter (runs on the Orbic itself), NyanBOX (own ESP32),
  Pwnagotchi (docked charge/offload bay — kept separate per design), Project Nomad
  (**blocked on ARM** — needs an x64 LattePanda; does NOT run on the Pi 5).
- **ESP Terminator** guide doubles as the deck's "which firmware on which board" flashing hub.

### HARDWARE-VERIFIED CORRECTION (2026-06-07, later) — Gold boards are CLASSIC ESP32, not S3

While flashing, the user's own boards proved the earlier "S3" claim WRONG. ESP Terminator's
auto-detect on **all three Gold boards** reports `Device: ESP32` (classic, CH340 converter,
16 MB flash) — and the `_multiboardS3.bin` firmware fails preflight
(`Firmware target (ESP32-S3) does not match detected chip (ESP32)`). The user successfully
flashed the **standard ESP32 (WROOM)** Marauder build. So:

- The three **Lonely Binary Gold** boards = **classic ESP32 (WROOM-class, CH340)**. Use the
  standard ESP32 Marauder build, "ESP32 Dev Module" in Arduino IDE, `--chip esp32`, bootloader
  at `0x1000`. The old `01-esp32-marauder/README.md` §12 ("ESP32-WROOM") was actually RIGHT.
- The **Heltec LoRa V3 genuinely IS an ESP32-S3** — that one is correct (flashed via Meshtastic's
  own web flasher anyway).
- All affected integration guides were re-corrected: `01-esp32-marauder`, `06-flock-drone-detection`,
  `08-ble-detection`, `13-esp-terminator`, the `integrations/README.md` index, and `parts/displays`.

### CYD vs Gold — they are TWO INDEPENDENT Marauders (corrected 2026-06-07)

The original design implied "CYD = serial display for the Gold." That's not how Marauder works —
it runs *on* the board it's flashed to. The CYD (ESP32 + screen on one PCB) is a **standalone
touchscreen Marauder**; the Gold is a **headless** Marauder (CLI over serial). They do NOT wire
together. A headless Gold's "screen" is the Pi's 7" dashboard. The Marauder + displays guides now
reflect this, including a "Does the Gold get its own screen?" section (Pi dashboard / standalone
CYD / advanced wired-TFT).

---

## Critical Discoveries (still valid)

1. **Lonely Binary ESP32 Gold is a CLASSIC ESP32** (WROOM-class, CH340, 16MB flash) — verified
   by esptool on all three boards 2026-06-07. **NOT an ESP32-S3.** Use the standard ESP32 Marauder
   build, NOT `_multiboardS3.bin`. (Earlier notes claiming S3 were wrong — see correction below.)

2. **Marauder has built-in Flock Sniff** — serial `sniffbt -t flock`. Gold #1 can cover Flock,
   so Gold #2 is kept dedicated only for flexibility (drop it and Marauder covers Flock).

3. **Pi 5 DSI uses a 22-pin connector** (not 15-pin like Pi 4). The Hosyond 7" display needs a
   22-to-15 pin adapter cable.

---

## What's Left / Future Work

- **Dashboard app:** Build the actual Flask + SocketIO dashboard (scaffold/protocols documented in
  `integrations/parts/dashboard/`, still not coded).
- **`temp_monitor.py`** for the 2.42" OLED (pattern in cooling/dashboard guides).
- **systemd services:** auto-start files (gpsd → kismet → dashboard).
- **Physical build:** follow the 9-phase plan in the cyberdeck README + the per-part guides.
- **Purchases still needed:** Pelican 1300 NF, IP67 SMA bulkheads + pigtails, Coolerguys IP67 fans,
  Noctua, VK-162 GPS, 2.42" OLED, Flipper Zero (+ AWOK Dual C5 Touch), Orbic RC400L, etc.
- **Optional:** mirror the corrected S3 firmware note back into the original `01` README if the
  "don't edit originals" rule is ever relaxed.

---

## Constraints / User Preferences

- **Commit as the user (LxveAce), NO Claude co-author** in git commits — the user wants the credit.
- **Do NOT edit the existing project READMEs or the cyberdeck `README.md`** — the integration guides
  are *new clones*, oriented to the deck; originals are the untouched reference library.
- **Decision-made, not option-dumps** — guides present the one choice per component, simply.
- **No Pwnagotchi** wired into the deck — kept separate (docked only).
- **No 3D printer** — acrylic, DIN rail, foam, L-brackets.
- **No Bluetooth keyboard** — wired only (BLE stealth).
- **Anker 347** = power bank. **Pelican 1300** = case.
- **Do NOT modify** `C:\Users\mmrla\Downloads\Barcode Label Gen` (original copy).

---

## Files Modified This Session

```
projects/14-cyberdeck/integrations/                     (NEW — 22 files: index + exemplar +
                                                          12 project guides + 8 part guides)
CLAUDE-TRANSFER.md                                       (this file)
```

No existing files were edited (verified via `git status` — only the new `integrations/` tree).
