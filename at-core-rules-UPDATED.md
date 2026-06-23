---
name: at-core-rules
description: Instinct RPG active gameplay rules — the single authoritative source for how the game currently plays. ALWAYS load this skill when creating any player-facing or GM-facing asset (tutorials, reference cards, how-to-play docs, GM guides, cheat sheets), when verifying whether a card design is rules-compliant, or when a question about how the game actually plays comes up. Triggers on phrases like "how does X work," "what's the rule for," "write the tutorial," "player reference card," "GM guide," "how do checks work," "what is Toll," "how does Resolve work," "how does combat work," "scene rules," "how do cards work at the table," or any session producing content that a real player or GM would read. Do NOT use at-design-archive as a source for any of this — it contains deprecated and future-scoped content only. This skill covers gameplay only; for card visual anatomy and writing conventions, also load at-card-language and at-design-system.
---

# Instinct RPG — Core Rules

**Version:** Post-Playtest #1 · June 2026 · Authoritative rules only — no deprecated or future-scoped content.

---

## §1 — GAME PHILOSOPHY

**The deck is who the character is in general. The hand is who they are right now.**

Cards are prompts, not contracts. A player narrates first. The card confirms the scope of what the fiction is allowed to achieve. The GM adjudicates what that means in this specific scene. Cards never fully prescribe outcomes — the GM and table fill the gap.

**A Miss is never a stop.** When a check produces a Miss die (a natural 1), the fiction advances regardless. The GM takes the scene somewhere interesting; the player is never punished with nothing.

**Fiction-first triggering.** Cards trigger when the fiction supports it, not when a mechanical condition is met. Triggers are soft gates — the table's social contract handles edge cases. A player should be able to look at a trigger and immediately know whether this scene qualifies.

