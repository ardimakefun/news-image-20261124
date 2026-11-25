"""
Generate entry.png (1024x1024) — THE GLOBAL DISPATCH for Tuesday, 24 November 2026.

Written from scratch in Python 3.13 (stdlib + Pillow) for make.fun bounty
news-image-20261124. Renders at 2x supersampled resolution (2048x2048) and
downsamples with LANCZOS for crisp typography, vector illustrations, and map pins.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Sequence

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Canvas & Supersampling Configuration
# ---------------------------------------------------------------------------
FINAL_SIZE = 1024
SCALE = 2
W = FINAL_SIZE * SCALE
H = FINAL_SIZE * SCALE

# Editorial Archival Broadsheet Palette
BG_PAPER = (244, 239, 228)       # Warm archival newsprint
BG_CARD = (252, 250, 245)        # Crisp ivory card surface
BG_CARD_ALT = (247, 243, 234)    # Secondary tint
BG_DARK = (17, 22, 31)           # Deep ink navy-charcoal
BG_SLATE = (28, 36, 50)          # Slate panel background
INK_PRIMARY = (16, 20, 27)       # Primary headline/body ink
INK_SECONDARY = (52, 62, 78)     # Subhead / body copy
INK_MUTED = (90, 101, 117)       # Metadata / labels
RULE_DARK = (26, 32, 44)         # Heavy structural rules
RULE_LIGHT = (204, 196, 180)     # Hairline dividers
WHITE = (255, 255, 255)
GOLD_ACCENT = (218, 165, 32)
CREAM_TEXT = (243, 237, 224)

# Region Colors (High contrast, saturated jewel tones)
REGION_COLORS: dict[str, tuple[int, int, int]] = {
    "N. AMERICA": (29, 78, 216),     # Royal Blue
    "LAT. AM": (4, 120, 87),         # Emerald
    "EUROPE": (67, 56, 202),         # Indigo
    "MID. EAST": (185, 28, 28),      # Crimson
    "AFRICA": (180, 83, 9),          # Amber Ochre
    "ASIA": (15, 118, 110),          # Deep Teal
    "GLOBAL": (109, 40, 217),        # Violet
}

# Field Colors
FIELD_COLORS: dict[str, tuple[int, int, int]] = {
    "SECURITY & CONFLICT": (185, 28, 28),
    "LAW & JUSTICE": (67, 56, 202),
    "MARKETS & ENERGY": (180, 83, 9),
    "POLITICS & DIPLOMACY": (15, 118, 110),
    "SPACE & SCIENCE": (29, 78, 216),
    "SOCIETY & SPORTS": (4, 120, 87),
}


def s(v: float) -> int:
    """Scale a logical 1024-px coordinate to the 2x supersampled canvas."""
    return int(round(v * SCALE))


def pt(v: float) -> int:
    """Scale a font size to the 2x supersampled canvas."""
    return max(8, int(round(v * SCALE)))


def load_font(candidates: Sequence[str], size: float) -> ImageFont.FreeTypeFont:
    """Load the first available TrueType font from Windows Fonts or fallback."""
    font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for name in candidates:
        path = os.path.join(font_dir, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, pt(size))
    return ImageFont.load_default()


# Pre-configured Font Families
FONT_SERIF_BOLD = ("georgiab.ttf", "timesbd.ttf", "GARABD.TTF", "arialbd.ttf")
FONT_SERIF_REG = ("georgia.ttf", "times.ttf", "GARA.TTF", "arial.ttf")
FONT_SANS_BOLD = ("segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "tahomabd.ttf")
FONT_SANS_SEMI = ("seguisb.ttf", "segoeuib.ttf", "arialbd.ttf")
FONT_SANS_REG = ("segoeui.ttf", "arial.ttf", "calibri.ttf")
FONT_MONO_BOLD = ("consolab.ttf", "CascadiaMono.ttf", "courbd.ttf")


# ---------------------------------------------------------------------------
# Verified Data Model (13 Stories = 3 Lead + 4 Sec + 3 Also + 3 Ticker)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Story:
    num: str
    tier: str
    region: str
    field: str
    headline: str
    summary: str
    location: str
    source: str
    verified_tag: str
    lat: float | None = None
    lon: float | None = None
    pin_code: str = ""


STORIES: tuple[Story, ...] = (
    # --- 3 LEADS ---
    Story(
        num="01",
        tier="LEAD",
        region="N. AMERICA",
        field="LAW & JUSTICE",
        headline="Huawei Convicted on 10 of 12 Federal Counts in N.Y.",
        summary=(
            "A Brooklyn federal jury found Huawei and 3 units guilty on 10 counts — "
            "trade-secret conspiracy, bank/wire fraud, money laundering & Iran sanctions "
            "breaches — while acquitting on 2 counts (RICO & obstruction). "
            "Judge Ann Donnelly set sentencing for 14 Sep 2027."
        ),
        location="Brooklyn, NY",
        source="DOJ / AP",
        verified_tag="VERIFIED",
        lat=40.70,
        lon=-74.60,
        pin_code="NY",
    ),
    Story(
        num="02",
        tier="LEAD",
        region="ASIA",
        field="SECURITY & CONFLICT",
        headline="S. Korea Scrambles F-15Ks Over 4 Russian Warplanes",
        summary=(
            "2 Tu-160 bombers and 2 Su-35 jets entered KADIZ, closing to 13 nmi "
            "(~24 km) off Ulleungdo at 07:52 KST (22:52Z Nov 23) and triggering a "
            "brief air-raid alert before turning east. Seoul later summoned "
            "Russian attache N. Marchenko in formal protest."
        ),
        location="Seoul / Ulleungdo",
        source="Al Jazeera / Chosun",
        verified_tag="VERIFIED",
        lat=37.45,
        lon=127.40,
        pin_code="SEL",
    ),
    Story(
        num="03",
        tier="LEAD",
        region="MID. EAST",
        field="MARKETS & ENERGY",
        headline="Brent Crude Rebounds to $91.40 Amid Hormuz Risks",
        summary=(
            "Brent futures bounced off 3-month lows ($88.10 trough) to settle "
            "+2.27% at $91.40/bbl as Strait of Hormuz tensions flared. Iran's IRGC "
            "claimed naval mines hit 3 oil tankers (unverified by Reuters); "
            "UKMTO reported 3 ships hit on 23 Nov."
        ),
        location="Strait of Hormuz",
        source="Reuters / AA*",
        verified_tag="VERIFIED",
        lat=27.25,
        lon=56.35,
        pin_code="HRM",
    ),
    # --- 4 SECONDARY GRID ---
    Story(
        num="04",
        tier="SECONDARY",
        region="EUROPE",
        field="SECURITY & CONFLICT",
        headline="Russian Strike on Zaporizhzhia Kills 2, Wounds 40+",
        summary=(
            "Overnight missiles & drones hit homes and apartments; children among "
            "injured. Zelenskyy sends front reinforcements."
        ),
        location="Zaporizhzhia, UKR",
        source="AP / WashPost",
        verified_tag="VERIFIED",
        lat=47.84,
        lon=35.14,
        pin_code="ZAP",
    ),
    Story(
        num="05",
        tier="SECONDARY",
        region="AFRICA",
        field="SOCIETY & SPORTS",
        headline="CAS Reinstates Senegal as 2025 AFCON Champions",
        summary=(
            "Lausanne panel invoked field-of-play rule to reverse CAF's "
            "forfeit, restoring Senegal's 1-0 win."
        ),
        location="Dakar, Senegal",
        source="CAS / Guardian",
        verified_tag="VERIFIED",
        lat=14.70,
        lon=-15.80,
        pin_code="DKR",
    ),
    Story(
        num="06",
        tier="SECONDARY",
        region="EUROPE",
        field="LAW & JUSTICE",
        headline="French Court Orders Sarkozy & Bruni to Stand Trial",
        summary=(
            "Ex-president, Carla Bruni & 9 others (11 total) face Nov 2027 "
            "trial over Libya-case witness tampering."
        ),
        location="Paris, France",
        source="AFP / The Star",
        verified_tag="VERIFIED",
        lat=48.86,
        lon=2.35,
        pin_code="PAR",
    ),
    Story(
        num="07",
        tier="SECONDARY",
        region="ASIA",
        field="POLITICS & DIPLOMACY",
        headline="Hasina Sets Dec 16 Return; Dhaka Seeks Extradition",
        summary=(
            "Ex-PM's camp sought a Biman flight from Delhi; Dhaka refused, "
            "citing her in-absentia death sentence."
        ),
        location="Dhaka, Bangladesh",
        source="Al Jazeera / CNA",
        verified_tag="VERIFIED",
        lat=23.81,
        lon=90.41,
        pin_code="DHK",
    ),
    # --- 3 ALSO TODAY ---
    Story(
        num="08",
        tier="ALSO",
        region="ASIA",
        field="SPACE & SCIENCE",
        headline="Progress MS-36 Launches 2.4t Cargo to ISS (10:17 UTC)",
        summary=(
            "Soyuz-2.1b lifted off from Baikonur carrying 2,427 kg total: "
            "~1,206 kg hardware, 750 kg fuel, 420 kg water & 51 kg gases."
        ),
        location="Baikonur, KAZ",
        source="NASA / Space.com",
        verified_tag="VERIFIED",
        lat=45.96,
        lon=63.31,
        pin_code="BKN",
    ),
    Story(
        num="09",
        tier="ALSO",
        region="MID. EAST",
        field="SECURITY & CONFLICT",
        headline="Israeli Strike Kills Hamas Security Chief in Gaza City",
        summary=(
            "Western Gaza City strike killed Naeem Abu Nahel, head of Hamas's "
            "internal security apparatus; confirmed by Hamas & IDF-Shin Bet."
        ),
        location="Gaza City",
        source="Just Security",
        verified_tag="VERIFIED",
        lat=31.45,
        lon=34.70,
        pin_code="GAZ",
    ),
    Story(
        num="10",
        tier="ALSO",
        region="LAT. AM",
        field="POLITICS & DIPLOMACY",
        headline="UN Chief Marks 10 Years of Colombia Peace Accord",
        summary=(
            "Guterres urged redoubled commitment to reintegration & victims' "
            "rights with 5 years left, warning of ongoing violence (23 Nov blasts)."
        ),
        location="Bogota, Colombia",
        source="UN News / AA",
        verified_tag="VERIFIED",
        lat=4.71,
        lon=-74.07,
        pin_code="BOG",
    ),
    # --- 3 TICKER ---
    Story(
        num="11",
        tier="TICKER",
        region="GLOBAL",
        field="SOCIETY & SPORTS",
        headline="UNODC: 47,000 Women & Girls Killed by Kin in 2025",
        summary="Avg. 5/hr by partners or family (60% of ~78k cases).",
        location="Global",
        source="UNODC / UN",
        verified_tag="VERIFIED",
    ),
    Story(
        num="12",
        tier="TICKER",
        region="N. AMERICA",
        field="MARKETS & ENERGY",
        headline="Nvidia Slides 5.86% ($155.38) After Huang Apology",
        summary="CEO cited 'terrible mistakes' after Mon (23 Nov) +31.48% jump.",
        location="Santa Clara, CA",
        source="Reuters / Hindu",
        verified_tag="VERIFIED",
        lat=37.35,
        lon=-121.00,
        pin_code="CA",
    ),
    Story(
        num="13",
        tier="TICKER",
        region="GLOBAL",
        field="SPACE & SCIENCE",
        headline="Beaver Supermoon Peaks 14:53 UTC at 360,768 km",
        summary="Full supermoon grazed Pleiades before 14:53 UTC peak.",
        location="Global",
        source="Forbes / Time&Date",
        verified_tag="VERIFIED",
    ),
)


# ---------------------------------------------------------------------------
# Simplified Real-World Continent & Inland Sea Polygons (lon, lat)
# ---------------------------------------------------------------------------
CONTINENTS: list[tuple[str, list[tuple[float, float]]]] = [
    ("North America", [
        (-168, 65), (-162, 70), (-140, 70), (-125, 71), (-95, 73), (-80, 70),
        (-65, 62), (-55, 52), (-60, 46), (-67, 45), (-70, 42), (-73.5, 40.5),
        (-76, 35), (-80, 31), (-80.5, 25), (-82.5, 28), (-84, 30), (-90, 29),
        (-97, 26), (-96, 19), (-90, 21), (-87, 21), (-88, 16), (-83, 14),
        (-83, 9), (-78, 8.5), (-79.5, 9), (-85, 10), (-92, 14.5), (-105, 19),
        (-110, 24), (-117, 32.5), (-122.5, 37.5), (-124.5, 42), (-124, 48),
        (-130, 54), (-140, 59), (-152, 60), (-162, 55), (-166, 60),
    ]),
    ("Greenland", [
        (-52, 60), (-43, 60), (-34, 68), (-20, 74), (-22, 81), (-48, 82),
        (-65, 78), (-56, 70), (-52, 64),
    ]),
    ("Iceland", [(-24, 64), (-14, 64), (-14, 66.5), (-23.5, 66.2)]),
    ("South America", [
        (-78, 9), (-75, 11), (-71, 12), (-62, 10.5), (-50, 1.5), (-35, -5.5),
        (-38, -13), (-40, -21), (-48, -26), (-53, -33.5), (-58, -38), (-65, -43),
        (-68, -52), (-70, -55), (-74, -52), (-74, -42), (-71.5, -33), (-70.5, -20),
        (-77, -12), (-81, -5), (-79.5, 1), (-77.5, 6),
    ]),
    ("UK & Ireland", [
        (-6, 50), (1.7, 51), (1.5, 53), (-1.5, 55.5), (-3, 58.6), (-6, 58),
        (-5.5, 54.5), (-5, 51.5),
    ]),
    ("Europe & Asia", [
        (-9.5, 37), (-9, 43), (-2, 43.5), (-4.5, 48.2), (2, 51), (5, 53),
        (8.5, 54), (8.5, 57), (12, 56), (10.5, 59), (5, 61), (12, 66),
        (20, 70), (30, 71), (42, 67), (58, 69), (70, 73), (95, 76), (115, 74),
        (140, 73), (170, 68), (178, 65), (170, 60), (162, 55), (156, 51),
        (142, 54), (138, 45), (131, 42.5), (129, 38), (129.2, 35.1), (126.2, 35.1),
        (126.3, 37.8), (124, 40), (120, 39), (122, 37), (119.5, 35), (122, 31),
        (120, 26), (114, 22.3), (108.5, 21.5), (109.2, 12), (105, 8.6), (100.5, 13.5),
        (103.8, 1.3), (100, 5), (96.5, 16), (92, 21), (89, 22), (85, 19.5),
        (80.2, 13), (77.5, 8.1), (73, 18), (68.5, 23), (62, 25.2), (57, 25.5),
        (56.5, 27.1), (52, 27.8), (48.5, 30.0), (50.8, 25.4), (55.5, 24.4), (59.5, 22.5),
        (53, 16.5), (45.0, 13.0), (43.5, 12.6), (42.5, 15.5), (40.0, 20.5), (36.2, 27.0),
        (34.6, 29.6), (33.5, 31.2), (35.8, 35.5), (36, 36.8), (27, 37),
        (26.5, 40.5), (29, 41.2), (28, 42.5), (30.5, 46.2), (34, 45), (36.5, 46.8),
        (41.5, 41.6), (36, 41.5), (26, 40), (23.5, 38), (22, 36.5), (19.5, 40),
        (14, 45.5), (16.5, 42.0), (18.2, 40.2), (15.8, 38.0), (14.2, 40.8),
        (12.0, 42.2), (9.5, 44.3), (5, 43.3), (3, 42.4), (-1, 37.5), (-5.5, 36),
    ]),
    ("Sri Lanka", [(79.8, 9.6), (81.8, 7.6), (80.5, 6.0), (79.7, 7.5)]),
    ("Taiwan", [(120.2, 22.0), (121.9, 25.1), (120.9, 24.8), (120.1, 23.0)]),
    ("Japan", [
        (130.5, 31.5), (134, 33.5), (139.8, 35.5), (141.5, 41), (145, 43.5),
        (142, 45), (139.5, 40), (136.5, 37), (131, 34),
    ]),
    ("Philippines", [(120, 18.4), (122.4, 16.5), (126.2, 7.2), (124, 6.2), (120.4, 14)]),
    ("Africa", [
        (-5.8, 35.8), (10, 37), (11.5, 33), (20, 32), (32.3, 31.2), (33.5, 27.5),
        (37.5, 21.5), (43.3, 12.5), (51.2, 11.8), (48, 5), (41, -2), (40.5, -11),
        (35, -20), (33, -26), (28, -33), (20, -34.8), (18, -33), (14.5, -23),
        (12, -16), (13, -6), (9, 4), (3, 6.4), (-7.5, 4.5), (-13.5, 9),
        (-17.4, 14.7), (-16, 21), (-13, 27.5), (-6.5, 33.5),
    ]),
    ("Madagascar", [(44, -25), (47, -25), (50, -15), (49, -12), (44, -18)]),
    ("Indonesia", [(95.5, 5.5), (105.5, -6), (114.5, -8.5), (114, -7), (104, -1.5), (100, 1.5)]),
    ("Borneo", [(109, -3), (117, -3.5), (118.5, 5.5), (115, 6.5), (110, 1.5)]),
    ("Australia", [
        (114, -22), (122, -17), (131, -12), (136, -12), (137, -15), (141, -16),
        (142.5, -11), (146, -18), (153.5, -26), (151, -34), (149.5, -37.5),
        (140, -38), (135, -35), (129, -32), (115.5, -34.5), (114.5, -28),
    ]),
    ("New Zealand", [(167, -46), (173, -42), (178, -37.5), (174.5, -35), (172.5, -40), (166.5, -45)]),
]

INLAND_SEAS: list[list[tuple[float, float]]] = [
    [(49.5, 46.5), (52.5, 46.8), (54.0, 42.0), (53.5, 37.0), (50.0, 36.8), (48.5, 40.0), (47.5, 44.5)],
]


def point_in_poly(x: float, y: float, poly: Sequence[tuple[float, float]]) -> bool:
    """Ray-casting point-in-polygon check."""
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) if (yj - yi) != 0 else 1e-12) + xi
        ):
            inside = not inside
        j = i
    return inside


def is_on_land(lon: float, lat: float) -> bool:
    """Return True if geographic (lon, lat) is on land and not inside an inland sea."""
    in_continent = any(point_in_poly(lon, lat, poly) for _, poly in CONTINENTS)
    in_sea = any(point_in_poly(lon, lat, sea) for sea in INLAND_SEAS)
    return in_continent and not in_sea


# ---------------------------------------------------------------------------
# Drawing Primitives & Text Helpers
# ---------------------------------------------------------------------------
def draw_rounded_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float, float, float],
    radius: float,
    fill: tuple[int, int, int] | None = None,
    outline: tuple[int, int, int] | None = None,
    width: float = 1.0,
) -> None:
    x0, y0, x1, y1 = s(xy[0]), s(xy[1]), s(xy[2]), s(xy[3])
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=s(radius),
        fill=fill,
        outline=outline,
        width=max(1, s(width)) if outline else 0,
    )


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width_logical: float,
) -> list[str]:
    """Wrap text cleanly to fit within max_width_logical."""
    max_w = s(max_width_logical)
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        candidate = w if not cur else f"{cur} {w}"
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: float,
    fill: tuple[int, int, int],
    line_height: float,
    max_lines: int | None = None,
) -> float:
    """Draw wrapped text and return the bottom logical y coordinate."""
    lines = wrap_text(draw, text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textbbox((0, 0), last + "...", font=font)[2] > s(max_width):
            last = last[:-1].rstrip()
        lines[-1] = last + "..."
    cy = y
    for line in lines:
        draw.text((s(x), s(cy)), line, font=font, fill=fill)
        cy += line_height
    return cy


def draw_pill(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    bg: tuple[int, int, int],
    fg: tuple[int, int, int] = WHITE,
    pad_x: float = 5.0,
    height: float = 14.0,
    radius: float = 3.0,
    fixed_w: float | None = None,
) -> float:
    """Draw a compact colored badge pill and return its right x coordinate."""
    tw = draw.textlength(text, font=font) / SCALE
    w = fixed_w if fixed_w is not None else (tw + pad_x * 2)
    draw_rounded_box(draw, (x, y, x + w, y + height), radius=radius, fill=bg)
    bbox = draw.textbbox((0, 0), text, font=font)
    th = (bbox[3] - bbox[1]) / SCALE
    ty = y + (height - th) / 2 - bbox[1] / SCALE
    tx = x + (w - tw) / 2 if fixed_w is not None else (x + pad_x)
    draw.text((s(tx), s(ty)), text, font=font, fill=fg)
    return x + w


def draw_verified_badge(
    draw: ImageDraw.ImageDraw,
    x_right: float,
    y: float,
    source: str,
    font: ImageFont.FreeTypeFont,
) -> None:
    """Draw right-aligned verification checkmark badge + source name."""
    check_color = (22, 130, 62)
    tw = draw.textlength(source, font=font) / SCALE
    badge_w = tw + 18
    x0 = x_right - badge_w
    draw_rounded_box(
        draw,
        (x0, y, x_right, y + 14),
        radius=3.0,
        fill=(237, 245, 239),
        outline=check_color,
        width=0.9,
    )
    cx, cy = x0 + 7.5, y + 7.0
    draw.ellipse([s(cx - 4.5), s(cy - 4.5), s(cx + 4.5), s(cy + 4.5)], fill=check_color)
    draw.line(
        [(s(cx - 2.2), s(cy + 0.1)), (s(cx - 0.4), s(cy + 2.0)), (s(cx + 2.6), s(cy - 1.8))],
        fill=WHITE,
        width=s(1.4),
    )
    bbox = draw.textbbox((0, 0), source, font=font)
    th = (bbox[3] - bbox[1]) / SCALE
    ty = y + (14 - th) / 2 - bbox[1] / SCALE
    draw.text((s(x0 + 14), s(ty)), source, font=font, fill=INK_PRIMARY)


# ---------------------------------------------------------------------------
# Custom Editorial Scene Illustrations for the 3 Lead Stories
# ---------------------------------------------------------------------------
def draw_lead1_illustration(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
) -> None:
    """Lead 1: Brooklyn Federal Courtroom, Scales of Justice, Gavel & Circuit Motif."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw_rounded_box(draw, box, radius=4, fill=(21, 30, 52), outline=(42, 57, 88), width=1.0)

    circuit_c = (48, 76, 132)
    for idx in range(5):
        cy = y0 + 16 + idx * 19
        draw.line([(s(x0 + 8), s(cy)), (s(x0 + 68 - idx * 6), s(cy))], fill=circuit_c, width=s(1.2))
        draw.ellipse([s(x0 + 68 - idx * 6 - 2), s(cy - 2), s(x0 + 68 - idx * 6 + 2), s(cy + 2)], fill=(76, 128, 212))
        draw.line([(s(x1 - 8), s(cy)), (s(x1 - 65 + idx * 5), s(cy))], fill=circuit_c, width=s(1.2))
        draw.ellipse([s(x1 - 65 + idx * 5 - 2), s(cy - 2), s(x1 - 65 + idx * 5 + 2), s(cy + 2)], fill=(76, 128, 212))

    # Classical Federal Courthouse Pediment & Fluted Columns
    cx = x0 + w * 0.48
    roof_top = y0 + 10
    entab_y = y0 + 34
    base_y = y0 + h - 22
    pediment = [(s(cx - 76), s(entab_y)), (s(cx), s(roof_top)), (s(cx + 76), s(entab_y))]
    draw.polygon(pediment, fill=(235, 228, 210), outline=(180, 140, 45))
    draw.rectangle([s(cx - 73), s(entab_y), s(cx + 73), s(entab_y + 7)], fill=GOLD_ACCENT)
    f_plaque = load_font(FONT_SANS_BOLD, 5.5)
    plaque = "U.S. DISTRICT COURT · EDNY"
    pw = draw.textlength(plaque, font=f_plaque) / SCALE
    draw.text((s(cx - pw / 2), s(entab_y + 0.5)), plaque, font=f_plaque, fill=INK_PRIMARY)

    for px in (cx - 56, cx - 21, cx + 21, cx + 56):
        draw.rectangle([s(px - 6), s(entab_y + 7), s(px + 6), s(base_y)], fill=(224, 216, 198))
        # Subtle vertical column fluting
        for fl in (-2.5, 0.0, 2.5):
            draw.line([(s(px + fl), s(entab_y + 12)), (s(px + fl), s(base_y - 5))], fill=(182, 172, 152), width=s(0.7))
        draw.rectangle([s(px - 8), s(entab_y + 7), s(px + 8), s(entab_y + 11)], fill=(198, 186, 162))
        draw.rectangle([s(px - 8), s(base_y - 4), s(px + 8), s(base_y)], fill=(198, 186, 162))
    draw.rectangle([s(cx - 80), s(base_y), s(cx + 80), s(base_y + 5)], fill=(180, 172, 156))
    draw.rectangle([s(cx - 86), s(base_y + 5), s(cx + 86), s(base_y + 10)], fill=(140, 134, 122))

    # Golden Scales of Justice tilted (10 Guilty vs 2 Acquitted)
    sx, sy = cx, y0 + 55
    draw.line([(s(sx), s(sy - 9)), (s(sx), s(base_y - 4))], fill=GOLD_ACCENT, width=s(2.6))
    draw.line([(s(sx - 36), s(sy + 7)), (s(sx + 36), s(sy - 7))], fill=(250, 204, 21), width=s(2.5))
    draw.line([(s(sx - 36), s(sy + 7)), (s(sx - 44), s(sy + 25))], fill=GOLD_ACCENT, width=s(1.2))
    draw.line([(s(sx - 36), s(sy + 7)), (s(sx - 28), s(sy + 25))], fill=GOLD_ACCENT, width=s(1.2))
    draw.pieslice([s(sx - 48), s(sy + 19), s(sx - 24), s(sy + 33)], 0, 180, fill=(220, 38, 38), outline=GOLD_ACCENT)
    draw.line([(s(sx + 36), s(sy - 7)), (s(sx + 28), s(sy + 11))], fill=GOLD_ACCENT, width=s(1.2))
    draw.line([(s(sx + 36), s(sy - 7)), (s(sx + 44), s(sy + 11))], fill=GOLD_ACCENT, width=s(1.2))
    draw.pieslice([s(sx + 24), s(sy + 5), s(sx + 48), s(sy + 19)], 0, 180, fill=(37, 99, 235), outline=GOLD_ACCENT)

    # Stylized Mahogany Judicial Gavel & Sounding Block on right flank
    gx, gy = x1 - 44, y0 + 62
    draw.rounded_rectangle([s(gx - 14), s(gy + 16), s(gx + 14), s(gy + 22)], radius=s(2), fill=(180, 120, 48), outline=GOLD_ACCENT)
    draw.line([(s(gx - 2), s(gy)), (s(gx + 22), s(gy + 16))], fill=(217, 155, 78), width=s(3.2))
    draw.polygon(
        [(s(gx - 14), s(gy + 6)), (s(gx + 1), s(gy - 12)), (s(gx + 10), s(gy - 5)), (s(gx - 5), s(gy + 13))],
        fill=(146, 64, 14),
        outline=GOLD_ACCENT,
    )

    f_badge = load_font(FONT_SANS_BOLD, 8.0)
    draw_pill(draw, x0 + 8, y0 + 8, "BROOKLYN JURY", f_badge, (42, 57, 88), (250, 204, 21), pad_x=5, height=13.5)
    draw_pill(draw, x0 + 8, y1 - 20, "10 GUILTY", f_badge, (185, 28, 28), WHITE, pad_x=5, height=13.5)
    draw_pill(draw, x1 - 76, y1 - 20, "2 ACQUITTED", f_badge, (30, 64, 175), WHITE, pad_x=5, height=13.5)


