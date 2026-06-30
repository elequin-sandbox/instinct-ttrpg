#!/usr/bin/env python3
"""Regenerate core-leading-upright-proof.html — 4 done classes, full layout visualization."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_core_upright_html import (  # noqa: E402
    DONE_CLASSES,
    LEADING_CORE,
    CLASS_THEME,
    build_character_sheet_row,
    build_opponent_view_row,
    build_upright_flat,
    build_upright_tent,
)

CSS = """
:root{--ink:#1e1810;--gold:#c8a96e;--gold-d:#7a6030;--public:#c45c5c;--private:#6b8cce;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;min-height:100vh;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;margin-bottom:20px;line-height:1.55;max-width:980px;}
.rule-box{max-width:980px;background:#1d140b;border:1px solid #3a2c19;border-left:4px solid var(--gold);border-radius:8px;padding:14px 16px;margin-bottom:28px;font-size:12.5px;line-height:1.55;color:#cbb98e;}
.rule-box strong{color:var(--gold);}
h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);margin:36px 0 8px;padding-bottom:6px;border-bottom:1px solid #2a1d10;}
.h2-note{font-size:12px;color:#8a7a5a;margin-bottom:18px;line-height:1.55;max-width:980px;}
.grid-2{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;align-items:end;}
.grid-4{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:20px;align-items:end;}
.sample{display:flex;flex-direction:column;gap:8px;align-items:center;}
.stag{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#e7d6ac;text-align:center;}
.stag-sub{font-size:9px;color:#8a7a5a;font-style:italic;text-align:center;}

/* ── shared upright tokens (Figma 750×2100 → ~200px wide) ── */
.upright-flat,.upright-tent{--w:200px;--h:560px;font-family:'Spectral',Georgia,serif;}
.upright-outline{position:absolute;inset:4px;border:3px solid var(--a);border-radius:10px;pointer-events:none;z-index:2;}
.upright-fold{position:absolute;left:0;right:0;top:50%;border-top:1px dashed #999;z-index:5;display:flex;justify-content:center;}
.fold-label{font-family:system-ui,sans-serif;font-size:7px;color:#999;background:#fff;padding:0 6px;transform:translateY(-50%);letter-spacing:.08em;text-transform:uppercase;}

.ribbon-band{position:relative;height:28px;margin:0 10px;background:var(--ribbon);}
.ribbon-cap{position:absolute;width:20px;height:20px;top:4px;background:var(--bg);transform:rotate(45deg);}
.ribbon-cap-l{left:-10px;}.ribbon-cap-r{right:-10px;}
.ribbon-text{display:flex;align-items:center;justify-content:center;height:28px;font-size:16px;font-weight:400;letter-spacing:.04em;text-transform:uppercase;color:var(--a);text-align:center;line-height:1;}
.ribbon-text.inverted{transform:rotate(180deg);}

.upright-subtitle{font-family:'Spectral',Georgia,serif;font-style:italic;font-weight:300;font-size:8.5px;line-height:1.35;text-align:center;color:var(--ad);margin:8px 14px 4px;}
.upright-content{padding:0 14px;display:flex;flex-direction:column;gap:5px;}
.upright-zone{font-family:Inter,system-ui,sans-serif;font-size:7px;font-weight:600;line-height:1.3;color:var(--ad);text-transform:uppercase;letter-spacing:.3px;}
.upright-body{font-family:Inter,system-ui,sans-serif;font-size:7px;font-weight:600;line-height:1.45;color:#4b4b4b;}
.upright-body.italic{font-weight:400;font-style:italic;color:var(--ad);font-size:6.5px;}
.upright-footer{font-size:7px;text-align:center;text-transform:uppercase;color:var(--a);letter-spacing:.02em;margin-top:8px;padding-bottom:10px;}

.public-class-name{font-family:'Spectral',Georgia,serif;font-size:22px;font-weight:400;letter-spacing:.04em;text-transform:uppercase;color:var(--a);text-align:center;margin-top:40px;line-height:1.1;}
.public-class-name.large{font-size:26px;margin-top:20px;}

.face-tag{font-family:system-ui,sans-serif;font-size:6.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:3px 8px;border-radius:3px;margin:8px 10px 4px;display:inline-block;}
.face-tag-public{background:rgba(196,92,92,.15);color:#e8a0a0;border:1px solid rgba(196,92,92,.4);}
.face-tag-private{background:rgba(107,140,206,.15);color:#a0c0e8;border:1px solid rgba(107,140,206,.4);}

.kw{display:inline-block;padding:0 2px;border-radius:2px;font-size:6px;font-weight:700;font-family:system-ui,sans-serif;line-height:1.35;}
.kw-boost{background:#0F766E;color:#CCFBF1;}.kw-resolve{background:#166534;color:#F0FDF4;}
.kw-crit{background:#B8860B;color:#FFFDE7;}.kw-hd{background:#7F1D1D;color:#FEE2E2;}

/* ── flat unfolded die ── */
.upright-flat{position:relative;width:var(--w);height:var(--h);background:var(--bg);border-radius:10px;margin:0 auto;}
.flat-half{position:absolute;left:4px;right:4px;height:calc(50% - 8px);overflow:hidden;}
.flat-half-public{top:4px;border-radius:6px 6px 0 0;}
.flat-half-private{bottom:4px;border-radius:0 0 6px 6px;}

/* ── folded tent ── */
.upright-tent{position:relative;width:140px;margin:0 auto;}
.tent-cap{font-size:8px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;text-align:center;margin-bottom:6px;color:#8a7a5a;}
.tent-body{position:relative;background:var(--bg);border:3px solid var(--a);border-radius:8px 8px 4px 4px;min-height:200px;overflow:hidden;}
.tent-roof{height:0;border-left:70px solid transparent;border-right:70px solid transparent;border-bottom:18px solid var(--a);opacity:.25;margin:0 auto;}
.tent-face{padding:8px 6px 10px;min-height:170px;}
.tent-face-public{display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,var(--bg),rgba(0,0,0,.03));}
.view-public .tent-cap{color:#e8a0a0;}
.view-player .tent-cap{color:#a0c0e8;}

/* ── character sheet row ── */
.sheet-row{position:relative;display:grid;grid-template-columns:1fr 1fr 1.1fr;gap:12px;max-width:720px;margin:0 auto 48px;padding:24px 16px 32px;background:linear-gradient(180deg,#f8f4ee,#ece6dc);border:1px solid #bbb;border-radius:10px;}
.sheet-panel{position:relative;border:2px solid #c5c5c5;border-radius:8px;background:#fff;min-height:240px;padding:8px;}
.panel-tag{font-family:system-ui,sans-serif;font-size:7px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#a0a0a0;text-align:center;margin-bottom:4px;}
.panel-foot{font-size:8px;text-align:center;color:#666;margin-top:6px;font-style:italic;}
.panel-foot.public-read{font-style:normal;font-weight:700;letter-spacing:.06em;color:var(--a,#444);}
.sheet-card-slot{display:flex;justify-content:center;margin-top:8px;transform:scale(.85);transform-origin:top center;}
.char-sketch-box{margin:12px;border:2px solid #c5c5c5;border-radius:6px;height:80px;display:flex;align-items:center;justify-content:center;font-size:9px;color:#a0a0a0;text-transform:uppercase;}
.char-name-line{margin:8px 12px;border-top:2px solid #c5c5c5;padding-top:6px;font-size:9px;color:#a0a0a0;text-transform:uppercase;}
.char-appearance{font-size:8px;color:#555;padding:8px 12px;line-height:1.6;}
.char-name-display{font-family:'Spectral',serif;font-size:22px;text-align:center;margin-top:80px;color:#333;letter-spacing:.04em;}
.pov-arrow{position:absolute;left:50%;transform:translateX(-50%);font-size:9px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;white-space:nowrap;}
.pov-you{bottom:-28px;color:#6b8cce;}
.pov-them{top:-24px;color:#c45c5c;}
.opponent-row{opacity:.95;border-color:#c45c5c;}
.legend{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px;font-size:11px;}
.legend span{display:inline-flex;align-items:center;gap:6px;}
.legend i{display:inline-block;width:12px;height:12px;border-radius:2px;}
"""

def main() -> None:
    # Section 1: flat unfolded dies
    flat_cards = []
    for cls in DONE_CLASSES:
        d = LEADING_CORE[cls]
        flat_cards.append(
            f'<div class="sample"><div class="stag">{d["name"]}</div>'
            f'<div class="stag-sub">Unfolded die</div>{build_upright_flat(cls)}</div>'
        )

    # Section 2: tent both views per class
    tent_pairs = []
    for cls in DONE_CLASSES:
        d = LEADING_CORE[cls]
        tent_pairs.append(
            f'<div class="sample"><div class="stag">{d["name"]}</div>'
            f'<div class="stag-sub">{CLASS_THEME[cls]["label"]}</div>'
            f'<div style="display:flex;gap:12px;align-items:flex-end;">'
            f'{build_upright_tent(cls, "player")}'
            f'{build_upright_tent(cls, "public")}'
            f"</div></div>"
        )

    # Section 3: four class tents player view
    four_tents = []
    for cls in DONE_CLASSES:
        d = LEADING_CORE[cls]
        four_tents.append(
            f'<div class="sample">{build_upright_tent(cls, "player")}'
            f'<div class="stag">{d["name"]}</div></div>'
        )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Spectral:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<title>Instinct RPG — Upright Core Layout (4 classes)</title>
<style>{CSS}</style>
</head>
<body>
<h1>Upright Core — Layout Understanding</h1>
<p class="sub">Four <strong>done</strong> classes only. Leading picks locked: <strong>Rage</strong> · <strong>Ace</strong> · <strong>Bulwark</strong> · <strong>Pact</strong>. This page shows my read of the Jun 27 conversation — two-sided tent cards that fold on the dashed line and stand in the character-sheet slots.</p>

<div class="rule-box">
<strong>My understanding:</strong><br>
① <strong>Two-sided die</strong> — cut/fold one tall rectangle. Fold line at mid-height.<br>
② <strong>Private face (you)</strong> — leading Core rules: ribbon = <em>card name</em> (Rage, Ace…), subtitle, body text, footer <em>⁘ CLASS | Core ⁘</em>.<br>
③ <strong>Public face (across the table)</strong> — big <em>CLASS</em> name only (ROGUE, BARBARIAN…). Same geometry as ancestry’s public face (DWARF, ELF).<br>
④ <strong>Not Loadout</strong> — permanent tent; rules you reference all campaign. Loadout retired; primer owns setup.<br>
⑤ <strong>3-panel sheet</strong> — Class slot (left) · Ancestry slot (center) · Character slot (right, name + sketch). Opponent reads left→right: Class · Ancestry · Name.
</div>

<div class="legend">
  <span><i style="background:rgba(107,140,206,.4)"></i> Private — your eyes only</span>
  <span><i style="background:rgba(196,92,92,.4)"></i> Public — across the table</span>
</div>

<section>
<h2>1 — Unfolded print die</h2>
<p class="h2-note">Both faces visible before folding. Top half = public (class name). Bottom half = private (Core rules). Ribbon band sits on the fold line — card name on your side, class name on theirs.</p>
<div class="grid-4">{"".join(flat_cards)}</div>
</section>

<section>
<h2>2 — Folded tent: your side vs their side</h2>
<p class="h2-note">After folding into a tent and standing upright. Left = what you read. Right = what faces the table.</p>
<div class="grid-2">{"".join(tent_pairs)}</div>
</section>

<section>
<h2>3 — Your POV: 3-panel character sheet</h2>
<p class="h2-note">Rogue example — leading Core (Ace) in Class slot, Dwarf ancestry in center, character panel right. Tents stand in the cut slots.</p>
{build_character_sheet_row("rogue", "Dwarf")}
</section>

<section>
<h2>4 — Across the table: what they see</h2>
<p class="h2-note">Opponent reads your row left → right: <strong>ROGUE</strong> · <strong>DWARF</strong> · <strong>Mika</strong>. No rules text visible — only identity labels.</p>
{build_opponent_view_row("rogue", "Mika", "Dwarf")}
</section>

<section>
<h2>5 — All four done classes (your side)</h2>
<p class="h2-note">Leading Core tents — private face only.</p>
<div class="grid-4">{"".join(four_tents)}</div>
</section>

</body>
</html>
"""

    out = ROOT / "core-leading-upright-proof.html"
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
