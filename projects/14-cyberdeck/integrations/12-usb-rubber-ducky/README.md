# USB Rubber Ducky — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../README.md) · **Integrations index:** [integrations/](../README.md)
> **Full reference (all options):** [projects/12-usb-rubber-ducky](../../../12-usb-rubber-ducky/)
> **Deck role:** Keystroke-injection payload runner — a stored dongle, plugged in only when needed
> **Status:** DIY route (buy a small ESP32-S2 Mini; flashed with the deck's web flasher)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Path** | **DIY on owned-class hardware** — *not* the Hak5 hardware to start |
| **Board** | **ESP32-S2 Mini** (~$5-8) — native USB OTG/HID, the go-to DIY Ducky platform |
| **Firmware** | **[SuperWiFiDuck](https://github.com/wasdwasd0105/SuperWiFiDuck)** — DuckyScript-compatible, WiFi web UI for payloads |
| **Flash tool** | [ESP Terminator](../13-esp-terminator/) web flasher (same flasher used for every deck ESP32) |
| **Payloads** | [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads) (authorized use only) |
| **Form** | Small dongle stored in the deck; plug into a target **or the Pi 5** on demand |
| **Power** | Powered by the host it's plugged into — **no permanent hub port or toggle** |
| **Upgrade** | Hak5 USB Rubber Ducky Mark IV (~$80-100) — buy later for polish, not to get running |

> **Why DIY, not the Hak5 unit:** the repo lists the Hak5 USB Rubber Ducky (~$80) as
> *low priority (can DIY)*. An ESP32-S2 flashed with SuperWiFiDuck gives native USB HID
> plus WiFi payload management (edit/deploy over a web UI — no reflash per payload), at a
> fraction of the cost. The Hak5 unit is the later upgrade for stealth and DuckyScript 3.0,
> not the get-running choice.

> **Critical:** the deck's **ESP32-WROOM-32** (inventory #5) **cannot** do this — it has no
> native USB HID (it sits behind a USB-to-serial bridge chip). The owned **Waveshare
> ESP32-C5** boards *do* have native USB, but the repo reserves their RISC-V chips for WiFi 6
> research. So this subsystem gets its **own dedicated ESP32-S2 Mini** rather than borrowing a
> deck board.

> **Authorization:** keystroke injection is only legal against systems you **own or are
> explicitly authorized to test** in writing. Unauthorized use is a criminal offense (CFAA in
> the US, Computer Misuse Act in the UK, etc.). See the legal section in the
> [full source](../../../12-usb-rubber-ducky/).

---

## What You Need

- **ESP32-S2 Mini** dev board (~$5-8) — buy one; native USB HID is required
- USB cable / direct USB plug for the board (also used for flashing)
- A PC running **Chrome or Edge** for the web flasher (WebSerial)
- WiFi-capable phone or laptop to reach the SuperWiFiDuck web UI
- Payloads from [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads)
- *(Not from deck inventory — the WROOM-32 and C5 are unsuitable/reserved; see above)*

---

## Get It Running

### 1. Flash the DIY Ducky

1. Open **Chrome or Edge** (WebSerial required — Firefox/Safari won't work).
2. Go to the deck's flasher: [ESP Terminator](../13-esp-terminator/) ([espterminator.com](https://espterminator.com/)).
3. Plug the **ESP32-S2 Mini** into your PC.
4. Hold **BOOT**, click **Connect**, pick the COM port, release BOOT.
5. Select the **SuperWiFiDuck** firmware target (or flash the SuperWiFiDuck build per its repo).
6. Click **Install** / **Flash**, wait for "complete," then press **RST**.

CLI alternative (same result):
```bash
pip install esptool
esptool.py --chip esp32s2 --port /dev/ttyUSB0 --baud 921600 \
  write_flash 0x0 superwifiduck.bin
```
(If it stalls at connect, hold BOOT during connect and drop to `--baud 115200`.)

### 2. Load a payload

1. After first boot, the board exposes its own **WiFi access point**.
2. Join that AP and open the **SuperWiFiDuck web interface** in a browser.
3. Paste a DuckyScript payload (standard syntax) — grab one from
   [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads), e.g. a
   recon `systeminfo`/`ipconfig`/`whoami` grabber.
4. Save it. No reflash needed — swap payloads any time over WiFi.

A minimal "open Notepad" sanity payload:
```ducky
DELAY 2000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRINGLN Hello from the deck Ducky!
```

### 3. Use with / around the deck

- **As a dropped dongle:** unplug from your setup machine, plug into the **authorized target**;
  it enumerates as a keyboard and runs the payload.
- **Against the Pi 5:** plug into a free Pi 5 USB port to test payloads on the deck itself
  (handy for building/validating before deployment).
- **Stored, not wired:** keep it loose in the deck's small-parts pocket — it draws power only
  from whatever host it's plugged into, so it touches no powered-hub port and no toggle switch.

### 4. Verify

- LED/status comes up and the SuperWiFiDuck AP appears in your WiFi list.
- Plug into the Pi 5 (or your own PC) and trigger the payload — Notepad opens and types the
  test line.
- Confirm payload swaps take effect over the web UI without reflashing.

---

## Cyberdeck Compatibility Notes

- **USB/serial budget:** consumes **nothing** in standby — it's a stored dongle, not a
  hub-attached board. No SW toggle, no `/dev/ttyUSB*` claim, no antenna bulkhead.
- **No board conflict:** it does **not** reuse Gold #1/#2/#3, the WROOM-32, or the C5 boards —
  those stay dedicated to their assigned radios (see the index's master wiring table).
- **Flashing shares the [ESP Terminator](../13-esp-terminator/) workflow** with every other
  deck ESP32 — one flasher, same Chrome/Edge + BOOT/RST routine.
- **Pi 5 pairing:** the Pi 5 brain is both a payload **test target** and a place to keep the
  payload library / clone the upstream repo.
- **Authorization scope:** only fire payloads at hardware you own or are contracted to test.

## Standalone Mode

This subsystem is standalone by design — it never wires into the chassis. The ESP32-S2 +
SuperWiFiDuck dongle works the same on a bench, in a pocket, or plugged into any host: power
comes from the target's USB port, payloads are managed over its own WiFi AP. The deck is just
where it's stored and (optionally) tested against the Pi 5.

## Source / Upstream

- DIY firmware: [wasdwasd0105/SuperWiFiDuck](https://github.com/wasdwasd0105/SuperWiFiDuck)
- Payloads: [hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads)
- Deck flasher guide: [13-esp-terminator](../13-esp-terminator/)
- Inventory: [INVENTORY.md](../../../../INVENTORY.md)
- Full options, DuckyScript, DIY comparison, legal notes: [projects/12-usb-rubber-ducky](../../../12-usb-rubber-ducky/)
