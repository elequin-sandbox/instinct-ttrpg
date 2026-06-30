#!/usr/bin/env python3
"""Build upright (foldable tent) HTML — leading Core, Ancestry, Character sheet cards."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DONE_CLASSES = ("barbarian", "rogue", "paladin", "warlock")

CLASS_THEME: dict[str, dict[str, str]] = {
    "barbarian": {"a": "#9E2B2B", "ad": "#822323", "bg": "#F5EDE4", "ribbon": "#E8C4A8", "label": "Barbarian"},
    "rogue": {"a": "#6C5BA8", "ad": "#594b8a", "bg": "#F0EFF6", "ribbon": "#CDC7E1", "label": "Rogue"},
    "paladin": {"a": "#B8860B", "ad": "#976e09", "bg": "#F8F3E7", "ribbon": "#E7D6AC", "label": "Paladin"},
    "warlock": {"a": "#9A2B5E", "ad": "#7e234d", "bg": "#F5EAEF", "ribbon": "#DDB7C8", "label": "Warlock"},
}

# Simple class icons (SVG) for public face
CLASS_ICONS: dict[str, str] = {
    "barbarian": '<svg viewBox="0 0 48 48" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 36 L24 8 L40 36"/><line x1="14" y1="28" x2="34" y2="28"/></svg>',
    "rogue": '<svg viewBox="0 0 48 48" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 38 L38 10"/><circle cx="32" cy="16" r="4"/></svg>',
    "paladin": '<svg viewBox="0 0 48 48" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2"><path d="M24 6 L38 14 V28 C38 36 24 42 24 42 C24 42 10 36 10 28 V14 Z"/></svg>',
    "warlock": '<svg viewBox="0 0 48 48" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2"><circle cx="24" cy="24" r="14"/><path d="M24 10 L26 20 L36 22 L26 24 L24 34 L22 24 L12 22 L22 20 Z"/></svg>',
}

ANCESTRY_ICON = '<svg viewBox="0 0 48 48" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 38 L18 18 L24 28 L30 14 L38 38"/></svg>'

LEADING_KEYS = {
    "barbarian": "rage-barbarian-core",
    "rogue": "ace-rogue-core",
    "paladin": "bulwark-paladin-core",
    "warlock": "pact-warlock-core",
}


def _load_card_html(key: str) -> str:
    text = (ROOT / "card-data.js").read_text(encoding="utf-8")
    cards = json.loads(re.search(r"window\.CARD_DATA\s*=\s*(\[.*\])", text, re.DOTALL).group(1))
    for c in cards:
        if c.get("Card_Key") == key:
            return c["HTML"]
    raise KeyError(key)


def _ribbon_bar(name: str, inverted: bool = False) -> str:
    inv = " ribbon-inv" if inverted else ""
    return f"""<div class="ribbon-band{inv}">
      <div class="ribbon-cap ribbon-cap-l"></div>
      <div class="ribbon-cap ribbon-cap-r"></div>
      <div class="ribbon-text">{html.escape(name)}</div>
    </div>"""


def build_public_face(label: str, icon_svg: str, theme: dict[str, str]) -> str:
    """Table-facing panel: ONE class/ancestry name + icon, right-side up for across-the-table reader."""
    return f"""<div class="die-half die-public" style="--a:{theme['a']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="half-tag public-tag">Public — across the table</div>
  <div class="public-hero">
    <div class="public-name">{html.escape(label.upper())}</div>
    <div class="public-icon" style="color:{theme['a']}">{icon_svg}</div>
  </div>
</div>"""


def build_private_core_face(cls: str, card_html: str, theme: dict[str, str]) -> str:
    """Player-facing panel: standard 2.5×3.5 Instinct card, unchanged."""
    return f"""<div class="die-half die-private" style="--a:{theme['a']};--bg:{theme['bg']}">
  <div class="half-tag private-tag">Private — you read this</div>
  <div class="std-card-slot cls-{cls}">
    <div class="cardwrap"><div class="scope-core cls-{cls}">{card_html}</div></div>
  </div>
</div>"""


def build_core_double_die(cls: str) -> str:
    theme = CLASS_THEME[cls]
    card_html = _load_card_html(LEADING_KEYS[cls])
    pub = build_public_face(theme["label"], CLASS_ICONS[cls], theme)
    priv = build_private_core_face(cls, card_html, theme)
    return f"""<div class="double-die cls-{cls}" style="--a:{theme['a']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="die-outline"></div>
  <div class="die-fold"><span>fold here</span></div>
  {pub}
  {priv}
</div>"""


def build_ancestry_double_die() -> str:
    theme = {"a": "#7D5725", "ad": "#623807", "bg": "#F5F0E9", "ribbon": "#DDCBB8"}
    pub = build_public_face("Dwarf", ANCESTRY_ICON, theme)
    priv = f"""<div class="die-half die-private ancestry-private" style="--a:{theme['a']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="half-tag private-tag">Private — you read this</div>
  {_ribbon_bar("Dwarf")}
  <div class="upright-subtitle">You were carved from stone and stubbornness, and it shows</div>
  <div class="upright-content">
    <div class="upright-body">When a blow would stagger someone else, choose one:</div>
    <div class="upright-body">Absorb it — take it and stay standing; you don't let the cost show.</div>
    <div class="upright-body">Shake it off — make a Luck Check. On a success, your resilience turns the tide.</div>
    <div class="upright-body">Dig in — your refusal to be moved becomes a statement the Scene must acknowledge</div>
  </div>
  <div class="upright-footer">⁘ Ancestry | Action ⁘</div>
