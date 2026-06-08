# Headless Marauder GUI

> **This project has moved to its own repo:**
> **https://github.com/LxveAce/headless-marauder-gui**

The code in this folder is a stale snapshot from v1.0.0. The current version (v1.2.0) lives at the link above and includes:

- **Four front-ends** — PyQt5 GUI, Tkinter GUI, Textual TUI, and a Browser UI (Flask + WebSocket)
- **Standalone executables** — pre-built binaries for Windows x64, Linux x64, and **Linux ARM64** (Raspberry Pi / ARM SBCs) on the [Releases page](https://github.com/LxveAce/headless-marauder-gui/releases/latest)
- 70+ Marauder commands, live AP/Station tables, target picker, built-in firmware flasher, data logging
- Bug fixes, security policy, legal disclaimer

**For the cyberdeck:** grab the [ARM64 Linux binary](https://github.com/LxveAce/headless-marauder-gui/releases/latest) — it runs directly on the Pi without needing Python or any dependencies installed.

**Install from source on the Pi:**
```bash
git clone https://github.com/LxveAce/headless-marauder-gui.git
cd headless-marauder-gui
./install.sh
```

See the [full README](https://github.com/LxveAce/headless-marauder-gui#readme) for docs, install instructions, and troubleshooting.
