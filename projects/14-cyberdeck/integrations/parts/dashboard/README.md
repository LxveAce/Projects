# Dashboard — Flask + SocketIO Kiosk (Cyberdeck Part)

> **Part of:** [Project 14 — The Cyberdeck](../../../README.md) · **Integrations index:** [integrations/](../../README.md)
> **Full reference (all options):** [deck README §11 Software Integration](../../../README.md)
> **Deck role:** The central hub UI — aggregates every board onto the 7" screen
> **Status:** Designed, not yet coded — scaffold + protocol reference below make it buildable

---

## The Decision

| Question | Choice for the deck |
|----------|---------------------|
| **Software** | Custom **Python Flask + SocketIO** web app on the Pi 5 |
| **Display** | 7" DSI in **Chromium kiosk** mode (`chromium-browser --kiosk http://localhost:5000`) |
| **Layout** | **800x480**, 5 tabs: Overview / WiFi-Marauder / BLE-Flock / Mesh / Sys — status cards |
| **Data sources** | ESP32 serial (115200), Kismet REST (localhost:2501), Meshtastic SDK, `gpsd` |
| **Real-time** | WebSocket push (SocketIO) — every panel updates live |
| **Auto-start** | systemd services, dependency order: `gpsd` → `kismet` → `dashboard` → Chromium kiosk |

> **Why Flask + SocketIO over Grafana or tmux:** one Python codebase handles serial I/O *and*
> serves the UI; WebSocket push updates all device panels instantly; HTML/CSS gives full control
> over the 800x480 touch layout (Leaflet maps, Chart.js, command buttons back to the ESP32s);
> lightweight — no Electron bloat. **Grafana+InfluxDB and tmux split-panes are NOT chosen.**

> **Honest status:** the dashboard is *designed, not yet coded*. This guide gives the install,
> the scaffold, and the exact serial/REST protocol reference so it can be built start-to-finish.

---

## What You Need (from the repo inventory)

