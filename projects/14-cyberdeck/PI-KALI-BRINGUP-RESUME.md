# RESUME — Pi 5 → Kali bring-up + session state (2026-06-12)

*Written before a PC restart so the next session picks up seamlessly. Read this top-to-bottom.
The **Pi/Kali bring-up** (Section 1) is the live, half-finished task — start there.*

---

## 1. LIVE TASK: get Kali on the Pi 5 + SSH in (where we stopped)

### Goal
Boot the Pi 5 headless on Kali and SSH into it from this PC, then install Cyber Controller on the
Pi and test flashing an ESP **through** the Pi (the cyberdeck-core flow). One ESP is to be left
connected to the Pi for that test; the other ESPs can be unplugged.

### Hardware / network facts
- **Pi:** Raspberry Pi 5 (8 GB, CanaKit kit). Powered by its **27 W USB-C PSU**.
  - Ports: **1× USB-C** (power **and** the only `dwc2` USB-gadget-capable port) · 2× USB-A (host only,
    cannot do gadget) · 1× built-in RJ45 Gigabit Ethernet.
  - **Pi 5 USB gotcha:** USB networking only works over the USB-C port — which is also the power input,
    and there's only one. So you either power+network over a single USB-C cable (PC USB-C → Pi USB-C,
    no PSU), or power via PSU and network another way (Ethernet/WiFi).
- **PC:** this box, IP **192.168.1.160**, internet via **"Ethernet 3"** (a Realtek USB-GbE dongle).
  Router **192.168.1.1**. Spare adapters present but disconnected: **"Ethernet"** (built-in PCIe RJ45),
  **"Ethernet 2"** (2nd USB-GbE dongle), **Wi-Fi** (RZ616, disconnected). The ICS "share to" dropdown
  offered Ethernet 2 / Local Area Connection / Wi-Fi (NOT the built-in "Ethernet").
- **Constraint the owner stated:** the only Ethernet is the PC's internet uplink — no free router port
  to wire the Pi to. So the Pi must reach the network via **WiFi** or **USB-gadget**, not a direct
  router cable.

### SD card — FULLY STAGED (Kali written + headless config)
Kali Linux ARM (`kali-linux-2026.x-raspberry-pi-arm64`) was written to the SD with Raspberry Pi
Imager. The FAT **BOOT** partition (shows as **drive `E:`** when the SD is in the USB reader on this
PC) was staged by me with all of these (verified):
- **`ssh`** — empty file, enables headless SSH on first boot.
- **`wpa_supplicant.conf`** — joins WiFi SSID **`KashPatel007`**. Contains BOTH password capitalizations
  (`Rebadolly2028` priority 2, `rebadolly2028` priority 1) so we don't have to guess. `country=US`.
