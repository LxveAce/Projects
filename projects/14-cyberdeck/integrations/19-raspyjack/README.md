# Cyberdeck Integration: RaspyJack

> **Source project:** [Project 19 — RaspyJack](../../../19-raspyjack/)
> **Board:** Raspberry Pi Zero 2 W (dedicated unit — separate from Pwnagotchi)
> **Deck role:** Wired network pentesting + Linux-based reconnaissance
> **Power:** Hub → switch SW9 (or PiSugar battery)
> **Display:** Waveshare 1.44" LCD HAT (self-contained)
> **Network:** USB-to-Ethernet adapter (wired attacks)

---

## What This Does in the Deck

RaspyJack fills a gap no other device in the deck covers: **wired network attacks.** Every ESP32 board does wireless (WiFi/BLE/RF), but none can plug into an Ethernet port and run Responder, ARP MITM, DNS spoofing, or Nmap scans on a wired LAN.

**Key capabilities:**
- **Wired network pentesting** — plug into a switch/router and attack
- **Responder** — LLMNR/NBT-NS/MDNS poisoning for credential capture
- **ARP MITM** — man-in-the-middle with live traffic analysis
- **DNS spoofing** — redirect DNS queries to capture credentials
- **Nmap scanning** — network discovery and service enumeration
- **Evil portal** — 84 captive portal templates
- **231+ payloads** — scripts ready to run from the LCD menu
- **WebUI** — accessible from Pi 5's browser for remote control

### The Dock Concept

Like Pwnagotchi, RaspyJack sits in a dock slot inside the cyberdeck case. It operates independently but can be controlled from the Pi 5's dashboard via WebUI:

1. Pi 5 connects to RaspyJack's WiFi AP (or via USB networking)
2. Open `http://raspyjack.local` in Chromium on the 7" DSI display
3. Full dashboard: payload browser, code IDE, loot viewer, remote control

For wired attacks, run an Ethernet cable from RaspyJack's USB-to-Ethernet adapter through a cable pass-through in the Pelican case to the target network.

---

## Hardware Assignment

| Component | Source | Notes |
|-----------|--------|-------|
| Raspberry Pi Zero 2 WH | **Purchase** (~$15-20) | Dedicated to RaspyJack (don't repurpose Pwnagotchi Pi) |
| Waveshare 1.44" LCD HAT | **Purchase** (~$12-15) | ST7735S, 128x128, joystick + 3 buttons |
| Micro SD card (16GB+) | INVENTORY | RaspyJack OS image |
| USB OTG adapter | **Purchase** (~$3-5) | Micro-USB to USB-A for adapters |
| USB-to-Ethernet adapter | **Purchase** (~$5-10) | For wired network attacks |

**Total new cost: ~$35-50**

---

## Setup for the Deck

1. Flash latest RaspyJack image to SD card
2. Attach Waveshare 1.44" LCD HAT to Pi Zero GPIO
3. Connect USB OTG adapter → USB-to-Ethernet adapter
4. Power via USB from deck's powered hub (switch SW9)
5. Boot — LCD shows payload menu
6. Access WebUI from Pi 5 for remote control

---

## Standalone Mode

Pull RaspyJack from the dock → power via any USB source or PiSugar battery → fully portable wired/wireless network pentesting toolkit with its own LCD screen and controls.

---

## Deck Placement

RaspyJack + LCD HAT is small enough to mount on the inner lid or side panel of the Pelican case. Route USB-to-Ethernet cable through a waterproof cable gland in the case wall for field connections.

---

*Decision-made guide for the cyberdeck build. See [Project 19](../../../19-raspyjack/) for the full research and all options.*