</div>"""
    return f"""<div class="double-die cls-ancestry" style="--a:{theme['a']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="die-outline"></div>
  <div class="die-fold"><span>fold here</span></div>
  {pub}
  {priv}
</div>"""


def build_character_double_die(name: str = "Nathan") -> str:
    theme = {"a": "#4B4B4B", "ad": "#333", "bg": "#FFFFFF", "ribbon": "#E8E8E8"}
    pub = f"""<div class="die-half die-public char-public" style="--a:{theme['a']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="half-tag public-tag">Public — across the table</div>
  <div class="public-hero char-name-hero">
    <div class="public-name char-public-name">{html.escape(name)}</div>
  </div>
</div>"""
    priv = f"""<div class="die-half die-private char-private" style="--a:{theme['a']};--bg:{theme['bg']}">
  <div class="half-tag private-tag">Private — you fill in</div>
  <div class="char-sketch-frame">Sketch</div>
  <div class="char-name-blank">
    <div class="char-name-label">Character name</div>
    <div class="char-write-line"></div>
  </div>
  <div class="char-appearance-block">
    <div class="char-app-title">Appearance</div>
    <div class="char-app-hint">Choose one for each, or write your own:</div>
    <div class="char-field"><strong>Body:</strong> <span class="blank">Built, Lithe, Padded, Tattooed</span></div>
    <div class="char-field"><strong>Eyes:</strong> <span class="blank">Hard, Kind, Sharp, Sad</span></div>
    <div class="char-field"><strong>Hair:</strong> <span class="blank">Cropped, Fancy, Shaved, Wild</span></div>
    <div class="char-field"><strong>Clothes:</strong> <span class="blank">Flowing, Finery, Common, Scavenged</span></div>
  </div>
</div>"""
    return f"""<div class="double-die cls-character" style="--a:{theme['a']};--bg:{theme['bg']}">
  <div class="die-outline"></div>
  <div class="die-fold"><span>fold here</span></div>
  {pub}
  {priv}
</div>"""


def build_folded_tent_public(cls: str) -> str:
    theme = CLASS_THEME[cls]
    return f"""<div class="mini-tent tent-public cls-{cls}" style="--a:{theme['a']};--bg:{theme['bg']}">
  <div class="tent-panel">
    <div class="public-name">{html.escape(theme['label'].upper())}</div>
    <div class="public-icon" style="color:{theme['a']}">{CLASS_ICONS[cls]}</div>
  </div>
</div>"""


def build_folded_tent_private_core(cls: str) -> str:
    card_html = _load_card_html(LEADING_KEYS[cls])
    return f"""<div class="mini-tent tent-private cls-{cls}">
  <div class="std-card-slot sm cls-{cls}">
    <div class="cardwrap"><div class="scope-core cls-{cls}">{card_html}</div></div>
  </div>
</div>"""


def build_sheet_row_pov(pov: str = "player", cls: str = "rogue", name: str = "Nathan", ancestry: str = "Dwarf") -> str:
    """Player POV: Class | Ancestry | Character. Table POV: reversed → Name · Ancestry · Class."""
    class_tent = build_folded_tent_private_core(cls) if pov == "player" else build_folded_tent_public(cls)
    ancestry_pub = f"""<div class="mini-tent tent-public cls-ancestry" style="--a:#7D5725;--bg:#F5F0E9">
  <div class="tent-panel"><div class="public-name">{html.escape(ancestry.upper())}</div><div class="public-icon" style="color:#7D5725">{ANCESTRY_ICON}</div></div></div>"""
    ancestry_priv = f"""<div class="mini-tent tent-private ancestry-mini" style="--a:#7D5725;--bg:#F5F0E9">
  <div class="tent-panel mini-rules"><div class="mini-title">{html.escape(ancestry)}</div><div class="mini-sub">Absorb · Shake it off · Dig in</div></div></div>"""
    char_pub = f"""<div class="mini-tent tent-public char-mini"><div class="tent-panel"><div class="public-name char-public-name">{html.escape(name)}</div></div></div>"""
    char_priv = f"""<div class="mini-tent tent-private char-mini"><div class="tent-panel mini-char"><div class="mini-sketch"></div><div class="mini-name-line">Character name</div></div></div>"""

    if pov == "player":
        panels = [
            ("Class", class_tent, f"{CLASS_THEME[cls]['label']} · {LEADING_KEYS[cls].split('-')[0].title()}"),
            ("Ancestry", ancestry_priv, ancestry),
            ("Character", char_priv, name),
        ]
        arrow = '<div class="pov-note player-pov">Your POV — left to right: Class · Ancestry · Character</div>'
    else:
        panels = [
            ("Character", char_pub, name),
            ("Ancestry", ancestry_pub, ancestry.upper()),
            ("Class", build_folded_tent_public(cls), CLASS_THEME[cls]["label"].upper()),
        ]
        arrow = '<div class="pov-note table-pov">Across the table — reads left → right: <strong>Nathan, the Dwarf Rogue</strong></div>'

    cells = "".join(
        f'<div class="sheet-cell"><div class="cell-tag">{tag}</div><div class="cell-tent">{tent}</div><div class="cell-foot">{foot}</div></div>'
        for tag, tent, foot in panels
    )
    return f'<div class="sheet-row {pov}-row">{arrow}{cells}</div>'
