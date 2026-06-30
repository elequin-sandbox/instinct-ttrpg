#!/usr/bin/env python3
"""Regenerate core-leading-upright-proof.html — upright foldable leading Core cards."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_core_upright_html import (  # noqa: E402
    CLASS_THEME,
    LEADING_CORE,
    build_character_sheet_demo,
    build_upright_card,
)

CLASS_ORDER = [
    "barbarian",
    "bard",
    "cleric",
    "druid",
    "fighter",
    "monk",
    "paladin",
    "ranger",
    "rogue",
    "warlock",
    "wizard",
]

CSS = """
:root{--ink:#1e1810;--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;min-height:100vh;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;margin-bottom:20px;line-height:1.55;max-width:960px;}
.rule-box{max-width:960px;background:#1d140b;border:1px solid #3a2c19;border-left:4px solid var(--gold);border-radius:8px;padding:14px 16px;margin-bottom:28px;font-size:12.5px;line-height:1.55;color:#cbb98e;}
.rule-box strong{color:var(--gold);}
h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);margin:32px 0 8px;padding-bottom:6px;border-bottom:1px solid #2a1d10;}
.h2-note{font-size:12px;color:#8a7a5a;margin-bottom:16px;line-height:1.5;max-width:960px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:28px 20px;align-items:start;}
.sample{display:flex;flex-direction:column;gap:8px;align-items:center;}
.stag{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#e7d6ac;text-align:center;}
.stag-sub{font-size:9px;color:#8a7a5a;font-style:italic;text-align:center;margin-top:-4px;}

/* upright card — Figma 750×2100 scaled to ~190px wide */
.upright-card{position:relative;width:190px;height:532px;margin:0 auto;font-family:'Spectral',Georgia,serif;}
.upright-outline{position:absolute;inset:3px 3px 3px 3px;border:2.5px solid var(--a);border-radius:8px;pointer-events:none;z-index:2;}
.upright-fold{position:absolute;left:0;right:0;top:50%;height:0;border-top:1px dashed #c5c5c5;z-index:4;pointer-events:none;}
.upright-half{position:absolute;left:3px;right:3px;height:calc(50% - 3px);overflow:hidden;}
.upright-half-top{top:3px;background:var(--bg);border-radius:6px 6px 0 0;}
.upright-half-bottom{bottom:3px;background:var(--bg);border-radius:0 0 6px 6px;}

.ribbon-band{position:absolute;left:8px;right:8px;height:26px;top:50%;transform:translateY(-50%);background:var(--ribbon);}
.ribbon-cap{position:absolute;width:18px;height:18px;top:4px;background:var(--bg);transform:rotate(45deg);}
.ribbon-cap-l{left:-9px;}
.ribbon-cap-r{right:-9px;}
.ribbon-text{position:absolute;left:12px;right:12px;top:0;height:26px;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:400;letter-spacing:.04em;text-transform:uppercase;color:var(--a);text-align:center;line-height:1;}
.ribbon-text.inverted{transform:rotate(180deg);}

.upright-subtitle{position:absolute;left:14px;right:14px;top:58px;font-family:'Spectral',Georgia,serif;font-style:italic;font-weight:300;font-size:8px;line-height:1.35;text-align:center;color:var(--ad);}
.upright-content{position:absolute;left:12px;right:12px;top:88px;bottom:36px;overflow:hidden;display:flex;flex-direction:column;gap:6px;}
.upright-zone{font-family:Inter,system-ui,sans-serif;font-size:7px;font-weight:600;line-height:1.3;color:var(--ad);text-transform:uppercase;letter-spacing:.3px;}
.upright-body{font-family:Inter,system-ui,sans-serif;font-size:7px;font-weight:600;line-height:1.45;color:#4b4b4b;}
.upright-body.italic{font-weight:400;font-style:italic;color:var(--ad);font-size:6.5px;}
.upright-footer{position:absolute;left:0;right:0;bottom:8px;font-size:7px;text-align:center;text-transform:uppercase;color:var(--a);letter-spacing:.02em;}
.draft-tag{position:absolute;right:10px;bottom:22px;font-family:system-ui,sans-serif;font-size:6px;font-weight:800;letter-spacing:.5px;padding:1px 5px;border:1px solid #B8860B;color:#B8860B;border-radius:3px;background:rgba(184,134,11,.12);}

.kw{display:inline-block;padding:0 2px;border-radius:2px;font-size:6px;font-weight:700;vertical-align:baseline;font-family:system-ui,sans-serif;line-height:1.35;}
.kw-boost{background:#0F766E;color:#CCFBF1;}
.kw-resolve{background:#166534;color:#F0FDF4;}
.kw-crit{background:#B8860B;color:#FFFDE7;}

/* character sheet demo */
.sheet-demo{position:relative;max-width:960px;height:320px;margin:0 auto 40px;background:#f5f0e8;border:1px solid #ccc;border-radius:8px;overflow:hidden;}
.sheet-panel{position:absolute;top:30px;bottom:30px;width:28%;border:1px solid #c5c5c5;border-radius:8px;background:#fff;}
.sheet-class{left:4%;}
.sheet-ancestry{left:36%;}
.sheet-appearance{left:68%;width:28%;}
.sheet-placeholder-label{font-family:'Spectral',serif;font-size:28px;text-align:center;color:#4b4b4b;text-transform:uppercase;letter-spacing:.04em;margin-top:80px;}
.sheet-fold-hint{font-family:'Spectral',serif;font-style:italic;font-weight:300;font-size:11px;text-align:center;color:#4b4b4b;margin-top:20px;line-height:1.4;padding:0 20px;}
.sheet-card-slot{position:absolute;left:50%;top:55%;transform:translate(-50%,-50%) scale(.42);transform-origin:center center;z-index:5;}
.sheet-sketch{position:absolute;top:8px;left:50%;transform:translateX(-50%) rotate(180deg);font-size:10px;color:#a0a0a0;text-transform:uppercase;}
.sheet-name-line{position:absolute;bottom:60px;left:10%;right:10%;border-top:2px solid #c5c5c5;padding-top:8px;font-size:9px;color:#a0a0a0;text-transform:uppercase;}
.sheet-fold-guide{position:absolute;left:33%;right:33%;top:50%;border-top:2px dashed #c5c5c5;pointer-events:none;}
.view-tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;}
.view-tab{font-size:11px;padding:6px 12px;border:1px solid #3a2c19;border-radius:6px;color:#cbb98e;cursor:default;}
.view-tab.on{background:#2a1d10;border-color:var(--gold);color:var(--gold);}
"""

def main() -> None:
    cards_html = []
    for cls in CLASS_ORDER:
        data = LEADING_CORE[cls]
        card = build_upright_card(cls, data)
        draft = " · draft" if data.get("draft") else ""
        cards_html.append(
            f'<div class="sample"><div class="stag">{data["name"]}</div>'
            f'<div class="stag-sub">{cls.title()}{draft}</div>{card}</div>'
        )

    demo = build_character_sheet_demo("rogue")

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Spectral:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<title>Instinct RPG — Leading Core Upright Proof</title>
<style>{CSS}</style>
</head>
<body>
<h1>Leading Core — Upright Fold Format</h1>
<p class="sub">Prototype: one leading Core card per class in the <strong>character-sheet tent format</strong> (ancestry / loadout geometry). Replaces retired Loadout cards — folds into the Class slot on the full character sheet. <strong>Not labeled</strong> as “leading”; role is invisible at the table.</p>
<div class="rule-box">
<strong>Format:</strong> Fold on the dashed line → stand upright in the Class panel of the 3-panel character sheet. Ribbon shows the <strong>card name</strong> (readable right-side-up on the lower half). Footer: <em>⁘ CLASS | Core ⁘</em>. Monk + Wizard are <strong>draft concepts</strong> (no Baserow row yet).<br><br>
<strong>Retired:</strong> All 9 Loadout Core cards removed from the game — chargen now flows from the Player Primer v2 steps only.
</div>

<section>
<h2>Character sheet context</h2>
<p class="h2-note">Rogue / Ace shown folded into the Class slot — ancestry and appearance panels empty for reference.</p>
{demo}
</section>

<section>
<h2>All classes — upright preview</h2>
<p class="h2-note">Lower half is the player-facing read when the card stands in the Class slot. Upper half mirrors the ribbon (upside-down) for the tent fold.</p>
<div class="grid">
{"".join(cards_html)}
</div>
</section>
</body>
</html>
"""

    out = ROOT / "core-leading-upright-proof.html"
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out} ({len(CLASS_ORDER)} cards)")


if __name__ == "__main__":
    main()
