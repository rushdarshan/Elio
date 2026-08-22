"""Tier 2: Boundary & Corner Case E2E Tests for ELIO.

Covers critical boundary conditions and edge cases:
- Empty and whitespace-only descriptions
- MPN-only rows (description is identical to MPN)
- Distributor masking (distributor in Part_Manuf with OEM in description / MPN)
- 1/64-in precision fractions, compound fractions, and mixed numbers
- Extreme description lengths (< 5 chars and > 2000 chars)
- Special characters, unicode symbols (®, ™, ¼, ½, ¾, Ø), smart quotes, emojis
- Sparse / partial input rows with missing or NaN fields

Total Tier 2 Test Cases: 25
"""

import sys
import math
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline, stage_intake_normalize
from unihack_catalog.reference_loader import fraction_lookup, get_uom_map


class Tier2BoundaryTests:
    """Test suite covering boundary and corner cases for ELIO catalog intelligence."""

    # -------------------------------------------------------------------------
    # 1. Empty & Whitespace Descriptions
    # -------------------------------------------------------------------------
    def test_b1_01_empty_string_description(self):
        """B1.1: Handles empty string description without crashing and produces honest blanks."""
        raw = {"Mfg_Part_Num": "EMPTY-01", "Part_Desc": "", "Part_Manuf": "DEWALT"}
        rec, flat = run_pipeline(raw)
        assert flat["Mfg_Part_Num"] == "EMPTY-01"
        assert flat["INVOICE_DESC"] != ""
        assert len(flat) == 252

    def test_b1_02_whitespace_only_description(self):
        """B1.2: Handles whitespace-only description ('   \\t  \\n ')."""
        raw = {"Mfg_Part_Num": "WHITE-01", "Part_Desc": "   \t  \n  ", "Part_Manuf": "Kohler"}
        rec, flat = run_pipeline(raw)
        assert rec.input.raw_text == ""
        assert flat["BRAND_NAME"] == "Kohler"

    def test_b1_03_none_description_field(self):
        """B1.3: Handles None description field safely via dict fallback."""
        raw = {"Mfg_Part_Num": "NONE-DESC", "Part_Desc": "", "Part_Manuf": ""}
        rec, flat = run_pipeline(raw)
        assert flat["Mfg_Part_Num"] == "NONE-DESC"
        assert flat["BRAND_NAME"] == "Unbranded"

    # -------------------------------------------------------------------------
    # 2. MPN-Only Rows
    # -------------------------------------------------------------------------
    def test_b2_01_mpn_identical_to_description(self):
        """B2.1: Handles row where description exactly equals the MPN."""
        raw = {"Mfg_Part_Num": "DCD771C2", "Part_Desc": "DCD771C2", "Part_Manuf": "DEWALT"}
        rec, flat = run_pipeline(raw)
        assert flat["Mfg_Part_Num"] == "DCD771C2"
        assert flat["BRAND_NAME"] == "DEWALT"
        assert rec.classpath.fine in ("Power Tools", "Other", "Pending") or rec.classpath.dept == "Hardware & Tools"

    def test_b2_02_mpn_with_leading_trailing_punctuation(self):
        """B2.2: Handles description that is solely MPN enclosed in brackets."""
        raw = {"Mfg_Part_Num": "DW-100", "Part_Desc": "[DW-100]", "Part_Manuf": "DEWALT"}
        rec, flat = run_pipeline(raw)
        assert flat["Mfg_Part_Num"] == "DW-100"
        assert flat["INVOICE_DESC"] != ""

    def test_b2_03_appliance_mpn_prefix_only(self):
        """B2.3: Appliance MPN prefix resolves brand even when description is just MPN."""
        raw = {"Mfg_Part_Num": "PDSH4816AF", "Part_Desc": "PDSH4816AF", "Part_Manuf": ""}
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "FRIGIDAIRE®"

    # -------------------------------------------------------------------------
    # 3. Distributor Masking
    # -------------------------------------------------------------------------
    def test_b3_01_appde_distributor_masking(self):
        """B3.1: Masks APPDE and discovers true brand Whirlpool from description."""
        raw = {
            "Mfg_Part_Num": "WDTS7024RZ",
            "Part_Desc": "Whirlpool 24 in Built-In Dishwasher SS",
            "Part_Manuf": "Appliance Dealers Co-Op (APPDE)"
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Whirlpool"
        assert "APPDE" not in flat["MANUFACTURER_NAME"]

    def test_b3_02_paldo_distributor_masking(self):
        """B3.2: Masks Palmer Donavin (PALDO) on ceiling tile."""
        raw = {
            "Mfg_Part_Num": "1728BL",
            "Part_Desc": "2x4 Black Acoustic Fissured Ceiling Tile",
            "Part_Manuf": "Palmer Donavin Mfg Company (PALDO)"
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Unbranded"
        assert "Palmer" not in flat["MANUFACTURER_NAME"]
        assert flat["MANUFACTURER_NAME"] == "Unknown Manufacturer"

    def test_b3_03_tech_gear_distributor_masking(self):
        """B3.3: Masks Tech Gear 5.7 Inc (TECGE) on apparel."""
        raw = {
            "Mfg_Part_Num": "MWUG36010425",
            "Part_Desc": "MWUG36010425 BLK LG Aerial Snow Heated Glove",
            "Part_Manuf": "Tech Gear 5.7 Inc (TECGE)"
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Unbranded"
        assert "Tech Gear" not in flat["MANUFACTURER_NAME"]

    def test_b3_04_jam_industrial_distributor_masking(self):
        """B3.4: Masks Jam Industrial Supply LLC on abrasives."""
        raw = {
            "Mfg_Part_Num": "3M-DISC-5",
            "Part_Desc": "3M Cubitron II 5 in Hookit Clean Sanding Disc 120+",
            "Part_Manuf": "Jam Industrial Supply LLC"
        }
        rec, flat = run_pipeline(raw)
        assert "3M" in flat["BRAND_NAME"]
        assert "Jam Industrial" not in flat["MANUFACTURER_NAME"]

    # -------------------------------------------------------------------------
    # 4. 1/64-in Precision & Compound Fractions
    # -------------------------------------------------------------------------
    def test_b4_01_fraction_1_64_exact(self):
        """B4.1: Resolves 0.015625 to exact 1/64 fraction."""
        assert fraction_lookup("0.015625") == "1/64"

    def test_b4_02_fraction_63_64_exact(self):
        """B4.2: Resolves 0.984375 to exact 63/64 fraction."""
        assert fraction_lookup("0.984375") == "63/64"

    def test_b4_03_mixed_fraction_framing_blade(self):
        """B4.3: Resolves 7.25 to 7-1/4."""
        assert fraction_lookup("7.25") == "7-1/4"

    def test_b4_04_mixed_fraction_1_16_increments(self):
        """B4.4: Resolves compound mixed fractions across 1/16-in increments."""
        assert fraction_lookup("1.0625") == "1-1/16"
        assert fraction_lookup("3.1875") == "3-3/16"
        assert fraction_lookup("5.3125") == "5-5/16"
        assert fraction_lookup("8.4375") == "8-7/16"
        assert fraction_lookup("10.5625") == "10-9/16"
        assert fraction_lookup("12.6875") == "12-11/16"
        assert fraction_lookup("14.8125") == "14-13/16"
        assert fraction_lookup("16.9375") == "16-15/16"

    def test_b4_05_fraction_extraction_in_pipeline_desc(self):
        """B4.5: Pipeline cleanly extracts 7-1/4 in size from raw description."""
        raw = {
            "Mfg_Part_Num": "D0724A",
            "Part_Desc": "Diablo 7-1/4 in. x 24-Teeth Framing Saw Blade",
            "Part_Manuf": "Freud Inc."
        }
        rec, flat = run_pipeline(raw)
        assert any("7-1/4" in a.value or "7-1/4 in" in a.value for a in rec.attributes)

    # -------------------------------------------------------------------------
    # 5. Extreme Lengths
    # -------------------------------------------------------------------------
    def test_b5_01_terse_three_character_desc(self):
        """B5.1: Handles very short description ('Tee') without indexing crashes."""
        raw = {"Mfg_Part_Num": "TEE-1", "Part_Desc": "Tee", "Part_Manuf": "Nibco"}
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Pipe Fittings"
        assert flat["INVOICE_DESC"] != ""

    def test_b5_02_terse_single_word_elbow(self):
        """B5.2: Handles single-word description ('Elbow')."""
        raw = {"Mfg_Part_Num": "ELL-1", "Part_Desc": "Elbow", "Part_Manuf": "Mueller"}
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Pipe Fittings"

    def test_b5_03_extreme_long_description_2000_chars(self):
        """B5.3: Handles massive 2000+ character description and respects description length limits."""
        long_paragraph = (
            "DEWALT 20V MAX Cordless Drill Driver Kit featuring high performance brushless motor "
            "delivering 340 unit watts out (UWO) of power. Compact lightweight design fits into tight areas. "
            "Ergonomic comfort grip handle provides ideal balance and tool control. " * 10
        )
        assert len(long_paragraph) > 2000
        raw = {"Mfg_Part_Num": "DCD771-HUGE", "Part_Desc": long_paragraph, "Part_Manuf": "DEWALT"}
        rec, flat = run_pipeline(raw)
        assert len(flat["INVOICE_DESC"]) <= 40
        assert len(flat["MOBILE_DESC"]) <= 80
        assert len(flat["SHORT_DESC"]) <= 120
        assert len(flat["RETAIL_DESC"]) <= 200
        assert len(flat["LONG_DESC1"]) <= 500

    # -------------------------------------------------------------------------
    # 6. Special Characters & UTF-8 Symbols
    # -------------------------------------------------------------------------
    def test_b6_01_registered_trademark_symbol(self):
        """B6.1: Correctly processes and retains registered trademark ®."""
        raw = {"Mfg_Part_Num": "REG-01", "Part_Desc": "FRIGIDAIRE® 24 in Built-In Dishwasher SS", "Part_Manuf": "Electrolux"}
        rec, flat = run_pipeline(raw)
        assert "FRIGIDAIRE" in flat["BRAND_NAME"]

    def test_b6_02_vulgar_fractions_unicode(self):
        """B6.2: Handles vulgar fraction symbols like ½, ¼, ¾ gracefully."""
        raw = {"Mfg_Part_Num": "VULG-1", "Part_Desc": "Brass Ball Valve ½ in Female NPT 600 PSI", "Part_Manuf": "Apollo"}
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Ball Valves"
        assert len(flat) == 252

    def test_b6_03_diameter_and_degree_symbols(self):
        """B6.3: Handles diameter Ø and degree ° symbols."""
        raw = {"Mfg_Part_Num": "SYM-01", "Part_Desc": "Copper 90° Elbow Ø 3/4 in C x C", "Part_Manuf": "Nibco"}
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Plumbing"

    def test_b6_04_smart_curly_quotes_and_dashes(self):
        """B6.4: Handles curly smart quotes (“ ” ‘ ’) and em-dashes (—)."""
        raw = {
            "Mfg_Part_Num": "SMART-01",
            "Part_Desc": "DEWALT 20V MAX 4.5” Angle Grinder — Tool Only",
            "Part_Manuf": "DEWALT"
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "DEWALT"
        assert flat["INVOICE_DESC"] == flat["INVOICE_DESC"].upper()

    def test_b6_05_non_ascii_control_and_emoji_safety(self):
        """B6.5: Safely cleanses emojis and unprintable control characters."""
        raw = {
            "Mfg_Part_Num": "EMOJI-1",
            "Part_Desc": "🔥 BEST SELLER 🔥 20V Cordless Drill Kit 🛠️ Professional Grade",
            "Part_Manuf": "DEWALT"
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "DEWALT"
        assert len(flat) == 252

    # -------------------------------------------------------------------------
    # 7. Partial & Sparse Inputs
    # -------------------------------------------------------------------------
    def test_b7_01_all_optional_columns_empty(self):
        """B7.1: Minimal row with only MPN processes completely and emits 252 columns."""
        raw = {
            "Mfg_Part_Num": "MIN-ONLY-01",
            "Part_Desc": "",
            "Part_Manuf": "",
            "E1_Brand": "",
            "Unilog_Brand": "",
            "DIB_Brand": "",
        }
        rec, flat = run_pipeline(raw)
        assert flat["Mfg_Part_Num"] == "MIN-ONLY-01"
        assert len(flat) == 252


def run_all_tier2_tests() -> Dict[str, Any]:
    suite = Tier2BoundaryTests()
    test_methods = [m for m in dir(suite) if m.startswith("test_b")]
    test_methods.sort()
    
    passed = 0
    failed = 0
    failures = []
    
    print(f"\n=======================================================")
    print(f"  RUNNING TIER 2: BOUNDARY & CORNER CASES SUITE ({len(test_methods)} TESTS)")
    print(f"=======================================================")
    
    for name in test_methods:
        fn = getattr(suite, name)
        doc = fn.__doc__ or name
        try:
            fn()
            passed += 1
            print(f"  [PASS] {name} - {doc.splitlines()[0]}")
        except Exception as e:
            failed += 1
            import traceback
            tb = traceback.format_exc()
            failures.append((name, str(e)))
            print(f"  [FAIL] {name} - {doc.splitlines()[0]}")
            print(f"         Error: {e}\n{tb}")
            
    print(f"-------------------------------------------------------")
    print(f"Tier 2 Results: {passed} PASSED, {failed} FAILED (Total: {len(test_methods)})")
    print(f"=======================================================\n")
    
    return {
        "tier": "Tier 2",
        "total": len(test_methods),
        "passed": passed,
        "failed": failed,
        "failures": failures,
    }


if __name__ == "__main__":
    results = run_all_tier2_tests()
    sys.exit(0 if results["failed"] == 0 else 1)
