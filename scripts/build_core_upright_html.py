#!/usr/bin/env python3
"""Build upright (foldable tent) HTML for leading Core cards — character-sheet slot format."""
from __future__ import annotations

import html
import re
from typing import Any

# Class accent colors (match index.html acc-* tokens)
CLASS_THEME: dict[str, dict[str, str]] = {
    "barbarian": {"a": "#9E2B2B", "ad": "#822323", "bg": "#F5EDE4", "ribbon": "#E8C4A8"},
    "bard": {"a": "#B5388D", "ad": "#942e74", "bg": "#F8EBF4", "ribbon": "#E6BBD8"},
    "cleric": {"a": "#5E81AC", "ad": "#4d6a8d", "bg": "#EFF2F7", "ribbon": "#C8D4E3"},
    "druid": {"a": "#5A7D2A", "ad": "#4a6722", "bg": "#EEF2EA", "ribbon": "#C7D3B7"},
    "fighter": {"a": "#B45309", "ad": "#944407", "bg": "#F8EEE6", "ribbon": "#E6C5AB"},
    "monk": {"a": "#164E63", "ad": "#124051", "bg": "#E8EDEF", "ribbon": "#B0C3CA"},
    "paladin": {"a": "#B8860B", "ad": "#976e09", "bg": "#F8F3E7", "ribbon": "#E7D6AC"},
    "ranger": {"a": "#2F6B3D", "ad": "#275832", "bg": "#EAF0EC", "ribbon": "#B8CDBD"},
    "rogue": {"a": "#6C5BA8", "ad": "#594b8a", "bg": "#F0EFF6", "ribbon": "#CDC7E1"},
    "warlock": {"a": "#9A2B5E", "ad": "#7e234d", "bg": "#F5EAEF", "ribbon": "#DDB7C8"},
    "wizard": {"a": "#3C3489", "ad": "#312b70", "bg": "#ECEBF3", "ribbon": "#BDBAD7"},
}

