# BW16 / RTL8720DN — Hardware-Validated (Vampire Deauther, dual-band, CyberC-flashable)

Validation notes for the **EC Buying BW16-Kit (RTL8720DN ×3)** in inventory. Confirmed on real
hardware this session. Additive to `README.md` (which currently notes "no BW16 board is needed" for
5 GHz because Panda + Kismet on the Pi cover it — see "Role" below for why that can be revisited).

## What it is
- **RTL8720DN = Realtek AmebaD** (dual-core KM4 Cortex-M33 + KM0 M23). Dual-band **2.4 + 5 GHz** WiFi
  + BLE 5.0. **NOT an ESP32** — `esptool` and `ltchiptool` do **not** work on it.
- Onboard **CH340** USB-UART (shares VID/PID 1A86:7523 with classic ESP32 — can't be told apart by
  USB IDs alone; identify by the serial banner or pick the firmware manually).

## Flashing (AmebaD ImageTool, NOT esptool)
- Tool: Realtek `upload_image_tool` (from `ambiot/ambd_arduino`); on Windows it's a Cygwin build that
  needs `cygwin1.dll` beside it. Flashes a **3-file AmebaD bundle** at fixed offsets:
  `km0_boot_all.bin` @0x08000000, `km4_boot_all.bin` @0x08004000, `km0_km4_image2.bin` @0x08006000,
  plus the SRAM loader `imgtool_flashloader_amebad.bin`.
- **Auto-download via DTR/RTS works** on the BW16-Kit — no BOOT/RESET button press needed.
- **Effectively unbrickable over UART** (mask-ROM loader); best practice is still dump-first where the
  tool supports it.

## Firmware: Vampire Deauther (validated)
- Source bundle: `vampel/vampel.github.io` (raw files). Real **`AT+` serial CLI @115200**:
  `AT+SCAN` · `AT+DEAUTHIDX=<n>` · `AT+DEAUTHIDX=ALL` · `AT+BEACONRANDOM=<n>` · `AT+STOP`.
- `AT+SCAN` performs a real **dual-band** scan — confirmed returning both 2.4 GHz (CH 1–11) and
  **5 GHz (CH 36–165)** APs. Scan line format: `<idx>: <SSID> (CH <n>, RSSI <n>)`.

## Flashable end-to-end from CyberC
- Cyber Controller now flashes the BW16 directly: `rtl8720` flash backend + `RtlAmeba8720Profile` +
  the `bw16` protocol parser. It downloads the Vampire bundle and drives the AmebaD ImageTool;
  validated end-to-end (checksum verified) through `FlashEngine`. The Realtek tool isn't bundled
  (Cygwin/GPL vs MIT repo) — set `CYBERC_AMEBAD_TOOL` or drop it in `tools/realtek/`. See
  `cyber-controller/docs/HARDWARE-FIRMWARE-MATRIX.md`.

## Antenna
- Works fine on the **onboard PCB antenna** (scanned 24 APs across both bands). Optional external:
  move the 0Ω jumper from the PCB-antenna path to the U.FL/IPEX pad and attach a **U.FL→SMA pigtail**
  (the Rydocyee IPEX→SMA pigtails in inventory fit) + a **dual-band** SMA antenna (not 2.4-only).

## Role — worth revisiting
The deck design note said "no BW16 needed" because the Pi's Panda 6E + Kismet cover 5 GHz. That still
holds for *passive 5 GHz wardriving*. But with 3 BW16-Kits + a working dual-band deauther, the BW16
now offers something the Pi path doesn't: a **low-power, ESP-class, standalone 5 GHz scan/deauth radio**
that CyberC can drive over `AT+` and feed into cross-comm — independent of the Pi being up. Complement,
not replacement. (Owner's design call.)
