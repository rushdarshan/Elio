"""Verify the generated content-addressed ELIO receipt."""

import argparse
import sys
from pathlib import Path

from receipt_chain import ReceiptError, ROOT, verify_receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=ROOT / "artifacts" / "receipt.json")
    args = parser.parse_args()
    print("=== ELIO CONTENT-ADDRESSED RECEIPT VERIFIER ===")
    try:
        report = verify_receipt(args.receipt)
    except (OSError, ValueError) as exc:
        print(f"[FAIL] {exc}")
        return 1
    print(f"[PASS] {report['claims']} claims across {report['rows']} rows verified")
    print(f"  receipt_sha256: {report['receipt_sha256']}")
    print(f"  source_attestation: {report['source_attestation']}")
    print("RECEIPT_CHAIN_STATUS: VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
