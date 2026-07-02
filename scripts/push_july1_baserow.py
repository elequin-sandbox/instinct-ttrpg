#!/usr/bin/env python3
"""Push all July 1 2026 card changes to Baserow table 911939.

Merges scripts/flourish_cards_batch.json (Phase 2B, 8 cards) and
scripts/pool_simplification_p4_batch.json (Phase 2C, 34 cards).

Usage:
  python3 scripts/push_july1_baserow.py           # dry-run summary
  python3 scripts/push_july1_baserow.py --push    # push to Baserow
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import push_baserow  # noqa: E402

BATCH_FILES = (
    ROOT / "scripts" / "flourish_cards_batch.json",
    ROOT / "scripts" / "pool_simplification_p4_batch.json",
)
MCP_CONFIG = ROOT / ".cursor" / "mcp.json"
CONFIG_JS = ROOT / "config.js"


def _token_from_mcp_config() -> str:
    if not MCP_CONFIG.is_file():
        return ""
    try:
        data = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
        url = data["mcpServers"]["Baserow MCP"]["args"][1]
        m = re.search(r"/mcp/([^/]+)/", url)
        return m.group(1) if m else ""
    except (KeyError, IndexError, json.JSONDecodeError):
        return ""


def load_merged_batch() -> list[dict]:
    by_id: dict[int, dict] = {}
    for path in BATCH_FILES:
        if not path.is_file():
            raise SystemExit(f"Missing batch file: {path}")
        for row in json.loads(path.read_text(encoding="utf-8")):
            by_id[row["id"]] = row
    return list(by_id.values())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    batch = load_merged_batch()
    print(f"July 1 batch: {len(batch)} unique rows")
    for item in sorted(batch, key=lambda r: r["id"]):
        fields = {k: v for k, v in item.items() if k != "id"}
        print(f"  row {item['id']}: {item.get('Card_Key')} ({len(fields)} fields)")

    if not args.push:
        print("Dry run — pass --push to update Baserow")
        return

    token = _token_from_mcp_config()
    if token:
        import os

        os.environ["BASEROW_TOKEN"] = token

    push_baserow(batch)


if __name__ == "__main__":
    main()
