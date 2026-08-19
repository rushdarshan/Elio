"""Bar-3 LLM-assisted proposal layer.

Stand-in for a real LLM call (no API key in this environment). A real
implementation replaces ``propose`` with an LLM prompt over ``raw_text`` and
returns the same dict shape. Proposals are NOT accepted here — the existing
stage_verification dual-pass gate is the only acceptance path.
"""

from typing import Dict, Tuple
import re

_QTY_RE = re.compile(r"(?:^|\s)(\d{1,4})\s*(?:pk|ct|pcs?|pack|box|sheets?|pairs?|set)s?(?=\s|$|[.,;:!?/])")
_QTY_SLASH_RE = re.compile(r"(?<![0-9])/\s*(\d{1,4})(?:pk|pack|set)?(?=\s|$|[.,;])")
_QTY_OF_RE = re.compile(r"\b(?:pack|box|set)\s+of\s+(\d{1,4})\b")

_SIZE_PAIR_RE = re.compile(
    r"(?<![./\d])(\d+(?:\.\d+)?)\s*(['\"]?)\s*x\s*['\"]?\s*(\d+(?:\.\d+)?)(?![\d./])\s*(ft|foot|feet|in|inch|inches|mm|'|\")?"
)
_BATT_RE = re.compile(r"\b(m\d{2})\b")
_HP_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*hp\b")
_MM_RE = re.compile(r"\b(\d{2,4})\s*mm\b")
_KTEMP_RE = re.compile(r"\b(\d{2})k\b")
_SHAPE_RE = re.compile(r"\b(t5|t6|t8|t9|t12|st18|st19|st64|a19|a21|a23|b11|br30|br40|par20|par30|par38|r20|r30|r40|g25|g40|s11)\b")
_LUMBER_RE = re.compile(
    r"(?<![./\d])(\d+(?:\.\d+)?)\s*n?\s*['\"]?\s*x\s*['\"]?\s*(\d+(?:\.\d+)?)(?![\d./])"
    r"\s*[-x]\s*(\d+(?:\.\d+)?)\s*(ft|foot|feet|'|in|inch|mm|\")"
)
_LUMBER_PROFILES = {"1", "2", "3", "4", "5", "6", "8", "10", "12", "16"}
_SINGLE_SIZE_RE = re.compile(r"\b(\d{2}(?:\.\d+)?)\s*\"")
_FT_LEN_RE = re.compile(r"\b(\d{2,3})\s*'")
_GRIT_RE = re.compile(r"\b(\d{2,4})\s*grit\b")
_FLUX_RE = re.compile(r"\b(\d{3,5})\s*(?:l|lm)\b")
_KIT_SIZE_RE = re.compile(r"\b(?:kit|size)\s+(s|m|l|xl|2xl|3xl)\b")

_LIGHT_WORDS = ("light", "led", "bulb", "incan", "cand", "flor", "lamp", "t5", "t8", "t9", "t12", "retro", "lt", "fixture")
_APPLIANCE_WORDS = ("dryer", "washer", "dishwasher", "laundry", "range", "refrigerator",
                    "stove", "oven", "rail", "deck", "gate", "balust", "fascia", "trim", "select",
                    "fan", "dimmer", "door", "window")
_APPAREL_WORDS = ("hoodie", "jacket", "vest", "glove", "gloves", "apparel", "shirt", "pants", "bib", "coverall", "coat")
_FAN_WORDS = ("fan",)
_SAW_WORDS = ("bandsaw", "table saw", "miter", "saw", "circular")
_DECK_WORDS = ("trex", "transcend", "enhance", "composite")

_COLOR_PHRASE_RE = re.compile(
    r"\b((?:dark|light|charcoal|slate|french|harvest|bright|medium)\s+)?"
    r"((?:white|black|gray|grey|buff|chocolate|oak)\s+)?"
    r"(white|black|gray|grey|buff|chocolate|oak|blue|green|red|yellow|brown|tan|ivory|almond|beige|silver|gold|copper|nickel|bronze)\b"
)
_COLOR_ABBR_RE = re.compile(r"(?<=\s)(wh|bk|bz|mb)(?=\s|$)")
_COLOR_ABBR_MAP = {"wh": "White", "bk": "Black", "bz": "Bronze", "mb": "Matte Black"}

_BRAND_TOKENS = ("milw", "makita", "dewalt", "festool", "bosch", "ryobi", "ridgid")

_TRIPLE_UNIT_RE = re.compile(r"\s*x\s*['\"]?\d+(?:\.\d+)?\s*(?:ft|foot|feet|')(?![\d.])")


