#!/usr/bin/env python3
"""Build upright (foldable tent) HTML for leading Core cards — character-sheet slot format."""
from __future__ import annotations

import html
import re
from typing import Any

# Done classes only — leading Core picks locked June 2026
DONE_CLASSES = ("barbarian", "rogue", "paladin", "warlock")

CLASS_THEME: dict[str, dict[str, str]] = {
    "barbarian": {"a": "#9E2B2B", "ad": "#822323", "bg": "#F5EDE4", "ribbon": "#E8C4A8", "label": "Barbarian"},
    "rogue": {"a": "#6C5BA8", "ad": "#594b8a", "bg": "#F0EFF6", "ribbon": "#CDC7E1", "label": "Rogue"},
    "paladin": {"a": "#B8860B", "ad": "#976e09", "bg": "#F8F3E7", "ribbon": "#E7D6AC", "label": "Paladin"},
    "warlock": {"a": "#9A2B5E", "ad": "#7e234d", "bg": "#F5EAEF", "ribbon": "#DDB7C8", "label": "Warlock"},
}

LEADING_CORE: dict[str, dict[str, Any]] = {
    "barbarian": {
        "name": "Rage",
        "subtitle": "Everything that hurts you makes you worse to face.",
        "sections": [
            {
                "label": "Fuel — Rage Pool",
                "text": "When you fail a Check, place those rolled dice in your Rage pool. When you take damage, place the damage dice from each hit into your Rage pool.",
            },
            {
                "label": "Frenzy — 5+ Dice",
                "text": "Immediately top-deck and play the top card of your deck — narrate how your rage shapes it. That Action gains Boost 3. Unplayable cards generate 1 Resolve. Rage pool fully clears.",
            },
            {
                "label": "Spend — Retribution",
                "text": "At any point, spend your entire pool for Retribution (see your second Core card).",
            },
        ],
    },
    "rogue": {
        "name": "Ace",
        "subtitle": "Always one more card up the sleeve.",
        "sections": [
            {
                "label": "Effect",
                "text": "Once per Scene: when you play a card and succeed on the check, gain Boost 1 on your next check this beat. This triggers automatically — no action required.",
            },
            {
                "label": "Crit",
                "text": "Draw a card instead of gaining Boost 1.",
                "italic": True,
            },
        ],
    },
    "paladin": {
        "name": "Bulwark",
        "subtitle": "Your armor is not equipment. It is a promise.",
        "sections": [
            {
                "label": "Always Active",
                "text": "Your armor and shield are always present — no equip action required.",
            },
            {
                "label": "Resolve Bonus",
                "text": "Add +2 directly to every Resolve roll you make.",
            },
        ],
    },
    "warlock": {
        "name": "Pact",
        "subtitle": "Power has a price. You agreed to the terms.",
        "sections": [
            {
                "label": "Before Any Check",
                "text": "Spend any number of Resolve Dice from your pool to Boost your roll.",
            },
            {
                "label": "After Any Check (Before Resolution)",
                "text": "Spend any number of Hit Dice from your pool to Boost your roll.",
            },
        ],
    },
}


def _kw(text: str) -> str:
    out = html.escape(text)
    for kw, cls in [("Boost", "kw-boost"), ("Resolve", "kw-resolve"), ("Crit", "kw-crit"), ("Hit Dice", "kw-hd")]:
        out = re.sub(rf"\b{re.escape(kw)}\b", f'<span class="kw {cls}">{kw}</span>', out)
    for word in ("Draw", "Scene", "Action", "Discard", "Check"):
        out = re.sub(rf"\b{word}\b", f"<strong>{word}</strong>", out)
    return out


def _ribbon(name: str, inverted: bool = False) -> str:
    inv = " inverted" if inverted else ""
    return f"""<div class="ribbon-band">
      <div class="ribbon-cap ribbon-cap-l"></div>
      <div class="ribbon-cap ribbon-cap-r"></div>
      <div class="ribbon-text{inv}">{html.escape(name)}</div>
    </div>"""


def _body_sections(data: dict[str, Any]) -> str:
    parts = []
    for sec in data.get("sections", []):
        label = sec.get("label", "")
        text = _kw(sec.get("text", ""))
        if label:
            parts.append(f'<div class="upright-zone">{html.escape(label)}</div>')
        cls = "upright-body italic" if sec.get("italic") else "upright-body"
        parts.append(f'<div class="{cls}">{text}</div>')
    return "\n".join(parts)


def build_upright_flat(cls: str, data: dict[str, Any] | None = None) -> str:
    """Unfolded die — both faces visible (print layout). Top = public face, bottom = private face."""
    data = data or LEADING_CORE[cls]
    theme = CLASS_THEME[cls]
    name = data["name"]
    class_label = theme["label"].upper()
    footer = f"⁘ {class_label} | Core ⁘"
    public_half = f"""<div class="flat-half flat-half-public">
      <div class="face-tag face-tag-public">Public face — across the table sees this</div>
      {_ribbon(class_label, inverted=True)}
      <div class="public-class-name">{html.escape(class_label)}</div>
    </div>"""
    private_half = f"""<div class="flat-half flat-half-private">
      <div class="face-tag face-tag-private">Private face — you read this</div>
      {_ribbon(name)}
      <div class="upright-subtitle">{html.escape(data.get('subtitle', ''))}</div>
      <div class="upright-content">{_body_sections(data)}</div>
      <div class="upright-footer">{footer}</div>
    </div>"""
    return f"""<div class="upright-flat cls-{cls}" style="--a:{theme['a']};--ad:{theme['ad']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="upright-outline"></div>
  <div class="upright-fold"><span class="fold-label">fold here</span></div>
  {public_half}
  {private_half}
</div>"""


