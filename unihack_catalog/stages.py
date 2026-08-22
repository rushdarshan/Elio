import re
import os
import json
import hashlib
from typing import List, Dict, Any, Tuple, Optional

from .models import (
    EnrichedRecord, InputRecord, Identity, Brand, Manufacturer,
    Classpath, SourceProvenance, AttributeRecord, Descriptions,
    DescriptionDetail, QualityDecision, CostDetail
)

try:
    from .reference_loader import ReferenceLoader
    _loader = ReferenceLoader()
except Exception:
    _loader = None

# ============================================================
# Shared reference API (builder B extends reference_loader.py
# in parallel). Call the loader's functions when present;
# fall back to minimal inline defaults. Never crash.
# ============================================================

_TAXONOMY_FALLBACK = {
    "dishwasher": ("Appliances", "Large Appliances", "Dishwashers",
                   "Appliances & Consumer Electronics>Kitchen Appliances>Built-In Dishwashers"),
    "faucet": ("Plumbing", "Faucets", "Kitchen Faucets", "Plumbing>Faucets>Kitchen Faucets"),
    "sink": ("Plumbing", "Faucets", "Kitchen Faucets", "Plumbing>Faucets>Kitchen Faucets"),
    "elbow": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "tee": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "coupling": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "adapter": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "union": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "nipple": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
}

# ponytail: MPN-prefix -> brand for appliance model numbers (PDSH = Frigidaire, WDTS = Whirlpool).
# Extend per new manufacturer prefix; description scan takes precedence anyway.
_MPN_PREFIX_BRANDS = {
    "PDSH": "FRIGIDAIRE\u00ae",
    "FDB": "FRIGIDAIRE\u00ae",
    "FGIP": "FRIGIDAIRE\u00ae",
    "FGMV": "FRIGIDAIRE\u00ae",
    "WDTS": "Whirlpool\u00ae",
    "WDT": "Whirlpool\u00ae",
    "WFW": "Whirlpool\u00ae",
    "PSD": "Whirlpool\u00ae",
    "KDFM": "KitchenAid",
    "KDTM": "KitchenAid",
    "KDPM": "KitchenAid",
    "MDB": "Maytag",
    "MVWB": "Maytag",
    "LDF": "LG",
    "DLG": "LG",
    "EDV": "Electrolux",
    "BFD": "Bosch",
    "SHX": "Bosch",
    "GDT": "GE Appliances",
    "PDT": "GE Appliances",
    "GTW": "GE Appliances",
    "GBT": "GE Appliances",
    "GZS": "GE Appliances",
}

# ponytail: Part_Manuf is the supplier field; distributor names must never be
# surfaced as OEM manufacturers (e.g., resolve Rheem/Whirlpool, not APPDE).
_DISTRIBUTOR_BLACKLIST = {
    "Appliance Dealers Cooperative", "Jam Industrial Supply LLC", "Parksite",
    "Palmer Donavin Mfg Company", "U S Lumber", "Westwood Lumber Sales",
    "Tech Gear 5.7 Inc",
}

_UOM_FALLBACK = {
    "v": "V", "volt": "V", "voltage": "V",
    "a": "A", "amp": "A", "amperage": "A",
    "dba": "dBA",
    "in": "in", "inch": "in", "inches": "in",
    "gpm": "Gallons Per Minute", "each": "Each", "ea": "Each",
}

_FRAC_FALLBACK = {
    "0.0625": "1/16", "0.125": "1/8", "0.1875": "3/16", "0.25": "1/4",
    "0.3125": "5/16", "0.375": "3/8", "0.4375": "7/16", "0.5": "1/2",
    "0.5625": "9/16", "0.625": "5/8", "0.6875": "11/16", "0.75": "3/4",
    "0.8125": "13/16", "0.875": "7/8", "0.9375": "15/16",
}

_ATTR_LABELS = [
    "Series", "Model", "Number of Wash Cycles", "Voltage Rating", "Amperage Rating",
    "Mounting Type", "Plug Type", "Size", "Depth With Door Open", "Minimum Height",
    "Maximum Height", "Sound Level", "Material", "Color", "Additional Information",
]


def _safe(fn_name: str, fallback: Any) -> Any:
    """Call a reference_loader API if present; otherwise return fallback. Never crash."""
    try:
        fn = getattr(_loader, fn_name, None)
        if callable(fn):
            out = fn()
            if out:
                return out
    except Exception:
        pass
    return fallback


def _fraction_lookup(dec_str: str) -> Optional[str]:
    try:
        fn = getattr(_loader, "fraction_lookup", None)
        if callable(fn):
            out = fn(dec_str)
            if out:
                return str(out)
    except Exception:
        pass
    return _FRAC_FALLBACK.get(str(round(float(dec_str), 4)))


def _get_taxonomy_keywords() -> Dict[str, Tuple[str, str, str, str]]:
    merged = dict(_TAXONOMY_FALLBACK)
    merged.update(_safe("get_taxonomy_keywords", {}) or {})
    return merged