- Raspberry Pi 5 8GB — the [pi5-brain](../pi5-brain/), running Kali (always on)
- Hosyond 7" DSI Touchscreen — the kiosk display, see [displays](../displays/)
- VK-162 USB GPS via `gpsd` — see [gps](../gps/)
- Every feeding board, over USB serial / REST:
  - [ESP32 Marauder](../../01-esp32-marauder/) (Gold #1) — `/dev/ttyUSBx`, 115200
  - [Flock + Drone](../../06-flock-drone-detection/) — Marauder flock sniff + WROOM JSON
  - [BLE Detection](../../08-ble-detection/) (Gold #3) — ASCII serial
  - [Meshtastic](../../04-meshtastic/) (Heltec V3) — `meshtastic-python`
  - [Kismet Wardriving](../../07-kismet-wardriving/) — REST at `localhost:2501`
- Full part list / links: [INVENTORY.md](../../../../../INVENTORY.md)

No new hardware — the dashboard is software glue over boards already in the deck.

---

## Get It Running

### 1. Install the dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv chromium-browser
python3 -m venv ~/deck-dash/venv
source ~/deck-dash/venv/bin/activate
pip install flask flask-socketio pyserial meshtastic kismet-rest gps3
```

`gpsd` itself is set up in the [gps](../gps/) guide (`sudo apt install gpsd gpsd-clients`).

### 2. Scaffold the Flask / SocketIO app

```
~/deck-dash/
├── app.py            # Flask + SocketIO server, background reader threads
├── sources/
│   ├── marauder.py   # pyserial reader for Gold #1 (WiFi/Flock)
│   ├── ble.py        # pyserial reader for Gold #3 (BLE)
│   ├── drone.py      # pyserial reader for WROOM-32 (JSON RemoteID)
│   ├── mesh.py       # meshtastic-python interface
│   ├── kismet.py     # kismet-rest client
│   └── gps.py        # gps3 / gpsd client
├── templates/
│   └── index.html    # 800x480, 5 tabs, status cards
└── static/           # Leaflet.js, Chart.js, CSS
```

Server skeleton (`app.py`):
```python
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

def emit_update(tab, payload):
    socketio.emit(tab, payload)   # e.g. "marauder", "ble", "mesh", "kismet", "sys"

if __name__ == "__main__":
    # start_background_threads()  # one reader per source (step 3)
    socketio.run(app, host="0.0.0.0", port=5000)
```

The browser subscribes to each event name and repaints the matching status card. The 5 tabs map
to the layout: **Overview** (all status cards), **WiFi/Marauder**, **BLE/Flock**, **Mesh**, **Sys**.

### 3. Wire each data source

Each source runs in its own background thread and calls `emit_update(...)`. All ESP32 links are
**115200 baud**. Use this protocol reference (from the deck's serial-protocol table):

| Source | Transport | Read / command reference |
|--------|-----------|--------------------------|
| **Marauder** (Gold #1) | `pyserial` ASCII CLI | send `scanap`, `scansta`, `attack -t deauth`, `stopscan`; parse AP/station lines |
| **Flock** | via Marauder | send `sniffbt -t flock` (Flock OUI), `Flock Wardrive` for GPS-tagged logging |
| **BLE Scanner** (Gold #3) | `pyserial` ASCII | parse MAC, RSSI, device name, manufacturer data per line |
| **Drone RemoteID** (WROOM) | `pyserial` JSON | parse `{"mac":...,"rssi":-45,"drone_lat":...,"drone_long":...,"altitude":120}` |
| **Meshtastic** (Heltec) | `meshtastic-python` (protobuf) | `interface.sendText()`, `showNodes()`, `getMyNodeInfo()` |
| **Kismet** | `kismet-rest` REST | client against `http://localhost:2501` — AP/device counts |
| **GPS** | `gps3` → `gpsd` | connect `localhost:2947` for live lat/lon, feed Flock/BLE timestamps |
| **System** | `vcgencmd` / `psutil` | CPU temp, RAM, battery — the Sys tab |

Open the serial ports read-only where possible and reconnect on unplug, so a powered-off board
(its [toggle switch](../../../README.md) off) degrades one card instead of crashing the app.

### 4. Kiosk + systemd autostart

Create one unit per stage so they start in dependency order. Example dashboard unit
(`/etc/systemd/system/deck-dashboard.service`):
```ini
[Unit]
Description=Cyberdeck Flask Dashboard
After=gpsd.service kismet.service
Wants=gpsd.service kismet.service

[Service]
ExecStart=/home/kali/deck-dash/venv/bin/python /home/kali/deck-dash/app.py
Restart=on-failure
User=kali

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now gpsd kismet deck-dashboard
```

Launch Chromium kiosk on boot once the dashboard is up (desktop autostart, e.g.
`~/.config/lxsession/LXDE-pi/autostart` or a user systemd unit):
```bash
chromium-browser --kiosk --noerrdialogs --disable-infobars http://localhost:5000
```

Boot sequence overall: `gpsd` (GPS feed) → `kismet` (if GPS lock) → ESP32 serial readers +
Meshtastic connect → `deck-dashboard` → Chromium kiosk on the 7" DSI.

### 5. Verify

```bash
source ~/deck-dash/venv/bin/activate
python ~/deck-dash/app.py            # then browse to http://localhost:5000 from the Pi
systemctl status deck-dashboard      # should be active (running)
curl -s http://localhost:5000 | head # Flask serving the tabbed page
```
Confirm each card populates: power on the boards via their toggles and watch the Overview tab —
Marauder AP count, BLE device count, mesh node count, Kismet AP count, GPS fix, and Sys vitals
should all go live. A board left off should show a dead card, not a stack trace.

---

## Cyberdeck Compatibility Notes

- **It's the hub every board feeds.** This part has no radio of its own — it aggregates the
  others. Each feeding board's own guide documents its serial/REST output; this guide consumes it:
  [Marauder](../../01-esp32-marauder/), [Flock/Drone](../../06-flock-drone-detection/),
  [BLE](../../08-ble-detection/), [Meshtastic](../../04-meshtastic/), [Kismet](../../07-kismet-wardriving/).
- **Runs on the brain.** Lives on the [pi5-brain](../pi5-brain/) (always-on, USB-C PD), so it's up
  whenever the deck is. ESP32 boards reach it as `/dev/ttyUSBx` through the powered hub.
- **Shares one GPS.** Pulls coordinates from the single [gps](../gps/) `gpsd` daemon
  (`localhost:2947`) — same feed Kismet and Meshtastic use; no second GPS.
- **Owns the 7" screen.** Renders full-screen in Chromium kiosk on the 7" DSI
  ([displays](../displays/)); the CYDs stay independent Marauder/Flock touch GUIs.
- **Power-switch aware.** Cards for boards whose [toggle switch](../../../README.md) is off should
  show "offline," matching the deck's per-device power modes — the app must tolerate missing serial.
- **Marauder/Flock overlap:** because Marauder carries `sniffbt -t flock`, the WiFi-Marauder and
  BLE-Flock tabs can both source from Gold #1 if Gold #2 is dropped.

## Standalone Mode

The dashboard is plain Python + Flask — it runs on **any Pi or Linux box** with the data sources
reachable. Point each reader at whatever serial ports / hosts exist (`localhost:2501` Kismet,
`localhost:2947` gpsd, the right `/dev/ttyUSB*`), skip the sources you don't have, and browse to
`http://<host>:5000` from any device on the network instead of the kiosk. Nothing ties it to the
Pelican build; pull it onto a laptop for bench testing and it works the same.

## Source / Upstream

- [ESP32 Marauder Web GUI](https://github.com/Pranav-V-20/ESP32-Marauder-Web-GUI) — browser Marauder control via Web Serial (UI reference)
- [python-kismet-rest](https://github.com/kismetwireless/python-kismet-rest) — official Kismet REST API wrapper
- [meshtastic-python](https://github.com/meshtastic/python) — official Meshtastic Python SDK
- Frameworks: [Flask-SocketIO](https://flask-socketio.readthedocs.io/), [pyserial](https://pyserial.readthedocs.io/), [gps3](https://pypi.org/project/gps3/)
- Full software-integration context: [deck README §11](../../../README.md)
