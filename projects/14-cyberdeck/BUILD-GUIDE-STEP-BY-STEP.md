# Cyberdeck Build Guide — Parts That Come Together

A workbench-grade, start-to-finish build of a Raspberry Pi 5 cyberdeck assembled from your **owned fleet only**. The philosophy is "parts that come together": every module is flashed, bench-proven, and checked off **standalone** first, then the proven parts converge into the deck. Nothing gets mounted until it works on the desk — diagnosing a dead board inside a sealed case is ten times harder.

> **Scope note vs. the existing repo `BUILD-GUIDE.md`:** that document assumes some parts you don't currently have in working order (a live Pi Zero 2 W for RaspyJack, a VK-162 GPS, an Anker 347 specifically). This guide is rebuilt around the **fleet you actually own and the firmware you validated this session** (Marauder, Bruce, HaleHound, ESP32-DIV v1.1.0, GhostESP, BW16 Vampire Deauther, Meshtastic). Where this guide corrects the old one, it is called out inline. Treat this as the authoritative wiring/flash reference; fold the deltas back into the repo guide afterward.

**Legal:** WiFi deauth, BLE spoofing, IMSI-catcher work, IoT credential brute force, and Flock/ALPR detection are powerful. Only operate radios you are licensed/authorized to use, only attack networks/devices you own or have **written** authorization to test, and respect local RF law (deauth/jamming is illegal in many jurisdictions; the BW16 Vampire Deauther in particular can take down 5 GHz networks — bench-test it inside a Faraday bag or RF-quiet area).

---

## 0. The Fleet → Role Map (what each owned part becomes)

This is the master assignment. Everything below references it. Spares stay on the shelf.

| Owned part | Qty | Deck role | Firmware (validated) | RF out | IO |
|---|---|---|---|---|---|
| **Raspberry Pi 5 8GB** | 1 | **CORE** — brain, serial host, dashboard, Kismet | Kali / Pi OS | Panda PAU0F | 7" DSI |
| **Panda PAU0F (AXE3000)** | 1 | Kismet primary capture (2.4/5/6 GHz) | in-kernel mt7921u | own dual antennas | USB3 direct |
| **Lonely Binary ESP32 Gold #1** (WROOM-32E 16MB) | 1 | Marauder 2.4 GHz (WiFi/BLE attack) | **Marauder** | SMA #1 | CYD #1 (paired) |
| **Lonely Binary ESP32 Gold #2** | 1 | Flock ALPR detection (passive) | **Marauder** (`sniffbt -t flock`) | SMA #2 | — |
| **Lonely Binary ESP32 Gold #3** | 1 | BLE tracker / "chasing your tail" | **Marauder** BLE / Bruce | SMA #3 | — |
| **2× Waveshare ESP32-C5** (WiFi6 dual-band) | 2 | C5 #1 dual-band Marauder; C5 #2 GhostESP scanner | **Marauder C5** / **GhostESP** | SMA #4, #5 | headless |
| **3× BW16-Kit (RTL8720DN)** | 3 | Dual-band (2.4+5 GHz) deauth/recon node | **BW16 Vampire Deauther** | PCB / U.FL | headless AT-CLI |
| **ESP-WROOM-32** (bare) | 1 | Drone RemoteID scanner | Sky-Spy / Marauder | internal PCB | — |
| **LILYGO T-Display-S3** (ST7789) | 1 | Portable handheld tool (OUI-Spy / Bruce) | **Bruce** | internal | built-in 1.9" |
| **Heltec LoRa V3** (ESP32-S3 + SX1262) | 1 | Off-grid 915 MHz mesh comms | **Meshtastic** | SMA #6 (915) | 0.96" OLED |
| **2× CYD 2.8" (2432S028R, ILI9341)** | 2 | CYD #1 = Marauder display; CYD #2 = HaleHound | **HaleHound** / ESP32-DIV | internal / +modules | 2.8" touch |
| **AITRIP 4" ST7796** | 1 | Optional larger touch console (Bruce/ESP32-DIV) | **Bruce** / **ESP32-DIV v1.1.0** | internal | 4" touch |
| **7" Hosyond DSI** | 1 | Pi 5 primary display (lid-mounted) | — | — | DSI |
| **PiSugar** | 1 | **See §1 caveat** — not a Pi 5 auto-boot UPS | — | — | — |
| **NRF24L01 + adapters, OLEDs, 315/dual antennas, IPEX→SMA pigtails** | — | HaleHound add-on radios, status displays, RF I/O | — | SMA bulkheads | — |
| **Pi Zero 2 W** | 1 | **FRIED — out of scope** (RaspyJack deferred until replaced) | — | — | — |

