import re

class CompetitorBaselineEnricher:
    """
    A simple baseline enricher representing the competitor UNI-Hack.
    It does basic string cleaning, regex matching for attributes, and simple description generation.
    It has no safety checks, no LOV mapping, no UOM validation, and no custody chains.
    """
    def enrich_row(self, mpn, manufacturer, raw_text):
        # 1. Clean brand/manufacturer
        resolved_brand = manufacturer.strip() if manufacturer else "Unknown"
        resolved_mfr = manufacturer.strip() if manufacturer else "Unknown"
        
        # 2. Crude taxonomy guess
        raw_text_lower = raw_text.lower() if raw_text else ""
        dept, cls, fine = "Other", "Other", "Other"
        if "faucet" in raw_text_lower or "sink" in raw_text_lower:
            dept, cls, fine = "Plumbing", "Faucets", "Kitchen Faucets"
        elif "fitting" in raw_text_lower or "coupling" in raw_text_lower or "elbow" in raw_text_lower or "adapter" in raw_text_lower:
            dept, cls, fine = "Plumbing", "Fittings", "Pipe Fittings"
        
        # 3. Basic attribute extraction (no verification or source span tracking)
        attributes = []
        
        # Match dimensions (e.g. 1/2 in, 3/4 inch, 1.5 in)
        dim_match = re.search(r'(\d+(?:\/\d+)?|\d+\.\d+)\s*(?:in|inch|\")\b', raw_text_lower)
        if dim_match:
            attributes.append({
                "label": "Size",
                "value": dim_match.group(1),
                "uom": "in",
                "source": "Regex match",
                "confidence": 0.5
            })
            
        # Match pack size (e.g. 10 pack, pk of 5, 2pc)
        pack_match = re.search(r'(?:pk|pack|pc|piece) of\s*(\d+)|\b(\d+)\s*(?:pack|pk|pcs|pc)\b', raw_text_lower)
        if pack_match:
            pack_val = pack_match.group(1) or pack_match.group(2)
            attributes.append({
                "label": "Pack Size",
                "value": pack_val,
                "uom": "EA",
                "source": "Regex match",
                "confidence": 0.5
            })

        # Match finish/color
        for color in ["chrome", "bronze", "brass", "nickel", "black"]:
            if color in raw_text_lower:
                attributes.append({
                    "label": "Finish",
                    "value": color.capitalize(),
                    "uom": "N/A",
                    "source": "Regex match",
                    "confidence": 0.5
                })
                break

        # 4. Naive description compiler (does not enforce length limits strictly)
        clean_text = raw_text.strip() if raw_text else ""
        descriptions = {
            "mobile": f"{resolved_brand} {mpn} - {clean_text[:30]}",
            "invoice": f"{resolved_brand[:10]} {mpn} {clean_text[:20]}".upper(),
            "short": f"{resolved_brand} {mpn} {clean_text[:50]}",
            "long": f"{resolved_brand} Model {mpn}. {clean_text}.",
            "retail": f"Buy {resolved_brand} {mpn} today! {clean_text}",
            "marketing": f"Introducing the high-performance {resolved_brand} {mpn}. Designed for reliability. {clean_text}"
        }

        return {
            "input": {"mpn": mpn, "raw_manufacturer": manufacturer, "raw_text": raw_text},
            "identity": {
                "brand": {"id": "B01", "label": resolved_brand, "parent": resolved_mfr},
                "manufacturer": {"id": "M01"}
            },
            "classpath": {"dept": dept, "class": cls, "fine": fine, "candidate_ids": []},
            "attributes": attributes,
            "descriptions": descriptions,
            "quality": {"decision": "auto_accept", "field_error_budget": 0.05, "review_reasons": []},
            "cost": {"llm_calls": 0, "estimated_usd": 0.0}
        }

if __name__ == "__main__":
    enricher = CompetitorBaselineEnricher()
    res = enricher.enrich_row("K-596-VS", "Kohler", "Kohler K-596-VS Simplice Kitchen Faucet, Vibrant Stainless, 1.5 gpm, 1/2 in connection")
    import pprint
    pprint.pprint(res)
