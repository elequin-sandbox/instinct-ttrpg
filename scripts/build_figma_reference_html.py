#!/usr/bin/env python3
"""Pure Figma CSS recreation — uploaded designs, unmodified, scaled for screen."""
from __future__ import annotations

# Scale: Figma artboard 750×2100 → display ~225×630 (0.3)
S = 0.3
W, H = 750 * S, 2100 * S


def _figma_wrap(inner: str, label: str, w: float = W, h: float = H) -> str:
    return f"""<div class="figma-sample">
  <div class="figma-label">{label}</div>
  <div class="figma-canvas" style="width:{w}px;height:{h}px">{inner}</div>
</div>"""


def figma_ancestry_dwarf() -> str:
    """Literal ancestry-card_20be.css — Dwarf."""
    inner = f"""
<div class="fig-ancestry" style="width:{W}px;height:{H}px;position:relative;background:#fff;">
  <div style="position:absolute;left:{13*S}px;top:{13*S}px;width:{724*S}px;height:{2074*S}px;border:{4*S}px solid #7D5725;border-radius:{24*S}px;box-sizing:border-box;"></div>
  <div style="position:absolute;left:{13*S}px;top:{843*S}px;width:{724*S}px;height:{447.82*S}px;background:#F5F0E9;"></div>
  <div style="position:absolute;left:0;top:{1050*S}px;width:{750*S}px;border-top:1px dashed #C5C5C5;"></div>
  <!-- ribbon bottom -->
  <div style="position:absolute;left:{87.79*S}px;top:{1096.5*S}px;width:{554.96*S}px;height:{101.82*S}px;background:#DDCBB8;"></div>
  <div style="position:absolute;left:{35.97*S}px;top:{1096.5*S}px;width:{72*S}px;height:{72*S}px;background:#DDCBB8;transform:rotate(45deg);"></div>
  <div style="position:absolute;left:{592.75*S}px;top:{1096.5*S}px;width:{72*S}px;height:{72*S}px;background:#DDCBB8;transform:rotate(45deg);"></div>
  <div style="position:absolute;left:{112*S}px;top:{1096.5*S}px;width:{526*S}px;height:{101.82*S}px;font-family:Spectral,serif;font-size:{72.6481*S}px;line-height:{82*S}px;letter-spacing:.04em;text-transform:uppercase;color:#7D5725;display:flex;align-items:center;justify-content:center;">Dwarf</div>
  <!-- ribbon top inverted -->
  <div style="position:absolute;left:{87.79*S}px;top:{908.18*S}px;width:{554.96*S}px;height:{101.82*S}px;background:#DDCBB8;transform:rotate(-180deg);"></div>
  <div style="position:absolute;left:{92.54*S}px;top:{908.18*S}px;width:{526*S}px;height:{101.82*S}px;font-family:Spectral,serif;font-size:{72.6481*S}px;line-height:{82*S}px;letter-spacing:.04em;text-transform:uppercase;color:#7D5725;display:flex;align-items:center;justify-content:center;transform:rotate(-180deg);">Dwarf</div>
  <div style="position:absolute;left:{163.98*S}px;top:{1221.82*S}px;width:{422*S}px;font-family:Spectral,serif;font-style:italic;font-weight:300;font-size:{24*S}px;line-height:{32*S}px;text-align:center;color:#7D5725;">You were carved from stone and stubbornness, and it shows</div>
  <div style="position:absolute;left:{61.77*S}px;top:{1361.94*S}px;width:{618*S}px;font-family:Inter,sans-serif;font-size:{28*S}px;font-weight:600;line-height:{40*S}px;color:#7D5725;">
    <div>When a blow would stagger someone else, choose one:</div>
    <div style="margin-top:{16*S}px">Absorb it — take it and stay standing; you don't let the cost show.</div>
    <div style="margin-top:{16*S}px">Shake it off — make a Luck Check. On a success, your resilience turns the tide.</div>
    <div style="margin-top:{16*S}px">Dig in — your refusal to be moved becomes a statement the Scene must acknowledge</div>
  </div>
  <div style="position:absolute;left:{70*S}px;top:{2034*S}px;width:{610*S}px;font-family:Spectral,serif;font-size:{24*S}px;text-transform:uppercase;text-align:center;color:#623807;">⁘ Ancestry | action ⁘</div>
</div>"""
    return _figma_wrap(inner, "ancestry-card.css — Dwarf (uploaded, unmodified)")