def propose(raw_text: str) -> Dict[str, Tuple[str, str]]:
    t = raw_text.lower()
    out: Dict[str, Tuple[str, str]] = {}

    # 1. Quantity: "2pk", "500CT", "50 Sheets/Box", "GR PRO/10"
    q = _QTY_RE.search(t)
    if q:
        out["Quantity"] = (q.group(1), "pk")
    q2 = _QTY_SLASH_RE.search(t)
    if q2 and "Quantity" not in out:
        after = t[q2.end():q2.end() + 2]
        if not after.startswith(("'", '"', "x")):
            out["Quantity"] = (q2.group(1), "pk")
    q3 = _QTY_OF_RE.search(t)
    if q3 and "Quantity" not in out:
        out["Quantity"] = (q3.group(1), "pk")

    # 2. Generic Size pair (tapes, panels, trim...) — merge step fills only
    #    labels extractors left empty, so no duplication risk here.
    m = _SIZE_PAIR_RE.search(t)
    if m:
        a, b = m.group(1), m.group(3)
        unit = m.group(4) or ""
        quoted = bool(m.group(2))
        blade_rows = re.search(r"(disc|blade|bit|demon|wheel|cut-off|cutoff|grinding)", t)
        if quoted and blade_rows:
            pass  # extractors own these: Diameter/Arbor/Thickness, not Size
        elif unit in ("ft", "foot", "feet", "'"):
            if not m.group(2) and a in _LUMBER_PROFILES and b in _LUMBER_PROFILES:
                # "1x6'" bare pair = lumber profile in inches, trailing ' = length
                out["Size"] = (f"{a} x {b}", "in")
                out["Length"] = (b, "ft")
            else:
                out["Size"] = (f"{a} x {b}", "ft")
        elif unit in ("mm",):
            out["Size"] = (f"{a} x {b}", "mm")
        elif unit in ("in", "inch", "inches", '"'):
            out["Size"] = (f"{a} x {b}", "in")
        elif _TRIPLE_UNIT_RE.search(t, m.end()):
            # "1.5x1.5x13'" convention: cross-section pair, length carries the unit
            out["Size"] = (f"{a} x {b}", "in")
        # no unit anywhere -> skip (honest abstention)

    # 3. Battery platform: M12/M18 on tool-brand rows (skip dual-platform rows)
    if any(b in t for b in _BRAND_TOKENS):
        ms = set(m.upper() for m in _BATT_RE.findall(t))
        if len(ms) == 1 and "Battery Platform" not in out:
            out["Battery Platform"] = (ms.pop(), "")

    # 4. Horsepower
    m = _HP_RE.search(t)
    if m:
        out["Horsepower"] = (m.group(1), "hp")

    # 5. mm dimension (calipers etc.) — only when "mm" appears exactly once
    if t.count("mm") == 1:
        m = _MM_RE.search(t)
        if m and "Size" not in out:
            out["Size"] = (m.group(1), "mm")

    # 6. Color temperature shorthand: "27K" = 2700 K (lighting rows)
    if any(w in t for w in _LIGHT_WORDS):
        m = _KTEMP_RE.search(t)
        if m and "Color Temperature" not in out:
            k = int(m.group(1)) * 100
            if k in (2500, 2700, 3000, 3500, 4000, 5000, 6500):
                out["Color Temperature"] = (str(k), "K")

    # 7. Color: multi-word phrase, single word, or appliance/rail abbreviations
    m = _COLOR_PHRASE_RE.search(t)
    if m:
        phrase = " ".join(p for p in m.groups() if p)
        out["Color"] = (" ".join(w.capitalize() for w in phrase.split()), "")
    elif any(w in t for w in _APPLIANCE_WORDS):
        m = _COLOR_ABBR_RE.search(t)
        if m and m.group(1) in _COLOR_ABBR_MAP:
            out["Color"] = (_COLOR_ABBR_MAP[m.group(1)], "")

    # 8. Bulb shape: T8/T9/T12/A19/BR30/PAR38...
    if any(w in t for w in _LIGHT_WORDS):
        m = _SHAPE_RE.search(t)
        if m and "Bulb Shape" not in out:
            out["Bulb Shape"] = (m.group(1).upper(), "")

    # 9. Lumber "1x6-16'" / "1nx6-16'" -> Size 1 in x 6 in + Length 16 ft
    m = _LUMBER_RE.search(t)
    if m:
        a, b, ln, lu = m.group(1), m.group(2), m.group(3), m.group(4)
        out["Size"] = (f"{a} x {b}", "in")
        unit = "ft" if lu in ("ft", "foot", "feet", "'") else ("mm" if lu == "mm" else "in")
        out["Length"] = (ln, unit)

    # 9b. Trex/composite decking material (never override an explicit material token)
    _EXPLICIT_MATERIAL = r"(alum|aluminum|steel|stainless|pvc|vinyl|wood|brass|copper|iron|stone|plastic|glass)"
    if any(w in t for w in _DECK_WORDS) and "Material" not in out and not re.search(_EXPLICIT_MATERIAL, t):
        out["Material"] = ("Composite", "")

    # 9c. Fan size "44\"" and saw size "14\"" / "30\""
    if "Size" not in out and not re.search(r"(blade|disc|bit|demon|wheel|cut-off|cutoff|grinding)", t):
        m = _SINGLE_SIZE_RE.search(t)
        if m:
            n = float(m.group(1))
            if any(w in t for w in _FAN_WORDS) and 36 <= n <= 60:
                out["Size"] = (m.group(1), "in")
            elif any(w in t for w in _SAW_WORDS) and 8 <= n <= 40:
                out["Size"] = (m.group(1), "in")

    # 9d. Tape light length "16'"
    if "Length" not in out and any(w in t for w in _LIGHT_WORDS):
        m = _FT_LEN_RE.search(t)
        if m:
            out["Length"] = (m.group(1), "ft")

    # 10. Grit "220 Grit"
    m = _GRIT_RE.search(t)
    if m and "Grit" not in out:
        out["Grit"] = (m.group(1), "")

    # 11. Luminous flux "4500L" / "1600 lm" (lighting rows)
    if any(w in t for w in _LIGHT_WORDS):
        m = _FLUX_RE.search(t)
        if m and "Luminous Flux" not in out:
            out["Luminous Flux"] = (m.group(1), "L")

    # 12. Apparel size "Kit L" / "Size M"
    if any(w in t for w in _APPAREL_WORDS):
        m = _KIT_SIZE_RE.search(t)
        if m and "Size" not in out:
            out["Size"] = (m.group(1).upper(), "")

    return out