"""
Parse Marauder serial output into structured records for live tables + the target picker.

Two AP formats are handled (they differ by command and firmware):

  scanap stream:   RSSI: -57 Ch: 3 BSSID: 50:ff:20:84:d6:0f ESSID: Octoglass Beacon: ...
  list -a dump:    [0][CH:5] SpectrumSetup-B566 -54

The `list -a` form carries the **index** that `select -a <index>` expects, so it's the
authoritative source for the AP table and the picker. `scanap` lines (when a build streams
them) carry the BSSID. Both are kept; the table prefers the indexed (list -a) set.

Lines that are our own tags (">> cmd", "[error]", "$ ...") or "N selected" are ignored.
"""

import re
from dataclasses import dataclass

_MAC = r"[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}"

# scanap stream line
_SCAN_RE = re.compile(
    r"RSSI:\s*(-?\d+)\s+Ch:\s*(\d+)\s+BSSID:\s*(" + _MAC + r")\s+ESSID:\s*(.*?)\s*(?:Beacon:.*)?$"
)
# list -a / list -c dump line:  [0][CH:5] <name or mac> -54
_LIST_RE = re.compile(r"^\s*\[(\d+)\]\[CH:\s*(\d+)\]\s+(.*?)\s+(-?\d+)\s*$")
_STA_RE = re.compile(r"(?i)\b(?:sta(?:tion)?|client)\b.*?(" + _MAC + r")(?:.*?(" + _MAC + r"))?")
_RSSI_RE = re.compile(r"RSSI:\s*(-?\d+)")


@dataclass
class AP:
    index: int = -1          # Marauder's own index (from list -a); -1 if unknown
    ssid: str = ""
    channel: str = ""
    rssi: str = ""
    bssid: str = ""          # only from scanap stream


@dataclass
class Station:
    mac: str
    ap_bssid: str = ""
    rssi: str = ""


def _is_tag(line: str) -> bool:
    """Our own emitted lines, not device output."""
    if line.startswith((">>", "$")):
        return True
    # a "[" tag that is NOT a "[<digit>]" list row  -> our [error]/[mock]/[i]/[*]/... messages
    return line[:1] == "[" and not (len(line) > 1 and line[1].isdigit())


class MarauderParser:
    """Feed serial lines in; read APs / stations out for tables + picker."""

    def __init__(self):
        self.aps: dict[int, AP] = {}        # keyed by Marauder index (list -a)
        self.scan_aps: dict[str, AP] = {}   # keyed by BSSID (scanap stream)
        self.stations: dict[str, Station] = {}
        self.dirty = False

    def clear(self):
        self.aps.clear()
        self.scan_aps.clear()
        self.stations.clear()
        self.dirty = True

    def feed(self, line: str):
        """Return ('ap'|'sta'|None, record|None)."""
        if not line or _is_tag(line):
            return (None, None)

        # list -a / list -c indexed dump (authoritative — has the select index)
        m = _LIST_RE.match(line)
        if m:
            idx, ch, name, rssi = m.groups()
            idx = int(idx)
            if idx == 0:           # a fresh dump starts at [0] -> replace the old set
                self.aps.clear()
            self.aps[idx] = AP(index=idx, ssid=(name.strip() or "<hidden>"), channel=ch, rssi=rssi)
            self.dirty = True
            return ("ap", self.aps[idx])

        # scanap stream (carries BSSID)
        m = _SCAN_RE.search(line)
        if m:
            rssi, ch, bssid, ssid = m.groups()
            key = bssid.lower()
            self.scan_aps[key] = AP(ssid=(ssid.strip() or "<hidden>"), channel=ch, rssi=rssi, bssid=key)
            self.dirty = True
            return ("ap", self.scan_aps[key])

        # station line (tolerant — format not formally documented)
        m = _STA_RE.search(line)
        if m:
            mac = m.group(1).lower()
            self.stations[mac] = Station(mac, (m.group(2) or "").lower(),
                                         _RSSI_RE.search(line).group(1) if _RSSI_RE.search(line) else "")
            self.dirty = True
            return ("sta", self.stations[mac])

        return (None, None)

    def indexed_aps(self):
        """APs from list -a, in index order — the picker uses these."""
        return [self.aps[i] for i in sorted(self.aps)]

    def ap_rows(self):
        """Rows for the AP table: prefer the indexed (list -a) set, else the scanap stream."""
        if self.aps:
            return self.indexed_aps()

        def strength(a: AP):
            try:
                return int(a.rssi)
            except (ValueError, TypeError):
                return -999
        return sorted(self.scan_aps.values(), key=strength, reverse=True)

    def station_rows(self):
        return list(self.stations.values())
