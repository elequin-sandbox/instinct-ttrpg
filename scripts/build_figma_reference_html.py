#!/usr/bin/env python3
"""Pure Figma CSS recreation — uploaded designs, unmodified, scaled for screen."""
from __future__ import annotations

# Thumbnail scale (core-leading-upright-proof grid): 750×2100 → ~225×630
THUMB_S = 0.3
# Readable viewer default: body copy ≥ ~12px on screen
VIEWER_FOLDED_S = 0.48
VIEWER_SHEET_S = 0.58

FOLDED_W, FOLDED_H = 750, 2100
SHEET_W, SHEET_H = 3300, 2550


def _figma_wrap(inner: str, label: str, w: float, h: float) -> str:
    return f"""<div class="figma-sample">
  <div class="figma-label">{label}</div>
  <div class="figma-canvas" style="width:{w}px;height:{h}px">{inner}</div>
</div>"""


def _folded_dims(scale: float) -> tuple[float, float]:
    return FOLDED_W * scale, FOLDED_H * scale


def figma_ancestry_dwarf(scale: float = THUMB_S, *, wrap: bool = True, label: str | None = None) -> str:
    """Literal ancestry-card.css — Dwarf."""
    s = scale
    w, h = _folded_dims(s)
    inner = f"""
<div class="fig-ancestry" style="width:{w}px;height:{h}px;position:relative;background:#fff;">
  <div style="position:absolute;left:{13*s}px;top:{13*s}px;width:{724*s}px;height:{2074*s}px;border:{4*s}px solid #7D5725;border-radius:{24*s}px;box-sizing:border-box;"></div>
  <div style="position:absolute;left:{13*s}px;top:{843*s}px;width:{724*s}px;height:{447.82*s}px;background:#F5F0E9;"></div>
  <div style="position:absolute;left:0;top:{1050*s}px;width:{750*s}px;border-top:1px dashed #C5C5C5;"></div>
  <!-- ribbon bottom -->
  <div style="position:absolute;left:{87.79*s}px;top:{1096.5*s}px;width:{554.96*s}px;height:{101.82*s}px;background:#DDCBB8;"></div>
  <div style="position:absolute;left:{35.97*s}px;top:{1096.5*s}px;width:{72*s}px;height:{72*s}px;background:#DDCBB8;transform:rotate(45deg);"></div>
  <div style="position:absolute;left:{592.75*s}px;top:{1096.5*s}px;width:{72*s}px;height:{72*s}px;background:#DDCBB8;transform:rotate(45deg);"></div>
  <div style="position:absolute;left:{112*s}px;top:{1096.5*s}px;width:{526*s}px;height:{101.82*s}px;font-family:Spectral,serif;font-size:{72.6481*s}px;line-height:{82*s}px;letter-spacing:.04em;text-transform:uppercase;color:#7D5725;display:flex;align-items:center;justify-content:center;">Dwarf</div>
  <!-- ribbon top inverted -->
  <div style="position:absolute;left:{87.79*s}px;top:{908.18*s}px;width:{554.96*s}px;height:{101.82*s}px;background:#DDCBB8;transform:rotate(-180deg);"></div>
  <div style="position:absolute;left:{92.54*s}px;top:{908.18*s}px;width:{526*s}px;height:{101.82*s}px;font-family:Spectral,serif;font-size:{72.6481*s}px;line-height:{82*s}px;letter-spacing:.04em;text-transform:uppercase;color:#7D5725;display:flex;align-items:center;justify-content:center;transform:rotate(-180deg);">Dwarf</div>
  <div style="position:absolute;left:{163.98*s}px;top:{1221.82*s}px;width:{422*s}px;font-family:Spectral,serif;font-style:italic;font-weight:300;font-size:{24*s}px;line-height:{32*s}px;text-align:center;color:#7D5725;">You were carved from stone and stubbornness, and it shows</div>
  <div style="position:absolute;left:{61.77*s}px;top:{1361.94*s}px;width:{618*s}px;font-family:Inter,sans-serif;font-size:{28*s}px;font-weight:600;line-height:{40*s}px;color:#7D5725;">
    <div>When a blow would stagger someone else, choose one:</div>
    <div style="margin-top:{16*s}px">Absorb it — take it and stay standing; you don't let the cost show.</div>
    <div style="margin-top:{16*s}px">Shake it off — make a Luck Check. On a success, your resilience turns the tide.</div>
    <div style="margin-top:{16*s}px">Dig in — your refusal to be moved becomes a statement the Scene must acknowledge</div>
  </div>
  <div style="position:absolute;left:{70*s}px;top:{2034*s}px;width:{610*s}px;font-family:Spectral,serif;font-size:{24*s}px;text-transform:uppercase;text-align:center;color:#623807;">⁘ Ancestry | action ⁘</div>
</div>"""
    if not wrap:
        return inner
    return _figma_wrap(inner, label or "ancestry-card.css — Dwarf (uploaded, unmodified)", w, h)