def draw_lead2_illustration(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
) -> None:
    """Lead 2: East Sea / KADIZ Radar Intercept — 4 Russian Warplanes vs ROKAF F-15Ks."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw_rounded_box(draw, box, radius=4, fill=(11, 24, 38), outline=(28, 72, 92), width=1.0)

    ux, uy = x0 + w * 0.42, y0 + h * 0.68
    draw.pieslice([s(ux - 88), s(uy - 88), s(ux + 88), s(uy + 88)], 240, 315, fill=(18, 56, 70))
    for r, col in ((88, (22, 86, 108)), (60, (28, 112, 134)), (32, (245, 158, 11)), (22, (251, 191, 36))):
        draw.arc([s(ux - r), s(uy - r), s(ux + r), s(uy + r)], 190, 355, fill=col, width=s(1.2))
    draw.line([(s(x0 + 8), s(uy)), (s(x1 - 8), s(uy))], fill=(18, 52, 70), width=s(1.0))
    draw.line([(s(ux), s(y0 + 8)), (s(ux), s(y1 - 8))], fill=(18, 52, 70), width=s(1.0))

    korea_poly = [
        (s(x0 + 4), s(y0 + 18)), (s(x0 + 46), s(y0 + 22)),
        (s(x0 + 54), s(y0 + 56)), (s(x0 + 42), s(y0 + h - 8)),
        (s(x0 + 4), s(y0 + h - 8)),
    ]
    draw.polygon(korea_poly, fill=(38, 74, 72), outline=(94, 234, 212))
    draw.polygon(
        [(s(ux - 9), s(uy + 3)), (s(ux - 2), s(uy - 6)), (s(ux + 9), s(uy - 2)), (s(ux + 6), s(uy + 7))],
        fill=(245, 158, 11),
        outline=(254, 240, 138),
    )

    path_pts = [(x0 + w * 0.72, y0 + 16), (x0 + w * 0.56, y0 + 42), (ux + 20, uy - 24), (x1 - 24, y0 + 48)]
    for i in range(len(path_pts) - 1):
        draw.line([(s(path_pts[i][0]), s(path_pts[i][1])), (s(path_pts[i + 1][0]), s(path_pts[i + 1][1]))], fill=(239, 68, 68), width=s(2.0))

    def draw_jet(jx: float, jy: float, sc: float, color: tuple[int, int, int], heading_right: bool = True) -> None:
        d = 1 if heading_right else -1
        pts = [
            (s(jx + 14 * sc * d), s(jy)),
            (s(jx + 2 * sc * d), s(jy - 4 * sc)),
            (s(jx - 8 * sc * d), s(jy - 13 * sc)),
            (s(jx - 11 * sc * d), s(jy - 11 * sc)),
            (s(jx - 5 * sc * d), s(jy - 2 * sc)),
            (s(jx - 13 * sc * d), s(jy)),
            (s(jx - 5 * sc * d), s(jy + 2 * sc)),
            (s(jx - 11 * sc * d), s(jy + 11 * sc)),
            (s(jx - 8 * sc * d), s(jy + 13 * sc)),
            (s(jx + 2 * sc * d), s(jy + 4 * sc)),
        ]
        draw.polygon(pts, fill=color)

    draw_jet(x0 + w * 0.62, y0 + 34, 1.15, (239, 68, 68), heading_right=False)
    draw_jet(x0 + w * 0.78, y0 + 28, 0.85, (248, 113, 113), heading_right=False)
    # Intercept contrails + F-15K fighters
    draw.line([(s(x0 + 46), s(y0 + 78)), (s(ux - 18), s(uy - 24))], fill=(56, 189, 248), width=s(1.6))
    draw.line([(s(x0 + 42), s(y0 + 89)), (s(x0 + 64), s(y0 + 84))], fill=(125, 211, 252), width=s(1.1))
    draw_jet(x0 + 82, y0 + 66, 0.95, (56, 189, 248), heading_right=True)
    draw_jet(x0 + 66, y0 + 84, 0.82, (125, 211, 252), heading_right=True)

    f_ul = load_font(FONT_MONO_BOLD, 6.8)
    draw.text((s(ux - 21), s(uy + 11)), "ULLEUNG", font=f_ul, fill=(254, 240, 138))

    f_badge = load_font(FONT_SANS_BOLD, 8.0)
    draw_pill(draw, x0 + 8, y0 + 8, "KADIZ · 13 NMI ALERT", f_badge, (185, 28, 28), WHITE, pad_x=5, height=13.5)
    draw_pill(draw, x1 - 92, y1 - 20, "4 RU JETS · F-15K", f_badge, (15, 118, 110), WHITE, pad_x=5, height=13.5)


def draw_lead3_illustration(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
) -> None:
    """Lead 3: Strait of Hormuz Shipping Risk + Brent Rebound Chart ($88.10 -> $91.40)."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    draw_rounded_box(draw, box, radius=4, fill=(24, 18, 22), outline=(92, 42, 42), width=1.0)

    sea_y = y0 + h * 0.56
    draw.rectangle([s(x0 + 2), s(sea_y), s(x1 - 2), s(y1 - 2)], fill=(17, 36, 58))
    for wy in (sea_y + 10, sea_y + 24, sea_y + 36):
        draw.line([(s(x0 + 18), s(wy)), (s(x1 - 18), s(wy))], fill=(30, 58, 92), width=s(0.9))

    draw.polygon(
        [(s(x0 + 2), s(sea_y + 16)), (s(x0 + 58), s(sea_y + 6)), (s(x0 + 104), s(sea_y + 20)), (s(x0 + 2), s(y1 - 2))],
        fill=(62, 50, 38),
    )
    draw.polygon(
        [(s(x1 - 76), s(y1 - 2)), (s(x1 - 54), s(sea_y + 16)), (s(x1 - 2), s(sea_y + 8)), (s(x1 - 2), s(y1 - 2))],
        fill=(62, 50, 38),
    )

    tx, ty = x0 + 84, sea_y + 17
    draw.polygon(
        [(s(tx - 44), s(ty)), (s(tx + 40), s(ty)), (s(tx + 48), s(ty - 11)), (s(tx - 38), s(ty - 11))],
        fill=(32, 38, 48),
        outline=(148, 163, 184),
    )
    draw.rectangle([s(tx - 32), s(ty - 20), s(tx - 18), s(ty - 11)], fill=(226, 232, 240))
    draw.rectangle([s(tx - 8), s(ty - 16), s(tx + 26), s(ty - 11)], fill=(180, 83, 9))
    for sx_off, sy_off, sr, scol in (
        (16, -34, 10, (55, 58, 66)),
        (22, -43, 12, (72, 76, 86)),
        (12, -26, 8, (153, 27, 27)),
    ):
        draw.ellipse([s(tx + sx_off - sr), s(ty + sy_off - sr), s(tx + sx_off + sr), s(ty + sy_off + sr)], fill=scol)
    flame = [
        (s(tx + 4), s(ty - 16)),
        (s(tx + 10), s(ty - 32)),
        (s(tx + 14), s(ty - 24)),
        (s(tx + 19), s(ty - 35)),
        (s(tx + 22), s(ty - 16)),
    ]
    draw.polygon(flame, fill=(249, 115, 22))
    draw.polygon(
        [(s(tx + 8), s(ty - 16)), (s(tx + 13), s(ty - 27)), (s(tx + 18), s(ty - 16))],
        fill=(253, 224, 71),
    )

    gx0, gy0, gx1, gy1 = x0 + w * 0.48, y0 + 10, x1 - 10, sea_y + 10
    draw_rounded_box(draw, (gx0, gy0, gx1, gy1), radius=3, fill=(16, 23, 34), outline=(62, 74, 94), width=0.9)
    for frac in (0.36, 0.68):
        ly = gy0 + (gy1 - gy0) * frac
        draw.line([(s(gx0 + 4), s(ly)), (s(gx1 - 4), s(ly))], fill=(38, 49, 66), width=s(0.8))

    pts = [
        (gx0 + 10, gy0 + 25),
        (gx0 + 32, gy0 + 31),
        (gx0 + 54, gy0 + 42),
        (gx0 + 82, gy0 + 28),
        (gx0 + 112, gy0 + 21),
        (gx1 - 12, gy0 + 17),
    ]
    scaled_pts = [(s(px), s(py)) for px, py in pts]
    area_pts = scaled_pts + [(scaled_pts[-1][0], s(gy1 - 14)), (scaled_pts[0][0], s(gy1 - 14))]
    draw.polygon(area_pts, fill=(20, 48, 42))
    draw.line(scaled_pts, fill=(34, 197, 94), width=s(2.4))
    draw.ellipse([scaled_pts[2][0] - s(3), scaled_pts[2][1] - s(3), scaled_pts[2][0] + s(3), scaled_pts[2][1] + s(3)], fill=(239, 68, 68))
    draw.ellipse([scaled_pts[-1][0] - s(3.5), scaled_pts[-1][1] - s(3.5), scaled_pts[-1][0] + s(3.5), scaled_pts[-1][1] + s(3.5)], fill=(74, 222, 128))

    f_chart = load_font(FONT_MONO_BOLD, 7.8)
    draw.text((s(gx0 + 7), s(gy0 + 3.5)), "BRENT $91.40 (+2.27%)", font=f_chart, fill=(74, 222, 128))
    draw.text((s(gx0 + 28), s(gy1 - 12.5)), "LOW $88.10 (3-MO)", font=f_chart, fill=(248, 113, 113))

    f_badge = load_font(FONT_SANS_BOLD, 8.0)
    draw_pill(draw, x0 + 8, y0 + 8, "HORMUZ RISK", f_badge, (185, 28, 28), WHITE, pad_x=5, height=13.5)
    draw_pill(draw, x1 - 118, y1 - 20, "*IRGC CLAIM UNVERIFIED", f_badge, (120, 53, 15), (254, 240, 138), pad_x=5, height=13.5)


