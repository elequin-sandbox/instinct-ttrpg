---
name: at-card-renderer
description: Complete HTML/CSS/JS rendering stack for Act Tactics cards. Use this skill whenever a design session involves rendering a card, showing a card visually, building a card widget, visualizing a hand, creating a card grid, or producing any HTML or React output that contains Act Tactics cards. Also trigger proactively during card design sessions — always render before committing. Contains the canonical TAG_MAP (steel-blue verbs, locked v0.3), CSS, parse(), resolveBase(), TYPE_COLORS, and renderCard() functions.
---

# Act Tactics — Card Renderer

> ⚠️ **Gospel pointer & reconciliation pending.** The canonical keyword **formatting gospel** (Impact
> pills / Index chips / Narrative bold) and pill colors are in **`design/card-anatomy.md`** — treat it
> as truth. This code predates the current rules and must be reconciled: conditions (Exposed, Rattled,
> Rooted, Hidden, Marked) are now **plain-bold narrative**, not pills; `Bolstered` is retired (→ Boost);
> the Item Check / placed-dice / Save system is cut; and Impact Keywords **Threat, Crit, Toll, Miss,
> Aid, Mill** need canonical pills added. Until this stack is updated, follow `design/card-anatomy.md`.

Complete, copy-paste-ready rendering stack for Act Tactics cards. Use any time a session asks to "show a card," "render this," "build a card widget," "visualize a hand," or produce HTML/React output involving cards. Also apply proactively during card design — always render before committing.

---

## ⚠️ TAG_MAP Canonical Source Warning

`act-tactics-cards.js` is the single source of truth. `act-tactics-viewer.html` embeds an **older** multi-color TAG_MAP (Move = sky blue, Strike = bright red) that predates the locked unified-verb decision. **Always use the canonical TAG_MAP below** in new widgets — never copy TAG_MAP from `viewer.html`.

---