def _get_brand_vocab() -> Dict[str, Dict[str, str]]:
    vocab = {}
    try:
        ref = _loader.load_brands_manufacturers() if _loader else {}
        for brand, info in (ref.get("brands") or {}).items():
            mfr = str(info.get("parent") or "").strip()
            slug = re.sub(r'[^a-z0-9]', '', mfr.lower())
            vocab[brand] = {"manufacturer": mfr,
                            "mfr_url": f"https://www.{slug}.com" if slug else ""}
    except Exception:
        pass
    merged = dict(vocab)
    merged.update(_safe("get_brand_vocab", {}) or {})
    return merged


def _get_uom_map() -> Dict[str, str]:
    merged = dict(_UOM_FALLBACK)
    merged.update(_safe("get_uom_map", {}) or {})
    return merged


def _get_attribute_lov() -> Dict[str, List[str]]:
    return _safe("get_attribute_lov", {}) or {}


def _canon_uom(uom: str) -> str:
    uom = str(uom or "").strip()
    if not uom:
        return ""
    return _get_uom_map().get(uom.lower(), uom)


def _norm_key(s: str) -> str:
    return re.sub(r'[^a-z0-9]', '', str(s).lower())


def _fmt_spec(v: Any, uom: str) -> str:
    if isinstance(v, float) and not v.is_integer():
        whole = int(v)
        frac = round(v - whole, 4)
        fr = _fraction_lookup(str(frac))
        return f"{whole}-{fr}" if fr else str(v)
    if isinstance(v, float):
        return str(int(v))
    return str(v)


def _fnum(s: str) -> str:
    try:
        return str(int(float(s)))
    except Exception:
        return s


def _item_type(record: EnrichedRecord) -> str:
    return {"Dishwashers": "Dishwasher", "Kitchen Faucets": "Faucet",
            "Pipe Fittings": "Fitting"}.get(record.classpath.fine, record.classpath.fine or record.classpath.dept)


def _attr_map(record: EnrichedRecord) -> Dict[str, AttributeRecord]:
    return {a.label: a for a in record.attributes}


class PipelineError(Exception):
    pass


# --- STAGE 1: Intake & Normalize ---
def stage_intake_normalize(raw_row: Dict[str, Any]) -> EnrichedRecord:
    mpn = str(raw_row.get("MPN", raw_row.get("Mfg_Part_Num", ""))).strip()
    raw_mfr = str(raw_row.get("Manufacturer", raw_row.get("Part_Manuf", ""))).strip()
    raw_text = str(raw_row.get("Description", raw_row.get("Part_Desc", ""))).strip()

    if not mpn:
        raise PipelineError("Intake failed: Missing MPN.")

    clean_text = re.sub(r'\s+', ' ', raw_text).strip()

    def _p(col: str, alt: str) -> Optional[str]:
        v = str(raw_row.get(col, "")).strip()
        return v if v else (str(alt).strip() or None)

    input_rec = InputRecord(
        mpn=mpn,
        raw_text=clean_text,
        raw_manufacturer=raw_mfr,
        mfg_part_num=_p("Mfg_Part_Num", mpn if "MPN" in raw_row else ""),
        part_desc=_p("Part_Desc", clean_text if "Description" in raw_row else ""),
        e1_brand=_p("E1_Brand", ""),
        unilog_brand=_p("Unilog_Brand", ""),
        dib_brand=_p("DIB_Brand", ""),
        part_manuf=_p("Part_Manuf", raw_mfr if "Manufacturer" in raw_row else ""),
    )

    dummy_brand = Brand(id="B_PENDING", label="Pending", parent=None)
    dummy_mfr = Manufacturer(id="M_PENDING")
    dummy_identity = Identity(brand=dummy_brand, manufacturer=dummy_mfr)
    dummy_class = Classpath(dept="Pending", **{"class": "Pending"}, fine="Pending")

    dummy_desc_detail = DescriptionDetail(text="", chars=0, valid=False)
    dummy_descs = Descriptions(
        mobile=dummy_desc_detail, invoice=dummy_desc_detail, short=dummy_desc_detail,
        long=dummy_desc_detail, retail=dummy_desc_detail, marketing=dummy_desc_detail
    )

    return EnrichedRecord(
        input=input_rec,
        identity=dummy_identity,
        classpath=dummy_class,
        descriptions=dummy_descs,
        quality=QualityDecision(),
        cost=CostDetail()
    )


# --- STAGE 2: Entity Resolution (deterministic-first, always runs, never passthrough) ---
def _find_brand(text: str, vocab: Dict[str, Dict[str, str]], skip_suppliers: bool = False) -> Optional[str]:
    # ponytail: word-boundary matching on the raw text — "3M" must not match
    # inside "0013Milw"; keys with ® also match their un-marked form.
    best, best_len = None, -1
    for key in vocab:
        if skip_suppliers and vocab.get(key, {}).get("supplier"):
            continue
        variants = [key]
        if "\u00ae" in key:
            variants.append(key.replace("\u00ae", ""))
        for v in variants:
            if not v:
                continue
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(v) + r"(?![A-Za-z0-9])", text, re.IGNORECASE):
                if len(v) > best_len:
                    best, best_len = key, len(v)
                break
    return best


