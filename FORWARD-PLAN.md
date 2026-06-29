# LxveAce/Projects - Forward Plan

> Status: Healthy PUBLIC docs/research portfolio (19 projects + cyberdeck) | Health: GREEN | Date: 2026-06-27 (update on next pickup)

## Where this stands

**What it is.** `LxveAce/Projects` is a PUBLIC, MIT-licensed documentation/research portfolio (~1.4 MB, default branch `main`, last pushed 2026-06-17). The README states plainly: "Everything here is documentation, research, and build notes — not production software." It catalogs 19 cybersecurity/wireless/hardware hobby projects (ESP32 Marauder, Pwnagotchi, Meshtastic, RayHunter, a 14-device Pelican-1300 cyberdeck, etc.), each under `projects/NN-name/` with research notes, build guides, and links.

**How to build/run.** There is NO top-level build system, NO CI (`.github/` absent), NO package manifest, NO releases, NO tags, NO issues. The repo has no build surface of its own. The only real code is one deliberately STALE vendored snapshot: `projects/14-cyberdeck/integrations/01-esp32-marauder/headless-marauder-gui/` (PyQt5 + Tkinter + Textual front-ends, `marauder_core/`). All 14 of its Python files byte-compile cleanly. Its `install.sh` / `run-*.sh` are Linux/Kali-only (venv, apt, `~/.local/bin` launchers, `.desktop`). The maintained home of that code is the separate repo `LxveAce/headless-marauder-gui` (latest v1.3.2).

**Current state.** Working tree clean, `main` in sync with `origin/main`. Health is GREEN for a docs repo — no broken builds, no crash-level defects. The real risks are documentation accuracy: planning docs that have fallen behind already-shipped sibling software, and one hardware-fact contradiction.

**The big picture (from cross-repo recon).** The software this repo once *planned* has already SHIPPED outside it: `headless-marauder-gui` -> `universal-flasher` (+ `universal-flasher-ui`) -> **`cyber-controller`** (the current flagship successor app, v1.1.0, 21 firmware profiles, cybercontroller.org). Any plan here should INFORM that lineage, not duplicate it.

## P0 - do first

1. **Reconcile the stale `UNIVERSAL-FLASHER.md` planning doc.** It still says `Status: Planning` / `Target repo: New repo (TBD)` (lines 4-6) and brainstorms naming candidates (lines 373-385) — but the tool already shipped as `LxveAce/universal-flasher` (v1.3.0, 2026-06-09) and was folded into the flagship **`LxveAce/cyber-controller`** (v1.1.0). Repoint the doc at those shipped repos; remove the moot naming brainstorm (the product is named **Cyber Controller**).
2. **Fix the Gold-board chip contradiction.** `UNIVERSAL-FLASHER.md` lines 138 / 170 / 216 say Lonely Binary "Gold" boards are **ESP32-S3**. The HARDWARE-VERIFIED truth (CLAUDE-TRANSFER.md lines 79-101/199-201, SESSION.md line 213, headless-marauder-gui README line 5) is that Gold boards are **CLASSIC ESP32 (WROOM / CH340)** — esptool reports `Device: ESP32` on all three, and `_multiboardS3.bin` fails preflight. Correct all three references before any plan relies on them.
3. **Validate the flagship installer / `.exe` download surface (cyber-controller).** WEB recon byte-verified exactly ONE asset (cyber-controller `windows-x64.exe` -> HTTP 206, application/octet-stream). But `esp32marauder.com/downloads.html` / `cybercontroller.org` render release links via client-side JS that non-JS recon could not confirm. In a real JS-capable browser, confirm the downloads pages render working clickable installer links for all 4 tools and that each `.exe`/installer downloads end-to-end.

## Surface bugs found

