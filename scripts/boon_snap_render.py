"""Shared HTML blocks for Boon-family Snap Check cards (Ancestry, Background)."""
from __future__ import annotations

Option = tuple[str, str]


def render_react_trigger(react_condition: str) -> str:
    body = (
        f"When {react_condition}, "
        f"<strong>React</strong> with a <strong>Snap Check</strong>:"
    )
    return (
        '<div class="anc-trigger">'
        '<div class="anc-freq">Once per Scene</div>'
        f'<div class="anc-callout anc-callout-react">{body}</div>'
        "</div>"
    )


def render_act_trigger(act_phrase: str) -> str:
    body = (
        f"You may take an <strong>Action</strong> to {act_phrase} "
        f"by making a <strong>Snap Check</strong>:"
    )
    return (
        '<div class="anc-trigger">'
        '<div class="anc-freq">Once per Scene</div>'
        f'<div class="anc-callout anc-callout-act">{body}</div>'
        "</div>"
    )


def render_options_list(options: list[Option]) -> str:
    rows = []
    for verb, desc in options:
        rows.append(f'<div class="bf-choice"><strong>{verb}</strong> — {desc}</div>')
    return '<div class="bf-choices">' + "".join(rows) + "</div>"


def render_snap_compact() -> str:
    return (
        '<div class="snap-compact">'
        '<span class="snap-chip"><span class="kw kw-snap">1–3</span> Fails</span>'
        '<span class="snap-dot">·</span>'
        '<span class="snap-chip"><span class="kw kw-snap">4–8</span> Choose 1</span>'
        '<span class="snap-dot">·</span>'
        '<span class="snap-chip"><span class="kw kw-snap">9+</span> Choose 2</span>'
        "</div>"
    )


def render_mill_line() -> str:
    return (
        '<div class="bf-mill">'
        '<span class="kw kw-mill">Mill</span> — At scene start, you may discard this to draw 1.'
        "</div>"
    )