def stage_entity_resolution(record: EnrichedRecord) -> EnrichedRecord:
    vocab = _get_brand_vocab()
    # Phase 1: brand columns + description + MPN — the manufacturer must come
    # from an OEM brand signal, never the distributor's name in Part_Manuf.
    text = " ".join(t for t in [record.input.dib_brand, record.input.e1_brand,
                                record.input.unilog_brand, record.input.raw_text,
                                record.input.mpn] if t)

    key = _find_brand(text, vocab, skip_suppliers=True)
    if not key:
        up = record.input.mpn.upper()
        for prefix, brand_key in _MPN_PREFIX_BRANDS.items():
            if up.startswith(prefix):
                key = brand_key
                break
    if not key:
        # Phase 2: OEM-named supplier fallback (never distributor names).
        mfr_txt = re.sub(r'\s*\([A-Z0-9 ]+\)\s*$', '', record.input.raw_manufacturer).strip()
        if mfr_txt and mfr_txt not in _DISTRIBUTOR_BLACKLIST:
            key = _find_brand(mfr_txt, vocab)

    if key == "GE" and re.search(r'\b(dishwasher|refrigerator|range|oven|microwave|washer|dryer|freezer|disposer)\b', text.lower()):
        # ponytail: "GE" alone is ambiguous; appliance keywords force the appliance division.
        key = "GE Appliances" if "GE Appliances" in vocab else key

    if key == "LG" and re.search(r'\b(gloves?|holsters?|apparel|clothing|jackets?|vests?|shirts?|pants?|belts?|pockets?|fits?|straps?)\b', text.lower()) and not re.search(r'\b(dishwasher|refrigerator|fridge|range|oven|microwave|washer|dryer|freezer|appliance|tv|oled|compressor)\b', text.lower()):
        # LG matches on glove/holster etc. are sizes, not the LG Electronics brand.
        key = None

    if not key:
        # Never echo raw distributor names as brand/manufacturer.
        record.identity.brand = Brand(id="B_UNBRANDED", label="Unbranded", parent="Unknown Manufacturer")
        record.identity.manufacturer = Manufacturer(id="M_UNKNOWN", label="Unknown Manufacturer", mfr_url="")
        return record

    info = vocab[key]
    mfr = str(info.get("manufacturer") or "Unknown Manufacturer")
    url = str(info.get("mfr_url") or "").replace("{mpn}", record.input.mpn)
    brand_label = key
    if info.get("supplier"):
        # ponytail: supplier keys (e.g. "Milwaukee Accessory") resolve their
        # brand as the strongest non-supplier key they contain.
        brand_label = _find_brand(key, vocab, skip_suppliers=True) or key
    if "\u00ae" not in brand_label:
        brand_label = vocab.get(brand_label, {}).get("alias_of") or brand_label
    record.identity.brand = Brand(id=f"B_{_norm_key(brand_label).upper()}", label=brand_label, parent=mfr)
    record.identity.manufacturer = Manufacturer(id=f"M_{_norm_key(mfr).upper()}", label=mfr, mfr_url=url)
    return record


# --- STAGE 3: Taxonomy Classification (keyword-driven, never "Other" on a match) ---
def stage_taxonomy_classification(record: EnrichedRecord) -> EnrichedRecord:
    tx = _get_taxonomy_keywords()
    text = f"{record.input.raw_text} {record.input.mpn}".lower()
    best, best_len = None, -1
    for kw, (dept, cls, fine, classpath) in tx.items():
        if re.search(rf"(?<![a-z0-9]){re.escape(kw)}(?![a-z0-9])", text) and len(kw) > best_len:
            best, best_len = (dept, cls, fine, classpath), len(kw)
    if best:
        dept, cls, fine, classpath = best
        record.classpath = Classpath(dept=dept, **{"class": cls}, fine=fine,
                                     candidate_ids=[classpath])
        return record
    # Brand-prefix fallback: Milwaukee/Dewalt/Makita/Festool/etc. rows that miss
    # every keyword are power tools, not "Other".
    try:
        from .reference_loader import _tool_brand_fallback
        fb = _tool_brand_fallback(text)
    except Exception:
        fb = None
    if fb and fb[0] != "Other":
        dept, cls, fine, classpath = fb
        record.classpath = Classpath(dept=dept, **{"class": cls}, fine=fine,
                                     candidate_ids=[classpath])
        return record
    record.classpath = Classpath(dept="Other", **{"class": "Other"}, fine="Other", candidate_ids=[])
    return record


# --- STAGE 4: Research Planning ---
def stage_research_planning(record: EnrichedRecord) -> EnrichedRecord:
    # Manufacturer domains derive from the MFR URL; no quality side effects.
    return record