def figma_loadout_rogue(scale: float = THUMB_S, *, wrap: bool = True, label: str | None = None) -> str:
    s = scale
    w, h = _folded_dims(s)
    inner = f"""
<div style="width:{w}px;height:{h}px;position:relative;background:#fff;">
  <div style="position:absolute;left:{13*s}px;top:{13*s}px;width:{724*s}px;height:{2074*s}px;border:{4*s}px solid #6D5BA8;border-radius:{24*s}px;box-sizing:border-box;"></div>
  <div style="position:absolute;left:{13*s}px;top:{843*s}px;width:{724*s}px;height:{447.82*s}px;background:#F0EFF6;"></div>
  <div style="position:absolute;left:0;top:{1050*s}px;width:{750*s}px;border-top:1px dashed #C5C5C5;"></div>
  <div style="position:absolute;left:{97.52*s}px;top:{1089.5*s}px;width:{554.96*s}px;height:{101.82*s}px;background:#CDC7E1;"></div>
  <div style="position:absolute;left:{112*s}px;top:{1089.5*s}px;width:{526*s}px;height:{101.82*s}px;font-family:Spectral,serif;font-size:{72.6481*s}px;text-transform:uppercase;color:#6D5BA8;display:flex;align-items:center;justify-content:center;">Rogue</div>
  <div style="position:absolute;left:{97.52*s}px;top:{908.18*s}px;width:{554.96*s}px;height:{101.82*s}px;background:#CDC7E1;transform:rotate(-180deg);"></div>
  <div style="position:absolute;left:{112*s}px;top:{908.18*s}px;width:{526*s}px;height:{101.82*s}px;font-family:Spectral,serif;font-size:{72.6481*s}px;text-transform:uppercase;color:#6D5BA8;display:flex;align-items:center;justify-content:center;transform:rotate(-180deg);">Rogue</div>
  <div style="position:absolute;left:{163.98*s}px;top:{1220.82*s}px;width:{422*s}px;font-family:Spectral,serif;font-style:italic;font-weight:300;font-size:{24*s}px;text-align:center;color:#8353A7;">Build your character deck</div>
  <div style="position:absolute;left:{112*s}px;top:{1320.76*s}px;width:{444*s}px;font-family:Inter,sans-serif;">
    <div style="font-size:{28*s}px;font-weight:600;color:#4B4B4B;">Character draft</div>
    <div style="font-size:{24*s}px;color:#4B4B4B;">Draw 3, pick 1 to add to your deck</div>
  </div>
  <div style="position:absolute;left:{112*s}px;top:{1423*s}px;font-family:Inter,sans-serif;font-size:{24*s}px;color:#4B4B4B;">
    <span style="background:#623807;color:#fff;padding:{4*s}px {12*s}px;border-radius:{12*s}px;font-weight:600;">Background</span> ×1
  </div>
  <div style="position:absolute;left:{204*s}px;top:{2029*s}px;font-family:Spectral,serif;font-size:{24*s}px;text-transform:uppercase;color:#6D5BA8;">⁘ ROGUE | Loadout ⁘</div>
</div>"""
    if not wrap:
        return inner
    return _figma_wrap(inner, label or "loadout-card.css — Rogue (uploaded, unmodified)", w, h)


def figma_character_sheet_base(scale: float = THUMB_S * 0.4, *, wrap: bool = True, label: str | None = None) -> str:
    """full-card-base.css — 3 empty slots."""
    s = scale
    w, h = SHEET_W * s, SHEET_H * s
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
    if not wrap:
        return inner
    return _figma_wrap(inner, label or "full-card-base.css — 3-panel sheet (uploaded, unmodified)", w, h)


VIEWER_CSS = """
:root{--gold:#c8a96e;--gold-d:#7a6030;--bg:#16110a;--panel:#1d140b;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:#f0e6cf;padding:20px 16px 48px;}
h1{font-size:17px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;line-height:1.55;max-width:920px;margin-bottom:18px;}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;}
.tab{border:1px solid #4a3820;background:#241a0e;color:#e7d6ac;padding:8px 14px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;}
.tab.active{background:#3a2c19;border-color:var(--gold);color:var(--gold);}
.toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:12px;padding:10px 12px;background:var(--panel);border:1px solid #3a2c19;border-radius:8px;}
.toolbar label{font-size:11px;color:#cbb98e;text-transform:uppercase;letter-spacing:.6px;}
.zoom-btn{border:1px solid #4a3820;background:#2a1d10;color:#e7d6ac;padding:6px 10px;border-radius:5px;font-size:12px;cursor:pointer;}
.zoom-btn.active{border-color:var(--gold);color:var(--gold);}
.zoom-btn:hover{background:#352618;}
#zoom-label{font-size:12px;color:var(--gold);min-width:3.5em;text-align:center;}
.viewport-wrap{background:#0d0a06;border:1px solid #3a2c19;border-radius:8px;padding:12px;overflow:auto;max-height:calc(100vh - 200px);min-height:420px;}
.viewport{display:inline-block;transform-origin:top left;}
.artboard{position:relative;box-shadow:6px 6px 0 rgba(0,0,0,.45);border:1px solid #555;}
.panel{display:none;}.panel.active{display:block;}
.panel h2{font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--gold);margin-bottom:10px;}
.hint{font-size:11px;color:#8a7350;margin-top:8px;}
"""


