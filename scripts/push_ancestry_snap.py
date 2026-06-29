#!/usr/bin/env python3
"""Push Ancestry Snap Check HTML to Baserow table 911939."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "ancestry_snap_batch.json"


def main() -> None:
    if not BATCH_OUT.is_file():
        raise SystemExit(f"Batch file missing: {BATCH_OUT} — run build_ancestry_snap.py --write first")
    batch = json.loads(BATCH_OUT.read_text(encoding="utf-8"))
    for item in batch:
        if "anc-callout" not in item.get("HTML", ""):
            raise SystemExit(f"Batch missing Snap Check block: {item.get('Card_Key')}")
    print(f"Prepared {len(batch)} rows from {BATCH_OUT.name}")
    push_baserow(batch)


if __name__ == "__main__":
    main()
