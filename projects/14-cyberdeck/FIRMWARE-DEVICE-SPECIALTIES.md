# Firmware x Device Specialties — The Field Dossier

> Deep, web-researched specialties for every security firmware in the fleet and the EXACT
> owned boards each runs on. Companion to `FIRMWARE-REFERENCE.md` (this goes deeper on the
> *why* and the device fit). Each section cites upstream sources; open questions are flagged
> at the end for hardware verification. Built to be actionable in the field.

## Quick-pick matrix

| Firmware | Best chip | Unique specialty | Owned-board fit (short) |
|---|---|---|---|
| ESP32 Marauder (justcallmekoko/ESP32Mara... | Classic ESP32 (WROOM-32) — the only chip... | Flock Safety ALPR camera detection (Flock Sniff / Flock Wardrive) — a combined BLE+WiFi si... | RUNS GREAT (full WiFi+BLE): 3x Lonely Binary ESP32 Gold + ESP-WROOM-32 dev board (headless... |
| Bruce (BruceDevices/firmware, formerly p... | ESP32-S3 overall; uniquely also ESP32-C5... | The only firmware in the fleet that is a true Flipper-Zero-class multi-band signals handhe... | BEST FITS (owned): (1) CYD 2.8" ESP32-2432S028R x2 — first-class `CYD-2432S028` merged-bin... |
| GhostESP (GhostESP-Revival fork) | ESP32-S3 (richest feature set + display/... | Real 2.4 GHz AND 5 GHz dual-band WiFi work on ESP32-C5/C6 silicon — 5 GHz AP scanning, war... | RUNS ON, mapped to owned boards: (1) ESP32-C5 x2 (Waveshare WiFi6) — flagship fit, `ACE_C5... |
| HaleHound-CYD | Classic ESP32 (ESP32-WROOM / ESP32-D0WD)... | Guardian / Jam-Detect — a persistent, multi-band defensive blue-team mode (WiFi Guardian +... | Runs natively and "Fully Tested" on the user's 2x CYD 2.8" ESP32-2432S028R (ILI9341 + XPT2... |
| ESP32-DIV (cifertech/ESP32-DIV) | ESP32-S3 | A single touchscreen handheld that fuses 3x NRF24 (2.4 GHz spectrum/proto-kill) + CC1101 s... | Best fit for an OWNED board: LILYGO T-Display-S3 or Heltec LoRa V3 (both ESP32-S3) chip-wi... |
| Meshtastic (meshtastic/firmware) | ESP32-S3 + Semtech SX1262 (your Heltec W... | It is the ONLY firmware in your fleet that does true long-range, internet-independent LoRa... | RUN IT ON: Heltec LoRa V3 (ESP32-S3 + SX1262 915MHz) — perfect, first-class supported, use... |
| BW16 Vampire Deauther (vampel) — AT+ CLI... | Realtek RTL8720DN (AmebaD / RTL872xDx) —... | Real 5GHz (and 2.4GHz) WiFi deauthentication driven entirely over a plain 115200-baud AT+ ... | Runs ONLY on your 3x BW16-Kit (Realtek RTL8720DN, AmebaD). It is AmebaD/RTL872xDx firmware... |
| Flock-You (colonelpanichacks/flock-you) | ESP32-S3 (specifically the Seeed Studio ... | It is the only firmware in the fleet purpose-built as a Flock Safety / SoundThinking ALPR ... | Closest owned fit: LILYGO T-Display-S3 or Heltec LoRa V3 (both ESP32-S3, USB-native CDC) —... |
| OUI-Spy (OUI-SPY Unified Blue + standalo... | ESP32-S3 (specifically the Seeed Studio ... | Concurrent, purpose-built surveillance-infrastructure detection: it ships a curated heuris... | Best fit: LILYGO T-Display-S3 (ESP32-S3) — it is the ONLY owned board with the required ES... |
| Sky-Spy (colonelpanichacks/Sky-Spy) | ESP32-S3 (Seeed XIAO ESP32-S3) for the m... | It is the only firmware in the fleet that passively detects and decodes drone Remote ID (O... | PRIMARY (best, dual-band): 2x Waveshare ESP32-C5 -> flash the xiao-c5-5g/ sub-project (boa... |
| AirTag Scanner (MatthewKuKanich/ESP32-Ai... | Classic ESP32 (WROOM-32) — bare-metal BL... | It is a purpose-built, zero-UI Apple FindMy/AirTag BLE beacon sniffer that prints MAC + RS... | Runs best on the 4x classic ESP32 boards you own — the 3x Lonely Binary ESP32 Gold (WROOM-... |
| Minigotchi-ESP32 (dj1ch/minigotchi-ESP32... | Classic dual-core ESP32 (ESP32-WROOM-32 ... | Pwnagotchi-peer participation: it advertises and detects on the Pwnagotchi/Minigotchi/Paln... | Best fit: the 3x Lonely Binary ESP32 Gold (WROOM-32E, 16MB) and the ESP-WROOM-32 dev board... |
| Flipper (Momentum / Unleashed) | STM32WB55RG (Flipper Zero "F7" hardware)... | An all-in-one, battery-powered RF/access-control multitool in one handheld: CC1101 sub-GHz... | Needs a board not owned. This firmware runs exclusively on Flipper Zero hardware (STM32WB5... |
| RayHunter (EFForg/rayhunter) | Qualcomm LTE baseband (e.g. the Orbic RC... | Passive cellular control-plane IMSI-catcher / cell-site-simulator (Stingray) detection by ... | Needs a board not owned. RayHunter runs ONLY on a Linux/Android device with a Qualcomm cel... |
| Pwnagotchi (jayofelony fork) | Broadcom BCM (Raspberry Pi SoC) — NOT an... | The only member of the fleet that runs a real reinforcement-learning agent (A2C / LSTM+MLP... | Runs ONLY on the Raspberry Pi 5 (8GB) of the owned boards — and even that is a compromise ... |
| RaspyJack | Raspberry Pi (Broadcom BCM2710A1 / Pi Ze... | It is the only "firmware" in the fleet that is a full Linux red-team drop-box on a quad-co... | Runs ONLY on a Raspberry Pi Linux SBC — none of the owned ESP32/ESP32-S2/S3/C5, CYD, Helte... |

---

## ESP32 Marauder

### What it is + latest version
ESP32 Marauder (justcallmekoko/ESP32Marauder) is "a suite of WiFi/Bluetooth offensive and defensive tools for the ESP32" — the canonical, reference WiFi/BLE recon-and-attack firmware that most other ESP32 security firmwares (and host apps) measure themselves against. **Latest stable release: v1.12.1, dated 2026-05-05** ([releases](https://github.com/justcallmekoko/ESP32Marauder/releases)). The v1.12.x line's headline work is around **Flock Safety camera hunting** ("Rework beacon content for Flock advertising," "Channel Hop to Flock Sniff," hidden-network probe fixes, Apple Juice CLI command) ([releases](https://github.com/justcallmekoko/ESP32Marauder/releases)).

### Chip/board it runs best (or only) on
- **Best / full-feature: classic ESP32 (WROOM-32).** This is the original target and the only silicon with complete WiFi **and** BLE parity — beacon/probe/deauth attacks, BLE spam, BLE/AirTag/Tile sniffing, Flock detection all work.
- **ESP32-S2: WiFi-only.** The S2 has **no Bluetooth radio at all** ([SparkFun S2 — "No Bluetooth"](https://www.amazon.com/SparkFun-Thing-Highly-Integrated-System-Chip/dp/B098TZ64LK)), so every BLE feature (BLE spam, sniffbt, AirTag/Tile, the BLE half of Flock Sniff) is simply absent. S2 is fine as a headless 2.4GHz WiFi recon/attack node.
- **ESP32-S3: supported** (koko's own MultiBoard S3 / Flipper Multi Board S3 are S3-based, and the release ships S3 bins). Full WiFi+BLE.
- **ESP32-C5: officially supported** via the dedicated [ESP32‑C5‑DevKitC‑1 wiki page](https://github.com/justcallmekoko/ESP32Marauder/wiki/ESP32%E2%80%90C5%E2%80%90DevKitC%E2%80%901). This is the **only path to dual-band 2.4+5GHz Wi‑Fi 6** scanning and deauth in the Marauder ecosystem — koko's "Double Barrel 5G" moved to the C5 chipset specifically for this ([CNX / Tindie](https://www.tindie.com/products/honeyhoneytrading/esp32-marauder-double-barrel-5g-c5-version/)).
- **Realtek RTL8720DN / BW16 / AmebaD: NOT supported as a Marauder host.** Marauder is ESP32-family firmware. The RTL8720 only appears as a 5GHz **co-processor slave** wired to an ESP32 in the "Double Barrel 5G" board ([CNX Software](https://www.cnx-software.com/2025/09/22/esp32-marauder-double-barrel-5g-adds-5ghz-deauthentication-with-rtl8720dn-module/)) — you cannot flash Marauder onto a BW16 and have it run.

### Unique specialty vs the rest of the fleet
1. **Flock Safety ALPR camera detection** — `Flock Sniff` and `Flock Wardrive` combine BLE + WiFi sniffing to flag misconfigured/legacy Flock surveillance cameras (battery telemetry over BLE, admin probe/beacon frames over WiFi) ([Flock Sniff wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/Flock-Sniff)). This is a Marauder-original feature.
2. **It's the reference firmware.** When a host tool ships an "ESP32 WiFi" mode (Flipper Zero WiFi Marauder app, your Cyber Controller), Marauder's serial protocol is the target it's written against first.
3. **Dual-band 5GHz** via the C5 — see above.

### Full feature/command surface
**WiFi attacks:** `attack -t deauth | beacon | probe | rickroll` (deauth flood, beacon spam, probe spam, rickroll SSID flood). **WiFi scan/sniff:** `scanap`, `scansta`, `scanall`, `sniffraw`, `sniffbeacon`, `sniffprobe`, `sniffdeauth`, `sniffpmkid` (handshake/PMKID capture → PCAP), `sigmon` (signal monitor), `packetcount`. **Evil Portal:** `evilportal` spins a rogue AP + captive-portal webserver serving an SD-card `index.html`; captured creds print to Serial/screen/log; optional `EPDeauth` deauths real APs to herd clients onto the portal ([evilportal wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/evilportal)). **Bluetooth/BLE:** `sniffbt`, `blespam -t` (incl. Apple/Samsung/Swift Pair/SourApple/Apple Juice variants), `spoofat`, AirTag/Tile detection, BLE wardrive. **Wardriving:** WiFi + Bluetooth + Flock wardrive with GPS-tagged logging. **Aux/admin:** `list`, `select`, `ssid`, `save`, `load`, `channel`, `clearlist`, `settings`, `led`, `gps`, `gpsdata`, `ls`, `stopscan`, `reboot`, `update`, `help`. Command set per [CLI wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/CLI) and [DeepWiki CLI](https://deepwiki.com/justcallmekoko/ESP32Marauder/2.3-command-line-interface).

### External modules it needs
- **SD card** — required for PCAP capture, wardrive logs, and serving Evil Portal HTML (`ls`/`save`/`load` depend on it).
- **GPS module (UART)** — required for `gps`/`gpsdata` and any wardriving (lat/long tagging).
- **No NRF24 required** for core Marauder. (Your NRF24L01 adapters are a GhostESP/Bruce/jammer thing, or the dual-NRF "Double Barrel" hardware — not needed for stock Marauder features.)
- No external radio needed for 2.4GHz; 5GHz needs C5 silicon (or the RTL8720 co-pro hardware variant).

### Host control (can Cyber Controller drive it?)
**Yes — real text CLI over UART/USB serial at 115200 baud** ([CLI wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/CLI)). Input is read line-by-line (`Serial.readStringUntil('\n')`) and dispatched to a `CommandLine` handler, so a host program can drive **every** capability programmatically by writing newline-terminated commands and reading back results — this is exactly how the Flipper WiFi Marauder app and a host GUI like Cyber Controller operate. The touchscreen/button UI on display boards is a parallel front-end, **not** a requirement: headless ESP32/S2 boards with no screen are fully usable over serial. This makes Marauder an ideal serial-driven backend for Cyber Controller.

### Flashing specifics
**Separate files at offsets, NOT a single merged bin** ([update-firmware wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/update-firmware)):
- bootloader → **0x1000**, partitions → **0x8000**, boot_app0 → **0xE000**, firmware app → **0x10000**.
- **ESP32-S3 exception:** bootloader goes to **0x0** (not 0x1000) — get this wrong and you brick-boot. (This matters for your T-Display-S3 and Heltec V3.)
- **ESP32-C5:** flash with the bundled **`c5_flasher.py`** python flasher (`C5_Py_Flasher/`), USB-C, follow the reset prompt ([C5 wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/ESP32%E2%80%90C5%E2%80%90DevKitC%E2%80%901)).
- Web-flash route: Spacehuhn Web Updater (esp.huhn.me) or ESP Terminator; SD-card/CLI `update` for on-device updates.
- Pick the **exact board bin**: the v1.12.1 release ships per-board binaries (cyd_2432s028, cyd_2432s024 RL Phantom, 3.5"/ST7796, M5 Cardputer / Cardputer ADV, Flipper, ESP32-C5 DevKit, Dev Board Pro, MultiBoard S3, Mini, Kit, v4/v6/v7/v8, S2 Reverse Feather).

### Gotchas
- **S2 has zero Bluetooth** — don't expect any BLE feature on your S2U boards.
- **BW16/RTL8720 cannot host Marauder** — it's a co-processor only.
- **CYD chip-ID ambiguity** (your known issue): a generic ESP32 and a CYD report the same chip ID, so you must pick the **CYD-specific bin** (display+touch pins differ) — flashing a plain-ESP32 build to a CYD = blank/white screen.
- **S3 bootloader at 0x0**, not 0x1000.
- Official "Marauder versions" (v4–v8, Mini, Dev Board Pro, Flipper BFFB) are koko's own boards ([versions wiki](https://github.com/justcallmekoko/ESP32Marauder/wiki/marauder-versions)); CYD/Cardputer/C5/T-Display are supported via prebuilt bins or custom builds, and koko explicitly **won't add source support for arbitrary displays** ([FAQ](https://github.com/justcallmekoko/ESP32Marauder/wiki/faq)).
- Deauth/Evil Portal are jurisdiction-restricted; this is a security-research/defensive-testing tool.

---

## Bruce

### What it is + version
**Bruce** is a "Predatory ESP32 Firmware" — a versatile, display-centric multi-tool for red-team / offensive-security work spanning WiFi, BLE, RF/SubGHz, RFID/NFC, IR, BadUSB, NRF24, and a built-in JavaScript interpreter. It is the spiritual "Flipper-Zero-on-an-ESP32" of the fleet: menu-driven, touchscreen/keyboard-first, with a large feature surface and an active project + web ecosystem. The repo moved from `pr3y/Bruce` to **`BruceDevices/firmware`** (old URLs redirect). **Current release: 1.15 (May 25, 2026)**; 1.14 was Feb 1, 2026. Home: https://bruce.computer · Repo: https://github.com/BruceDevices/firmware · Wiki: https://wiki.bruce.computer · DeepWiki: https://deepwiki.com/pr3y/Bruce.

### Chips / boards it runs best on
Bruce is **optimized for ESP32 devices that have a built-in display + buttons/touch** (M5Stack Cardputer/Core2/CoreS3/StickC, LilyGo T-Embed/T-Deck/T-Display-S3/T-Watch-S3, CYD ESP32-2432S028). It is happiest on **ESP32-S3** (USB-OTG for BadUSB, PSRAM, more flash) and the **classic ESP32 CYD**. Crucially for this fleet, Bruce has **first-class ESP32-C5 dual-band support** — board envs `esp32-c5`, `esp32-c5-tft`, and `nm-cyd-c5` exist, and **5GHz WiFi is confirmed working** on the Waveshare C5 (Waveshare even publishes a "How to Flash Bruce Firmware on ESP32-C5 (dual-band)" guide). Sources: board list https://github.com/BruceDevices/firmware/tree/main/boards ; C5 + 5GHz https://www.youtube.com/watch?v=E_2W-ITtgMo and https://www.cnx-software.com/2026/04/28/ ; supported devices https://deepwiki.com/pr3y/Bruce/9.1-supported-devices.

### UNIQUE specialty vs the rest of the fleet
Two things make Bruce distinct in this firmware fleet:
1. **It is the only firmware here that is a true Flipper-Zero-class SubGHz/IR/RFID/iButton handheld on ESP32** — with **CC1101 SubGHz scan/copy/replay/jam, `.sub` file TX, spectrum waterfall, IR TV-B-Gone + protocol decode/replay, 125kHz + 13.56MHz NFC (PN532) read/clone/emulate (Chameleon, Amiibolink), and iButton/1-Wire cloning**. Marauder/GhostESP/ESP32-DIV are WiFi/BLE-centric; Bruce is the multi-band signals tool.
2. **It is the only firmware here with a real Flipper-compatible serial CLI built on SimpleCLI** *plus* a **JavaScript interpreter** for on-device automation. This makes it the most "scriptable/host-drivable" firmware in the collection (see Serial section).

It is also the **strongest C5/5GHz firmware** in this set alongside the Waveshare C5 boards — most ESP32 attack firmwares have no C5 build at all.

### Full feature / command surface (verified)
- **WiFi:** Connect/AP modes, MAC spoofing, **deauth**, beacon spam, **Evil Portal** (credential harvest), wardriving, raw/promiscuous sniffer, NetCut, ARP scan/spoof/poison, TCP listener/client, TelNet, SSH, Responder, **WireGuard** tunneling, **Brucegotchi** (pwnagotchi-style).
- **BLE:** scan, **BadBLE** (Ducky over BLE), BLE HID keyboard (select devices), advertisement spam (Apple/iOS, Microsoft/Windows Swift Pair, Samsung, Google/Android).
- **RF / SubGHz:** scan/copy, custom payloads, spectrum analysis/waterfall, raw record, **full + intermittent jamming**, `.sub` replay — **requires CC1101** for real range/TX (basic GPIO RF exists but is weak).
- **NRF24:** 2.4GHz spectrum, **2.4GHz jamming**, **MouseJack** — **requires NRF24L01**.
- **RFID/NFC (TagOMatic):** read/write/clone, **125kHz LF**, NDEF write, **Chameleon emulation**, Amiibolink — **requires PN532 / PN532Killer** (some boards have ST25R3916).
- **IR:** TV-B-Gone (NA/EU), NEC/RC5/RC6/Sony/Samsung decode + custom replay, IR jamming.
- **BadUSB / HID:** Ducky-script keyboard emulation — **requires native USB-OTG (ESP32-S2/S3 only)**.
- **Other:** FM broadcast, **JavaScript interpreter** (`/scripts`, `/BruceJS`), QR (incl. PIX), mic spectrum, **iButton** 1-Wire, ESP-NOW file/command transfer, SD card mgmt, RTC, LED control, WebUI.
- **Serial CLI commands:** `ir, subghz, music_player, say, led, power, clock, screen, color, tone, gpio, i2c, storage, settings, factory_reset, badusb, js, crypto, uptime, date, free, info, webui, loader` + file ops (`ls/read/rm/md5/crc32`), `ymodem_receive`, `set <k> <v>`, `reboot` — "most are compatible with the Flipper Zero CLI." Feature source: https://deepwiki.com/pr3y/Bruce/1.1-features ; serial source: https://github.com/BruceDevices/firmware/wiki/Serial and https://deepwiki.com/pr3y/Bruce/11.2-serial-commands.

### External modules it needs
Bruce's headline radio features are **not on-board** for generic ESP32 — they need wired modules: **CC1101** (SubGHz, on SPI), **NRF24L01** (2.4GHz jam/MouseJack, on SPI), **PN532** (NFC, I2C/SPI). LoRa/W5500 also supported. Pins are **user-configurable in-firmware** (RF → Config → RF Module → "CC1101 on SPI"; pin editor for CC1101/NRF24/LoRa/W5500), so you do **not** need a board-specific build to wire a module. Wiring diagrams: https://wiki.bruce.computer/external-modules/cc1101/ and https://wiki.bruce.computer/wiring-diagrams/. Your **NRF24L01 adapters** are directly usable; you'd need to add a **CC1101** and a **PN532** to unlock SubGHz/NFC (not owned yet).

### Host control / serial (can Cyber Controller drive it?)
**Partially yes — better than touch-only, but not a full attack remote.** Bruce has a genuine **SimpleCLI serial interface at 115200 8N1** running as a dedicated FreeRTOS task with **structured, host-parseable output**, reachable from any terminal/Python script or the WebUI "SerialCmd" button. Cyber Controller can absolutely drive: **IR send, SubGHz rx/tx + `.sub` TX, BadUSB, JS execution (`js run_from_buffer`), settings get/set, file transfer (ymodem), info/free/reboot/factory_reset**. **Gotcha / limitation:** the documented serial command set does **not** expose the WiFi/BLE attacks (deauth, Evil Portal, BLE spam) — those remain **menu/touch-driven on the device UI**. There is also a **binary "Navigator" packet protocol that streams the UI to a host (remote display)**, plus a full **WebUI** and **headless mode** for boards without a screen. Net: Cyber Controller's existing Bruce protocol parser is justified for the CLI-exposed subset; treat WiFi/BLE attacks as on-device-only unless driven via a JS script pushed over `js`. Sources: https://github.com/BruceDevices/firmware/wiki/Serial ; https://deepwiki.com/pr3y/Bruce/11.2-serial-commands ; headless https://github.com/BruceDevices/firmware/wiki/FAQ.

### Flashing specifics
Bruce ships as a **single merged full bin flashed at offset 0x0** (bootloader+partitions+app combined) for every board. Three install paths:
1. **Web flasher (recommended):** https://bruce.computer/flasher — ESP-Web-Tools, picks board, one-click. Board dropdown includes CYD-2432S028, CYD-3248S035, T-Display-S3, ESP32-C5, M5 family, T-series.
2. **esptool (offline):** `esptool.py --port <COM> write_flash 0x0 Bruce_<device>_<ver>.bin` (per the wiki). Note: the merged bin already embeds the bootloader, so **0x0 is correct for all chips here** (this differs from the per-region 0x1000/0x8000/0x10000 layout — do NOT split it).
3. **M5Burner** (M5Stack devices). OTA updates available via WebUI once flashed. **No AmebaD/Realtek path** — Bruce is ESP-IDF/Arduino-ESP32 only. Sources: https://wiki.bruce.computer/how-to-install/ ; https://bruce.computer/flasher.

### Gotchas
- **No classic WROOM-32 official build.** The "generic" `ESP-General` env is actually an **ESP32-S3 DevKitC** target, and **headless mode's reference env is `esp32-s3-devkitc-1` (S3-only)**. Running Bruce on a bare classic ESP32 WROOM-32 is a **community/DIY port** (open issues #951, #558, #494), not a maintained binary.
- **No ESP32-S2 board folder exists** — and **BadUSB needs USB-OTG**, which classic ESP32 lacks (so even if ported, no BadUSB on classic).
- **No Realtek/BW16 and no LoRa-radio build** — the Heltec SX1262 is unused by Bruce (it'd run as a plain S3, SX1262 idle).
- SubGHz/NFC are **module-gated**: out of the box on a CYD you only get WiFi/BLE/IR(if IR LED)/NRF24(if wired) — the "Flipper killer" reputation assumes you add CC1101 + PN532.
- WiFi/BLE attacks are **not** in the serial CLI (UI-only) — see host-control note.

---

## GhostESP

**What it is + version.** GhostESP is an open-source ESP-IDF firmware that turns an ESP32 into a WiFi/BLE/RF "multitool" with a full on-device LVGL touch UI *and* a real serial CLI. The original `Spooks4576/Ghost_ESP` was archived by its author on **Apr 22, 2025**; active development moved to the community **`GhostESP-Revival/GhostESP`** org, which is the canonical source today. Latest release at time of writing is **v1.9.10 (May 18, 2026)** ([repo](https://github.com/GhostESP-Revival/GhostESP), [releases](https://github.com/GhostESP-Revival/GhostESP/releases), [project site](https://ghostesp.net/), [docs](https://docs.ghostesp.net/latest/getting-started/supported-hardware/)). It advertises 40+ board targets.

**Chips / boards it runs on.** Supported silicon: **ESP32 (WROOM), ESP32-S2, ESP32-C3, ESP32-S3, ESP32-C5, ESP32-C6** ([supported-hardware](https://docs.ghostesp.net/latest/getting-started/supported-hardware/)). It is **Espressif-only** — there is **no RTL8720DN / BW16 / AmebaD** target anywhere in the matrix or release assets. Generic targets ship as `esp32-generic.zip` (covers ESP32/S2/C3/S3/C6); C5 has its own path (`xiao_esp32c5.zip` and vendor builds `ACE_C5.zip` / `Banshee_C5.zip`). Notable vendor zips: `CYD2432S028R.zip`, `CYD2USB.zip`, `LilyGo-TDisplayS3-Touch.zip`, `LilyGo-T-Deck.zip`, `heltecv3.zip`, `ESP32-S3-Cardputer.zip`, `Waveshare_LCD.zip`, `ghostboard.zip` ([supported-hardware](https://docs.ghostesp.net/latest/getting-started/supported-hardware/), [releases](https://github.com/GhostESP-Revival/GhostESP/releases)).

**Best/only chip & the UNIQUE specialty.** Feature-richest on **ESP32-S3** (touch UI, USB-HID/BadUSB, camera builds). But its one capability nothing else in the fleet matches is on **ESP32-C5/C6: genuine 5 GHz dual-band WiFi.** The C5 is Espressif's first 2.4+5 GHz Wi-Fi 6 RISC-V part ([Espressif](https://www.espressif.com/en/products/socs/esp32-c5)), and GhostESP exposes 5 GHz AP scanning, wardriving, and SAE/WPA3 flooding there. v1.9.10's changelog explicitly fixed *"ESP32-C5 not discovering 5 GHz channels above UNII-1"* via country-code/driver re-init ([releases](https://github.com/GhostESP-Revival/GhostESP/releases)) — so 5 GHz is real and actively maintained, not a stub. Every other ESP32 in the fleet is 2.4 GHz-only by silicon.

**Per-chip caveats (important for the fleet).** The docs compatibility matrix shows **ESP32-S2 = WiFi + GPS + SD only**: ✗ Bluetooth, ✗ NFC, ✗ IR, ✗ keyboard, ✗ display — because the S2 die has no BLE radio at all ([supported-hardware](https://docs.ghostesp.net/latest/getting-started/supported-hardware/); [S2 has no Bluetooth](https://www.espboards.dev/blog/esp32-soc-options/)). So the owned S2U boards run GhostESP but lose its BLE/NFC/IR surface. **Heltec V3** appears in the matrix with status-display + GPS + SD + Chameleon-NFC, but **LoRa/SX1262 is not listed as a GhostESP feature** (flagged below).

**Full feature / command surface.** GhostESP is driven by a real serial CLI (see below) organized into categories: **Core, WiFi, BLE, Portal, GhostLink/comm, Storage(sd), Camera, RGB/led, Infrared, GPS, Ethernet, Settings, BadUSB** ([CLI reference](https://docs.ghostesp.net/latest/getting-started/command-line-reference/)).
- **WiFi:** `scanap`, `scansta`, `scanall`, `sweep`, `listenprobes`, `select`, `connect/disconnect`, `trackap/tracksta`, `attack -d|-c|-e|-s` (deauth/disassoc/evil-portal), `beaconspam`, `karma`, `saeflood` (WPA3/SAE), `scanports`, `dhcpstarve`, `capture` (PMKID/handshake → PCAP), plus Evil Portal and live Wireshark-over-USB streaming.
- **BLE:** `blescan`, `blewardriving`, `blespam`, `spoofairtag`, GATT (`enumgatt/trackgatt/listgatt/selectgatt`), and "aerial" AirTag/skimmer/Flipper detection (`aerialscan/aerialtrack/aerialspoof`).
- **GPS:** `gpspin`, `gpsinfo`, `startwd` (wardriving → WiGLE-format CSV on SD).
- **IR:** `ir list/send/learn/dazzler`, Flipper `.ir` compatible.
- **NFC (PN532):** read/write NTAG + MIFARE Classic dictionary attacks, Flipper `.nfc` import/export.
- **SubGHz / NRF24:** documented as supported (CC1101 subghz scan/replay across ~64 channels with waterfall + 20+ decoders; NRF24 spectrum analyzer / MouseJack) ([repo](https://github.com/GhostESP-Revival/GhostESP), [docs](https://docs.ghostesp.net/latest/getting-started/supported-hardware/)).

**External modules.** Most radio extras need add-on hardware over GPIO/SPI: **CC1101** for SubGHz; **NRF24** for spectrum/MouseJack (owned — NRF24L01 adapters); **PN532** for NFC; **SX1262** for LoRa ([supported-hardware](https://docs.ghostesp.net/latest/getting-started/supported-hardware/)). Core WiFi/BLE need no module. On a bare classic-ESP32 or C5 you get WiFi/BLE out of the box; CC1101/PN532 are not owned, so SubGHz/NFC are out until acquired.

**Host control (Cyber Controller over serial — YES, real CLI).** GhostESP exposes a genuine bidirectional serial console at **115200 baud** (selectable up to 921600), responses prefixed with `>`, plus a `help` listing all categories ([CLI reference](https://docs.ghostesp.net/latest/getting-started/command-line-reference/), [serial console](https://ghostesp.net/serial)). The official `ghostesp.net/serial` console drives it via the Web Serial API in Chromium. **This means a host controller like Cyber Controller can drive GhostESP over the COM port with real text commands** — not touch/button-only. (Open question: whether the CLI is 100% feature-parity with the touch UI.) This makes the headless classic-ESP32 and C5 dev boards good Cyber-Controller targets.

**Flashing specifics.** Each board `.zip` contains the three standard ESP-IDF binaries — `bootloader.bin`, `partitions.bin`, `firmware.bin` — flashed at chip-specific offsets, **and** (per third-party flasher docs) a full **`merged-gesp.bin`** for single-shot flashing at **0x0** with esptool ([install guide](https://docs.ghostesp.net/latest/getting-started/installation-guide/), [esp-flasher notes](https://github.com/Spooks4576/Ghost_ESP/wiki/Installation)). Offsets:
- **ESP32-S2:** bootloader `0x1000`, partitions `0x8000`, firmware `0x10000`.
- **ESP32-S3 / C3 / C6 (and C5):** bootloader `0x0`, partitions `0x8000`, firmware `0x10000`.

Easiest path is the web flasher (`flasher.ghostesp.net`, Chromium only); manual fallback is `esp.huhn.me` (load the 3 bins at the offsets) or esptool with `merged-gesp.bin` at 0x0 ([install guide](https://docs.ghostesp.net/latest/getting-started/installation-guide/)). **Do NOT** load `merged-gesp.bin` into a Flipper "FirmwareA" slot — use the separate `firmware.bin` there. The owned **S2U boards are USB-native (CP2102 present anyway)** so they flash cleanly; note the S2's `0x1000` bootloader offset differs from S3/C5.

**Gotchas.**
- **BW16 x3 won't run it** — RTL8720DN/AmebaD is not an Espressif chip; use a Realtek-targeted firmware instead.
- **S2 boards are crippled** (no BLE/NFC/IR/display) — fine as WiFi-only/GPS nodes, not as the full multitool.
- **S2 vs S3/C5 flash offset differs** (bootloader `0x1000` vs `0x0`) — wrong offset = boot loop.
- **Web flasher is Chromium-only** (Web Serial API) — no Firefox/Safari.
- **C5 5 GHz needed a recent fix** (≤ v1.9.10) — flash current, not an old build, or 5 GHz channels above UNII-1 won't enumerate.
- **Heltec V3 LoRa is likely unused** by GhostESP (see open questions).

Sources: [GhostESP-Revival/GhostESP](https://github.com/GhostESP-Revival/GhostESP) · [releases](https://github.com/GhostESP-Revival/GhostESP/releases) · [docs: supported hardware](https://docs.ghostesp.net/latest/getting-started/supported-hardware/) · [docs: CLI reference](https://docs.ghostesp.net/latest/getting-started/command-line-reference/) · [docs: installation](https://docs.ghostesp.net/latest/getting-started/installation-guide/) · [serial console](https://ghostesp.net/serial) · [ghostesp.net](https://ghostesp.net/) · [ESP32-C5 / Espressif](https://www.espressif.com/en/products/socs/esp32-c5)

---

## HaleHound (HaleHound-CYD)

**What it is + version.** HaleHound-CYD is a multi-protocol offensive-security toolkit by JesseCHale — the "ESP32-DIV HaleHound Edition for Cheap Yellow Display." It is a port of the original ESP32-DIV HaleHound firmware onto the resistive-touch CYD form factor, fanned out across five+ RF domains (WiFi / BLE / SubGHz / 2.4GHz-NRF24 / NFC / Guardian). **Latest release: v3.5.5 (April 3, 2026)** (prior: v3.5.1 Mar 28, v3.5.0 Mar 27, v3.4.0 Mar 15). Sources: [repo](https://github.com/JesseCHale/HaleHound-CYD), [README](https://github.com/JesseCHale/HaleHound-CYD/blob/main/README.md), [releases](https://github.com/JesseCHale/HaleHound-CYD/releases), [halehound.com](https://halehound.com/).

**Chip / board it runs best (or only) on.** Classic **ESP32-WROOM only** — this is a fork of the classic-ESP32 ESP32-DIV project, NOT an S3/S2/C5 codebase. The README's official board matrix (build target):
- `esp32-cyd` — **ESP32-2432S028 (CYD 2.8")**, ILI9341 240x320, XPT2046 touch — *Fully Tested* (your board)
- `esp32-e32r35t` — QDtech E32R35T (3.5"), **ST7796 320x480**, XPT2046 — *Fully Tested*
- `esp32-e32r28t` — QDtech E32R28T (2.8"), ILI9341, XPT2046 — *Fully Tested*
- `esp32-cyd-hat` — NM-RF-Hat (2.8"), ILI9341, XPT2046 — *Supported*

**UNIQUE specialty vs the rest of the fleet.** Two things set it apart: (1) the **Guardian / Jam-Detect** defensive suite — WiFi Guardian (deauth-flood detection), SubGHz Sentinel (carrier-jam detection), 2.4GHz Watchdog (broadband-disruption detection), Full Spectrum monitor — a real cross-band *blue-team* detector, persistent across reboots; and (2) it is the only fleet firmware that fuses **WiFi + BLE + CC1101 SubGHz + NRF24 2.4GHz + PN532 NFC** into one touchscreen device with bleeding-edge BLE CVE exploits (see below). Where Marauder is WiFi/BLE-centric and Bruce/Flipper-style tools lean SubGHz/NFC, HaleHound spans all five on a $7-class board.

**Full feature / command surface (touch menu tree, not a CLI):**
- **WiFi (+20.5 dBm):** deauth floods, beacon spam, Evil Twin / GARMR captive portal, probe sniffing, auth-frame flooding, station scan, EAPOL/PMKID capture, Karma, wardriving w/ GPS logging. "40+ attack modules" total across domains.
- **BLE (+9 dBm):** **BLE Predator** (3-phase: SCAN→threat-classify, RECON→GATT enumerate, HONEYPOT→clone connectable server + harvest creds on WRITE); **WhisperPair** (CVE-2025-36911, Google Fast Pair); **Airoha RACE** (CVE-2025-20700/20701/20702 — unauthenticated link-key/BD_ADDR/firmware extraction from Sony XM4/XM5/XM6, Marshall, JBL, Jabra, Beyerdynamic, *no pairing*); BLE Cinder/Spoofer/Beacon; **Lunatic Fringe** (AirTag/FindMy tracker detect + spoof).
- **SubGHz (CC1101, +12 dBm stock / +20 dBm w/ E07 PA):** record/replay 300–928 MHz, brute force (Princeton/CAME/Nice/PT2262, De Bruijn sequences), **Tesla charge-port opener** (static 43-byte OOK, US 315 / EU 433.92 MHz, zero rolling code), `.sub` file browser (Flipper-format), spectrum analysis, RSSI-gated replay.
- **2.4GHz (NRF24L01+PA+LNA, +20 dBm):** promiscuous sniffer, **MouseJack** keystroke injection (Logitech Unifying, Dell, Microsoft via HID++; pre-built payloads incl. reverse shell / WiFi exfil / custom string), WLAN Ember broadband disruption, spectrum analyzer.
- **RFID/NFC (PN532 V3, SPI):** card scan/read/clone, MIFARE key brute force, UID emulation.
- **Guardian (defensive):** the jam/attack detectors above.
- **Tools:** UART **Serial Monitor / passthrough** (P1 connector, UART0 GPIO3 RX, default 115200, auto-scan 9600 for device detect), GPS satellite view, SD loot browser, OTA update.
- **VALHALLA Protocol:** all offensive modules are gated behind a liability disclaimer; declining drops the device into **Blue Team mode** (passive/defensive only, persists across reboots).

**External modules it needs.** All radios are external add-ons over the CYD's VSPI breakout (SCK/MOSI/MISO = GPIO 18/23/19 shared):
- **CC1101** (HW-863 stock, or E07-433M20S PA) — SubGHz. CS=GPIO27 (GPIO21 on E32R28T/R35T), GDO0=22, GDO2=35.
- **NRF24L01+PA+LNA** — 2.4GHz/MouseJack. CSN=GPIO4 (GPIO26 on R28T/R35T), CE=16, IRQ=17.
- **PN532 V3 (SPI mode, DIP CH1=OFF/CH2=ON)** — NFC. SS=GPIO17.
- **GPS** (GT-U7 / NEO-6M) — wardriving. TX→GPIO3; **GPIO3 is shared with USB serial**, firmware calls `Serial.end()` during GPS use.
- **You own:** NRF24L01 adapters ✓, IPEX→SMA pigtails + 315MHz antennas ✓ (good for the Tesla/SubGHz 315MHz path). **You do NOT own a CC1101 or a PN532** — SubGHz and NFC domains are dark until you buy those. PA modules (E07-433M20S / E01-2G4M27SX) **must** be powered from an independent 5V→3.3V buck (AMS1117-3.3 / MP2307, 500mA+) — sharing the CYD 3.3V rail causes brownouts/resets.

**Host control (Cyber Controller fit).** **Touch-only — there is NO host-driveable attack CLI.** The README and FLASH_INSTRUCTIONS explicitly state no serial CLI / host-driven control; every module is reached through the capacitive-menu tree. The only serial surface is a *UART passthrough Serial Monitor* tool meant for probing *external* target devices, not for a host PC to drive HaleHound. So **Cyber Controller can FLASH it (esptool/web-flasher) but cannot orchestrate its attacks over serial** — unlike a Marauder-class CLI firmware. Treat it as a flash-and-walk-away touch device in your fleet.

**Flashing specifics.** Pre-built bins live in `flash_package/` (and per-release assets), **one bin per board**:
- **Single-file (preferred):** flash `HaleHound-CYD-FULL.bin` at **0x0**. CYD-HAT = `HaleHound-CYD-HAT-FULL.bin`; 3.5" = `HaleHound-E32R35T-FULL.bin`; 2.8" QDtech = `HaleHound-E32R28T-FULL.bin`. Web flasher: [esp.huhn.me](https://esp.huhn.me) (Chrome/Edge/Opera). esptool: `esptool.py --chip esp32 --baud 115200 write_flash 0x0 HaleHound-CYD-FULL.bin`.
- **4-file fallback (use if black screen):** bootloader.bin@0x1000, partitions.bin@0x8000, boot_app0.bin@0xe000, `HaleHound-CYD.bin`@0x10000.
- **OTA:** drop a `.bin` in SD `/firmware/`, then Tools > Update Firmware. SD must be FAT32 (`/subghz/`, EAPOL, wardrive, BLE loot, `creds.txt`).
- First boot runs touch calibration; rotation is set in Settings (no reflash).

**Gotchas.** CH340 driver needed on Win/macOS. NRF24 random resets → solder a 10µF cap across module VCC/GND. PA modules require their own buck (above). Building from source: PlatformIO breaks on Python 3.14 — use 3.10–3.13. Beware the third-party `SLZLabs/HaleHound-CYD-3.2-ESP32E-40R` fork (self-labeled "WIP MOST STUFF IS BROKEN") — use upstream JesseCHale only.

---

## ESP32-DIV

### What it is + latest version
**ESP32-DIV** (cifertech/ESP32-DIV) is an open-source, Flipper-style **handheld multi-band wireless multitool** with a touchscreen UI. It is a *device-first* firmware: it is written for one specific custom PCB ("ESP32-DIV V2"), not as a generic flash-and-go image. The current release is **v1.6.0 (May 13, 2026)**, which added the full RFID/NFC toolkit, GPS wardriving, and a satellite scanner. Release lineage:

- **v1.0.0 (Apr 25, 2025)** and **v1.1.0 (May 11, 2025)** — classic **ESP32-WROOM**; WiFi deauth, captive portal, BLE sniffer, early dual-band.
- **v1.5.0 (Jan 5, 2026)** — **major hardware refresh to ESP32-S3** ("resolves previous pin conflicts and unlocks new capabilities"); packet monitor, WiFi deauther.
- **v1.5.3 (May 4, 2026)** — universal IR controller, Android/BLE spoofing, SD file manager.
- **v1.6.0 (May 13, 2026)** — RFID/NFC toolkit, GPS wardriver, satellite scanner, UI/bug fixes.

Sources: https://github.com/cifertech/ESP32-DIV/releases · https://github.com/cifertech/ESP32-DIV · https://cifertech.net/esp32div-your-swiss-army-knife-for-wireless-networks/

### Chip / board it runs best (or only) on
**v1.5.0+ targets ESP32-S3 exclusively; the classic-ESP32 path is frozen at v1.1.0.** The S3 move was made specifically to escape GPIO conflicts and to gain native USB. Critically, ESP32-DIV is bound to a **custom pogo-pin mainboard+shield** — ILI9341 2.8" TFT, XPT2046 touch, PCF8574 I/O-expander buttons, IP5306-I2C battery PMIC, CP2102 (or native S3 USB-JTAG), and onboard radios. It is **not** designed to run on off-the-shelf dev boards; the wiki explicitly documents no CYD/other-board compatibility. (Hardware: https://github.com/cifertech/ESP32-DIV/wiki/Hardware · Schematics: https://github.com/cifertech/ESP32-DIV/wiki/Schematics)

### UNIQUE specialty vs the rest of the fleet
This is the fleet's **only "all-RF-bands-in-one-handheld" firmware**. Where Marauder = WiFi/BLE, and a bare CC1101 build = sub-GHz, ESP32-DIV converges **WiFi + BLE + 2.4 GHz (3xNRF24) + sub-GHz (CC1101) + IR (record/replay/universal) + RFID/NFC (PN532) + GPS wardriving + a satellite scanner** behind one touch UI. The **triple-NRF24 2.4 GHz spectrum analyzer / "Proto Kill"** and the **CC1101 replay+jam with SD-saved profiles** are things no other firmware in your fleet does, and the **PN532 RFID/NFC suite** (read/clone/dump/erase/decode-access/jam) is unique here too.

### Full feature / command surface (from the Features wiki)
- **WiFi (built-in S3 radio):** Packet Monitor (waterfall + PCAP-to-SD), Beacon Spammer, WiFi Deauther, Probe Request Flood, Deauth Detector, WiFi Scanner, Captive Portal.
- **BLE (built-in):** BLE Jammer, BLE Spoofer (incl. Apple "Sour Apple" + Android spoof), Sniffer, BLE Scanner, BLE Rubber Ducky (HID payloads in `/ducky`).
- **2.4 GHz (NRF24):** Scanner (channel-energy spectrum), Proto Kill.
- **Sub-GHz (CC1101):** Replay Attack, SubGHz Jammer (carrier/sweep), Saved Profile (replay from SD).
- **IR (built-in):** Record, Saved Profile (replay), Universal Controller.
- **RFID/NFC (PN532, SPI):** Card Reader, Clone, Erase, Dump, Decode Access, Jam Reader, Tag Disrupt, Disrupt Emulate.
- **GPS:** Wardriver (WiFi+BLE geo-logging), Satellite Scanner.
- **System/Tools:** Serial Monitor (on-screen debug terminal), Update Firmware (OTA/SD), Touch Calibrate, SD File Manager, themes, NeoPixel + buzzer feedback.

Source: https://github.com/cifertech/ESP32-DIV/wiki/Features

### External modules it needs
The radios are **not on the ESP32 itself** (only WiFi/BLE are). To get the headline features you need: **3x NRF24L01** (2.4 GHz), **1x CC1101** (sub-GHz), an **IR transceiver**, a **PN532 (SPI)** for RFID/NFC, and a **GNSS/GPS** module for wardriving. On the V2 board these are integrated via the pogo-pin shield. From your inventory: your **NRF24L01 adapters + IPEX->SMA pigtails** cover the 2.4 GHz side, but you do **not** own a CC1101 or PN532, so sub-GHz and NFC would need sourcing.

### Host control — touch/button ONLY, no real serial CLI
**A host controller such as Cyber Controller CANNOT drive ESP32-DIV over serial.** This is the key divergence from Marauder: ESP32-DIV is **operated entirely by the on-device touchscreen + PCF8574 buttons**. Its "Serial Monitor" is an *on-device* terminal/debug feature (you pick baud and watch traffic on the TFT) — it is **diagnostic output, not an inbound command parser**. There is no documented companion/host app and no serial command grammar a PC can send. The USB/CP2102 (or S3 USB-JTAG) link is used for **flashing and log viewing only**. So in your stack, Cyber Controller's serial-driving model applies to Marauder, not to ESP32-DIV. (Sources: https://github.com/cifertech/ESP32-DIV/wiki/Features · https://github.com/cifertech/ESP32-DIV)

### Flashing specifics
The Firmware-Upload wiki documents using the **Espressif Flash Download Tool** with a **multi-file (NOT merged) layout**: `.bin` → **0x10000**, `.partitions` → **0x8000**, SPI **40 MHz / DIO**, "check both file boxes." **Caveat:** that page still says **"Chip: ESP32"**, which looks stale from the v1.1.0 era and conflicts with the v1.5.0+ ESP32-S3 hardware — for an S3 build expect a bootloader@0x0 + partitions@0x8000 + app@0x10000 set (or `esptool --chip esp32s3 ... write_flash 0x0 <merged>.bin`) and **USB-CDC-on-boot enabled**. Releases ship a precompiled app bin (e.g. `ESP32-DIV-v1.6.0.bin`, ~1.54 MB). Building from source requires **ESP32 Arduino core v2.0.10 specifically** (newer cores break it), a **platform.txt replacement**, and author-pinned libs: **SmartRC-CC1101-Driver-Lib, arduinoFFT, TFT_eSPI**. **No AmebaD/RTL8720 path exists** — your BW16 kits are irrelevant to this firmware. (Sources: https://github.com/cifertech/ESP32-DIV/wiki/Firmware-Upload · https://github.com/cifertech/ESP32-DIV/issues/102)

### Gotchas
- **GPIO14 IR/NRF24 conflict:** the IR emit tube shares GPIO14 with NRF24 — you must **restart between IR and NRF24 use**.
- **Pogo-pin reliability:** documented field failures are mostly **cold solder + pad oxidation at the pogo headers**, causing NRF24/CC1101 init failures; verify 3V3/5V/CE/CSN (CE & CSN should read >3 V after init) before blaming firmware.
- **IP5306-I2C (not plain IP5306):** battery % needs custom I2C register reads; GPIO34 ADC is unconnected.
- **NeoPixel (GPIO1, 4 LEDs) and buzzer** needed manual enablement in some builds.
- **Wiki/version drift:** the upload page's "Chip: ESP32" note is the biggest trap — confirm chip/offsets per-release before flashing.

(Source: https://github.com/cifertech/ESP32-DIV/issues/102 · https://github.com/cifertech/ESP32-DIV/wiki/Hardware)

---

## Meshtastic

### What it is + version
Meshtastic is the official open-source firmware for an **off-grid, encrypted LoRa mesh communication system** — long-range, low-power text messaging, GPS/position sharing, and sensor telemetry that works with **no internet, cellular, or Wi-Fi infrastructure**. Nodes auto-form a multi-hop mesh and relay each other's packets over kilometers. It is fundamentally different from the rest of your fleet: every other firmware you run (Marauder, ESP32-DIV, custom recon) is short-range Wi-Fi/BLE/sub-GHz tooling; Meshtastic is your only resilient comms backbone and the only firmware that *requires* a dedicated LoRa transceiver (SX1262/SX1276) to function at all.

- **Latest release at research time:** `v2.7.25.104df5f` — **Alpha / pre-release**, dated 2026-06-10. The project ships fast: recent tags `v2.7.25` (Jun 10), `v2.7.24.472b14c` (May 23), `v2.7.23.b246bcd` (May 8), `v2.7.22.96dd647` (Apr 14), `v2.7.21.1370b23` (Apr 6), all marked **Alpha pre-release**, on a ~1-4 week cadence. There is no separate "stable" channel surfaced on the releases page right now — the Android app and Web Flasher track these tagged builds. **Always re-check the releases page before flashing** ([github.com/meshtastic/firmware/releases](https://github.com/meshtastic/firmware/releases)). Repo: [github.com/meshtastic/firmware](https://github.com/meshtastic/firmware).
- Codebase is C++/C; supported MCU families are **ESP32, nRF52, RP2040/RP2350, and Linux-native (portduino)** — notably **NOT Realtek/AmebaD** ([meshtastic.org/docs/hardware/devices](https://meshtastic.org/docs/hardware/devices/)).

### Best chip / board (and the one you own)
The canonical, first-class target for you is the **Heltec WiFi LoRa 32 V3** = **ESP32-S3FN8 + Semtech SX1262** + 0.96" OLED, available in 433/470-510/863-870/**902-928 MHz (US_915)** band variants. This is a plug-and-flash device — pick **"Heltec V3"** in the Web Flasher (the V4 shares the same firmware) ([meshtastic.org Heltec LoRa32 docs](https://meshtastic.org/docs/hardware/devices/heltec-automation/lora32/), [heltec.org WiFi LoRa 32 V3](https://heltec.org/project/wifi-lora-32-v3/)). The firmware artifact is `firmware-heltec-v3-X.X.X.xxxxxxx.bin`.

The **Raspberry Pi 5 (8GB)** is the other great fit: run **`meshtasticd`** (the firmware compiled for Linux via portduino) to make the Pi an always-on gateway/router/MQTT bridge. **Caveat:** meshtasticd needs an **SPI-based LoRa HAT** (e.g. RAK6421 / MeshAdv) — **UART HATs are NOT supported**, and you do not currently own a LoRa HAT, so the Pi 5 is a future build, not a today-build ([meshtastic.org Linux-native](https://meshtastic.org/docs/hardware/devices/linux-native-hardware/), [meshtasticd config](https://meshmonitor.org/configuration/meshtasticd.html)).

### Unique specialty vs the rest of your fleet
- **Only true mesh networking** in your kit: self-healing, multi-hop, no central node, survives nodes dropping out.
- **Encrypted by default** — AES256 (or AES128) per-channel PSK; channels shareable via QR/`--seturl`.
- **Sub-mW idle, multi-km range** on LoRa — none of your Wi-Fi/BLE boards come close on range or battery.
- It is the *only* firmware you own that **demands a dedicated SX1262/SX1276 radio** — which is exactly why it maps cleanly to the Heltec V3 and almost nothing else without hand-wiring.

### Feature / module surface
Core: encrypted text messaging, position/GPS sharing, node DB, traceroute, channel management. Optional **modules** (all toggle via config) ([Module Configuration](https://meshtastic.org/docs/configuration/module/)):
- **Telemetry** (auto-discovers I2C sensors at boot, environment/device metrics)
- **Serial** (UART passthrough, GPIO RX/TX, 110-921600 baud — useful for bridging to your other hardware)
- **Store & Forward** (caches messages for offline nodes)
- **Range Test** (field range/packet-loss testing)
- **MQTT** (gateway packets to an internet broker — pair with the Pi 5)
- **Canned Message** (predefined messages without a phone — button/rotary input)
- **External Notification** (drive a buzzer/LED on message)
- **Detection Sensor** (GPIO trip → mesh alert)
- **Remote Hardware / Paxcounter / Neighbor Info / Waypoint**

### Host control — YES, a real serial CLI (Cyber Controller can drive it)
Meshtastic is **fully host-drivable over serial**, not touch/button-only. It exposes a **Client API** over **USB-Serial, TCP, and BLE** using a clean **protobuf stream**: `ToRadio` packets host→device, `FromRadio` device→host. The serial/TCP framing is a **4-byte header — `0x94 0xc3` + length MSB/LSB — max 512-byte packet** ([Client API docs](https://meshtastic.org/docs/development/device/client-api/)). This means **your Cyber Controller / any host can implement a real protobuf serial driver** — the same wire format the official Python `meshtastic` CLI uses.

The reference CLI (`pip install meshtastic`) drives it over USB serial with commands like `--info`, `--nodes`, `--sendtext "hi"`, `--set <path> <val>`, `--ch-set` / `--ch-index` / `--seturl` (channels + PSK: `none`/`random`/`default`/`0x<hex>`), `--set-ham`, `--setlat/--setlon/--setalt`, `--ble`/`--ble-scan`, and `--noproto` ("dumb serial terminal" for raw debug) ([CLI usage](https://meshtastic.org/docs/software/python/cli/usage/)). **Practical note for Cyber Controller:** the doc does not pin a baud rate — implement against the protobuf framing rather than assuming a baud; the framing is baud-independent.

### Flashing specifics (ESP32 / ESP32-S3)
- **Easiest:** [Meshtastic Web Flasher](https://flasher.meshtastic.org/) in Chrome/Edge (Web Serial), pick device + region — done in ~2 min.
- **Factory/merged bin** is written at **offset `0x00`** (includes bootloader + partition table + app). The **littlefs** filesystem partition goes at a **variant-specific high offset** (e.g. ~`0x670000` on 8MB BigDB, `0xc90000` on 16MB BigDB, `0x300000` on T-LoRa) — get this right or the device won't store config ([Flash ESP32 docs](https://meshtastic.org/docs/getting-started/flashing-firmware/esp32/), [CLI flashing](https://meshtastic.org/docs/getting-started/flashing-firmware/esp32/cli-script/)).
- For **ESP32-S3** boards you may need to force download mode via the Web Flasher's **"1200bps reset"** button (the Heltec V3 generally does not require manual BOOT-button juggling; the S3 Wireless Tracker does).
- OTA: ESP32 boards support Wi-Fi OTA updates once flashed.
- Not relevant to your Heltec, but for completeness: nRF52/RP2040 boards flash by **UF2 drag-and-drop**, not esptool — and there is **no AmebaD/RTL8720 path at all**.

### Gotchas
- **BW16 (RTL8720DN / AmebaD) is unsupported** — do not plan any of your 3 BW16-Kits for Meshtastic.
- **ESP32-C5 has no official target** — its Wi-Fi6 dual-band is irrelevant to LoRa; skip it.
- **Bare classic ESP32 / ESP32-S2U / T-Display-S3 / CYD** can only run Meshtastic as a **DIY custom variant with a hand-wired SX1262/SX1276** — you currently own **no LoRa module**, so these are project boards, not flash-and-go.
- **Antenna:** your **315 MHz antennas are the wrong band** — US Meshtastic LoRa is 915 MHz; use the 915 MHz antenna that ships with the Heltec V3. NEVER power a LoRa node with no antenna (PA damage).
- **Region must be set** (US_915) before TX, or the radio stays silent/illegal.
- Releases are **Alpha** — pin a known-good tag for anything you depend on.

---

## BW16 Vampire Deauther

### What it is + version
The **Vampire Deauther** is a dual-band (2.4GHz **and 5GHz**) WiFi deauthentication firmware for the **Realtek RTL8720DN (BW16 / AmebaD)**, packaged by **vampel** as a **browser-based Web Serial flasher** at [vampel.github.io](https://vampel.github.io/) with sources at [github.com/vampel/vampel.github.io](https://github.com/vampel/vampel.github.io). It is explicitly positioned as a **Flipper Zero companion** ("Flipper Zero 2.4ghz & 5ghz deauther", topics: flipperzero, deauthentication, pentesting) and ships a Flipper app `vampire_deauther.fap` (24,596 bytes) alongside the firmware. **Version is ambiguous:** the flasher page title reads "BW16 Web Flasher **v1.31** AUTO-DOWNLOAD MODE" while the in-page header reads "**v2.4.6** Now save PCAP, AUTO-DOWNLOAD MODE" — the underlying `Vamp_FW.bin` itself carries no clearly published version stamp (see open questions). The firmware/flasher is MIT-licensed per the repo.

**Lineage:** It is functionally a **fork/repackage of tesa-klebeband's `RTL8720dn-Deauther`** ([github.com/tesa-klebeband/RTL8720dn-Deauther](https://github.com/tesa-klebeband/RTL8720dn-Deauther), GPLv3), which is itself an ESP32-Deauther port to the RTL8720dn that "allow[s] users to deauthenticate on 5GHz." **Important divergence:** the *upstream* tesa-klebeband firmware is **web-UI controlled** (hosts a WiFi AP `RTL8720dn-Deauther` / password `0123456789`, browse to `192.168.1.1`) — it is **NOT** an AT+ CLI. The **Vampire Deauther fork replaces that web UI with an AT+ serial command surface** tailored for Flipper/host control. The vampel README does not credit upstream (it is a 175-byte stub: "Vampel Proyects / Custom Board"), so the lineage is inferred, not stated.

### Chip / board it runs on
- **Realtek RTL8720DN only** (AmebaD, RTL872xDx). This is **not** Espressif silicon — it shares nothing with the ESP32 toolchain.
- **22-pin BLACK-PCB BW16 required.** The vendor page warns: *"Used black PCB 22 pins BW16(RTL8720DN). 30 pins version doesn't work properly (blue PCB)."* (per [vampel.github.io](https://vampel.github.io/)).

### Unique specialty vs the rest of your fleet
**This is the only firmware you can run that does real 5GHz deauth, and it does it over a scriptable AT+ serial CLI.** Every ESP32-based deauther/Marauder/Bruce build in your fleet is **2.4GHz-only** (Espressif radios can't TX on 5GHz). The RTL8720DN is the only chip you own (other than the Waveshare ESP32-C5 — wrong vendor, see below) that operates on 5GHz, and Vampire Deauther exposes that as plain text commands a host can drive — versus the touch-only/web-only nature of the upstream and most CYD firmwares.

### Full command / feature surface (AT+ CLI, 115200 baud)
Documented commands (from [vampel.github.io](https://vampel.github.io/)):

| Command | Action |
|---|---|
| `AT+SCAN` | Scan WiFi networks (2.4 + 5GHz) and save them to memory as an **indexed list** |
| `AT+DEAUTHIDX=<n>` | Deauth a single indexed network (press physical **RESET** to restart BW16 after) |
| `AT+DEAUTHIDX=ALL` | Deauth **all** networks in the index |
| `AT+BEACONRANDOM=Vampel` | Beacon-spam: floods SSIDs with a suffix, e.g. `Vampel 001 … Vampel 050` (up to 50) |
| `AT+STOP` | Stop current operation (note: RAM fills during deauth — a hardware RESET is often still needed) |

**LED status indicators:** solid green = BW16 ready; blinking blue = scanning; blinking red = single-network deauth; **slower** blinking red = deauth-all; blinking green = beacon spam.

Feature set is therefore: **dual-band scan → indexed targeting → single/all deauth → randomized beacon flood.** No evil-portal/captive-portal, no PMKID/handshake capture, and no client probe-sniffing are documented in the command list (some *other* RTL8720dn forks add evil-portal/beacon-flood, but those are not in this command surface).

### Host control (Cyber Controller)
**Yes — this is a genuine serial CLI, so Cyber Controller CAN drive it.** Commands are ASCII `AT+...` lines at **115200 baud** over the BW16's UART (PA26/PA25). This is a meaningful contrast with touch/web-only firmwares: a host can issue `AT+SCAN`, parse the indexed list, then fire `AT+DEAUTHIDX=ALL`. Caveats for any host integration: (1) the firmware frequently requires a **physical RESET** to recover between deauth runs (RAM exhaustion), so the host can't assume `AT+STOP` always returns it to a clean state; (2) it was designed for the Flipper Zero `.fap`, so the host should expect Flipper-style line semantics. For Flipper wiring: BW16 Pin1 3V3→Flipper Pin9, Pin2 GND→Pin18, Pin3 PA26_TXD→Pin14(RX), Pin4 PA25_RXD→Pin13(TX).

### Flashing specifics (AmebaD via Web Serial)
Flashed in-browser through the **Web Serial flasher** at [vampel.github.io](https://vampel.github.io/) (Chrome/Edge). It is an **AmebaD multi-bin flash, not a single merged ESP32-style image**. The repo ships these artifacts ([github.com/vampel/vampel.github.io](https://github.com/vampel/vampel.github.io)):
- `Vamp_FW.bin` — main firmware, **4,194,304 bytes (4MB)**
- `imgtool_flashloader_amebad.bin` — 4,688 B (AmebaD flashloader, loaded to **RAM 0x082000**)
- `km0_boot_all.bin` (4,500 B), `km4_boot_all.bin` (4,456 B) — KM0/KM4 bootloaders
- `km0_km4_image2.bin` (696,320 B), `km4_image2_all.bin` (585,728 B) — image2 partitions

Observed flasher addressing: flashloader staged at RAM `0x082000`; firmware **flash offset `0x006000`** (firmware write/RAM address `0x08000000` mapping to flash `0x000000`). Baud: **115200 default**, with an optional **1,500,000 baud** fast-flash mode. **AUTO-DOWNLOAD MODE** = the flasher auto-pulls the default firmware from GitHub if you don't pick your own files; you can alternatively select any custom Ameba RTL872xDx bins (2MB/4MB/any). To run upstream tesa-klebeband instead, it builds via **Arduino IDE + the Realtek AmebaD board package**, and most BW16 devboards require **bridging LOG_UART TX/RX to LP_UART TX/RX during upload**.

### Gotchas
- **22-pin black PCB only** — your 30-pin/blue BW16s (if any) are documented as non-working.
- **RAM fills during deauth** → expect to mash the physical **RESET** button between runs; `AT+STOP` is not guaranteed to fully recover.
- **Version strings disagree on the page itself** (v1.31 vs v2.4.6) — don't trust the page label; confirm via the serial banner.
- **"Save PCAP" is advertised but undocumented** — it may be a flasher-side log save rather than true on-device 802.11 capture (flag, don't assume).
- **No BLE features** despite the RTL8720DN supporting BLE — the command set is WiFi-only.
- **MIT repo, GPLv3 upstream, no credit given** — license/attribution hygiene is questionable; relevant if you ever redistribute or fold it into a controller.

Sources: [vampel.github.io](https://vampel.github.io/) · [github.com/vampel/vampel.github.io](https://github.com/vampel/vampel.github.io) · [github.com/tesa-klebeband/RTL8720dn-Deauther](https://github.com/tesa-klebeband/RTL8720dn-Deauther) · [RTL8720dn-Deauther README](https://github.com/tesa-klebeband/RTL8720dn-Deauther/blob/master/README.md)

---

## Flock-You

### What it is + version
**Flock-You** ([colonelpanichacks/flock-you](https://github.com/colonelpanichacks/flock-you)) is a passive **counter-surveillance detector** for **Flock Safety ALPR cameras** and **SoundThinking/ShotSpotter "Raven" gunshot sensors**. It is *source-only*: **there are no releases, no tags, no precompiled `.bin`, and no web flasher** — the repo explicitly shows "No releases published / Packages 0" ([repo](https://github.com/colonelpanichacks/flock-you), [releases](https://github.com/colonelpanichacks/flock-you/releases)). The only "versioning" is **branch names**, so pin a commit:
- **`promiscious-dev`** — current WiFi-promiscuous sniffer (adds DeFlockJoplin's 31st OUI + wildcard-probe tightening over the `promiscious` baseline).
- **`promiscious`** — older WiFi baseline.
- **`main`** — the **BLE companion firmware** (NimBLE scanner with its own phone-facing AP). ([DeepWiki](https://deepwiki.com/colonelpanichacks/flock-you))

These are **two separate firmwares** — WiFi-sniff and BLE-scan ship on different branches, not one combined build.

### Chip / board it runs best (or only) on
**Hard-targeted at the Seeed Studio XIAO ESP32-S3.** Pin map and partitions are baked into source ([README](https://github.com/colonelpanichacks/flock-you/blob/main/README.md), [DeepWiki](https://deepwiki.com/colonelpanichacks/flock-you)):
- **GPIO3** piezo buzzer, **GPIO21** onboard LED (active-low), **GPIO43** = Serial1 TX mirror @115200.
- `partitions.csv`: **6 MB app + 1.9 MB SPIFFS** (needs ≥8 MB flash).
- Native **USB-CDC** is the data path. The **BLE branch requires the S3's Bluetooth radio + NimBLE.**

There is **no TFT/screen support** in the stock firmware on either branch. A third-party guide ([simeononsecurity 2026](https://simeononsecurity.com/articles/flock-you-detection-project-counter-surveillance-hardware-guide-2026/)) loosely claims plain ESP32-WROOM works, but that conflicts with the upstream S3-only targeting and is likely conflated with other sniffer tools — treat as unverified (see open questions).

### Unique specialty vs the rest of the fleet
This is the **only Flock/ALPR-intelligence firmware** you'd run. Its value is the **curated target intelligence**, not generic sniffing:
- **31 Flock Safety MAC OUI prefixes** (e.g. `70:c9:4e`, `3c:91:80`, `d8:f3:bc`, … `82:6b:f2`).
- **BLE manufacturer ID `0x09C8` (XUNTONG)** — Will Greenberg's research, used to catch Flock BLE beacons.
- **Raven service UUIDs** sourced from GainSec's `raven_configurations.json`.
- **SSID/device-name patterns**: `flock*`, `FS_*`, `Penguin*`, `Pigvision*`, plus the `DeFlockJoplin` wildcard-probe signature.
Marauder/ESP32-DIV can sniff WiFi/BLE generically but carry **none** of this Flock fingerprint database or the GPS-mapping backend.

### Full feature / command surface
**WiFi branch (`promiscious-dev`)** — promiscuous 2.4 GHz sniff, **no AP, no TX**. Channel hop CUSTOM (1/6/11), FULL_HOP (1–11), or SINGLE; default **350 ms dwell** (`CHANNEL_DWELL_MS`). Detection methods: `wifi_wildcard_probe`, `wifi_oui_addr2` (TX-side OUI), `wifi_oui_addr1` (RX-side, @NitekryDPaul), `wifi_oui_addr3` (BSSID, off by default), `wifi_ssid` (off by default). Tunables are **compile-time `#define`s** in `main.cpp`: `RSSI_MIN -95`, `ALERT_COOLDOWN_MS 5000`, `MAX_DETECTIONS 200`, `AUTOSAVE_INTERVAL_MS 60000`. Crash-safe **SPIFFS** persistence (`/session.json`, `/session.tmp`, `/prev_session.json`, CRC32 0xEDB88320). Boot plays the **SMB World 1-2 theme**; per-hit buzzer beep + LED flash.

**BLE branch (`main`)** — **NimBLE active scan** for the OUIs/UUIDs/manufacturer-ID/name patterns above; **hosts its own WiFi AP with a phone dashboard at `http://192.168.4.1`** (no host PC needed); emits the *same Flask JSON schema* for unified mapping. ([README](https://github.com/colonelpanichacks/flock-you/blob/main/README.md))

**USB-CDC output** (one JSON line per detection):
```json
{"event":"detection","detection_method":"wifi_oui_addr2","protocol":"wifi_2_4ghz","mac_address":"aa:bb:cc:dd:ee:ff","oui":"aa:bb:cc","device_name":"","rssi":-62,"channel":6,"frequency":2437,"ssid":""}
```

### External modules it needs
**None on the ESP32 side** — it's a self-contained sniffer. **GPS is host-side, not a module on the board**: either a **USB NMEA puck plugged into the Flask host**, or the **browser Geolocation API** (phone posting to Flask). The Flask app (`cd api && pip install -r requirements.txt && python flockyou.py`, `http://localhost:5000`) does temporal GPS↔detection matching and exports **JSON/CSV/KML** (Google Earth). Your owned NRF24/CC1101/OLED/315 MHz gear is irrelevant here.

### Host control (Cyber Controller over serial)?
**Read-only, no CLI.** The device is **autonomous** — there is **no serial command interpreter**; all configuration is compile-time `#define` + reflash. A host like **Cyber Controller can passively INGEST the USB-CDC JSON stream** (115200) — exactly what the Flask dashboard does — but it **cannot drive/command the firmware** (no start/stop/channel/mode commands exist). So in your fleet it's a **listener you parse, not a device you steer.**

### Flashing specifics
**PlatformIO source build only** — no merged bin, no zip bundle, no esptool-offset trio published:
```
pio run            # build (espressif32 platform, Arduino-ESP32 core; no extra libs)
pio run -t upload  # flash over USB-C
pio device monitor # 115200 serial JSON
```
For a **T-Display-S3 or Heltec V3** you must port: confirm/edit `platformio.ini` board + flash size, match `partitions.csv` to the board's flash, remap GPIO3/GPIO21 (the XIAO LED/buzzer pins differ), and ensure **USB-CDC-On-Boot** so Flask's serial-port picker enumerates it.

### Gotchas
- **S3-only + USB-native CDC** — not portable to your classic ESP32 Gold/WROOM, **ESP32-S2U** (no BLE for the main branch), **ESP32-C5**, **CYD**, or **BW16/RTL8720DN** (AmebaD, not NimBLE) without real rework.
- **No releases/tags** → "latest" is a moving HEAD; **pin a commit** for reproducibility.
- **WiFi and BLE detection are different branches** — you can't catch both attack surfaces on one chip from one build; you'd flash two boards (e.g. one for `promiscious-dev`, one for `main`).
- **No TFT path** — flashing it to your T-Display-S3 leaves the ST7789 dark unless you fork in display code.
- Detection is **2.4 GHz only**; despite owning dual-band C5/BW16, this firmware can't exploit 5 GHz, and those chips can't run it anyway.

---

## OUI-Spy

### What it is + version
OUI-Spy is a passive, detection-only RF-surveillance awareness firmware for the ESP32-S3, written by Colonel Panic (`colonelpanichacks`). It started as a slick BLE scanner / "foxhunting" handset and grew into a multi-mode surveillance-detection suite. The flagship build is **OUI-SPY Unified Blue**, which packs four modes into one binary selectable from a WiFi boot menu — no reflashing to switch modes ([repo](https://github.com/colonelpanichacks/oui-spy-unified-blue), [README](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/README.md), [ecosystem hub](https://github.com/colonelpanichacks/oui-spy)).

**Version caveat:** there is **no released version number**. As of research (June 2026) `oui-spy-unified-blue` has **zero GitHub releases/tags** — "Unified Blue" is the build name, not a semver. Pin your build by commit hash, not a version string. The project got mainstream coverage in late September 2025 ([Hackaday, 2025-09-26](https://hackaday.com/2025/09/26/detecting-surveillance-cameras-with-the-esp32/); [Hackster](https://www.hackster.io/colonelpanic/oui-spy-now-and-beyond-1f9c9a)).

### Chip / board it runs best (or only) on
**ESP32-S3 only**, and specifically built around the **Seeed Studio XIAO ESP32-S3** pinout. The dedicated OUI-Spy hardware sold at colonelpanic.tech / Tindie is a XIAO-S3 carrier with an integrated PWM piezo buzzer and a NeoPixel ([Tindie](https://www.tindie.com/products/colonel_panic/oui-spy/)). The unified firmware hardcodes:

| GPIO | Function |
|------|----------|
| 3 | Piezo buzzer (PWM) |
| 21 | NeoPixel LED |
| 0 | BOOT button (hold 2 s to return to mode selector) |

The classic ESP32 (WROOM-32), ESP32-S2, and Realtek BW16 cannot run it (wrong SoC). The ecosystem README also references **ESP32-C5** builds for the Unified and Sky-Spy variants (dual-band, attractive for 5 GHz drone RemoteID), but that is a separate target, not the XIAO-S3 bin.

### Unique specialty vs the rest of the fleet
This is the fleet's **named-target surveillance detector**. Where Marauder / ESP32-DIV / Bruce show anonymous MACs, OUI-Spy ships curated heuristics that *identify the infrastructure*:
- **Flock-You mode:** Flock Safety ALPR cameras and Raven gunshot detectors via **42+ MAC prefixes, BLE device-name patterns, manufacturer ID `0x09C8`, and Raven service UUIDs** — technique derived from the DeFlock project, with findings submittable to deflock.me ([Hackaday](https://hackaday.com/2025/09/26/detecting-surveillance-cameras-with-the-esp32/)).
- **Sky-Spy mode:** passive **FAA Remote ID / ASTM F3411 (ODID)** drone detection over WiFi beacon + BLE, extracting drone serial, operator/UAV ID, GPS, altitude, speed, heading.

No other firmware you run does targeted ALPR / Raven / RemoteID attribution. It pairs naturally with the BW16 for raw dual-band capture and Marauder for general wardriving, but OUI-Spy is the one that tells you *what* the device is.

### Full feature / command surface (Unified Blue, 4 modes)
1. **Detector** — multi-target BLE scanner; alert on OUI prefix, full MAC, or device-name pattern. Web dashboard at `192.168.4.1`, AP `snoopuntothem` / `astheysnoopuntous`. NeoPixel + buzzer alerts, smart cooldown.
2. **Foxhunter** — RSSI radio-direction-finding on a single locked MAC; buzzer cadence speeds up as you close in. AP `foxhunter` / `foxhunter`; manual or auto target select. (A 2.4 GHz directional SMA antenna dramatically improves this — see [Hackster foxhunter writeup](https://www.hackster.io/news/colonel-panic-s-oui-spy-is-a-slick-bluetooth-low-energy-scanner-or-a-foxhunting-handset-c16927adad71).)
3. **Flock-You** — Flock/Raven detection (above). JSON + CSV export (MAC, name, RSSI, detection method, timestamps, count, Raven status, firmware version, GPS). Browser-Geolocation GPS wardriving, KML/CSV export, session persistence in SPIFFS/LittleFS, up to **200 unique devices** (FreeRTOS-mutex protected). AP `flockyou` / `flockyou123`.
4. **Sky-Spy** — drone RemoteID (above). **No AP — serial JSON output only**, designed for ingestion by a companion Flask dashboard; dedicated FreeRTOS buzzer task.

**Boot selector** is a WiFi AP `oui-spy` / `ouispy123` at `192.168.4.1`: pick a mode, reboot, go. Per-boot MAC randomization (stealth), persistent mode memory, distinct boot sounds per mode, and a global buzzer mute toggle.

**Adjacent standalone firmwares** in the same family (separate bins, same hardware): **UniPwn** (Unitree-robot BLE command injection, AES-CFB128 — *active, not passive*), **Remote-ID-Spoofer** (RemoteID/swarm simulator with Flask UI — carries a legal-transmission disclaimer), and Luke Switzer's **OUIspy Omni** fork (7 engines concurrent, BLE-GATT mobile app control, 39k-entry OUI DB, WiGLE export, geofencing) ([oui-spy hub](https://github.com/colonelpanichacks/oui-spy)).

### External modules it needs
**None required.** Buzzer, NeoPixel, WiFi, and BLE are all onboard the dedicated OUI-Spy/XIAO-S3 hardware. The only optional add-on that materially helps is a **2.4 GHz directional SMA antenna** for Foxhunter (you own IPEX→SMA pigtails and 315 MHz antennas — note the 315 MHz antennas are the wrong band; you'd need a 2.4 GHz directional). No CC1101 / NRF24 / PN532 are used or supported.

### Host control over serial — can Cyber Controller drive it?
**No real inbound CLI.** OUI-Spy is **emit-only over serial**: Sky-Spy and Flock-You *stream JSON out* (for a Flask host to ingest), but I found **no evidence of an inbound serial command parser**. Mode selection and all configuration happen over the **WiFi captive portal / web dashboard** or the physical **BOOT button**, not over a serial CLI. So a host like Cyber Controller can usefully act as a **serial JSON reader/logger** (tail the Sky-Spy / Flock-You stream, forward to a map or Flask), but it **cannot drive or reconfigure the firmware over serial** the way it can with a Marauder-style CLI. Baud rate / USB-CDC settings are undocumented — sniff on hardware. (Omni fork adds BLE-GATT app control, but that's BLE, not serial, and a different firmware.)

### Flashing specifics
Flashing is via a **Python esptool wrapper** (`flash.py`) in the repo root — **no web flasher (no ESP Web Tools / esptool-js) and no single merged bin** published. It writes the standard 4-file ESP32-S3 layout ([README](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/README.md)):

| File | Offset |
|------|--------|
| `bootloader.bin` | `0x0000` |
| `partitions.bin` | `0x8000` |
| `boot_app0.bin` | `0xe000` |
| `oui-spy-unified-blue.bin` | `0x10000` |

Custom partition table (~6 MB app + ~2 MB LittleFS for detection logs). Commands: `pip install -r requirements.txt` (Python 3.8+, esptool, pyserial), then `python3 flash.py` (auto-detects/confirms), `--batch` (hands-free multi-board), `--erase`, or `--batch --erase` for production runs. Success = **4 ascending boot beeps**. Built with PlatformIO (NimBLE-Arduino, ESPAsyncWebServer + AsyncTCP, ArduinoJson, Adafruit NeoPixel).

### Gotchas
- **No version / no releases** — pin to a commit hash.
- **XIAO-S3 pinmap is hardcoded** (buzzer GPIO 3, NeoPixel GPIO 21). On a non-XIAO S3 board the buzzer/LED will be silent/dead unless you rebuild with remapped pins.
- **No TFT/display driver** — the firmware is headless+web; it will not light up the T-Display-S3 / ST7796 / ILI9341 screens.
- **AP auto-rejoin trap:** after switching modes your phone/laptop auto-joins the *previous* mode's saved AP — forget old networks first.
- **GPS wardriving is Android-Chrome-only:** iOS Safari won't do Geolocation over HTTP; Android Chrome needs the `chrome://flags` "insecure origins" override to allow GPS at `http://192.168.4.1`.
- **Data USB cable required** (not charge-only).
- **Per-boot MAC randomization** — your device's MAC changes every boot (good for stealth, surprising in logs).
- **Active-mode siblings** (UniPwn, Remote-ID-Spoofer) leave the passive umbrella and carry legal risk — keep them mentally separate from the detection-only Unified Blue build.

Sources: [oui-spy hub](https://github.com/colonelpanichacks/oui-spy) · [Unified Blue repo](https://github.com/colonelpanichacks/oui-spy-unified-blue) · [Unified Blue README](https://github.com/colonelpanichacks/oui-spy-unified-blue/blob/master/README.md) · [Hackaday](https://hackaday.com/2025/09/26/detecting-surveillance-cameras-with-the-esp32/) · [Hackster — Now and Beyond](https://www.hackster.io/colonelpanic/oui-spy-now-and-beyond-1f9c9a) · [Hackster — scanner/foxhunter](https://www.hackster.io/news/colonel-panic-s-oui-spy-is-a-slick-bluetooth-low-energy-scanner-or-a-foxhunting-handset-c16927adad71) · [Tindie](https://www.tindie.com/products/colonel_panic/oui-spy/)

---

## Sky-Spy

**What it is:** Sky-Spy is the "official OUI-SPY firmware for drone RemoteID detection and mapping" by Colonel Panic ([github.com/colonelpanichacks/Sky-Spy](https://github.com/colonelpanichacks/Sky-Spy)). It is a passive **drone Remote ID detector**: it listens for the FAA/ASTM F3411 **OpenDroneID** broadcasts that compliant drones are required to transmit, decodes them, and streams the results as JSON over USB serial. It is the fleet's dedicated counter-UAS / airspace-awareness sensor — nothing else you own does this.

**Version:** No tagged release. There are **no GitHub Releases, no prebuilt/merged binary, and no web flasher** — the repo is main-branch source only, built with PlatformIO. Treat "version" as "current `main`" and pin a commit hash for reproducibility. Repo language mix is ~53% Python (the host mapper) / ~40% C / ~8% C++ ([repo root](https://github.com/colonelpanichacks/Sky-Spy)).

**Chip / board it runs best on:**
- **Mainline build = ESP32-S3.** The root `platformio.ini` defines exactly one environment, `[env:seeed_xiao_esp32s3]` (board `seeed_xiao_esp32s3`, Arduino framework on the `pioarduino` Espressif32 platform, `-std=gnu++17`, ArduinoJson `^6.18.5`, 115200 monitor/upload) ([platformio.ini](https://raw.githubusercontent.com/colonelpanichacks/Sky-Spy/main/platformio.ini)). The README also names the **Seeed XIAO ESP32-C6** as an "alternative," but that env is NOT in the root ini — see open questions.
- **Dual-band build = ESP32-C5.** There is a separate sub-project, **`xiao-c5-5g/`**, whose own `platformio.ini` targets `board = esp32c5` with `-DARDUINO_XIAO_ESP32C5` and `-DBOARD_HAS_PSRAM` (and keeps a legacy `seeed_xiao_esp32s3` env) ([xiao-c5-5g/platformio.ini](https://raw.githubusercontent.com/colonelpanichacks/Sky-Spy/main/xiao-c5-5g/platformio.ini)). This is the variant that matters for catching **5GHz** Remote ID.

**Why the C5 variant is the unique specialty (vs the rest of the fleet):** Drones broadcast WiFi Remote ID on the 2.4GHz "social" channel 6 **and** on 5GHz channel 149, plus BLE. A 2.4GHz-only radio (classic ESP32, S2, S3, C6) physically cannot hear the 5GHz-only WiFi NaN/Beacon broadcasts ([Remote ID band/channel refs: btframework.com](https://www.btframework.com/droneremoteid.htm), [dronescout.co](https://dronescout.co/dronescout-remote-id-receiver/)). The `xiao-c5-5g` build on an ESP32-C5 (WiFi 6, native dual-band 2.4+5GHz) is therefore the **only configuration in your entire firmware fleet that can see 5GHz WiFi Remote ID**. That is the one thing no other board/firmware combo you own does.

**Detection method / feature surface** (from [README](https://github.com/colonelpanichacks/Sky-Spy)):
- **Dual-protocol scanning, dual-core:** Core 0 runs **WiFi promiscuous mode** (802.11 beacon/probe frames, parses OpenDroneID **NAN action frames**, listens on **channel 6**); Core 1 runs **BLE** (active scan, 100ms interval, 1s scan duration, **service UUID 0xFFFA** = Remote ID), plus JSON output and the buzzer task.
- **OpenDroneID fields decoded:** Basic ID (drone serial / CAA registration), Location (lat/long, altitude, speed, heading), System (operator/pilot location), Operator ID.
- **Multi-drone tracking** simultaneously.
- **Audio alerts (non-blocking FreeRTOS buzzer task):** detection = 3 quick beeps @ 1000 Hz; heartbeat = double beep @ 600 Hz every 5s; heartbeat auto-stops after 7s with no detection.
- **Range:** "200-500m depending on conditions." Caveats: Remote ID may not be mandated locally and **not all drones broadcast it**.

**Serial / host-control surface — is it a real CLI or output-only?** Effectively **output-only telemetry**, NOT an interactive CLI. It emits one JSON object per detection at **115200 baud**, e.g.:
```json
{"mac":"aa:bb:cc:dd:ee:ff","rssi":-45,"drone_lat":37.7749,"drone_long":-122.4194,"drone_altitude":120,"pilot_lat":37.7750,"pilot_long":-122.4195,"basic_id":"1234567890ABCDEF"}
```
plus a periodic status/keepalive line (~every 60s). The companion host **`mesh-mapper.py`** is a full Flask + Socket.IO web app (Leaflet map, CSV/KML logging, FAA registration lookups, webhooks) that **ingests** this JSON from one or more USB receivers ([mesh-mapper.py](https://raw.githubusercontent.com/colonelpanichacks/Sky-Spy/main/mesh-mapper.py)). It does write a single `WATCHDOG_RESET\n` line to the port on connect, but there is **no documented interactive command set** — so **Cyber Controller cannot "drive" Sky-Spy like a CLI firmware**; it can only open the port, optionally send that watchdog kick, and **parse/forward the JSON stream**. For your stack, treat Sky-Spy as a sensor whose serial JSON you consume, not a device you command.

**External modules needed:** Minimal. **Passive buzzer optional**, on **GPIO3 (D2, PWM)** — buzzer+ to GPIO3, buzzer- to GND (`#define BUZZER_PIN 3`, freqs at lines 24-27, heartbeat interval ~line 397). **No GPS module needed** (drone + pilot GPS come from the Remote ID payload itself). **No display** — output is serial JSON only. So none of your OLEDs, NRF24, CC1101, or antennas are required; an external **915MHz/5GHz-capable antenna helps range** on boards with IPEX (your C5 / Heltec).

**Flashing specifics:** PlatformIO source build only — **no merged bin, no .zip bundle, no offsets table, no AmebaD, no web installer.**
- S3: `pio run -e seeed_xiao_esp32s3 -t upload`
- C5 dual-band: build from inside `xiao-c5-5g/` with the `esp32c5` env (`pio run -e seeed_xiao_esp32c5 -t upload`).
PlatformIO auto-detects the port and handles the bootloader/offsets behind esptool; there is no manual `0x10000` app-offset step documented. RAM/flash footprint is light (~21% RAM, ~43% of a 4MB app partition).

**Gotchas:**
- **No releases / no flasher** — you must compile. Use the `pioarduino` platform (not stock `platform-espressif32`) so the toolchain is new enough for ESP32-C5.
- **ESP32-S2 (your 3x S2U) cannot run this usefully** — S2 has no Bluetooth, killing half the detection (BLE 0xFFFA). 2.4GHz-only boards (classic ESP32, S3, C6) also **miss 5GHz Remote ID**.
- **BW16 (Realtek RTL8720DN / AmebaD) is out of scope** — Sky-Spy is Arduino-ESP32; it will not build for Realtek.
- **C5 env name says "Seeed XIAO," your C5s are Waveshare** — pinout, USB-CDC, PSRAM (`-DBOARD_HAS_PSRAM`), and the GPIO3 buzzer may differ; verify before trusting the buzzer or assuming a clean flash.
- **5GHz scanning is inferred** from the C5 hardware + the variant's name; no explicit channel-149 build flag is present in the ini, so confirm on real hardware that it actually listens on 5GHz, not just 2.4GHz ch6.

---

## AirTag Scanner

### What it is + version
**ESP32-AirTag-Scanner** ([github.com/MatthewKuKanich/ESP32-AirTag-Scanner](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner)) is a single-file Arduino firmware whose entire job is to passively scan BLE and surface Apple **FindMy / AirTag** beacons — "*Scan for AirTag MACs and Payloads without the need for an Android device or nrfConnect*." It is the ESP32 companion to the same author's **FindMyFlipper** app: you use it to harvest a real tag's MAC + raw payload so they can be cloned/imported into a Flipper FindMy beacon.

**Version: there is none.** The repo has **no releases and no tags** (only ~5 commits on `main`) — pin the commit SHA you flash, because "latest" is just HEAD. Source: [repo root](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/tree/main), 100% C++ ([repo](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner)).

### Chip/board it runs best (or only) on
Pure Arduino-ESP32 BLE code using `<BLEDevice.h> / <BLEScan.h> / <BLEAdvertisedDevice.h>` ([AirTag_Scanner.ino](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/blob/main/AirTag_Scanner.ino)). The repo ships **two prebuilt binary sets** in `ESP32-WROOM/` and `ESP32-S3/` folders ([tree/main](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/tree/main)). It runs **best on a classic ESP32-WROOM** — it's headless, needs only the BLE radio, and any cheap WROOM does the job. S3 is the only other official target. There is **no display or button code at all**, so screen boards gain nothing.

### UNIQUE specialty vs the rest of the fleet
Unlike Marauder / ESP32-DIV (broad recon suites), this firmware does exactly one thing extremely well: it dumps the **full raw Apple manufacturer-data hex payload** alongside MAC + RSSI, which is the clone-ready artifact FindMyFlipper consumes. It filters on **Apple company ID 0x4C** using two payload signatures — `1E FF 4C 00` (Apple continuity prefix) and `4C 00 12 19` (FindMy / offline-finding frame, type 0x12, len 0x19) ([.ino source](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/blob/main/AirTag_Scanner.ino)). Nothing else in your fleet hands you import-ready FindMy payloads out of the box.

### Full feature / command surface
- **Active BLE scan**: `setActiveScan(true)`, interval **100 ms**, window **99 ms**, **1-second** scan cycles, looping continuously.
- **Per-hit serial output**: prints `AirTag found!`, a sequential count, the **MAC address**, **RSSI (dBm)**, and a complete **raw hex payload dump**.
- **Dedup cache**: tracks seen devices so each tag is reported once until cleared.
- **Serial baud: 115200**.

### Host/CLI control surface — IS serial-driveable
This is genuinely host-driveable, not touch/button-only. The firmware reads `Serial.available()` and accepts **one newline-terminated command: `rescan`**, which clears the device cache and resets the counter to restart detection ([.ino source](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/blob/main/AirTag_Scanner.ino)). So a host controller (e.g. **Cyber Controller**) at 115200 baud can read the tag stream and issue `rescan` — a minimal but real CLI. There is **no display driver and no GPIO/button handler** in the code; output is serial-only.

### External modules needed
**None.** Uses only the ESP32's built-in BLE radio. No CC1101 / NRF24 / PN532 / SX1262 / antenna module required. (Your IPEX→SMA pigtails are only relevant for raw RF range on the IPEX WROOM boards, not functionally needed.)

### Flashing specifics
**Not a merged bin and not a release zip** — it's the classic **3-file app+bootloader+partitions** layout per board folder ([README](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/blob/main/README.md)):
1. `airtag_scanner.ino.bootloader.bin`
2. `airtag_scanner.ino.partitions.bin`
3. `airtag_scanner.ino.bin`

The documented path is the **Flipper Zero ESP Flasher** (Apps > GPIO > Manual Flash; files under `apps_data/esp_flasher/`), and you toggle **"Select if using S3"** for the S3 variant — but **you do NOT own a Flipper**, so flash with **esptool** instead, using the standard ESP32 offsets: **bootloader 0x1000, partitions 0x8000, app 0x10000** ([esptool flashing guide](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/flashing-firmware.html)). On classic WROOM this is correct; **on ESP32-S3 the bootloader offset is 0x0, not 0x1000** ([ESP-IDF bootloader docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/bootloader.html)) — verify the S3 prebuilt's offset before flashing or you'll boot-loop. Enter download mode with **hold BOOT + tap RESET + release BOOT**. This is **not AmebaD** — no relevance to your BW16 boards.

### Gotchas
- **No screen.** On your T-Display-S3 / CYD / AITRIP the TFT stays dark; it's serial-only. Use a plain WROOM.
- **Apple-only, unconfirmed for SmartTag/Tile.** Issue #3 asks about Samsung SmartTag / Tile and is **unanswered**; the source has no non-Apple manufacturer filter, so treat it as **Apple FindMy only** ([issue #3](https://github.com/MatthewKuKanich/ESP32-AirTag-Scanner/issues/3)).
- **ESP32-S2 = no Bluetooth.** Your **ESP32-S2U** boards almost certainly cannot run this — S2 silicon lacks a BLE radio. Verify before wasting a flash.
- **C5 / BW16 not supported** without a from-source port (C5 isn't a build target; BW16 is Realtek/AmebaD, a different SDK entirely).
- **No version pinning** — record the commit SHA you build from.

---

## Minigotchi (dj1ch/minigotchi-ESP32)

**What it is + version.** Minigotchi-ESP32 is the ESP32 port of dj1ch's "Minigotchi" — a tiny, autonomous Pwnagotchi-style WiFi gadget written in C/C++ for the Arduino-ESP32 framework. It does low-level 802.11 frame work (channel-hopping, beacon/advertisement injection, deauthentication) and replicates the Pwnagotchi's peer-detection ("friend") system, but it is a clean-room reimplementation: the real Pwnagotchi is Python/Go and is *not* code-compatible. Latest release is **v3.6.4-beta** (Dec 23, 2025); the config file also stamps `version = "3.6.4-beta"`. It is explicitly beta and updated sporadically. Source: <https://github.com/dj1ch/minigotchi-ESP32>, <https://github.com/dj1ch/minigotchi-ESP32/releases>.

**Chip/board it runs best (or only) on.** Requirement is hard and simple: **"any ESP32-S* or ESP32* based microcontroller (must have two cores)."** That means classic dual-core ESP32 (WROOM-32/WROOM-32E) is the reference target, with dual-core ESP32-S2 and ESP32-S3 also valid. Single-core parts and non-ESP32 silicon are out. Sources: <https://github.com/dj1ch/minigotchi-ESP32> (README), <https://github.com/dj1ch/minigotchi-ESP32/blob/main/INSTALL.md>.

**Unique specialty vs the rest of the fleet.** This is the only firmware you run that *participates in the Pwnagotchi ecosystem*. Two distinct modes matter:
- **Advertise/scan ("friend") mode:** it broadcasts Pwnagotchi-format advertisements and detects nearby Pwnagotchis, other Minigotchis, and Palnagotchis on a shared channel set.
- **Parasite mode:** wired to a full Raspberry-Pi Pwnagotchi over **serial** (with the companion *minigotchi* plugin installed on the Pi), the ESP32 acts as an extra radio/sensor feeding the Pi. The docs specifically tell you to match your Pwnagotchi's `personality.channels[]` in `/etc/pwnagotchi/config.toml` to the Minigotchi's `Config::channels[13]` so the two find each other. Nothing else in your fleet (Marauder, GhostESP, ESP32-DIV, BW16 firmwares) speaks this protocol. Sources: <https://github.com/dj1ch/minigotchi-ESP32/blob/main/INSTALL.md>, search corroboration on parasite mode + channel matching.

**Full feature/command surface.** Features are compile-time toggles in `config.cpp` (defaults shown):
- `deauth = true` — deauthenticate stations off an AP (honors a **whitelist** so your own SSIDs are skipped; default whitelist is placeholder `{"SSID","SSID","SSID"}`).
- `advertise = true` — emit Pwnagotchi-style advertisements (the "be a friend" behavior).
- `scan = true` — sniff/detect Pwnagotchi/Minigotchi/Palnagotchi peers.
- `spam = true` — beacon/BLE spam (BLE spam is documented as effective against iOS popups; BLE requires a chip with Bluetooth).
- `parasite = false` — serial link to a host Pwnagotchi (off by default).
- WiFi country `"US"`, channels `{1..13}`, initial channel `1`, baud `115200`.
- Behavioral randomization: AP TTL 30–600 s, station TTL 60–300 s, recon 5–60 s, min-RSSI −200…−50 dBm, max interactions 1–25 — i.e. it behaves "organically" rather than hammering.
- Personality: `name = "minigotchi"`, default face `(^-^)`.

There is **no interactive command menu**. The device runs autonomously after boot; behavior is governed entirely by the flashed config and the one-time web portal below. Sources: `config.cpp` / `config.h` in the repo tree.

**External modules it needs.** None required. It is self-contained WiFi/BLE on the SoC. It does **not** need CC1101, NRF24, PN532, or an SX12xx; on your Heltec V3 the LoRa radio simply goes unused. No GPS module is referenced anywhere in INSTALL/config — so despite third-party "wardriving" blurbs, treat it as passive WiFi observation, not geo-tagged wardriving (flagged in open questions). A display is optional (see below).

**Host control surface — can Cyber Controller drive it over serial? No (not as a CLI).** Minigotchi exposes **two non-interactive serial uses only**: (1) boot/status logging at 115200, and (2) *outbound* parasite data to a Pwnagotchi plugin. There is no inbound command parser, no menu, no "scanap/attack" verbs to send. So a host like **Cyber Controller cannot drive it like it drives Marauder/GhostESP** — you can open the port to watch logs, but you cannot issue commands. Configuration is done instead through a **one-time WiFi web portal**: on first boot it raises a SoftAP (**SSID `minigotchi` / `minigotchi 2`, password `dj1ch-minigotchi`**); browse to **http://192.168.4.1**, enter your whitelist (comma-separated SSIDs), then set the last text box to `true` to turn the WebUI off and lock in settings. After that it's headless-autonomous (plus optional on-device screen). Sources: <https://github.com/dj1ch/minigotchi-ESP32/blob/main/INSTALL.md>; parasite/serial corroboration from project docs and search.

**Displays (optional, compile-time).** `config.h` gates the screen with master `disp` plus one library define, all defaulting to 0: `SSD1306`, `SSD1305`, `SH1106`, `IDEASPARK_SSD1306`, `WEMOS_OLED_SHIELD`, `CYD`, `T_DISPLAY_S3`, `M5STICKCP`, `M5STICKCP2`, `M5CARDPUTER`, `M5ATOMS3`, `M5ATOMSR3`. So the Pwnagotchi face renders on the CYD and the LILYGO T-Display-S3 directly. Source: `config.h`.

**Flashing specifics (the part that bites people).** This is an **Arduino-IDE source build**, not a clean merged-bin/zip drop:
- Tool: Arduino IDE. Select an `esp32` board (e.g. an ESP32 / Feather ESP32-S3 TFT entry). Enable **Tools > Erase All Flash Before Sketch Upload**.
- **Board-package version is a known landmine.** The docs target esp32 core **`2.0.10`**, where you must patch `platform.txt` to add `-w` and `-zmuldefs` compiler flags. Core **>3.0.1** additionally needs `-zmuldefs` added to multiple per-chip `ld_flags` files and is called out as **WIP / may not compile**. Budget time for this; it's the #1 build failure.
- Libraries: ArduinoJson, Adafruit GFX, AsyncTCP, and a **custom fork of ESPAsyncWebServer** (the stock one won't do), plus the display lib for your chosen screen (Adafruit SSD1306 / TFT_eSPI / M5Unified / u8g2 as applicable).
- Output: you can `Sketch > Export Compiled Binary` to get a `.bin` for manual/esptool flashing, but there is **no official prebuilt merged firmware or web flasher**, and (as of this writing) the v3.6.4-beta release asset list failed to enumerate — assume build-from-source.
- Flipper Zero WiFi-dev-board users set `#define fz 1` to disable BLE; you don't own a Flipper so ignore. There is **no AmebaD/RTL path** — this firmware does not touch your BW16 boards.

Sources: <https://github.com/dj1ch/minigotchi-ESP32/blob/main/INSTALL.md>, repo `config.cpp`/`config.h`.

**Gotchas / map to your boards.**
- **Run it on:** Lonely Binary ESP32 Gold ×3 + ESP-WROOM-32 (ideal headless parasite/friend nodes), **T-Display-S3** (best face-on-screen build, `T_DISPLAY_S3`), and both **CYD 2.8"** (`CYD`).
- **Marginal:** ESP32-S2U ×3 — dual-core so it qualifies, but **no Bluetooth on S2** means BLE spam is dead weight; fine as WiFi-only/parasite nodes. Heltec LoRa V3 runs as a plain headless ESP32-S3 node (LoRa/OLED unused).
- **Won't run:** **ESP32-C5 ×2** (single-core RISC-V → fails the two-core rule, no dual-band benefit here anyway since it's a 2.4 GHz Pwnagotchi protocol), **BW16/RTL8720DN ×3** (not ESP32). AITRIP 4" ST7796 has no display define — headless-only unless you hand-wire a TFT_eSPI config (untested).
- The web portal SSID/password are hard-coded defaults (`minigotchi` / `dj1ch-minigotchi`) — change-of-config requires re-entering the portal, since there's no live serial control.
- Deauth is active and illegal against networks you don't own — the whitelist only protects *your* listed SSIDs from your own device, not bystanders. Keep it to your bench.

---

## Flipper (Momentum / Unleashed)

### What it is + latest version
"Flipper firmware" here means two community custom firmwares (CFW) for the **Flipper Zero**, both forks of Flipper Devices' Official Firmware (OFW):

- **Unleashed** (DarkFlippers) — the long-running "stability + unlocked RF" fork. Latest stable: **unlshd-089**, API 87.8, released ~May 2026. ([repo](https://github.com/DarkFlippers/unleashed-firmware), [unlshd-089 tag](https://github.com/DarkFlippers/unleashed-firmware/releases/tag/unlshd-089))
- **Momentum** (Next-Flip) — the feature-rich, heavily-customizable fork; the spiritual successor to Xtreme, and it pulls in most of Unleashed's unlocks on top. Latest stable: **mntm-012**, released **2025-12-31** (with rolling dev builds after, e.g. ~Mar 2026). ([repo](https://github.com/Next-Flip/Momentum-Firmware), [momentum-fw.dev](https://momentum-fw.dev/releases/mntm-012))

Rule of thumb: **Unleashed = lean + maximal RF unlock; Momentum = Unleashed's unlocks PLUS UI customization, asset packs, and extra apps.** Both are free/open-source and not affiliated with Flipper Devices.

### Chip / board it runs on (this is the big caveat for your fleet)
Flipper firmware runs **only on Flipper Zero hardware ("F7")**, built around an **STM32WB55RG** — ARM Cortex-M4 @ 64 MHz (app) + Cortex-M0+ @ 32 MHz (radio/BLE), 1024 KB flash, 256 KB SRAM. ([tech specs](https://docs.flipper.net/zero/development/hardware/tech-specs)) The radios are discrete onboard chips:
- **Sub-1 GHz:** TI **CC1101**, up to 20 dBm, bands 315 / 433 / 868 / 915 MHz
- **NFC/HF:** ST **ST25R3916** @ 13.56 MHz (ISO14443A/B, MIFARE, FeliCa, iClass)
- **125 kHz LF RFID** coil (EM4100, HID H10301, Indala…)
- **IR** (38 kHz RX / 940 nm TX), **iButton/1-Wire** (Dallas, Cyfral, Metakom), **BLE 5.x** via the WB55's M0+ core, 13 GPIO @ 3.3V (5V-tolerant).

**This is an STM32 target, not Espressif or Realtek.** Therefore **none of your owned boards run it** — not the WROOM-32E/ESP32-S2U/S3, not the C5, CYD, Heltec, and not the BW16 (RTL8720DN). Flipper is on your "not owned yet" list, so this dossier entry is **buy-hardware-first**, not flash-to-an-owned-board. (Your BW16 dual-band+BLE and Heltec SX1262 cover *adjacent* RF turf, but with entirely different firmware.)

### Unique specialty vs the rest of the fleet
The Flipper's edge is **integration in one battery-powered handheld with a screen**: it is the only platform in scope that does **sub-GHz capture/replay/brute-force + 13.56 MHz & 125 kHz card cloning/emulation + IR + iButton** together, with the CFWs **removing the OFW's regional TX restrictions** and letting you extend the frequency table in a settings file (hardware-damage caveat). Your ESP32/BW16 boards are Wi-Fi/BLE/2.4-GHz-centric (Marauder-class); the Flipper owns the **access-control and OOK/FSK sub-GHz cloning** lane that those boards do not.

### Feature / command surface
Shared CFW surface (Unleashed + Momentum):
- **Sub-GHz:** read/save/emulate, Read RAW, Frequency Analyzer, Bruteforce/Sub-Brute, custom frequency add, extended rolling-code protocol support (e.g., FAAC SLH, Keeloq variants) with "save & capture" on more protocols. Regional TX limits removed.
- **NFC / RFID:** read/emulate/save, Mifare fuzzers, EMV parser, 125 kHz LF cloning.
- **IR:** universal remotes + learned remotes. **iButton/1-Wire** read/write/emulate.
- **BadUSB / BadKB** (USB + BLE HID injection) with keyboard layouts; **TOTP** authenticator; barcode/converter tools; pin-lock; clock; custom device name.

**Momentum-only extras** (on top of the above): the **Momentum settings app**, **BLE Spam**, **FindMy Flipper** (Apple/Google tag beaconing), **NFC Maker**, **Wardriver**, **Bad-Keyboard**, **Asset Packs** (theming), expanded **JavaScript** API, SD file search, file cut/copy/paste, disk-image tools, desktop keybinds, RGB-backlight modes (for hardware-modded units), and Video Game Module color config. ([Momentum README](https://github.com/Next-Flip/Momentum-Firmware))

### External modules
The Flipper is self-contained, but the GPIO header accepts add-ons that both CFWs support: **external CC1101 board** (hardware-SPI, with amplifier/LED control — extends sub-GHz range), **NRF24L01** (Mousejack/2.4 GHz plugins — you already own NRF24 adapters), **ESP32/ESP8266 "WiFi Devboard"** (Marauder/deauther + the Wi-Fi side of attacks), **ESP32-CAM**, **GPS (NMEA)** for wardriving, plus I²C/temp sensors. Note: the Flipper's *own* CC1101 is fixed at 315/433/868/915 MMHz; the external CC1101 mod is what people add for gain/range, not new bands.

### Host control over serial (Cyber Controller relevance)
**Yes — unlike most touch/button-only ESP32 firmwares, the Flipper exposes a genuine interactive text CLI over USB CDC serial at 230400 baud.** ([CLI docs](https://docs.flipper.net/zero/development/cli)) `?` / `help` lists commands; categories include `info device`/`info power`, `storage` (list/read/write), `subghz` (`rx`, `rx_raw`, `tx`, `tx_from_file`, `decode_raw`, `chat`), `nfc` (dump/emulate/raw), `ir` (rx/tx/decode), `ikey`/`ibutton`, `gpio`, `bt`, `vibro`/`led`/`buzzer`, `loader`, `log`, `update`. There is also a binary **RPC (protobuf)** mode that qFlipper / the mobile apps use. So a host like **Cyber Controller could in principle drive a Flipper over serial** — but the protocol (Flipper CLI / RPC at 230400) is **different from the ESP32 firmwares your controller already speaks**, so it would need a Flipper-specific serial profile. Untested here since no Flipper is owned (see open questions).

### Flashing specifics
Flipper firmware is **NOT** an ESP32-style merged-bin-at-offsets or AmebaD image. It ships as a **`.tgz` update package** (firmware + updater + assets/IR libs/animations bundled) installed via:
- **Web updater / Flipper Lab** (Chromium WebSerial) — recommended,
- **qFlipper** desktop app, or
- **mobile app** over BLE.

Naming: `flipper-z-f7-update-<fw>-<ver>.tgz`. Variant suffixes drift between releases — **Unleashed currently uses `c` (base apps only) and `e` (base + extra apps)**; older builds had `n` (official animations only) and `r` (RGB-mod patch). ([unlshd-089 assets](https://github.com/DarkFlippers/unleashed-firmware/releases/tag/unlshd-089)) The `.tgz` extracts onto the SD/internal storage; you do **not** flash raw offsets like you do on the WROOM/CYD boards.

### Gotchas
- **STM32, not ESP32** — zero overlap with your existing flashing toolchain; qFlipper/WebSerial, not esptool.
- **Regional TX unlock is on you** — extending the frequency table can exceed CC1101/antenna limits and is a legal/hardware risk.
- **Stay on tagged stable** (unlshd-089 / mntm-012); nightly/dev auto-builds float and one June-2026 Unleashed timestamp I saw is a dev build, not a new stable.
- **CFW API lock-step:** external apps (.fap) must match the firmware's API version (Unleashed 089 = API 87.8); mismatched .fap won't load.
- Pick **Momentum** if you want the kitchen-sink app set + theming; pick **Unleashed** if you want the leanest, most-vetted RF-unlock base.

Sources: [Unleashed repo](https://github.com/DarkFlippers/unleashed-firmware), [unlshd-089 release](https://github.com/DarkFlippers/unleashed-firmware/releases/tag/unlshd-089), [Momentum repo](https://github.com/Next-Flip/Momentum-Firmware), [Momentum site](https://momentum-fw.dev/releases/mntm-012), [Flipper CLI docs](https://docs.flipper.net/zero/development/cli), [Flipper tech specs](https://docs.flipper.net/zero/development/hardware/tech-specs).

---

## RayHunter

**What it is.** RayHunter is the Electronic Frontier Foundation's open-source **IMSI-catcher / cell-site-simulator ("Stingray") detector** — a Rust daemon that passively watches your cellular baseband for the telltale signatures of a fake base station. It is *not* a Wi-Fi/BLE/sub-GHz tool like the rest of this fleet; it operates one layer down, on the actual LTE/2G control plane of the carrier network you're connected to. Repo: [github.com/EFForg/rayhunter](https://github.com/EFForg/rayhunter). Project handbook: [efforg.github.io/rayhunter](https://efforg.github.io/rayhunter/).

**Latest version.** **v0.11.2, released 2026-05-28** (per the [releases page](https://github.com/EFForg/rayhunter/releases)). Recent feature deltas: v0.11.2 added a **GPS logging framework** and software-update notifications (web UI + ntfy); v0.11.0 added **Wi-Fi client mode** and **WebDAV auto-upload** of recordings; v0.10.0 added a "High Visibility" full-screen red/green display mode and an improved 2G-downgrade heuristic.

### Chip / board it runs on (this is the whole story)
RayHunter does **not** run on a microcontroller. It runs on a **Linux/Android device with a Qualcomm modem that exposes a `/dev/diag` (Qualcomm `DIAG_CHAR`) interface plus root** — that's the hard requirement ([docs](https://efforg.github.io/rayhunter/supported-devices.html)). The daemon reads the raw QMI/DIAG stream the baseband produces and analyzes it. Supported devices ([supported-devices](https://efforg.github.io/rayhunter/supported-devices.html)):
- **Recommended:** Orbic RC400L (a.k.a. Kajeet RC400L, Americas) — the reference/original target; **TP-Link M7350** (EMEA, also works in Americas).
- **Functional:** Wingtech CT2MHS01, T-Mobile TMOHS1, TP-Link M7310, **PinePhone / PinePhone Pro**, FY UZ801, Moxee hotspot.
- Theoretically: *any* Qualcomm-modem device with an exposed `/dev/diag` + root.

> **None of the user's owned boards can run this.** See `user_board_fit` — ESP32 (all variants), RTL8720DN/BW16, and the Pi's have no Qualcomm cellular baseband and no `/dev/diag`. The **Orbic RC400L is currently NOT owned**; it (or a TP-Link M7350) must be acquired to use RayHunter at all.

### Unique specialty vs the rest of the fleet
This is the only firmware in the inventory that touches the **cellular layer**. Marauder/ESP32-DIV/etc. attack Wi-Fi/BLE/2.4GHz; Heltec does LoRa; BW16 does dual-band Wi-Fi/BLE. RayHunter is the **defensive cellular-surveillance detector** — it tells you when a Stingray is impersonating a tower near you. There is zero capability overlap, and no owned board can substitute.

### Feature / detection surface (the analyzers)
RayHunter ships a set of named heuristics ([heuristics page](https://efforg.github.io/rayhunter/heuristics.html)):
- **IMSI Requested** — flags NAS identity requests pulling your IMSI without proper authentication (classic IMSI-catcher behavior).
- **Null Cipher (RRC, EEA0)** — connection running with encryption disabled; should essentially never happen on a real network. *FP-prone on encryption-negotiation failures.*
- **NAS Null Cipher** — null cipher suggested at the NAS layer post-auth. *FP possible if a provider deliberately uses null cipher.*
- **2G Downgrade (Connection Release / Redirected Carrier)** — tower releases/redirects you to 2G, where MITM interception is feasible.
- **LTE SIB6/7 Downgrade** — SIB6/7 broadcasts advertising 2G/3G at high priority to lure devices off LTE. *Historically FP-prone.*
- **Incomplete SIB** — broken SIB chain in SIB1, a fake-base-station tell.
- **Diagnostic Information** — surfaces tower connect/disconnect events for PCAP analysis.
- **Test Analyzer** — fires on every new tower; for verifying your install works, not for real detection.

(Default-on vs opt-in set is not documented per-analyzer — see open questions.)

### How you interact with it — web UI, NOT a serial CLI
RayHunter is driven through a **built-in web UI on port 8080**, served by the on-device daemon ([README/docs](https://github.com/EFForg/rayhunter)):
- **Over Wi-Fi:** join the hotspot's SSID, browse to `http://192.168.1.1:8080` (Orbic) or `http://192.168.0.1:8080` (TP-Link). (No HTTPS — ignore the browser warning.)
- **Over USB:** `adb forward tcp:8080 tcp:8080` then `http://localhost:8080`.
From the UI you **start/stop recordings, view heuristic analysis, and download/delete captures**. On-device, a **status line** across the top of the display indicates state: **green = normal**; it shifts to **yellow dots / orange dashes / solid red** as alert severity rises ([using-rayhunter](https://efforg.github.io/rayhunter/using-rayhunter.html)). v0.10.0's "High Visibility" mode turns the whole screen red/green. (Double-tap-power to start a recording exists but is disabled by default since v0.4.0.)

**Can Cyber Controller drive it over serial?** **No — not as a serial-CLI device the way an ESP32 firmware is.** RayHunter has **no UART AT/CLI command surface** for a host like Cyber Controller to puppet. Control is **HTTP (port 8080)** plus **ADB**. A host *can* script it, but over the network/ADB transport: there is an **ADB shell** on the Orbic, and `/bin/rootshell` gives root for managing files under `/data/rayhunter/qmdl` ([export discussion](https://github.com/EFForg/rayhunter/discussions/239)). So host automation = `adb forward` + HTTP API + `adb shell`/`rootshell`, not a serial terminal. The natural host is the **Raspberry Pi 5** (or any PC), used to run the installer and to pull/convert captures.

### Captures / export
Recordings live at **`/data/rayhunter/qmdl`** on-device. RayHunter records native **QMDL** (Qualcomm modem diag log) and can export **PCAP**, which is a strict superset of the QMDL content ([discussion #239](https://github.com/EFForg/rayhunter/discussions/239)). Both are downloadable from the web UI's History section. For deep offline analysis you convert QMDL→PCAP with SCAT/SignalCat: `scat -t qc -d YOUR.qmdl -F OUT.pcap`, then open in Wireshark.

### "Flashing" — there is NO firmware flash
This is the biggest mental-model difference from the ESP32 world. RayHunter is **not flashed to a chip** — there are **no offsets, no merged bin, no esptool, no AmebaD image**. Instead you run a **platform installer binary** that deploys the daemon onto a running device over its admin interface ([installing-from-release](https://efforg.github.io/rayhunter/installing-from-release.html)):
1. Download `rayhunter-vX.X.X-PLATFORM.zip` for your **host OS** (macOS Intel/ARM, Linux x64/aarch64/armv7 — armv7/aarch64 means the **Pi 5 can be the installer host**, Windows). Each release ships per-platform zips (~20 MB) with SHA256 files.
2. Connect the target over **Wi-Fi or USB tethering**.
3. Run the installer with device args, e.g. `./installer orbic --admin-password <pw>` or `./installer tplink`. (On macOS, clear the quarantine xattr first.)
4. The installer talks to the device's web admin (`192.168.1.1` Orbic / `192.168.0.1` TP-Link), drops the daemon, and **reboots** the device.

### Gotchas
- **Hardware gate is absolute:** no Qualcomm modem + `/dev/diag` + root = it simply cannot run. Don't expect any owned ESP32/RTL/Pi board to host the *detector* role.
- **Install fragility over USB:** docs explicitly warn that bad cables/hubs cause installer failures — use a known-good direct USB connection.
- **False positives:** SIB6/7 downgrade and the null-cipher analyzers are flagged FP-prone; treat a single alert as "investigate," not "confirmed Stingray," and correlate against your carrier's normal behavior.
- **No HTTPS** on the web UI (plain HTTP on 8080) — fine on the device's own LAN, but don't expose it.
- **Not a real-time push to a host:** alerting is on-device (display line + optional ntfy/WebDAV in newer versions); a host controller polls the HTTP API rather than receiving a serial event stream.
- **Region/carrier matters:** Orbic = Americas; TP-Link M7350 = EMEA-first. Pick the device for the band plan you'll actually use.

---

## Pwnagotchi

### What it is + current version
Pwnagotchi is a **Raspberry-Pi-only** Wi-Fi auditing "pet": a full Raspberry Pi OS Linux box that instruments **[bettercap](https://www.bettercap.org/)** to survive off its surrounding Wi-Fi environment and capture the maximum amount of crackable WPA/WPA2 key material. The user runs the actively-maintained **jayofelony fork**, which is the de-facto modern Pwnagotchi (the original evilsocket repo is abandoned).

- **Latest release: `v2.9.5.4`, released 29 Jan 2025**, built on the latest **Trixie** Raspberry Pi OS. ([releases](https://github.com/jayofelony/pwnagotchi/releases/tag/v2.9.5.4))
- It is delivered as flashable **`.img.xz` SD-card images** (one per Pi class), NOT as an ESP32-style firmware bin. ([repo](https://github.com/jayofelony/pwnagotchi))

> **CRITICAL CORRECTION to the task framing — the "AI" is real and present.** The current jayofelony `master` README describes Pwnagotchi as *"an A2C-based 'AI' leveraging bettercap that learns from its surrounding Wi-Fi environment"* and *"using an LSTM with MLP feature extractor as its policy network for the A2C agent,"* and the shipped `defaults.toml` sets `ai.enabled = true`. ([README raw](https://raw.githubusercontent.com/jayofelony/pwnagotchi/master/README.md), [defaults.toml](https://raw.githubusercontent.com/jayofelony/pwnagotchi/master/pwnagotchi/defaults.toml)) There is a widely-repeated community claim (and a `noai` branch) that jayofelony "removed the AI for Wi-Fi-firmware stability and battery life." That may be true for a specific branch/older image, but it is **NOT** what the current shipping `master`/v2.9.5.4 says. Confirm on your flashed image (see open questions) — do not assume the AI is gone.

### Chip / board it runs best (or only) on
This is a **Linux SoC firmware, not an MCU firmware.** Officially supported boards ([README](https://github.com/jayofelony/pwnagotchi)):
- **RPi Zero W** (32-bit image) — classic form factor.
- **RPi Zero 2 W, RPi 3, RPi 4, RPi 5** (64-bit images).

Best-on hardware is the **Pi Zero 2 W** (small, low-power, internal radio supports monitor mode via nexmon → no dongle needed). The fork also publishes an "other boards" path (Orange Pi 3B + external Comfast adapter, headless/no-display) for non-Pi Linux SBCs. ([other-boards wiki](https://github.com/jayofelony/pwnagotchi/wiki/Step-1-Installation-for-other-boards))

### UNIQUE specialty vs the rest of your fleet
Among everything you own, Pwnagotchi is the **only on-device *learning* Wi-Fi attacker** and the only one that is a full Linux box. Versus your ESP32/RTL fleet:
- It runs **bettercap + an A2C reinforcement-learning agent** that tunes its own deauth/associate/channel-hop parameters over epochs — your ESP32 Marauder/DIV firmwares run fixed scripts; none learn.
- It produces **hashcat-ready PCAPs** containing **full + half WPA handshakes AND PMKIDs**, captured passively or via active **authentication/association attacks**. ([README](https://github.com/jayofelony/pwnagotchi))
- It has a **mesh/peering "parasite protocol"**: multiple Pwnagotchis broadcast custom 802.11 information elements to detect and "greet" each other (the social/face-on-screen gimmick). No ESP32 firmware you own peers like this.
- It is **display-first**: an e-ink face shows mood/uptime/handshake count, designed for a wearable battery build.

### Full feature / command surface
- **Attack engine:** bettercap-driven channel hopping, deauthentication attacks, association/PMKID attacks, passive sniffing. Handshakes land in `/root/handshakes/` (or `/home/pi/handshakes`). ([defaults.toml](https://raw.githubusercontent.com/jayofelony/pwnagotchi/master/pwnagotchi/defaults.toml))
- **Web UI:** served on **port 8080** (`ui.web.address = "::"`, default creds `changeme/changeme`) — shows the face, plugin tiles, and a `webcfg` plugin for editing config from the browser. ([plugins](https://pwnagotchi.ai/plugins/))
- **bettercap API** runs on **port 8081** (creds `pwnagotchi/pwnagotchi`). ([plugins](https://pwnagotchi.ai/plugins/))
- **Modes:** AUTO (the AI personality drives everything) and MANUAL (you walk it / it just listens). Personality knobs in `personality.*` (advertise, deauth, associate, channel list, epoch timings).
- **Rich plugin ecosystem** (jayofelony bundles many as default in v2.9.5.4): `auto-backup` (now default), `cache`, `pisugar` (battery HAT), `bt-tether` (Bluetooth tether to phone for uploads / phone-as-display), `gps`/`gpsd`, `wpa-sec` (auto-submit caps for cracking), `wigle` (wardriving uploads), `webgpsmap`, `wardriver`, `ohcapi`. ([release notes](https://github.com/jayofelony/pwnagotchi/releases/tag/v2.9.5.4), [plugins](https://pwnagotchi.ai/plugins/))
- **Screen rotation** 90/270° added in v2.9.5.4.

### External modules it needs
- **Display HAT** — your **Waveshare 2.13in V4 e-ink** is the canonical Pwnagotchi screen (this is exactly what it's for). Driver in-tree: `waveshare2in13_V4.py`; the config literal exposed in `defaults.toml` is `ui.display.type = "waveshare_4"` (B/touch variants use `waveshare2in13b_V4.py`). ([hw drivers](https://github.com/jayofelony/pwnagotchi/tree/master/pwnagotchi/ui/hw)) ⚠️ The **2.13 V4 is the historically problematic panel** on this fork — multiple open issues report it "not drawing properly." ([bookworm issue #36](https://github.com/jayofelony/pwnagotchi-bookworm/issues/36))
- **Battery HAT** (PiSugar) for wearable use — first-class `pisugar` plugin support.
- **Monitor-mode USB Wi-Fi adapter** — required on **Pi 5 and Pi 3/4** and all "other boards" (internal radio lacks a working monitor patch); NOT required on Zero W / Zero 2 W (nexmon). The user does **not** list a known-good monitor-mode dongle as owned.
- Your NRF24L01 / CC1101 / 315MHz / OLED modules are **irrelevant** here — Pwnagotchi is pure Wi-Fi (+ optional GPS via gpsd) and does not use sub-GHz or 2.4GHz-radio side modules.

### Host controller (Cyber Controller) — can it drive this over serial?
**No.** Pwnagotchi has **no serial CLI for a host to drive** the way an ESP32 firmware exposes a USB-serial command shell. It is **network-only**:
- It presents as a **USB ethernet gadget** (RNDIS/ECM) at **`10.0.0.2`** and you reach it by **SSH** (`ssh pi@10.0.0.2` or `pi@pwnagotchi.local`, default creds **`pi/raspberry`**), plus the **web UI on :8080** and **bettercap API on :8081**. Pi 4/5 can also use real Ethernet. ([connecting wiki](https://github.com/jayofelony/pwnagotchi/wiki/Step-2-Connecting))
- "Control" = a full Linux SSH session + REST/web, not an AT-style serial protocol. **Cyber Controller / headless-marauder-gui cannot enumerate or command it over a COM port.** If you ever want host integration, it's SSH/HTTP automation against a Linux box — a fundamentally different transport than the rest of your serial-driven fleet. Treat it as touch/button + headless-network, **not** host-serial-driven.

### Flashing specifics
- **SD-card image flash, not an MCU flash.** Download the matching **`.img.xz`** for your Pi class and write it with Raspberry Pi Imager / balenaEtcher. There is **no merged bin, no app+offset, no AmebaD/zip-bundle** step — those concepts don't apply (this is the Pi side of your bench, not ESP32/RTL8720). ([releases](https://github.com/jayofelony/pwnagotchi/releases/tag/v2.9.5.4))
- Pick the right image: **32-bit** for Zero W; **64-bit** for Zero 2 W / 3 / 4 / 5.
- After first boot, edit `/etc/pwnagotchi/config.toml` (over SSH or the `webcfg` plugin) to set `main.name`, `ui.display.type`, plugin keys (wpa-sec/wigle API keys), and Wi-Fi/BT tether.

### Gotchas
1. **Your only runnable board is the Pi 5** (Zero 2 W is fried) — and the Pi 5 is a poor Pwnagotchi host: power-hungry, bulky for a wearable, and needs an **external monitor-mode dongle you don't own**. Sourcing a replacement **Pi Zero 2 W** is the real fix.
2. **Display mismatch:** your **2.13 V4 e-ink HAT** is a Pi-header HAT (Zero form factor) and is the known-flaky V4 panel; pairing it to a Pi 5 is mechanically awkward and the V4 driver itself has open drawing bugs. Plan to verify `display.type` empirically.
3. **AI status is genuinely ambiguous in the wild** — current `master` says A2C AI is in; community lore says it was removed. Don't write docs that state it's removed without checking your own image's `defaults.toml`.
4. **Legal/RF:** active deauth/association attacks are real WPA attacks — same lab-only/own-network discipline as your Marauder work.
5. **Not cross-flashable** with anything else you own: do not expect to put Pwnagotchi on an ESP32-C5/S3/CYD or the BW16/RTL8720DN — it is Linux-only.

Sources: [jayofelony/pwnagotchi repo](https://github.com/jayofelony/pwnagotchi) · [v2.9.5.4 release](https://github.com/jayofelony/pwnagotchi/releases/tag/v2.9.5.4) · [README (raw)](https://raw.githubusercontent.com/jayofelony/pwnagotchi/master/README.md) · [defaults.toml](https://raw.githubusercontent.com/jayofelony/pwnagotchi/master/pwnagotchi/defaults.toml) · [hw display drivers](https://github.com/jayofelony/pwnagotchi/tree/master/pwnagotchi/ui/hw) · [Connecting wiki](https://github.com/jayofelony/pwnagotchi/wiki/Step-2-Connecting) · [Other-boards wiki](https://github.com/jayofelony/pwnagotchi/wiki/Step-1-Installation-for-other-boards) · [plugins](https://pwnagotchi.ai/plugins/)

---

## RaspyJack

### What it is + version
**RaspyJack** (repo: [`7h30th3r0n3/Raspyjack`](https://github.com/7h30th3r0n3/Raspyjack)) is a **small offensive network toolkit for the Raspberry Pi**, built around a Waveshare 1.44″/1.3″ LCD HAT + joystick, "inspired by pager and sharkjack functionalities… for redteam and educational purposes only." It is **not microcontroller firmware** — it is a Python application stack that runs on top of Raspberry Pi OS Lite (a full Linux SBC), installed via `git clone` + `install_raspyjack.sh`. Think "handheld Hak5 Shark-Jack/Bash-Bunny clone you build yourself on a Pi."

- **Latest version: v1.0.6, released 6 April 2026** ("135 new payloads, dual-display support (128×128 + 240×240), Game Boy emulator, CCTV viewer, performance optimizations"). Release history: v1.0.0 (22 Jun) → v1.0.1 payloads → v1.0.2 Wi-Fi → v1.0.3 MITM & games → v1.0.4 WebUI toolkit → v1.0.5 Web IDE & authentication → **v1.0.6** (latest). Source: [Releases](https://github.com/7h30th3r0n3/Raspyjack/releases). (Year caveat noted in open questions.)
- ~555 commits, **Python ~53% / HTML ~36%** — the large HTML share is the **WebUI** (see below). Source: [repo root](https://github.com/7h30th3r0n3/Raspyjack).

### The chip/board it runs best (or only) on
RaspyJack runs **only on a Raspberry Pi (Linux SBC)** — there is **no ESP32/RTL8720 build**. Per README + [DeepWiki Hardware Setup](https://deepwiki.com/7h30th3r0n3/Raspyjack/2.2-hardware-setup):
- **Primary / best target: Raspberry Pi Zero 2 W (Zero 2 WH)** — quad-core 1 GHz, 512 MB. ~22 s boot. This is the canonical handheld build.
- **Also supported: Pi 3B, Pi 4B, Pi 5** — but README warns "Raspberry Pi 4/5 is not fully tested yet."
- **Display:** Waveshare **1.44″ HAT = 128×128, ST7735(S)** or **1.3″ HAT = 240×240, ST7789** (SPI; LCD_DC=GPIO25, RST=GPIO27, CS=GPIO8, BL=GPIO24, MOSI=GPIO10, SCLK=GPIO11). v1.0.6 auto-scales the UI from the 128×128 baseline via a `ScaledDraw`/`gui_conf.json` layer. Installer prompts `ST7735_128` vs `ST7789_240`; switchable later via **Payload → Utilities → display_selector**.
- A third target, **M5Stack CardputerZero (320×170 framebuffer, TCA8418 I²C keyboard)**, exists in the installer (`CARDPUTER_320` mode) — *not an owned device*.

### UNIQUE specialty vs the rest of the fleet
RaspyJack is the fleet's **only full-Linux wired+wireless red-team drop-box**. Everything the ESP32/RTL boards do is constrained to RF/Wi-Fi/BLE microcontroller tricks; RaspyJack instead gives you **real Linux network attacks over Ethernet and USB-NIC Wi-Fi**:
- **LAN credential capture** the ESP32 fleet physically can't do: **Responder (LLMNR/NBT-NS/MDNS poisoning)**, **ARP MITM** (ettercap/dsniff), **DNS spoofing**, packet sniffing (tcpdump/tshark).
- **Real recon:** `nmap`, `arp-scan`, **Shodan/OSINT** lookups.
- **Arbitrary Python payloads** (231–233 payloads across 13 categories) + an **in-browser Web IDE** to write/edit them live — a genuinely extensible platform, not a fixed menu.
- Drop it on a wired corporate LAN via the Waveshare Ethernet/USB-HUB HAT and it behaves like a Shark Jack with a screen.

### Full feature / command surface (231+ payloads, 13 categories)
- **Recon/scan:** Nmap scan, network info, Shodan, OSINT.
- **Credential capture / MITM:** Responder, ARP MITM, DNS spoofing, sniff.
- **Wi-Fi attacks (USB adapter required):** deauth (2.4 + 5 GHz), evil twin, SSID injection, beacon flood, **handshake hunter with auto-upload**, **Evil Portal with 84 captive-portal templates** + credential capture, wardriving.
- **BLE:** scanner / spam / MITM.
- **Shells & C2:** reverse shell, **Discord C2**, **HTTPS stealth shell**.
- **Exfiltration channels:** HTTP, DNS, BLE, Discord, SMB, FTP, USB, Dropbox.
- **Reference/extras:** read files, Discord webhook, file structure, **25 games** (Pac-Man, Tetris, Tron), Game Boy emulator, CCTV viewer (v1.0.6).
- **On-device controls:** UP/DOWN navigate, LEFT back, RIGHT/OK select, KEY1 context, KEY2 secondary, KEY3 exit; List/Grid/Carousel view modes. (Sources: [README](https://github.com/7h30th3r0n3/Raspyjack/blob/main/README.md), [Wiki](https://github.com/7h30th3r0n3/Raspyjack/wiki).)

### External modules it needs
- **USB Wi-Fi adapter is mandatory for any Wi-Fi attack** — "the onboard Pi Wi-Fi (Broadcom 43430) cannot be used for Wi-Fi attacks." Explicitly supported: **Alfa AWUS036ACH (RTL8812AU)**, **TP-Link TL-WN722N v1 (Atheros AR9271)**, **Panda PAU09 (RTL8812AU)** — all monitor-mode + injection capable.
- **Ethernet:** Waveshare Ethernet/USB-HUB HAT (3×USB + 1×Ethernet) for headless wired drops.
- The installer also pulls `rtl-sdr` / `rtl-433` / `gpsd` (SDR + GPS for wardriving) and, for CardputerZero, `mpv`/`bluez-alsa-utils`/`chocolate-doom`.
- **No NRF24** and no 315/433 MHz sub-GHz attack module is part of RaspyJack's documented surface (rtl-sdr is receive-only). The owned NRF24 adapters / 315 MHz antennas are **not** RaspyJack accessories — they belong to the ESP32 side of the fleet.

### Host control: WebUI, NOT a serial CLI
**A host controller like Cyber Controller cannot "drive" RaspyJack over a serial/UART CLI — there is no serial control surface.** Control is two-way only:
1. **On-device** joystick + buttons on the LCD.
2. **WebUI (browser, network)** — a real remote control surface, not just monitoring: dashboard at `https://<device-ip>/` (HTTP fallback `:8080`), a **Web IDE** at `/ide`, and a Ragnar launcher (`:8091`) exposing status, automation/manual toggles, network-scan and vuln-scan triggers, and log view. v1.0.5 added **authentication**.

So RaspyJack integrates with a host over **HTTP(S)/WebSocket on the LAN**, the same way you'd reach a web app — fundamentally different from the ESP32 fleet's USB-serial CLIs. If Cyber Controller is to manage it, it would do so by talking to the WebUI/REST endpoints over the network, not over a COM port.

### Flashing specifics
There is **no merged-bin / app+offset / AmebaD flashing** — this is an SBC, so you provision an SD card and install software:
1. Flash **Raspberry Pi OS Lite 32-bit** with Raspberry Pi Imager (enable SSH, set user/pass).
2. As root: `apt install git` → `git clone https://github.com/7h30th3r0n3/raspyjack.git` → `mv raspyjack Raspyjack` → `cd Raspyjack` → `chmod +x install_raspyjack.sh` → `sudo ./install_raspyjack.sh` → `reboot`.
3. Installer enables **SPI + I²C** (`dtparam=spi=on`, `dtparam=i2c_arm=on`, loads `spi_bcm2835`/`i2c-dev`), prompts for the LCD type, installs the toolchain (`nmap ncat tcpdump tshark arp-scan dsniff ettercap-text-only aircrack-ng hostapd dnsmasq-base reaver john autossh rtl-sdr ffmpeg yt-dlp gpsd` + Python libs `scapy/netifaces/pyudev/serial/smbus/rpi.gpio/spidev/pil/qrcode/numpy`), and registers **three systemd services**: `raspyjack.service` (LCD UI), `raspyjack-device.service` (WebSocket device server), `raspyjack-webui.service` (HTTP), plus optional **Caddy** TLS (`raspyjack-caddy-autoconfig.service`). It also pins onboard Wi-Fi → `wlan0` and USB dongle → `wlan1` via udev/systemd `.link` rules. (Source: [install_raspyjack.sh](https://github.com/7h30th3r0n3/Raspyjack/blob/main/install_raspyjack.sh), [Installation wiki](https://github.com/7h30th3r0n3/Raspyjack/wiki/Installation).)

### Gotchas (act on these)
- **Wrong fleet class:** Do not try to flash this to any ESP32/ESP32-S2/S3/C5, CYD, Heltec, or BW16 board — it is Linux/Pi-only. The owned **Pi 5 (8GB)** can run it but the owned **Pi Zero 2 W is fried**, so the *intended* handheld target is currently dead.
- **Onboard Pi Wi-Fi is useless for attacks** — you must add a supported USB dongle (RTL8812AU/AR9271). The owned NRF24/315 MHz/IPEX gear does **not** satisfy this; **no supported Wi-Fi dongle is in the owned-modules list** → Wi-Fi payloads are blocked until one is acquired.
- **wlan0/wlan1 pinning** assumes onboard = `wlan0`, USB = `wlan1`; on a Pi 5 with multiple/odd adapters double-check the udev rules so payloads target the right interface.
- **Pi 4/5 "not fully tested"** — expect rough edges and missing LCD/joystick on a Pi 5 (you'd run WebUI-only there).
- **Network-only host control:** plan any Cyber Controller integration around the WebUI/WebSocket (auth required since v1.0.5), not a serial port.
- **OpSec:** full Linux pentest stack (Responder, ettercap, reaver) — authorized-testing only.

Sources: [repo](https://github.com/7h30th3r0n3/Raspyjack) · [README](https://github.com/7h30th3r0n3/Raspyjack/blob/main/README.md) · [Wiki](https://github.com/7h30th3r0n3/Raspyjack/wiki) · [Installation](https://github.com/7h30th3r0n3/Raspyjack/wiki/Installation) · [Releases](https://github.com/7h30th3r0n3/Raspyjack/releases) · [DeepWiki Hardware Setup](https://deepwiki.com/7h30th3r0n3/Raspyjack/2.2-hardware-setup) · [install_raspyjack.sh](https://github.com/7h30th3r0n3/Raspyjack/blob/main/install_raspyjack.sh)

---

## Open questions (verify on hardware)

### ESP32 Marauder (justcallmekoko/ESP32Marauder)
1) AITRIP 4" ST7796 — confirm on hardware whether the release's 3.5"/ST7796 bin drives the 4" panel correctly (resolution/rotation/touch offsets may differ); may need a from-source build. 2) LILYGO T-Display-S3 and Heltec LoRa V3 are NOT official koko targets — there are community/TTGO forks, but verify a current, S3-correct build exists (and that the S3 0x0 bootloader offset is used); the Heltec's SX1262 LoRa radio is unused by Marauder. 3) Exact C5 feature parity: the C5 wiki page does not enumerate which attacks are 5GHz-capable vs 2.4-only — verify on the Waveshare C5 whether deauth/evilportal actually function on 5GHz channels, not just scanning. 4) Whether v1.12.1 BLE spam set still includes Samsung/Swift Pair on S3 vs only classic ESP32 — confirm per-chip. 5) NRF24 is listed for koko's dual-NRF hardware, not stock Marauder — confirm none of your target features silently expect it.

### Bruce (BruceDevices/firmware, formerly pr3y/Bruce)
1) Classic WROOM-32 (your 3x Gold + 1x dev board): is there ANY current maintained binary, or strictly a DIY platformio port? Web flasher dropdown showed no plain-ESP32 entry — verify on hardware before assuming it flashes. 2) ESP32-S2U x3: no S2 board folder found; confirm whether a community S2 env builds (S2 has USB-OTG so BadUSB could work) or if S2 is entirely unsupported. 3) AITRIP 4" ST7796: confirm exact board match (CYD-3248S035 vs ES3C28P vs a 4" variant) in the live flasher — wrong panel build = blank/garbled screen. 4) ESP32-C5 flash offset: merged bin is 0x0, but the user's broader notes flag C5 bootloader at 0x2000 for SPLIT flashing — confirm the Bruce C5 merged bin self-handles this (it should, since it's a full image at 0x0) before any manual split-flash. 5) Whether 1.15 added any WiFi/BLE attack to the serial CLI (currently UI-only) — re-check the Serial wiki against the running build. 6) Does the headless/WebUI mode run on a classic-ESP32 CYD, or is headless truly S3-only as the reference env implies?

### GhostESP (GhostESP-Revival fork)
1) Owned LILYGO T-Display-S3 is the NON-touch variant; the published build is `LilyGo-TDisplayS3-Touch.zip` — confirm a non-touch T-Display-S3 build exists or that the touch build degrades gracefully (UI may expect XPT2046/CST816 touch). 2) Heltec LoRa V3: GhostESP boots and uses it as a status-display ESP32-S3, but I found NO documentation that GhostESP drives the on-board SX1262 (no LoRa sniff/Meshtastic-detect feature in the matrix) — verify on hardware whether LoRa is dead weight here. 3) AITRIP 4" ST7796: no exact GhostESP build named for ST7796 4-inch; `JC3248W535EN_LCD.zip` is a 3.5" capacitive board, not a guaranteed match — confirm panel/touch driver before flashing. 4) ESP32-C5 5 GHz: changelog v1.9.10 fixed UNII channel discovery, but verify on the Waveshare C5 specifically that 5 GHz scan/attack actually enumerates UNII-2/UNII-3, and that the right C5 zip (generic vs ACE/Banshee vendor build) maps to a bare Waveshare dev board — pin map may differ. 5) merged-gesp.bin presence per-zip: confirmed for some bundles via 3rd-party flasher docs, but verify each owned-board zip actually ships merged-gesp.bin vs only the 3 offset bins. 6) Whether the serial CLI exposes 100% of touch-UI features or a subset (host-drive parity).

### HaleHound-CYD
1) AITRIP 4" ST7796 fit: HaleHound's `esp32-e32r35t` build targets an ST7796 320x480 + XPT2046, which is the SAME controller as the AITRIP 4" panel — but QDtech's E32R35T pinout, backlight, and touch calibration may not match the AITRIP board. The 4" AITRIP could need a different display/touch pin map or panel-init; flashing the E32R35T-FULL.bin is worth trying but is unverified on AITRIP hardware (risk: white/black screen, mirrored/rotated touch). Verify panel orientation and touch-cal on first boot. 2) Whether the AITRIP 4" is classic-ESP32 (required) vs an S3 board — confirm the chip before flashing; an S3-based 4" panel would NOT run this firmware at all. 3) Exact CC1101 GDO2/RX behavior and whether stock HW-863 (no PA) is adequate for the user's 315MHz Tesla/SubGHz use without the E07 PA. 4) Confirm v3.5.5 is still latest at flash time (release cadence is fast — multiple point releases in March 2026).

### ESP32-DIV (cifertech/ESP32-DIV)
1) The Firmware-Upload wiki literally says "Chip: ESP32" with .bin@0x10000 / .partitions@0x8000 in the Flash Download Tool — this appears STALE from the v1.1.0 classic-ESP32 era and conflicts with the v1.5.0+ ESP32-S3 hardware. For S3, expect a full set (bootloader@0x0, partitions@0x8000, app@0x10000) or `esptool --chip esp32s3 write_flash 0x0 <merged>.bin`, plus USB-CDC-on-boot. Verify the exact offsets/merged-bin layout per-release on real hardware before flashing — do not trust the wiki's single-chip note. 2) Exact ESP32-S3 flash size required (likely 8/16 MB given SD-less builds and OTA) is not documented — confirm against the release .bin size (~1.54 MB app) and partition table. 3) Whether v1.6.0 ships a single merged bin vs app+partitions vs a zip bundle is not explicitly stated; the release page lists `ESP32-DIV-v1.6.0.bin` (~1.54 MB) but the full asset set/offsets need confirmation. 4) Confirm on hardware that the on-device "Serial Monitor" truly has no inbound command parser (all evidence says debug/terminal output only, not a host CLI). 5) GPIO14 IR/NRF24 share is documented as needing a restart between IR and NRF24 use — verify this is still true in v1.6.0. 6) PN532 is listed as SPI in the Features wiki; confirm bus/CS wiring before sourcing a module.

### Meshtastic (meshtastic/firmware)
1) Exact "latest" tag drifts weekly — confirmed v2.7.25.104df5f (Alpha, 2026-06-10) at research time, but Meshtastic ships Alpha pre-releases every 1-4 weeks; check the releases page before flashing and prefer the newest tag the Web Flasher offers. 2) No official Meshtastic variant exists for ESP32-C5 or for a bare classic-ESP32 + external radio in your parts bin — both would require writing/maintaining a custom variant; unverified that anyone has a working C5 port. 3) The exact littlefs/SPIFFS offset for a hand-built classic-ESP32 variant depends on the partition table you choose — verify against your variant's `partition-table.csv` before manual esptool flashing. 4) Whether your IPEX->SMA pigtails + 315MHz antennas are usable: NO for the antennas (Meshtastic LoRa here is 915MHz US band; a 315MHz antenna is badly mismatched) — you need a 915MHz antenna; the Heltec V3 ships with one. 5) Not validated on hardware whether the SX1262 on a generic ESP32 needs the same DIO/BUSY pin mapping as Heltec — variant-specific.

### BW16 Vampire Deauther (vampel) — AT+ CLI fork of tesa-klebeband's RTL8720dn-Deauther
1) VERSION INCONSISTENCY: the web flasher page title still reads "v1.31" while its own subtitle/header reads "v2.4.6" — the true firmware (Vamp_FW.bin) version is not authoritatively stamped; confirm on-device via serial banner. 2) LINEAGE NOT CREDITED: vampel's README is a 175-byte stub ("Vampel Proyects / Custom Board") with NO credit to tesa-klebeband, Realtek, or Ameba — the AT+ lineage is inferred from feature/structure overlap, not stated; treat the "fork of tesa-klebeband" claim as strong-but-unconfirmed. 3) PCAP / AUTO-DOWNLOAD: the page advertises "Now save PCAP, AUTO-DOWNLOAD MODE" but AUTO-DOWNLOAD clearly refers to the FLASHER auto-pulling firmware from GitHub; whether the FIRMWARE itself sniffs and exports PCAP (vs. the flasher just saving logs) is unverified — test on hardware. 4) BLE: the RTL8720DN chip supports BLE, but NOTHING in the Vampire Deauther command set or docs exposes BLE — the task's "+BLE" is a chip capability, not a firmware feature. Do not assume BLE attacks. 5) AT+STOP reliability: docs note memory fills during deauth and a physical RESET button press is often required to recover — confirm whether AT+STOP alone cleanly halts via serial without the reset. 6) Whether 5GHz deauth works on ALL 5GHz channels or only a subset (DFS/region limits) is undocumented. 7) Exact set of bootloader offsets when flashing a CUSTOM bin vs. the bundled Vamp_FW.bin — confirm against AmebaD imgtool before flashing anything non-default.

### Flock-You (colonelpanichacks/flock-you)
1) Exact required flash size: XIAO ESP32-S3 ships 8MB but partitions.csv reserves 6MB app + 1.9MB SPIFFS — verify a T-Display-S3 (often 16MB, sometimes 8MB) or Heltec V3 (8MB) partition table matches before flashing. 2) Whether the unmerged WiFi-sniff radio + NimBLE BLE scan can coexist on one chip (the repo splits them into TWO branches/firmwares — confirm there is no single combined build). 3) No version tags or releases exist at all (1.1k stars, "No releases published"); the only versioning is branch names (promiscious-dev vs promiscious vs main) — "latest" is a moving HEAD, so pin a commit. 4) Does the T-Display-S3's USB-CDC enumerate identically for the Flask serial-ingest path, or does it need USB-CDC-On-Boot toggled? 5) Third-party guides (simeononsecurity) claim classic ESP32-WROOM works — this conflicts with the upstream S3-only targeting and is likely conflated with other tools; treat as unverified.

### OUI-Spy (OUI-SPY Unified Blue + standalone modes)
1) No tagged GitHub releases exist (oui-spy-unified-blue has 0 releases as of research date) — there is no semantic version number anywhere; "Unified Blue" is the build name, not a version. Confirm current commit hash on hardware rather than citing a version. 2) Whether the official unified bin runs the T-Display-S3 ST7789 TFT at all (almost certainly NOT — no display driver referenced); verify on the bench. 3) Exact buzzer/NeoPixel behavior when the XIAO-S3 bin runs on T-Display-S3 pins (GPIO 3 / 21) — likely silent/dead; needs hardware test. 4) ESP32-C5 support is mentioned in the ecosystem table but I could not confirm a ready-to-flash C5 binary or which modes are ported — verify before relying on the user's C5 boards for 5 GHz. 5) Serial is EMIT-ONLY JSON (Sky-Spy/Flock-You); I found no evidence of an inbound serial CLI — confirm there is no command parser before assuming Cyber Controller can do anything beyond reading the stream. 6) Baud rate / USB-CDC settings for the Sky-Spy JSON stream are undocumented — sniff on hardware. 7) Luke Switzer's "OUIspy Omni" fork (lukeswitz) adds BLE-GATT app control and a 39k OUI DB but is a separate firmware — not validated here.

### Sky-Spy (colonelpanichacks/Sky-Spy)
1) The README lists Seeed XIAO ESP32-C6 as an "alternative," but the ROOT platformio.ini defines ONLY [env:seeed_xiao_esp32s3] — verify on hardware whether a C6 build actually exists/compiles or whether the C6 claim is stale docs. 2) No GitHub Releases are published and there is NO prebuilt merged bin or web flasher — you MUST build from source with PlatformIO (pioarduino platform). Confirm the pioarduino platform pulls an Arduino-ESP32 core new enough for native ESP32-C5 support at build time. 3) The C5 '5GHz' capability is asserted from hardware + the xiao-c5-5g project name; the platformio.ini has NO explicit channel-149/5GHz build flag, so 5GHz Remote ID scanning is presumed inherent to C5 + the variant's src — VERIFY on a real C5 that it actually hops/listens on 5GHz ch149, not just 2.4GHz ch6. 4) mesh-mapper.py sends a single 'WATCHDOG_RESET\n' on connect but exposes no real interactive command set — confirm there is no hidden serial command parser in main.cpp before treating it as 100% output-only. 5) Waveshare ESP32-C5 is NOT the Seeed XIAO C5 the env name targets; pin map / USB-CDC / PSRAM (-DBOARD_HAS_PSRAM) and the buzzer GPIO3 may differ on the Waveshare board — verify pinout/PSRAM presence before relying on the buzzer or assuming a clean flash. 6) Whether ESP32-C5 needs a non-standard flash offset / bootloader handling under esptool vs the S3 — untested here.

### AirTag Scanner (MatthewKuKanich/ESP32-AirTag-Scanner)
1) No versioning exists — repo has NO releases/tags and ~5 commits; "latest version" = whatever main HEAD is, so pin a commit SHA when you flash. 2) Unconfirmed whether the prebuilt ESP32-S3/ bootloader is built for offset 0x0 (S3 default) vs 0x1000 — if hand-flashing with esptool instead of the Flipper ESP Flasher, verify the S3 bootloader offset on hardware or it will brick-boot-loop. 3) The second filter pattern "4C 00 12 19" (0x12 = FindMy, length 0x19) targets FindMy/offline-finding frames specifically vs the generic "1E FF 4C 00" Apple-continuity prefix — needs a bench check to confirm it reliably catches AirTags in "nearby/registered" state vs only "lost/offline" broadcasts. 4) Samsung SmartTag / Tile detection is asked about in issue #3 but UNANSWERED by the maintainer and there is NO non-Apple manufacturer-ID filter in the source — treat as Apple-only until tested. 5) S2 (your ESP32-S2U) has NO Bluetooth radio at all on most ESP32-S2 silicon — VERIFY before flashing; if your S2U parts are true S2 (not S2+BLE), this firmware cannot scan and the board is unusable for it. 6) C5 and BW16 require from-source porting; not validated.

### Minigotchi-ESP32 (dj1ch/minigotchi-ESP32)
1) "Wardriving"/GPS: third-party listings (osrtos, market.dev) and the project's own feature blurbs mention wardriving, but the INSTALL.md/config show no GPS module support or coordinate logging — likely it means passive AP/MAC observation, not Marauder-style geo-tagged wardriving. Confirm on-device whether any CSV/coords are produced. 2) S2 behavior: dual-core requirement is met by ESP32-S2, but S2 has no Bluetooth — verify the BLE-spam/parasite-BLE paths compile-guard cleanly and the WiFi/parasite features still build for the S2U boards. 3) AITRIP 4" ST7796 and Heltec V3 OLED: no defines exist; confirm whether a generic TFT_eSPI build can drive the ST7796 or if it's headless-only. 4) Exact release assets for v3.6.4-beta could not be read (GitHub asset list failed to load) — confirm whether prebuilt .bin/merged firmware is attached or if source-build via Arduino IDE is the only path. 5) Parasite serial is described as a one-way feed to the Pwnagotchi plugin; confirm there is genuinely NO inbound command parser before relying on "host cannot drive it."

### Flipper (Momentum / Unleashed)
1) The very latest STABLE tags I could confirm are Unleashed unlshd-089 (API 87.8, May 2026) and Momentum mntm-012 (Dec 31 2025). One search snippet referenced an Unleashed build timestamped 2026-06-11 — that is almost certainly a nightly/dev auto-build, not a new tagged stable; verify on the releases page before quoting a newer number. 2) The exact OFW (official firmware) base version that mntm-012 / unlshd-089 sync to (OFW ~1.3.x range) was not cleanly extractable — confirm from the release notes on-device. 3) Whether Cyber Controller's serial layer needs any change to speak Flipper's CLI (230400 baud, USB CDC, `?`/`help`, RPC/protobuf mode) vs ESP32 firmwares — untested since no Flipper is owned. 4) Asset-pack/animation variant letters drift between releases (older n/r, current c/e); re-confirm the c vs e suffix meaning at flash time.

### RayHunter (EFForg/rayhunter)
1) Exact GPS-logging hardware/path in v0.11.2 — docs say a "GPS logging framework" was added but it is unclear whether the Orbic supplies GPS itself or whether an external/phone GPS feed is required; verify on hardware. 2) Whether the QMDL→PCAP conversion now happens fully on-device via the web UI export on current firmware, or still benefits from host-side SCAT/SignalCat (scat -t qc -d X.qmdl -F out.pcap) for deep analysis. 3) Default-enabled analyzer set: the heuristics page names eight analyzers but does not state which are on by default vs opt-in — confirm in the on-device config (config.toml). 4) Whether /bin/rootshell over ADB exists identically on the non-Orbic supported devices (TP-Link/Moxee) or is Orbic-specific. 5) Confirm the precise current default web-UI port is still 8080 (an open issue requested an alternate) and the Orbic admin IP (192.168.1.1) on the latest firmware. 6) Live false-positive behavior of the SIB6/7 and NAS-null-cipher analyzers on US carriers — flagged as FP-prone in docs; verify against the user's actual carrier before trusting alerts.

### Pwnagotchi (jayofelony fork)
1) The current jayofelony master README (Jan 2026, v2.9.5.4) describes Pwnagotchi as an "A2C-based AI" with an LSTM/MLP policy network and ships defaults.toml with ai.enabled=true — so AI is PRESENT in the current release, contradicting older/community claims (and a `noai` branch) that "jayofelony removed the AI." Verify on the actual flashed image whether ai.enabled defaults true and whether the A2C agent actually loads, vs. being a vestigial config key. 2) Waveshare 2.13 V4 (B/non-touch) is historically flaky on this fork — confirm the exact working display.type string on YOUR image: the driver file is waveshare2in13_V4.py but defaults.toml exposes the literal "waveshare_4"; the touch/B variants (waveshare2in13b_V4.py) differ. The user owns the 2.13 V4 e-ink specifically, which is the known-problematic one (multiple open issues: not drawing properly). 3) Pi 5 onboard-WiFi monitor-mode support — confirm an external dongle (e.g., a known-good monitor-mode USB adapter) is required; the user does not list one as owned. 4) Whether the 32-bit Zero W image vs 64-bit Zero 2 W image distinction matters once a replacement Zero 2 W is sourced.

### RaspyJack
1) Release-DATE provenance: GitHub release list shows v1.0.6 dated "06 Apr" and repo metadata reads April 2026; one WebFetch mis-expanded this to "April 2024." Treating v1.0.6 = 6 April 2026 as latest, but confirm the year on the actual /releases page on hardware. 2) Exact payload count drifts across sources (README "231," wiki "233," "135 NEW payloads" in v1.0.6 marketing) — verify the live count in the on-device menu. 3) Cardputer Zero (M5Stack, ESP32-S3 + 320x170 framebuffer + TCA8418 I2C keyboard) appears as a supported BUILD TARGET in install_raspyjack.sh (CARDPUTER_320 mode, mpv/rtl-433/chocolate-doom extras) — but that is a SEPARATE device the user does NOT own; confirm whether it runs the same Python codebase under Linux (CardputerZero is a Linux-capable board) vs a port. 4) "https on port 443 / http fallback :8080, IDE on /ide, Ragnar on :8091" came from README parsing — confirm exact ports and that the WebUI requires auth (v1.0.5 added authentication). 5) No UART/serial control surface was found in any source — confirmed absent, but flag for certainty. 6) Whether any owned USB Wi-Fi dongle (the user lists "315MHz antennas / IPEX->SMA pigtails" but no RTL8812AU/AR9271 adapter) actually exists for monitor mode — Wi-Fi attacks are blocked without one.