| Title | Location | Severity | Note |
|---|---|---|---|
| `UNIVERSAL-FLASHER.md` is stale (plans an already-shipped tool) | `projects/14-cyberdeck/UNIVERSAL-FLASHER.md` lines 4-6, 373-385 | P2 | Repoint to LxveAce/universal-flasher (v1.3.0) + cyber-controller (v1.1.0); drop naming brainstorm. |
| Gold-board chip contradiction (says S3, is classic ESP32) | `projects/14-cyberdeck/UNIVERSAL-FLASHER.md` lines 138, 170, 216 | P2 | Contradicts CLAUDE-TRANSFER.md, SESSION.md l.213, hmg README l.5; esptool reports ESP32. |
| Embedded marauder README understates upstream version (v1.2.0 vs v1.3.2) | `.../integrations/01-esp32-marauder/headless-marauder-gui/README.md` line 6 | P3 | Latest upstream release is v1.3.2 (2026-06-11). |
| ~~Missing `integrations/17-oui-spy` guide while `projects/17-oui-spy` exists~~ | `projects/14-cyberdeck/integrations/17-oui-spy/` | P3 | **DONE 2026-06-29.** Authored the decision-made guide (LILYGO T-Display S3 + Unified Blue, companion passive detector); confirmed OUI-Spy is distinct, not folded into 18-halehound. Index row added. |
| Stale code snapshot vendored in docs repo (drifts from upstream) | `.../integrations/01-esp32-marauder/headless-marauder-gui/` | P3 | Self-declared stale v1.0.0; its install.sh builds outdated code. Prefer pointer/submodule. |
| Repo `homepageUrl` has a trailing space | GitHub metadata for LxveAce/Projects | P3 | `gh repo edit LxveAce/Projects --homepage https://esp32marauder.com` |

## Features to add

> No explicit user directives were supplied for this plan. The items below derive from recon evidence only.

- **Repoint cyberdeck planning docs to the shipped lineage.** Add a "this shipped as Cyber Controller" banner (with repo + cybercontroller.org links) to `UNIVERSAL-FLASHER.md`, and cross-check `FIRMWARE-REFERENCE.md` / root `README.md` so they INFORM rather than duplicate `cyber-controller` / `universal-flasher`.
- ~~**Add the missing `integrations/17-oui-spy` guide**~~ **DONE 2026-06-29** — authored at `integrations/17-oui-spy/` (T-Display S3 + Unified Blue companion); index updated.
- **Bump the embedded marauder README** version reference v1.2.0 -> v1.3.2 and point readers to the maintained repo's Releases.
- **Optional lightweight CI:** `python -m py_compile` over the vendored snapshot so the one code artifact the repo carries is guarded (today there is no `.github/`).
- **Refresh continuity:** promote `session-context/SESSION.md` (current to 2026-06-27) as authoritative and mark `Projects/CLAUDE-TRANSFER.md` (2026-06-07) as superseded — it predates projects 17-19 and the cyber-controller pivot.

## Red-team / hardening

This repo is PUBLIC — frame everything as responsible hardening, no exploit recipes.

- **PII hygiene.** Recent commits scrubbed legal name + gmail to `LxveAce` / `lxveace@proton.me`. Before the next push, re-grep the whole tree (incl. `INVENTORY.md`, `amazon links.md`, `resources/osint/`, the vendored snapshot, and git history) for residual name/email/address/order-number leakage.
- **Commit identity.** Per standing rules: commit as **LxveAce with NO Claude co-author**; do NOT edit original project READMEs or the cyberdeck `README.md` (integration guides are new clones).
- **Responsible offensive-tooling framing.** Keep project 16 (bluejammer) detector/reference-only (no operational RF jammer), and no Pwnagotchi wired into the deck.
- **Vendored `install.sh` trust boundary.** It uses `sudo`/`apt` and writes `~/.local/bin` launchers + a `.desktop` file (Linux/Kali only). Fine by design, but document the trust boundary so a reader doesn't run it blindly on a non-target host.
- **Ecosystem context (NOT Projects-internal).** Cloudflare HTTP security headers are still MISSING live on all 4 sites incl. cybercontroller.org (served grey-cloud from GitHub Pages) — tracked in private `website-playbook/MANUAL-ACTIONS.md`. Surfaced here only as context.

