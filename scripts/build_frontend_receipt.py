"""Publish the minimal receipt index consumed by the offline cockpit drawer."""

import json
import sys
from pathlib import Path

from receipt_chain import ROOT


def main() -> int:
    source = ROOT / "artifacts" / "receipt.json"
    target = ROOT / "elio-frontend" / "public" / "data" / "receipt_chain.json"
    receipt = json.loads(source.read_text(encoding="utf-8"))
    claims = {}
    for claim in receipt["claims"]:
        key = f"{claim['mpn']}_{claim['attribute']}"
        claims[key] = {
            "mpn": claim["mpn"],
            "attribute": claim["attribute"],
            "value": claim["value"],
            "uom": claim["uom"],
            "export_column": claim["export_column"],
            "source_text": next(
                item["evidence"]["text"]
                for item in json.loads((ROOT / "artifacts" / "evidence.json").read_text(encoding="utf-8"))["rows"][claim["mpn"]]["accepted"]
                if item["attribute"] == claim["attribute"]
            ),
            "source_hash": claim["source_hash"],
            "char_span": claim["char_span"],
            "source_kind": claim["source_kind"],
            "input_row_hash": claim["input_row_hash"],
            "claim_hash": claim["claim_hash"],
            "decision_hash": claim["decision_hash"],
            "output_hash": claim["output_hash"],
            "chain_hash": claim["chain_hash"],
        }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(
            {
                "schema_version": receipt["schema_version"],
                "receipt_sha256": receipt["receipt_sha256"],
                "source_attestation": receipt["source_attestation"],
                "claims": claims,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[PASS] frontend receipt index written: {len(claims)} claims")
    return 0


if __name__ == "__main__":
    sys.exit(main())
