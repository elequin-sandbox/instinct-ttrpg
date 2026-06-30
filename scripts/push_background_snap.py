#!/usr/bin/env python3
"""Push Background Snap Check HTML to Baserow table 911939."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "background_snap_batch.json"


def main() -> None:
    if not BATCH_OUT.is_file():
        raise SystemExit(f"Batch missing: {BATCH_OUT} — run build_background_snap.py --write first")
    batch = json.loads(BATCH_OUT.read_text(encoding="utf-8"))
    for item in batch:
        html = item.get("HTML", "")
        if "anc-callout-react" not in html or "bf-mill" not in html:
            raise SystemExit(f"Batch invalid: {item.get('Card_Key')}")
    print(f"Prepared {len(batch)} rows from {BATCH_OUT.name}")
    push_baserow(batch)


if __name__ == "__main__":
    main()