**The north star (Ben, Playtest #1):**
> *"The core of the game is giving people funny excuses to use their cards in unexpected ways."*

Every rules decision should be measured against this. If a rule makes it harder to use cards unexpectedly, reconsider it.

**Conditions are narrative vocabulary.** Tags like **Exposed**, **Rooted**, and **Rattled** exist so players and GMs share a word to point at something happening in the fiction. What a condition means is determined by the GM in real time — these are not mechanically enforced states. Cards may include a parenthetical *(here: [interpretation])* to signal this card's intended reading — this is a suggestion, not a rule.

---

## §2 — THE GAME LOOP

Three repeating steps:

1. **Narrate** — a player describes what their character does or says.
2. **Roll & Resolve** — if the outcome is uncertain, build a dice pool and roll against the GM's opposing pool. The GM adjudicates.
3. **Story Moves** — the fiction advances based on the result. Miss? GM gains **[Toll]** and the scene moves. Hit? Narrate success. Crit? Spend [Crit] options.

---

## §3 — SCENES

Scenes are the primary unit of play. A scene has a clear location, a set of active participants, and a dramatic question. Scenes do not have formal initiative or turn order.

**Five scene types — every card should work in at least 4:**
1. **Combat** — direct physical conflict
2. **Social** — negotiation, persuasion, roleplay
3. **Exploration** — discovery, investigation, travel
4. **Rest/Downtime** — recovery, planning, interstitial moments
5. **Party Scenes** — internal group dynamics

Cards in hand are valid in any scene where the fiction supports their trigger. Cards are not restricted by scene type.

**Scene end:** At the end of a scene, player hands are discarded and redrawn. Conditions from cards (like **Exposed** applied mid-scene) clear unless the GM decides they persist narratively.

---

## §4 — THE HAND & CARD DRAW

**Hand size:** Players draw a full hand of cards at the start of each scene. Standard hand size is not fixed — it is determined by the table (typically 5 cards). The GM sets the scene; players draw.

**Cards in hand = the character's current state.** An **Instinct** card in hand means that quality is alive right now. A **Bond** means that connection is active this scene. A **Flaw** means that pressure is being felt right now. A **Background** or **Ancestry** means past experience is being called upon.

**Playing cards:** A player plays a card by narrating the fictional action that triggers it, then resolving its effect. Playing a card does not automatically mean rolling — only uncertain actions call for a roll.

**Discarding:** Cards may be discarded without playing them. Some effects require discarding as a cost.

**Deck depletion:** When a player's deck runs out, the discard pile shuffles back in. This is automatic.

**Empty hand:** When a player has no cards left, they fall back to narrative/basic actions only — no card effects available. GM guidance: aim to transition or end scenes once the party's average hand size drops to roughly 2 or fewer cards. A depleted hand is a pacing signal, not a punishment.

**Card economy as spotlight:** As hands deplete, players naturally cede the scene to those with more cards. GMs should read card counts as a pacing signal — "read the room by reading the hands."

---

## §5 — MAKING A CHECK

Only roll when the outcome is genuinely uncertain. If the answer is obvious given the fiction, the scene just moves — no roll needed.

All checks — combat and non-combat alike — resolve via the same **dice-pool-vs-dice-pool model**. The player builds their pool and rolls; the GM assembles an opposing pool representing difficulty and opposition. Player dice directly clear opposing dice one at a time. This is the single core resolution method for the entire game.

**Three phases: Build → Roll → Read**

### Phase 1 — Build

**Base pool by Tier:**
| Tier | Levels | Base dice |
|---|---|---|
| Tier 1 | 1–3 | 2d6 |
| Tier 2 | 4–6 | 3d6 |
| Tier 3 | 7–9 | 4d6 |

The default die is a d6. Some weapons and abilities upgrade to d8 or d10 (noted on the card). A d8 crits on 8; a d10 on 10.

**Adding extra dice (Boost):** Before rolling, a player may discard 1 card from their hand to add 1 extra die. This can be done even without a card in play. Declare before picking up the dice — never after seeing results. Cannot discard a 🔒 Bane card this way.

Card effects may also grant **[Boost N]** — N extra dice added to the pool as part of the card's effect. All bonus dice work the same way regardless of source.

**Aid (Ally assist):** An ally may discard a card to add 1 die to another player's check (granting [Boost 1]). **Aid is capped at one assist per check, maximum. Self-Aid does not exist — Aid must always come from an ally.** When a card formalizes this as a named mechanic, it's called Stack or Rally — see §10.

### Phase 2 — Roll

Roll all dice simultaneously.

### Phase 3 — Read Your Dice

**Pull 1s — those are Miss dice.** A **Miss** is strictly a die that rolled a natural 1. Each Miss die gives the GM 1 **[Toll]** immediately and is removed from the pool; Miss dice contribute nothing to the result. A die that partially-but-not-fully resolves its target is NOT a Miss — it is a partial success.

**Check for max-face dice — those are Crits.** Each die showing its maximum face value (6 on a d6, 8 on a d8, 10 on a d10) explodes: roll one bonus die and add it to your total. A bonus die showing max face counts toward Crit options but does not explode again.

**Count your Crits.** How many dice across the whole pool are still showing their max face? That count is how many Crit options you can spend.

*(Note: the tutorial v3 calls this resource "Flourishes" at the player-facing level. For design and card-writing purposes, use "Crit." When writing player-facing materials, use "Flourish.")*

**Read vs. opposing pool.** The player's dice directly clear opposing dice one at a time. The GM's pool is the difficulty made physical — there is no hidden DC or target number.

**Deadly Contests use pool clearing for damage:** When in a Deadly Contest, your roll IS the damage — face values deal damage directly to enemy Hit Dice. Miss dice (1s) still generate [Toll].

---

## §6 — THE OPPOSING DICE POOL (DIFFICULTY MODEL)

Difficulty in all checks — not just Deadly Contests — is represented by the **GM's opposing dice pool**. There is no DC ladder or hidden target number. The opposing pool is placed physically on the table before the roll, making difficulty visible and tactile.

**How the GM builds an opposing pool:**
- **Random method:** The GM rolls dice appropriate to the scene's danger level and lets them land. The resulting values become the opposition.
- **Hand-placed method:** The GM selects specific die values to represent particular threats. For example: a named villain may be hand-placed as a fixed d10 showing a high value, while generic enemies around them are random d6s. This differentiates bosses from mooks within the same Contest without separate stat blocks.

**Resolution:** Player dice clear opposing dice one at a time. When all opposing dice are cleared, the check succeeds. Remaining player dice after clearing the pool are surplus (see §8 for defensive spillover rules).

**Partial resolution:** If a player's pool clears some but not all opposing dice, the outcome is partial — the GM adjudicates what was and wasn't achieved in the fiction. This is not a Miss; it is a partial success.

**Pool sizing guidance:**
| Difficulty feel | Suggested opposing pool |
|---|---|
| Easy | 1–2 dice, low values |
| Moderate | 2–3 mixed dice |
| Hard | 3–4 dice, some high values |
| Very Hard | 4–5 dice, high values |
| Boss / Climactic | Mixed pool with hand-placed high-face dice for named threats alongside random dice for generic threats |

---

## §7 — TOLL

**[Toll]** is a GM resource generated by Miss dice — any die that rolled a natural 1, regardless of whether the check otherwise succeeded. Each 1 = 1 Toll added to the GM's pool.

**GM uses Toll to:** escalate the scene, trigger NPC reactions, activate enemy abilities, introduce complications. Toll is the game's pressure valve — even a successful roll can generate Toll if 1s were rolled, meaning the world is always reacting to player actions.

Players may spend Toll via specific card effects. Some cards reference Toll explicitly.

---

## §8 — DEADLY CONTESTS (PHYSICAL CONFLICT)

A **Deadly Contest** is any Contest where Hit Dice can be lost — characters are eligible to die. This is what was formerly called "combat encounter."

### Threat & Open Floor Model (Locked, Playtest #1)

When players enter a Deadly Contest, enemies reveal their **Threat** — the damage they will deal — **upfront before players commit.** The GM places Threat dice visibly in front of relevant players at Contest start. Threat is locked at the moment the Contest begins; it resolves regardless of the order players choose to act.

Players then choose: **fight** (knowing they will take the incoming Threat), **flee**, or **negotiate**. Engaging means accepting the Threat — there is no avoiding it once you choose to fight.

**Open Floor:** Deadly Contests have no fixed turn order. After Threat is revealed, any player may act in whatever sequence makes narrative sense. The group collectively decides who acts when, moment to moment. This is the Open Floor.

This makes Deadly Contests a genuine tactical decision with known stakes, not a surprise tax.

### Defensive Dice & Spillover

When a player deploys defensive dice (from a card or React ability) and those dice fully clear an incoming Threat pool, any leftover dice may be applied defensively to **any target of the player's choice — including themselves.** Spillover is not restricted to allies.

### Resolve Pool (Locked, replaces Guard)

At the start of any Contest (Deadly or Social), players set up a **[Resolve]** layer:
- Resolve is a temporary Hit Die pool placed in front of the player
- Resolve is lost before the health pool — it absorbs damage first
- When Resolve is depleted, damage starts hitting actual Hit Dice
- Resolve is narrated per class: *Bard's swashbuckling wit being worn down / Paladin's armor getting battered / Barbarian's rage fueling recklessness*

Cards that previously generated **Guard** now function as Resolve healing or reroll abilities. Guard is eliminated.

⚠️ *Exact mechanic for Resolve setup (how many dice to move, cost, free action) is still being refined. Working version: at Contest start, move [X] Hit Dice forward as Resolve.*

⚠️ *Wave structure (whether damage can overflow between Resolve and health pools) was debated at Playtest #1 and left unresolved. Nathan's lean: allow overflow for simplicity. Needs playtesting.*

### Hit Dice (Health)

**Hit Dice** are the player's health resource. Not "HP" — always call them Hit Dice or Hit Die (singular).

- **At Level 1:** All Hit Dice start at their maximum face value. No rolling for health at level 1.
- **Damage:** Threat dice deal damage equal to their face values. Damage removes Hit Dice or reduces their values.
- **Hit Dice spend model:** Hit Dice removal is **full-removal** — a die spent is fully removed. There is no partial "shave" model. This is intentional.
- **Breather:** After a Deadly Contest, players may recover Hit Dice. Working version: recover dice *as ones* (minimum value), then reroll through cards or rest actions. Exact wording not locked.

**Enemies:** Use fixed or maximized Hit Die arrangements, visible to players at Contest start. This creates tactical legibility — players can plan around "this guard has one D8 and two D4s."

### NPC Threats — Two Valid GM Techniques

The GM has discretion between two explicitly valid approaches for NPCs in harm's way per scene:

**(a) Real Threat dice:** Roll actual Threat dice against the NPC, exactly as a player would face. This means "defend" actions by players have something physical to intercept. Use this when the NPC's survival matters mechanically to the scene.

**(b) Abstracted description:** Give the NPC a health/severity description instead of tracked dice. "Defend" actions change the narrated outcome rather than removing physical dice. Use this for NPCs whose survival is narratively important but mechanically simple to resolve.

GM chooses based on how mechanically significant that NPC's fate is to the scene. Both are legitimate.

### Physical Dice as Table Components

Dice are physical objects that stay on the table — not abstract numbers on a sheet.
- **Enemy Hit Dice:** Placed physically in front of players. Removing or reducing a die is satisfying and communicative.
- **Barbarian Rage pool:** d6s from Miss checks and incoming Threat dice, placed on the table
- **Cleric Prayer:** Crit dice placed physically on the Prayer Core card
- **Druid Grove:** d6s accumulated on tended cards between scenes

Prefer d6s wherever possible. Players need a handful of d6s — not a full polyhedral set — for most mechanics.

---

## §9 — SOCIAL CONTESTS

A **Social Contest** is any Contest where Resolve is at risk but characters are **not** eligible to lose Hit Dice. This is what was formerly called "non-combat encounter."

Social Contests use the **same resolution engine** as Deadly Contests (Playtest #1, locked) — the same opposing-pool-vs-player-pool model, the same Open Floor structure, the same Miss/Crit/Toll mechanics.

- Both sides have a Resolve pool; "damage" chips at it
- When one side's pool is depleted, the confrontation ends (defeated in debate or in battle)
- The terms differ; the mechanics do not
- Social Resolve is narrated as: *composure, credibility, emotional momentum*

Cards work the same way in Social Contests. "Attacks" in social contexts are verbal challenges, pressure, or emotional appeals. The roll IS the damage to the other side's Resolve.

---

## §10 — CARD PLAY RULES

### Card Types & Timing

| Type | Cost | When Played |
|---|---|---|
| **Act** | 1 (costs your spotlight) | On your turn — primary action |
| **React** | 0 | At any time, in response to another player's or GM's action |
| **Core** | — | Always-active; placed face-up in Active area; never goes into deck |
| **Instinct** | — | Reveal from hand when the quality is driving the character's action; gain [Boost 2] |
| **Background** | — | Plays when the fictional trigger fires; choose-one or Luck Check effect |
| **Ancestry** | — | Plays when the fictional trigger fires |
| **Bond** | — | Find the moment; both you and the named person gain [Boost 1] |
| **Flaw** | — | Find a scene element that fits; choose: Dramatic path or Suppression path |

**React window:** After every roll, before narration, there is a brief beat where React cards can be played. The GM and players recognize this window; it should be named at the table.

⚠️ *Universal discard-to-React (discard 2 to play any Act card as a React) is a proposed direction from Playtest #1, not yet a locked rule.*

### Card Zones

| Zone | Contents | Persists? |
|---|---|---|
| **Hand** | Currently held cards | Discards at scene end |
| **Active** | Core cards, Items in use | Always — never discards |
| **Deck** | Undrawn cards | Reshuffles when empty |
| **Discard** | Played or discarded cards | Reshuffles into deck |

**Class-specific zones:** Druid Grove, Rogue Ace Pile — see at-class-quick-ref.

### Equipment

There is no universal equip-slot system or **Equip** keyword. The "always have my gear" fantasy is baked directly into specific classes' own Core ability cards, applied on a case-by-case basis per class. Fighter and Paladin are the current examples — their class-specific Core cards handle equipment access for those classes. Other classes do not have a general equipment mechanic.

### Luck Check

When a card calls for a **Luck Check**, the player rolls a die (GM adjudicates the die size based on fiction) with no stats applied. Boost dice are eligible. The GM interprets the result in context.

---

## §11 — CONDITIONS & KEYWORDS

These are the authoritative game terms. For card text formatting rules, see at-card-language.

### Effect Keywords (countable/trackable)
| Term | Meaning |
|---|---|
| **[Boost N]** | Additional dice added to a pool. Expire at scene end. Remove from pool if they show a 1. |
| **[Crit]** | The result tier above Success. Unlocks spend options on the played card. Spending a Crit does not remove the die from the pool — it only determines which options are available. Always spend after all dice are fully resolved. |
| **[Resolve]** | Temporary Hit Die pool set up at Contest start. Lost before health pool. Replaces retired Guard. |
| **[Hit Die] / [Hit Dice]** | Player health resource. Always capitalized. Never called "HP." |
| **[Toll]** | GM resource. Generated on any Miss die (a natural 1). Used to escalate scenes. |
| **[Aid]** | Ally-only assistance mechanic — functionally similar to Boost. Capped at one assist per check. Self-Aid does not exist. |
| **Mill** | Printed keyword on Item cards and React-subtype class ability cards only. Text reads: *"At scene start, you may discard this to draw 1."* Formally replaces the previously undocumented soft Mulligan. Does not apply to other card types. |

### Conditions (narrative vocabulary — GM adjudicates)

**Exposed**, **Rattled**, and **Rooted** are purely descriptive narrative terms with no enforced mechanical fallback. What they mean in any given moment is determined by the GM in real time. Because they carry no mechanical weight of their own, they are formatted as plain **bolded title case** in card text — not colored pill/tag treatment. *(Card studio formatting update for this change is a separate Phase 3 task.)*

| Condition | Narrative Meaning |
|---|---|
| **Exposed** | Vulnerable, open to attack |
| **Rattled** | Shaken, off-balance, psychologically disrupted |
| **Rooted** | Cannot reposition |

The following conditions carry mechanical properties and retain their standard keyword formatting:

| Condition | Meaning |
|---|---|
| **Hidden** | Cannot be detected or targeted by normal means; enemies cannot target without a check first |
| **Bolstered** | Strengthened, healed, fortified — receive bonus Hit Dice or reroll dice |
| **Marked** | Designated target — cannot be Hidden from whoever placed the Mark |
| **Sundered** | Structural damage — produced by Barbarian; consumed by other classes for conditional effects |
| **Break** | Structural impact on an object or enemy — produces Sundered on Crit when augmented by Barbarian |

### Declared Actions (Bold+Cap in card text)
**Action** · **Reaction** · **Draw** · **Discard** · **Shuffle** · **Cleanse** · **Luck Check** · **Scene**

### Retired Terms — Do Not Use
- ~~Guard~~ → use **[Resolve]**
- ~~Strong Roll~~ → use **[Crit]**
- ~~Encounter~~ → use **Contest** (umbrella), **Deadly Contest** (physical conflict), or **Social Contest** (non-combat)
- ~~Combat encounter~~ → use **Deadly Contest**
- ~~Non-combat encounter~~ → use **Social Contest**
- ~~Simultaneous~~ → use **Open Floor** (turn order) or **Threat** (damage-lock at Contest start) as appropriate
- ~~Failure~~ (as a trigger condition) → use **Miss** (natural 1 only); a partial result is not a Miss
- ~~Self-Aid~~ → Aid must come from an ally; self-assisting does not exist
- ~~DC ladder / target number / DC~~ → difficulty is a physical opposing dice pool; no hidden numbers
- ~~"while held, [negative effect]"~~ on Flaw cards → hand slot cost IS the consequence
- ~~"the fiction advances"~~ → designer-speak; do not put on player-facing materials

---

## §12 — CHARACTER CREATION PROCEDURE

### At the Table (Character Creation = Play)

Character creation is itself a form of play. It takes roughly one hour. Characters emerge from card stems — players are not filling out a stat sheet, they are being prompted into a backstory.

**Steps:**
1. **Draw 5 Instincts** at random from the Instinct card tableau
2. **Choose 1 Background** from the available set (12 options)
3. **Choose 1 Ancestry** from the available set (10 options)
4. **Bond cards:** Assigned or chosen based on party setup (~2 per character)
5. **Flaw cards:** Draw **2 Flaw cards** from the single Flaw pool; complete the fill-in stem for each at the table. Both Flaws come from the same pool — there is no sub-category distinction between them.
6. **Class deck:** Added to complete the deck (class ability cards)

**Deck target:** 20 cards total. Character creation cards + class ability cards = 20.

### Fill-in Stems

Every character creation card has an **Origin Stem** or **Fill-in Stem** — a prompted 1st-person past-tense incomplete sentence the player completes at the table. This is where characters come from. Stems are soft doorways, not corridors — they suggest a direction, not a requirement.

### Character Creation Deck Math

| Component | Count |
|---|---|
| Instinct cards (shuffled in) | 6 |
| Background | 1 |
| Ancestry | 1 |
| Bond(s) | ~2 |
| Flaw(s) | 2 |
| Class ability cards | Remaining to total 20 |

**Hypergeometric note:** With 6 Instincts in a 20-card deck, the median is 1 Instinct per 5-card hand (~13% chance of zero-Instinct scenes).

---

## §13 — CLASS MECHANICS SUMMARY

Each class has a locked identity, unique mechanic, and primary condition tags it produces. For full detail, load **at-class-quick-ref**.

**Tag ownership rule:** Overlapping production between classes is a design problem. One class owns each condition as primary producer. Others may consume or reference it.

**System-level locks (all classes):**
- Miss dice (natural 1s) always generate [Toll], regardless of class or card effect
- [Resolve] is set up at Contest start, before any cards are played
- [Crit] options are declared after all dice are fully resolved; spending a Crit does not remove the die from the pool

### Barbarian — Rage & Frenzy

The Barbarian's Rage pool accumulates d6s from **Miss** dice and incoming Threat dice. Physical dice are placed on the table.

**Frenzy trigger:** When the Rage pool reaches **5 or more dice**, the Barbarian may trigger Frenzy.
- On trigger: grants flat **Boost 3** to the frenzied action
- On trigger: **fully empties the entire Rage pool**

*Design note: Threshold lowered from 6 → 5 to compensate for Misses being rarer under the new Miss = natural-1-only definition. Pool fully depletes on trigger (replacing the old "halve the pool" behavior) to prevent chain re-triggers.*

### Warlock — Patron Invocation

The Patron invocation cost must be stated clearly and unambiguously **on the card itself** — do not rely on a separate tutorial section to communicate this rule:

- **First invocation (per scene):** Free — the Warlock chooses which Mark to assign
- **Later invocations (same scene):** The GM rolls randomly to determine the Mark cost

This is the rule as played. The card rewrite to reflect this language clearly is a Phase 2 task.

---

*End of at-core-rules. For card anatomy, visual formatting, and writing conventions, also load at-card-language and at-design-system.*
