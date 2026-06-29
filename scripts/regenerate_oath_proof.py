#!/usr/bin/env python3
"""Regenerate paladin-oath-proof.html from build_oath_html."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_oath_html import OATHS, build, build_oath_template, build_patron_template  # noqa: E402

CSS = """\
:root{--ink:#1e1810;--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;min-height:100vh;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;margin-bottom:20px;line-height:1.55;max-width:920px;}
.rule-box{max-width:920px;background:#1d140b;border:1px solid #3a2c19;border-left:4px solid #B8860B;border-radius:8px;padding:14px 16px;margin-bottom:32px;font-size:12.5px;line-height:1.55;color:#cbb98e;}
.rule-box strong{color:var(--gold);}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;align-items:start;}
.sample{display:flex;flex-direction:column;gap:10px;}
.stag{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#e7d6ac;text-align:center;}
.acc-paladin{--a:#B8860B;--ad:#976e09;--al:#e7d6ac;--ah:#f8f3e7;--at:#f5eedd;}
.acc-warlock{--a:#9A2B5E;--ad:#7e234d;--al:#ddb7c8;--ah:#f5eaef;--at:#f1e1e8;}
.kw{display:inline-block;padding:0 4px;border-radius:3px;font-size:10px;font-weight:700;vertical-align:middle;line-height:1.5;font-style:normal;font-family:system-ui,-apple-system,sans-serif;}
.kw-boost{background:#0F766E;color:#CCFBF1;}
.kw-crit{background:#B8860B;color:#FFFDE7;}
.kw-resolve{background:#166534;color:#F0FDF4;}
.kw-toll{background:#B45309;color:#FFFBEB;}
.die-slot{box-sizing:border-box;}
.hdr{padding:7px 9px 5px;display:flex;flex-direction:column;gap:2px;flex-shrink:0;background:var(--ah);border-bottom:1px solid rgba(0,0,0,.10);}
.hdr-top{display:flex;justify-content:space-between;align-items:center;gap:6px;min-height:16px;}
.cap{display:inline-flex;align-items:center;border:1.5px solid;border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;line-height:1.35;}
.cap-neutral{border-color:#3a3320;color:#3a3320;}
.hdr-name{font-family:'EB Garamond',Georgia,serif;font-weight:700;font-size:15px;line-height:1.08;text-align:center;padding:3px 10px;margin:6px -1px 2px;color:var(--ad);background:var(--al);border-top:2px solid var(--a);border-bottom:2px solid var(--a);clip-path:polygon(0 0,100% 0,calc(100% - 11px) 50%,100% 100%,0 100%,11px 50%);}
.hdr-name[style*="text-align:left"]{clip-path:none;}
.hdr-sub{font-style:italic;font-size:9px;color:#5a4020;text-align:center;line-height:1.35;padding:0 4px 2px;}
.zone-label{font-family:'EB Garamond',Georgia,serif;font-size:6px;letter-spacing:0.8px;text-transform:uppercase;color:#7a6030;}
.rule{height:0.5px;background:#c8a96e;opacity:.45;}
.hdr-blankname{display:flex;align-items:center;justify-content:center;}
.writein-line{box-sizing:border-box;}
.idtag{position:absolute;left:8px;bottom:7px;border:1.5px solid var(--a);color:var(--ad);background:var(--at);border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;line-height:1.35;}
.cardwrap{position:relative;width:2.5in;margin:0 auto;}
.cardwrap .card{box-shadow:5px 5px 0 rgba(0,0,0,.55);}
.card{position:relative;border-left:5px solid var(--a);display:flex;flex-direction:column;width:2.5in;min-height:3.5in;background:#f7f0e0;border:0.5px solid #c8a96e;font-family:system-ui,-apple-system,sans-serif;color:#241a08;overflow:hidden;}
section{margin-bottom:44px;}
h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;padding-bottom:6px;border-bottom:1px solid #2a1d10;}
.h2-note{font-size:12px;color:#8a7a5a;margin-bottom:16px;line-height:1.5;max-width:920px;}
"""

cards = "".join(
    f'<div class="sample"><div class="stag">{o["name"]}</div>'
    f'<div class="cardwrap">{build(o)}</div></div>'
    for o in OATHS
)

templates = (
    '<section><h2>Blank templates</h2><p class="h2-note">Fill title, subtitle, and word lists only. '
    "Procedure text stays printed.</p><div class=\"grid\">"
    f'<div class="sample"><div class="stag">Oath template</div><div class="cardwrap">{build_oath_template()}</div></div>'
    f'<div class="sample"><div class="stag">Patron template</div><div class="cardwrap">{build_patron_template()}</div></div>'
    "</div></section>"
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600;700&display=swap" rel="stylesheet">
<title>Instinct RPG — Paladin Oath / Scene Vow Proof</title>
<style>
{CSS}
</style>
</head>
<body>
<h1>Paladin Oath — Scene Vow Proof</h1>
<p class="sub">Five Oath Core cards + blank templates. L→R mad-lib: dice in top slots, numbered verb/noun columns. Header tags <strong>Core</strong> + <strong>Oath</strong>; ribbon reads <em>Oath of …</em></p>
<div class="rule-box">
<strong>Vow</strong> — At <strong>Scene start</strong>, place 2d6 in the top slots; each die face picks its column row. Read left → right: <em>Verb the Noun</em>. <strong>Fulfill</strong> once per Scene — <strong>Boost 2</strong> from both dice.<br><br>
<strong>Break Your Oath</strong> — Defiance → dice to <strong>Resolve</strong>; GM <strong>Toll 2</strong> vs you this scene.<br><br>
Alignment comparison (classic grid vs mad-lib): <a href="paladin-oath-layout-exploration.html" style="color:var(--gold);">paladin-oath-layout-exploration.html</a>
</div>
<section><div class="grid">{cards}</div></section>
{templates}
</body>
</html>
"""

OUT = ROOT / "paladin-oath-proof.html"
OUT.write_text(html, encoding="utf-8")
print("Wrote", OUT)
