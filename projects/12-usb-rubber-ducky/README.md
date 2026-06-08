# USB Rubber Ducky

Hak5's keystroke injection tool — hardware, DuckyScript 3.0, payloads, DIY alternatives, and defenses.

---

## Table of Contents

1. [Overview: Keystroke Injection](#1-overview-keystroke-injection)
2. [Hardware Specifications](#2-hardware-specifications)
3. [DuckyScript 3.0 Language Guide](#3-duckyscript-30-language-guide)
4. [Setup from Unboxing](#4-setup-from-unboxing)
5. [Best Payloads](#5-best-payloads)
6. [DIY Alternatives](#6-diy-alternatives)
7. [Defense and Detection](#7-defense-and-detection)
8. [Legal Considerations](#8-legal-considerations)
9. [Pricing and Where to Buy](#9-pricing-and-where-to-buy)
10. [Key Resources](#key-resources)

---

## 1. Overview: Keystroke Injection

The USB Rubber Ducky is a keystroke injection attack platform created by Hak5. It looks like an ordinary USB flash drive but the computer recognizes it as a USB Human Interface Device (HID) keyboard. When plugged in, it executes pre-programmed keystrokes at speeds exceeding 1,000 words per minute -- far faster than any human typist.

### How It Works at the USB Protocol Level

- Every computer inherently trusts keyboards. The USB HID specification defines keyboards as a trusted device class.
- When the Rubber Ducky is inserted, the operating system enumerates it as a generic keyboard -- not as a storage device, not as a suspicious peripheral.
- Because it IS a keyboard to the OS, no driver installation is needed, no user approval is prompted, and no antivirus triggers.
- The device then "types" a pre-compiled payload (`inject.bin`) at machine speed, executing commands through the OS shell (PowerShell, Terminal, CMD, etc.).

### Core Attack Concept

The Rubber Ducky exploits the fundamental trust relationship between a computer and its input devices. It does not exploit a software vulnerability -- it exploits human and system trust in USB keyboards.

### Use Cases (Authorized)

- Penetration testing and red team engagements
- Security awareness training and demonstrations
- IT automation and repetitive task scripting
- Physical security audits

---

## 2. Hardware Specifications

### Mark I (2011 -- Original)

| Spec | Detail |
|------|--------|
| Processor | 60 MHz CPU |
| Storage | MicroSD card slot (user-supplied) |
| USB | USB-A only |
| Language | DuckyScript 1.0 (interpreted) |
| LED | Single color |
| Form factor | USB flash drive shell |

### Mark II (2022 -- Current Generation)

| Spec | Detail |
|------|--------|
| Processor | Upgraded (faster than 60 MHz; exact spec not publicly disclosed by Hak5) |
| Storage | Onboard (larger than Mark I; no external SD needed for payload) |
| USB | USB-C and USB-A (via included adapter), attacks desktops and mobile |
| Language | DuckyScript 3.0 (compiled, structured programming language) |
| LED | Bi-color LED for status feedback |
| Form factor | Compact USB drive enclosure |
| Target OS | Windows, macOS, Linux, ChromeOS, Android, iOS (limited) |
| Attack modes | HID-only mode, HID + Storage combo attack mode |

### Mark IV (Latest)

The latest iteration available in the Hak5 shop, priced at $99.99. Features dual USB-C/USB-A connectivity and full DuckyScript 3.0 support.

### Arming Mode

When first plugged into your setup computer, the device appears as a mass storage device labeled "DUCKY." This is arming mode, where you place the compiled `inject.bin` file. On the target machine, it enumerates as a keyboard only.

---

## 3. DuckyScript 3.0 Language Guide

DuckyScript 3.0 (released 2022) is a fully structured programming language, backward-compatible with DuckyScript 1.0. Payloads are compiled into `inject.bin` binary files using PayloadStudio.

### 3.1 Basic Commands

```ducky
REM This is a comment -- ignored by the compiler
REM_BLOCK
  Multi-line comments go here
END_REM

DELAY 1000                   REM Pause for 1000 milliseconds
DEFAULT_DELAY 100            REM Set default delay between every command
STRINGLN Hello, World!       REM Types text and presses ENTER
STRING Hello, World!         REM Types text without pressing ENTER
```

### 3.2 Key Commands

```ducky
ENTER                        REM Press Enter key
GUI r                        REM Windows key + R (Run dialog)
GUI                          REM Windows/Cmd key alone
ALT F4                       REM Alt + F4
CTRL c                       REM Ctrl + C
SHIFT TAB                    REM Shift + Tab
CTRL ALT DELETE              REM Ctrl + Alt + Delete
TAB                          REM Tab key
ESCAPE                       REM Escape key
UPARROW / DOWNARROW          REM Arrow keys
LEFTARROW / RIGHTARROW
SPACE                        REM Spacebar
BACKSPACE                    REM Backspace
DELETE                       REM Delete key
HOME / END
PAGEUP / PAGEDOWN
PRINTSCREEN
CAPSLOCK / NUMLOCK / SCROLLLOCK
F1 through F12               REM Function keys
```

### 3.3 Constants and Variables

```ducky
DEFINE #WAIT 2000            REM Compile-time constant (find-and-replace)
DEFINE #TARGET_URL https://example.com

VAR $counter = 0             REM Runtime variable (unsigned int, 0-65535)
VAR $flag = TRUE             REM Boolean
$counter = ($counter + 1)    REM Assignment
```

### 3.4 Operators

| Operator | Meaning |
|----------|---------|
| `=` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |
| `&&` | Logical AND |
| `\|\|` | Logical OR |

### 3.5 Conditional Statements

```ducky
IF ($counter > 10) THEN
    STRING Counter exceeded 10
    ENTER
ELSE IF ($counter > 5) THEN
    STRING Counter exceeded 5
    ENTER
ELSE
    STRING Counter is 5 or less
    ENTER
END_IF
```

### 3.6 Loops

```ducky
REM WHILE loop
VAR $i = 10
WHILE ($i > 0)
    STRING .
    $i = ($i - 1)
    DELAY 500
END_WHILE

REM Infinite loop (use with caution)
WHILE TRUE
    LED_G
    DELAY 1000
END_WHILE
```

### 3.7 Functions

```ducky
FUNCTION open_powershell()
    GUI r
    DELAY 500
    STRING powershell
    ENTER
    DELAY 1000
END_FUNCTION

REM Call the function
open_powershell()
STRING Get-Process
ENTER
```

### 3.8 Advanced Features

**LED Control:**

```ducky
LED_R                        REM Red LED
LED_G                        REM Green LED
LED_OFF                      REM LED off
```

**OS Detection:** DuckyScript 3.0 can detect the target operating system and branch payload logic accordingly.

**Keystroke Reflection:** Detects the keyboard layout of the target system to ensure correct character injection regardless of locale.

**Randomization and Jitter:** Built-in randomization for evasion; adds variable delays to mimic human typing patterns.

**HID + Storage Attack Mode:** The Ducky can simultaneously present as a keyboard AND a mass storage device, enabling file exfiltration directly to the device's onboard storage.

**Extensions:** Reusable code blocks that can be imported into any payload -- think of them as libraries or snippets.

### 3.9 Payload Header Convention

Every payload should begin with metadata comments:

```ducky
REM Title: WiFi Password Grabber
REM Author: YourName
REM Description: Extracts saved WiFi passwords
REM Target: Windows 10/11
REM Version: 1.0
REM Category: Exfiltration
```

### 3.10 Development Environment

**PayloadStudio** -- Official Hak5 web-based IDE:

- Syntax highlighting and autocomplete
- Live error checking
- DuckyScript encoder (compiles `.txt` to `inject.bin`)
- Repository synchronization with GitHub
- Free Community Edition available; Pro version for advanced features
- URL: payloadstudio.hak5.org

---

## 4. Setup from Unboxing

### Step-by-Step

1. **Unbox:** The package includes the USB Rubber Ducky device, a USB-A adapter (if USB-C model), and quick-start documentation.

2. **Connect to your computer:** Plug the Ducky into your setup PC. It will appear as a removable drive labeled "DUCKY" -- this is **arming mode**.

3. **Write your payload:** Create a DuckyScript `.txt` file (e.g., `payload.txt`) using PayloadStudio or any text editor.

4. **Compile the payload:** Use PayloadStudio (payloadstudio.hak5.org) to encode your `.txt` file into `inject.bin`. This is the compiled binary the Ducky executes.

5. **Load the payload:** Copy the `inject.bin` file to the root of the DUCKY drive, replacing any existing `inject.bin`.

6. **Safely eject** the Ducky from your setup computer.

7. **Deploy:** Plug the Ducky into the target machine. It will enumerate as a keyboard and immediately begin executing the payload.

8. **Observe the LED:** The bi-color LED provides status feedback during payload execution.

### Your First Payload (Hello World)

```ducky
REM My first payload
DELAY 2000
GUI r
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRINGLN Hello from USB Rubber Ducky!
```

### Troubleshooting

- **Payload not executing:** Ensure the file is named exactly `inject.bin` (not `inject.bin.txt`).
- **Wrong characters typed:** Check keyboard language settings; use keystroke reflection or the correct language file.
- **Too fast for the OS:** Increase `DELAY` values. Initial enumeration needs 1500-2500ms. Inter-action delays of 500-1200ms reflect realistic OS responsiveness.
- **Arming mode not appearing:** Hold the button on the device while inserting to force arming mode.

---

## 5. Best Payloads

The official Hak5 payload repository ([github.com/hak5/usbrubberducky-payloads](https://github.com/hak5/usbrubberducky-payloads)) organizes payloads into categories. All payloads below are for **educational and authorized testing purposes only**.

### 5.1 Reconnaissance

- **System info grabber:** Opens PowerShell, runs `systeminfo`, `ipconfig`, `whoami`, and exports results.
- **Network scanner:** Enumerates network adapters, ARP tables, and routing info.

### 5.2 Exfiltration

- **WiFi password harvester:** Runs `netsh wlan show profiles` and extracts saved WiFi passwords to a file, then exfiltrates via HID+Storage mode.
- **Browser credential dump:** Extracts saved passwords from Chrome/Edge credential stores.
- **File crawler:** Searches all drives for specific file types (.docx, .xlsx, .pdf) and compresses them for exfiltration.

### 5.3 Remote Access

- **Reverse shell:** Opens PowerShell, downloads and executes a reverse shell connecting back to an attacker-controlled server.
- **Persistent backdoor:** Creates a scheduled task or registry run key for persistence.

### 5.4 Security Manipulation

- **Disable Windows Defender:** Navigates Windows Security UI to turn off real-time protection.
- **Firewall disable:** Uses `netsh advfirewall set allprofiles state off`.

### 5.5 Phishing / Social Engineering

- **Fake Windows Update screen:** Launches a full-screen browser window mimicking a Windows Update to keep users away while the payload executes in the background.
- **Credential harvester:** Opens a fake login prompt and captures typed credentials.

### 5.6 Cross-Platform

- **macOS Terminal payload:** Uses Cmd+Space (Spotlight) to open Terminal and execute commands.
- **Linux payload:** Uses Ctrl+Alt+T to open terminal on most distros.

> **Note:** Destructive payloads (wiping data, bricking systems) are explicitly rejected from the official Hak5 repository. All payloads should be used only with explicit authorization.

---

## 6. DIY Alternatives

### 6.1 Arduino Leonardo / Pro Micro (ATmega32u4) -- ~$5-15

**Why it works:** The ATmega32u4 has native USB, allowing it to appear as an HID keyboard without any additional chips. Boards using a separate USB-to-serial chip (like the Uno's ATmega328P + CH340) cannot do this.

**Setup:**

1. Install Arduino IDE
2. Select board: "Arduino Leonardo" or "SparkFun Pro Micro"
3. Use the built-in `Keyboard.h` library
4. Write sketch using `Keyboard.press()`, `Keyboard.release()`, `Keyboard.println()`
5. Upload, unplug, replug into target

**Example payload (Windows -- open Notepad):**

```cpp
#include <Keyboard.h>

void setup() {
  delay(2000);
  Keyboard.begin();
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  Keyboard.releaseAll();
  delay(500);
  Keyboard.println("notepad");
  delay(1000);
  Keyboard.println("Hello from Arduino!");
  Keyboard.end();
}

void loop() {}
```

**Pros:** Proven, massive community, cheap, easy setup.

**Cons:** Payload hardcoded in firmware (must reflash to change), no onboard storage, 6KB limited flash on Pro Micro, no wireless capability.

---

### 6.2 Digispark ATtiny85 -- ~$1.50-3

The cheapest option. A tiny board with a direct USB plug.

**Setup:**

1. Install Arduino IDE + Digistump board package (add URL to Board Manager: `http://digistump.com/package_digistump_index.json`)
2. Select board: "Digispark (Default - 16MHz)"
3. Use `DigiKeyboard.h` library
4. Write payload, click upload, plug in board when prompted (within 60 seconds)

**Example payload:**

```cpp
#include "DigiKeyboard.h"

void setup() {}

void loop() {
  DigiKeyboard.delay(2000);
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);
  DigiKeyboard.println("notepad");
  DigiKeyboard.delay(1000);
  DigiKeyboard.println("Hello from Digispark!");
  for(;;) {}  // Stop loop
}
```

**Pros:** Absurdly cheap (~$1.50 from AliExpress), tiny form factor, direct USB plug.

**Cons:** Only 6,012 bytes for code (extremely limiting), unreliable timing, no native USB (uses software V-USB which causes enumeration issues on some systems), no storage, limited keystroke capabilities.

**Translation tool:** `duck2spark` converts standard DuckyScript to Digispark-compatible Arduino code.

---

### 6.3 ESP32-S2 / ESP32-S3 -- ~$5-10

The most feature-rich DIY option. Native USB HID support + built-in WiFi.

**Key project: [SuperWiFiDuck](https://github.com/wasdwasd0105/SuperWiFiDuck)**

- Uses native USB function of ESP32-S2/S3
- Runs on a single default module under $10
- No special hardware modifications required
- Compatible with standard DuckyScript syntax
- WiFi-enabled: connect via WiFi to manage, edit, and deploy payloads through a web interface -- no need to physically reflash

**Setup:**

1. Flash SuperWiFiDuck firmware to an ESP32-S2/S3 development board
2. Connect to the device's WiFi access point
3. Open the web interface in a browser
4. Write/upload DuckyScript payloads
5. Execute wirelessly

**Other notable projects:**

- **[ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder/wiki/badusb):** Multi-tool firmware with BadUSB capabilities
- **Bruce firmware:** Includes HID emulation and BadUSB features
- **HackyPi 2.0:** ESP32-S3-based commercial tool with AI-assisted control and automatic OS detection

**Pros:** WiFi payload management (no reflash needed), native USB, cheap, powerful processor, large storage, can run complex payloads.

**Cons:** Larger form factor than a USB stick, more complex firmware setup, less "plug and play" than Hak5.

---

### 6.4 Raspberry Pi Pico (RP2040) -- ~$4-6

Rapidly becoming the most popular DIY Rubber Ducky platform.

**Key project: [pico-ducky](https://github.com/dbisu/pico-ducky)**

- Uses CircuitPython for easy payload scripting
- Directly compatible with DuckyScript syntax

**Setup:**

1. Download CircuitPython UF2 firmware for Pico from circuitpython.org
2. Hold BOOTSEL button, plug Pico into PC, release -- appears as RPI-RP2 drive
3. Copy the CircuitPython `.uf2` file to the drive (it will reboot as CIRCUITPY)
4. Download `adafruit_hid` library from the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases) and copy to `/lib/` on the Pico
5. Copy the pico-ducky code files to the Pico
6. Write your payload in DuckyScript as `payload.dd` in the root directory
7. **Setup mode:** Connect GP0 to GND (pin 1 to pin 3) with a jumper wire to prevent the payload from executing on your own machine while editing
8. Remove the jumper wire and replug to execute

**Pico W variant:** Adds WiFi, enabling wireless payload management similar to the ESP32 approach.

**Pros:** Extremely cheap ($4-6), powerful dual-core ARM processor, 2MB flash, large community, native USB, direct DuckyScript compatibility, CircuitPython makes payload changes easy (just edit a text file, no compilation).

**Cons:** Larger than a USB stick, no enclosure (you can 3D print one), requires jumper wire for setup mode.

---

### DIY Comparison Table

| Feature | Hak5 Ducky | Arduino Leo/Pro Micro | Digispark | ESP32-S2/S3 | RPi Pico |
|---------|------------|----------------------|-----------|-------------|----------|
| **Price** | $99.99 | $5-15 | $1.50-3 | $5-10 | $4-6 |
| **Native USB** | Yes | Yes | No (V-USB) | Yes | Yes |
| **WiFi** | No | No | No | Yes | Pico W only |
| **DuckyScript** | Native | Needs conversion | Needs conversion | SuperWiFiDuck | pico-ducky |
| **Payload change** | Copy inject.bin | Reflash firmware | Reflash firmware | WiFi web UI | Edit text file |
| **Storage** | Onboard | None | ~6KB code | MB-level flash | 2MB flash |
| **Form factor** | USB stick | Board | Tiny USB | Dev board | Dev board |
| **Stealth** | High | Medium | Medium | Low | Low |
| **OS Detection** | Yes | No | No | Some firmwares | No |
| **Difficulty** | Beginner | Beginner | Beginner | Intermediate | Beginner |

---

## 7. Defense and Detection

### 7.1 Why Traditional Defenses Fail

- **Antivirus does not detect it.** The Rubber Ducky sends keystrokes, not malware files. No malicious executable is transferred from the device.
- **It uses legitimate system tools.** Payloads typically invoke PowerShell, CMD, Bash, or Terminal -- all trusted system binaries.
- **The OS trusts keyboards implicitly.** There is no "are you sure you want to use this keyboard?" prompt.

### 7.2 Effective Defenses

**USB Device Control Policies:**

- Implement device whitelisting: only allow keyboards with approved Vendor IDs (VIDs) and Product IDs (PIDs).
- Block "extra keyboards" -- if a workstation already has a keyboard, deny additional HID keyboard devices.
- Use Group Policy (Windows) to control USB device access.
- Physical USB port locks/blockers for kiosks, servers, and public workstations.

**Endpoint Detection and Response (EDR):**

- Deploy EDR solutions that monitor for abnormal command sequences (e.g., PowerShell launching within 2 seconds of a new HID device appearing).
- Behavioral analysis: flag when a "keyboard" types 500+ characters in under a second.
- Monitor for rapid succession of GUI+R, followed by command-line invocation.

**Application Whitelisting:**

- Only allow approved applications to execute.
- If a workstation does not need PowerShell, block it entirely.
- If PowerShell is required, enable Constrained Language Mode.
- Use Windows Defender Application Control (WDAC) or AppLocker.

**Network-Level Defenses:**

- Block outbound connections from workstations to unknown IPs (prevents reverse shells).
- DNS filtering to block known C2 domains.
- Monitor for data exfiltration patterns.

**Physical Security:**

- Security awareness training: teach employees never to plug in unknown USB devices.
- USB port locks/epoxy on sensitive systems.
- Implement clean desk policies.
- Use USB data blockers (charge-only cables) where appropriate.

**Specific Tools:**

- **USBGuard (Linux):** Allows/blocks USB devices based on policy rules.
- **Microsoft Defender for Endpoint:** Includes device control capabilities.
- **ThreatLocker:** Application whitelisting with USB device control.
- **Netwrix:** BadUSB attack prevention and monitoring.

### 7.3 Detection Indicators

- New HID keyboard device enumerated in Windows Event Log (Event ID 6416 in Security log).
- PowerShell or CMD launched within seconds of USB insertion.
- Extremely rapid keystroke input (no human types 1000 WPM).
- Unusual processes spawned from explorer.exe or shell processes.

---

## 8. Legal Considerations

### 8.1 Legality of Ownership

**The device itself is legal to own and purchase.** It is marketed and sold as a penetration testing and IT automation tool. Hak5 operates openly, sells through their website and Amazon, and the device has appeared in mainstream media (Mr. Robot TV show).

### 8.2 Legality of Use

**Using it on any system without explicit written authorization is a criminal offense.**

| Jurisdiction | Law | Notes |
|-------------|-----|-------|
| United States | Computer Fraud and Abuse Act (CFAA), 18 U.S.C. 1030 | Unauthorized access via physical insertion is a federal crime. Penalties: fines and up to 10+ years imprisonment. |
| United Kingdom | Computer Misuse Act 1990 | Unauthorized access and modification offenses. |
| Germany | StGB 202c | Preparation of data espionage. |
| Brazil | Lei 12.737/2012 (Carolina Dieckmann Law) | Computer invasion crimes. |
| European Union | Directive 2013/40/EU | Attacks against information systems. |

### 8.3 Requirements for Legal Use

1. **Written authorization** from the system/network owner -- must be specific, scoped, and revocable.
2. **Defined scope:** which systems, time windows, data types, and escalation paths.
3. **Rules of engagement** document reviewed by legal counsel.
4. **Logging and reporting:** every keystroke sequence must be auditable and disclosed in the post-engagement report.
5. **Professional standards:** Penetration testers should hold relevant certifications (OSCP, CEH, GPEN, PNPT).
6. **Data handling:** Any data accessed during testing must be handled according to the engagement agreement and applicable data protection laws (GDPR, CCPA, etc.).
7. **Insurance:** Professional liability / E&O insurance is recommended for pentest firms.

### 8.4 Gray Areas

- **Using on your own personal devices:** Legal.
- **Using on company devices you administer (without written policy):** Risky -- get written authorization even for your own IT infrastructure.
- **Security demonstrations at conferences:** Legal if using your own equipment.
- **Dropping Duckies in a parking lot (social engineering test):** Only legal if part of an authorized engagement with a signed scope.

---

## 9. Pricing and Where to Buy

### Official Hak5 Products

| Product | Price | Notes |
|---------|-------|-------|
| USB Rubber Ducky (current gen) | **$99.99** | From shop.hak5.org |
| USB Rubber Ducky R (restricted/B2B) | Varies | Enterprise/bulk pricing |
| USB Rubber Ducky Pocket Guide | ~$14.99 | Physical reference booklet |
| PayloadStudio Pro | Subscription | Advanced IDE features |

### Where to Buy

- **Official:** [shop.hak5.org](https://shop.hak5.org/products/usb-rubber-ducky) -- recommended, includes warranty and support
- **Amazon:** Search "USB Rubber Ducky Hak5" -- available but verify seller authenticity
- **Hacker Warehouse:** [hackerwarehouse.com](https://hackerwarehouse.com/product/usb-rubber-ducky/) -- authorized reseller
- **eBay:** Available but beware counterfeits
- **International:** Various regional resellers

### DIY Alternative Costs

| Board | Approx. Cost | Source |
|-------|-------------|--------|
| Digispark ATtiny85 | $1.50-3 | AliExpress, Amazon |
| Raspberry Pi Pico | $4-6 | Official distributors, Adafruit, SparkFun |
| ESP32-S2 DevKit | $5-10 | AliExpress, Amazon, Mouser |
| Arduino Pro Micro | $5-15 | SparkFun, Amazon, AliExpress |
| Arduino Leonardo | $10-25 | Official Arduino store, Amazon |

---

## Key Resources

### Official Hak5

- [Official Documentation](https://docs.hak5.org/hak5-usb-rubber-ducky/usb-rubber-ducky-by-hak5/)
- [Payload Repository](https://github.com/hak5/usbrubberducky-payloads)
- [PayloadStudio IDE](https://payloadstudio.hak5.org)
- [PayloadHub](https://payloadhub.com/blogs/payloads/tagged/usb-rubber-ducky)
- [DuckyScript Quick Reference](https://docs.hak5.org/hak5-usb-rubber-ducky/duckyscript-quick-reference/)
- [DuckyScript Basics](https://docs.hak5.org/hak5-usb-rubber-ducky/docs/ducky-script-basics/)
- [Advanced Features](https://docs.hak5.org/hak5-usb-rubber-ducky/docs/advanced-features/)
- [Unboxing / Quack-Start Guide](https://docs.hak5.org/hak5-usb-rubber-ducky/unboxing-quack-start-guide/)

---

## 11. Best-Fit Hardware from Your Inventory

### Status: Partially Ready (DIY Route Available)

The official Hak5 USB Rubber Ducky (~$100) is not yet purchased. For a DIY alternative, you need an ESP32 board with native USB HID support.

### DIY Option from Your Inventory

| Component | Notes |
|-----------|-------|
| **Waveshare ESP32-C5 WiFi 6 Dev Board #1** | Has USB but its RISC-V architecture is better reserved for WiFi 6 research |
| **Generic ESP32-WROOM-32** | Does NOT support USB HID natively (uses USB-to-serial bridge chip). Not suitable for Rubber Ducky |

### Recommendation

Purchase a dedicated **ESP32-S2 Mini** (~$5-8) which has native USB OTG/HID support and is the go-to DIY Rubber Ducky platform. Or get the official Hak5 USB Rubber Ducky ($100) for the most polished experience with DuckyScript 3.0 support.

| Buy Option | Price | Capability |
|-----------|-------|-----------|
| ESP32-S2 Mini (DIY) | ~$5-8 | Native USB HID, WiFi payload delivery, open-source |
| Raspberry Pi Pico (DIY) | ~$4-6 | USB HID via CircuitPython, large community |
| Hak5 USB Rubber Ducky (official) | ~$100 | Best DuckyScript 3.0 support, most polished |

### DIY Projects

- [pico-ducky (Raspberry Pi Pico)](https://github.com/dbisu/pico-ducky)
- [SuperWiFiDuck (ESP32-S2/S3)](https://github.com/wasdwasd0105/SuperWiFiDuck)
- [EvilDuck (Arduino Micro)](https://github.com/cifertech/evilduck)
- [Digispark Payloads (ATtiny85)](https://github.com/MTK911/Attiny85)
- [DIY Build Guide (TheLinuxCode)](https://thelinuxcode.com/how-to-make-a-usb-rubber-ducky-at-home-educational-build-guide/)

### Defense and Security

- [ThreatLocker -- USB Rubber Ducky Attacks Explained](https://www.threatlocker.com/blog/usb-rubber-ducky-attacks-explained-keystroke-injection-evasion-and-defense)
- [Netwrix -- BadUSB Attack Prevention](https://netwrix.com/en/resources/blog/badusb-attack-prevention/)
- [Keepnet Labs -- USB Rubber Ducky Attack Tool (Legal Analysis)](https://keepnetlabs.com/blog/usb-rubber-ducky-attack-tool)
