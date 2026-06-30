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

ANCESTRY_KEY = "dwarf-ancestry"

CHARACTER_ICON = '<svg viewBox="0 0 48 48" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="24" cy="16" r="8"/><path d="M8 42c0-8 7-14 16-14s16 6 16 14"/></svg>'


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


def build_private_std_card_face(scope: str, cls: str, card_html: str, theme: dict[str, str]) -> str:
    """Player-facing panel: standard 2.5×3.5 Instinct card (Core, Ancestry, Background, etc.)."""
    return f"""<div class="die-half die-private" style="--a:{theme['a']};--bg:{theme['bg']}">
  <div class="half-tag private-tag">Private — you read this</div>
  <div class="std-card-slot cls-{cls}">
    <div class="cardwrap"><div class="scope-{scope} cls-{cls}">{card_html}</div></div>
  </div>
</div>"""


def build_private_core_face(cls: str, card_html: str, theme: dict[str, str]) -> str:
    return build_private_std_card_face("core", cls, card_html, theme)


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


def build_ancestry_double_die(ancestry_key: str = ANCESTRY_KEY) -> str:
    theme = {"a": "#9a6a2e", "ad": "#7e5726", "bg": "#F5F0E9", "ribbon": "#DDCBB8"}
    card_html = _load_card_html(ancestry_key)
    name = ancestry_key.replace("-ancestry", "").title()
    pub = build_public_face(name, ANCESTRY_ICON, theme)
    priv = build_private_std_card_face("boon", "ancestry", card_html, theme)
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


def build_folded_tent_private_ancestry() -> str:
    card_html = _load_card_html(ANCESTRY_KEY)
    return f"""<div class="mini-tent tent-private cls-ancestry">
  <div class="std-card-slot sm cls-ancestry">
    <div class="cardwrap"><div class="scope-boon cls-ancestry">{card_html}</div></div>
  </div>
</div>"""


def _tableside_tent_col(
    *,
    border: str,
    bg: str,
    icon_html: str,
    name_html: str,
    extra_cls: str = "",
) -> str:
    return f"""<div class="ts-col {extra_cls}">
  <div class="ts-tent-silhouette">
    <div class="ts-roof" style="border-bottom-color:{border}"></div>
    <div class="ts-panel" style="border-color:{border};background:{bg}">
      <div class="ts-icon-row">{icon_html}</div>
      <div class="ts-name-row">{name_html}</div>
    </div>
  </div>
</div>"""


def build_tableside_inline_strip(
    cls: str = "rogue",
    name: str = "Nathan",
    ancestry: str = "Dwarf",
    show_blank_name: bool = False,
) -> str:
    """Table reads left → right: Name · Ancestry · Class — icons + labels on aligned rows."""
    theme_cls = CLASS_THEME[cls]
    theme_anc = {"a": "#9a6a2e", "bg": "#F5F0E9"}

    if show_blank_name:
        name_html = '<span class="ts-blank-line" aria-label="Character name blank"></span>'
        icon_html = f'<span class="ts-icon" style="color:#888">{CHARACTER_ICON}</span>'
        caption_name = "________"
    else:
        name_html = f'<span class="ts-name char-public-name">{html.escape(name)}</span>'
        icon_html = '<span class="ts-icon ts-icon-spacer" aria-hidden="true"></span>'
        caption_name = name

    char_cell = _tableside_tent_col(
        border="#888",
        bg="#fff",
        icon_html=icon_html,
        name_html=name_html,
        extra_cls="char-col",
    )
    anc_cell = _tableside_tent_col(
        border=theme_anc["a"],
        bg=theme_anc["bg"],
        icon_html=f'<span class="ts-icon" style="color:{theme_anc["a"]}">{ANCESTRY_ICON}</span>',
        name_html=f'<span class="ts-name">{html.escape(ancestry.upper())}</span>',
        extra_cls="ancestry-col",
    )
    class_cell = _tableside_tent_col(
        border=theme_cls["a"],
        bg=theme_cls["bg"],
        icon_html=f'<span class="ts-icon" style="color:{theme_cls["a"]}">{CLASS_ICONS[cls]}</span>',
        name_html=f'<span class="ts-name">{html.escape(theme_cls["label"].upper())}</span>',
        extra_cls="class-col",
    )

    return f"""<div class="tableside-strip">
  <div class="tableside-caption">Tableside — aligned left → right: <strong>{html.escape(caption_name)}, the {html.escape(ancestry)} {html.escape(theme_cls['label'])}</strong></div>
  <div class="tableside-row">
    {char_cell}
    <div class="ts-join ts-comma">,</div>
    <div class="ts-join ts-the">the</div>
    {anc_cell}
    {class_cell}
  </div>
</div>"""


def build_card_format_comparison() -> str:
    """Dwarf ancestry + Field Medic background — confirms live card anatomy."""
    dwarf = _load_card_html("dwarf-ancestry")
    medic = _load_card_html("field-medic-background")
    return f"""<div class="format-compare">
  <div class="sample"><div class="stag">Dwarf — live card-data</div>
    <div class="std-card-slot cls-ancestry"><div class="cardwrap"><div class="scope-boon cls-ancestry">{dwarf}</div></div></div></div>
  <div class="sample"><div class="stag">Field Medic — Background reference</div>
    <div class="std-card-slot cls-background"><div class="cardwrap"><div class="scope-boon cls-background">{medic}</div></div></div></div>
</div>"""


def build_folded_tent_public(cls: str) -> str:
    theme = CLASS_THEME[cls]
    return f"""<div class="mini-tent tent-public cls-{cls}" style="--a:{theme['a']};--bg:{theme['bg']}">
  <div class="tent-panel">
    <div class="public-name">{html.escape(theme['label'].upper())}</div>
    <div class="public-icon" style="color:{theme['a']}">{CLASS_ICONS[cls]}</div>
  </div>
</div>"""


def build_folded_tent_public_ancestry(ancestry: str = "Dwarf") -> str:
    return f"""<div class="mini-tent tent-public cls-ancestry" style="--a:#9a6a2e;--bg:#F5F0E9">
  <div class="tent-panel">
    <div class="public-name">{html.escape(ancestry.upper())}</div>
    <div class="public-icon" style="color:#9a6a2e">{ANCESTRY_ICON}</div>
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
    ancestry_pub = build_folded_tent_public_ancestry(ancestry)
    ancestry_priv = build_folded_tent_private_ancestry()
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