def figma_loadout_rogue() -> str:
    inner = f"""
<div style="width:{W}px;height:{H}px;position:relative;background:#fff;">
  <div style="position:absolute;left:{13*S}px;top:{13*S}px;width:{724*S}px;height:{2074*S}px;border:{4*S}px solid #6D5BA8;border-radius:{24*S}px;box-sizing:border-box;"></div>
  <div style="position:absolute;left:{13*S}px;top:{843*S}px;width:{724*S}px;height:{447.82*S}px;background:#F0EFF6;"></div>
  <div style="position:absolute;left:0;top:{1050*S}px;width:{750*S}px;border-top:1px dashed #C5C5C5;"></div>
  <div style="position:absolute;left:{97.52*S}px;top:{1089.5*S}px;width:{554.96*S}px;height:{101.82*S}px;background:#CDC7E1;"></div>
  <div style="position:absolute;left:{112*S}px;top:{1089.5*S}px;width:{526*S}px;height:{101.82*S}px;font-family:Spectral,serif;font-size:{72.6481*S}px;text-transform:uppercase;color:#6D5BA8;display:flex;align-items:center;justify-content:center;">Rogue</div>
  <div style="position:absolute;left:{97.52*S}px;top:{908.18*S}px;width:{554.96*S}px;height:{101.82*S}px;background:#CDC7E1;transform:rotate(-180deg);"></div>
  <div style="position:absolute;left:{112*S}px;top:{908.18*S}px;width:{526*S}px;height:{101.82*S}px;font-family:Spectral,serif;font-size:{72.6481*S}px;text-transform:uppercase;color:#6D5BA8;display:flex;align-items:center;justify-content:center;transform:rotate(-180deg);">Rogue</div>
  <div style="position:absolute;left:{163.98*S}px;top:{1220.82*S}px;width:{422*S}px;font-family:Spectral,serif;font-style:italic;font-weight:300;font-size:{24*S}px;text-align:center;color:#8353A7;">Build your character deck</div>
  <div style="position:absolute;left:{112*S}px;top:{1320.76*S}px;width:{444*S}px;font-family:Inter,sans-serif;">
    <div style="font-size:{28*S}px;font-weight:600;color:#4B4B4B;">Character draft</div>
    <div style="font-size:{24*S}px;color:#4B4B4B;">Draw 3, pick 1 to add to your deck</div>
  </div>
  <div style="position:absolute;left:{112*S}px;top:{1423*S}px;font-family:Inter,sans-serif;font-size:{24*S}px;color:#4B4B4B;">
    <span style="background:#623807;color:#fff;padding:{4*S}px {12*S}px;border-radius:{12*S}px;font-weight:600;">Background</span> ×1
  </div>
  <div style="position:absolute;left:{204*S}px;top:{2029*S}px;font-family:Spectral,serif;font-size:{24*S}px;text-transform:uppercase;color:#6D5BA8;">⁘ ROGUE | Loadout ⁘</div>
</div>"""
    return _figma_wrap(inner, "loadout-card.css — Rogue (uploaded, unmodified)")