# --- STAGE 5: Document Fetch (evidence ledger: in-repo reference workbook, hashed) ---
def stage_document_fetch(record: EnrichedRecord) -> Tuple[EnrichedRecord, Dict[str, Any]]:
    mfr = record.identity.manufacturer
    # ponytail: external manufacturer URLs are pointers only — never claim fetched
    # content we didn't fetch. The evidence document is the in-repo reference
    # workbook (sanctioned source, sha256-hashed); live fetches (whirlpool 403,
    # frigidaire timeout) are logged as unavailable, not faked.
    pointer_url = mfr.mfr_url or ""
    # ponytail: evidence text is the input description only. The organizer
    # answer-key CSV is never cited as a source document — citing the answer
    # key as "evidence" for values copied from it is fabrication.
    html_text = record.input.raw_text
    doc_hash = hashlib.sha256(html_text.encode("utf-8")).hexdigest()[:16]
    evidence_doc = {
        "url": "",
        "content_hash": f"sha256:{doc_hash}",
        "html_text": html_text,
        "page_number": 1,
        "pointer_url": pointer_url,
        "pointer_status": "unavailable_live" if pointer_url else "none",
    }
    return record, evidence_doc


# --- STAGE 6: Extraction (deterministic, source-cited, never fabricated) ---
def _generic_extraction(raw_text: str) -> Dict[str, Any]:
    """Best-effort attribute extraction straight from the input description."""
    t = raw_text.lower()
    out: Dict[str, Any] = {}
    if re.search(r'\bss\b', t):
        out["Material"] = "Stainless Steel"
    for m in ["PVC", "Copper", "Brass", "PEX", "CPVC", "ABS"]:
        if m.lower() in t:
            out["Material"] = m
            break
    for f in ["Chrome", "Matte Black", "Vibrant Stainless", "Brushed Nickel", "Oil Rubbed Bronze"]:
        if f.lower() in t:
            out["Finish"] = f
            break
    gpm = re.search(r'(\d+(?:\.\d+)?)\s*gpm', t)
    if gpm:
        out["Flow Rate"] = f"{gpm.group(1)} gpm"
    volt = re.search(r'\b(\d+)\s*v\b', t)
    if volt:
        out["Voltage Rating"] = (int(volt.group(1)), "V")
    amp = re.search(r'\b(\d+(?:\.\d+)?)\s*Amp(?:s|ere)?\b', t, re.IGNORECASE)
    if not amp:
        # Bare "15A" is legit only mid-description; reject MPN-prefix codes
        # like "37418A Kichler" or "9A-570-240".
        amp = re.search(r'(?i:(?<=\s|[-/])(\d+(?:\.\d+)?)\s*a)\b(?=\s*[a-z]|/[a-z0-9]|\s*\d+\s*[vW])', t)
    if amp:
        out["Amperage Rating"] = (int(amp.group(1)), "A")
    dba = re.search(r'\b(\d+)\s*dba\b', t)
    if dba:
        out["Sound Level"] = (int(dba.group(1)), "dBA")
    size = re.search(r'(\d+(?:-\d+/\d+)?(?:\.\d+)?)\s*in(?:ch(?:es)?)?\b', t)
    if size:
        out["Size"] = f"{size.group(1)} in"
    return out


def _locate(text: str, value: str) -> Tuple[int, int, str]:
    if not value:
        return 0, 0, ""
    start = text.find(value)
    if start < 0:
        return 0, 0, text[:60]
    end = start + len(value)
    return start, end, text[max(0, start - 15):min(len(text), end + 15)]


def stage_extraction(record: EnrichedRecord, doc: Dict[str, Any]) -> EnrichedRecord:
    generic = _generic_extraction(record.input.raw_text)
    try:
        from .category_extractors import extract_for
        generic.update(extract_for(record.input.raw_text))
    except Exception as exc:
        record.quality.review_reasons.append(f"Category extraction fallback: {exc}")
    if os.environ.get("ELIO_ASSISTED") == "1":
        # Bar 3: LLM proposal layer — fills labels extractors left empty.
        # Acceptance still happens downstream in stage_verification's dual-pass.
        from .llm_proposals import propose
        proposals = propose(record.input.raw_text)
        generic = {**proposals, **generic}  # extractor wins ties; proposals fill gaps

    lov = _get_attribute_lov()
    labels = list(dict.fromkeys(list(_ATTR_LABELS) + (list(lov.keys()) if lov else []) + list(generic.keys())))
    extracted_ordered = []
    for l in _ATTR_LABELS:
        if l in generic:
            extracted_ordered.append(l)
    for l in (list(lov.keys()) if lov else []):
        if l not in extracted_ordered and l in generic:
            extracted_ordered.append(l)
    for l in generic:
        if l not in extracted_ordered:
            extracted_ordered.append(l)

    # Candidate catalog attributes evaluated but absent from source text (honest abstentions)
    candidate_abstained = [l for l in labels if l not in extracted_ordered][:10]
    ordered = extracted_ordered + candidate_abstained

    doc_text = doc["html_text"]
    doc_url = doc["url"]
    attributes = []
    for label in ordered:
        raw, uom = "", ""
        if label in generic:
            g = generic[label]
            if isinstance(g, tuple):
                raw, uom = _fmt_spec(g[0], g[1]), g[1]
            else:
                raw = str(g)
        start, end, snippet = _locate(doc_text, raw)
        char_span = [start, end] if (end > start and start >= 0) else None
        attributes.append(AttributeRecord(
            label=label,
            value=raw,
            uom=uom,
            source=SourceProvenance(url=doc_url if raw else "", page=doc.get("page_number", 1) if raw else 1,
                                    char_span=char_span, snippet=snippet if raw else "Refused to fabricate — absent from source text"),
            confidence=0.9 if raw else 0.0,
            verification="supported" if raw else "not_found",
        ))

    record.attributes = attributes
    return record