def figma_viewer_page_html() -> str:
    """Standalone zoomable viewer — readable defaults + fit-width."""
    ancestry = figma_ancestry_dwarf(VIEWER_FOLDED_S, wrap=False)
    loadout = figma_loadout_rogue(VIEWER_FOLDED_S, wrap=False)
    sheet = figma_character_sheet_base(VIEWER_SHEET_S, wrap=False)
    aw, ah = _folded_dims(VIEWER_FOLDED_S)
    sw, sh = SHEET_W * VIEWER_SHEET_S, SHEET_H * VIEWER_SHEET_S
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Spectral:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<title>Instinct RPG — Figma CSS viewer (readable)</title>
<style>{VIEWER_CSS}</style>
</head>
<body>
<h1>Figma CSS viewer</h1>
<p class="sub">Uploaded Figma Dev Mode exports recreated as HTML. Use the tabs and zoom controls — the character sheet needs <strong>Fit width</strong> or <strong>100%+</strong> on smaller screens. Scroll inside the gray frame.</p>
<div class="tabs" role="tablist">
  <button class="tab active" data-panel="ancestry" type="button">ancestry-card.css</button>
  <button class="tab" data-panel="loadout" type="button">loadout-card.css</button>
  <button class="tab" data-panel="sheet" type="button">full-card-base.css</button>
</div>
<div class="toolbar">
  <label>Zoom</label>
  <button class="zoom-btn" data-zoom="0.75" type="button">75%</button>
  <button class="zoom-btn active" data-zoom="1" type="button">100%</button>
  <button class="zoom-btn" data-zoom="1.25" type="button">125%</button>
  <button class="zoom-btn" data-zoom="1.5" type="button">150%</button>
  <button class="zoom-btn" data-zoom="fit" type="button">Fit width</button>
  <span id="zoom-label">100%</span>
</div>
<div id="panel-ancestry" class="panel active" data-w="{aw}" data-h="{ah}">
  <h2>ancestry-card.css — Dwarf</h2>
  <div class="viewport-wrap"><div class="viewport"><div class="artboard">{ancestry}</div></div></div>
</div>
<div id="panel-loadout" class="panel" data-w="{aw}" data-h="{ah}">
  <h2>loadout-card.css — Rogue</h2>
  <div class="viewport-wrap"><div class="viewport"><div class="artboard">{loadout}</div></div></div>
</div>
<div id="panel-sheet" class="panel" data-w="{sw}" data-h="{sh}">
  <h2>full-card-base.css — 3-panel character sheet</h2>
  <div class="viewport-wrap"><div class="viewport"><div class="artboard">{sheet}</div></div></div>
  <p class="hint">Wide artboard (3300×2550 in Figma). Fit width is the easiest way to read panel labels.</p>
</div>
<script>
(function() {{
  let zoom = 1;
  let activePanel = document.querySelector('.panel.active');
  const label = document.getElementById('zoom-label');
  const btns = document.querySelectorAll('.zoom-btn');

  function applyZoom() {{
    if (!activePanel) return;
    const wrap = activePanel.querySelector('.viewport-wrap');
    const vp = activePanel.querySelector('.viewport');
    const baseW = parseFloat(activePanel.dataset.w);
    const baseH = parseFloat(activePanel.dataset.h);
    let z = zoom;
    if (zoom === 'fit' && wrap) {{
      const pad = 24;
      z = Math.min(1.5, Math.max(0.5, (wrap.clientWidth - pad) / baseW));
    }}
    vp.style.transform = 'scale(' + z + ')';
    vp.style.width = (baseW * z) + 'px';
    vp.style.height = (baseH * z) + 'px';
    label.textContent = (typeof zoom === 'number' ? Math.round(zoom * 100) : Math.round(z * 100)) + '%';
  }}

  document.querySelectorAll('.tab').forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      document.querySelectorAll('.tab').forEach(function(t) {{ t.classList.remove('active'); }});
      document.querySelectorAll('.panel').forEach(function(p) {{ p.classList.remove('active'); }});
      btn.classList.add('active');
      activePanel = document.getElementById('panel-' + btn.dataset.panel);
      activePanel.classList.add('active');
      applyZoom();
    }});
  }});

  btns.forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      btns.forEach(function(b) {{ b.classList.remove('active'); }});
      btn.classList.add('active');
      const v = btn.dataset.zoom;
      zoom = v === 'fit' ? 'fit' : parseFloat(v);
      applyZoom();
    }});
  }});

  window.addEventListener('resize', applyZoom);
  applyZoom();
}})();
</script>
</body>
</html>"""


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
<p class="h2-note">Thumbnail scale for side-by-side compare. For readable text, open <a href="figma-css-viewer.html" style="color:#e7c87a;">figma-css-viewer.html</a> (zoom + tabs).</p>
<div class="figma-grid">
{figma_ancestry_dwarf(THUMB_S)}
{figma_loadout_rogue(THUMB_S)}
{figma_character_sheet_base(THUMB_S * 0.4)}
</div>
</section>
"""