# ---------------------------------------------------------------------------
# World Map Projection & Rendering
# ---------------------------------------------------------------------------
def project_geo(
    lon: float,
    lat: float,
    map_box: tuple[float, float, float, float],
) -> tuple[float, float]:
    """Equirectangular projection covering [-168..180] lon, [-56..79] lat."""
    mx0, my0, mx1, my1 = map_box
    lon_min, lon_max = -168.0, 180.0
    lat_min, lat_max = -56.0, 79.0
    px = mx0 + (lon - lon_min) / (lon_max - lon_min) * (mx1 - mx0)
    py = my1 - (lat - lat_min) / (lat_max - lat_min) * (my1 - my0)
    return px, py


def draw_world_map_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
) -> None:
    """Render world map with verified continent polygons, 11 land pins & 2 global badges."""
    x0, y0, x1, y1 = box
    draw_rounded_box(draw, box, radius=5, fill=BG_CARD, outline=RULE_DARK, width=1.4)

    f_hdr = load_font(FONT_SANS_BOLD, 9.5)
    f_sub = load_font(FONT_SANS_SEMI, 8.0)
    draw.rectangle([s(x0), s(y0), s(x1), s(y0 + 21)], fill=BG_DARK)
    draw.text((s(x0 + 8), s(y0 + 4.5)), "WORLD COVERAGE MAP · 11 LAND PINS + 2 GLOBAL = 13", font=f_hdr, fill=WHITE)
    draw.text((s(x1 - 122), s(y0 + 5.5)), "COLOR-CODED BY REGION", font=f_sub, fill=GOLD_ACCENT)

    map_box = (x0 + 6, y0 + 24, x1 - 6, y1 - 6)
    mx0, my0, mx1, my1 = map_box
    ocean_fill = (214, 229, 240)
    draw.rectangle([s(mx0), s(my0), s(mx1), s(my1)], fill=ocean_fill, outline=(148, 175, 198), width=s(1.0))

    for glon in range(-150, 180, 30):
        gx, _ = project_geo(glon, 0, map_box)
        draw.line([(s(gx), s(my0)), (s(gx), s(my1))], fill=(195, 214, 229), width=s(0.7))
    for glat in (-30, 0, 30, 60):
        _, gy = project_geo(0, glat, map_box)
        col = (158, 186, 208) if glat == 0 else (195, 214, 229)
        draw.line([(s(mx0), s(gy)), (s(mx1), s(gy))], fill=col, width=s(0.9 if glat == 0 else 0.7))

    land_fill = (233, 224, 203)
    land_outline = (138, 128, 108)
    for _, poly in CONTINENTS:
        pts = [(s(px), s(py)) for lon, lat in poly for px, py in [project_geo(lon, lat, map_box)]]
        draw.polygon(pts, fill=land_fill, outline=land_outline)
    for sea in INLAND_SEAS:
        pts = [(s(px), s(py)) for lon, lat in sea for px, py in [project_geo(lon, lat, map_box)]]
        draw.polygon(pts, fill=ocean_fill, outline=land_outline)

    pin_stories = [st for st in STORIES if st.lat is not None and st.lon is not None]
    for st in pin_stories:
        assert st.lon is not None and st.lat is not None
        if not is_on_land(st.lon, st.lat):
            raise ValueError(f"Story #{st.num} ({st.location}) pin ({st.lon}, {st.lat}) fell outside land polygon!")

    label_offsets: dict[str, tuple[float, float]] = {
        "01": (8, -6),
        "02": (9, -3),
        "03": (9, 3),
        "04": (8, -9),
        "05": (-28, 5),
        "06": (-30, -9),
        "07": (8, 3),
        "08": (8, -8),
        "09": (-30, 3),
        "10": (8, 3),
        "12": (-28, -5),
    }

    f_pin = load_font(FONT_SANS_BOLD, 7.2)
    f_lbl = load_font(FONT_SANS_BOLD, 7.3)

    for st in pin_stories:
        assert st.lon is not None and st.lat is not None
        px, py = project_geo(st.lon, st.lat, map_box)
        col = REGION_COLORS[st.region]

        r = 6.8 if st.tier == "LEAD" else 5.8
        draw.ellipse([s(px - r - 1.5), s(py - r - 1.5), s(px + r + 1.5), s(py + r + 1.5)], fill=WHITE)
        draw.ellipse([s(px - r), s(py - r), s(px + r), s(py + r)], fill=col, outline=INK_PRIMARY, width=s(0.8))

        nbbox = draw.textbbox((0, 0), st.num, font=f_pin)
        nw = (nbbox[2] - nbbox[0]) / SCALE
        nh = (nbbox[3] - nbbox[1]) / SCALE
        draw.text(
            (s(px - nw / 2 - nbbox[0] / SCALE), s(py - nh / 2 - nbbox[1] / SCALE)),
            st.num,
            font=f_pin,
            fill=WHITE,
        )

        dx, dy = label_offsets[st.num]
        lx, ly = px + dx, py + dy
        tw = draw.textlength(st.pin_code, font=f_lbl) / SCALE
        draw_rounded_box(
            draw,
            (lx - 2, ly - 1, lx + tw + 3, ly + 10),
            radius=2,
            fill=(255, 253, 248),
            outline=col,
            width=0.7,
        )
        draw.text((s(lx + 0.5), s(ly - 0.5)), st.pin_code, font=f_lbl, fill=INK_PRIMARY)

    gx0, gy0, gx1, gy1 = mx0 + 8, my1 - 52, mx0 + 202, my1 - 6
    draw_rounded_box(draw, (gx0, gy0, gx1, gy1), radius=4, fill=(248, 246, 255), outline=REGION_COLORS["GLOBAL"], width=1.1)
    f_gtitle = load_font(FONT_SANS_BOLD, 7.8)
    f_gbody = load_font(FONT_SANS_SEMI, 7.4)
    draw.text((s(gx0 + 6), s(gy0 + 3.5)), "GLOBAL / NON-REGIONAL (2):", font=f_gtitle, fill=REGION_COLORS["GLOBAL"])
    draw.text((s(gx0 + 6), s(gy0 + 16)), "#11 UNODC: 47,000 Femicides (2025)", font=f_gbody, fill=INK_PRIMARY)
    draw.text((s(gx0 + 6), s(gy0 + 29)), "#13 Beaver Supermoon · 14:53 UTC", font=f_gbody, fill=INK_PRIMARY)