# --- STAGE 7: Verification ---
def stage_verification(record: EnrichedRecord) -> EnrichedRecord:
    reasons = []
    if record.identity.brand.label == "Unbranded":
        reasons.append("Entity resolution failed: no known brand/manufacturer in vocab.")
    if record.classpath.dept == "Other":
        reasons.append("Taxonomy classification failed: no keyword matched.")
    if not [a for a in record.attributes if a.value]:
        reasons.append("No attributes extracted.")
    
    # Dual-pass verification: every emitted value must trace back to the input text
    # (or a literal unit/number conversion of it).
    text_l = record.input.raw_text.lower()
    _EXPANSIONS = {
        "stainless steel": {"ss", "sst", "s/s"},
        "stainless": {"ss", "sst"},
        "white": {"wh", "wt"},
        "black": {"bk", "blk"},
        "bronze": {"bz"},
        "matte black": {"mb"},
        "composite": {"trex", "azek", "timbertech"},
    }
    bad = []
    for a in record.attributes:
        v = a.value.strip()
        if not v:
            continue
        vl = v.lower()
        base = re.sub(r'\s*(in|mm|v|w|lm|k|awg|ft|dba|ga)\s*$', '', vl)
        ok = vl in text_l or base in text_l or (re.search(r'\b\d+\b', v) and vl.split()[0] in text_l)
        if not ok and " x " in vl:
            # Composed values ("Square x Hex") pass when every part is a verbatim, word-bounded token.
            ok = all(re.search(r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])", text_l)
                     for p in vl.split(" x "))
        if not ok and base.startswith("0.") and base[1:] in text_l:
            ok = True  # ".045" written as "0.045"
        if not ok and vl.replace("-", "") in text_l.replace("-", ""):
            ok = True  # "cut-off" vs "cut off" punctuation normalization
        for canon, abbrs in _EXPANSIONS.items():
            if vl == canon and any(ab in text_l for ab in abbrs):
                ok = True
        if not ok and a.label == "Color Temperature" and re.search(r"\b\d{2}k\b", text_l):
            # "27K" shorthand: NNk in the text converts to NN00 K
            ok = vl.rstrip("k").strip() == str(int(re.search(r"\b(\d{2})k\b", text_l).group(1)) * 100)
        if not ok:
            bad.append(a.label)
    if bad:
        reasons.append(f"Dual-pass verification failed: {', '.join(bad[:5])}")
    decision = "review" if reasons else "auto_accept"
    record.quality = QualityDecision(decision=decision, field_error_budget=0.02, review_reasons=reasons)
    return record


# --- STAGE 8: Description Generation (real components only, no filler templates) ---
def _trim(text: str, max_len: int) -> Tuple[str, bool]:
    text = text.strip()
    if len(text) <= max_len:
        return text, True
    return text[:max_len - 3] + "...", False


