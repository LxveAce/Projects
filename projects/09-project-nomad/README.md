# Project N.O.M.A.D. -- Comprehensive Guide

**Node for Offline Media, Archives, and Data**

> A free, open-source, self-contained offline knowledge and education server packed with critical tools, knowledge bases, and local AI -- accessible via any web browser, anytime, anywhere.

---

## Table of Contents

1. [Overview and Use Cases](#1-overview-and-use-cases)
2. [Architecture](#2-architecture)
3. [System Requirements (Why x64 Only)](#3-system-requirements-and-why-x64-only)
4. [ARM Compatibility: Status, Workarounds, and What Needs Changing](#4-arm-compatibility-status-workarounds-and-what-needs-changing)
5. [LattePanda Option: Which Model and Setup](#5-lattepanda-option-which-model-and-setup)
6. [Installation Guide](#6-installation-guide)
7. [Features](#7-features)
8. [Meshtastic Integration](#8-meshtastic-integration)
9. [Field Deployment](#9-field-deployment)
10. [Building Your Own (Forking Guide)](#10-building-your-own-forking-guide)

---

## 1. Overview and Use Cases

Project N.O.M.A.D. is a free, open-source (Apache 2.0), self-contained offline knowledge and education server created by [Crosstalk Solutions](https://github.com/Crosstalk-Solutions). It bundles critical tools, knowledge bases, and local AI into a single Docker-orchestrated platform accessible via any web browser. The core philosophy: download everything while online, then run entirely disconnected -- no internet, no cloud, no signal required. Zero telemetry by design.

**Repository stats (as of June 2026):** 29.1k GitHub stars, 2.9k forks, 69 releases (latest v1.32.1), 582 commits, Apache 2.0 license.

### Primary Use Cases

- **Emergency preparedness / disaster response** -- Medical references, survival guides, offline Wikipedia, maps when infrastructure is down
- **Off-grid living** -- Cabins, RVs, sailboats, remote homesteads
- **Education without internet** -- Khan Academy courses, K-12 curriculum, Project Gutenberg library for schools or families without connectivity
- **Field deployments** -- Military, humanitarian, research stations
- **Tech enthusiast / data sovereignty** -- Local AI with full data ownership, no cloud dependency
- **Homelab / prepper builds** -- Grab-and-go offline computer with everything loaded

### What It Is NOT (Yet)

It is not a communications platform. It does not currently integrate Meshtastic, mesh radios, or any real-time messaging between nodes. It is a knowledge/AI server, not a comms server -- though community discussions are exploring that direction (see [Section 8](#8-meshtastic-integration)).

---

## 2. Architecture

### Tech Stack

| Component | Role |
|-----------|------|
| TypeScript (93.5%) | Command Center UI and API |
| Shell (5.6%) | Installation, lifecycle scripts |
| Node.js 22 | Runtime (built from `node:22-slim` Docker image) |
| MySQL | Application state, tool registry, settings, benchmark scores |
| Redis | Session management and caching |
| Docker | All services run as containers orchestrated by the Command Center |

### Architectural Pattern: Docker-outside-of-Docker

The Command Center is itself a Docker container that manages sibling containers on the host's Docker daemon. It acts as a control plane handling installation, configuration, lifecycle management, and updates for all bundled applications.

### Container Inventory

All NOMAD containers are prefixed with `nomad_` and include:

| Container | Purpose | Notes |
|-----------|---------|-------|
| Command Center | Management UI + API | Port 8080 (default) |
| MySQL | State persistence | Credentials auto-generated |
| Redis | Sessions/caching | Internal only |
| Ollama | Local LLM inference | GPU passthrough auto-detected |
| Open WebUI | AI chat interface | RAG-enabled via Qdrant |
| Qdrant | Vector database | Semantic search for uploaded docs |
| Kiwix | Offline encyclopedias | Wikipedia, medical refs, Gutenberg |
| Kolibri | Education platform | Khan Academy, K-12 content |
| ProtoMaps + MapLibre GL JS | Offline maps | Regional downloads, OSM data |
| CyberChef | Data/crypto tools | Encoding, hashing, analysis |
| FlatNotes | Note-taking | Local markdown notes |
| Dozzle | Container logs | Port 9999, shell access disabled |
| Updater sidecar | Self-update mechanism | Updates Command Center only |

### Startup Sequencing

Uses `wait-for-it.sh` (from vishnubob/wait-for-it) for healthcheck-based container startup ordering.

### Internet Detection

Single request to Cloudflare's `1.1.1.1/cdn-cgi/trace` endpoint to determine online/offline status. Internet is needed only during initial install and content downloads.

### Installation Path

Everything deploys to `/opt/project-nomad/`. Helper scripts: `start_nomad.sh`, `stop_nomad.sh`, `update_nomad.sh`, `uninstall_nomad.sh`.

---

## 3. System Requirements (And Why x64 Only)

### Minimum (Basic Browsing, No AI)

| Spec | Requirement |
|------|-------------|
| CPU | 2 GHz dual-core x86-64 |
| RAM | 4 GB |
| Storage | 5 GB free |
| OS | Debian-based Linux (Ubuntu recommended) |
| Internet | During installation only |

### Recommended (With AI Capabilities)

| Spec | Requirement |
|------|-------------|
| CPU | AMD Ryzen 7 / Intel Core i7 or better |
| RAM | 32 GB |
| GPU | NVIDIA RTX 3060+ or AMD equivalent (more VRAM = larger models) |
| Storage | 250 GB+ SSD (1 TB handles all Wikipedia with images + Khan Academy + maps) |
| OS | Ubuntu Desktop 24.04 LTS |

### Why x86-64 Only

The x64 requirement stems from multiple factors:

1. **Docker images are built only for `linux/amd64`** -- The official container images published by the project target exclusively amd64 architecture. No multi-arch manifests are published.

2. **Upstream dependency images** -- Several bundled tools (Ollama, Kiwix, Open WebUI, Qdrant) publish their own Docker images primarily for amd64. While some do offer arm64 variants, not all do, and NOMAD's Compose files do not reference multi-arch tags.

3. **GPU acceleration assumptions** -- The installer auto-detects NVIDIA GPUs and configures the NVIDIA Container Toolkit for Docker GPU passthrough. This NVIDIA-centric path has no ARM equivalent (ARM GPU acceleration for LLM inference is a different ecosystem entirely).

4. **Install script validation** -- The `install_nomad.sh` script (~500+ lines) validates for bash, Debian-based OS, and sudo access. It does not explicitly block ARM, but the amd64-only Docker images it pulls will fail on ARM hosts.

5. **Performance positioning** -- The project deliberately targets "beefy machines" over single-board computers. As stated in their materials: "other offline products are stuck on Raspberry Pis, while NOMAD supports GPU-accelerated inference on models with real intelligence."

### Officially NOT Supported

- Raspberry Pi / ARM devices
- Virtual machines (Proxmox, Hyper-V, VMware)
- macOS (Docker GPU passthrough limitations)
- Non-Debian Linux (install scripts are Debian-optimized)
- Windows native (WSL2 is community-supported)

---

## 4. ARM Compatibility: Status, Workarounds, and What Needs Changing

### Current Status

**Officially unsupported.** The FAQ states: "Project N.O.M.A.D. is currently designed to run on x86-64 architecture. We have not yet tested or optimized it for ARM-based devices."

ARM support is on the roadmap, and there is an open feature request ([Issue #816](https://github.com/Crosstalk-Solutions/project-nomad/issues/816), opened May 2026) marked as "Critical -- Blocking my use of N.O.M.A.D." by the submitter, requesting official arm64/Raspberry Pi support.

### Community ARM Fork: project-nomad-rpi

A community member (eglische) has published a working fork at [github.com/eglische/project-nomad-rpi](https://github.com/eglische/project-nomad-rpi) that adds:

- **Raspberry Pi 5 ARM64 support** with adapted installer and service logic
- **External storage awareness** for USB/HDD-backed data (avoids filling SD cards)
- **NVIDIA eGPU/CUDA integration** (work-in-progress) for Pi 5 inference acceleration
- **Recovery-aware installation** that detects preserved content on reinstall
- **Expanded diagnostics** with frontend health monitoring and repair tools
- **RTL-SDR radio capabilities** via containerized SDR services

Install command for the RPi fork:

```bash
sudo apt-get update && sudo apt-get install -y curl &&
curl -fsSL https://raw.githubusercontent.com/eglische/project-nomad-rpi/refs/heads/main/install/install_nomad.sh -o install_nomad.sh &&
sudo bash install_nomad.sh
```

### What Specifically Needs Changing for ARM

If you wanted to fork and port NOMAD to ARM yourself, here is what you would need to address:

1. **Docker image rebuilds** -- The Command Center image (based on `node:22-slim`) needs to be built for `linux/arm64`. Node.js 22 does have official arm64 images, so this is straightforward.

2. **Compose file platform tags** -- All `docker-compose.yml` service definitions need multi-arch image references or arm64-specific tags.

3. **Upstream service images:**
   - **Ollama** -- Has official arm64 Docker images. Should work.
   - **Open WebUI** -- Has arm64 images. Should work.
   - **Qdrant** -- Has arm64 images. Should work.
   - **Kiwix-serve** -- Has arm64 images. Should work.
   - **Kolibri** -- Runs on Python; arm64 compatible.
   - **CyberChef** -- Web-based; should work on any arch.
   - **MySQL** -- Has official arm64 images.
   - **Redis** -- Has official arm64 images.

4. **GPU detection logic** -- The NVIDIA Container Toolkit detection in `install_nomad.sh` is irrelevant on Pi. The installer needs ARM-specific GPU handling or graceful fallback to CPU-only mode.

5. **Native dependencies** -- `graphicsmagick` and `libvips-dev` (used by the Command Center for PDF thumbnails and image processing) need to be available as arm64 packages. Both are available in Ubuntu's arm64 repos.

6. **Benchmark system** -- The built-in hardware benchmark and "Builder Tags" leaderboard may need ARM-specific scoring adjustments.

### QEMU Emulation (Running x64 Images on ARM)

Technically possible but **not recommended** for NOMAD:

- Enable with: `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes`
- Performance penalty is severe: **5-8x slower** than native execution
- An operation taking 30 seconds natively takes 2-5 minutes under emulation
- Running Ollama LLM inference under QEMU on a Pi would be essentially unusable
- QEMU emulation is meant for building/testing, not production workloads

**Bottom line:** QEMU is not a viable path. Use the community RPi fork or a native x64 board.

---

## 5. LattePanda Option: Which Model and Setup

Since the Raspberry Pi 5 (ARM) does not work with NOMAD, a LattePanda board is an excellent alternative -- it is x86-64, runs Ubuntu natively, supports Docker, and is small enough for field deployment.

### LattePanda 3 Delta (~$220-270)

| Spec | Detail |
|------|--------|
| CPU | Intel Celeron N5105 (4C/4T, up to 2.9 GHz, 10W TDP) |
| RAM | 8 GB LPDDR4 2933 MHz |
| Storage | 64 GB eMMC + M.2 M-Key (NVMe) + M.2 B-Key (SATA/4G) |
| Network | 2.5 GbE, Wi-Fi 6 |
| Size | 125 x 78 x 16 mm |
| GPU | Intel UHD Graphics (no discrete GPU) |

**NOMAD viability:** Can run all NOMAD services EXCEPT AI/LLM inference will be very slow (CPU-only, low-end). Perfect for Kiwix, Kolibri, maps, CyberChef, and notes. Could use a remote Ollama server for AI if needed.

**Best for:** Budget NOMAD build, non-AI use cases, portable knowledge server.

### LattePanda Sigma (~$579-650)

| Spec | Detail |
|------|--------|
| CPU | Intel Core i5-1340P (4P+8E cores, 16 threads, up to 4.6 GHz, 28W TDP) |
| RAM | 16 GB or 32 GB LPDDR5 6400 MHz |
| Storage | Dual M.2 M-Key slots (up to 8 TB NVMe) |
| Network | Dual 2.5 GbE, Wi-Fi 6E (optional) |
| GPU | Intel Iris Xe (80 EU) -- decent integrated graphics |
| Thunderbolt 4 | 2x ports (eGPU possible for AI acceleration) |

**NOMAD viability:** Excellent. Can run all NOMAD services including local AI with smaller models (7B-13B parameter LLMs). The 32 GB RAM version can handle RAG workloads. Thunderbolt 4 enables eGPU for larger models.

**Best for:** Full-featured NOMAD build with AI, field deployable, serious offline knowledge station.

### Recommended Builds

**Budget build (LP3 Delta):**

| Component | Cost |
|-----------|------|
| LattePanda 3 Delta 864 | ~$230 |
| 512 GB or 1 TB NVMe SSD | ~$40-80 |
| Ubuntu Desktop 24.04 LTS | Free |
| 12V 3A power supply | Included/~$15 |
| Optional: portable battery pack | ~$40 |
| **Total** | **~$270-310** |

**Full-featured build (LP Sigma):**

| Component | Cost |
|-----------|------|
| LattePanda Sigma 32GB | ~$650 |
| 1 TB NVMe SSD | ~$60 |
| Ubuntu Desktop 24.04 LTS | Free |
| 12V power supply | Included/~$15 |
| Optional: Thunderbolt 4 eGPU enclosure + GPU | ~$300-500 |
| **Total** | **~$710-1200+** |

### LattePanda NOMAD Installation Steps

1. Install Ubuntu Desktop 24.04 LTS on the NVMe SSD (use Rufus/Etcher to create USB installer)
2. Configure BIOS to boot from NVMe
3. Run `sudo apt update && sudo apt upgrade -y`
4. Install NOMAD using the standard install script (see [Section 6](#6-installation-guide))
5. Configure content downloads via the Command Center UI
6. Disconnect from internet -- NOMAD runs fully offline

---

## 6. Installation Guide

### Prerequisites

- x86-64 hardware with Debian-based Linux (Ubuntu Desktop 24.04 LTS recommended)
- Internet connection for initial setup
- Minimum 5 GB free disk space (1 TB recommended for full content)

### Step 1: Prepare Ubuntu

1. Download Ubuntu Desktop 24.04 LTS from [ubuntu.com](https://ubuntu.com) (~6 GB)
2. Create bootable USB with Rufus (Windows) or Balena Etcher
3. Boot from USB, select "Try or Install Ubuntu"
4. Choose "Interactive installation" > "Default apps"
5. Enable third-party graphics/Wi-Fi drivers
6. Select "Erase disk and install Ubuntu"
7. Create user account, set timezone

### Step 2: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 3: (Optional) Enable SSH for Remote Access

```bash
sudo apt install openssh-server -y && sudo systemctl enable --now ssh
```

### Step 4: Install Project NOMAD

```bash
sudo apt install curl -y
curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/main/install/install_nomad.sh -o install_nomad.sh
sudo bash install_nomad.sh
```

The installer (~500+ lines) automatically:

- Validates environment (bash, Debian, sudo)
- Installs Docker if missing
- Detects NVIDIA GPUs and configures NVIDIA Container Toolkit
- Generates random MySQL credentials
- Downloads Docker Compose manifests
- Deploys to `/opt/project-nomad/`
- Sets up the updater sidecar container
- Installation completes in approximately 1 minute (excluding content downloads)

### Step 5: Access Command Center

Open browser to `http://localhost:8080` or `http://<device-ip>:8080`

### Step 6: Configure via Easy Setup Wizard

1. Select applications to install (Information Library, Education Platform, AI Assistant)
2. Choose map regions
3. Select content tiers (Essential / Standard / Comprehensive)
4. Monitor storage usage bar while selecting
5. Click "Complete Setup" to begin downloading content

### Step 7: Download Content While Online

Content download times vary. A full build with Wikipedia (images), Khan Academy, and regional maps can take several hours on a fast connection. 1 TB handles everything comfortably.

### Step 8: Go Offline

Once content is downloaded, disconnect from the internet. NOMAD runs entirely self-contained.

### Management Scripts

Located at `/opt/project-nomad/`:

```bash
sudo bash /opt/project-nomad/start_nomad.sh      # Start all containers
sudo bash /opt/project-nomad/stop_nomad.sh       # Stop all containers
sudo bash /opt/project-nomad/update_nomad.sh     # Update Command Center
sudo bash /opt/project-nomad/uninstall_nomad.sh  # Complete removal
```

### WSL2 (Windows)

Community-supported. Install WSL2 with Ubuntu 24.04, then follow the same install steps above. GPU passthrough works with NVIDIA GPUs through WSL2's native CUDA support.

---

## 7. Features

### Information Library (Kiwix)

- Offline Wikipedia (full text or with images -- 99.6 GB with images)
- Project Gutenberg (70,000+ free ebooks)
- Medical references (WikiMed, offline health guides)
- Survival/repair guides
- Wiktionary, Wikivoyage, and more
- Three content tiers: Essential, Standard, Comprehensive

### AI Assistant (Ollama + Open WebUI + Qdrant)

- Local LLM chat with no cloud dependency
- RAG (Retrieval-Augmented Generation) via Qdrant vector database
- Document upload and semantic search against your own files
- Auto-detects NVIDIA GPU for acceleration; AMD ROCm support added in v1.32.0
- Remote Ollama support: point to an external server with `OLLAMA_HOST=0.0.0.0`
- LM Studio compatible (OpenAI-compatible API)
- Per-file ingest state machine with policy controls (v1.32.0+)
- KB guardrails at storage thresholds (50 GB / 10% free)

### Education Platform (Kolibri)

- Khan Academy courses (math, science, computing, etc.)
- K-12 curriculum content
- Progress tracking for individual learners
- Content available in multiple languages

### Offline Maps (ProtoMaps + MapLibre GL JS)

- OpenStreetMap data downloadable by region
- Street-level detail with search and navigation
- Regional pmtiles extraction (v1.32.0+)
- No internet needed after initial download

### Data and Security Tools (CyberChef)

- Encryption, encoding, decoding, hashing
- Data analysis and transformation
- Fully offline web-based tool

### Notes (FlatNotes)

- Local markdown-based note-taking
- No cloud sync, no accounts

### System Benchmark

- Hardware scoring system
- "Builder Tags" for community identification
- Community leaderboard at benchmark.projectnomad.us
- Scores range 10-95 depending on hardware

### Container Monitoring (Dozzle)

- Real-time container log viewing
- Shell access disabled by default for security

### Security Posture

- No authentication by default (by design -- "open and available without hurdles")
- No telemetry
- Not designed for internet exposure
- Caddy with basicauth available for network deployments to gate `/settings` and admin APIs
- MySQL/Redis ports not exposed externally by default
- SSRF patches applied in v1.32.0

---

## 8. Meshtastic Integration

### Current Status: NOT INTEGRATED

As of v1.32.1 (June 2026), Project NOMAD has **no Meshtastic integration** and **no built-in mesh communication features**. The project website, GitHub README, and FAQ do not mention Meshtastic anywhere.

### Community Vision: "Sovereign P2P Node"

[GitHub Discussion #381](https://github.com/Crosstalk-Solutions/project-nomad/discussions/381) proposes evolving NOMAD from an "Offline Server" into a "Sovereign P2P Node." Key proposals include:

- **Reticulum protocol integration** -- Would enable node-to-node discovery and messaging via LoRa, packet radio, or local Wi-Fi meshes. The existing "Nomad Network" project by Mark Qvist (which runs on Reticulum) was noted for name synergy.
- **Decentralized updates** -- Using Freenet or IPFS to distribute patches and content without GitHub
- **Sneakernet data sync** -- LAN cable or USB drive synchronization of large datasets between NOMAD nodes
- **APRStac** -- Mentioned as complementary infrastructure supporting messaging, email, BBS, and ATAK integration

### Why Reticulum Instead of Meshtastic?

The community discussion favors Reticulum over Meshtastic because:

- Reticulum scales to millions of nodes (Meshtastic is limited to ~80 nodes per mesh)
- Reticulum supports multiple transports: LoRa, packet radio, TCP/IP, Wi-Fi, serial
- Reticulum has an existing "Nomad Network" application for messaging, BBS, and file transfer
- Reticulum is protocol-level, while Meshtastic is more of an end-user product

### What You Could Do Today (DIY Integration)

If you want mesh comms alongside NOMAD on the same hardware:

1. **Meshtastic node** -- Connect a Meshtastic radio (T-Beam, RAK WisBlock, Heltec V3) via USB to your NOMAD machine. Run the Meshtastic Python CLI or web client in a separate Docker container. NOMAD and Meshtastic would be independent services sharing hardware.

2. **Reticulum/Nomad Network** -- Install `pip install nomadnet` and `pip install rns` alongside NOMAD. Connect a LoRa radio (RNode, T-Beam with Reticulum firmware). This gives you encrypted mesh messaging, BBS, and file transfer.

3. **SimpleX Chat** -- Some community members have mentioned running SimpleX Chat server as an additional Docker container on NOMAD hardware for encrypted messaging over local networks.

None of these are integrated into the NOMAD UI -- they would be separate services running on the same machine.

---

## 9. Field Deployment

### Power Considerations

- LattePanda 3 Delta: 10W TDP, 12V input -- runs from a car cigarette lighter, portable battery, or solar panel
- LattePanda Sigma: 28W TDP, 12V input -- needs beefier portable power but still very feasible
- A 100Wh portable battery (~$40) runs a LP3 Delta for 8-10 hours

### Network Configuration for Field Use

- NOMAD serves via HTTP on port 8080
- Any device on the same network can access it via browser
- Set up the NOMAD host as a Wi-Fi hotspot (using `hostapd` or NetworkManager) so phones/tablets/laptops can connect and browse
- No internet required -- just local Wi-Fi

### Ruggedization

- House the SBC in a waterproof Pelican-style case
- Add a small 7" touchscreen (eDP or HDMI) for direct interaction
- Include a USB Wi-Fi adapter configured as an access point
- Pre-load all content before deployment

### Content Pre-Loading Checklist

- [ ] Wikipedia with images (~100 GB)
- [ ] Regional maps for deployment area
- [ ] Medical references (WikiMed)
- [ ] Khan Academy courses (relevant subjects)
- [ ] Project Gutenberg ebooks
- [ ] AI model (7B parameter for LP Sigma, skip for LP3 Delta)
- [ ] Custom documents uploaded to RAG knowledge base
- [ ] Survival/repair guides

### Multi-Node Deployment

Currently, each NOMAD instance is independent. No built-in node-to-node sync exists. For multi-node scenarios:

- Pre-image a master drive, clone to other nodes
- Use "sneakernet" (USB drives) to transfer content updates between nodes
- Future Reticulum integration could enable automatic mesh sync

---

## 10. Building Your Own (Forking Guide)

### Fork Strategy for ARM Support

If you want to create your own ARM-compatible fork rather than using the existing community RPi fork:

#### Step 1: Fork the Repository

```bash
gh repo fork Crosstalk-Solutions/project-nomad --clone
cd project-nomad
```

#### Step 2: Identify Architecture-Specific Components

Key files to modify:

- `install/install_nomad.sh` -- Main installer, ~500+ lines. Remove/modify NVIDIA GPU detection for ARM. Add ARM architecture detection.
- `docker-compose.yml` (template) -- Change image tags to multi-arch or arm64-specific variants
- Any Dockerfiles in the repo -- Change base images from amd64-specific to multi-arch (e.g., `node:22-slim` already supports arm64)

#### Step 3: Rebuild the Command Center Image for ARM

```bash
# Enable buildx multi-arch
docker buildx create --use
# Build for arm64
docker buildx build --platform linux/arm64 -t your-registry/project-nomad:arm64 --push .
```

#### Step 4: Update Service Image References

For each service in the Compose file, verify arm64 image availability:

| Service | arm64 Available? |
|---------|-----------------|
| `ollama/ollama` | Yes |
| `ghcr.io/open-webui/open-webui` | Yes |
| `qdrant/qdrant` | Yes |
| `kiwix/kiwix-serve` | Yes |
| `mysql` | Yes |
| `redis` | Yes |
| `learningequality/kolibri` | Yes (Python-based) |

#### Step 5: Modify the Installer

Key changes in `install_nomad.sh`:

```bash
# Add architecture detection
ARCH=$(dpkg --print-architecture)
if [ "$ARCH" != "amd64" ] && [ "$ARCH" != "arm64" ]; then
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

# Make GPU detection conditional
if [ "$ARCH" = "amd64" ]; then
    # Existing NVIDIA detection logic
    detect_nvidia_gpu
fi

# Use arch-appropriate image tags
if [ "$ARCH" = "arm64" ]; then
    NOMAD_IMAGE="your-registry/project-nomad:arm64"
else
    NOMAD_IMAGE="ghcr.io/crosstalk-solutions/project-nomad:latest"
fi
```

#### Step 6: Handle ARM-Specific Concerns

- **Storage:** ARM SBCs often use SD cards. Add external storage detection and data directory redirection (the RPi fork does this).
- **Memory:** Pi 5 has 4-8 GB RAM. Set conservative defaults for MySQL/Redis buffer sizes.
- **AI models:** Default to tiny models (TinyLlama 1.1B, Phi-2 2.7B) or disable AI by default on ARM.
- **Thermal:** ARM SBCs throttle under sustained load. Consider adding temperature monitoring/alerts.

#### Step 7: Test Thoroughly

```bash
# On your Pi 5 with Ubuntu 24.04 arm64
sudo bash install_nomad.sh
# Verify all containers start
docker ps | grep nomad_
# Test each service via browser
```

### Alternatively: Use the Existing RPi Fork

The [eglische/project-nomad-rpi](https://github.com/eglische/project-nomad-rpi) fork has already done most of this work. It supports:

- Pi 5 ARM64
- External USB/HDD storage
- eGPU integration (WIP)
- RTL-SDR radio
- Recovery-aware installation

Consider contributing to that fork rather than starting from scratch.

### Contributing Back Upstream

The official [Issue #816](https://github.com/Crosstalk-Solutions/project-nomad/issues/816) proposes a phased approach for official ARM support:

1. Publish multi-arch Docker images (amd64 + arm64)
2. Add architecture validation to the installer with warnings
3. Move port config to environment files
4. Enable port conflict detection
5. Document remote Ollama configuration

If your fork works well, submit a PR referencing Issue #816.

---

## Decision Matrix

| Option | Cost | AI Capable | Portable | Effort | Recommendation |
|--------|------|-----------|----------|--------|----------------|
| LattePanda 3 Delta | ~$270-310 | Limited (CPU only) | Excellent | Low (standard install) | Best budget option for non-AI NOMAD |
| LattePanda Sigma 32GB | ~$710-1200 | Yes (with eGPU: very) | Good | Low (standard install) | Best full-featured portable NOMAD |
| Pi 5 + RPi Fork | ~$100-150 | Minimal | Excellent | Medium (community fork) | Cheapest if AI not needed |
| Pi 5 + Your Own Fork | ~$100-150 | Minimal | Excellent | High (significant dev work) | Only if RPi fork doesn't meet needs |
| Pi 5 + QEMU emulation | ~$100-150 | No (too slow) | N/A | N/A | NOT recommended, 5-8x performance hit |
| Used Mini PC (x64) | ~$50-150 | Maybe (depends on specs) | Moderate | Low (standard install) | Best value if portability is secondary |

---

## Recent Release History

| Version | Date | Highlights |
|---------|------|------------|
| v1.32.1 | May 27, 2026 | Fixed logging, Qdrant facet optimization |
| v1.32.0 | May 20, 2026 | 40+ bug fixes, AMD ROCm GPU support, SSRF patches, per-file ingest |
| v1.31.1 | Apr 21, 2026 | Model download cancellation, NFS mount fixes, Qdrant telemetry disabled |
| v1.31.0 | Earlier 2026 | Feature release |

No ARM-specific modifications in any recent releases. Updates focus on x86_64 optimization, GPU acceleration (NVIDIA/AMD), and security hardening.

---

## Sources

- [Project NOMAD GitHub Repository](https://github.com/Crosstalk-Solutions/project-nomad)
- [Project NOMAD Official Website](https://www.projectnomad.us/)
- [Project NOMAD Install Guide](https://www.projectnomad.us/install)
- [Project NOMAD FAQ](https://github.com/Crosstalk-Solutions/project-nomad/blob/main/FAQ.md)
- [Issue #816: ARM64/Raspberry Pi Support Request](https://github.com/Crosstalk-Solutions/project-nomad/issues/816)
- [Community RPi Fork (eglische)](https://github.com/eglische/project-nomad-rpi)
- [Discussion #381: Sovereign P2P Node Vision](https://github.com/Crosstalk-Solutions/project-nomad/discussions/381)
- [VirtusLab Architecture Analysis](https://virtuslab.com/blog/ai/project-nomad)
- [Project NOMAD Releases](https://github.com/Crosstalk-Solutions/project-nomad/releases)
- [LattePanda 3 Delta Specs](https://www.lattepanda.com/lattepanda-3-delta)
- [LattePanda Sigma Specs](https://www.lattepanda.com/lattepanda-sigma)
- [Docker Multi-Architecture Builds](https://docs.docker.com/build/building/multi-platform/)
- [Meshtastic Official](https://meshtastic.org/)
- [Reticulum / Nomad Network](https://unsigned.io/software/Nomad_Network.html)

---

## 11. Best-Fit Hardware from Your Inventory

### Status: Blocked -- Need x64 SBC

Your Pi 5 is ARM64 and Project Nomad requires x86-64. **No compatible board in current inventory.**

### Reserved Components (Once x64 SBC Purchased)

| Component | Assignment | Why |
|-----------|-----------|-----|
| **Display** | Hosyond 7" DSI Touchscreen IPS #2 | Desktop-class display for the NOMAD web UI (if SBC has DSI). Otherwise ELECROW 5" HDMI TFT |
| **Keyboard** | ProtoArc XK01 TP Foldable Bluetooth Keyboard | Full-size foldable layout with touchpad. Ideal for a portable hacking workstation -- more comfortable than Rii mini for extended sessions |
| **Adapter** | JSAUX Micro HDMI to HDMI Adapter #3 (spare) | If x64 SBC uses micro HDMI |
| **Storage** | 128GB Micro SD or 32GB USB 3.0 Flash Drive | For bootable OS |

### What to Buy

| Item | Price | Why |
|------|-------|-----|
| **LattePanda 3 Delta** | ~$200-250 | Best budget x64 SBC for NOMAD. Intel N100, 8GB RAM. Standard Docker install works |
| LattePanda Sigma 32GB | ~$710-1200 | Full-featured option with eGPU support for AI features |
| Used Mini PC (x64) | ~$50-150 | Best value if portability is secondary |