def build_upright_tent(cls: str, view: str = "player", data: dict[str, Any] | None = None) -> str:
    """Folded tent — view='player' (private rules) or 'public' (class name only)."""
    data = data or LEADING_CORE[cls]
    theme = CLASS_THEME[cls]
    name = data["name"]
    class_label = theme["label"].upper()
    footer = f"⁘ {class_label} | Core ⁘"

    if view == "public":
        inner = f"""<div class="tent-face tent-face-public">
      <div class="public-class-name large">{html.escape(class_label)}</div>
    </div>"""
        cap = "Across the table"
    else:
        inner = f"""<div class="tent-face tent-face-private">
      {_ribbon(name)}
      <div class="upright-subtitle">{html.escape(data.get('subtitle', ''))}</div>
      <div class="upright-content">{_body_sections(data)}</div>
      <div class="upright-footer">{footer}</div>
    </div>"""
        cap = "Your side"

    return f"""<div class="upright-tent cls-{cls} view-{view}" style="--a:{theme['a']};--ad:{theme['ad']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="tent-cap">{cap}</div>
  <div class="tent-body">
    <div class="tent-roof"></div>
    {inner}
  </div>
</div>"""


def build_character_sheet_row(cls: str = "rogue", ancestry: str = "Dwarf") -> str:
    """3-panel character sheet with class tent standing in slot."""
    tent = build_upright_tent(cls, "player")
    theme = CLASS_THEME[cls]
    ancestry_theme = {"a": "#7D5725", "ad": "#623807", "bg": "#F5F0E9", "ribbon": "#DDCBB8"}
    ancestry_tent = f"""<div class="upright-tent cls-ancestry view-player" style="--a:{ancestry_theme['a']};--ad:{ancestry_theme['ad']};--bg:{ancestry_theme['bg']};--ribbon:{ancestry_theme['ribbon']}">
  <div class="tent-body">
    <div class="tent-roof"></div>
    <div class="tent-face tent-face-private">
      <div class="ribbon-band"><div class="ribbon-cap ribbon-cap-l"></div><div class="ribbon-cap ribbon-cap-r"></div><div class="ribbon-text">{html.escape(ancestry)}</div></div>
      <div class="upright-subtitle">You were carved from stone and stubbornness.</div>
      <div class="upright-content"><div class="upright-body">When a blow would stagger someone else, choose one: Absorb it, Shake it off, or Dig in.</div></div>
      <div class="upright-footer">⁘ Ancestry | Action ⁘</div>
    </div>
  </div>
</div>"""
    return f"""<div class="sheet-row">
  <div class="sheet-panel sheet-class">
    <div class="panel-tag">Class slot</div>
    <div class="sheet-card-slot">{tent}</div>
    <div class="panel-foot">{theme['label']} · {LEADING_CORE[cls]['name']}</div>
  </div>
  <div class="sheet-panel sheet-ancestry">
    <div class="panel-tag">Ancestry slot</div>
    <div class="sheet-card-slot">{ancestry_tent}</div>
    <div class="panel-foot">{ancestry}</div>
  </div>
  <div class="sheet-panel sheet-character">
    <div class="panel-tag">Character</div>
    <div class="char-sketch-box">Sketch</div>
    <div class="char-name-line">Character name</div>
    <div class="char-appearance">
      <div><strong>Body:</strong> Built, Lithe…</div>
      <div><strong>Eyes:</strong> Hard, Kind…</div>
    </div>
  </div>
  <div class="pov-arrow pov-you">▼ you sit here</div>
</div>"""


def build_opponent_view_row(cls: str = "rogue", char_name: str = "Mika", ancestry: str = "Dwarf") -> str:
    """What the player across the table sees — name · ancestry · class, left to right."""
    theme = CLASS_THEME[cls]
    class_tent = build_upright_tent(cls, "public")
    ancestry_public = f"""<div class="upright-tent cls-ancestry view-public" style="--a:#7D5725;--bg:#F5F0E9;--ribbon:#DDCBB8">
  <div class="tent-body"><div class="tent-roof"></div>
  <div class="tent-face tent-face-public"><div class="public-class-name large">{html.escape(ancestry.upper())}</div></div>
  </div></div>"""
    return f"""<div class="sheet-row opponent-row">
  <div class="sheet-panel sheet-class">
    <div class="sheet-card-slot">{class_tent}</div>
    <div class="panel-foot public-read">{theme['label'].upper()}</div>
  </div>
  <div class="sheet-panel sheet-ancestry">
    <div class="sheet-card-slot">{ancestry_public}</div>
    <div class="panel-foot public-read">{ancestry.upper()}</div>
  </div>
  <div class="sheet-panel sheet-character">
    <div class="char-name-display">{html.escape(char_name)}</div>
  </div>
  <div class="pov-arrow pov-them">▲ their POV — reads left → right: Class · Ancestry · Name</div>
</div>"""
