# THE GLOBAL DISPATCH — Tuesday, 24 November 2026 (`news-image-20261124`)

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ardimakefun/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ardimakefun/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

Newspaper digest for [`news-image-20261124`](https://make.fun/bounty/news-image-20261124).

## Overview

`entry.png` is a **1024×1024** broadsheet newspaper digest summarizing **13 verified world news stories** from **Tuesday, 24 November 2026**, rendered deterministically from scratch in Python 3.13 (`main.py`, using `Pillow` and Python stdlib at 2× supersampling downsampled with `LANCZOS`).

## Visual & Editorial Structure

1. **Masthead (`THE GLOBAL DISPATCH`)** — Edition tag (`2026-11-24`), publication date (`TUESDAY, 24 NOV 2026`), and total count (`13 VERIFIED STORIES`).
2. **Region Strip (`13`) & Fields Diversity Bar (`13`)**:
   - **Regions:** N. America (2), Lat. Am (1), Europe (2), Mid. East (2), Africa (1), Asia (3), Global (2) — **Total = 13**.
   - **Fields:** Security & Conflict (3), Law & Justice (2), Markets & Energy (2), Politics & Diplomacy (2), Space & Science (2), Society & Sports (2) — **Total = 13**.
3. **Key Numbers Strip (`6` figures, all sourced on-page):** `10 / 12` (Huawei guilty counts), `13 NMI` (Russian jets off Ulleungdo), `$91.40` (Brent crude settle), `40+` (Zaporizhzhia wounded), `47,000` (2025 kin femicides, UNODC), `-5.86%` (Nvidia Tuesday close at `$155.38`).
4. **Front Page Leads (`3` illustrated dispatches):**
   - `#01` Huawei convicted on 10 of 12 federal counts in Brooklyn (acquitted on RICO & obstruction).
   - `#02` South Korea scrambles F-15Ks & issues Ulleungdo air-raid alert over 4 Russian warplanes; summons Russian attaché.
   - `#03` Brent crude rebounds +2.27% to `$91.40/bbl` amid Strait of Hormuz risks and unverified IRGC tanker-mine claims.
5. **World Desk Secondary Grid (`4`):** Zaporizhzhia strike (`#04`), CAS Senegal AFCON reinstatement (`#05`), Sarkozy & Bruni trial order (`#06`), Sheikh Hasina 16 Dec return / Dhaka extradition demand (`#07`).
6. **World Coverage Map (`11 Land Pins + 2 Global = 13`) + Also Today (`3`):** Programmatically verified continent polygons ensuring all 11 geographic pins fall strictly on landmass, paired with briefs on Progress MS-36 (`#08`), Gaza City (`#09`), and Colombia's 10th-anniversary peace accord (`#10`).
7. **Wire Ticker (`3`) + The Day in UTC + Date Check Footer:** UNODC 47,000 femicides (`#11`), Nvidia -5.86% / Huang apology (`#12`), Beaver Supermoon at `14:53 UTC` (`#13`), verified UTC timeline, explicit cross-day caveats, and wire source list.

## Reproducing `entry.png`

```bash
python main.py
```

Running `main.py` deterministically regenerates `entry.png` (1024×1024 PNG) using Python 3.13 + Pillow and Windows system fonts.

## Files in Deliverables

- `entry.png` — Final 1024×1024 newspaper summary image.
- `main.py` — Original Python 3.13 rendering script written in this session.
- `research-24-nov.md` — Numbered, source-backed verification dossier with explicit date-disambiguation & uncertainty notes.
- `README.md` — This draft summary (ready for Babu's review and badge additions).