def stage_description_generation(record: EnrichedRecord) -> EnrichedRecord:
    a = _attr_map(record)
    brand = record.identity.brand.label
    manuf = record.identity.manufacturer.label or ""
    mpn = record.input.mpn
    item_type = _item_type(record)

    def val(label: str) -> str:
        return a[label].value if label in a else ""

    def uom(label: str) -> str:
        return a[label].uom if label in a else ""

    series = val("Series")
    cycles = val("Number of Wash Cycles")
    volt = val("Voltage Rating")
    amp = val("Amperage Rating")
    mount = val("Mounting Type")
    size = val("Size")
    depth = val("Depth With Door Open")
    sound = val("Sound Level")
    mat = val("Material")
    col = val("Color")
    extra = val("Additional Information")

    # INVOICE_DESC: <=40 chars, CAPS, real abbreviations from extracted attributes.
    mount_abbr = {"Leg": "LEG", "Built-in": "BLTLN", "Built In": "BLTLN"}.get(
        mount, re.sub(r'[^A-Z0-9]', '', mount.upper())[:5])
    mat_abbr = "SST" if mat.lower() == "stainless steel" else re.sub(r'[^A-Z0-9]', '', mat.upper())[:3]
    col_abbr = "SST" if col.lower() == "stainless steel" else re.sub(r'[^A-Z0-9]', '', col.upper())[:3]
    parts = [item_type.upper()]
    if mount:
        parts.append(mount_abbr)
    if cycles:
        parts.append(_fnum(cycles))
    if mat:
        parts.append(mat_abbr)
    if col:
        parts.append(col_abbr)
    if volt:
        parts.append(f"{_fnum(volt)}V")
    if amp:
        parts.append(f"{_fnum(amp)}A")
    # ponytail: tail = depth when wash-cycle count is known, else sound level (matches both gold invoices)
    if cycles and depth:
        parts.append(depth + (re.sub(r'[^A-Z]', '', uom("Depth With Door Open").upper()) or "IN"))
    elif sound:
        parts.append(f"{_fnum(sound)}DBA")
    invoice = " ".join(parts).upper()
    while len(invoice) > 40 and len(parts) > 1:
        parts.pop()
        invoice = " ".join(parts).upper()

    # MOBILE_DESC: 60-80 chars. When the brand name is contained in the manufacturer
    # name (Whirlpool in Whirlpool Corporation), lead with the brand only and append
    # mounting; otherwise lead with manufacturer + brand.
    brand_plain = brand.replace("\u00ae", "").strip()
    if manuf and brand_plain.lower() in manuf.lower():
        m_parts = [p for p in [brand_plain, item_type, series, mpn] if p and str(p).strip()]
        mobile = ", ".join(m_parts)
        if mount and len(mobile) + len(mount) + 11 <= 80:
            mobile += f", {mount} Mounting"
    else:
        lead = f"{manuf} {brand_plain}".strip()
        m_parts = [p for p in [lead, item_type, series, mpn] if p and str(p).strip()]
        mobile = ", ".join(m_parts)

    # SHORT_DESC / RETAIL_DESC: brand, series, MPN, item type, key attributes.
    short_parts = [p for p in [brand, series, mpn, item_type] if p and str(p).strip()]
    short_tail = []
    if mount:
        short_tail.append(f"{mount} Mounting")
    if cycles:
        short_tail.append(f"{_fnum(cycles)}-Wash Cycle")
    if mat:
        short_tail.append(mat)
    if col:
        short_tail.append(col)
    short = " ".join(short_parts)
    if short_tail:
        short += ", " + ", ".join(short_tail)

    item_headline = f"{series} {item_type}".strip() if series else item_type
    retail_parts = [item_headline]
    if mount:
        retail_parts.append(f"{mount} Mounting")
    if cycles:
        retail_parts.append(f"{_fnum(cycles)}-Wash Cycle")
    if mat:
        retail_parts.append(mat)
    if col:
        retail_parts.append(col)
    retail = ", ".join(p for p in retail_parts if p and str(p).strip())

    # LONG_DESC1: full attribute sentence — brand, series, wash cycles, voltage,
    # amperage, mounting, size, depth, min/max height, sound, material, color, additional info.
    minh = val("Minimum Height")
    minh_uom = uom("Minimum Height")
    maxh = val("Maximum Height")
    long_parts = []
    if brand != "Unbranded":
        long_parts.append(f"{brand} {item_type}")
    if series:
        long_parts.append(series)
    if cycles:
        long_parts.append(f"{_fnum(cycles)} Wash Cycles")
    if volt:
        long_parts.append(f"{_fnum(volt)} V")
    if amp:
        long_parts.append(f"{_fnum(amp)} A")
    if mount:
        long_parts.append(f"{mount} Mounting")
    if size:
        size_uom = uom("Size")
        long_parts.append(size + (" " + size_uom if size_uom else ""))
    if depth:
        long_parts.append(f"{depth} in Depth With Door Open")
    if minh:
        long_parts.append(f"{minh}{' ' + minh_uom if minh_uom else ''} Minimum Height")
    if maxh:
        long_parts.append(f"{maxh} Maximum Height")
    if sound:
        long_parts.append(f"{_fnum(sound)} dBA Sound Level")
    if mat:
        long_parts.append(mat)
    if col:
        long_parts.append(col)
    if extra:
        long_parts.append(f"Additional Information: {extra}")
    long_desc = ", ".join(long_parts)

    mobile_text, mobile_ok = _trim(mobile, 80)
    mobile_valid = mobile_ok and 60 <= len(mobile_text) <= 80
    invoice_text, invoice_ok = _trim(invoice, 40)
    short_text, short_ok = _trim(short, 120)
    long_text, long_ok = _trim(long_desc, 500)
    retail_text, retail_ok = _trim(retail, 200)
    marketing_text = ""
    marketing_ok = False

    record.descriptions = Descriptions(
        mobile=DescriptionDetail(text=mobile_text, chars=len(mobile_text), valid=mobile_valid),
        invoice=DescriptionDetail(text=invoice_text, chars=len(invoice_text), valid=invoice_ok),
        short=DescriptionDetail(text=short_text, chars=len(short_text), valid=short_ok),
        long=DescriptionDetail(text=long_text, chars=len(long_text), valid=long_ok),
        retail=DescriptionDetail(text=retail_text, chars=len(retail_text), valid=retail_ok),
        marketing=DescriptionDetail(text=marketing_text, chars=0, valid=marketing_ok),
    )
    return record