# Leading core per class — card name, subtitle, body sections [{label, text, italic?}]
# Monk/Wizard: draft concepts from core-cards-draft.html (no Baserow rows yet)
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
    "bard": {
        "name": "Showstopper",
        "subtitle": "You make everyone else look good. Or you take the stage.",
        "sections": [
            {
                "label": "Once Per Scene — Discard 1",
                "text": "Choose one:",
            },
            {
                "label": "",
                "text": "Mimic — copy an ally's Action as they perform it. You roll independently.",
            },
            {
                "label": "",
                "text": "Lead — an ally copies your Action as you perform it. They roll independently.",
                "italic": True,
            },
        ],
    },
    "cleric": {
        "name": "Prayer",
        "subtitle": "You don't ask for power. You ask for purpose.",
        "sections": [
            {
                "label": "Each Scene — Declare Aloud",
                "text": "[Verb] the [Noun] — your petition for this Scene. All Crit dice from any roll bank here (up to your Level).",
            },
            {
                "label": "Once Per Scene",
                "text": "Spend ALL banked dice as Boost on one Action that serves your prayer. Flip this card face-down. Refreshes next Scene.",
            },
        ],
    },
    "druid": {
        "name": "Beastform",
        "subtitle": "You don't wear another shape. You remember it.",
        "sections": [
            {
                "label": "Equip System",
                "text": "You have 3 Beastform cards chosen at creation. Equipping one unequips all others → Draw 1. Swap freely between Scenes.",
            },
            {
                "label": "While Equipped",
                "text": "The Kinship passive on your active Beastform is always true. Transform freely — make a Check to use a Full Form ability.",
            },
        ],
    },
    "fighter": {
        "name": "Weapon Master",
        "subtitle": "Your hands know the weight of everything.",
        "sections": [
            {
                "label": "Passive",
                "text": "Whenever you equip any Item card into your Equip zone, Draw 1.",
            },
            {
                "label": "Note",
                "text": "Triggers on any equip — weapon, armor, or otherwise. Rewards active gear management every Scene.",
                "italic": True,
            },
        ],
    },
    "monk": {
        "name": "Stances",
        "subtitle": "You don't change who you are. You change how you move.",
        "draft": True,
        "sections": [
            {
                "label": "The Three Forms",
                "text": "You hold one Stance — Iron Palm, Wind Step, or Cobra. Its passive is always true while held.",
            },
            {
                "label": "Shift",
                "text": "At the start of your turn you may switch Stance for free. Narrate the change in your footing.",
            },
            {
                "label": "Note",
                "text": "Stances modify how your actions chain — never their damage. Chosen at creation.",
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
    "ranger": {
        "name": "Trapper",
        "subtitle": "The best ambush is one they walk into.",
        "sections": [
            {
                "label": "Setup",
                "text": "Stow up to 2 Trap cards face-down per Scene. Draw 1 for each trap prepared.",
            },
            {
                "label": "Trigger",
                "text": "When a trap's trigger condition is met, reveal the card to interrupt the triggering effect before it resolves.",
            },
        ],
    },
    "rogue": {
        "name": "Ace",
        "subtitle": "You already know how this ends.",
        "sections": [
            {
                "label": "Effect",
                "text": "Once per Scene: when you play a card and succeed on the check, gain Boost 1 on your next check this beat. This triggers automatically — no action required.",
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
    "wizard": {
        "name": "Prepared",
        "subtitle": "You already know how this scene begins. You wrote it.",
        "draft": True,
        "sections": [
            {
                "label": "Before the Scene",
                "text": "Set 1 Act card from your hand Prepared, face-up in your Active area. It holds no hand slot while Prepared.",
            },
            {
                "label": "Cast",
                "text": "Play your Prepared card at any moment without drawing it — even out of turn. Then Prepare nothing until the next scene.",
            },
            {
                "label": "Study",
                "text": "When you search your deck, you may immediately Prepare the card you find.",
                "italic": True,
            },
        ],
    },
}


def _kw(text: str) -> str:
    """Light keyword markup for upright body (Boost, Resolve, Crit, Draw, Scene, Action)."""
    out = html.escape(text)
    for kw, cls in [
        ("Boost", "kw-boost"),
        ("Resolve", "kw-resolve"),
        ("Crit", "kw-crit"),
    ]:
        out = re.sub(
            rf"\b{kw}\b",
            f'<span class="kw {cls}">{kw}</span>',
            out,
        )
    for word in ("Draw", "Scene", "Action", "Discard", "Check"):
        out = re.sub(rf"\b{word}\b", f"<strong>{word}</strong>", out)
    return out


def build_upright_card(cls: str, data: dict[str, Any] | None = None) -> str:
    """Return HTML for one upright foldable Core card."""
    data = data or LEADING_CORE[cls]
    theme = CLASS_THEME[cls]
    name = data["name"]
    subtitle = data.get("subtitle", "")
    class_label = cls.upper()
    footer = f"⁘ {class_label} | Core ⁘"
    draft_badge = (
        '<span class="draft-tag">DRAFT</span>' if data.get("draft") else ""
    )

    sections_html = []
    for sec in data.get("sections", []):
        label = sec.get("label", "")
        text = _kw(sec.get("text", ""))
        italic = sec.get("italic", False)
        label_html = (
            f'<div class="upright-zone">{html.escape(label)}</div>' if label else ""
        )
        style = ' class="upright-body italic"' if italic else ' class="upright-body"'
        sections_html.append(f"{label_html}<div{style}>{text}</div>")

    body = "\n".join(sections_html)
    esc_name = html.escape(name)
    esc_sub = html.escape(subtitle)

    # Ribbon geometry: center band with angled end caps (ancestry / loadout pattern)
    ribbon = f"""
    <div class="ribbon-band" style="--ribbon:{theme['ribbon']};--bg:{theme['bg']}">
      <div class="ribbon-cap ribbon-cap-l"></div>
      <div class="ribbon-cap ribbon-cap-r"></div>
      <div class="ribbon-text">{esc_name}</div>
    </div>"""

    return f"""<div class="upright-card cls-{cls}" style="--a:{theme['a']};--ad:{theme['ad']};--bg:{theme['bg']};--ribbon:{theme['ribbon']}">
  <div class="upright-outline"></div>
  <div class="upright-fold"></div>
  <div class="upright-half upright-half-top">
    {ribbon.replace('ribbon-text', 'ribbon-text inverted')}
  </div>
  <div class="upright-half upright-half-bottom">
    {ribbon}
    <div class="upright-subtitle">{esc_sub}</div>
    <div class="upright-content">{body}</div>
    <div class="upright-footer">{footer}</div>
    {draft_badge}
  </div>
</div>"""


def build_character_sheet_demo(cls: str = "rogue") -> str:
    """Mini 3-panel character sheet showing class slot with upright card."""
    card = build_upright_card(cls)
    return f"""<div class="sheet-demo">
  <div class="sheet-panel sheet-class">
    <div class="sheet-placeholder-label">Class</div>
    <div class="sheet-fold-hint">Fold and place your<br>leading Core card<br>here</div>
    <div class="sheet-card-slot">{card}</div>
  </div>
  <div class="sheet-panel sheet-ancestry">
    <div class="sheet-placeholder-label">Ancestry</div>
    <div class="sheet-fold-hint">Fold and place your<br>ancestry card<br>here</div>
  </div>
  <div class="sheet-panel sheet-appearance">
    <div class="sheet-sketch">Sketch</div>
    <div class="sheet-name-line">Character name</div>
  </div>
  <div class="sheet-fold-guide"></div>
</div>"""