def figma_character_sheet_base() -> str:
    """full-card-base.css — 3 empty slots at 0.12 scale."""
    s = 0.12
    w, h = 3300 * s, 2550 * s
    inner = f"""
<div style="width:{w}px;height:{h}px;position:relative;background:#faf8f4;">
  <div style="position:absolute;left:{352.5*s}px;top:{1275*s}px;width:{1180.75*s}px;border-top:2px dashed #C5C5C5;"></div>
  <div style="position:absolute;left:{1724.25*s}px;top:{1275*s}px;width:{1180.75*s}px;border-top:2px dashed #C5C5C5;"></div>
  <div style="position:absolute;left:{1264*s}px;top:{1236*s}px;font-family:Spectral,serif;font-size:{24*s}px;color:#A0A0A0;text-transform:uppercase;">Fold here</div>
  <!-- class slot -->
  <div style="position:absolute;left:{488*s}px;top:{238*s}px;width:{724*s}px;height:{2074*s}px;border:2px solid #C5C5C5;border-radius:{24*s}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{80*s}px;padding:{200*s}px {99*s}px;">
    <div style="font-family:Spectral,serif;font-size:{72.6481*s}px;text-transform:uppercase;color:#4B4B4B;">Class</div>
    <div style="font-family:Spectral,serif;font-style:italic;font-weight:300;font-size:{40*s}px;text-align:center;color:#4B4B4B;line-height:1.35;">Fold and place your class loadout card here</div>
  </div>
  <!-- ancestry slot -->
  <div style="position:absolute;left:{1264*s}px;top:{238*s}px;width:{724*s}px;height:{2074*s}px;border:2px solid #C5C5C5;border-radius:{24*s}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{80*s}px;">
    <div style="font-family:Spectral,serif;font-size:{72.6481*s}px;text-transform:uppercase;color:#4B4B4B;">Ancestry</div>
    <div style="font-family:Spectral,serif;font-style:italic;font-weight:300;font-size:{40*s}px;text-align:center;color:#4B4B4B;">Fold and place your ancestry card here</div>
  </div>
  <!-- character slot -->
  <div style="position:absolute;left:{2040*s}px;top:{238*s}px;width:{724*s}px;height:{2074*s}px;border:2px solid #C5C5C5;border-radius:{24*s}px;">
    <div style="position:absolute;left:{31*s}px;top:{75*s}px;width:{662*s}px;height:{609*s}px;border:3px solid #C5C5C5;border-radius:{8*s}px;"></div>
    <div style="position:absolute;left:{47*s}px;top:{1168*s}px;width:{633*s}px;border-top:2px solid #C5C5C5;"></div>
    <div style="position:absolute;left:{47*s}px;top:{1180*s}px;font-family:Spectral,serif;font-size:{24*s}px;color:#A0A0A0;text-transform:uppercase;">Character name</div>
    <div style="position:absolute;left:{47*s}px;top:{1329*s}px;font-family:Spectral,serif;font-size:{40*s}px;text-transform:uppercase;">Appearance</div>
    <div style="position:absolute;left:{47*s}px;top:{1380*s}px;font-family:Inter,sans-serif;font-size:{24*s}px;color:#4B4B4B;">Choose one for each, or write your own:</div>
  </div>
</div>"""
    return _figma_wrap(inner, "full-card-base.css — 3-panel sheet (uploaded, unmodified)", w, h)


FIGMA_CSS = """
.figma-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:28px;align-items:start;margin-bottom:32px;}
.figma-sample{display:flex;flex-direction:column;gap:8px;align-items:center;}
.figma-label{font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#cbb98e;text-align:center;max-width:280px;line-height:1.4;}
.figma-canvas{position:relative;overflow:hidden;border:1px solid #555;box-shadow:4px 4px 0 rgba(0,0,0,.4);flex-shrink:0;}
"""


def figma_section_html() -> str:
    return f"""
<section class="figma-section">
<h2>0 — Pure Figma uploads (comparison only)</h2>
<p class="h2-note">Your uploaded CSS files recreated at scale — <strong>no changes</strong>. Compare against sections below.</p>
<div class="figma-grid">
{figma_ancestry_dwarf()}
{figma_loadout_rogue()}
{figma_character_sheet_base()}
</div>
</section>
"""
