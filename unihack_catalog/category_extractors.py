"""Category-specific attribute extraction for the real held-out data.

Every value MUST appear in the raw text (or be a literal conversion of it).
No invented values, no guessing — abstention is the product's contract.
Labels follow the gold attribute vocabulary where applicable.

Category detection: keyword triggers -> category. Longest trigger wins.
"""
import re
from typing import Dict, Any, Tuple, List, Optional

# label -> (value, uom) tuples or plain strings (same shape as _generic_extraction)

CATEGORY_TRIGGERS: Dict[str, List[str]] = {
    "discs": ["disc", "cut-off", "cutoff", "cut off", "wheel", "grinding", "flap"],
    "blades": ["blade", "teeth"],
    "belts": ["belt", "sanding", "abrasive", "stikit", "cubitron", "film"],
    "drill-bits": ["bit", "drill", "hole saw", "brad point", "countersink", "reamer", "auger", "router"],
    "adapters": ["socket adapter", "adapter", "shank"],
    "fasteners": ["nailer", "stapler", "tacker", "staple"],
    "fasteners": ["nailer", "stapler", "tacker"],
    "lighting": ["bulb", "lamp", "led", "fluorescent", "cfl", "halogen", "incandescent",
                 "lumens", "lumen", "e26", "mr16", "par30", "par38", "t8", "t12",
                 "fixture", "pendant", "chandelier", "vanity", "ceiling fan"],
    "lumber": ["lumber", "plywood", "stud", "board", "moulding", "molding", "trim",
               "siding", "lattice", "drywall", "decking", "trex", "timbertech",
               "joist", "osb", "fascia"],
    "wire": ["wire", "cable"],
    "electrical": ["outlet", "receptacle", "switch", "gfci", "dimmer"],
}


def detect_category(raw_text: str) -> str:
    t = raw_text.lower()
    best, best_len = None, -1
    for cat, triggers in CATEGORY_TRIGGERS.items():
        for trig in triggers:
            if re.search(r"(?<![a-z0-9])" + re.escape(trig) + r"(?![a-z0-9])", t) and len(trig) > best_len:
                best, best_len = cat, len(trig)
    return best or ""


_MEAS = r'(\d+(?:-\d+/\d+)?(?:/\d+)?(?:\.\d+)?)'
_DIM_RE = re.compile(r'%s\s*["\']?\s*x\s*["\']?\s*%s' % (_MEAS, _MEAS))
_SIZE_RE = re.compile(r'%s\s*["\']\s*[A-Za-z ]+?\s*x\s*%s' % (_MEAS, _MEAS))


def _norm_meas(raw: str, unit: str = "in") -> str:
    """1/2 -> '1/2 in', 12-1/4 -> '12-1/4 in', 20mm handled by caller."""
    return f"{raw} {unit}"


def _parse_size(t: str) -> Tuple[Optional[str], Optional[str]]:
    """Best-effort 'A x B' parse; handles 1/2"x18", 12"x1", 1/4" Square x1/4" Hex.
    Returns (left, right) as raw tokens or None."""
    m = _DIM_RE.search(t) or _SIZE_RE.search(t)
    if not m:
        return None, None
    a, b = m.group(1), m.group(2)
    return a, b


def _inches(raw: str) -> str:
    """Normalize a measurement token: 12\" or 12in -> '12 in'."""
    m = re.match(r'^%s\s*(?:["\']|in|inch|inches)?$' % _MEAS, raw.strip())
    return f"{m.group(1)} in" if m else raw.strip()


def _grit(raw: str) -> str:
    m = re.search(r'[Pp]?(\d{2,4})', raw)
    return m.group(1) if m else ""