# ---------------------------------------------------------------------------
# Page Sections
# ---------------------------------------------------------------------------
def render_masthead(draw: ImageDraw.ImageDraw) -> None:
    """Row 1: Archival Newspaper Masthead (y=12..82)."""
    draw.rectangle([s(16), s(12), s(1008), s(16)], fill=RULE_DARK)
    draw.line([(s(16), s(19)), (s(1008), s(19))], fill=RULE_DARK, width=s(1.2))

    f_meta = load_font(FONT_MONO_BOLD, 8.5)
    f_title = load_font(FONT_SERIF_BOLD, 37.5)
    f_tag = load_font(FONT_SANS_BOLD, 9.5)
    f_count = load_font(FONT_SANS_BOLD, 10.5)

    draw_rounded_box(draw, (16, 24, 212, 74), radius=4, fill=BG_CARD, outline=RULE_DARK, width=1.1)
    draw.text((s(24), s(29)), "EDITION NO. 2026-11-24", font=f_meta, fill=INK_PRIMARY)
    draw.text((s(24), s(43)), "WORLD WIRE SYNTHESIS", font=f_meta, fill=INK_SECONDARY)
    draw.text((s(24), s(57)), "VERIFIED EDITION · EN", font=f_meta, fill=(15, 118, 110))

    title = "THE GLOBAL DISPATCH"
    tw = draw.textlength(title, font=f_title) / SCALE
    draw.text((s(512 - tw / 2), s(22.5)), title, font=f_title, fill=INK_PRIMARY)
    sub = "DAILY VERIFIED WORLD RECORD  ·  ONE-PAGE ARCHIVAL DIGEST"
    sw = draw.textlength(sub, font=f_meta) / SCALE
    draw.text((s(512 - sw / 2), s(65)), sub, font=f_meta, fill=INK_SECONDARY)

    draw_rounded_box(draw, (812, 24, 1008, 74), radius=4, fill=BG_DARK)
    draw.text((s(822), s(29)), "TUESDAY, 24 NOV 2026", font=f_tag, fill=GOLD_ACCENT)
    draw.text((s(822), s(45)), "13 VERIFIED STORIES", font=f_count, fill=WHITE)
    draw.text((s(822), s(59)), "7 REGIONS · 6 FIELDS", font=f_meta, fill=(190, 202, 218))

    draw.line([(s(16), s(80)), (s(1008), s(80))], fill=RULE_DARK, width=s(1.6))