**Two deltas you must internalize before buying screws:**
1. **The Pi Zero 2 W is fried** → there is **no RaspyJack** wired-attack node in this build. The wired-Ethernet pentest capability is the one gap; defer it or drop a working Zero 2 W in later (the bay is reserved in §3).
2. **PiSugar does not properly UPS a Pi 5.** The PiSugar S/S-Plus/2-Plus cannot auto-power-on the Pi 5 after a soft shutdown because of the Pi 5 boot-process change; only the **PiSugar 3 Plus** is Pi-5-rated ([PiSugar docs](https://docs.pisugar.com/docs/product-wiki/battery/pisugar-s-series), [PiSugar 3 Plus](https://www.pisugar.com/products/pisugar-3-plus-raspberry-pi-ups)). **Power the deck from a USB-C PD power bank**, and keep the PiSugar for a Pi Zero-class project. This guide powers the Pi 5 from a PD bank, not the PiSugar.

---

# PART A — Bench-Prove Every Part (do not skip)

Tools: a laptop with real **USB-C/micro-USB data cables** (verify data lines — charge-only cables are the #1 cause of "board won't flash"), Chrome/Edge (WebSerial flashers need them; Firefox/Safari won't work), Python 3.10+ with `esptool` (`pip install esptool`), an SD card reader, and your **Fluke 17B+**.

Universal ESP bootloader entry (memorize): **hold BOOT, tap RST, release BOOT.** If a flash stalls at "Connecting…", do this and retry; if it still fails, drop `--baud` to `115200`.

---

## Phase 1 — Enclosure + Power (the chassis the parts come into)

**Goal:** a sealed, thermally sane case and a single-battery power spine, so every part has a home and clean 5 V before it arrives.

### 1.1 Enclosure decision

Use a hard rugged case (Pelican 1300-class, as the repo already specs). The empty (no-foam) version is best — you fabricate plates. Drill plan (low-RPM step drill on polycarbonate — high speed melts/cracks it; deburr every hole so O-rings seat and cables don't get cut):

- **One side wall:** 6 IP67 SMA bulkheads in a row (SMA #1–#6) + intake/exhaust fan cutouts.
- **Front panel:** 7 SPST toggle holes (per-device 5 V cutoff) + a panel-mount USB-C **charge in** + a panel-mount USB-A **data out**.
- **Lid:** 7" DSI display window + a small fan.
- **Lower wall:** one ePTFE membrane vent (pressure equalize; blocks water/dust) — required because a sealed case + heat = condensation.

### 1.2 IPEX→SMA bulkheads — best practice (research-backed)

This is the single most-abused interface on a cyberdeck. Rules:

- **U.FL/IPEX is rated for only ~30–50 mating cycles** and tears its pad if abused; **SMA bulkheads survive 500+ cycles** ([data-alliance](https://www.data-alliance.net/blog/antenna-jacks-ufl-mhf4-rpsma-sma-add-upgrade-antenna-to-vastly-increase-range/), [nanovna-users thread](https://groups.io/g/nanovna-users/topic/u_fl_connector_mating_cycles/91082892)). So: snap the U.FL pigtail onto the board **once** and treat it as permanent; do all your swapping at the **external SMA** side.
- **Snap technique:** align the U.FL straight over the IPEX socket, press **straight down** until you feel a faint **click** (~20 N). **Never twist.** No click = don't force it ([tejte pigtail guide](https://tejte.com/blog/ufl-to-sma-pigtail-guide/)).
- **Keep pigtails short — under ~150 mm / 6"** — to limit loss, and **don't loop or kink** them (a loop radiates and couples EMI into the deck) ([tejte](https://tejte.com/blog/u-fl-to-sma-cable-guide/)). At 15 cm the loss is ~0.3 dB — negligible.
- **Bulkhead thread length:** match wall thickness — a plastic/polycarbonate case wall wants an **11–13 mm** bulkhead body ([tejte](https://tejte.com/blog/ufl-to-sma-pigtail-guide/)).
- Route pigtails **away from power/USB cables**; clip them down so they can't migrate onto a switching converter.

### 1.3 Power spine — single battery, two rails, per-device switching

Mirror the proven repo power architecture (it's sound):

- **Battery:** USB-C **PD power bank** (25,600 mAh / ≥30 W class). The Pi 5 peaks ~12 W and wants a clean 5 V/5 A feed; a 15 W (5 V/3 A) supply throttles downstream USB to 600 mA ([Raspberry Pi cooling/power notes](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/)).
- **Rail 1 (always on):** PD bank **USB-C → Pi 5** directly. No switch. Verify clean power later with `vcgencmd get_throttled` (`0x0` = good).
- **Rail 2 (switched):** PD bank **USB-A → powered USB hub** (strip its enclosure, mount the bare PCB). The hub's downstream ports feed every ESP/radio. **The hub upstream also runs back to a Pi USB port** so the Pi sees all serial devices.
- **Per-device cutoff:** one **SPST mini toggle per device, inline on the 5 V (red) wire only** — GND/D+/D- pass through unbroken. OFF = that device draws zero power and emits zero RF (this is your "stealth" capability). Use **waterproof boot caps** to keep the panel sealed.

```
PD bank ─USB-C(PD)──────────────────────────────► Pi 5   (always on)
        └USB-A──► powered hub ─┬─[5V cut][SW1]──► Gold #1 (Marauder)
                  (upstream to  ├─[5V cut][SW2]──► Gold #2 (Flock)
                   a Pi USB)    ├─[5V cut][SW3]──► Gold #3 (BLE)
                                ├─[5V cut][SW4]──► C5 #1
                                ├─[5V cut][SW5]──► C5 #2
                                ├─[5V cut][SW6]──► Heltec (Meshtastic)
                                └─[5V cut][SW7]──► BW16 node / WROOM-32
GND / D+ / D-  pass through every switch unbroken.
```

### 1.4 Power best-practice you must NOT violate — separate the PA rail

**Do not power a PA/LNA RF module (the NRF24L01+PA+LNA, or any Ebyte PA radio) from a display board's 3.3 V rail.** The CYD's onboard 3.3 V regulator cannot source the transmit current of a PA module — sharing it causes **brownouts, random resets, and failed radio init**. Power PA modules from an **independent 5 V→3.3 V buck converter** and run **only the signal lines** (SPI/CS/CE/IRQ) back to the ESP32 GPIOs ([CYD pinout + power notes, Random Nerd Tutorials](https://randomnerdtutorials.com/esp32-cheap-yellow-display-cyd-pinout-esp32-2432s028r/); [Mischianti CYD](https://mischianti.org/esp32-2432s028-cheap-yellow-display-high-resolution-pinout-datasheet-schema-and-specs/)). This matters specifically for the **HaleHound CYD #2 + NRF24L01+PA+LNA** combo in §5.

- Use a small **5 V→3.3 V buck** (not the breadboard linear 3.3 V — a PA module will sag it). Set/verify its output to **3.30 V** with the Fluke before connecting the radio.
- Tie all grounds common. Add a **bulk cap (100–470 µF) + 0.1 µF** across the PA module's 3.3 V/GND right at the module to absorb TX current spikes.

### 1.5 Thermal — the enclosed-Pi-5 trap

A Pi 5 in a sealed box becomes a heat-soaked thermal mass; the official guidance is explicit that an enclosed lid-on Pi 5 under load can't wick heat and cooks itself ([Raspberry Pi heating/cooling](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/)). Mitigations, in order:

1. **Active Cooler on the Pi 5 SoC** (firmware-managed: fan kicks at 60 °C, ramps at 67.5 °C, full at 75 °C). This is non-negotiable for a sealed deck.
2. **Standoff / plate clearance** so air circulates *under* the board and the cooler can actually move air — don't sandwich the cooler against a wall.
3. **Cross-flow case fans** (intake one wall, exhaust the opposite) + the **membrane vent** for pressure/condensation. Case fans are typically 12 V — feed them from a **5 V→12 V boost converter** off a spare USB-A tap; verify 12.0 V (±0.5) on the Fluke before connecting.

**Phase 1 checklist**
- [ ] Case drilled (6 SMA holes, 7 toggle holes, USB-C in, USB-A out, fan cutouts, membrane vent), all holes deburred
- [ ] IP67 SMA bulkheads installed + marine-silicone sealed; 24 h cure
- [ ] PD bank → Pi 5 (USB-C) and → hub (USB-A); hub upstream returns to a Pi USB port
- [ ] 7 SPST toggles wired inline on **5 V only**, boot caps fitted
- [ ] Pi 5 Active Cooler mounted; case fans on a verified 12 V boost rail; membrane vent in
- [ ] A separate **5 V→3.3 V buck** set to 3.30 V is on hand for the HaleHound PA module
- [ ] `vcgencmd get_throttled` → `0x0` on a bench boot

---

## Phase 2 — The Pi 5 Core (the part everything else plugs into)

**Board:** Raspberry Pi 5 8GB. **Boot media:** a 128GB card from your kit. **OS:** Kali Linux ARM (offensive tooling preinstalled) — or Pi OS if you prefer and `apt install` the tools.

### 2.1 Flash + first boot
1. Raspberry Pi Imager → Kali ARM (Pi 5) image → your 128GB card. Verify the drive letter (erases the target).
2. Boot with the **7" Hosyond DSI** + USB keyboard. Default Kali creds `kali`/`kali` → **`passwd` immediately**.
3. `sudo hostnamectl set-hostname cyberdeck`; join WiFi for updates: `sudo nmcli dev wifi connect "SSID" password "PW"`.

### 2.2 Core packages
```bash
sudo apt update && sudo apt full-upgrade -y && sudo reboot
sudo apt install -y kismet gpsd gpsd-clients python3-pip python3-venv \
  python3-flask screen tmux git esptool i2c-tools chromium aircrack-ng \
  bettercap nmap wireshark adb
pip install --break-system-packages pyserial flask flask-socketio meshtastic \
  gps3 luma.oled Pillow psutil
sudo systemctl enable --now ssh
```
Enable I2C (for the OLED later): `sudo raspi-config` → Interface → I2C → enable → reboot.

### 2.3 Panda PAU0F (Kismet primary)
- Plug the **PAU0F into a Pi USB 3.0 port directly — not the hub** (Kismet needs full bandwidth). It uses the in-kernel `mt7921u` driver ([USB-WiFi reference](https://github.com/morrownr/USB-WiFi)).
- Confirm: `iwconfig` shows a second `wlanX`. Monitor mode:
  ```bash
  sudo ip link set wlan1 down && sudo iw wlan1 set monitor none && sudo ip link set wlan1 up
  ```

**Phase 2 checklist**
- [ ] Kali boots on the 7" DSI; password changed; hostname `cyberdeck`
- [ ] `esptool version` (4.x), `kismet --version`, `python3 --version` (3.11+) all OK
- [ ] PAU0F enumerates on USB3, goes to monitor mode
- [ ] `vcgencmd get_throttled` → `0x0`

---

## Phase 3 — The ESP / Radio Node Bay (flash each, then it's a "part")

Flash and bench-prove each board **before** it enters the bay. Determine each board's chip first — it dictates the firmware variant and flash command:
```bash
esptool --port COM3 chip_id        # Windows
esptool --port /dev/ttyUSB0 chip_id  # Linux
```
Your Lonely Binary "Gold" boards are **classic WROOM-32E** (you confirmed this in inventory: WROOM-32E 16MB) → use the **ESP32 (WROOM)** firmware variant, **not** S3.

### 3.1 Gold #1 — Marauder 2.4 GHz (paired with CYD #1)
Classic-ESP32 Marauder, 4-file flash at the standard offsets:
```bash
esptool --chip esp32 --port /dev/ttyUSB0 --baud 921600 write_flash \
  0x1000 esp32_marauder.ino.bootloader.bin \
  0x8000 esp32_marauder.ino.partitions.bin \
  0xe000 boot_app0.bin \
  0x10000 esp32_marauder_v1_xx_esp32.bin
```
*(Use the WebSerial flasher at the Marauder site if you prefer GUI.)* Bench test over serial `screen /dev/ttyUSB0 115200`: `scanap` lists APs; `stopscan`. Snap the U.FL pigtail on **once** (→ SMA #1).

### 3.2 Gold #2 — Flock ALPR detection
Same Marauder flash as #1 (it's the same firmware family; Flock mode is a runtime command). Over serial: `sniffbt -t flock` → it scans 2.4 GHz for Flock OUIs; you'll only see hits near an actual ALPR camera. Pigtail → SMA #2.

### 3.3 Gold #3 — BLE tracker / chasing-your-tail
Marauder BLE (or Bruce if you want the richer BLE menu). Serial: confirm it streams nearby BLE MAC/RSSI as you walk a phone/AirTag past it. Pigtail → SMA #3.

### 3.4 C5 #1 / #2 — dual-band WiFi 6 (the 5 GHz backbone) ⚠ corrected flash
The ESP32-C5 is your **only 5 GHz-capable WiFi attack/scan radio**. **Critical correction over the old guide:** the C5 is **not** a single-bin-at-0x10000 flash, and its **second-stage bootloader lives at `0x2000`, not `0x0`/`0x1000`** ([Espressif esptool C5 flashing](https://docs.espressif.com/projects/esptool/en/latest/esp32c5/esptool/flashing-firmware.html)). This is the "C5 0x2000 gotcha." Full 4-file flash:
```bash
esptool --chip esp32c5 --port /dev/ttyUSB0 --baud 921600 write_flash \
  0x2000 bootloader.bin \
  0x8000 partition-table.bin \
  0xf000 ota_data_initial.bin \
  0x20000 esp32_marauder_<ver>_esp32c5_devkit.bin
```
- Use the binary marked **`_esp32c5_devkit.bin`** ([Marauder C5 wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/ESP32%E2%80%90C5%E2%80%90DevKitC%E2%80%901)). Offsets/extra bins vary by release — **read the release notes / use the provided `c5_flasher.py`**, which writes the exact map for that build. If unsure, run the project's flasher rather than hand-typing offsets.
- The C5 is **native-USB** (VID `303a`) — for bootloader mode use BOOT+RST as usual.
- **C5 #1 = Marauder** (dual-band attack): `scanap`, then `channel -s 36; scanap` to confirm 5 GHz networks appear that the Gold boards can't see. Pigtail → SMA #4, **Bingfu dual-band** antenna.
- **C5 #2 = GhostESP** (passive dual-band scan / Wireshark stream): flash the C5 GhostESP build, confirm scan output. Pigtail → SMA #5, dual-band antenna.

### 3.5 BW16 node — Vampire Deauther (dual-band 2.4+5 GHz) ⚠ different toolchain
The RTL8720DN is **not an ESP** — it does **not** use esptool. Flash with the **AmebaD image tool** (or the web flasher). You validated this firmware this session.
- **Use the 22-pin BW16 (the green-PCB 30-pin variant is known-bad)** ([BW16 troubleshooting](https://forum.amebaiot.com/t/resources-bw16-troubleshooting-guide/678)).
- Easiest path: the **Vampire web flasher** (Chrome/Edge, WebSerial, auto-download mode) at [vampel.github.io](https://vampel.github.io/) — it handles the Ameba image map for you.
- CLI path: `amebad_image_tool.exe COM_PORT` puts the chip in flash mode via RTS/DTR, loads the xmodem loader, erases from `0x08000000`, writes the image ([Ameba image tool notes](https://www.elektroda.com/news/news4130029.html)).
- Bench test: open the AT-style CLI over serial; confirm `2.4 GHz + 5 GHz` scan/target listing. Because this can **deauth 5 GHz**, test only against your own AP, ideally in an RF-quiet space or shielded bag.
- One BW16 goes in the bay (headless node); keep the other two as spares (you have 3).

### 3.6 Heltec LoRa V3 — Meshtastic ⚠ antenna-before-power
**Attach the 915 MHz antenna BEFORE powering or transmitting.** Keying the SX1262 with no antenna can permanently destroy the radio — this is the #1 killer of Heltec boards. You already validated Meshtastic here; reconfirm:
```bash
# Web flasher (flasher.meshtastic.org) → "Heltec WiFi LoRa 32 V3" → Latest Stable → Full Erase
meshtastic --port /dev/ttyUSB0 --set lora.region US
meshtastic --port /dev/ttyUSB0 --set-owner "CYBERDECK"
meshtastic --port /dev/ttyUSB0 --info   # confirm Region US, LONG_FAST
```
LoRa won't TX until the region is set (legal requirement). Pigtail/antenna → SMA #6 (915 MHz). OLED shows node status.

### 3.7 WROOM-32 (bare) — Drone RemoteID
Flash Sky-Spy (PlatformIO `pio run -e esp32dev -t upload`) or use Marauder's RemoteID. Internal PCB antenna is fine (RemoteID range is generous) → **no bulkhead**. Serial shows JSON drone records when a RemoteID-compliant drone is near.

**Phase 3 checklist**
- [ ] `chip_id` run on every board; firmware variant matches chip (Gold = classic ESP32)
- [ ] Gold #1/#2/#3 flashed (Marauder); `scanap`/`sniffbt`/BLE proven; U.FL snapped once each
- [ ] **C5 bootloader written at `0x2000`**; C5 #1 Marauder shows 5 GHz; C5 #2 GhostESP scans
- [ ] BW16 flashed via Ameba/web flasher (22-pin board); dual-band CLI proven in RF-quiet area
- [ ] Heltec: **antenna attached first**, Meshtastic region=US, `--info` clean
- [ ] WROOM-32 RemoteID boots and emits status

---

## Phase 4 — Antennas + RF (the sealed external interface)

**Goal:** every radio terminates at a sealed, swappable SMA on the case wall. Internal-PCB boards (WROOM-32, both CYDs, T-Display-S3, BW16-internal) consume **zero** bulkheads.

### 4.1 Bulkhead ownership (no collisions)
| Bulkhead | Owner | Antenna | Band |
|---|---|---|---|
| SMA #1 | Gold #1 (Marauder) | 2.4 GHz omni | 2.4 |
| SMA #2 | Gold #2 (Flock) | 2.4 GHz omni | 2.4 |
| SMA #3 | Gold #3 (BLE) | 2.4 GHz omni | 2.4 |
| SMA #4 | C5 #1 (Marauder) | Bingfu dual-band | 2.4/5 |
| SMA #5 | C5 #2 (GhostESP) | Bingfu dual-band | 2.4/5 |
| SMA #6 | Heltec (Meshtastic) | 915 MHz LoRa | 915 |
| *(opt)* SMA #7/#8 | HaleHound CC1101 / NRF24+PA | 315/433/915 whip; 2.4 duck | SubGHz / 2.4 |

### 4.2 Routing rules (apply §1.2 here)
1. Snap U.FL **straight down, once**, never twist; treat as permanent.
2. Pigtail run **< 6"**, no loops/kinks, 5 mm+ bend radius.
3. Pigtails **away from USB/power**; clip them.
4. Do **all** antenna swapping at the external SMA. Cap unused bulkheads with SMA dust caps (also keeps the seal flush).
5. **Panda PAU0F** keeps its own antennas — it's USB, not on a bulkhead (unless you run an SMA extension out a spare hole).

**Phase 4 checklist**
- [ ] 6 bulkheads owned 1:1 by their boards; pigtails snapped + routed short/clean
- [ ] External antenna on each; range improves vs. no-antenna (`scanap` sees more/farther APs)
- [ ] Dust caps on any unused bulkhead; seal intact after 24 h silicone cure

---

## Phase 5 — Displays + IO (the parts you actually look at)

**Goal:** mount and prove every screen. You own a deliberate mix; assign by role.

### 5.1 7" Hosyond DSI → Pi 5 (primary)
Lid-mounted via L-brackets/standoffs — **do not drill through the lid** (breaks the seal; use adhesive standoffs or partial-depth screws). Route the DSI FPC through the hinge gap, secure with **Kapton tape**, open/close the lid 10× to confirm the ribbon never pinches. This is the Kismet/dashboard console at 800×480.

### 5.2 CYD #1 → Gold #1 (Marauder display)
CYD #1 is the **touchscreen for Marauder** (Gold #1 does the RF; CYD shows the menu). Mount face-up. Already paired in §3.1.

### 5.3 CYD #2 → HaleHound (self-contained attack console)
Flash **HaleHound** (you validated it): web flasher at the HaleHound site, or `esptool --chip esp32 --port … --baud 921600 write_flash 0x0 HaleHound-CYD-FULL.bin`. Insert a micro-SD for loot. Touch menu: IoT Recon, WiFi (deauth/evil-portal), BLE, SubGHz/NFC if modules attached.
- **PA module power (the §1.4 rule in practice):** if you add the **NRF24L01+PA+LNA** to CYD #2, power it from the **separate 5 V→3.3 V buck**, not the CYD 3.3 V rail; run only SPI/CE/CSN/IRQ to the ESP32; bulk-cap at the module. Route its 2.4 GHz duck to optional SMA #8. The CC1101 (SubGHz) → optional SMA #7 (swap 315/433/915 whips externally).

### 5.4 LILYGO T-Display-S3 → Bruce (handheld, leaves the deck)
This is your **pocket tool**, not a fixed panel. Flash **Bruce** (validated): web flasher at [bruce.computer/flasher](https://bruce.computer/flasher), or esptool:
```bash
esptool --chip esp32s3 --baud 921600 --before default_reset --after hard_reset \
  write_flash -z --flash_mode dio --flash_freq 80m 0x0 bruce_tdisplays3.bin
```
(per [Bruce/LILYGO flashing refs](https://www.espboards.dev/esp32/lilygo-t-display-s3/)). Powers from the EEMB LiPo for field use; lives in the lid pocket.

### 5.5 AITRIP 4" ST7796 → optional big console (Bruce / ESP32-DIV v1.1.0)
Optional larger touch console if you want a roomier menu than the CYD — flash **Bruce** or **ESP32-DIV v1.1.0** (both validated) using the ST7796/TFT_eSPI profile. Skip if the two CYDs already cover your panels; it's a swap-in, not required.

### 5.6 Status OLED → Pi 5 (I2C vitals)
Wire a 1.3" SH1106 OLED to Pi I2C: VCC→3.3 V (pin 1), GND→pin 9, SDA→GPIO2 (pin 3), SCL→GPIO3 (pin 5). `i2cdetect -y 1` → device at **0x3C**. Drive it with `luma.oled` to show CPU temp / throttle / active tools.

**Phase 5 checklist**
- [ ] 7" DSI mounted, ribbon survives 10 lid cycles, Kali desktop visible
- [ ] CYD #1 shows Marauder menu (touch navigates); CYD #2 shows HaleHound + SD detected
- [ ] T-Display-S3 runs Bruce on LiPo (handheld)
- [ ] (opt) AITRIP 4" runs Bruce/ESP32-DIV; OLED shows at 0x3C
- [ ] Any PA radio is on the **separate buck**, never the CYD 3.3 V rail

---

# PART B — Bring It Together

## Phase 6 — Wiring + Bring-Up (parts become a system)

**Goal:** physical convergence — mount the proven parts, wire switches, bring up power.

### 6.1 Plates and layout
- **Base plate:** Pi 5 (+Active Cooler, on standoffs for under-board airflow), powered hub PCB, PD bank (Velcro), buck/boost converters.
- **Radio plate:** Gold #1–#3, C5 #1/#2, Heltec (OLED up), WROOM-32, BW16 node — ~12 mm between boards for airflow/cable routing; M2.5 standoffs.
- Leave enough slack that either plate can lift out **without unplugging anything**.

### 6.2 Switch wiring (5 V only)
Per §1.3: cut only the **red** wire, toggle inline, GND/D+/D- untouched, heatshrink each joint.

| SW | Device | Hub port |
|---|---|---|
| SW1 | Gold #1 (Marauder) | 1 |
| SW2 | Gold #2 (Flock) | 2 |
| SW3 | Gold #3 (BLE) | 3 |
| SW4 | C5 #1 | 4 |
| SW5 | C5 #2 | 5 |
| SW6 | Heltec (Meshtastic) | 6 |
| SW7 | BW16 node *(or WROOM-32)* | 7 |

Always-on (no switch): **Pi 5** (PD), **Panda PAU0F** (Pi USB3 direct). WROOM-32 and the BW16 share SW7 territory — if you want both switched independently, add an 8th toggle or chain a second small hub.

### 6.3 First power-up (staged)
1. All switches **OFF**. Power the PD bank.
2. Pi 5 boots Kali on the 7" DSI within ~30 s. `vcgencmd get_throttled` → `0x0`.
3. Flip switches **one at a time**, 5 s apart. After each: `lsusb` shows one new device; `dmesg | tail -20` is clean (no `over-current`/`disconnect`).
4. All on → every serial board enumerates; nothing browns out (if a board resets when its neighbor's radio TXes, you have a power/EMI problem — re-check the PA-rail rule and pigtail routing).

**Phase 6 checklist**
- [ ] Plates mounted; both removable with slack intact
- [ ] 7 toggles cut **5 V only**; each toggles its device in `lsusb`
- [ ] Pi 5 + Panda stay present regardless of any switch
- [ ] No undervoltage/over-current in `dmesg`; `get_throttled` `0x0` under load

---

## Phase 7 — Software / Firmware Load (the parts talk to the core)

**Goal:** stable device names, services, and a dashboard so the Pi orchestrates the bay.

### 7.1 Stable serial names (udev) — do this or you'll fight `ttyUSB` shuffle
Linux renames `ttyUSB*` per enumeration order. Pin each board with a udev symlink. The Gold/CYD boards use **CH340 (`1a86:7523`)** so they share VID:PID — differentiate by **physical hub port path** (`KERNELS`) or by serial. The C5s are native USB (`303a:1001`).
```bash
udevadm info -a -n /dev/ttyUSB0 | grep -E '{idVendor}|{idProduct}|{serial}|KERNELS'
sudoedit /etc/udev/rules.d/99-cyberdeck.rules
```
```
# CH340 boards differentiated by hub port (fix each board to one port)
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.1:1.0", SYMLINK+="marauder24", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.2:1.0", SYMLINK+="flock",      MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", KERNELS=="1-1.3:1.0", SYMLINK+="ble",        MODE="0666"
# C5 native-USB
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", KERNELS=="1-1.4:1.0", SYMLINK+="marauder5g", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", KERNELS=="1-1.5:1.0", SYMLINK+="scanner5g",  MODE="0666"
# Heltec (CP2102 10c4:ea60)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="meshtastic", MODE="0666"
```
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
ls -la /dev/marauder24 /dev/flock /dev/ble /dev/marauder5g /dev/scanner5g /dev/meshtastic
```

### 7.2 Services (auto-start, ordered)
- **Kismet:** `source=wlan1:type=linuxwifi` in `/etc/kismet/kismet.conf`; add user to `kismet` group; systemd unit `After=network.target`.
- **Dashboard:** a small Flask + Socket.IO app that opens each `/dev/<symlink>` at 115200 and streams lines to a 800×480 page; one systemd unit, Chromium `--kiosk http://localhost:5000` on the 7" DSI.
- **OLED monitor:** `luma.oled` script showing CPU temp / `get_throttled` / active tools; systemd unit.
(The repo `BUILD-GUIDE.md` Appendix C has working unit templates — reuse them verbatim; just swap the device list to match this fleet, and **drop the RaspyJack/Orbic/VK-162 services you don't have**.)

### 7.3 Fan control
Add to `/boot/firmware/config.txt`: `dtoverlay=gpio-fan,gpiopin=18,temp=55000` (case fan on at 55 °C). The SoC Active Cooler is firmware-managed automatically.

**Phase 7 checklist**
- [ ] Every board has a stable `/dev/<name>` symlink across reboots
- [ ] Kismet captures via PAU0F; dashboard auto-launches kiosk on the 7" DSI
- [ ] OLED shows live vitals; fans respond to temp
- [ ] No dangling services for absent hardware (RaspyJack/GPS/Orbic removed)

---

## Phase 8 — Final Integration + Test (prove the whole comes together)

### 8.1 Full power-on
All switches OFF → power on → Pi boots, dashboard loads, OLED live. Flip SW1→SW7 one at a time; confirm each device appears in `lsusb`/its symlink and the dashboard tab populates.

### 8.2 Sealed thermal soak (the make-or-break test)
Close the lid, all devices on, run **30 min**. Targets: **Pi 5 CPU < 70 °C**, `get_throttled` stays `0x0`, case warm-not-hot. If it climbs: confirm Active Cooler airflow isn't blocked, verify fan direction (intake→exhaust cross-flow), raise fan voltage, add the membrane vent if you skipped it. Re-soak after any change.

### 8.3 RF function pass (per band, RF-quiet first)
| Radio | Command/Action | Pass |
|---|---|---|
| Gold #1 (2.4) | `scanap` | APs listed, stronger with antenna |
| Gold #2 (Flock) | `sniffbt -t flock` | scanning active (hits only near ALPR) |
| Gold #3 (BLE) | BLE scan | nearby trackers/MACs stream |
| C5 #1/#2 (5 GHz) | `channel -s 36; scanap` / GhostESP | **5 GHz nets the Golds can't see** |
| BW16 | dual-band CLI vs. **your own** AP, shielded | 2.4+5 GHz target/scan works |
| Heltec (915) | `--sendtext` to a 2nd node | message delivered; **antenna on** |
| PAU0F | Kismet 2.4/5/6 GHz | networks captured |

### 8.4 Power-profile + runtime
Validate the modes (all-on ≈ 3 A; "stealth" = MAIN only, all ESP RF dead). Time a full-load run to empty to learn real runtime; record it on the quick-start card.

### 8.5 Weather pass (powered OFF)
Dust caps on, lid latched, spray each penetration 30 s/side, open, inspect for ingress. Re-seal/cure/retest any leak.

**Phase 8 checklist**
- [ ] Every switch maps to exactly one device that comes alive
- [ ] 30-min sealed soak: Pi 5 < 70 °C, `0x0`, no throttle
- [ ] Each band proven; C5 confirmed seeing 5 GHz; BW16 tested safely
- [ ] Power profiles work; runtime measured; stealth = zero ESP RF
- [ ] Water spray test passes; quick-start card laminated in the lid

---

## Appendix — Master Wiring Table (this fleet)

| Part | Bay | Power | Switch | SMA | Antenna | Display | Serial |
|---|---|---|---|---|---|---|---|
| Pi 5 8GB | core | PD bank USB-C | always | — | — | 7" DSI | — |
| Panda PAU0F | core | Pi USB3 direct | always | — | own duals | — | — |
| Gold #1 | radio | hub→SW1 | SW1 | #1 | 2.4 omni | CYD #1 | /dev/marauder24 |
| Gold #2 | radio | hub→SW2 | SW2 | #2 | 2.4 omni | — | /dev/flock |
| Gold #3 | radio | hub→SW3 | SW3 | #3 | 2.4 omni | — | /dev/ble |
| C5 #1 | radio | hub→SW4 | SW4 | #4 | dual-band | — | /dev/marauder5g |
| C5 #2 | radio | hub→SW5 | SW5 | #5 | dual-band | — | /dev/scanner5g |
| Heltec V3 | radio | hub→SW6 | SW6 | #6 | 915 LoRa | 0.96" OLED | /dev/meshtastic |
| BW16 node | radio | hub→SW7 | SW7 | (PCB/U.FL) | internal/2.4 | — | AT-CLI |
| WROOM-32 | radio | hub→SW7* | SW7* | internal | PCB | — | /dev/drone |
| CYD #2 (HaleHound) | console | hub (own SW) | opt | #7/#8 opt | PCB +PA on buck | 2.8" touch | /dev/halehound |
| T-Display-S3 | handheld | EEMB LiPo | — | internal | PCB | 1.9" | (removable) |
| AITRIP 4" | console (opt) | hub | opt | internal | PCB | 4" touch | — |

\*WROOM-32 and BW16 can't both sit on a single SPST cleanly — add an 8th toggle or a second tiny hub if you want independent cutoff for both.

## Open gaps (deliberate, from the owned fleet)
- **No wired-Ethernet pentest node** (RaspyJack) — the Pi Zero 2 W is fried. Bay reserved; drop a working Zero 2 W + USB-Ethernet + 1.44" LCD HAT in later.
- **No GPS** in fleet → Kismet/Flock wardriving runs without geotagging until you add a USB GPS (`gpsd` wiring is already in the repo guide).
- **No IMSI-catcher (RayHunter)** — no Orbic in the owned fleet; out of scope here.

---

### Sources
- [Random Nerd Tutorials — CYD ESP32-2432S028R pinout/power](https://randomnerdtutorials.com/esp32-cheap-yellow-display-cyd-pinout-esp32-2432s028r/) · [Mischianti CYD schema](https://mischianti.org/esp32-2432s028-cheap-yellow-display-high-resolution-pinout-datasheet-schema-and-specs/)
- [Raspberry Pi — heating & cooling the Pi 5](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/)
- [PiSugar S-series docs (Pi 5 limitation)](https://docs.pisugar.com/docs/product-wiki/battery/pisugar-s-series) · [PiSugar 3 Plus (Pi-5-rated)](https://www.pisugar.com/products/pisugar-3-plus-raspberry-pi-ups)
- [Data-Alliance — U.FL/MHF4/SMA mating cycles & range](https://www.data-alliance.net/blog/antenna-jacks-ufl-mhf4-rpsma-sma-add-upgrade-antenna-to-vastly-increase-range/) · [nanovna-users — U.FL cycle life](https://groups.io/g/nanovna-users/topic/u_fl_connector_mating_cycles/91082892) · [tejte — U.FL→SMA pigtail guide](https://tejte.com/blog/ufl-to-sma-pigtail-guide/)
- [Espressif esptool — ESP32-C5 flashing (bootloader @ 0x2000)](https://docs.espressif.com/projects/esptool/en/latest/esp32c5/esptool/flashing-firmware.html) · [Marauder ESP32-C5 DevKitC wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/ESP32%E2%80%90C5%E2%80%90DevKitC%E2%80%901)
- [Vampire Deauther BW16 web flasher](https://vampel.github.io/) · [BW16 troubleshooting (22-pin vs 30-pin)](https://forum.amebaiot.com/t/resources-bw16-troubleshooting-guide/678) · [Ameba image tool CLI](https://www.elektroda.com/news/news4130029.html)
- [Bruce firmware flasher](https://bruce.computer/flasher) · [LILYGO T-Display-S3 specs/flash](https://www.espboards.dev/esp32/lilygo-t-display-s3/)
- [morrownr USB-WiFi (PAU0F / mt7921u)](https://github.com/morrownr/USB-WiFi)