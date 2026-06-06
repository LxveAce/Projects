# Pwnagotchi: Comprehensive Guide

An AI-powered WiFi auditing tool built on Raspberry Pi Zero W, using deep reinforcement learning to maximize WPA handshake captures.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Hardware List](#2-hardware-list)
3. [Soldering Guide for GPIO Headers](#3-soldering-guide-for-gpio-headers)
4. [Detailed Troubleshooting](#4-detailed-troubleshooting)
5. [Setup Guide](#5-setup-guide)
6. [Best Plugins](#6-best-plugins)
7. [Verify Captures Without Display](#7-verify-captures-without-display)
8. [All Resources](#8-all-resources)

---

## 1. Overview

### What Is Pwnagotchi?

Pwnagotchi is an A2C (Advantage Actor-Critic) reinforcement learning AI that instruments [bettercap](https://www.bettercap.org/) to passively and actively audit WiFi networks. It runs on a Raspberry Pi Zero W, looks like a Tamagotchi with facial expressions, and learns from its surrounding WiFi environment to maximize the crackable WPA key material it captures. It collects PCAP files containing full and half WPA handshakes as well as PMKIDs, which are compatible with hashcat for offline cracking.

### How the AI Works

Pwnagotchi uses A2C reinforcement learning -- the same class of algorithms used in game-playing AI -- but instead of training on games, it tunes its own parameters over time to get better at pwning WiFi in real-world environments. Over time, it adjusts its behavior (channel hopping timing, deauthentication aggressiveness, target selection) based on what yields the most handshakes. Its "mood" (face expressions) reflects how well it is performing.

### What Bettercap Does

Bettercap is the underlying network attack framework. It handles the actual WiFi operations: monitor mode, packet capture, deauthentication attacks, and PMKID collection. Pwnagotchi sits on top of bettercap as an AI controller, telling bettercap what to do and when. Bettercap runs via caplet files (`pwnagotchi-auto.cap` for autonomous mode, `pwnagotchi-manual.cap` for manual mode).

### Operating Modes

- **AUTO mode**: Fully autonomous. Runs when powered by battery (not connected to PC). Hunts for handshakes independently.
- **MANUAL (MANU) mode**: Active when connected to a PC via USB. You can SSH in and configure it while it stays idle.
- **AI mode**: The reinforcement learning is actively making decisions (subset of AUTO mode once the AI model is loaded).

---

## 2. Hardware List

### Raspberry Pi (the "brain")

| Board | Status | Notes |
|-------|--------|-------|
| **Pi Zero W** | Officially supported | The original target. Has WiFi + mini HDMI + micro USB. Requires soldering GPIO header. |
| **Pi Zero WH** | Recommended for beginners | Same as Zero W but with pre-soldered GPIO header. No soldering needed. |
| **Pi Zero 2 W** | Supported (jayofelony fork) | Faster quad-core CPU, same form factor. Use jayofelony's image (v2.9.x+). |
| **Pi Zero 2 WH** | Best for beginners | Zero 2 W with pre-soldered header. |
| Pi 3B/3B+ | Supported with caveats | Requires more power, has ethernet for easier setup. |
| Pi 4B | Supported with caveats | Overkill but works. Needs underclocking (`arm_freq=800` in config.txt) for battery life. |

### Compatible Displays

| Display | Config Value | Resolution | Notes |
|---------|-------------|------------|-------|
| **Waveshare 2.13" V2** | `waveshare_2` | 250x122 | **Officially recommended**. Best partial refresh support. |
| Waveshare 2.13" V1 | `waveshare_1` | 250x122 | Legacy, hard to find new. |
| Waveshare 2.13" V3 | `waveshare_3` | 250x122 | Newer revision, well supported. |
| Waveshare 2.13" V4 | `waveshare_4` or `waveshare213inb_v4` | 250x122 | Latest revision. Some firmware images need patching. |
| Waveshare 2.7" V1 | `waveshare27inch` | 264x176 | Larger display. |
| Waveshare 2.7" V2 | `waveshare27inch_v2` | 264x176 | Updated driver. |
| Waveshare 2.9" | `waveshare2in9` | 296x128 | Wide format. |
| Waveshare 1.54" | `waveshare1in54` | 152x152 | Square, compact. |
| Pimoroni Inky pHAT | `inky` | 212x104 | Good alternative. |
| PaPiRus | `papirus` | Various | Another e-ink option. |
| DFRobot e-Ink | `dfrobot` | Various | Less common. |
| OLED HAT | `oledhat` | 128x64 | Monochrome OLED, fast refresh. |
| Waveshare 1.44" LCD | `waveshare144lcd` | 128x128 | Color LCD option. |
| Waveshare 3.5" LCD | `waveshare35lcd` | 480x320 | Large color LCD. |
| DisplayHAT Mini | `displayhatmini` | 320x240 | Color LCD, ST7789 controller. |
| Dummy/Headless | `dummydisplay` | N/A | No physical display, web UI only. |

### Batteries / Power

| Battery | Runtime (approx.) | Notes |
|---------|-------------------|-------|
| 1200 mAh power bank | ~5 hours | Minimum viable. |
| 5000 mAh power bank | ~18 hours | Good daily carry. |
| 10000 mAh power bank | ~36 hours | Extended sessions. |
| 25600 mAh power bank | ~49 hours | Marathon sessions. |
| **PiSugar 3** | Varies by cell | Integrated battery HAT, compact, has RTC. Recommended. |
| **UPS-Lite V1.1** | Varies by cell | Has battery level indicator. Plugin (`ups_lite.py`) shows voltage on display. Built-in serial adapter. |
| Waveshare UPS HAT | Varies by cell | Another integrated option. |

**Power requirements**: 5V / 2A minimum. 5V / 2.5A recommended. Cheap battery banks can cause voltage sag under load, causing crashes.

### Cases

- 3D-printed custom cases (STL files on Thingiverse, search "pwnagotchi case")
- Modified Altoid tins
- Commercial cases from Noppitlabs, Biscuit Shop, etc.
- Amazon enclosures with drilled holes

### Optional: Hardware Clock (RTC)

The Pi Zero has no onboard clock. For accurate timestamps on captures:

- PCF8523, DS1307, or DS3231 I2C modules
- Can be soldered directly to GPIO to save space
- Enables accurate time tracking when offline

### SD Card

- Minimum 8GB (16GB or 32GB recommended)
- UHS-I speed class or better
- Recommended brands: SanDisk Ultra/Extreme, Samsung EVO
- High-endurance cards preferred (frequent writes)

---

## 3. Soldering Guide for GPIO Headers

If you bought a Pi Zero W (without pre-soldered header), you must solder a 2x20 (40-pin) male header.

### Tools Needed

- Temperature-controlled soldering iron (do NOT use a cheap unregulated iron)
- Fine/conical tip
- Lead-free or 60/40 tin-lead solder (0.8mm diameter recommended)
- Cheap single-sided perfboard (non-plated-through, NOT a breadboard)
- Circuit board holder or "third hand" with clips
- Flux (liquid or pen)
- Flux remover / isopropyl alcohol
- Old toothbrush (for cleaning)
- Magnifying glass or loupe
- Multimeter (for post-solder verification)

### Step-by-Step Process

1. **Prepare the header**: Insert the 40-pin male header (long pins down) into a cheap perfboard. This holds the pins straight and stable.

2. **Mount the Pi**: Place the Pi Zero upside-down onto the header pins protruding through the perfboard. The Pi's top (component side) faces down.

3. **Secure in holder**: Clamp the entire assembly (perfboard + Pi) in a circuit board holder or third hand.

4. **Set temperature**: 350-370 degrees C (660-700 degrees F) for lead-free solder. 300-320 degrees C (570-610 degrees F) for leaded solder.

5. **Solder corner pins first**: Start with one corner pin, then the diagonally opposite corner. Check alignment before proceeding -- the header must be perfectly perpendicular.

6. **Solder remaining pins**: Work through all 40 pins. For each pin:
   - Touch the iron tip to BOTH the pad and the pin simultaneously (heat both)
   - Wait 1-2 seconds for heat to transfer
   - Feed solder into the junction (not onto the iron tip)
   - Let solder flow and form a small concave "mountain" (volcano shape) around the pin
   - Remove solder wire first, then remove iron
   - Total contact time per pin: 3-5 seconds maximum

7. **Do NOT linger**: Excessive heat damages PCB traces and pads. If a joint does not take, let it cool, add flux, and retry.

### Good vs. Bad Solder Joints

| Good Joint | Bad Joint |
|-----------|-----------|
| Shiny, smooth, concave cone shape | Dull, grainy, rough texture (cold joint) |
| Solder wets both pin and pad | Solder balls up on pin, does not touch pad |
| Pin fully surrounded by solder | Visible gap between solder and pad |
| No cracks visible | Cracks visible in the solder |

### Post-Solder Inspection

1. **Visual inspection**: Use a magnifying glass. Check every pin for:
   - Cold joints (dull/grainy appearance)
   - Bridges (solder connecting two adjacent pins)
   - Insufficient solder (pin visible with no solder cone)
   - Lifted pads

2. **Clean residue**: Apply flux remover or isopropyl alcohol with a toothbrush. Scrub gently around all joints.

3. **Multimeter continuity test** (critical if display is not working):
   - Set multimeter to resistance mode (200 ohm range) or continuity/beep mode
   - Touch one probe to the TOP of the GPIO pin (where the display plugs in)
   - Touch the other probe to the BOTTOM solder joint on the PCB
   - A good joint reads less than 1 ohm (or beeps in continuity mode)
   - Do NOT press hard on the solder -- pressing can compress a cold joint and create temporary contact, giving a false positive
   - Test EVERY pin used by your display (see SPI pin table in section 4A below)

---

## 4. Detailed Troubleshooting

### 4A. Display Blank / Not Working

This is the most common Pwnagotchi issue. Work through these checks in order.

#### Check 1: Correct `ui.display.type` in config.toml

This is wrong in "almost every case" according to experienced builders. The display type string must EXACTLY match your hardware version.

Open your config.toml (on the SD card's boot partition, or at `/etc/pwnagotchi/config.toml` via SSH) and verify:

```toml
ui.display.enabled = true
ui.display.type = "waveshare_2"   # MUST match your exact display version
ui.display.color = "black"
ui.fps = 0                         # 0 = update only on changes (required for e-ink)
ui.display.rotation = 180          # Try 0 if image is upside down
```

**How to identify your Waveshare version**: Look at the back of the display PCB. It will say "2.13inch e-Paper HAT (V2)", "(V3)", or "(V4)". Match accordingly:

| Display Version | Config Value |
|----------------|--------------|
| V1 | `waveshare_1` |
| V2 | `waveshare_2` |
| V3 | `waveshare_3` |
| V4 | `waveshare_4` (some images need `waveshare213inb_v4`) |

#### Check 2: SPI Is Enabled

SPI must be enabled in the Pi's boot config. Check `/boot/config.txt` for:

```
dtparam=spi=on
```

If missing, add it. The Pwnagotchi image should include this by default, but verify.

#### Check 3: Physical Pin Connections (Waveshare 2.13" HAT SPI Pinout)

The Waveshare 2.13" e-Paper HAT uses these GPIO connections when plugged into the 40-pin header:

| Display Signal | Function | BCM GPIO | Physical Pin |
|---------------|----------|----------|-------------|
| VCC | 3.3V Power | 3.3V | Pin 1 or 17 |
| GND | Ground | GND | Pin 6, 9, 14, 20, 25, 30, 34, or 39 |
| DIN (MOSI) | SPI Data In | GPIO 10 (SPI0_MOSI) | Pin 19 |
| CLK (SCLK) | SPI Clock | GPIO 11 (SPI0_SCLK) | Pin 23 |
| CS (CE0) | SPI Chip Select | GPIO 8 (SPI0_CE0) | Pin 24 |
| DC | Data/Command | GPIO 25 | Pin 22 |
| RST | Reset | GPIO 17 | Pin 11 |
| BUSY | Busy Status | GPIO 24 | Pin 18 |

**If you soldered the header yourself**, use your multimeter to test continuity on EACH of these specific pins. A single bad joint on DIN, CLK, CS, DC, RST, or BUSY will cause a blank display.

#### Check 4: Display Seated Properly

- The HAT connector must be fully pushed onto the GPIO header
- All 40 pins should be engaged
- No bent pins
- Remove and re-seat the display firmly

#### Check 5: Validate config.toml Syntax

TOML is strict. A single misplaced quote, missing quote, extra comma, or wrong bracket silently breaks the config. Validate your config at: https://www.toml-lint.com

#### Check 6: Check Logs via SSH

If you can SSH in but the display is blank:

```bash
# View Pwnagotchi logs
tail -f /var/log/pwnagotchi.log

# Run in debug mode
sudo pwnagotchi --debug

# Check for display-related errors
grep -i "display\|waveshare\|spi\|epd" /var/log/pwnagotchi.log
```

Look for errors like "SPI not available", "display init failed", or "No module named" which indicate driver/config issues.

#### Check 7: Test with dummydisplay

Temporarily set `ui.display.type = "dummydisplay"` in config.toml. If Pwnagotchi boots and works (visible via web UI at `http://10.0.0.2:8080`), the issue is display-specific, not a boot problem.

---

### 4B. HDMI Shows Nothing (Blank / No Signal)

The Pi Zero W has a mini-HDMI port. When troubleshooting, you may want to see boot output. If HDMI shows nothing:

#### Check 1: Power Supply

Insufficient power is the number one cause. Requirements:

- Use a known-good 5V / 2.5A power supply
- Do NOT use a cheap battery bank during troubleshooting -- use a wall adapter
- Try powering via the DATA micro-USB port (not the POWER port) -- some setups only boot from the data port
- Check that the green LED blinks (reading SD card). If only solid red + no green = bad SD card or bootloader

#### Check 2: SD Card / Image

- Re-flash the SD card with a fresh image using Balena Etcher or Raspberry Pi Imager
- Verify the SD card has a `boot` partition with files like `kernel.img`, `cmdline.txt`, `config.txt`
- Try a different SD card (some cards are silently defective)
- Verify SHA-256 checksum of the downloaded image

#### Check 3: Force HDMI Output

Edit `/boot/config.txt` on the SD card (mount on your PC):

```
# Force HDMI output even without hotplug detect
hdmi_force_hotplug=1

# Force HDMI audio mode (ensures video output)
hdmi_drive=2

# Boost HDMI signal strength (try 4, up to 9 if needed)
config_hdmi_boost=4

# Force a specific resolution if auto-detect fails
# hdmi_group=1
# hdmi_mode=1
```

#### Check 4: Mini-HDMI Adapter/Cable

- The Pi Zero uses mini-HDMI, NOT micro-HDMI
- Ensure your adapter is mini-HDMI (type C) to full HDMI (type A)
- Some cheap adapters have poor contact -- try a different one
- Some Pi Zero cases prevent the mini-HDMI plug from fully inserting
- Try a direct mini-HDMI to HDMI cable instead of an adapter
- Use a shorter cable (long cables can lose signal)

#### Check 5: Wait for First Boot

- First boot takes 3-10 minutes for RSA key generation
- Do NOT unplug during first boot -- interrupting key generation corrupts the install
- The HDMI output may not appear until the OS is fully booted
- Note: Pwnagotchi does NOT output its face to HDMI by default -- HDMI shows the Linux console, not the Pwnagotchi UI

#### Check 6: LED Diagnostics

| LED State | Meaning |
|-----------|---------|
| Solid red, no green blink | Bad SD card, corrupt image, or missing bootloader |
| Green LED blinking | Pi is reading the SD card and attempting to boot (good sign) |
| Green LED solid then off | Boot completed (or failed after loading kernel) |
| No LEDs at all | Dead Pi, bad power, or bad solder on power pins |

#### Check 7: Pwnagotchi-Specific HDMI Note

By default, Pwnagotchi sends its UI to the e-ink display, NOT to HDMI. HDMI will only show the Linux console/terminal. There is a community project for HDMI output: [pwnagotchi-hdmi-viewer](https://github.com/solution-libre/pwnagotchi-hdmi-viewer) that can mirror the Pwnagotchi face to HDMI for debugging.

---

### 4C. SSH Testing (Verify Pi Is Alive Without Any Display)

This is the most important diagnostic. If SSH works, your Pi is alive and booting -- the problem is display-only.

#### Windows Setup

1. Connect Pi Zero to PC via the DATA micro-USB port (the one closer to the center of the board, NOT the one on the edge labeled PWR)
2. Wait 2-3 minutes for boot
3. Windows should detect a new USB Ethernet/RNDIS device. If not, install RNDIS driver manually.
4. Open Network Connections (`ncpa.cpl`), find the new RNDIS adapter
5. Set IPv4 manually:
   - IP: `10.0.0.1`
   - Subnet: `255.255.255.0`
   - Gateway: leave blank
   - DNS: leave blank
6. Open PowerShell or Command Prompt:

```
ping 10.0.0.2
```

If it replies, the Pi is alive. Then SSH in:

```
ssh pi@10.0.0.2
```

Default password: `raspberry` (change it immediately with `passwd`)

#### Mac/Linux Setup

1. Connect via data USB port
2. A new network interface appears automatically
3. Configure it to IP `10.0.0.1`, subnet `255.255.255.0`
4. `ssh pi@10.0.0.2`

#### If SSH Fails

- Verify you are using a DATA cable (not power-only). Many micro-USB cables are charge-only.
- Try a different USB cable
- Try a different USB port on your PC
- Verify the RNDIS adapter appeared in your OS
- Wait longer (first boot can take up to 10 minutes)
- Check that `dtoverlay=dwc2` is in `/boot/config.txt` and `modules-load=dwc2,g_ether` is appended to `/boot/cmdline.txt` (the Pwnagotchi image should include these)

---

### 4D. Multimeter Continuity Testing for Solder Joints

> **STATUS (2026-06-06):** Continuity tested on all pins with Fluke 17B+ -- ALL PASSED. No cold joints, no bridges. Solder quality is confirmed good. Skip to software/config troubleshooting (Sections 4A-4C).

If display and HDMI both show nothing, and you soldered the GPIO header yourself, bad solder joints are the prime suspect.

#### What You Need

- Digital multimeter with continuity/beep mode (or resistance mode at 200 ohm range)

#### Procedure

1. **Power off the Pi completely**. Remove all cables and battery.

2. **Set multimeter to continuity mode** (the symbol looks like a sound wave or diode with lines). The meter will beep when it detects a connection.

3. **Test critical power pins first**:
   - Pin 1 (3.3V): Probe the top of the pin and the bottom solder joint. Should beep.
   - Pin 2 (5V): Same test. Should beep.
   - Pin 6 (GND): Same test. Should beep.
   - If ANY power pin fails continuity, your Pi is not getting power through the header.

4. **Test all SPI display pins** (see pin table in section 4A above):
   - Pin 19 (MOSI/DIN): Must have continuity
   - Pin 23 (SCLK/CLK): Must have continuity
   - Pin 24 (CE0/CS): Must have continuity
   - Pin 22 (GPIO 25/DC): Must have continuity
   - Pin 11 (GPIO 17/RST): Must have continuity
   - Pin 18 (GPIO 24/BUSY): Must have continuity

5. **Check for bridges**: Set multimeter to continuity mode. Test between adjacent pins (e.g., Pin 1 and Pin 2). They should NOT beep -- if they do, you have a solder bridge (short circuit).

6. **Do NOT press hard on solder joints** during testing. Pressing can compress a cold joint and create temporary contact, giving a false pass.

#### What to Do If You Find Bad Joints

1. **Reflow**: Apply flux to the bad joint. Touch the soldering iron tip to the joint for 2-3 seconds, letting existing solder melt and re-wet. Add a tiny amount of fresh solder if needed. Remove iron.

2. **If pad is lifted**: This is more serious. You may need to run a jumper wire from the pin to the nearest via or trace connected to that GPIO.

3. **After reflow**: Clean with isopropyl alcohol, re-test continuity, then try booting.

---

### Quick Diagnostic Flowchart

Since your display does not work AND HDMI shows nothing, and you soldered the GPIO header yourself:

```
1. Can you SSH in? (Connect data USB, set IP 10.0.0.1, ssh pi@10.0.0.2)
   |
   +-- YES --> Pi is alive. Display issue only.
   |           a. Check ui.display.type matches your exact display version
   |           b. Validate config.toml syntax at toml-lint.com
   |           c. ~~Multimeter continuity test~~ DONE - all pins passed (2026-06-06)
   |           d. Try dummydisplay mode to isolate display vs config
   |           e. Try a different display if possible
   |
   +-- NO --> Pi may not be booting.
              a. Check LED: solid red only = bad SD card. Reflash.
              b. Check LED: no LEDs at all = power issue or dead Pi.
              c. ~~Multimeter test solder joints~~ DONE - all passed (2026-06-06)
              d. Try a different USB cable (must be data-capable)
              e. Try a different SD card with fresh flash
              f. Add hdmi_force_hotplug=1 to /boot/config.txt
              g. If all fails: try a Pi Zero WH (pre-soldered header)
```

---

## 5. Setup Guide

### Step 1: Download the Image

- **Original project** (evilsocket): https://github.com/evilsocket/pwnagotchi/releases -- older, not actively maintained
- **Jayofelony fork** (recommended, actively maintained): https://github.com/jayofelony/pwnagotchi/releases -- version 2.9.x+, supports Pi Zero 2 W
- **Pwnagotchi.org community**: https://pwnagotchi.org/getting-started/index.html

### Step 2: Flash the SD Card

1. Download and install [Balena Etcher](https://etcher.balena.io) or Raspberry Pi Imager
2. Insert your microSD card
3. Select the downloaded `.img.xz` file
4. Select your SD card as the target
5. Click Flash and wait (~5 minutes)
6. **Do NOT use Raspberry Pi Imager's customization options** (username/password/WiFi). The Pwnagotchi image handles this itself.

### Step 3: Create config.toml

After flashing, the SD card will have a `boot` partition. Create a file called `config.toml` in the root of the boot partition:

```toml
main.name = "pwnagotchi"
main.lang = "en"
main.whitelist = [
    "YourHomeNetwork",
    "AA:BB:CC:DD:EE:FF"
]

ui.display.enabled = true
ui.display.type = "waveshare_2"
ui.display.color = "black"
ui.display.rotation = 180
ui.fps = 0

main.plugins.grid.enabled = true
main.plugins.grid.report = true
```

**Change `ui.display.type`** to match your exact display hardware.

**Add your home network** to the whitelist so it is never attacked.

### Step 4: First Boot

1. Insert SD card into Pi
2. Connect Pi to PC via the DATA micro-USB port (not PWR)
3. Wait 3-10 minutes without touching anything (RSA key generation)
4. The display should show a face, or the USB RNDIS interface should appear on your PC
5. Green LED activity = good. Solid red only = problem.

### Step 5: SSH In and Configure

```bash
ssh pi@10.0.0.2
# Password: raspberry
# Change password immediately:
passwd

# Edit config for further customization:
sudo nano /etc/pwnagotchi/config.toml

# Restart pwnagotchi service after config changes:
sudo systemctl restart pwnagotchi
```

### Step 6: Web UI

Access the web dashboard at: `http://10.0.0.2:8080`

Default credentials: `changeme` / `changeme` (change these in config)

### Step 7: Internet Sharing (for updates/plugins)

**Windows**: In Network Connections, share your WiFi/Ethernet connection with the RNDIS adapter. On the Pi:

```bash
sudo ip route add default via 10.0.0.1
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**Mac/Linux**: Enable IP forwarding and NAT masquerading on the host.

### Step 8: Go Autonomous

Disconnect from PC. Power from a battery bank via the PWR micro-USB port. Pwnagotchi enters AUTO mode and begins hunting for handshakes.

---

## 6. Best Plugins

### Official / Built-in Plugins

| Plugin | What It Does | Enable In config.toml |
|--------|-------------|----------------------|
| **grid** | Connects to PwnGRID community network, reports peers and stats | `main.plugins.grid.enabled = true` |
| **webcfg** | Web-based configuration editor + terminal | `main.plugins.webcfg.enabled = true` |
| **memtemp** | Shows CPU temperature and memory usage on display | `main.plugins.memtemp.enabled = true` |
| **gps** | Saves GPS coordinates with each handshake (requires USB GPS dongle) | `main.plugins.gps.enabled = true` |
| **net-pos** | Geolocation via WiFi (no GPS hardware needed) | `main.plugins.net-pos.enabled = true` |
| **wpa-sec** | Auto-uploads handshakes to wpa-sec.stanev.org for cracking | `main.plugins.wpa-sec.enabled = true` |
| **onlinehashcrack** | Auto-uploads to onlinehashcrack.com | `main.plugins.onlinehashcrack.enabled = true` |
| **wigle** | Uploads data to Wigle.net for wardriving maps | `main.plugins.wigle.enabled = true` |
| **bt-tether** | Bluetooth tethering to your phone for internet + web UI access | `main.plugins.bt-tether.enabled = true` |
| **led** | Blinks the Pi's green LED based on events (handshake = blink pattern) | `main.plugins.led.enabled = true` |
| **auto-update** | Runs apt update/upgrade when internet is available | `main.plugins.auto-update.enabled = true` |
| **session-stats** | Shows current session statistics | `main.plugins.session-stats.enabled = true` |
| **webgpsmap** | Plots captured handshakes on an interactive map (web UI) | `main.plugins.webgpsmap.enabled = true` |
| **ups_lite** | Shows battery voltage for UPS-Lite V1.1 hardware | `main.plugins.ups_lite.enabled = true` |
| **logtail** | View log file through browser | `main.plugins.logtail.enabled = true` |
| **gpio_buttons** | GPIO button support for triggering actions | `main.plugins.gpio_buttons.enabled = true` |
| **show_ip** | Displays IP address on the e-ink screen | `main.plugins.show_ip.enabled = true` |
| **switcher** | Temporarily switch to non-pwnagotchi tasks | `main.plugins.switcher.enabled = true` |

### Recommended Community / Third-Party Plugins

| Plugin | What It Does |
|--------|-------------|
| **hashie** | Converts captured pcap files to hashcat-compatible format automatically |
| **wardriving** | Enhanced wardriving with Wigle.net upload |
| **f0xtr0t** | Enhanced wardriving plugin with better UI |
| **Nomadotchi** | GPS-based travel scoring -- scores unique networks and locations visited |
| **Home Assistant BLE** | Broadcasts mood, battery, handshakes, and uptime via Bluetooth Low Energy to Home Assistant |
| **check_wpa** | Validates whether captured pcap files contain crackable handshake material |
| **Pwnagetty** | Automation tool for handshake retrieval and conversion |
| **V0rT3x suite** | Collection of utility plugins (62 stars on GitHub, actively updated) |

Install community plugins by placing `.py` files in `/usr/local/share/pwnagotchi/custom-plugins/` or the directory specified in `main.custom_plugins` in config.toml.

---

## 7. Verify Captures Without Display

If your display is not working, you can still verify your Pwnagotchi is capturing handshakes.

### Method 1: SSH + File Check

```bash
ssh pi@10.0.0.2

# List captured handshake files
ls -la /home/pi/handshakes/

# Count total captures
ls /home/pi/handshakes/*.pcap 2>/dev/null | wc -l

# Check file sizes (0-byte files = failed captures)
ls -lh /home/pi/handshakes/
```

### Method 2: Web UI

Navigate to `http://10.0.0.2:8080` in your browser. The dashboard shows:

- Current face/mood
- Number of handshakes captured
- Networks seen
- Session statistics

### Method 3: Copy Files to PC and Verify

```bash
# From your PC, copy all handshakes
scp pi@10.0.0.2:/home/pi/handshakes/* ./handshakes/

# Or use a specific file
scp pi@10.0.0.2:/home/pi/handshakes/NetworkName_BSSID.pcap ./
```

### Method 4: Validate Handshake Quality

Not all pcap files contain crackable material. Approximately half may be incomplete.

**Using aircrack-ng** (on your PC):

```bash
aircrack-ng handshake_file.pcap
```

If it finds a valid handshake, it will prompt for a wordlist.

**Using hcxpcapngtool** (convert for hashcat):

```bash
hcxpcapngtool -o hash.hc22000 handshake_file.pcap
```

If the output file is non-empty, the handshake is crackable.

**Using the check_wpa plugin**: Enable it in config.toml to automatically scan your handshakes directory and report which files contain valid material.

### Method 5: Check Pwnagotchi Logs

```bash
ssh pi@10.0.0.2
tail -100 /var/log/pwnagotchi.log | grep -i "handshake\|captured\|pwned"
```

### Method 6: LED Feedback

Enable the `led` plugin. The green LED will blink in specific patterns when handshakes are captured, giving you visual feedback without needing the e-ink display.

---

## 8. All Resources

### Official Resources

- Official website: https://pwnagotchi.ai/
- Official installation guide: https://pwnagotchi.ai/installation/
- Official configuration docs: https://pwnagotchi.ai/configuration/
- Official plugins docs: https://pwnagotchi.ai/plugins/

### Jayofelony Fork (Recommended / Active)

- GitHub repo: https://github.com/jayofelony/pwnagotchi
- Releases/images: https://github.com/jayofelony/pwnagotchi/releases
- Wiki - Connecting: https://github.com/jayofelony/pwnagotchi/wiki/Step-2-Connecting
- Wiki - Configuration: https://github.com/jayofelony/pwnagotchi/wiki/Step-3-Configuration

### Community Hub

- Pwnagotchi.org: https://pwnagotchi.org/getting-started/index.html
- Third-party plugins: https://pwnagotchi.org/3rd-party-plugins/index.html
- Pwnagotchi Unofficial GitHub org: https://github.com/Pwnagotchi-Unofficial/

### Setup Guides

- [Noppitlabs Complete Beginner's Guide](https://www.noppitlabs.com/blogs/guides-projects/pwnagotchi-setup-guide)
- [Medium Practical Guide (ccoskun)](https://medium.com/@ccoskun742/pwnagotchi-setup-a-practical-guide-and-my-advanced-usage-notes-0c698bc07b28)
- [Simplicity Solved Ethical Guide](https://simplicitysolved.ca/2025/02/setting-up-a-pwnagotchi-a-fun-and-ethical-guide-to-wi-fi-security/)
- [StratoBuilds Build Guide + Home Assistant](https://stratobuilds.com/project/pwnagotchi/)
- [CyberSpaceManMike Tutorial Series](https://cyberspacemanmike.com/pwnagotchi-tutorial-series/)
- [DIY 2025 Full Build Video (YouTube)](https://www.youtube.com/watch?v=NA289GGBszI)
- [Joshua Morris Setup Gist](https://gist.github.com/JoshuaMorris/47d2c87bce931ca7e1ff753b010395fc)

### Troubleshooting

- [Biscuit Shop Troubleshooting Guide](https://biscuitshop.us/blogs/how-to-guides/troubleshoot-your-pwnagotchi)
- [Pi Forums: Pi Zero Blank Screen](https://forums.raspberrypi.com/viewtopic.php?t=182046)
- [Pi Forums: HDMI No Output on Zero W](https://forums.raspberrypi.com/viewtopic.php?t=204281)
- [Pi Forums: Zero 2 W HDMI Signal Issues](https://forums.raspberrypi.com/viewtopic.php?t=340140)
- [Pi Forums: Soldering Broke My Pi (Solved)](https://forums.raspberrypi.com/viewtopic.php?t=198453)
- [Pi Forums: GPIO Detect Bad Solder](https://forums.raspberrypi.com/viewtopic.php?t=213417)
- [Pi HDMI No Signal Fixes (Zbotic)](https://zbotic.in/raspberry-pi-hdmi-output-troubleshooting-fix-no-signal-issues/)
- [Raspberry Pi HDMI Fix Guide](https://howtoraspberrypi.com/raspberry-pi-hdmi-not-working/)
- [GitHub Issue: Waveshare V4 Not Starting](https://github.com/evilsocket/pwnagotchi/issues/1187)
- [GitHub Issue: Image Won't Boot Pi Zero 2 W](https://github.com/evilsocket/pwnagotchi/issues/1046)
- TOML validator: https://www.toml-lint.com

### Soldering Guides

- [DroneBot Workshop: Soldering Pi Zero GPIO](https://dronebotworkshop.com/soldering-raspberry-pi-zero-gpio/)
- [Pi Forums: Tips for Soldering GPIO](https://forums.raspberrypi.com/viewtopic.php?t=234057)
- [Pi Forums: Soldering GPIO on Pi Zero](https://forums.raspberrypi.com/viewtopic.php?t=184494)
- [Pi Forums: Multimeter Testing Solder Joints](https://forums.raspberrypi.com/viewtopic.php?t=132180)

### Handshake Cracking

- [How to Crack Pwnagotchi Handshakes](https://woliveiras.com/posts/how-to-crack-pwnagotchi-captured-handshakes/)
- [Pwnagetty Automation Tool](https://github.com/CyrisXD/Pwnagetty)
- [Check/Delete PCAP Plugin Guide](https://medium.com/@brntpcnr/pwnagotchi-check-delete-pcap-plugin-5314f6e28c21)

### Plugin Repositories

- [AlienMajik Plugin Collection](https://github.com/AlienMajik/pwnagotchi_plugins)
- [Kizeren Plugin Collection](https://github.com/kizeren/pwnagotchi-plugins)
- [Hannadiamond Plugins](https://github.com/hannadiamond/pwnagotchi-plugins)
- [wpa-2 Config Options Reference](https://github.com/wpa-2/Pwnagotchi-Plugins/blob/main/Config.toml_Options.md)
- [HDMI Viewer for Debugging](https://github.com/solution-libre/pwnagotchi-hdmi-viewer)

### Display Documentation

- [Waveshare 2.13" e-Paper HAT Wiki](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT)
- [Waveshare 2.13" Product Page](https://www.waveshare.com/2.13inch-e-paper-hat.htm)
- [Display System DeepWiki](https://deepwiki.com/jayofelony/pwnagotchi/5.1-display-system)
- [Hardware Requirements DeepWiki](https://deepwiki.com/jayofelony/pwnagotchi/1.2-hardware-requirements)

### Community

- Discord: https://discord.gg/PgaU3Vp (unofficial)
- Reddit: https://www.reddit.com/r/pwnagotchi/
- GitHub Discussions: https://github.com/jayofelony/pwnagotchi/discussions

---

## 9. Best-Fit Hardware from Your Inventory

### Recommended Build

| Component | Assignment | Why |
|-----------|-----------|-----|
| **Board** | CanaKit Raspberry Pi Zero 2 W (with 32GB SD from kit) | Only board that runs Pwnagotchi. Quad-core RP3A0, low power draw, PiSugar-compatible form factor |
| **Display** | Waveshare 2.13" E-Ink HAT V4 (250x122, SPI) | THE Pwnagotchi display. Shows AI face, handshake count, status. Zero power draw when static. Plugs directly onto GPIO header |
| **WiFi** | RT5370 WiFi USB Dongle | Pi Zero 2W onboard WiFi cannot do monitor mode injection. RT5370 (Ralink/MediaTek) is proven Pwnagotchi-compatible with monitor mode + packet injection on 2.4GHz |
| **Battery** | PiSugar S 1200mAh UPS | Purpose-built for Pi Zero, mounts underneath. ~3-4 hours portable operation. Note: PiSugar S lacks I2C -- no software battery monitoring |
| **Keyboard** | Rii K06 Mini Bluetooth Keyboard #1 | Dedicated to Pwnagotchi rig for headless SSH/terminal access during setup and troubleshooting |
| **Storage** | KOOTION 16GB Micro SD Card (Class 10) | 16GB is more than enough for Pwnagotchi image. Save 128GB cards for capture-heavy projects |
| **Adapter** | JSAUX Micro HDMI to HDMI Adapter #2 | For Pi Zero mini HDMI output during initial setup or debugging |
| **Testing** | Fluke 17B+ Multimeter | For testing GPIO solder joint continuity |

### Pinout Reference

The Pi Zero 2 W uses the standard Raspberry Pi 40-pin GPIO header. The Waveshare 2.13" e-ink HAT connects via SPI:

| Function | BCM GPIO | Physical Pin |
|----------|----------|-------------|
| SPI0 MOSI | GPIO 10 | Pin 19 |
| SPI0 MISO | GPIO 9 | Pin 21 |
| SPI0 SCLK | GPIO 11 | Pin 23 |
| SPI0 CE0 (Chip Select) | GPIO 8 | Pin 24 |
| Data/Command (DC) | GPIO 25 | Pin 22 |
| Reset (RST) | GPIO 17 | Pin 11 |
| Busy | GPIO 24 | Pin 18 |

**Interactive pinout:** [pinout.xyz](https://pinout.xyz/) | **Waveshare e-ink wiring:** [Waveshare Wiki](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual)

### Upgrade Recommendations

| Component | Upgrade To | Price | Improvement |
|-----------|-----------|-------|-------------|
| Battery | PiSugar 2 or PiSugar 3 | ~$30-40 | Adds I2C battery monitoring, software-readable charge level, RTC, longer runtime |
| WiFi | Alfa AWUS036ACH | ~$30 | Dual-band (2.4+5GHz), better range, higher injection speed |
| Board | Pi Zero 2 WH (pre-soldered headers) | ~$20 | Eliminates soldering requirement entirely |