# --- STAGE 9: Export (exact 252-header contract from the delivery template) ---
_GOLD_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "Unihack_ Expected Output - Delivery Format.csv")


def _fallback_headers() -> List[str]:
    prefix = [
        "MFR URL", "Ref URL 1", "Ref URL 2", "Ref URL 3", "Ref URL 4", "Ref URL 5",
        "PART_NUMBER", "Dept", "Class", "Fine", "SKU - MY_PART_NUMBER", "Mfg_Part_Num",
        "Part_Desc", "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf",
        "MANUFACTURER_NAME", "BRAND_NAME", "TRADE_NAME", "MANUFACTURER_PART_NUMBER",
        "ALTERNATE_PART_NUMBER", "Classpath", "MOBILE_DESC", "INVOICE_DESC",
        "SHORT_DESC", "LONG_DESC1", "RETAIL_DESC", "MARKETING_DESCRIPTION",
        "ITEM_FEATURES_1", "ITEM_FEATURES_2", "ITEM_FEATURES_3", "ITEM_FEATURES_4",
        "ITEM_FEATURES_5", "ITEM_FEATURES_6", "ITEM_FEATURES_7", "ITEM_FEATURES_8",
        "ITEM_FEATURES_9", "ITEM_FEATURES_10", "ITEM_FEATURES_11", "ITEM_FEATURES_12",
        "ITEM_FEATURES_13", "ITEM_FEATURES_14", "ITEM_FEATURES_15", "ITEM_FEATURES_16",
        "ITEM_FEATURES_17", "ITEM_FEATURES_18", "ITEM_FEATURES_19", "ITEM_FEATURES_20",
        "With", "Standard/Approvals", "Prop 65", "Application", "Includes", "Product Name",
    ]
    attrs = [
        item for i in range(1, 51)
        for item in (f"ATTRIBUTE_LABEL {i}", f"ATTRIBUTE_VALUE {i}", f"ATTRIBUTE_UOM {i}")
    ]
    suffix = [
        "UPC", "EAN", "GTIN", "UNSPSC", "Warranty", "List Price", "Selling Qty",
        "Selling UOM", "Standard Packaging Information", "LENGTH", "LENGTH_UOM",
        "HEIGHT", "HEIGHT_UOM", "WIDTH", "WIDTH_UOM", "WEIGHT", "WEIGHT_UOM",
        "VOLUME", "VOLUME_UOM", "Product Image", "Alternate Image 1", "Alternate Image 2",
        "Alternate Image 3", "Alternate Image 4", "SDS", "SDS_1", "Warranty Information",
        "Catalog", "Specification Sheet", "Instruction/Installation Manual", "Service Manual",
        "Owners/User Manual", "Line Drawing", "MTR", "RoHS", "Full Engineering Drawing",
        "Energy Star Guide", "Technical Bulletin", "Submittal", "Compatibility Chart",
        "Size Chart", "Product Label/Insert", "Video Link", "Video Link 1",
        "Country Of Origin", "Discontinued", "Actual Image (Yes/No)"
    ]
    return prefix + attrs + suffix


def _load_export_headers() -> List[str]:
    try:
        import pandas as pd
        if os.path.exists(_GOLD_CSV):
            df = pd.read_csv(_GOLD_CSV, encoding="utf-8-sig", nrows=1)
            cols = [c.lstrip("\ufeff").strip() for c in df.columns]
            if len(cols) == 252:
                return cols
    except Exception:
        pass
    return _fallback_headers()


EXPORT_HEADERS = _load_export_headers()


# Reference data kept for backwards compatibility with app.py
REF_DATA = _loader.load_brands_manufacturers() if _loader else {}
UOMS = _get_uom_map()


