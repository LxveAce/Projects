"""
Parse Marauder serial output into structured records for live tables.

Confirmed AP line format (scanap / list -a), e.g.:
    RSSI: -57 Ch: 3 BSSID: 50:ff:20:84:d6:0f ESSID: Octoglass Beacon: 11 18 1 17464

Station / list output isn't formally documented and varies by firmware, so the station
matcher is deliberately tolerant (any line that mentions a station + a MAC). Unmatched
lines (banners, ">> cmd", "[sys]") are simply ignored.
"""

import re
from dataclasses import dataclass

_MAC = r"[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}"

_AP_RE = re.compile(
    r"RSSI:\s*(-?\d+)\s+Ch:\s*(\d+)\s+BSSID:\s*(" + _MAC + r")\s+ESSID:\s*(.*?)\s*(?:Beacon:.*)?$"
)
# "Station: AA:.. ... [AP/BSSID BB:..]" or "STA AA:.. -> BB:.." etc.
_STA_RE = re.compile(r"(?i)\b(?:sta(?:tion)?|client)\b.*?(" + _MAC + r")(?:.*?(" + _MAC + r"))?")
_RSSI_RE = re.compile(r"RSSI:\s*(-?\d+)")


@dataclass
class AP:
    bssid: str
    ssid: str = ""
    channel: str = ""
    rssi: str = ""


@dataclass
class Station:
    mac: str
    ap_bssid: str = ""
    rssi: str = ""


class MarauderParser:
    """Feed serial lines in; read .aps / .stations out. Upserts by MAC."""

    def __init__(self):
        self.aps: dict[str, AP] = {}
        self.stations: dict[str, Station] = {}
        self.dirty = False

    def clear(self):
        self.aps.clear()
        self.stations.clear()
        self.dirty = True

    def feed(self, line: str):
        """Return ('ap'|'sta'|None, record|None)."""
        if not line or line.startswith((">>", "[", "$")):
            return (None, None)

        m = _AP_RE.search(line)
        if m:
            rssi, ch, bssid, ssid = m.groups()
            key = bssid.lower()
            self.aps[key] = AP(key, (ssid or "").strip() or "<hidden>", ch, rssi)
            self.dirty = True
            return ("ap", self.aps[key])

        m = _STA_RE.search(line)
        if m:
            mac = m.group(1).lower()
            ap = (m.group(2) or "").lower()
            # don't shadow an AP we already know about
            if mac in self.aps:
                return (None, None)
            rssi_m = _RSSI_RE.search(line)
            self.stations[mac] = Station(mac, ap, rssi_m.group(1) if rssi_m else "")
            self.dirty = True
            return ("sta", self.stations[mac])

        return (None, None)

    def ap_rows(self):
        """APs sorted by signal strength (strongest first)."""
        def strength(a: AP):
            try:
                return int(a.rssi)
            except (ValueError, TypeError):
                return -999
        return sorted(self.aps.values(), key=strength, reverse=True)

    def station_rows(self):
        return list(self.stations.values())