def render_region_and_fields_strip(draw: ImageDraw.ImageDraw) -> None:
    """Row 2: Weighted Colored Region Strip (=13) + Full-Width Fields Bar (=13) (y=84..122)."""
    region_counts: dict[str, int] = {}
    field_counts: dict[str, int] = {}
    for st in STORIES:
        region_counts[st.region] = region_counts.get(st.region, 0) + 1
        field_counts[st.field] = field_counts.get(st.field, 0) + 1

    assert sum(region_counts.values()) == 13
    assert sum(field_counts.values()) == 13

    f_lbl = load_font(FONT_SANS_BOLD, 8.2)
    f_seg = load_font(FONT_SANS_BOLD, 8.0)

    draw.text((s(16), s(87)), "REGIONS (13):", font=f_lbl, fill=INK_PRIMARY)
    bar_x0 = 98.0
    width_by_count = {1: 90.0, 2: 135.0, 3: 190.0}
    cx = bar_x0
    order_regions = ("N. AMERICA", "LAT. AM", "EUROPE", "MID. EAST", "AFRICA", "ASIA", "GLOBAL")
    for idx, reg in enumerate(order_regions):
        cnt = region_counts[reg]
        seg_w = width_by_count[cnt]
        if idx == len(order_regions) - 1:
            seg_w = (bar_x0 + 910.0) - cx
        col = REGION_COLORS[reg]
        draw_rounded_box(draw, (cx + 1, 84, cx + seg_w - 1, 101), radius=2.5, fill=col)
        label = f"{reg} {cnt}"
        tw = draw.textlength(label, font=f_seg) / SCALE
        draw.text((s(cx + (seg_w - tw) / 2), s(87)), label, font=f_seg, fill=WHITE)
        cx += seg_w

    draw.text((s(16), s(107.5)), "FIELDS (13):", font=f_lbl, fill=INK_PRIMARY)
    items = list(field_counts.items())
    gap = 4.0
    raw_widths = [draw.textlength(f"{fld} {cnt}", font=f_seg) / SCALE + 12 for fld, cnt in items]
    extra_each = (910.0 - sum(raw_widths) - gap * (len(items) - 1)) / len(items)
    fx = bar_x0
    for idx, ((fld, cnt), rw) in enumerate(zip(items, raw_widths)):
        w = rw + extra_each
        if idx == len(items) - 1:
            w = (bar_x0 + 910.0) - fx
        fx = draw_pill(draw, fx, 105, f"{fld} {cnt}", f_seg, FIELD_COLORS[fld], WHITE, height=15, radius=3, fixed_w=w) + gap