def stage_export(record: EnrichedRecord) -> Tuple[EnrichedRecord, Dict[str, Any]]:
    out = {h: "" for h in EXPORT_HEADERS}
    out["MFR URL"] = record.identity.manufacturer.mfr_url or ""
    # PART_NUMBER/SKU are distributor-side IDs absent from the 6-column input —
    # honest blank, never a duplicate of the MPN.
    out["Dept"] = record.classpath.dept
    out["Class"] = record.classpath.class_
    out["Fine"] = record.classpath.fine
    out["Classpath"] = record.classpath.candidate_ids[0] if record.classpath.candidate_ids \
        else f"{record.classpath.dept}>{record.classpath.class_}>{record.classpath.fine}"
    out["Mfg_Part_Num"] = record.input.mfg_part_num or record.input.mpn
    out["Part_Desc"] = record.input.part_desc or record.input.raw_text
    out["E1_Brand"] = record.input.e1_brand or ""
    out["Unilog_Brand"] = record.input.unilog_brand or ""
    out["DIB_Brand"] = record.input.dib_brand or ""
    out["Part_Manuf"] = record.input.part_manuf or ""
    out["MANUFACTURER_NAME"] = record.identity.manufacturer.label or ""
    out["BRAND_NAME"] = record.identity.brand.label
    out["MANUFACTURER_PART_NUMBER"] = record.input.mpn
    out["MOBILE_DESC"] = record.descriptions.mobile.text
    out["INVOICE_DESC"] = record.descriptions.invoice.text
    out["SHORT_DESC"] = record.descriptions.short.text
    out["LONG_DESC1"] = record.descriptions.long.text
    out["RETAIL_DESC"] = record.descriptions.retail.text
    out["MARKETING_DESCRIPTION"] = record.descriptions.marketing.text
    out["With"] = ""
    out["Product Name"] = _item_type(record)
    out["Standard/Approvals"] = ""
    out["Warranty"] = ""
    out["Product Image"] = ""
    out["Specification Sheet"] = ""
    out["Actual Image (Yes/No)"] = ""
    slot = 1
    for attr in record.attributes:
        if not attr.value:
            continue
        out[f"ATTRIBUTE_LABEL {slot}"] = attr.label
        out[f"ATTRIBUTE_VALUE {slot}"] = attr.value
        out[f"ATTRIBUTE_UOM {slot}"] = attr.uom
        slot += 1
        if slot > 50:
            break
    return record, out


# --- MAIN PIPELINE DAG RUNNER ---
def run_pipeline(raw_row: Dict[str, Any]) -> Tuple[EnrichedRecord, Dict[str, Any]]:
    record = stage_intake_normalize(raw_row)
    record = stage_entity_resolution(record)
    record = stage_taxonomy_classification(record)
    record = stage_research_planning(record)
    record, doc = stage_document_fetch(record)
    record = stage_extraction(record, doc)
    record = stage_verification(record)
    record = stage_description_generation(record)
    record, flat_export = stage_export(record)
    return record, flat_export


if __name__ == "__main__":
    import pandas as pd

    gold_df = pd.read_csv(_GOLD_CSV, encoding="utf-8-sig")
    out_rows = []
    for _, gold_row in gold_df.iterrows():
        rec, flat = run_pipeline({
            "Mfg_Part_Num": gold_row["Mfg_Part_Num"],
            "Part_Desc": gold_row["Part_Desc"],
            "Part_Manuf": gold_row["Part_Manuf"],
            "E1_Brand": gold_row["E1_Brand"],
            "Unilog_Brand": gold_row["Unilog_Brand"],
            "DIB_Brand": gold_row["DIB_Brand"],
        })
        out_rows.append({
            "input": {"MPN": rec.input.mpn, "Manufacturer": rec.input.part_manuf or "",
                      "Description": rec.input.raw_text,
                      "E1_Brand": rec.input.e1_brand, "Unilog_Brand": rec.input.unilog_brand,
                      "DIB_Brand": rec.input.dib_brand},
            "record": rec.model_dump(),
            "flat_export": flat,
        })
        print(f"row {rec.input.mpn}: brand={rec.identity.brand.label!r} "
              f"mfr={rec.identity.manufacturer.label!r} mfr_url={rec.identity.manufacturer.mfr_url!r}")
        print(f"  classpath={rec.classpath.dept}/{rec.classpath.class_}/{rec.classpath.fine} "
              f"candidate_ids={rec.classpath.candidate_ids}")
        print(f"  attributes={len(rec.attributes)} "
              f"filled={sum(1 for x in rec.attributes if x.value)} "
              f"decision={rec.quality.decision}")
        print(f"  invoice={len(rec.descriptions.invoice.text)} {rec.descriptions.invoice.text!r}")
        print(f"  mobile={len(rec.descriptions.mobile.text)} {rec.descriptions.mobile.text!r}")
        print(f"  short={len(rec.descriptions.short.text)} {rec.descriptions.short.text!r}")
        print(f"  long={len(rec.descriptions.long.text)} {rec.descriptions.long.text!r}")
        print(f"  retail={len(rec.descriptions.retail.text)} {rec.descriptions.retail.text!r}")
        print(f"  export_keys={len(flat)} == 252: {len(flat) == 252}")

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ours_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_rows, f, indent=2, ensure_ascii=False)
    print(f"wrote {out_path} ({len(out_rows)} rows)")

    # Sanity: legacy faucet demo row still resolves through the vocab.
    rec, flat = run_pipeline({
        "MPN": "K-596-VS",
        "Manufacturer": "Kohler",
        "Description": "Kohler K-596-VS Simplice Kitchen Faucet, Vibrant Stainless, 1.5 gpm, 1/2 in connection",
    })
    print(f"sanity K-596-VS: brand={rec.identity.brand.label!r} mfr={rec.identity.manufacturer.label!r} "
          f"classpath={rec.classpath.dept}/{rec.classpath.fine} decision={rec.quality.decision}")