def _extract_discs(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    tri = re.search(r'%s\s*["\']\s*x\s*(\.\d+|\d+(?:/\d+)?)\s*["\']\s*x\s*%s\s*["\']?' % (_MEAS, _MEAS), t)
    if tri:
        # ponytail: 5"x.045"x7/8" = diameter x thickness x arbor
        g2 = tri.group(2)
        thick = ("0" + g2 if g2.startswith(".") else str(int(g2))) + " in"
        out["Diameter"] = _inches(tri.group(1))
        out["Thickness"] = thick
        out["Arbor Size"] = _inches(tri.group(3))
    else:
        a, b = _parse_size(t)
        if a:
            out["Diameter"] = _inches(a)
            if b:
                if "mm" in t[max(0, t.find(b) - 3):t.find(b) + 5]:
                    out["Arbor Size"] = f"{b} mm"
                else:
                    out["Arbor Size"] = _inches(b)
    m = re.search(r'%s\s*["\']' % _MEAS, t)
    if m and "Diameter" not in out:
        out["Diameter"] = _inches(m.group(1))
    for mat, kw in [("Steel", "steel"), ("Metal", "metal"), ("Masonry", "masonry"),
                    ("Tile", "tile"), ("Concrete", "concrete"), ("Wood", "wood"),
                    ("Aluminum", "aluminum"), ("Cubitron II", "cubitron ii")]:
        if kw in t:
            out["Material"] = mat
            break
    for typ, kw in [("Cut-Off", "cut-off"), ("Cutoff", "cutoff"), ("Grinding", "grinding"),
                    ("Flap", "flap"), ("Diamond", "diamond")]:
        if kw in t:
            out["Type"] = typ
            break
    q = re.search(r'(\d+)\s*(?:pc|pack|pk)\b', t)
    if q:
        out["Quantity"] = q.group(1)
    return out


def _extract_blades(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if re.search(r'"\s*x\s*\d+\s*T\b', t):
        # ponytail: "10\"x80T" is diameter x teeth, not a size pair
        a = re.search(r'%s\s*["\']' % _MEAS, t)
        if a:
            out["Diameter"] = _inches(a.group(1))
    else:
        a, b = _parse_size(t)
        if a:
            out["Diameter"] = _inches(a)
            if b:
                if "mm" in t[max(0, t.find(b) - 3):t.find(b) + 5]:
                    out["Arbor Size"] = f"{b} mm"
                else:
                    out["Arbor Size"] = _inches(b)
    arb = re.search(r'%s\s*["\']?\s*arbor' % _MEAS, t)
    if arb:
        out["Arbor Size"] = _inches(arb.group(1))
    teeth = re.search(r'(\d+)\s*(?:teeth|t)\b', t, re.IGNORECASE)
    if teeth:
        out["Number of Teeth"] = teeth.group(1)
    for mat, kw in [("Steel", "steel"), ("Metal", "metal"), ("Carbide", "carbide"),
                    ("Diamond", "diamond"), ("Wood", "wood"), ("Cubitron II", "cubitron ii")]:
        if kw in t:
            out["Material"] = mat
            break
    for typ, kw in [("Laminate & Wood Flooring", "laminate & wood flooring"), ("Metal Cutting", "metal"),
                    ("Masonry", "masonry"), ("Rip Cut", "rip"), ("Crosscut", "crosscut")]:
        if kw in t:
            out["Type"] = typ
            break
    if "Type" not in out:
        # ponytail: only literal phrases; "blade" alone abstains
        for typ, kw in [("Jig Saw Blade", "jig saw blade"), ("Sawzall Blade", "sawzall blade"),
                        ("Planer Blade", "planer blade"), ("Tile Blade", "tile blade"),
                        ("Diamond Blade", "diamond blade"), ("Saw Blade", "saw blade"),
                    ("Blade", "blade")]:
            if kw in t:
                out["Type"] = typ
                break
    return out


def _extract_belts(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    a, b = _parse_size(t)
    if a and b:
        out["Size"] = f"{_inches(a)} x {_inches(b)}"
    grit = re.search(r'[Pp]\s*(\d{2,4})', t)
    if grit:
        out["Grit"] = grit.group(1)
    q = re.search(r'(\d+)\s*(?:pc|pack|pk|disc|sheet|box)\b', t)
    if q:
        out["Quantity"] = q.group(1)
    for mat, kw in [("Aluminum Oxide", "aluminum oxide"), ("Silicon Carbide", "silicon carbide"),
                    ("Zirconia", "zirconia"), ("Ceramic", "ceramic"), ("Cubitron II", "cubitron ii")]:
        if kw in t:
            out["Material"] = mat
            break
    if "sanding" in t:
        out["Type"] = "Sanding"
    return out


def _extract_drill_bits(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    a, b = _parse_size(t)
    if a:
        out["Diameter"] = _inches(a)
        if b:
            out["Size"] = f"{_inches(a)} x {_inches(b)}"
    m = re.search(r'%s\s*["\']' % _MEAS, t)
    if m and "Diameter" not in out:
        out["Diameter"] = _inches(m.group(1))
    for mat, kw in [("Carbide", "carbide"), ("Cobalt", "cobalt"), ("High Speed Steel", "hss"),
                    ("High Speed Steel", "high speed steel"), ("Titanium", "titanium")]:
        if kw in t:
            out["Material"] = mat
            break
    for typ, kw in [("Brad Point", "brad point"), ("Step", "step"), ("Countersink", "countersink"),
                    ("Masonry", "masonry"), ("Reamer", "reamer"), ("Auger", "auger"),
                    ("Hole Saw", "hole saw"), ("Router", "router")]:
        if kw in t:
            out["Type"] = typ
            break
    for sh, kw in [("Hex", "hex"), ("Square", "square"), ("Round", "round"), ("Quick Change", "quick change")]:
        if kw in t:
            out["Shank Type"] = sh
            break
    q = re.search(r'(\d+)\s*(?:pc|pack|pk|set)\b', t)
    if q:
        out["Quantity"] = q.group(1)
    return out


def _extract_adapters(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    a, b = _parse_size(t)
    if a and b:
        out["Size"] = f"{_inches(a)} x {_inches(b)}"
    has_hex = "hex" in t
    has_sq = "square" in t
    if has_hex and has_sq:
        out["Shank Type"] = "Square x Hex"
    elif has_hex:
        out["Shank Type"] = "Hex"
    elif has_sq:
        out["Shank Type"] = "Square"
    if "socket adapter" in t:
        out["Type"] = "Socket Adapter"
    elif "adapter" in t:
        out["Type"] = "Adapter"
    return out


def _extract_fasteners(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for typ, kw in [("Brad Nailer", "brad nailer"), ("Framing Nailer", "framing nailer"),
                    ("Finish Nailer", "finish nailer"), ("Roofing Nailer", "roofing nailer"),
                    ("Staple Gun", "staple gun"), ("Stapler", "stapler"), ("Staple", "staple")]:
        if kw in t:
            out["Type"] = typ
            break
    m = re.search(r'(\d+(?:-\d+/\d+)?(?:/\d+)?(?:\.\d+)?)\s*["\']', t)
    if m:
        out["Size"] = _inches(m.group(1))
    g = re.search(r'(\d{2})\s*GA\b', t, re.IGNORECASE)
    if g:
        out["Gauge"] = (int(g.group(1)), "GA")
    return out


def _extract_lighting(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    w_matches = list(re.finditer(r'(\d+(?:\.\d+)?)\s*W(?:att)?\b', t, re.IGNORECASE))
    if w_matches:
        # ponytail: "100W EQUIV 75W" — the value followed by EQUIV is
        # incandescent-equivalence marketing; the other number is the draw.
        equiv = None
        for m in w_matches:
            if "equiv" in t[m.end():m.end() + 10]:
                equiv = m
        chosen = w_matches[0]
        if equiv is not None and len(w_matches) > 1:
            chosen = w_matches[1] if w_matches[0] is equiv else w_matches[0]
        out["Wattage"] = (chosen.group(1), "W")
    v = re.search(r'(\d+)\s*V(?:olt)?\b', t, re.IGNORECASE)
    if v:
        out["Voltage Rating"] = (int(v.group(1)), "V")
    l = re.search(r'(\d[\d,]*)\s*(?:lumens?|lm)\b', t, re.IGNORECASE)
    if l:
        out["Luminous Flux"] = (l.group(1).replace(",", ""), "lm")
    k = re.search(r'(\d{3,4})\s*K\b', t, re.IGNORECASE)
    if k:
        out["Color Temperature"] = (k.group(1), "K")
    base = re.search(r'\b(E26|E27|GU10|GU24|G4|G9|E12|E17|BA15S)\b', t, re.IGNORECASE)
    if base:
        out["Base Type"] = base.group(1).upper()
    shape = re.search(r'\b(PAR30|PAR38|PAR20|BR30|BR40|MR16|T8|T12)\b', t, re.IGNORECASE)
    if shape:
        out["Bulb Shape"] = shape.group(1).upper()
    for typ, kw in [("LED", "led"), ("CFL", "cfl"), ("Fluorescent", "fluorescent"),
                    ("Halogen", "halogen"), ("Incandescent", "incandescent")]:
        if kw in t:
            out["Type"] = typ
            break
    if "dimmable" in t:
        out["Dimmable"] = "Yes"
    return out


def _extract_lumber(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    a, b = _parse_size(t)
    if a and b and not re.search(r'\b[124]\s*x\s*[246]\b', t):
        out["Size"] = f"{_inches(a)} x {_inches(b)}"
    lg = re.search(r'(\d+(?:\.\d+)?)\s*(?:ft|foot|feet|\')\b', t, re.IGNORECASE)
    if lg:
        out["Length"] = (lg.group(1), "ft")
    for mat, kw in [("Plywood", "plywood"), ("OSB", "osb"),
                    ("Cedar", "cedar"), ("Pine", "pine"), ("Fir", "fir")]:
        if kw in t:
            out["Material"] = mat
            break
    for grd, kw in [("Premium", "premium"), ("Prime", "prime"), ("Select", "select"),
                    ("Kiln Dried", "kiln dried")]:
        if kw in t:
            out["Grade"] = grd
            break
    for sp, kw in [("Douglas Fir", "douglas fir"), ("Hemlock", "hemlock"), ("Cedar", "cedar")]:
        if kw in t:
            out["Species"] = sp
            break
    if "2x4" in t or "2 x 4" in t:
        out["Nominal Size"] = "2x4"
    if "2x6" in t or "2 x 6" in t:
        out["Nominal Size"] = "2x6"
    return out


def _extract_wire(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    g = re.search(r'\b(\d{1,2})\s*(?:AWG|ga|gauge)\b', t, re.IGNORECASE)
    cond = re.search(r'\b(\d{1,2})/(\d)\b', t)
    if g:
        out["Wire Gauge"] = (int(g.group(1)), "AWG")
    elif cond:
        # ponytail: slash-style gauge ("14/2" = 14 AWG, 2 conductors, no suffix)
        out["Wire Gauge"] = (int(cond.group(1)), "AWG")
    if cond:
        out["Number of Conductors"] = int(cond.group(2))
    lg = re.search(r'(\d+(?:\.\d+)?)\s*(?:ft|foot|feet|\')\b', t, re.IGNORECASE)
    if lg:
        out["Length"] = (lg.group(1), "ft")
    for mat, kw in [("Copper", "copper"), ("Aluminum", "aluminum"), ("Steel", "steel")]:
        if kw in t:
            out["Material"] = mat
            break
    ctype = re.search(r'\b(NM-B|NM|MC|BX|THHN|THWN|UF-B|UF|SEU|ROMEX)\b', t, re.IGNORECASE)
    if ctype:
        out["Type"] = ctype.group(1).upper()
    v = re.search(r'(\d+)\s*V(?:olt)?\b', t, re.IGNORECASE)
    if v:
        out["Voltage Rating"] = (int(v.group(1)), "V")
    return out


def _extract_electrical(t: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    v = re.search(r'(\d+)\s*V(?:olt)?\b', t, re.IGNORECASE)
    if v:
        out["Voltage Rating"] = (int(v.group(1)), "V")
    a = re.search(r'(\d+(?:\.\d+)?)\s*A(?:mp)?\b', t, re.IGNORECASE)
    if a:
        out["Amperage Rating"] = (a.group(1), "A")
    for typ, kw in [("GFCI", "gfci"), ("Duplex Receptacle", "duplex receptacle"),
                    ("Toggle Switch", "toggle switch"), ("Dimmer Switch", "dimmer switch"),
                    ("Decorator Receptacle", "decorator receptacle")]:
        if kw in t:
            out["Type"] = typ
            break
    for clr, kw in [("White", "white"), ("Ivory", "ivory"), ("Black", "black"), ("Gray", "gray"),
                    ("Brown", "brown"), ("Red", "red")]:
        if kw in t:
            out["Color"] = clr
            break
    return out


EXTRACTORS: Dict[str, Any] = {
    "discs": _extract_discs,
    "blades": _extract_blades,
    "belts": _extract_belts,
    "drill-bits": _extract_drill_bits,
    "adapters": _extract_adapters,
    "fasteners": _extract_fasteners,
    "lighting": _extract_lighting,
    "lumber": _extract_lumber,
    "wire": _extract_wire,
    "electrical": _extract_electrical,
}


def extract_for(raw_text: str) -> Dict[str, Any]:
    """Detect category(ies) and merge all matching extractors' output."""
    t = raw_text.lower()
    out: Dict[str, Any] = {}
    seen = set()
    for cat, triggers in CATEGORY_TRIGGERS.items():
        for trig in triggers:
            if re.search(r"(?<![a-z0-9])" + re.escape(trig) + r"(?![a-z0-9])", t) and cat not in seen:
                seen.add(cat)
                out.update(EXTRACTORS[cat](t))
                break
    return out


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Unihack_ Sample Dataset - Input.csv", encoding="utf-8-sig")
    for _, r in df[df["Part_Desc"].str.contains("disc|blade|belt|bit|bulb|lumber|wire|outlet", case=False, na=False)].head(12).iterrows():
        print(f"{r['Mfg_Part_Num']}: {r['Part_Desc'][:60]}")
        print("   ->", extract_for(r["Part_Desc"]))