def render_numbers_strip(draw: ImageDraw.ImageDraw) -> None:
    """Row 3: 6 Key Labeled Numbers, all sourced from stories on page (y=125..178)."""
    metrics = [
        ("10 / 12", "HUAWEI GUILTY COUNTS", "Story #01 · Law", REGION_COLORS["N. AMERICA"], INK_PRIMARY),
        ("13 NMI", "RU JETS OFF ULLEUNG", "Story #02 · Defense", REGION_COLORS["ASIA"], INK_PRIMARY),
        ("$91.40", "BRENT CRUDE (+2.27%)", "Story #03 · Energy", REGION_COLORS["MID. EAST"], (4, 120, 87)),
        ("40+", "ZAPORIZHZHIA WOUNDED", "Story #04 · Conflict", REGION_COLORS["EUROPE"], INK_PRIMARY),
        ("47,000", "2025 KIN FEMICIDES (UN)", "Story #11 · Rights", REGION_COLORS["GLOBAL"], INK_PRIMARY),
        ("-5.86%", "NVIDIA CLOSE ($155.38)", "Story #12 · Markets", REGION_COLORS["N. AMERICA"], (185, 28, 28)),
    ]

    f_num = load_font(FONT_SANS_BOLD, 20.5)
    f_cap = load_font(FONT_SANS_BOLD, 7.6)
    f_ref = load_font(FONT_SANS_SEMI, 7.2)

    card_w = (992.0 - 5 * 6.0) / 6.0
    for idx, (val, cap, ref, accent, val_color) in enumerate(metrics):
        x0 = 16.0 + idx * (card_w + 6.0)
        x1 = x0 + card_w
        draw_rounded_box(draw, (x0, 125, x1, 178), radius=4, fill=BG_CARD, outline=RULE_LIGHT, width=1.0)
        draw.rectangle([s(x0 + 1), s(125), s(x1 - 1), s(128.5)], fill=accent)
        draw.text((s(x0 + 8), s(129.5)), val, font=f_num, fill=val_color)
        draw.text((s(x0 + 8), s(154.5)), cap, font=f_cap, fill=INK_SECONDARY)
        draw.text((s(x0 + 8), s(166)), ref, font=f_ref, fill=accent)