## Canonical TAG_MAP
```js
const TAG_MAP = {
  // All action verbs — steel blue (unified, locked v0.3)
  Move:     { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Strike:   { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Speak:    { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Sense:    { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Know:     { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Focus:    { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Enter:    { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Exit:     { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Read:     { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Summon:   { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Lift:     { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },
  Restrain: { bg: "#1D4ED8", text: "#EFF6FF", category: "verb" },

  // Positive states — deep green
  Bolstered: { bg: "#166534", text: "#F0FDF4", category: "positive_state" },
  Resolve:   { bg: "#166534", text: "#F0FDF4", category: "positive_state" },
  Hidden:    { bg: "#166534", text: "#F0FDF4", category: "positive_state" },

  // Negative states — deep red (filled)
  Exposed:   { bg: "#991B1B", text: "#FEF2F2", category: "negative_state" },
  "Exposed 1": { bg: "#991B1B", text: "#FEF2F2", category: "negative_state" },
  Rattled:   { bg: "#991B1B", text: "#FEF2F2", category: "negative_state" }, // RETIRED — do not use on new cards
  Rooted:    { bg: "#991B1B", text: "#FEF2F2", category: "negative_state" },
  "Rooted 1": { bg: "#991B1B", text: "#FEF2F2", category: "negative_state" },
  Marked:    { bg: "#991B1B", text: "#FEF2F2", category: "negative_state" },

  // Procedural game actions — deep sky blue
  Cleared:   { bg: "#0C4A6E", text: "#BAE6FD", category: "procedural" },

  // Buff states — blue outline (transparent bg, blue border+text)
  // NOTE: These render with inline styles only — TAG_MAP values are reference only.
  // Actual HTML: <span class="tp" style="background:transparent;color:#1D4ED8;border:1.5px solid #1D4ED8;box-sizing:border-box">Disguised</span>
  Disguised: { bg: "transparent", text: "#1D4ED8", category: "buff_state" },

  // Platform mechanics — deep violet
  "Stack 2": { bg: "#6B21A8", text: "#FAF5FF", category: "platform" },
  "Stack 3": { bg: "#6B21A8", text: "#FAF5FF", category: "platform" },
  "Rally 2": { bg: "#6B21A8", text: "#FAF5FF", category: "platform" },
  "Rally 3": { bg: "#6B21A8", text: "#FAF5FF", category: "platform" },

  // Damage modifiers
  "Damage+": { bg: "#7F1D1D", text: "#FEF2F2", category: "damage" },
  "Large":   { bg: "#7F1D1D", text: "#FEF2F2", category: "damage" },

  // Story / patron
  Debt:      { bg: "#78350F", text: "#FFFBEB", category: "story" },
  Pact:      { bg: "#1C1033", text: "#DDD6FE", category: "warlock" },
  Hunger:    { bg: "#450A0A", text: "#FEE2E2", category: "warlock" },

  // Wizard
  "Arcane Burn": { bg: "#312E81", text: "#E0E7FF", category: "wizard" },
  Prepared:      { bg: "#0E4D4D", text: "#CCFBF1", category: "wizard" },

  // Druid
  Beastform:       { bg: "#14532D", text: "#DCFCE7", category: "druid" },
  "Living Ground": { bg: "#1A3A1A", text: "#BBF7D0", category: "druid" },

  // Bard
  "Rally Token": { bg: "#0F766E", text: "#CCFBF1", category: "bard" },
  Performance:   { bg: "#86198F", text: "#FAE8FF", category: "bard" },
  Notoriety:     { bg: "#86198F", text: "#FAE8FF", category: "bard" },

  // Monk stances
  "Iron Palm": { bg: "#164E63", text: "#CFFAFE", category: "monk_stance" },
  "Wind Step": { bg: "#0C4A6E", text: "#BAE6FD", category: "monk_stance" },
  Cobra:       { bg: "#1E3A5F", text: "#DBEAFE", category: "monk_stance" },

  // Fighter
  "Battle-Hardened": { bg: "#3B2A00", text: "#FDE68A", category: "fighter" },
  Exchange:          { bg: "#92400E", text: "#FEF3C7", category: "fighter" },
};
```

**Adding a new tag:** Add to TAG_MAP first → add to card `tags` array → use `[TagName]` in card text. Never reverse this order.

---

## Card Type Colors & Labels
```js
const TYPE_COLORS = {
  act:        { h: '#1C3A5E', t: '#dbeafe' },
  react:      { h: '#0C4A6E', t: '#bae6fd' },
  condition:  { h: '#3C3489', t: '#ede9fe' },
  weapon:     { h: '#3B2A00', t: '#fef3c7' },
  stance:     { h: '#164E63', t: '#cffafe' },
  deck_manip: { h: '#1E3A5F', t: '#dbeafe' },
  omen:       { h: '#7F1D1D', t: '#fee2e2' },
  debt:       { h: '#3B0764', t: '#ede9fe' },
  ancestry:   { h: '#14532D', t: '#dcfce7' },
  background: { h: '#633806', t: '#fef3c7' },
  item:       { h: '#92400E', t: '#FEF3C7' }, // warm bronze — classless, Tier N
};
const TYPE_LABELS = {
  act: 'Act', react: 'React', condition: 'Condition', weapon: 'Weapon',
  stance: 'Stance', deck_manip: 'Deck Manip', omen: 'Omen', debt: 'Debt',
  ancestry: 'Ancestry', background: 'Background',
};
```

---