- **`config.txt`** — appended under `[all]`: `dtoverlay=dwc2,dr_mode=peripheral` (USB-gadget).
- **`cmdline.txt`** — inserted `modules-load=dwc2,g_ether` right after `rootwait` (kept ONE line).
- Files were written UTF-8 **no-BOM** via `[System.IO.File]::WriteAllText` (the Edit tool can't do
  atomic writes on the FAT removable drive — `EPERM mkdir E:\`; use PowerShell for E: edits).

So the SD supports **both** paths: boot on PSU → WiFi, OR C-to-C cable → USB-gadget.

### What we tried + the result
- **WiFi attempt FAILED to appear.** Booted the Pi on the PSU; scanned `192.168.1.0/24` — only the
  router (`.1.1`), one unknown device (`.1.7`, MAC `50-7b-91-…`, not a Pi), and this PC (`.1.160`)
  answered. No Raspberry Pi OUI, no open port 22. So the Pi did not land on the LAN.
  - Likely causes (unconfirmed): **Kali may not honor a boot-partition `wpa_supplicant.conf`** the way
    Raspberry Pi OS does (that firstboot importer is an RPi-OS feature); OR still mid-first-boot
    (resize can take 3–5 min); OR `KashPatel007` is a different subnet than the PC's Ethernet.
- The owner has a **USB-C-to-USB-C cable** and a USB-C port on the PC. We were **about to switch to
  the C-to-C USB-gadget path** when the PC needed a restart.

### NEXT STEP (resume here) — C-to-C USB-gadget
1. **Unplug the PSU** from the Pi. Connect the **C-to-C cable: PC USB-C → Pi USB-C** (that one cable
   powers + networks it; may be slightly power-marginal from a PC port but fine for boot + SSH).
2. Within ~30–60 s of boot, a **new "USB Ethernet / RNDIS" adapter** appears in Windows
   (`ncpa.cpl` / `Get-NetAdapter`) — that confirms the Pi booted and the gadget is up.
3. Give the Pi an IP on that link: easiest is **ICS** — `ncpa.cpl` → right-click the **internet**
   adapter ("Ethernet 3") → Properties → Sharing → share to the **new RNDIS adapter** → the Pi gets
   `192.168.137.x`. (Or rely on link-local + `kali.local` if mDNS works.)
4. Find it: `arp -a` on `192.168.137.x`, or `ssh kali@kali.local`. Then **`ssh kali@<ip>`**.
5. **Default login: `kali` / `kali`** — change immediately (`passwd`) and regen host keys.
6. **Diagnostic if nothing happens:** check the Pi's **green LED** — blinking = alive/reading SD;
   solid-red-only/nothing = not booting (suspect power or the SD write / Pi 5 EEPROM, not the network).

### Tools already in place
- **Raspberry Pi Imager** installer downloaded to `<HOME>\Downloads\RaspberryPiImager-setup.exe`
  (used to write the SD).
- Scan helper used: a fast async ping sweep (`SendPingAsync`, 500 ms) over `192.168.1.0/24` + ARP-MAC
  match for Pi OUIs (`b8-27-eb|dc-a6-32|e4-5f-01|d8-3a-dd|2c-cf-67|28-cd-c1`) + `Test-NetConnection -Port 22`.
- **End state goal:** Kali on the Pi as the cyberdeck brain; the Panda PAU0F tri-band USB WiFi covers
  monitor-mode (Pi 5 Kali has no Nexmon on the internal radio).

---

## 2. What SHIPPED this session (done — for context)

- **BlueJammer-V2 → Cyber Controller — MERGED (PR #12, master `7508aba`).** Two flash profiles
  (`bluejammer-esp32` esptool `0x1000/0x8000/0x10000` NO boot_app0; `bluejammer-bw16` via the rtl8720
  AmebaD backend), closed-source v0.2 bins **SHA-256-pinned** + fetched at flash time (never vendored),
  `illegal-tx` label, telemetry-only protocol (no serial command channel), +10 tests, adversarially
  reviewed → SHIP. **Control finding:** BlueJammer has NO serial control — control is its BW16 web UI
  (`http://192.168.1.1`, AP `BlueJ-V2_by_@emensta`/`NoConn1337`), documented in `bluejammer_bw16.json`
  for a future gated launcher. CC flashes + reads telemetry only; it never keys the transmitter.
  **HW-validation pending the owner's PCBs** (ESP32-RF / WiFiX / C3Mini Elecrow boards + nRF24 + caps).
- **Cyberdeck roadmap** written: `projects/14-cyberdeck/CYBERDECK-ROADMAP-2026-06.md` (inventory-anchored,
  per-project, build order). And `VISION-ROADMAP.md` earlier.
- **Inventory reconciled** from order screenshots (the June haul). Deck is ~95% sourced. Still shipping:
  **2× CC1101** for FreqFoxRF (~Jun 23–30). Still to buy: **Pi Zero 2 W** (Pwnagotchi), optional REYAX
  **RYLR998** (ModuLoRa). 27 W PSU confirmed (CanaKit). Panda PAU0F tri-band = monitor-mode for the Pi.
- **Branding assets** received in `<HOME>\Downloads\attachments\` and cataloged (filenames are
  WRONG — see [[feedback_asset_implementation]]): `LxveAce Brand Pics.png` = LxveAce primary logo
  (purple spade); `Cyber Controller Logos.png` = the LxveAce **YouTube banner**; `hand drawn LxveAce
  Logo.jpg` = the **Cyber Controller green logo set**. Two identities: **LxveAce = purple ace-of-spades**,
  **Cyber Controller = green CC**. Branding/website work is DEFERRED to after the cyberdeck.
- **Emensta research:** design inspiration site = **`emensta.pages.dev`** (per-section animated CSS
  backgrounds, app-shell, mono "lab-instrument" identity). ⚠️ **AVOID `emenstastoolhub.pages.dev`** —
  it's a malware-tools storefront, ISP-blocked. Best non-jammer add from Emensta = **FreqFoxRF**
  (sub-GHz CC1101 multi-tool); also WiFiX dual-band deauther + ModuLoRa.
- **local-archive** (`github.com/LxveAce/local-archive`) = PRIVATE; holds Claude config (live creds —
  don't keep long-term) + useful scripts (`crop_logos.py`, `fix_html_logos.py`) + js/python toolboxes.
  Nothing critical missing from the live repos.
- (Overnight, prior) Cyber Controller **v1.1.0 released**; full 10-finding security audit closed; UI
  perf; fact-check. See `cyber-controller/docs/NIGHT-SESSION-2026-06-12.md`.

---

## 3. Next-steps queue (after the Pi is up)
1. **Finish Pi/Kali** (Section 1) → SSH in.
2. **Install Cyber Controller on the Pi** → test flashing the one connected ESP **through the Pi**
   (cyberdeck-core proof), reachable/observed from this PC.
3. When the **CC1101** arrives (~Jun 23–30): build **FreqFoxRF** (sub-GHz) + add a CC profile.
4. When the **BlueJammer PCBs** arrive + assembled: HW-validate the BlueJammer-V2 flash (both halves),
   and capture the BW16 web-UI HTTP endpoints to wire a gated in-app control panel.
5. **THEN** websites + branding: implement the real logo files (drop them in, don't recreate — see
   [[feedback_asset_implementation]]) + the Emensta-inspired revamp (purple LxveAce / green CC).

## 4. Standing rules (don't forget)
- Commit cyber-controller + Projects + websites as **`LxveAce <lxveace@proton.me>` only — NO Claude
  co-author**. Pushing is authorized.
- Projects repo: **add new files, don't edit originals**; keep `CLAUDE-TRANSFER.md` updated.
- Dangerous RF (jammers/deauth) = **label, never block**; BlueJammer is lab-only/illegal-to-operate,
  CC flashes-and-studies only.
- WiFi password for `KashPatel007` is staged on the SD's `wpa_supplicant.conf` (NOT written here — this
  doc is committed). Kali default `kali`/`kali`.