def render_leads_section(draw: ImageDraw.ImageDraw) -> None:
    """Row 4: 3 Big Lead Stories, each with custom editorial illustration (y=182..456)."""
    f_sec = load_font(FONT_SANS_BOLD, 9.0)
    draw.rectangle([s(16), s(182), s(1008), s(197)], fill=BG_DARK)
    draw.text((s(24), s(184)), "FRONT PAGE LEADS (3)  ·  ILLUSTRATED PRIMARY DISPATCHES", font=f_sec, fill=WHITE)
    draw.text((s(830), s(184.5)), "TUESDAY 24 NOV 2026", font=f_sec, fill=GOLD_ACCENT)

    leads = [st for st in STORIES if st.tier == "LEAD"]
    col_w = (992.0 - 2 * 10.0) / 3.0

    f_pill = load_font(FONT_SANS_BOLD, 7.6)
    f_badge = load_font(FONT_SANS_SEMI, 7.3)
    f_hl = load_font(FONT_SERIF_BOLD, 14.3)
    f_body = load_font(FONT_SANS_REG, 9.4)
    f_foot = load_font(FONT_SANS_BOLD, 7.6)

    illus_drawers = [draw_lead1_illustration, draw_lead2_illustration, draw_lead3_illustration]

    for idx, st in enumerate(leads):
        x0 = 16.0 + idx * (col_w + 10.0)
        x1 = x0 + col_w
        y0, y1 = 201.0, 456.0
        draw_rounded_box(draw, (x0, y0, x1, y1), radius=4.5, fill=BG_CARD, outline=RULE_DARK, width=1.2)

        draw_pill(draw, x0 + 7, y0 + 6, f"#{st.num} {st.region}", f_pill, REGION_COLORS[st.region], WHITE, pad_x=5, height=14)
        draw_verified_badge(draw, x1 - 7, y0 + 6, st.source, f_badge)

        illus_box = (x0 + 7, y0 + 24, x1 - 7, y0 + 134)
        illus_drawers[idx](draw, illus_box)

        cy = draw_wrapped(draw, x0 + 8, y0 + 139, st.headline, f_hl, col_w - 16, INK_PRIMARY, 16.8, max_lines=2)
        draw_wrapped(draw, x0 + 8, cy + 3, st.summary, f_body, col_w - 16, INK_SECONDARY, 12.2, max_lines=6)

        draw.line([(s(x0 + 8), s(y1 - 18)), (s(x1 - 8), s(y1 - 18))], fill=RULE_LIGHT, width=s(0.8))
        draw.text((s(x0 + 8), s(y1 - 14)), f"{st.location}  ·  {st.field}", font=f_foot, fill=REGION_COLORS[st.region])


def render_secondary_grid(draw: ImageDraw.ImageDraw) -> None:
    """Row 5: 4 Secondary Grid Stories (y=461..584)."""
    f_sec = load_font(FONT_SANS_BOLD, 9.0)
    draw.rectangle([s(16), s(461), s(1008), s(476)], fill=BG_SLATE)
    draw.text((s(24), s(463)), "WORLD DESK · SECONDARY GRID (4)", font=f_sec, fill=WHITE)
    draw.text((s(792), s(463.5)), "CROSS-REGIONAL COVERAGE", font=f_sec, fill=GOLD_ACCENT)

    secs = [st for st in STORIES if st.tier == "SECONDARY"]
    col_w = (992.0 - 3 * 8.0) / 4.0

    f_pill = load_font(FONT_SANS_BOLD, 7.2)
    f_badge = load_font(FONT_SANS_SEMI, 7.0)
    f_hl = load_font(FONT_SERIF_BOLD, 11.5)
    f_body = load_font(FONT_SANS_REG, 8.8)
    f_foot = load_font(FONT_SANS_BOLD, 7.2)

    for idx, st in enumerate(secs):
        x0 = 16.0 + idx * (col_w + 8.0)
        x1 = x0 + col_w
        y0, y1 = 480.0, 584.0
        draw_rounded_box(draw, (x0, y0, x1, y1), radius=4, fill=BG_CARD, outline=RULE_LIGHT, width=1.1)
        draw.rectangle([s(x0), s(y0 + 3), s(x0 + 3.2), s(y1 - 3)], fill=REGION_COLORS[st.region])

        draw_pill(draw, x0 + 8, y0 + 5, f"#{st.num} {st.region}", f_pill, REGION_COLORS[st.region], WHITE, pad_x=4.5, height=13.5)
        draw_verified_badge(draw, x1 - 6, y0 + 5, st.source, f_badge)

        cy = draw_wrapped(draw, x0 + 8, y0 + 22.5, st.headline, f_hl, col_w - 15, INK_PRIMARY, 13.8, max_lines=2)
        draw_wrapped(draw, x0 + 8, cy + 2.5, st.summary, f_body, col_w - 15, INK_SECONDARY, 11.4, max_lines=3)
        draw.text((s(x0 + 8), s(y1 - 13)), f"{st.location}  ·  {st.field}", font=f_foot, fill=INK_MUTED)


