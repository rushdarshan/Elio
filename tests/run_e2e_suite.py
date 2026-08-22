"""Master 4-Tier E2E Test Suite Runner for ELIO (UniHack Catalog Intelligence).

Executes all 4 tiers of E2E verification:
- Tier 1: Feature Coverage (F1 through F14, >=5 tests per feature)
- Tier 2: Boundary & Corner Cases (empty descriptions, MPN-only, masking, fractions, lengths)
- Tier 3: Cross-Feature Combinations (pairwise interactions, multi-stage DAGs)
- Tier 4: Real-World Industrial Workloads (refrigeration, dishwashers, plumbing, faucets, wiring, abrasives, tools, building materials)

Produces structured summary and exits with code 0 on complete pass.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.test_tier1_features import run_all_tier1_tests
from tests.test_tier2_boundaries import run_all_tier2_tests
from tests.test_tier3_combinations import run_all_tier3_tests
from tests.test_tier4_workloads import run_all_tier4_tests


def run_master_e2e_suite() -> int:
    start_time = time.time()
    print("=" * 70)
    print("       ELIO 4-TIER COMPREHENSIVE E2E TEST SUITE RUNNER")
    print("=" * 70)
    print("Project Root: ", ROOT)
    print("Timestamp:    ", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("=" * 70)

    results: List[Dict[str, Any]] = []

    # Run Tier 1
    t1 = run_all_tier1_tests()
    results.append(t1)

    # Run Tier 2
    t2 = run_all_tier2_tests()
    results.append(t2)

    # Run Tier 3
    t3 = run_all_tier3_tests()
    results.append(t3)

    # Run Tier 4
    t4 = run_all_tier4_tests()
    results.append(t4)

    total_tests = sum(r["total"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    elapsed = time.time() - start_time

    print("\n" + "=" * 70)
    print("                       FINAL EXECUTION SUMMARY")
    print("=" * 70)
    print(f"{'Tier':<35} | {'Total':<8} | {'Passed':<8} | {'Failed':<8} | {'Status'}")
    print("-" * 70)
    for r in results:
        status = "[PASS]" if r["failed"] == 0 else "[FAIL]"
        print(f"{r['tier']:<35} | {r['total']:<8} | {r['passed']:<8} | {r['failed']:<8} | {status}")
    print("-" * 70)
    grand_status = "ALL PASS (100%)" if total_failed == 0 else f"FAILED ({total_failed} failures)"
    print(f"{'GRAND TOTAL':<35} | {total_tests:<8} | {total_passed:<8} | {total_failed:<8} | {grand_status}")
    print("=" * 70)
    print(f"Elapsed Time: {elapsed:.2f}s")
    print("=" * 70 + "\n")

    if total_failed > 0:
        print("FAILURES DETECTED:")
        for r in results:
            for name, err in r.get("failures", []):
                print(f"  - [{r['tier']}] {name}: {err}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_master_e2e_suite())