## Markup Parser & Tag Pill Renderer
```js
function esc(s) { return s ? s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') : ''; }

function resolveBase(raw) {
  if (TAG_MAP[raw]) return raw;
  const cap = raw.charAt(0).toUpperCase() + raw.slice(1).toLowerCase();
  if (TAG_MAP[cap]) return cap;
  const lower = raw.toLowerCase();
  for (const s of ['ing','ses','nes','tes','ves','zes','es','ed','s']) {
    if (lower.endsWith(s)) {
      const stem = lower.slice(0, -s.length);
      const sc = stem.charAt(0).toUpperCase() + stem.slice(1);
      if (TAG_MAP[sc]) return sc;
    }
  }
  return raw;
}

// Converts [Tag], _italic_, and (here: text) markup to HTML
function parse(t) {
  if (!t) return '';
  let r = '', last = 0, m;
  const re = /\[([^\]]+)\]|_([^_]+)_|\(here:([^)]+)\)/g;
  while ((m = re.exec(t)) !== null) {
    if (m.index > last) r += esc(t.slice(last, m.index));
    if (m[1]) {
      const raw = m[1], base = resolveBase(raw), ts = TAG_MAP[base];
      r += ts
        ? `<span class="tp" style="background:${ts.bg};color:${ts.text}">${esc(raw)}</span>`
        : `<strong>${esc(raw)}</strong>`;
    } else if (m[2]) {
      r += `<em style="color:#888">${esc(m[2])}</em>`;
    } else if (m[3]) {
      r += `<em style="color:#999;font-size:10px">(here:${esc(m[3])})</em>`;
    }
    last = m.index + m[0].length;
  }
  return r + esc(t.slice(last));
}
```

Markup syntax: `[Move]` → steel-blue pill · `[enters]` → resolves to Enter · `_text_` → italic · `_(here: note)_` → soft annotation

---

## renderCard(c)
```js
function renderCard(c) {
  const tc = TYPE_COLORS[c.cardType] || { h: '#333', t: '#eee' };
  const tl = TYPE_LABELS[c.cardType] || c.cardType;
  let body = '';
  if (c.exchange) body += `<span class="xbadge">Exchange</span>`;
  if (c.deckPool) body += `<span class="sbadge">Pool card</span>`;
  body += `<div class="flv">${esc(c.flavor)}</div>`;
  if (c.trigger) body += `<div class="trig"><strong>Trigger:</strong> ${parse(c.trigger)}</div>`;
  if (c.effect) body += `<div><div class="slbl">Effect</div><div class="etxt">${parse(c.effect)}</div></div>`;
  if (c.beastform) body += `<div class="bftitle">Beastform</div><div class="etxt">${parse(c.beastform)}</div>`;
  if (c.passive) body += `<div class="passbox">${parse(c.passive)}</div>`;
  if (c.react) body += `<div><div class="slbl" style="color:#3b82f6">React</div><div class="passbox" style="border-color:#3b82f6">${parse(c.react)}</div></div>`;
  if (c.stack) body += `<div class="etxt" style="margin-top:3px">${parse(c.stack)}</div>`;
  if (c.crit && c.crit.length) {
    body += `<div class="hr"></div><div class="srlbl">Crit</div>`;
    c.crit.forEach(o => body += `<div class="sropt">${parse(o)}</div>`);
  }
  if (c.failure) body += `<div class="hr"></div><div class="flbl">Failure</div><div class="ftxt">${parse(c.failure)}</div>`;
  body += `<div class="spacer"></div>`;
  if (c.discard) body += `<div class="discbox"><strong>Discard:</strong> ${esc(c.discard)}</div>`;
  const pip = c.cost !== null ? `<div class="cpip">${c.cost}</div>` : `<div style="width:20px"></div>`;
  const cls = c.class !== 'any' ? c.class : c.cardType;
  return `<div class="card">
    <div class="chead" style="background:${tc.h}">
      <span class="cname" style="color:${tc.t}" title="${esc(c.name)}">${esc(c.name)}</span>
      <span class="cbadge" style="color:${tc.t}">${tl}</span>
    </div>
    <div class="cbody">${body}</div>
    <div class="cfooter"><span class="fclass">${esc(cls)}</span>${pip}</div>
  </div>`;
}
```

---

