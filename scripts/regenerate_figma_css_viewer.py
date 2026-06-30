#!/usr/bin/env python3
"""Write figma-css-viewer.html — readable Figma CSS recreation with zoom."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_figma_reference_html import figma_viewer_page_html  # noqa: E402

OUT = ROOT / "figma-css-viewer.html"


def main() -> None:
    OUT.write_text(figma_viewer_page_html(), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
