#!/usr/bin/env python3
"""Legacy v6b Oath phrase layout — 3×2 grid inside dotted rounded phrase frame."""
from __future__ import annotations

from scripts.build_oath_html import (
    BODY_STYLE,
    ENTER_VOW,
    FULFILL_VOW,
    KW_SM,
    _break_section,
    _hdr,
    etxt,
)

# v6b phrase zone (bb7c7b0) — horizontal die slot + term per cell, 3×2 × 2.
VOW_TERM = (
    "font-family:'EB Garamond',Georgia,serif;font-size:7.5px;font-weight:700;font-style:italic;"
    "color:var(--ad,#976e09);letter-spacing:0.25px;line-height:1.1;"
)

DIE_SLOT = (
    '<span class="die-slot kw kw-crit" style="flex-shrink:0;width:16px;height:16px;'
    "display:flex;align-items:center;justify-content:center;font-size:7.5px;font-weight:700;"
    'border-radius:3px;margin:1px;line-height:1;">{n}</span>'
)

PILL = (
    '<div class="vow-entry" style="display:flex;align-items:stretch;width:100%;min-height:18px;'
    'border:0.5px solid rgba(184,134,11,0.2);border-radius:3px;overflow:hidden;background:rgba(255,252,245,0.5);">'
    + DIE_SLOT
    + '<span class="vow-term" style="flex:1;display:flex;align-items:center;justify-content:center;'
    "padding:1px 4px 1px 2px;"
    + VOW_TERM
    + 'word-break:break-word;text-align:center;text-transform:none;">'
    "{word}</span></div>"
)

VOW_GRID = (
    '<div class="vow-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
    'gap:2px;margin:2px 0;width:100%;">{cells}</div>'
)

VOW_CELL = '<div class="vow-cell" style="display:flex;min-width:0;">{pill}</div>'

THE_DIVIDER = (
    '<div class="vow-the" style="display:flex;align-items:center;justify-content:center;'
    'gap:5px;height:11px;margin:1px 0;">'
    '<span style="flex:1;border-top:1px dotted rgba(184,134,11,0.3);"></span>'
    '<span class="vow-term" style="'
    + VOW_TERM
    + 'padding:0 3px;">the</span>'
    '<span style="flex:1;border-top:1px dotted rgba(184,134,11,0.3);"></span></div>'
)

# v6 — oval pill on *the* (inside same grid frame).
THE_DIVIDER_OVAL = (
    '<div style="display:flex;align-items:center;justify-content:center;position:relative;'
    'height:16px;margin:4px 0;">'
    '<span style="position:absolute;left:0;right:0;top:50%;height:1px;background:#c8a96e;opacity:0.55;"></span>'
    '<span style="position:relative;z-index:1;background:#f7f0e0;padding:2px 12px;'
    "font-family:'EB Garamond',Georgia,serif;font-size:11px;font-weight:700;font-style:italic;"
    "color:var(--ad,#976e09);border:1.5px solid var(--a,#B8860B);border-radius:10px;"
    'letter-spacing:0.6px;box-shadow:0 0 0 2px rgba(247,240,224,0.9);">the</span></div>'
)

VOW_PHRASE = (
    '<div class="vow-phrase" style="border:1px dotted rgba(184,134,11,0.5);border-radius:10px;'
    'padding:4px 5px 5px;margin:1px 0;">{inner}</div>'
)


def _word_grid(words: list[str]) -> str:
    cells = "".join(
        VOW_CELL.format(pill=PILL.format(n=i + 1, word=words[i])) for i in range(6)
    )
    return VOW_GRID.format(cells=cells)


def word_stack_grid(*, verbs: list[str], nouns: list[str], oval_the: bool = False) -> str:
    divider = THE_DIVIDER_OVAL if oval_the else THE_DIVIDER
    inner = _word_grid(verbs) + divider + _word_grid(nouns)
    return VOW_PHRASE.format(inner=inner)


def build_grid_legacy(oath: dict, *, oval_the: bool = False) -> str:
    body = (
        etxt(ENTER_VOW, extra_style="margin-bottom:1px;")
        + word_stack_grid(verbs=oath["verbs"], nouns=oath["nouns"], oval_the=oval_the)
        + '<div class="rule" style="margin:4px 0 2px;"></div>'
        + etxt(FULFILL_VOW)
    )
    return (
        '<div class="card paladin acc-paladin">'
        + _hdr(name=oath["name"], sub=oath["sub"])
        + f'<div class="card-body" style="{BODY_STYLE}">'
        + body
        + _break_section()
        + '</div><div class="idtag">Paladin</div></div>'
    )