## Card CSS (paste into style tag)
```css
.card{background:#fff;border-radius:10px;border:0.5px solid #ddd;display:flex;flex-direction:column;overflow:hidden;width:195px;box-shadow:5px 5px 0 #1a1a1a;transition:transform 0.15s,box-shadow 0.15s;}
.card:hover{transform:translate(-2px,-2px);box-shadow:7px 7px 0 #1a1a1a;}
.chead{padding:7px 10px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(0,0,0,0.1);}
.cname{font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:65%;}
.cbadge{font-size:10px;font-weight:700;padding:1px 6px;border-radius:3px;background:rgba(0,0,0,0.18);text-transform:uppercase;letter-spacing:0.5px;}
.cbody{flex:1;padding:8px 10px;display:flex;flex-direction:column;gap:4px;font-size:11px;line-height:1.55;}
.flv{font-style:italic;color:#666;padding-bottom:5px;border-bottom:0.5px solid #eee;flex-shrink:0;}
.slbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#999;margin-bottom:1px;margin-top:3px;}
.etxt{color:#222;line-height:1.6;}
.tp{display:inline-block;padding:0 5px;border-radius:3px;font-size:10.5px;font-weight:700;vertical-align:middle;line-height:1.6;margin:0 1px;}
.trig{background:#EFF6FF;border-left:2px solid #3B82F6;padding:3px 6px;font-style:italic;color:#1e40af;line-height:1.4;}
.passbox{border-left:2px solid #a78bfa;padding:3px 6px;color:#555;line-height:1.4;}
.discbox{border-left:2px solid #ef4444;padding:3px 6px;font-style:italic;color:#dc2626;line-height:1.4;}
.hr{height:0.5px;background:#eee;flex-shrink:0;margin:2px 0;}
.srlbl{font-size:10px;font-weight:700;color:#16a34a;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:1px;}
.sropt{color:#444;line-height:1.4;}
.flbl{font-size:10px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:1px;}
.ftxt{font-style:italic;color:#dc2626;line-height:1.4;}
.xbadge{font-size:9px;font-weight:700;background:#fef3c7;color:#92400e;padding:1px 5px;border-radius:3px;display:inline-block;margin-bottom:3px;}
.sbadge{font-size:9px;font-weight:700;background:#dcfce7;color:#166534;padding:1px 5px;border-radius:3px;display:inline-block;margin-bottom:3px;}
.bftitle{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#14532D;margin-top:3px;margin-bottom:1px;}
.spacer{flex:1;}
.cfooter{padding:5px 10px;border-top:0.5px solid #eee;display:flex;justify-content:space-between;align-items:center;background:#fafaf8;}
.fclass{font-size:10px;color:#999;text-transform:capitalize;}
.cpip{width:20px;height:20px;border-radius:50%;border:1.5px solid #ccc;background:#fff;font-size:12px;font-weight:700;color:#333;display:flex;align-items:center;justify-content:center;}
```

Shadow: `5px 5px 0 #1a1a1a` (hard offset, no blur — woodblock aesthetic). Hover: `translate(-2px,-2px)` + `7px 7px`. Never use soft blurred shadows.

---

## Layout Constants
- **Card width:** `195px`
- **Grid:** `grid-template-columns: repeat(auto-fill, minmax(195px, 1fr))`
- **Print:** `grid-template-columns: repeat(3, 63mm)` + `@page { size: A4; }`
- **Class color rule:** Color in `.chead` = class ability cards ONLY. Banes, Bonds, Boons use ink/parchment/gold palette.

---

## Common Widget Patterns

**Single card:** Wrap `renderCard(c)` in `<div style="display:flex;justify-content:center;padding:40px;">`

**Grid:** `<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(195px,1fr));gap:14px;">`

**Hand fan (React):** `position:absolute`, `transform-origin: 50% 100%`, rotations at `-15deg, -7deg, 0deg, 7deg, 15deg`. Chec