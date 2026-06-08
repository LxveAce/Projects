# Headless Marauder — Field Guide

What every tool does, how to drive the app, and **how to chain scanning + attacks together and
feed the results into other software**. For authorized testing only (see [Legal](#legal)).

---

## 1. The mental model

The ESP32 board runs the **Marauder firmware**. This app is a **remote control** for it over USB
serial — every button just sends a text command and shows what the board prints back. So the loop
is always the same:

```
        ┌─────────── recon ───────────┐         ┌──── act ────┐
  scan  →  list  →  (tables fill)  →  select  →  attack / sniff / capture  →  STOP
```

1. **Scan** to discover things (APs, stations, BLE).
2. **List** to pull the indexed results (the app auto-does this — tables fill themselves).
3. **Select** the target(s) from the picker.
4. **Act** — deauth, sniff a handshake, evil portal, etc.
5. **STOP** (scans and attacks run forever until you stop them).

> **Tooltips:** hover any command button to see what it does and whether it's an attack /
> runs-until-STOP. *Help → Command Reference* lists them all inside the app.

---

## 2. Using the app

- **Connect** — auto-detects the board (115200 baud). Green = connected.
- **Scan APs** → the **Access Points** tab fills automatically (Auto-list on).
- **STOP** → ends the scan.
- **Select APs / Select Stations** → tick targets in the picker (it builds the right `select -a 0,2,5`).
- Run an action (e.g. **Deauth (selected APs)**).
- **● Log** → record everything to a folder (see [§5](#5-data--logging)).
- **⚡ Flash Firmware** → detect chip, fetch firmware, flash.
- **Raw box** (bottom) → type any command the buttons don't cover.

Keyboard: `Ctrl+L` clear · `F5` refresh ports · `Ctrl+K` command box · `Ctrl+.` STOP · `Ctrl+U` update.

---

## 3. What each tool does

(Generated from the live command catalog. "runs until STOP" = continuous; "attack" = offensive.)

### WiFi · Scan

| Command | Sends | What it does |
|---|---|---|
| Scan APs | `scanap` | Discover nearby access points. _(runs until STOP)_ |
| Scan Stations | `scansta` | Find client stations (run scanap first). _(runs until STOP)_ |
| Scan All | `scanall` | Scan APs and stations together. _(runs until STOP)_ |
| Signal Monitor | `sigmon` | Live signal-strength monitor for a target. _(runs until STOP)_ |
| Packet Count | `packetcount` | Live packets-per-second counter. _(runs until STOP)_ |
| MAC Track | `mactrack` | Track signal strength of selected MAC(s) — proximity/"hot-cold". _(runs until STOP)_ |
| Wardrive | `wardrive` | GPS-tagged AP logging to SD (WiGLE CSV). _(runs until STOP)_ |

### WiFi · Sniff

| Command | Sends | What it does |
|---|---|---|
| Sniff Raw | `sniffraw` | Capture raw 802.11 frames → PCAP. _(runs until STOP)_ |
| Sniff Beacons | `sniffbeacon` | Capture beacon frames. _(runs until STOP)_ |
| Sniff Probes | `sniffprobe` | Capture probe requests (what devices are looking for). _(runs until STOP)_ |
| Sniff Deauth | `sniffdeauth` | Detect deauth frames (defensive — spot someone attacking). _(runs until STOP)_ |
| Sniff ESP | `sniffesp` | Detect ESP-based devices. _(runs until STOP)_ |
| Sniff Pwnagotchi | `sniffpwn` | Detect nearby Pwnagotchi units. _(runs until STOP)_ |
| Sniff PMKID | `sniffpmkid` | Capture PMKID/EAPOL handshakes → PCAP (crackable). _(runs until STOP)_ |

### WiFi · Attack

| Command | Sends | What it does |
|---|---|---|
| Deauth (selected APs) | `attack -t deauth` | Kick all clients off the selected AP(s). _(attack)_ |
| Deauth (selected clients) | `attack -t deauth -c` | Kick only the selected client(s). _(attack)_ |
| Beacon Spam (list) | `attack -t beacon -l` | Broadcast SSIDs from your list. _(attack)_ |
| Beacon Spam (random) | `attack -t beacon -r` | Broadcast random SSIDs. _(attack)_ |
| Beacon Spam (clone APs) | `attack -t beacon -a` | Clone scanned APs' names. _(attack)_ |
| Probe Flood | `attack -t probe` | Flood probe requests. _(attack)_ |
| Rickroll Beacon | `attack -t rickroll` | Beacon-spam lyrics as SSIDs. _(attack)_ |
| Bad Msg (clients) | `attack -t badmsg -c` | Malformed-frame attack on selected clients. _(attack)_ |
| Evil Portal | `evilportal -c start` | Captive-portal credential harvester (needs SD HTML). _(attack)_ |
| Karma | `karma` | Answer a device's probe to lure it to connect. _(attack)_ |

### Bluetooth

| Command | Sends | What it does |
|---|---|---|
| Sniff Bluetooth | `sniffbt` | Scan BLE devices; filter `airtag` / `flipper` / `flock`. _(runs until STOP)_ |
| BT Wardrive | `btwardrive` | GPS-tagged Bluetooth logging. _(runs until STOP)_ |
| Detect Skimmers | `sniffskim` | Scan for card-skimmer BLE signatures. _(runs until STOP)_ |
| BLE Spam | `blespam -t <type>` | Spam BLE pairing pop-ups (sourapple/applejuice/google/samsung/windows/flipper/all). _(attack)_ |
| Spoof AirTag | `spoofat` | Broadcast a cloned AirTag. _(attack)_ |
| Sour Apple / Swiftpair / Samsung / Spam All | `sourapple` … | Targeted BLE pop-up spam. _(attack)_ |

### Lists & Targets · SSID · Channel · GPS · Files · System

`list -a/-c/-s/-t` (show) · `select -a/-c/-s/-f` (choose) · `clearlist` · `info` ·
`ssid -a/-r` (manage spam SSID list) · `channel [-s n]` · `gpsdata`/`nmea`/`gps -g` ·
`ls`/`save`/`load` (SD) · `settings -s <name> enable/disable` (e.g. **SavePCAP**) · `led` · `reboot` · `stopscan`.

> The full list (with every flag) is in *Help → Command Reference* and in
> [`marauder_core/commands.py`](marauder_core/commands.py).

---

## 4. Combining tools into bigger operations

This is where it gets powerful — recon feeds targeting, targeting feeds attacks, and attacks feed
capture you finish in other software.

### A. Capture a WPA handshake, then crack it offline
The classic chain — deauth forces clients to re-handshake, which you capture, then crack on a PC.
1. `settings -s SavePCAP enable` (once) and insert a FAT32 SD card.
2. **Scan APs** → **Select APs** (your target).
3. **Sniff PMKID** (`sniffpmkid`) — or `sniffpmkid -d` to **deauth while sniffing** so clients
   reconnect and you grab the handshake faster.
4. **STOP**. The `.pcap` is on the SD card.
5. On a PC: open in **Wireshark**, or crack with **hashcat**/**aircrack-ng**:
   ```bash
   hcxpcapngtool -o hash.hc22000 capture.pcap     # convert
   hashcat -m 22000 hash.hc22000 wordlist.txt     # crack
   # or:  aircrack-ng -w wordlist.txt capture.pcap
   ```

### B. Recon → targeted deauth
1. **Scan All** (`scanall`) to map APs *and* their clients.
2. **Select Stations** → pick a specific client.
3. **Deauth (selected clients)** to knock just that device off (surgical, vs. broadcast).

### C. Evil Portal credential capture
1. Put your `index.html` (and optional `ap.config.txt`) on the SD card.
2. **Scan APs** → **Select APs** (the AP to impersonate).
3. **Evil Portal** (`evilportal -c start`) — enable EPDeauth in settings to deauth the real AP so
   clients land on yours. Captured credentials are written to the SD card.

### D. Wardriving → map it on WiGLE
1. Plug in GPS (the deck shares one GPS via `gpsd`).
2. **Wardrive** (`wardrive`) while moving — writes a **WiGLE-format CSV** (`wardrive_*.csv`) to SD.
3. Upload that CSV to **wigle.net** (counts toward your stats / builds a coverage map).

### E. Find who's following you (BLE)
1. **Sniff Bluetooth** `sniffbt -t airtag` to surface trackers; `-t flock` for Flock cameras.
2. **MAC Track** a suspicious MAC to gauge proximity as you move.
3. Correlate sightings over time/location with **Chasing Your Tail NG** on the Pi (see the cyberdeck).

### F. Probe-sniff → Karma lure
1. **Sniff Probes** to learn which SSIDs nearby devices are searching for.
2. Add those to your SSID list (`ssid -a -n <name>`).
3. **Karma** to answer those probes and lure devices to associate.

---

## 5. Data & logging (feed other software / the connected device)

Turn on **● Log** (or `--log [dir]`, default `~/marauder-logs`). It writes, live:

| File | Format | Use it for |
|---|---|---|
| `serial-<ts>.log` | raw text | `tail -f` it from another terminal/box; grep; replay |
| `latest.json` | JSON snapshot | poll it from a script/app for current APs+stations+status |
| `aps.csv` / `stations.csv` | CSV | import to a spreadsheet / pandas / your own dashboard |

Everything is atomic + append-only, so **another process or device can read it while the app runs**:
```bash
tail -f ~/marauder-logs/serial-*.log                 # live stream
watch -n1 'jq ".ap_count,.station_count" ~/marauder-logs/latest.json'
python3 -c "import json;print(json.load(open('~/marauder-logs/latest.json'.replace('~',__import__('os').path.expanduser('~'))))['aps'][:3])"
```
PCAP/Evil-Portal/wardrive output lives on the **board's SD card** (pull it over USB or `ls`/`save`).

---

## 6. Using it with the rest of your kit

- **The cyberdeck dashboard** — `marauder_core` is importable; the deck's
  [dashboard](https://github.com/LxveAce/Projects/tree/main/projects/14-cyberdeck/integrations/parts/dashboard)
  reuses it to show Marauder beside Kismet/Meshtastic/GPS.
- **Kismet** — run Kismet on the Pi for deep WiFi mapping while Marauder does active attacks; both
  can share the **same GPS** via `gpsd` (`localhost:2947`).
- **Wireshark / hashcat / aircrack-ng / hcxtools** — for PCAP analysis and cracking (chain A).
- **WiGLE** — wardrive CSVs (chain D).
- **Flipper Zero** — pair sub-GHz/RFID/NFC/IR work (Flipper) with WiFi/BLE (this) for full coverage.

---

## 7. Flashing (built in)

⚡ **Flash Firmware** → **Detect chip** → **Load release list** → pick a variant →
**Update app only** (existing board) or **Full flash** (blank board). Uses `esptool` with
`--flash_size detect`. Classic ESP32 Gold → a non-S3 variant (e.g. *old_hardware*); S3 → *MultiBoard S3*.

---

## Legal

For **authorized security testing only** — networks/devices you own or have **written permission**
to test. Deauth, evil-portal, beacon/BLE spam, and karma can be illegal against others (US CFAA,
FCC rules, and equivalents). Many modern networks ignore deauth (802.11w/PMF). You are responsible
for your use. See the firmware's own [legal notes](https://github.com/justcallmekoko/ESP32Marauder).
