# Pi 5 Brain — Cyberdeck Integration

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Source of truth:** the deck [README](../../../README.md) (Section 11 — Software Integration)
> **Deck role:** The brain — runs Kismet, the dashboard, `gpsd`, and opens serial to every ESP32
> **Status:** Ready to build (Pi 5 + 128 GB SD in inventory)

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Compute** | Raspberry Pi 5 **8GB** |
| **OS** | **Kali Linux** (ARM image) |
| **Boot media** | **128 GB** micro SD |
| **GPIO use** | Tiny — **3-4 pins** total, no expander |
| **OLED bus** | I2C1: **SDA=GPIO2 / SCL=GPIO3** (2.42" SSD1309 OLED) |
| **Fan control** | **PWM=GPIO18** (Noctua NF-A4x10) |
| **USB 3.0 #1** | Panda PAU0F — **direct, always on** |
| **USB 3.0 #2** | Powered USB hub upstream (all ESP32s + RT5370 + flash) |
| **USB 2.0** | VK-162 GPS + wired keyboard |
| **Serial** | Every ESP32 at **115200 baud** |

> **Why the Pi 5 8GB / Kali / direct-Panda layout:** the Pi is the single brain that aggregates
> every subsystem. Kali ships Kismet + 600+ tools, so nothing has to be built from scratch. The
> Panda PAU0F sits on its own USB 3.0 lane (not the hub) so Kismet always gets full bandwidth; the
> hub carries everything serial and low-speed. GPIO stays nearly empty on purpose — only the OLED
> and the fan touch it, leaving 22+ pins free.

> **Critical:** keep the Panda on **USB 3.0 #1 directly** — never on the hub. Routing it through the
> hub starves Kismet of bandwidth. The hub upstream goes on USB 3.0 #2.

---

## What You Need (from the repo inventory)

- Raspberry Pi 5 8GB — from the CanaKit kit ([INVENTORY.md](../../../../../INVENTORY.md))
- 128 GB micro SD card (Kali OS + Kismet data)
- 2.42" SSD1309 OLED (128x64, I2C) — system vitals on GPIO
- Noctua NF-A4x10 5V fan — PWM on GPIO18
- Panda PAU0F WiFi 6E adapter (USB 3.0)
- Powered 7-port USB hub (hub upstream on USB 3.0 #2)
- VK-162 USB GPS module (USB 2.0)
- Wired USB mini keyboard (USB 2.0, BLE stealth)
- USB-C PD power from the [Anker 347](../power/) (always on)
- Another machine + SD reader to flash the image

---

## Get It Running

### 1. Flash Kali

1. Download the **Kali Linux ARM image for the Raspberry Pi 5** from kali.org.
2. Write it to the 128 GB micro SD with **Raspberry Pi Imager** or `dd` / balenaEtcher.
3. Insert the SD into the Pi 5.

### 2. First boot + setup

1. Boot the Pi 5 on the [7" DSI display](../displays/) with the wired keyboard attached.
2. Log in, then update:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   ```
3. Enable SSH (so the deck can run headless later):
   ```bash
   sudo systemctl enable --now ssh
   ```
4. Install the core packages — Kismet plus the Python plumbing the dashboard/serial/GPS need:
   ```bash
   sudo apt install -y kismet gpsd gpsd-clients
   pip install pyserial flask flask-socketio meshtastic kismet-rest gps3
   ```

### 3. Wire the buses

- **OLED (I2C1):** 2.42" SSD1309 → SDA=**GPIO2** (phys pin 3), SCL=**GPIO3** (phys pin 5), VCC=3.3V (pin 1), GND (pin 14). Enable I2C with `sudo raspi-config` (Interface Options → I2C).
- **Fan (PWM):** Noctua NF-A4x10 → PWM=**GPIO18** (phys pin 12), +5V (pin 4), GND (pin 9). Temperature-based control via `/boot/config.txt`:
  ```
  dtoverlay=gpio-fan,gpiopin=18,temp=55000
  ```
- **USB 3.0 #1:** Panda PAU0F **direct** — always powered with the Pi, full bandwidth for Kismet.
- **USB 3.0 #2:** powered USB hub upstream → all ESP32s (serial), RT5370 (monitor), flash drive.
- **USB 2.0 #1:** VK-162 GPS (`/dev/ttyACM0`). **USB 2.0 #2:** wired keyboard.
- **Power:** USB-C PD from the Anker 347 → Pi 5, always on (no toggle switch on the brain).

### 4. Verify

```bash
i2cdetect -y 1                  # OLED should show at 0x3C (or 0x3D)
ls /dev/ttyUSB* /dev/ttyACM*    # ESP32s (ttyUSB*) + GPS (ttyACM0)
cgps -s                         # GPS fix once gpsd is up
sudo kismet                     # then browse http://localhost:2501
```
All ESP32 serial links open at **115200 baud** (`screen /dev/ttyUSB0 115200`).

---

## Cyberdeck Compatibility Notes

- **Kismet:** the brain runs the primary [Kismet wardriving](../../07-kismet-wardriving/) stack —
  Panda PAU0F on USB 3.0 #1, RT5370 (secondary monitor) through the hub. Kismet REST API at
  `http://localhost:2501`.
- **Dashboard:** the Flask + SocketIO [dashboard](../dashboard/) runs here, parsing every ESP32's
  serial output and serving the UI to Chromium kiosk on the 7" screen.
- **GPS:** the VK-162 feeds one [`gpsd`](../gps/) daemon at `localhost:2947`, shared to Kismet,
  Meshtastic, the dashboard, and Flock/BLE timestamps.
- **ESP32s:** the Pi opens serial to Gold #1/#2/#3, Heltec, and the WROOM-32 — all at 115200 over
  the powered hub on USB 3.0 #2.
- **Displays:** the [2.42" OLED](../displays/) rides GPIO I2C1 for system vitals; the 7" DSI is the
  primary screen. The DSI uses a separate I2C bus, so no conflict with the OLED on I2C1.
- **Power:** the Pi is the one **always-on** device, fed USB-C PD straight from the
  [Anker 347](../power/) — it is *not* on a per-device toggle switch.
- **GPIO headroom:** only 3-4 pins used; 22+ free for future sensors/LEDs/buzzer, no expander.

## Standalone Mode

Pull the SD (or the whole Pi) out of the deck and it is just a Kali Raspberry Pi 5 — boot it on any
HDMI/DSI display with a keyboard and run Kismet, the dashboard, `gpsd`, and serial tools exactly the
same way. Nothing in the deck wiring is required; the USB/GPIO map above is the only thing that
changes when it goes back into the case.

## Source / Upstream

- Kali ARM images: [kali.org/get-kali](https://www.kali.org/get-kali/) (Raspberry Pi 5 image)
- Full deck software spec: [Project 14 README — Section 11](../../../README.md)
- Kismet build/usage: [projects/07-kismet-wardriving](../../07-kismet-wardriving/)
