"""Tier 4: Real-World Industrial Workload E2E Tests for ELIO.

Evaluates representative multi-domain industrial catalog workloads across 8 major domains:
1. Refrigeration & Freezers (Appliances)
2. Dishwashers (Appliances)
3. Plumbing Fittings & Pipe (Plumbing)
4. Faucets & Sinks (Plumbing)
5. Electrical Wiring, Cable & Devices (Electrical)
6. Abrasives, Sanding & Grinding Discs (Hardware & Tools)
7. Power Tools & Cutting Blades (Hardware & Tools)
8. Fasteners, Lumber & Building Materials (Building Materials & Fasteners)

Total Tier 4 Test Cases: 24
"""

import sys
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline


class Tier4IndustrialWorkloadTests:
    """Test suite evaluating domain-specific catalog workflows on realistic industrial datasets."""

    # -------------------------------------------------------------------------
    # 1. Refrigeration & Freezers
    # -------------------------------------------------------------------------
    def test_w1_01_french_door_refrigerator(self):
        """W1.1: 25 cu ft French Door Refrigerator with Ice & Water Dispenser."""
        raw = {
            "Mfg_Part_Num": "WRF535SWHZ",
            "Part_Desc": "Whirlpool 25 cu ft French Door Refrigerator Fingerprint Resistant Stainless Steel",
            "Part_Manuf": "Whirlpool",
            "E1_Brand": "Whirlpool",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Appliances"
        assert flat["BRAND_NAME"] == "Whirlpool"
        assert len(flat) == 252

    def test_w1_02_commercial_chest_freezer(self):
        """W1.2: 15 cu ft Chest Freezer with Defrost Drain."""
        raw = {
            "Mfg_Part_Num": "FFFC15M4TW",
            "Part_Desc": "Frigidaire 14.8 cu ft Chest Freezer White with Power-on Indicator Light",
            "Part_Manuf": "Frigidaire",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Appliances"
        assert "FRIGIDAIRE" in flat["BRAND_NAME"]

    def test_w1_03_undercounter_beverage_center(self):
        """W1.3: Undercounter Beverage Center with Glass Door."""
        raw = {
            "Mfg_Part_Num": "WUB50X24HZ",
            "Part_Desc": "Whirlpool 24 in Undercounter Beverage Center with LED Interior Lighting",
            "Part_Manuf": "Whirlpool",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Appliances"

    # -------------------------------------------------------------------------
    # 2. Dishwashers
    # -------------------------------------------------------------------------
    def test_w2_01_built_in_quiet_dishwasher(self):
        """W2.1: 24 in Built-In Dishwasher Stainless Steel 48 dBA 5 Cycles."""
        raw = {
            "Mfg_Part_Num": "WDTS7024RZ",
            "Part_Desc": "Whirlpool 24 in Built-In Dishwasher Stainless Steel 5 Wash Cycles 48 dBA",
            "Part_Manuf": "Whirlpool",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Dishwashers"
        assert flat["BRAND_NAME"] == "Whirlpool"
        assert len(flat["INVOICE_DESC"]) <= 40

    def test_w2_02_gallery_dual_orbit_clean_dishwasher(self):
        """W2.2: Frigidaire Gallery 24 in Dishwasher with OrbitClean."""
        raw = {
            "Mfg_Part_Num": "PDSH4816AF",
            "Part_Desc": "Frigidaire Gallery 24 in Built-In Dishwasher Stainless Steel 49 dBA",
            "Part_Manuf": "Frigidaire",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Dishwashers"
        assert "FRIGIDAIRE" in flat["BRAND_NAME"]

    def test_w2_03_front_control_lg_quadwash_dishwasher(self):
        """W2.3: LG QuadWash Dishwasher with distributor masking in Part_Manuf."""
        raw = {
            "Mfg_Part_Num": "LDFN4542S",
            "Part_Desc": "LG QuadWash Front Control Dishwasher Stainless Steel 48 dBA",
            "Part_Manuf": "Appliance Dealers Co-Op (APPDE)",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Dishwashers"
        assert flat["BRAND_NAME"] == "LG"

    # -------------------------------------------------------------------------
    # 3. Plumbing Fittings & Pipe
    # -------------------------------------------------------------------------
    def test_w3_01_copper_pressure_elbow(self):
        """W3.1: 3/4 in 90-Degree Copper Pressure Elbow C x C."""
        raw = {
            "Mfg_Part_Num": "607-3/4",
            "Part_Desc": "Nibco 3/4 in 90 Degree Copper Elbow Cup x Cup Pressure Fitting",
            "Part_Manuf": "Nibco",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Plumbing"
        assert "Fitting" in rec.classpath.class_ or "Fittings" in rec.classpath.fine

    def test_w3_02_schedule_40_pvc_coupling(self):
        """W3.2: 2 in Schedule 40 PVC Coupling Socket x Socket."""
        raw = {
            "Mfg_Part_Num": "PVC-00100-1000",
            "Part_Desc": "Charlotte Pipe 2 in PVC Schedule 40 Coupling Slip x Slip White",
            "Part_Manuf": "Charlotte Pipe",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Plumbing"

    def test_w3_03_brass_threaded_pipe_nipple(self):
        """W3.3: 1/2 in x 3 in Lead-Free Brass Pipe Nipple NPT."""
        raw = {
            "Mfg_Part_Num": "BN-12-30",
            "Part_Desc": "Mueller 1/2 in x 3 in Brass Pipe Nipple MPT x MPT",
            "Part_Manuf": "Mueller",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Plumbing"

    # -------------------------------------------------------------------------
    # 4. Faucets & Sinks
    # -------------------------------------------------------------------------
    def test_w4_01_pull_down_kitchen_faucet(self):
        """W4.1: Delta Leland Pull-Down Kitchen Faucet with ShieldSpray Chrome 1.8 gpm."""
        raw = {
            "Mfg_Part_Num": "9178-DST",
            "Part_Desc": "Delta Faucet Leland Single Handle Pull-Down Kitchen Faucet Chrome 1.8 gpm",
            "Part_Manuf": "Delta Faucet",
        }
        rec, flat = run_pipeline(raw)
        assert "Faucet" in rec.classpath.fine or "Faucets" in rec.classpath.class_
        assert flat["BRAND_NAME"] == "Delta Faucet"

    def test_w4_02_commercial_two_handle_lavatory_faucet(self):
        """W4.2: Moen Commercial 4 in Centerset Two-Handle Bathroom Faucet 1.2 gpm."""
        raw = {
            "Mfg_Part_Num": "8215",
            "Part_Desc": "Moen Commercial M-Bition 4 in Centerset Lavatory Faucet Chrome 1.2 gpm",
            "Part_Manuf": "Moen",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Plumbing"
        assert flat["BRAND_NAME"] == "Moen"

    def test_w4_03_stainless_steel_undermount_kitchen_sink(self):
        """W4.3: Kohler 33x22 in Undermount Double Bowl Stainless Steel Kitchen Sink."""
        raw = {
            "Mfg_Part_Num": "K-3821-4-NA",
            "Part_Desc": "Kohler Vault 33 in x 22 in Stainless Steel Undermount Double Equal Kitchen Sink",
            "Part_Manuf": "Kohler",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Plumbing"
        assert flat["BRAND_NAME"] == "Kohler"

    # -------------------------------------------------------------------------
    # 5. Electrical Wiring & Devices
    # -------------------------------------------------------------------------
    def test_w5_01_romex_nm_b_building_wire(self):
        """W5.1: 250 ft 12/2 Non-Metallic Romex Copper Wire 600V."""
        raw = {
            "Mfg_Part_Num": "28828228",
            "Part_Desc": "Southwire 250 ft 12/2 Solid Copper Romex SIMpull NM-B Wire 600V Yellow",
            "Part_Manuf": "Southwire",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Electrical"
        assert flat["BRAND_NAME"] == "Southwire"

    def test_w5_02_gfci_tamper_resistant_receptacle(self):
        """W5.2: 20 Amp 125V Self-Test Tamper-Resistant GFCI Outlet."""
        raw = {
            "Mfg_Part_Num": "2097TRW",
            "Part_Desc": "Pass & Seymour 20 Amp 125V Self-Test Tamper-Resistant GFCI Receptacle White",
            "Part_Manuf": "Legrand",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Electrical"

    def test_w5_03_industrial_load_center(self):
        """W5.3: 200 Amp 30-Space 60-Circuit Main Breaker Indoor Load Center."""
        raw = {
            "Mfg_Part_Num": "BR3060B200",
            "Part_Desc": "Eaton 200 Amp 30-Space 60-Circuit Main Breaker Load Center NEMA 1",
            "Part_Manuf": "Eaton Corporation",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Electrical"
        assert flat["BRAND_NAME"] == "Eaton"

    # -------------------------------------------------------------------------
    # 6. Abrasives, Sanding & Grinding Discs
    # -------------------------------------------------------------------------
    def test_w6_01_hookit_clean_sanding_disc(self):
        """W6.1: 3M Cubitron II 5 in Hookit Sanding Disc 80+ Grit."""
        raw = {
            "Mfg_Part_Num": "3M-7100096",
            "Part_Desc": "3M Cubitron II 5 in Hookit Clean Sanding Disc 80 Grit Multi-Hole 50 pk",
            "Part_Manuf": "3M",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Hardware & Tools"
        assert "3M" in flat["BRAND_NAME"]

    def test_w6_02_type_27_grinding_wheel(self):
        """W6.2: DEWALT 4-1/2 in x 1/4 in Type 27 Metal Grinding Wheel 5/8-11 Hub."""
        raw = {
            "Mfg_Part_Num": "DW4514",
            "Part_Desc": "DEWALT 4-1/2 in x 1/4 in x 5/8-11 Type 27 General Purpose Metal Grinding Wheel",
            "Part_Manuf": "DEWALT",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Hardware & Tools"
        assert flat["BRAND_NAME"] == "DEWALT"

    def test_w6_03_high_performance_sanding_belt(self):
        """W6.3: Norton 3 in x 21 in 120 Grit Aluminum Oxide Sanding Belt 5 pk."""
        raw = {
            "Mfg_Part_Num": "NOR-321-120",
            "Part_Desc": "Norton 3 in x 21 in 120 Grit Heavy Duty Sanding Belt 5 pk",
            "Part_Manuf": "Norton Abrasives",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.dept == "Hardware & Tools"

    # -------------------------------------------------------------------------
    # 7. Power Tools & Cutting Blades
    # -------------------------------------------------------------------------
    def test_w7_01_cordless_brushless_angle_grinder(self):
        """W7.1: DEWALT 20V MAX XR 4-1/2 in Brushless Paddle Switch Angle Grinder."""
        raw = {
            "Mfg_Part_Num": "DCG413B",
            "Part_Desc": "DEWALT 20V MAX XR 4-1/2 in Brushless Cordless Angle Grinder (Tool Only) 9000 RPM",
            "Part_Manuf": "DEWALT",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Angle Grinders"
        assert flat["BRAND_NAME"] == "DEWALT"

    def test_w7_02_framing_carbide_saw_blade(self):
        """W7.2: Diablo 7-1/4 in x 24-Teeth Tracking Point Carbide Framing Saw Blade."""
        raw = {
            "Mfg_Part_Num": "D0724A",
            "Part_Desc": "Diablo 7-1/4 in. x 24-Teeth Tracking Point Framing Saw Blade 5/8 in Arbor",
            "Part_Manuf": "Freud Inc.",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Diablo"

    def test_w7_03_hammer_drill_driver_kit(self):
        """W7.3: Milwaukee M18 FUEL 1/2 in Hammer Drill Kit with 2 Batteries."""
        raw = {
            "Mfg_Part_Num": "2804-22",
            "Part_Desc": "Milwaukee M18 FUEL 1/2 in Cordless Hammer Drill Driver Kit 18V Brushless",
            "Part_Manuf": "Milwaukee Electric Tool",
        }
        rec, flat = run_pipeline(raw)
        assert flat["BRAND_NAME"] == "Milwaukee"
        assert rec.classpath.dept == "Hardware & Tools"

    # -------------------------------------------------------------------------
    # 8. Fasteners, Lumber & Building Materials
    # -------------------------------------------------------------------------
    def test_w8_01_acoustic_ceiling_tile(self):
        """W8.1: Armstrong 2 ft x 4 ft Fissured Acoustic Ceiling Tile White."""
        raw = {
            "Mfg_Part_Num": "ARM-1728",
            "Part_Desc": "Armstrong 2x4 White Fine Fissured Ceiling Tile 5/8 in thick",
            "Part_Manuf": "Armstrong World Industries",
        }
        rec, flat = run_pipeline(raw)
        assert rec.classpath.fine == "Ceiling Tiles"
        assert len(flat) == 252

    def test_w8_02_collated_framing_nails(self):
        """W8.1: 3 in x 0.120 in 21-Degree Plastic Collated Framing Nails 1000 pk."""
        raw = {
            "Mfg_Part_Num": "FN-3-21",
            "Part_Desc": "Bostitch 3 in x 0.120 in 21 Degree Plastic Collated Framing Nails 1000 ct",
            "Part_Manuf": "Bostitch",
        }
        rec, flat = run_pipeline(raw)
        assert "Hardware & Tools" in rec.classpath.dept or "Building Materials" in rec.classpath.dept
        assert len(flat) == 252

    def test_w8_03_dimensional_framing_lumber(self):
        """W8.3: 2x4x8 ft Kiln-Dried Douglas Fir Dimensional Stud."""
        raw = {
            "Mfg_Part_Num": "DF-248",
            "Part_Desc": "Canfor 2x4x8 ft Doug Fir Kiln-Dried Framing Lumber Stud",
            "Part_Manuf": "Canfor",
        }
        rec, flat = run_pipeline(raw)
        assert "Lumber" in rec.classpath.fine or "Building Materials" in rec.classpath.dept
        assert len(flat) == 252


def run_all_tier4_tests() -> Dict[str, Any]:
    suite = Tier4IndustrialWorkloadTests()
    test_methods = [m for m in dir(suite) if m.startswith("test_w")]
    test_methods.sort()
    
    passed = 0
    failed = 0
    failures = []
    
    print(f"\n=======================================================")
    print(f"  RUNNING TIER 4: INDUSTRIAL WORKLOAD SUITE ({len(test_methods)} TESTS)")
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
    print(f"Tier 4 Results: {passed} PASSED, {failed} FAILED (Total: {len(test_methods)})")
    print(f"=======================================================\n")
    
    return {
        "tier": "Tier 4",
        "total": len(test_methods),
        "passed": passed,
        "failed": failed,
        "failures": failures,
    }


if __name__ == "__main__":
    results = run_all_tier4_tests()
    sys.exit(0 if results["failed"] == 0 else 1)