def render_map_and_also_today(draw: ImageDraw.ImageDraw) -> None:
    """Row 6: World Map (left 592px) + Also Today 3 Briefs (right 392px) (y=589..853)."""
    draw_world_map_panel(draw, (16, 589, 608, 853))

    rx0, rx1 = 616.0, 1008.0
    draw_rounded_box(draw, (rx0, 589, rx1, 853), radius=5, fill=BG_CARD_ALT, outline=RULE_DARK, width=1.3)
    f_hdr = load_font(FONT_SANS_BOLD, 9.5)
    draw.rectangle([s(rx0), s(589), s(rx1), s(610)], fill=BG_DARK)
    draw.text((s(rx0 + 8), s(593.5)), "ALSO TODAY · VERIFIED BRIEFS (3)", font=f_hdr, fill=WHITE)

    alsos = [st for st in STORIES if st.tier == "ALSO"]
    f_pill = load_font(FONT_SANS_BOLD, 7.3)
    f_badge = load_font(FONT_SANS_SEMI, 7.1)
    f_hl = load_font(FONT_SERIF_BOLD, 11.4)
    f_body = load_font(FONT_SANS_REG, 8.9)
    f_foot = load_font(FONT_SANS_BOLD, 7.3)

    slot_h = 75.8
    for idx, st in enumerate(alsos):
        sy0 = 615.0 + idx * (slot_h + 4.0)
        sy1 = sy0 + slot_h
        draw_rounded_box(draw, (rx0 + 6, sy0, rx1 - 6, sy1), radius=3.5, fill=BG_CARD, outline=RULE_LIGHT, width=0.9)
        draw_pill(draw, rx0 + 11, sy0 + 5, f"#{st.num} {st.region}", f_pill, REGION_COLORS[st.region], WHITE, pad_x=4.5, height=13.5)
        draw_verified_badge(draw, rx1 - 11, sy0 + 5, st.source, f_badge)
        cy = draw_wrapped(draw, rx0 + 11, sy0 + 21.5, st.headline, f_hl, (rx1 - rx0) - 22, INK_PRIMARY, 13.0, max_lines=1)
        draw_wrapped(draw, rx0 + 11, cy + 2, st.summary, f_body, (rx1 - rx0) - 22, INK_SECONDARY, 11.2, max_lines=2)
        draw.text((s(rx0 + 11), s(sy1 - 13)), f"{st.location}  ·  {st.field}", font=f_foot, fill=REGION_COLORS[st.region])


def render_ticker_and_utc_strip(draw: ImageDraw.ImageDraw) -> None:
    """Row 7: Ticker (3) with full Field tags + THE DAY IN UTC Timeline (y=858..956)."""
    tickers = [st for st in STORIES if st.tier == "TICKER"]
    col_w = (992.0 - 2 * 10.0) / 3.0
    f_pill = load_font(FONT_SANS_BOLD, 7.1)
    f_badge = load_font(FONT_SANS_SEMI, 6.9)
    f_hl = load_font(FONT_SANS_BOLD, 9.2)
    f_body = load_font(FONT_SANS_REG, 8.2)
    f_foot = load_font(FONT_SANS_BOLD, 7.0)

    for idx, st in enumerate(tickers):
        x0 = 16.0 + idx * (col_w + 10.0)
        x1 = x0 + col_w
        draw_rounded_box(draw, (x0, 858, x1, 916), radius=3.5, fill=BG_CARD, outline=RULE_LIGHT, width=1.0)
        draw_pill(draw, x0 + 6, 862, f"TICKER #{st.num} · {st.region}", f_pill, REGION_COLORS[st.region], WHITE, pad_x=4.5, height=13)
        draw_verified_badge(draw, x1 - 6, 862, st.source, f_badge)
        draw.text((s(x0 + 7), s(877.5)), st.headline, font=f_hl, fill=INK_PRIMARY)
        draw_wrapped(draw, x0 + 7, 890, st.summary, f_body, col_w - 14, INK_SECONDARY, 10.0, max_lines=1)
        draw.text((s(x0 + 7), s(903.5)), f"{st.location}  ·  {st.field}", font=f_foot, fill=REGION_COLORS[st.region])

    # THE DAY IN UTC Timeline Strip (y=920..956)
    draw_rounded_box(draw, (16, 920, 1008, 956), radius=4, fill=(236, 231, 220), outline=RULE_DARK, width=1.1)
    f_utc_hdr = load_font(FONT_SANS_BOLD, 8.2)
    f_time = load_font(FONT_MONO_BOLD, 7.6)
    f_ev = load_font(FONT_SANS_SEMI, 7.4)

    draw.rectangle([s(16), s(920), s(108), s(956)], fill=BG_DARK)
    draw.text((s(22), s(925.5)), "THE DAY", font=f_utc_hdr, fill=GOLD_ACCENT)
    draw.text((s(22), s(939)), "IN UTC", font=f_utc_hdr, fill=WHITE)

    nodes = [
        ("22:52Z (Nov 23)", "07:52 KST Ulleung (#02)"),
        ("10:17 UTC", "Progress MS-36 (#08)"),
        ("14:53 UTC", "Supermoon Peak (#13)"),
        ("12:00 EST (~17Z)", "UN Briefing (#10)"),
        ("21:00 UTC", "NVDA Close -5.86% (#12)"),
        ("PM EST (~21-22Z)", "Huawei Verdict (#01)"),
    ]
    draw.line([(s(120), s(937.5)), (s(996), s(937.5))], fill=RULE_DARK, width=s(1.2))
    step_w = (998.0 - 118.0) / len(nodes)
    for idx, (tm, ev) in enumerate(nodes):
        nx = 120.0 + idx * step_w
        draw.ellipse([s(nx - 3.5), s(934), s(nx + 3.5), s(941)], fill=GOLD_ACCENT, outline=BG_DARK, width=s(1.0))
        draw.text((s(nx + 6), s(923.5)), tm, font=f_time, fill=INK_PRIMARY)
        draw.text((s(nx + 6), s(941)), ev, font=f_ev, fill=INK_SECONDARY)


def render_footer(draw: ImageDraw.ImageDraw) -> None:
    """Row 8: Footer DATE CHECK + Sources List (y=960..1012)."""
    draw_rounded_box(draw, (16, 960, 1008, 1012), radius=4, fill=BG_DARK)
    f_lbl = load_font(FONT_SANS_BOLD, 8.2)
    f_txt = load_font(FONT_SANS_REG, 7.9)

    draw_pill(draw, 22, 965, "DATE CHECK", f_lbl, (22, 130, 62), WHITE, pad_x=5, height=13.5)
    date_note = (
        "All 13 stories verified for Tue 24 Nov 2026. Cross-day/caveat notes: "
        "#02 07:52 KST (22:52Z Nov 23); *#03 UKMTO 23 Nov & IRGC mines unverified by Reuters; "
        "#12 NVDA 23 Nov +31.48% surge. Excludes 25 Nov & 20-23 Nov events."
    )
    draw.text((s(96), s(966)), date_note[:142], font=f_txt, fill=CREAM_TEXT)
    if len(date_note) > 142:
        draw.text((s(24), s(980.5)), date_note[142:].lstrip(), font=f_txt, fill=CREAM_TEXT)

    draw.line([(s(22), s(993)), (s(1002), s(993))], fill=(58, 70, 92), width=s(0.8))
    draw.text((s(24), s(996.5)), "SOURCES:", font=f_lbl, fill=GOLD_ACCENT)
    sources_line = (
        "Reuters · AP · U.S. DOJ · Al Jazeera · CAS (tas-cas.org) · UN News · UNODC · "
        "NASA · Space.com · The Guardian · AFP · WashPost · Chosun Ilbo · The Hindu · Forbes"
    )
    draw.text((s(80), s(996.5)), sources_line, font=f_txt, fill=(203, 213, 225))


def main() -> None:
    """Render the 1024x1024 newspaper summary image deterministically to entry.png."""
    assert len(STORIES) == 13, f"Expected 13 stories, got {len(STORIES)}"

    canvas = Image.new("RGB", (W, H), BG_PAPER)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([s(8), s(8), s(1016), s(1016)], outline=RULE_DARK, width=s(1.5))

    render_masthead(draw)
    render_region_and_fields_strip(draw)
    render_numbers_strip(draw)
    render_leads_section(draw)
    render_secondary_grid(draw)
    render_map_and_also_today(draw)
    render_ticker_and_utc_strip(draw)
    render_footer(draw)

    final_img = canvas.resize((FINAL_SIZE, FINAL_SIZE), Image.Resampling.LANCZOS)
    final_img.save("entry.png", format="PNG", optimize=True)
    print(f"Generated entry.png ({final_img.size[0]}x{final_img.size[1]}) with {len(STORIES)} verified stories.")


if __name__ == "__main__":
    main()
