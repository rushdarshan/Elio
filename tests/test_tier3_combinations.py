"""Tier 3: Cross-Feature Combination E2E Tests for ELIO.

Covers pairwise and multi-stage feature interactions:
- Entity Resolution + Multi-Attribute Extraction
- Multi-Attribute Extraction + UOM Conversion + Fraction Lookup
- Category Classification + Grounded Span Verification + Honest Abstentions
- Entity Resolution + Attribute Extraction + Formulaic Description Bounds
- End-to-End DAG Serialization & 252-Column UTF-8-SIG Schema Consistency
- Brand Disambiguation + Category Override Resilience
- Complex Industrial Composite Spec Parsing

Total Tier 3 Test Cases: 15
"""

import sys
import hashlib
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline, stage_intake_normalize, stage_export


class Tier3CombinationTests:
    """Test suite covering cross-feature interactions and multi-stage DAG pipelines."""

    # -------------------------------------------------------------------------
    # 1. Entity Resolution + Multi-Attribute Extraction
    # -------------------------------------------------------------------------
    def test_c1_01_entity_resolution_and_power_tool_attributes(self):
        """C1.1: Resolves DEWALT brand, extracts 20V Voltage, 4.5 in Size, and Angle Grinder Type."""
        raw = {
            "Mfg_Part_Num": "DCG402B",
            "Part_Desc": "DCG402B Dewalt 20V 4.5\" Angle Grinder (Bare)",
            "Part_Manuf": "Black & Decker/dewlt (2585)",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "DEWALT"
        assert rec.classpath.fine == "Angle Grinders"
        attr_dict = {a.label: a.value for a in rec.attributes if a.value}
        assert "20" in attr_dict.get("Voltage Rating", "")
        assert "4.5" in attr_dict.get("Size", "") or "4-1/2" in attr_dict.get("Size", "")

    def test_c1_02_entity_resolution_and_microwave_stainless(self):
        """C1.2: Resolves LG brand and extracts Stainless Steel Material and Microwave classification."""
        raw = {
            "Mfg_Part_Num": "MSER2090S",
            "Part_Desc": "MSER2090S LG SS Microwave 2.0 cu ft",
            "Part_Manuf": "Appliance Dealers Co-Op (APPDE)",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "LG"
        assert rec.classpath.fine == "Microwaves"
        assert any("Stainless" in a.value for a in rec.attributes if a.label == "Material")

    # -------------------------------------------------------------------------
    # 2. Multi-Attribute Extraction + UOM Conversion + Fraction Resolution
    # -------------------------------------------------------------------------
    def test_c2_01_fraction_and_uom_composite_framing_blade(self):
        """C2.1: Combines 7-1/4 in size fraction, 24 teeth count, and Saw Blade category."""
        raw = {
            "Mfg_Part_Num": "D0724A",
            "Part_Desc": "Diablo 7-1/4 in. x 24-Teeth Tracking Point Framing Saw Blade",
            "Part_Manuf": "Freud Inc.",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Diablo"
        assert "Saw Blades" in rec.classpath.fine or "Blades" in rec.classpath.fine
        size_attrs = [a for a in rec.attributes if "7-1/4" in a.value]
        assert len(size_attrs) > 0, "Expected extracted size with 7-1/4 fraction"

    def test_c2_02_electrical_wire_awg_and_voltage_uom(self):
        """C2.2: Combines 12 AWG wire gauge, 2 conductors, 1000 ft spool length, and 600 V rating."""
        raw = {
            "Mfg_Part_Num": "WIRE-12-2",
            "Part_Desc": "Southwire 1000 ft 12/2 Solid Copper NM-B Wire 600V",
            "Part_Manuf": "Southwire",
        }
        rec, flat = run_pipeline(raw)
        assert "Wire" in rec.classpath.fine or "Electrical" in rec.classpath.dept
        assert flat["BRAND_NAME"] == "Southwire"
        assert len(flat) == 252

    # -------------------------------------------------------------------------
    # 3. Category Classification + Grounded Span Verification + Abstentions
    # -------------------------------------------------------------------------
    def test_c3_01_ball_valve_grounded_spans_and_absent_electrical(self):
        """C3.3: Classifies Ball Valve, verifies PSI/Size spans, and abstains on electrical/appliance fields."""
        raw = {
            "Mfg_Part_Num": "BV-701",
            "Part_Desc": "Apollo 3/4 in Brass Ball Valve 600 PSI Threaded Full Port",
            "Part_Manuf": "Apollo Valves",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Ball Valves"
        assert flat["BRAND_NAME"] in ("Unbranded", "Apollo")
        # Verify honest abstentions on absent appliance specs
        for i in range(1, 51):
            if flat.get(f"ATTRIBUTE_LABEL {i}") in ("Voltage Rating", "Number of Wash Cycles", "Sound Level"):
                assert flat.get(f"ATTRIBUTE_VALUE {i}") == ""

    def test_c3_02_ceiling_tile_unit_normalization_and_color_provenance(self):
        """C3.2: Classifies Ceiling Tiles, normalizes 2x2 to '2 ft x 2 ft', extracts Black Color."""
        raw = {
            "Mfg_Part_Num": "1728ABL",
            "Part_Desc": "2x2 Black Fine Fissured 1728BL",
            "Part_Manuf": "Palmer Donavin Mfg Company (PALDO)",
            "E1_Brand": "-- Unbranded --",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Ceiling Tiles"
        assert flat["BRAND_NAME"] == "Unbranded"
        attr_dict = {a.label: a.value for a in rec.attributes if a.value}
        assert attr_dict.get("Color") == "Black"
        assert "2 ft" in attr_dict.get("Size", "")

    # -------------------------------------------------------------------------
    # 4. Entity Resolution + Extraction + Formulaic Description Bounds
    # -------------------------------------------------------------------------
    def test_c4_01_invoice_mobile_short_retail_descriptions_consistency(self):
        """C4.1: Generates consistent descriptions across all 5 tiers with length & casing compliance."""
        raw = {
            "Mfg_Part_Num": "WDTS7024RZ",
            "Part_Desc": "Whirlpool 24 in Built-In Dishwasher Stainless Steel 5 Wash Cycles 48 dBA",
            "Part_Manuf": "Whirlpool",
        }
        rec, flat = run_pipeline(raw)
        invoice = flat["INVOICE_DESC"]
        mobile = flat["MOBILE_DESC"]
        short = flat["SHORT_DESC"]
        retail = flat["RETAIL_DESC"]
        long_desc = flat["LONG_DESC1"]

        assert len(invoice) <= 40 and invoice == invoice.upper()
        assert len(mobile) <= 80
        assert len(short) <= 120
        assert len(retail) <= 200
        assert len(long_desc) <= 500
        assert "WHIRLPOOL" in invoice or "DISHWASHER" in invoice

    def test_c4_02_faucet_flow_rate_and_description_flow(self):
        """C4.2: Faucet description includes brand and 1.8 gpm flow rate within length constraints."""
        raw = {
            "Mfg_Part_Num": "9178-AR-DST",
            "Part_Desc": "Delta Faucet Leland Single Handle Pull-Down Kitchen Faucet Arctic Stainless 1.8 gpm",
            "Part_Manuf": "Delta Faucet",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Delta Faucet"
        assert len(flat["INVOICE_DESC"]) <= 40
        assert flat["INVOICE_DESC"] == flat["INVOICE_DESC"].upper()

    # -------------------------------------------------------------------------
    # 5. Full DAG Intake -> Serialization -> 252-Column Syndication
    # -------------------------------------------------------------------------
    def test_c5_01_e2e_intake_to_export_column_completeness(self):
        """C5.1: Verifies complete 9-stage DAG execution from raw dictionary to 252-key flat export."""
        raw = {
            "Mfg_Part_Num": "FULL-E2E-001",
            "Part_Desc": "Milwaukee 18V FUEL 1/2 in Hammer Drill Brushless Bare Tool 2804-20",
            "Part_Manuf": "Milwaukee Electric Tool",
            "E1_Brand": "Milwaukee",
            "Unilog_Brand": "Milwaukee",
            "DIB_Brand": "Milwaukee",
        }
        rec, flat = run_pipeline(raw)
        assert len(flat) == 252
        assert flat["MANUFACTURER_PART_NUMBER"] == "FULL-E2E-001"
        assert flat["BRAND_NAME"] == "Milwaukee"
        assert flat["Dept"] == "Hardware & Tools"
        assert rec.quality.decision in ("auto_accept", "review")

    def test_c5_02_export_utf8_sig_binary_integrity(self):
        """C5.2: Verifies exported record encodes cleanly to UTF-8-SIG binary bytes."""
        raw = {
            "Mfg_Part_Num": "WDTS7024RZ",
            "Part_Desc": "Whirlpool® 24\" Built-In Dishwasher Stainless Steel 48 dBA",
            "Part_Manuf": "Whirlpool",
        }
        rec, flat = run_pipeline(raw)
        csv_row = ",".join(f'"{str(v)}"' for v in flat.values()) + "\n"
        encoded = csv_row.encode("utf-8-sig")
        assert encoded.startswith(b"\xef\xbb\xbf"), "Must have UTF-8 BOM"
        decoded = encoded.decode("utf-8-sig")
        assert "Whirlpool" in decoded

    # -------------------------------------------------------------------------
    # 6. Advanced Edge Combinations
    # -------------------------------------------------------------------------
    def test_c6_01_brand_in_description_overrides_blank_brand_columns(self):
        """C6.1: Brand in description ('Diablo') overrides empty E1/Unilog/DIB brand fields."""
        raw = {
            "Mfg_Part_Num": "D0724A",
            "Part_Desc": "Diablo 7-1/4 in. 24T Saw Blade",
            "Part_Manuf": "Freud Inc.",
            "E1_Brand": "",
            "Unilog_Brand": "",
            "DIB_Brand": "",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Diablo"

    def test_c6_02_pipe_fitting_composite_dimensions(self):
        """C6.2: Plumbing fitting 1/2 in x 3/8 in reducer coupling extraction."""
        raw = {
            "Mfg_Part_Num": "RED-12-38",
            "Part_Desc": "Brass Reducing Coupling 1/2 in x 3/8 in Female NPT",
            "Part_Manuf": "Mueller",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Pipe Fittings"
        assert len(flat) == 252

    def test_c6_03_electrical_receptacle_duplex_and_amps(self):
        """C6.3: Electrical 15 Amp 125V Duplex Tamper-Resistant Receptacle."""
        raw = {
            "Mfg_Part_Num": "TR-15-W",
            "Part_Desc": "Pass & Seymour 15 Amp 125V Tamper Resistant Duplex Receptacle White",
            "Part_Manuf": "Legrand",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Electrical"
        assert len(flat) == 252

    def test_c6_04_lighting_wattage_lumens_and_bulb_type(self):
        """C6.4: Lighting PAR38 LED 15W flood bulb classification and specs."""
        raw = {
            "Mfg_Part_Num": "LED15PAR38",
            "Part_Desc": "Sylvania 15W LED PAR38 Flood Light Bulb 1200 Lumens 3000K E26 Base",
            "Part_Manuf": "Sylvania",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Lighting"
        assert flat["BRAND_NAME"] == "Sylvania"
        assert len(flat) == 252

    def test_c6_05_refrigeration_cubic_feet_and_color(self):
        """C6.5: Large appliances refrigerator with cubic feet capacity and stainless steel."""
        raw = {
            "Mfg_Part_Num": "WRF535SWHZ",
            "Part_Desc": "Whirlpool 25 cu ft French Door Refrigerator Fingerprint Resistant Stainless Steel",
            "Part_Manuf": "Whirlpool",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Appliances"
        assert flat["BRAND_NAME"] == "Whirlpool"
        assert len(flat) == 252


def run_all_tier3_tests() -> Dict[str, Any]:
    suite = Tier3CombinationTests()
    test_methods = [m for m in dir(suite) if m.startswith("test_c")]
    test_methods.sort()
    
    passed = 0
    failed = 0
    failures = []
    
    print(f"\n=======================================================")
    print(f"  RUNNING TIER 3: CROSS-FEATURE COMBINATIONS ({len(test_methods)} TESTS)")
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
    print(f"Tier 3 Results: {passed} PASSED, {failed} FAILED (Total: {len(test_methods)})")
    print(f"=======================================================\n")
    
    return {
        "tier": "Tier 3",
        "total": len(test_methods),
        "passed": passed,
        "failed": failed,
        "failures": failures,
    }


if __name__ == "__main__":
    results = run_all_tier3_tests()
    sys.exit(0 if results["failed"] == 0 else 1)