## Dig deeper (next dedicated session)

1. **Line-by-line reconcile** `UNIVERSAL-FLASHER.md` Section 3 ("What Already Exists") and Sections 5/7/8 ("future work") against the shipped `uf_core/` in `<HOME>/repos/universal-flasher` and `cyber-controller`, so the doc reflects BUILT vs genuinely-open work.
2. **Audit all 50+ research/build `.md` docs** across the 19 projects for accuracy, dead external links (justcallmekoko, EFForg, etc. were never checked), and outdated technical claims — recon only verified internal `projects/NN-name/` links resolve.
3. **Diff the vendored snapshot vs upstream v1.3.2** to quantify drift and decide submodule-vs-pointer-README.
4. **Verify the esptool pin** `>=4.7,<6` against the API `flasher.py` actually calls (taken from a comment, not validated).
5. **Browser-verify the downloads pages** (esp32marauder.com/downloads.html, cybercontroller.org) render working release links for all 4 tools and that each installer/`.exe` downloads end-to-end (recon byte-verified only one asset).
6. **Audit `resources/osint/` and top-level `.md` files** (`INVENTORY.md`, `amazon links.md`, `SECURITY.md`), checked only for existence so far, for PII and accuracy.
7. **Re-verify GitHub-side state.** Pull local clones (universal-flasher, cyber-controller, headless-marauder-gui, session-context) fresh and confirm public/private status + latest-commit-vs-origin via `gh api` — CTX recon read local clones only and flagged they may lag origin.

## Dependencies & cross-repo context

- **Shipped software lineage Projects documents:** `headless-marauder-gui` (public, MIT, Marauder-only, 4 UIs, v1.3.2) -> `universal-flasher` + `universal-flasher-ui` (multi-firmware, v1.3.0 2026-06-09) -> **`cyber-controller`** (FLAGSHIP SUCCESSOR, v1.1.0, 21 firmware profiles, cybercontroller.org).
- **Sibling release health (recon-verified):** cyber-controller v1.1.0 (linux-x64 / macos-arm64 / windows-x64.exe — .exe 52 downloads, one asset byte-verified HTTP 206); universal-flasher v1.1.1 (4 assets, win .exe 48 dl); Suicide-Marauder v1.0.0 (4 assets); headless-marauder-gui v1.3.2.
- **Live sites (all HTTP 200):** esp32marauder.com (+ /downloads.html), lxveace.com, cybercontroller.org.
- **Continuity sources:** `<HOME>/repos/session-context/SESSION.md` (current to 2026-06-27, authoritative) and `<HOME>/Projects/CLAUDE-TRANSFER.md` (2026-06-07, older — predates projects 17-19 + the cyber-controller pivot).
- **Local clones for cross-repo work:** `<HOME>/repos/{universal-flasher, cyber-controller, headless-marauder-gui}`.
- **Standing rules:** commit as LxveAce, NO Claude co-author; no PII on public repos; decision-made not option-dumps; site-header hardening tracked in private `website-playbook/MANUAL-ACTIONS.md`.

## Open questions

- Is the missing `integrations/17-oui-spy` guide intentional (OUI-Spy folded into 18-halehound) or an oversight? Not determinable from files alone.
- Does the vendored snapshot diverge FUNCTIONALLY from upstream v1.3.2, or only in version label? No line-by-line diff was done.
- Do the downloads pages render working clickable release links in a real JS browser? Non-JS recon saw only "Fetching latest release..." placeholders.
- Why does GitHub report Python 123067 / Shell 4000 for a mostly-Markdown repo? Exact `.py`/`.sh` surface inside Projects not fully enumerated.
- Is the README (hardware catalog) vs site (software-tools-first) framing mismatch intentional or stale docs?
- Are the local clones up to date with origin? SESSION.md warns to `git pull` before editing.