# OSINT & CTI

Tools, methodology, workstation setup, training, and legal guidelines for open-source intelligence and cyber threat intelligence.

---

## Table of Contents

1. [Overview: OSINT and CTI](#1-overview-osint-and-cti)
2. [Tools by Category](#2-tools-by-category)
3. [BushidoUK Repo Highlights](#3-bushidouk-repo-highlights)
4. [OSINT Workstation Setup](#4-osint-workstation-setup)
5. [Methodology: The OSINT Intelligence Cycle](#5-methodology-the-osint-intelligence-cycle)
6. [Practice: CTFs, Challenges & Training](#6-practice-ctfs-challenges--training)
7. [Legal and Ethical Guidelines](#7-legal-and-ethical-guidelines)
8. [Sources](#sources)

---

## 1. Overview: OSINT and CTI

### What is OSINT?

OSINT is intelligence gathered from publicly available sources — websites, social media, public records, news, government reports, satellite imagery, etc. The difference between OSINT and just googling something is structure: you follow an intelligence cycle (define requirements, collect, process, analyze, report) instead of ad-hoc searching.

### What is CTI?

CTI (Cyber Threat Intelligence) applies OSINT specifically to cybersecurity — tracking threat actors, their TTPs, IOCs, and the broader threat landscape. It breaks down into three tiers:

- **Strategic Intelligence** -- Long-term trends, threat actor motivations, geopolitical context. Audience: executives and decision-makers.
- **Operational Intelligence** -- Campaigns, attack patterns, breach data, vulnerability tracking. Audience: security managers and incident responders.
- **Tactical Intelligence** -- Specific IOCs (IPs, hashes, domains), malware signatures, phishing infrastructure. Audience: SOC analysts and security engineers.

### Passive vs. Active OSINT

- **Passive OSINT**: Collecting information without directly interacting with the target. No packets sent, no accounts contacted. Examples: reading public posts, searching cached pages, reviewing WHOIS records.
- **Active OSINT**: Directly interacting with the target (port scanning, sending emails, creating sock puppet accounts to join closed groups). This crosses into gray/illegal territory depending on jurisdiction.

---

## 2. Tools by Category

### A. People Search & Identity Resolution

| Tool | URL | Description |
|------|-----|-------------|
| OSINT Industries | https://www.osint.industries/ | Real-time lookup across 200+ platforms by email, phone, username, or crypto wallet |
| Epieos | https://epieos.com/ | Reverse email and phone lookup; reveals linked Google accounts and reviews |
| Maigret | https://github.com/soxoj/maigret | Username enumeration across 2500+ sites; generates detailed reports |
| WhatsMyName | https://whatsmyname.app/ | Username search across hundreds of platforms |
| Holehe | https://github.com/megadose/holehe | Checks if an email is registered on 120+ sites without alerting the target |
| Profil3r | https://github.com/Rog3rSm1th/Profil3r | Cross-platform username/email profiling |
| CheckUsernames | https://checkusernames.com/ | Checks username availability across 160+ social networks |
| EagleEye | https://github.com/ThoughtfulDev/EagleEye | Reverse image search combined with facial recognition for people search |
| EmailRep.io | https://emailrep.io/ | Email reputation scoring with breach history and account age |
| RocketReach | https://rocketreach.co/ | Professional contact finder (email, phone, social profiles) |
| PGP Key Server | https://pgp.key-server.io/ | Search PGP public keys for email addresses and identities |
| Predicta Search | https://www.predictasearch.com | People search and background check aggregation |
| 192.com | https://www.192.com/people/search/ | UK-focused people, business, and address lookup |
| Whoxy | https://www.whoxy.com/ | WHOIS history and reverse WHOIS by owner name/email |
| IntelTechniques | https://inteltechniques.com/ | Michael Bazzell's comprehensive OSINT search tools and methodology |

### B. Domain, IP & Infrastructure Reconnaissance

| Tool | URL | Description |
|------|-----|-------------|
| Shodan | https://www.shodan.io/ | Internet-wide device/service scanner; indexes open ports, banners, SSL certs, IoT devices |
| Censys | https://censys.io/ | Internet infrastructure search; complements Shodan with certificate and host data |
| SpiderFoot | https://www.spiderfoot.net/ | Automated OSINT recon across 200+ data sources; correlates DNS, WHOIS, social, breaches |
| Maltego | https://www.maltego.com/ | Link analysis platform; visualizes relationships between entities (people, domains, IPs, orgs) |
| VirusTotal | https://www.virustotal.com/ | Multi-engine scanner for files, URLs, domains, IPs; community intelligence |
| SecurityTrails | https://securitytrails.com/ | Historical DNS data, WHOIS, subdomains, associated IPs |
| WhoisXMLAPI | https://whoisfreaks.com/ | WHOIS, reverse WHOIS, DNS, subdomain, IP geolocation APIs |
| Netlas | https://netlas.io/ | Internet-wide scanning and attack surface discovery |
| DNSdumpster | https://dnsdumpster.com/ | Free domain research; DNS recon and mapping |
| crt.sh | https://crt.sh/ | Certificate Transparency log search; discover subdomains via SSL certs |
| Synapsint | https://www.synapsint.com/ | Unified OSINT search across multiple intelligence categories |
| SARENKA | https://github.com/KTZgraph/sarenka | Aggregates Shodan, Censys, and other service data in one interface |

### C. Social Media Intelligence (SOCMINT)

| Tool | URL | Description |
|------|-----|-------------|
| Maltego + Social Links | https://www.maltego.com/ | Graph-based social media investigation across 500+ sources |
| Crimewall (Social Links) | https://sociallinks.io/ | Collects data from social media, messaging apps, blockchains, dark web |
| Hunchly | https://www.hunch.ly/ | Automated web capture tool; timestamps and digitally signs every page visited |
| Osintgram | https://github.com/Datalux/Osintgram | Instagram OSINT: followers, stories, hashtags, tagged posts, geolocation |
| Twint (archived) | https://github.com/twintproject/twint | Twitter/X scraping without API; advanced search and export |
| Reddit6 | https://reddit6.com/ | Reddit stream monitoring and analysis |
| Google Alerts | https://www.google.co.uk/alerts | Automated notifications for keyword mentions |
| Warble Alerts | https://warble.co/ | Social media monitoring and alerting |
| Pagefreezer | https://www.pagefreezer.com/ | Social media archiving for legal/compliance investigations |

**Platform-Specific Intelligence Value:**

- **X/Twitter**: Real-time events, public sentiment, OPSEC failures, threat actor communication
- **Facebook**: Personal connections, group memberships, location check-ins, event attendance
- **LinkedIn**: Org charts, employee movements, technology stack clues, corporate targeting
- **Instagram**: Visual evidence, geolocation via tagged photos, lifestyle patterns
- **Telegram**: Threat actor channels, data leak marketplaces, extremist communications
- **TikTok**: Geolocation via video backgrounds, trending disinformation

### D. Email Intelligence

| Tool | URL | Description |
|------|-----|-------------|
| Holehe | https://github.com/megadose/holehe | Checks if email is registered on 120+ services (passive) |
| Epieos | https://tools.epieos.com/ | Email-to-identity resolver; finds Google account info, linked services |
| EmailRep.io | https://emailrep.io/ | Email reputation: breach exposure, account age, deliverability |
| Hunter.io | https://hunter.io/ | Domain email finder; discovers professional email patterns |
| Have I Been Pwned | https://haveibeenpwned.com/ | Breach database search by email address |
| Phonebook.cz | https://phonebook.cz/ | Email, domain, and URL search from breach/intelligence data |
| h8mail | https://github.com/khast3x/h8mail | Email OSINT and breach hunting tool |

### E. Reverse Image Search & Visual Intelligence

| Tool | URL | Description |
|------|-----|-------------|
| Google Lens | https://lens.google.com/ | AI-powered visual search; object/text/landmark identification |
| Yandex Images | https://yandex.com/images/ | Often finds matches other engines miss, especially for faces |
| TinEye | https://tineye.com/ | Reverse image search with date-sorted results; finds earliest appearance |
| PimEyes | https://pimeyes.com/ | Facial recognition search engine across the open web |
| Bing Visual Search | https://www.bing.com/images/ | Microsoft's reverse image search with OCR and entity recognition |
| ExifTool | https://exiftool.org/ | Metadata extraction: GPS coordinates, camera model, timestamps, software |
| EXIF Data Online | https://exifdata.com/ | Browser-based EXIF metadata viewer |
| Pixsy | https://www.pixsy.com/ | Image theft detection and monitoring |
| FotoForensics | https://fotoforensics.com/ | Error Level Analysis (ELA) for detecting image manipulation |
| DupliChecker | https://www.duplichecker.com/reverse-image-search.php | Multi-engine reverse image search |

**Techniques:**

- Always check EXIF data first (GPS coords, camera serial, editing software)
- Yandex outperforms Google for facial recognition searches
- Use TinEye to find the oldest instance of an image online
- FotoForensics ELA reveals spliced/edited regions in photos
- Combine reverse image search with geolocation (Google Earth, Street View) for verification

### F. Geolocation & Geospatial Intelligence (GEOINT)

| Tool | URL | Description |
|------|-----|-------------|
| Google Earth Pro | https://earth.google.com/ | Historical satellite imagery, 3D terrain, measurement tools |
| Google Street View | https://www.google.com/maps/ | Ground-level imagery for visual verification |
| Bing Aerial Maps | https://www.bing.com/maps/aerial | High-res aerial/bird's-eye imagery |
| OpenStreetMap | https://www.openstreetmap.org/ | Community-maintained map data; infrastructure details missing from commercial maps |
| Snap Map | https://map.snapchat.com/ | Real-time geotagged Snapchat stories |
| FlightRadar24 | https://www.flightradar24.com/ | Real-time global flight tracking |
| ADSB Exchange | https://globe.adsbexchange.com/ | Unfiltered ADS-B flight data (includes military/gov aircraft) |
| MarineTraffic | https://www.marinetraffic.com/ | Real-time ship tracking via AIS data |
| LiveUAMap | https://liveuamap.com/ | Conflict and crisis mapping |
| Windy | https://www.windy.com/ | Weather, wind patterns, webcams; useful for temporal verification |
| MeteoBlue | https://www.meteoblue.com/ | Historical weather data for timestamp verification |
| SunCalc | https://www.suncalc.org/ | Sun position calculator; verify photo timestamps by shadow analysis |
| Sentinel Hub | https://www.sentinel-hub.com/ | Copernicus satellite imagery; free multispectral data |
| Radio.Garden | http://radio.garden/ | Global radio stations by location; cultural/linguistic verification |
| Freedar | https://radar.freedar.uk/ | UK-focused flight radar |

**Geolocation Methodology:**

1. Extract EXIF metadata for embedded GPS coordinates
2. Identify visual clues: language on signs, vegetation type, road markings, architecture style, sun position
3. Cross-reference with satellite imagery (Google Earth historical view)
4. Verify with Street View for ground-level confirmation
5. Use weather/sun data to confirm timestamps

### G. Dark Web & Underground Intelligence

| Tool | URL | Description |
|------|-----|-------------|
| Tor Browser | https://www.torproject.org/ | Primary gateway to .onion sites |
| Ahmia | https://ahmia.fi/ | Surface-web-accessible .onion site search engine |
| Haystak | (onion service) | Large-scale dark web search engine |
| Torch | (onion service) | One of the oldest dark web search engines |
| OnionScan | https://github.com/s-rah/onionscan | Scans .onion sites for security misconfigurations and deanonymization vectors |
| TorBot | https://github.com/DedSecInside/TorBot | Automated dark web crawler and scraper |
| TorCrawl.py | https://github.com/MikeMeliz/TorCrawl.py | Python-based .onion site crawler for bulk data collection |
| DeepDarkCTI | https://github.com/fastfire/deepdarkCTI | Dark web threat intelligence collection for CTI/SOC teams |
| DarkSearch | https://darksearch.io/ | Dark web search engine with API access |
| IntelligenceX | https://intelx.io/ | Search engine for leaked data, dark web, and historical content |

**Safety Requirements for Dark Web OSINT:**

- Always use a dedicated VM (never your host OS)
- Route all traffic through Tor (or Tor-over-VPN for additional layer)
- Use a non-attributable identity; never log into personal accounts
- Disable JavaScript in Tor Browser (Security Level: Safest)
- Never download files directly to your investigation machine
- Document everything with screenshots and hashes

### H. Frameworks & Aggregation Platforms

| Tool | URL | Description |
|------|-----|-------------|
| OSINT Framework | https://osintframework.com/ | Web-based directory organizing hundreds of tools by investigation type |
| SpiderFoot | https://www.spiderfoot.net/ | Automated recon across 200+ sources with correlation engine |
| Maltego | https://www.maltego.com/ | Visual link analysis with hundreds of data source transforms |
| Recon-ng | https://github.com/lanmaster53/recon-ng | Modular web reconnaissance framework (Python) |
| theHarvester | https://github.com/laramies/theHarvester | Gathers emails, subdomains, hosts, IPs from public sources |
| PhoneInfoga | https://github.com/sundowndev/phoneinfoga | Phone number OSINT framework (carrier, country, line type, linked accounts) |
| X-OSINT | https://github.com/TermuxHackz/X-osint | Multi-target OSINT (phone, email, IP) |
| Photon | https://github.com/s0md3v/Photon | Fast web crawler that extracts URLs, emails, social accounts, files |
| Trace (1TRACE) | https://www.1trace.io/ | Enterprise platform combining social, geospatial, cyber, and financial OSINT |
| Lampyre | https://lampyre.io/ | Multi-source intelligence platform with real-time data fusion |
| OSINT Yoga | https://yoga.osint.ninja/ | Curated OSINT tool selector |
| Awesome OSINT | https://github.com/jivoi/awesome-osint | Massive curated GitHub list of OSINT tools and resources |
| OSINT-BIBLE | https://github.com/frangelbarrera/OSINT-BIBLE | Comprehensive 2026 guide to OSINT tools, methodologies, ethics |
| Bellingcat Toolset | [Google Sheets](https://docs.google.com/spreadsheets/d/18rtqh8EG2q1xBo2cLNyhIDuK9jrPGwYr9DI2UncoqJQ/) | Bellingcat's curated investigation toolkit spreadsheet |

### I. Blockchain & Cryptocurrency Intelligence

| Tool | URL | Description |
|------|-----|-------------|
| Chainalysis | https://chainalysis.com/ | Enterprise blockchain analysis and transaction tracing |
| Elliptic | https://www.elliptic.co/ | Crypto compliance and forensics |
| Wallet Explorer | https://www.walletexplorer.com/ | Bitcoin wallet clustering and transaction graph |
| Blockchain.com Explorer | https://blockchain.com | Bitcoin/Ethereum transaction lookup |
| Check Bitcoin Address | https://checkbitcoinaddress.com/ | Check if a BTC address is linked to scams or darknet markets |
| Scorechain | https://scorechain.com/ | Multi-crypto analytics and AML compliance |

---

## 3. BushidoUK Repo Highlights

**Repository:** [BushidoUK/Open-source-tools-for-CTI](https://github.com/BushidoUK/Open-source-tools-for-CTI)
**Maintainer:** BushidoToken (https://bushidotoken.net, @BushidoToken on X)
**Stats:** 804+ stars, 139+ forks

### What Makes It Valuable

This repository is one of the most well-organized, CTI-analyst-focused collections on GitHub. Unlike generic OSINT lists, it is structured around the three tiers of intelligence (strategic, operational, tactical) plus auxiliary enablement, making it immediately practical for working analysts.

### Repository Structure

**Strategic Intelligence Resources:**

- CTI Fundamentals (links to curated-intel/CTI-fundamentals)
- Adversary Intelligence -- threat actor profiles and tracking
- Ransomware Intelligence -- gang tracking, ransom leak sites, decryptor availability
- Monthly CTI Reports -- recurring publications from major vendors
- CTI Reporting -- structured writing guidance (STIX, MITRE ATT&CK mapping)

**Operational Intelligence Resources:**

- Data Breaches -- breach notification trackers and databases
- Security News -- curated news aggregators and feeds
- Collections -- meta-lists and resource compilations
- CERTs -- national/regional Computer Emergency Response Teams
- Vulnerabilities -- CVE databases, exploit trackers, patch intelligence
- Darknet -- marketplace monitoring, forum tracking
- ICS/OT Threat Intel -- industrial control system specific threat data
- Mobile Threat Intel -- mobile malware, rogue app tracking
- Threat Hunting -- hypothesis-driven proactive detection resources

**Tactical Intelligence Resources:**

- Anti-Phishing Tools -- URL scanners, domain squatting detection
- Website Security -- SSL analysis, technology fingerprinting
- Search Engine Tools -- Google dorking, Shodan, Censys guides
- OSINT Investigation Tools -- the most comprehensive file; 74+ tools across people search, image analysis, geolocation, blockchain, and username enumeration
- Malware Analysis Tools -- sandboxes, disassemblers, behavioral analysis
- IOC Feeds -- free and commercial indicator feeds (AlienVault OTX, Abuse.ch, etc.)
- Network IOC Vetting -- tools to validate whether an IP/domain/hash is malicious

**Auxiliary CTI Enablement:**

- VPN and Private Browsing -- ProtonVPN, Mullvad, Tor configurations
- Virtual Machines -- pre-built OSINT VMs, isolation guidance
- Secure Email -- ProtonMail, Tutanota for investigation accounts
- Chrome Extensions -- Wappalyzer, Shodan browser plugin, BuiltWith
- GitHub Projects -- notable security/CTI repos
- Honeypots -- deception technology for threat data collection
- OPSEC Essentials -- operational security for analysts
- CTI Certifications -- SANS GCTI, CPTIA, EC-Council CTIA
- Training -- courses, labs, and skill development paths

**Community Resources:**

- InfoSec Twitter accounts to follow
- Podcasts (Darknet Diaries, Malicious Life, SANS Internet Stormcast)
- Conferences (DEF CON, Black Hat, BSides, SANS CTI Summit)
- YouTube Channels -- security education content creators
- OSINT Search Operators sub-repo (https://github.com/BushidoUK/OSINT-SearchOperators)

### Key Contributors

n14, @olihough86, @JCyberSec_, @Rag_Sec, @BufferOfStyx, @CybersecStu, @ScottMcGready, @TJ_Null, @ZephrFish

---

## 4. OSINT Workstation Setup

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4 GB | 16 GB+ |
| CPU | 2 cores | 4+ cores (VT-x/AMD-V enabled) |
| Storage | 30 GB | 100 GB+ SSD |
| Network | Wired ethernet preferred | Dual NIC (one for VPN/Tor, one for clearnet research) |
| Display | Single monitor | Dual monitors (one for research, one for documentation) |

### Virtualization Platform

Choose one:

- **VirtualBox** (free, cross-platform) -- https://www.virtualbox.org/
- **VMware Workstation Player** (free for personal use) -- https://www.vmware.com/
- **Hyper-V** (built into Windows Pro/Enterprise)

### Pre-Built OSINT Virtual Machines

1. **Trace Labs OSINT VM** (tl-osint-2025.12)
   - URL: https://github.com/tracelabs/tlosint-vm
   - Based on Kali Linux; pre-installed with OSINT tools
   - Latest release shifted to GitHub as primary distribution
   - Includes Metagoofil, SpiderFoot, Maltego, and browser extensions

2. **CSI Linux**
   - URL: https://csilinux.com/
   - Purpose-built for cyber investigations
   - Includes forensic, OSINT, and dark web investigation tools

3. **Tsurugi Linux**
   - URL: https://tsurugi-linux.org/
   - DFIR-focused but includes strong OSINT toolkit

4. **Buscador** (by Michael Bazzell, now retired)
   - Historical reference; concepts folded into IntelTechniques VM guides

### Building Your Own OSINT VM from Scratch

**Option A: Argos Script (recommended for Ubuntu)**

- URL: https://github.com/SOsintOps/Argos
- Automatically configures an OSINT workstation from a clean Ubuntu 24.04 LTS VM
- Installs and configures dozens of OSINT tools with one command

**Option B: Manual Setup on Ubuntu/Kali**

1. Install base OS (Ubuntu 24.04 LTS or Kali 2025.x)
2. Update the system:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   ```
3. Install core tools:
   ```bash
   sudo apt install -y tor torbrowser-launcher python3-pip git curl wget
   pip3 install maigret holehe phoneinfoga sherlock h8mail
   ```
4. Install browsers: Firefox (primary), Chromium (secondary), Tor Browser
5. Install browser extensions: Wappalyzer, BuiltWith, Wayback Machine, User-Agent Switcher
6. Install Maltego CE (Community Edition)
7. Install SpiderFoot:
   ```bash
   pip3 install spiderfoot
   ```
8. Configure VPN (ProtonVPN, Mullvad, or IVPN)
9. Snapshot the VM as your clean baseline

### OPSEC Configuration Checklist

- [ ] Never use personal accounts inside the OSINT VM
- [ ] Create dedicated "sock puppet" accounts for platforms requiring login
- [ ] Route all traffic through VPN (and optionally Tor for sensitive research)
- [ ] Disable WebRTC in browsers (prevents IP leakage)
- [ ] Use DNS-over-HTTPS or DNS-over-TLS
- [ ] Disable geolocation services in the VM
- [ ] Clear cookies and browser storage between investigations
- [ ] Rebuild the VM every 2-3 months (start from clean snapshot)
- [ ] Use a password manager with unique credentials per sock puppet
- [ ] Document your methodology for legal defensibility

---

## 5. Methodology: The OSINT Intelligence Cycle

### Phase 1: Planning & Requirements Definition

Before touching any tool, define:

- **Intelligence question**: What specifically do you need to find out?
- **Scope**: What entities are in scope (people, domains, IPs, organizations)?
- **Constraints**: Legal jurisdiction, time limits, acceptable risk level
- **Output format**: Who is the consumer? What format do they need?
- **Collection plan**: Which sources and tools will you use?

### Phase 2: Collection

Gather raw data from identified sources. Key principles:

- Start broad, then narrow (funnel approach)
- Begin with passive techniques before considering active ones
- Document every source URL, access timestamp, and tool used
- Capture screenshots and archive pages (Wayback Machine, archive.today)
- Use multiple independent sources for each data point

**Collection workflow:**

```
Target identifier (email/username/domain/IP/name)
    |
    +---> Username enumeration (Maigret, WhatsMyName)
    +---> Email intelligence (Holehe, Epieos, HIBP)
    +---> Domain/IP recon (Shodan, Censys, SecurityTrails)
    +---> Social media (platform-specific searches, Maltego)
    +---> Image/visual (reverse image search, EXIF extraction)
    +---> Public records (corporate filings, court records, property)
    +---> Dark web (Ahmia, IntelligenceX)
```

### Phase 3: Processing

Transform raw data into a usable format:

- Deduplicate entries
- Normalize data formats (dates, names, addresses)
- Translate foreign-language content
- Extract structured data from unstructured sources
- Tag and categorize findings

### Phase 4: Analysis

This is where intelligence is created from information:

- **Link analysis**: Map relationships between entities (Maltego graph)
- **Timeline analysis**: Reconstruct chronological sequence of events
- **Pattern analysis**: Identify behavioral patterns, operational schedules
- **Gap analysis**: Identify what is still unknown and requires additional collection
- **Confidence assessment**: Rate each finding (confirmed, probable, possible, doubtful)
- **Hypothesis testing**: Formulate theories and actively seek disconfirming evidence

### Phase 5: Dissemination

Produce the intelligence product:

- Tailor format to the audience (executive brief vs. technical report)
- Include sourcing and confidence levels for all claims
- Clearly separate facts from analyst assessments
- Use TLP (Traffic Light Protocol) for classification
- Provide actionable recommendations

### Phase 6: Feedback

- Collect consumer feedback on the product's usefulness
- Identify gaps that require additional collection cycles
- Refine future requirements based on lessons learned

---

## 6. Practice: CTFs, Challenges & Training

### CTF Platforms

| Platform | URL | Description |
|----------|-----|-------------|
| Trace Labs Search Party CTF | https://www.tracelabs.org/initiatives/search-party | Real-world missing persons OSINT; 4-person teams; monthly virtual events. Nov 2025 had 73 teams submitting 3,617 intelligence items. Next: DefCamp 2026 (Nov 29). |
| OSINT Industries CTF | https://ctf.osint.industries/ | Scenario-based OSINT challenges; weekly drops; progressive difficulty; public leaderboard |
| Trace Labs Weekly Challenges | https://docs.tracelabs.org/osint-challenges/osint-challenges-intro | Write-ups and sanitized prompts for self-paced practice |
| CTFtime OSINT Events | https://ctftime.org/ | Aggregator listing OSINT-tagged CTF competitions worldwide |
| GeoGuessr | https://www.geoguessr.com/ | Geolocation skill training using Street View imagery |
| Quiztime | (X/Twitter community) | Daily geolocation and visual OSINT challenges posted by researchers |
| CyberDefenders | https://cyberdefenders.org/ | Blue team CTF labs including OSINT scenarios |

### Training Courses & Resources

| Resource | URL | Description |
|----------|-----|-------------|
| SANS SEC497 (OSINT Gathering & Analysis) | https://www.sans.org/ | Gold-standard OSINT training; leads to GOSI certification |
| IntelTechniques Training | https://inteltechniques.com/ | Michael Bazzell's courses on OSINT methodology and tools |
| Trace Labs Webinars | https://www.tracelabs.org/ | Free webinars on OSINT operations and CTF preparation |
| MyOSINT.Training | https://www.myosint.training/ | Course: "Creating an OSINT Investigation Platform" |
| TCM Security OSINT Course | https://tcm-sec.com/ | Affordable practical OSINT fundamentals |
| Bellingcat Online Investigation Toolkit | https://www.bellingcat.com/ | Investigation methodology from the leading OSINT journalism organization |
| OSINT Curious Project | https://osintcurio.us/ | Community blog, webcasts, and tool tutorials |
| 30 Days of OSINT | https://publication.osintambition.org/ | Structured 30-day self-paced OSINT learning path |

### Certifications

| Certification | Issuer | Focus |
|---------------|--------|-------|
| GOSI (GIAC OSINT) | SANS/GIAC | OSINT gathering and analysis methodology |
| GCTI (GIAC CTI) | SANS/GIAC | Cyber threat intelligence analysis |
| CTIA (Certified Threat Intelligence Analyst) | EC-Council | CTI lifecycle and frameworks |
| CPTIA | Certified | CTI professional practices |

### Practice Recommendations for Beginners

1. Start with GeoGuessr and Quiztime for geolocation fundamentals
2. Complete the Trace Labs weekly challenges with write-ups
3. Join a Trace Labs Search Party CTF (real humanitarian impact)
4. Work through OSINT Industries CTF scenarios
5. Set up your own VM and practice the full intelligence cycle against a fictional target
6. Follow the 30 Days of OSINT curriculum
7. Join OSINT communities: OSINT Curious Discord, Trace Labs Slack, r/OSINT

---

## 7. Legal and Ethical Guidelines

### Is OSINT Legal?

OSINT is legal when it relies exclusively on publicly available information accessed without bypassing any security measures. However, "legal" varies dramatically by jurisdiction, and legality does not equal ethical permissibility.

### Key Legal Frameworks

| Regulation | Jurisdiction | Impact on OSINT |
|------------|-------------|-----------------|
| GDPR | EU/EEA | Processing personal data (even public) requires lawful basis; right to erasure applies |
| CCPA/CPRA | California, USA | Consumer data rights; opt-out requirements for data collection |
| LGPD | Brazil | Similar to GDPR; consent or legitimate interest required |
| PIPL | China | Strict personal information processing rules |
| CFAA | USA (Federal) | Unauthorized computer access; active OSINT techniques risk violation |
| CMA 1990 | UK | Computer Misuse Act; unauthorized access offenses |
| RIPA | UK | Regulation of Investigatory Powers; governs surveillance by public authorities |

**There is no single international OSINT law.** Analysts must understand the laws of both their jurisdiction AND the target's jurisdiction.

### What is Always Illegal (Regardless of Jurisdiction)

- Accessing systems without authorization (hacking, credential stuffing)
- Bypassing access controls (even if data "should be" public)
- Intercepting private communications
- Identity theft or impersonation of law enforcement
- Stalking, harassment, or intimidation using collected data
- Purchasing stolen data (even for research purposes)

### Ethical Principles for OSINT Practitioners

1. **Necessity & Proportionality**: Collect only what is needed for a documented, legitimate purpose. Do not mass-harvest data "just in case."

2. **Minimize Harm**: Consider the potential impact on subjects. Public availability does not eliminate privacy concerns. A person's old forum post being public does not make it ethical to weaponize.

3. **Passive First**: Always prefer passive collection. Active techniques (contacting the subject, creating fake accounts) require additional justification.

4. **Data Minimization**: Collect the minimum data necessary. Destroy data that is not relevant to the intelligence requirement.

5. **Accuracy**: Verify findings through multiple independent sources. Never present unverified data as confirmed intelligence. Clearly label confidence levels.

6. **Transparency of Method**: Maintain detailed records of methodology: timestamp of access, exact URL/source, screenshot of data, date of analysis, tools used, and conclusions drawn. This chain of custody proves the investigation was conducted legally and ethically.

7. **Secure Storage**: Collected intelligence (especially PII) must be stored securely with appropriate access controls and retention limits.

8. **No Vigilantism**: OSINT findings should be reported through proper channels (law enforcement, organizational leadership), never acted upon independently.

### Best Practices Checklist

- [ ] Document your intelligence requirement before beginning collection
- [ ] Verify you have lawful basis for the investigation
- [ ] Use the minimum-invasive technique that achieves the goal
- [ ] Screenshot and timestamp all evidence at time of collection
- [ ] Store personal data encrypted with defined retention periods
- [ ] Do not access authenticated/private content without authorization
- [ ] Consider the subject's reasonable expectation of privacy
- [ ] Report findings through proper channels only
- [ ] Destroy collected data when the intelligence requirement is fulfilled
- [ ] Maintain an audit trail of all investigative actions

---

## Sources

- [BushidoUK/Open-source-tools-for-CTI](https://github.com/BushidoUK/Open-source-tools-for-CTI)
- [ShadowDragon: Best OSINT Tools 2026](https://shadowdragon.io/blog/best-osint-tools/)
- [OSINT-BIBLE on GitHub](https://github.com/frangelbarrera/OSINT-BIBLE)
- [Cyble: Top 15 OSINT Tools 2026](https://cyble.com/knowledge-hub/top-15-osint-tools-for-powerful-intelligence-gathering/)
- [Lampyre: 15 Best OSINT Tools](https://lampyre.io/blog/15-best-osint-tools-in-2025/)
- [Technology.org: Top 10 OSINT Software 2026](https://www.technology.org/2026/04/29/the-top-10-osint-software-tools-for-research-and-investigation-2026/)
- [Wiz: OSINT Tools Evaluation](https://www.wiz.io/academy/threat-intel/osint-tools)
- [WebAsha: OSINT VM Setup Guide](https://www.webasha.com/blog/step-by-step-guide-to-configuring-an-osint-virtual-machine-on-ubuntu-secure-and-efficient-intelligence-gathering-setup)
- [Dr Zee's OSINT: VMs](https://drzeesinvestigations.com/2025/10/osint-and-virtual-machines/)
- [SpecialEurasia: OSINT Virtualisation](https://www.specialeurasia.com/2026/04/16/osint-virtualisation-tracelabs/)
- [Argos OSINT Workstation Script](https://github.com/SOsintOps/Argos)
- [Trace Labs](https://www.tracelabs.org/)
- [OSINT Industries CTF](https://ctf.osint.industries/)
- [awesome-osint](https://github.com/jivoi/awesome-osint)
- [Proelium Law: OSINT Compliance](https://proeliumlaw.com/open-source-intelligence-and-privacy/)
- [Altia Intel: OSINT Ethics](https://altiaintel.us/osint-investigation-ethics-legal-boundaries/)
- [EspectroSINT: Is OSINT Legal? (2026)](https://www.espectrosint.com/blog/is-osint-legal)
- [HENSOLDT: Ethics in OSINT](https://www.hensoldt.net/news/ethics-in-osint-is-open-source-intelligence-legal)
- [Neotas: Open Source Investigation Best Practices](https://www.neotas.com/open-source-investigation-best-practices/)
- [Recorded Future: OSINT Framework Explained](https://www.recordedfuture.com/threat-intelligence-101/intelligence-sources-collection/osint-framework)
- [BitSight: OSINT Framework Guide 2026](https://www.bitsight.com/learn/cti/osint-framework)
- [OSINTBench: Domain & IP Investigation Guide](https://osintbench.com/guides/domain-ip-osint/)
- [OSINTBench: Social Media OSINT Guide](https://osintbench.com/guides/social-media-osint/)
- [OSINT Industries](https://www.osint.industries/)
- [Epieos](https://epieos.com/)
- [The-Osint-Toolbox: Email-Username-OSINT](https://github.com/The-Osint-Toolbox/Email-Username-OSINT)
- [dark-web-osint-tools](https://github.com/apurvsinghgautam/dark-web-osint-tools)
- [Brandefense: OSINT Tools for Dark Web](https://brandefense.io/blog/dark-web/top-open-source-intelligence-osint-tools-for-dark-web/)
- [The-Osint-Toolbox: Image-Research-OSINT](https://github.com/The-Osint-Toolbox/Image-Research-OSINT)
- [Social-Media-OSINT-Tools-Collection](https://github.com/osintambition/Social-Media-OSINT-Tools-Collection)
