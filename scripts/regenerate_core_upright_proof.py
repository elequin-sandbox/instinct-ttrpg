#!/usr/bin/env python3
"""Regenerate core-leading-upright-proof.html."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_core_upright_html import (  # noqa: E402
    DONE_CLASSES,
    LEADING_KEYS,
    CLASS_THEME,
    build_ancestry_double_die,
    build_character_double_die,
    build_core_double_die,
    build_sheet_row_pov,
)
from scripts.build_figma_reference_html import FIGMA_CSS, figma_section_html  # noqa: E402

CSS = """
:root{--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub,.h2-note{color:var(--gold-d);font-size:13px;line-height:1.55;max-width:980px;margin-bottom:18px;}
.rule-box{max-width:980px;background:#1d140b;border:1px solid #3a2c19;border-left:4px solid var(--gold);border-radius:8px;padding:14px 16px;margin-bottom:24px;font-size:12.5px;line-height:1.55;color:#cbb98e;}
.rule-box strong{color:var(--gold);}
h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);margin:36px 0 8px;padding-bottom:6px;border-bottom:1px solid #2a1d10;}
.grid-4{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;align-items:start;}
.grid-2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;}
.sample{display:flex;flex-direction:column;gap:8px;align-items:center;}
.stag{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#e7d6ac;text-align:center;}

/* ── double die (2× standard card height) ── */
.double-die{position:relative;width:2.5in;height:7in;background:var(--bg);border-radius:10px;margin:0 auto;font-family:'Spectral',Georgia,serif;}
.die-outline{position:absolute;inset:3px;border:3px solid var(--a);border-radius:8px;pointer-events:none;z-index:3;}
.die-fold{position:absolute;left:0;right:0;top:50%;z-index:5;border-top:1px dashed #999;display:flex;justify-content:center;}
.die-fold span{font-size:7px;color:#999;background:#fff;padding:0 8px;transform:translateY(-50%);text-transform:uppercase;letter-spacing:.08em;}
.die-half{position:absolute;left:3px;right:3px;height:calc(50% - 4px);overflow:hidden;}
.die-public{top:3px;border-radius:6px 6px 0 0;}
.die-private{bottom:3px;border-radius:0 0 6px 6px;}
.half-tag{font-family:system-ui,sans-serif;font-size:6px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;padding:2px 6px;margin:6px 8px 0;display:inline-block;border-radius:3px;}
.public-tag{background:rgba(196,92,92,.15);color:#e8a0a0;border:1px solid rgba(196,92,92,.35);}
.private-tag{background:rgba(107,140,206,.15);color:#a0c0e8;border:1px solid rgba(107,140,206,.35);}

.ribbon-band{position:relative;height:24px;margin:4px 12px 0;background:var(--ribbon);}
.ribbon-band.ribbon-inv .ribbon-text{transform:rotate(180deg);}
.ribbon-cap{position:absolute;width:16px;height:16px;top:4px;background:var(--bg);transform:rotate(45deg);}
.ribbon-cap-l{left:-8px;}.ribbon-cap-r{right:-8px;}
.ribbon-text{display:flex;align-items:center;justify-content:center;height:24px;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--a);}

.public-hero{display:flex;flex-direction:column;align-items:center;justify-content:center;height:calc(100% - 40px);gap:8px;padding:8px;}
.public-name{font-family:'Spectral',serif;font-size:28px;font-weight:400;letter-spacing:.04em;text-transform:uppercase;color:var(--a);line-height:1.1;text-align:center;}
.public-icon{display:flex;align-items:center;justify-content:center;opacity:.85;}
.char-public-name{font-size:24px;text-transform:none;letter-spacing:.02em;}

/* standard card in private half */
.std-card-slot{width:2.5in;height:3.5in;margin:0 auto;overflow:hidden;}
.std-card-slot .cardwrap{width:2.5in;margin:0;}
.std-card-slot .card{width:2.5in;height:3.5in;background:#f7f0e0;border:0.5px solid #c8a96e;overflow:hidden;box-shadow:5px 5px 0 rgba(0,0,0,.45);}
.std-card-slot.sm{transform:scale(.72);transform-origin:top center;height:2.52in;}
.std-card-slot.sm .cardwrap{width:2.5in;}

.upright-subtitle{font-style:italic;font-weight:300;font-size:8px;text-align:center;color:var(--ad);margin:6px 12px;}
.upright-content{padding:0 12px;font-family:Inter,sans-serif;font-size:7px;font-weight:600;line-height:1.45;color:#7D5725;}
.upright-body{margin-bottom:4px;}
.upright-footer{font-size:7px;text-align:center;text-transform:uppercase;color:var(--a);margin-top:6px;padding-bottom:8px;}

/* character private face */
.char-sketch-frame{margin:8px 12px;height:70px;border:2px solid #c5c5c5;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:9px;color:#a0a0a0;text-transform:uppercase;}
.char-name-blank{margin:8px 12px;}
.char-name-label{font-size:8px;color:#a0a0a0;text-transform:uppercase;letter-spacing:.04em;}
.char-write-line{height:22px;border-bottom:2px solid #c5c5c5;margin-top:4px;}
.char-appearance-block{padding:8px 12px;font-family:Inter,sans-serif;font-size:7px;line-height:1.5;color:#4b4b4b;}
.char-app-title{font-family:'Spectral',serif;font-size:11px;text-transform:uppercase;margin-bottom:2px;}
.char-app-hint{font-size:6.5px;margin-bottom:8px;color:#666;}
.char-field{border-top:1px solid #ddd;padding:5px 0;}
.char-field .blank{color:#999;font-style:italic;}

/* sheet rows */
.sheet-row{position:relative;display:grid;grid-template-columns:1fr 1fr 1.1fr;gap:14px;max-width:680px;margin:0 auto 40px;padding:36px 14px 20px;background:linear-gradient(180deg,#f8f4ee,#ece6dc);border:1px solid #bbb;border-radius:10px;}
.player-row{border-color:#6b8cce;}
.table-row{border-color:#c45c5c;}
.pov-note{position:absolute;top:8px;left:14px;right:14px;font-size:9px;font-weight:700;letter-spacing:.3px;text-transform:uppercase;}
.player-pov{color:#6b8cce;}
.table-pov{color:#c45c5c;}
.sheet-cell{text-align:center;}
.cell-tag{font-size:7px;font-weight:700;text-transform:uppercase;color:#999;margin-bottom:6px;}
.cell-tent{display:flex;justify-content:center;min-height:160px;align-items:flex-end;}
.cell-foot{font-size:8px;color:#666;margin-top:6px;font-style:italic;}
.table-row .cell-foot{font-style:normal;font-weight:700;color:#444;}

.mini-tent{width:100px;}
.tent-panel{min-height:140px;border:2px solid var(--a,#888);border-radius:6px 6px 2px 2px;background:var(--bg,#fff);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:8px 4px;box-shadow:0 2px 0 rgba(0,0,0,.15);}
.tent-public .public-name{font-size:14px;}
.tent-public .public-icon svg{width:28px;height:28px;}
.tent-private .std-card-slot{transform:scale(.38);transform-origin:top center;height:1.35in;}
.mini-rules .mini-title{font-family:'Spectral',serif;font-size:11px;color:#7D5725;text-transform:uppercase;}
.mini-rules .mini-sub{font-size:7px;color:#7D5725;margin-top:4px;line-height:1.3;}
.mini-sketch{height:40px;width:80%;border:1px solid #ccc;border-radius:4px;margin-bottom:6px;}
.mini-name-line{font-size:7px;color:#aaa;text-transform:uppercase;border-top:1px solid #ccc;padding-top:4px;width:80%;}

""" + FIGMA_CSS


def main() -> None:
    core_dies = "".join(
        f'<div class="sample"><div class="stag">{CLASS_THEME[c]["label"]} · {LEADING_KEYS[c].split("-")[0].title()}</div>{build_core_double_die(c)}</div>'
        for c in DONE_CLASSES
    )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Spectral:ital,wght@0,300;0,400;1,300&family=EB+Garamond:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="primer-card-scope.css">
<title>Instinct RPG — Upright Core Layout (4 classes)</title>
<style>{CSS}
/* primer overrides for proof scope */
.scope-core .card{{position:relative;border-left:5px solid var(--a);display:flex;flex-direction:column;}}
.scope-core .card-body{{flex:1;padding:3px 9px 26px;font-size:9px;line-height:1.45;}}
.scope-core .zone-label{{font-family:'EB Garamond',serif;font-size:6px;letter-spacing:.8px;text-transform:uppercase;color:#7a6030;}}
.scope-core .effect-text{{font-size:9px;line-height:1.45;}}
.scope-core .rule{{height:.5px;background:#c8a96e;opacity:.45;margin:3px 0;}}
.scope-core .cbody{{flex:1;padding:4px 9px 26px;font-size:9px;}}
.scope-core .flv{{font-style:italic;font-size:8.5px;color:#5a4020;margin-bottom:2px;}}
.scope-core .elbl{{font-size:6px;text-transform:uppercase;letter-spacing:.8px;color:#7a6030;}}
.scope-core .etxt{{font-size:9px;line-height:1.45;}}
.scope-core .hr{{height:.5px;background:#c8a96e;opacity:.45;margin:3px 0;}}
.scope-core .clbl{{font-size:6px;text-transform:uppercase;color:#7a6030;}}
.scope-core .ci{{font-size:8.5px;line-height:1.4;}}
</style>
</head>
<body>
<h1>Upright Core — Layout Understanding (v2)</h1>
<p class="sub">Four done classes · leading picks: <strong>Rage · Ace · Bulwark · Pact</strong>. Private face = standard Instinct card. Public face = class name + icon (once). Player sheet order: Class · Ancestry · Character. Table reads reversed: <em>Nathan, the Dwarf Rogue</em>.</p>

<div class="rule-box">
<strong>Fixes from your notes:</strong><br>
• Private half embeds the <strong>real 2.5″×3.5″ card</strong> — same as every other ability card.<br>
• Public half shows class name <strong>once</strong> + icon — no duplicate ribbon or second label.
• Public text oriented <strong>right-side up for across-the-table</strong> readers.<br>
• <strong>Icon</strong> under class name on public face.<br>
• Full double-tall <strong>Ancestry</strong> + <strong>Character</strong> dies included.<br>
• Section 0 = your uploaded Figma CSS, untouched, for comparison.
</div>

{figma_section_html()}

<section>
<h2>1 — Leading Core double-tall dies (4 classes)</h2>
<p class="h2-note">Top = public (class + icon). Bottom = private (standard Core card). Fold on dashed line → stand in Class slot.</p>
<div class="grid-4">{core_dies}</div>
</section>

<section>
<h2>2 — Ancestry double-tall die (Dwarf)</h2>
<p class="h2-note">Top = public (DWARF + icon). Bottom = private (ancestry action text). Same tent geometry as class card.</p>
<div class="grid-2"><div class="sample">{build_ancestry_double_die()}</div></div>
</section>

<section>
<h2>3 — Character double-tall die</h2>
<p class="h2-note">Top = public (character name for the table). Bottom = private (sketch box + appearance blanks to fill in).</p>
<div class="grid-2"><div class="sample">{build_character_double_die("Nathan")}</div></div>
</section>

<section>
<h2>4 — Your POV — sheet layout</h2>
<p class="h2-note">Left → right: <strong>Class · Ancestry · Character</strong>. Rogue / Ace example with Dwarf ancestry.</p>
{build_sheet_row_pov("player", "rogue", "Nathan", "Dwarf")}
</section>

<section>
<h2>5 — Across the table</h2>
<p class="h2-note">Column order <strong>reversed</strong>. Reads left → right: <strong>Nathan · DWARF · ROGUE</strong> — "Nathan, the Dwarf Rogue."</p>
{build_sheet_row_pov("table", "rogue", "Nathan", "Dwarf")}
</section>

</body>
</html>
"""

    out = ROOT / "core-leading-upright-proof.html"
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
