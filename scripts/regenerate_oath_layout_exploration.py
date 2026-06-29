#!/usr/bin/env python3
"""Generate paladin-oath-layout-exploration.html — three layout variants of The Open Hand."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_oath_layout_variants import (  # noqa: E402
    LAYOUTS,
    OPEN_HAND,
    build_variant,
)

CSS = """\
:root{--ink:#1e1810;--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;min-height:100vh;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;margin-bottom:24px;line-height:1.55;max-width:960px;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;align-items:start;}
.sample{display:flex;flex-direction:column;gap:10px;}
.stag{font-size:10px;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;color:#e7d6ac;text-align:center;line-height:1.4;}
.stag-note{font-size:9px;font-weight:500;letter-spacing:0.2px;text-transform:none;color:#8a7a5a;display:block;margin-top:4px;}
.acc-paladin{--a:#B8860B;--ad:#976e09;--al:#e7d6ac;--ah:#f8f3e7;--at:#f5eedd;}
.kw{display:inline-block;padding:0 4px;border-radius:3px;font-weight:700;vertical-align:baseline;line-height:1.35;font-style:normal;font-family:system-ui,-apple-system,sans-serif;}
.kw-boost{background:#0F766E;color:#CCFBF1;}
.kw-resolve{background:#166534;color:#F0FDF4;}
.kw-toll{background:#B45309;color:#FFFBEB;}
.hdr{padding:7px 9px 5px;display:flex;flex-direction:column;gap:2px;flex-shrink:0;background:var(--ah);border-bottom:1px solid rgba(0,0,0,.10);}
.hdr-top{display:flex;justify-content:space-between;align-items:center;gap:6px;min-height:16px;}
.cap{display:inline-flex;align-items:center;border:1.5px solid;border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;line-height:1.35;}
.cap-neutral{border-color:#3a3320;color:#3a3320;}
.hdr-name{font-family:'EB Garamond',Georgia,serif;font-weight:700;font-size:15px;line-height:1.08;text-align:center;padding:3px 10px;margin:6px -1px 2px;color:var(--ad);background:var(--al);border-top:2px solid var(--a);border-bottom:2px solid var(--a);clip-path:polygon(0 0,100% 0,calc(100% - 11px) 50%,100% 100%,0 100%,11px 50%);}
.hdr-name[style*="text-align:left"]{clip-path:none;}
.hdr-sub{font-style:italic;font-size:9px;color:#5a4020;text-align:center;line-height:1.35;padding:0 4px 2px;}
.zone-label{font-family:system-ui,-apple-system,sans-serif;font-size:7px;letter-spacing:0.8px;text-transform:uppercase;color:#5a4020;font-weight:800;}
.rule{height:0.5px;background:#c8a96e;opacity:.45;}
.die-slot{box-sizing:border-box;}
.idtag{position:absolute;left:8px;bottom:7px;border:1.5px solid var(--a);color:var(--ad);background:var(--at);border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;line-height:1.35;}
.cardwrap{position:relative;width:2.5in;margin:0 auto;}
.cardwrap .card{box-shadow:5px 5px 0 rgba(0,0,0,.55);}
.card{position:relative;border-left:5px solid var(--a);display:flex;flex-direction:column;width:2.5in;min-height:3.5in;background:#f7f0e0;border:0.5px solid #c8a96e;font-family:system-ui,-apple-system,sans-serif;color:#241a08;overflow:hidden;}
"""

cards = "".join(
    f'<div class="sample"><div class="stag">{title}<span class="stag-note">{note}</span></div>'
    f'<div class="cardwrap">{build_variant(OPEN_HAND, key)}</div></div>'
    for key, title, note in LAYOUTS
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600;700&display=swap" rel="stylesheet">
<title>Instinct RPG — Oath Layout Exploration (The Open Hand)</title>
<style>
{CSS}
</style>
</head>
<body>
<h1>Oath layout exploration</h1>
<p class="sub">Three graphic-design directions for <strong>The Open Hand</strong> — same rules text and header; only the <strong>Vow phrase zone</strong> changes. Pick a direction to implement across all oaths.</p>
<section><div class="grid">{cards}</div></section>
</body>
</html>
"""

OUT = ROOT / "paladin-oath-layout-exploration.html"
OUT.write_text(html, encoding="utf-8")
print("Wrote", OUT)
