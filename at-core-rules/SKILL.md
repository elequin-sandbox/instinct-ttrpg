---
name: at-core-rules
description: Instinct RPG active gameplay rules — the single authoritative source for how the game currently plays. ALWAYS load this skill when creating any player-facing or GM-facing asset (tutorials, reference cards, how-to-play docs, GM guides, cheat sheets), when verifying whether a card design is rules-compliant, or when a question about how the game actually plays comes up. Triggers on phrases like "how does X work," "what's the rule for," "write the tutorial," "player reference card," "GM guide," "how do checks work," "what is Toll," "how does Resolve work," "how does combat work," "scene rules," "how do cards work at the table," or any session producing content that a real player or GM would read. Do NOT use at-design-archive as a source for any of this — it contains deprecated and future-scoped content only. This skill covers gameplay only; for card visual anatomy and writing conventions, also load at-card-language and at-design-system.
---

# Instinct RPG — Core Rules

**Version:** Post-Playtest #1 · June 2025 · Authoritative rules only — no deprecated or future-scoped content.

---

## GAME PHILOSOPHY

**The deck is who the character is in general. The hand is who they are right now.**

Cards are prompts, not contracts. A player narrates first. The card confirms the scope of what the fiction is allowed to achieve. The GM adjudicates what that means in this specific scene. Cards never fully prescribe outcomes — the GM and table fill the gap.

**Failure always moves the scene forward.** A miss is never a stop. The fiction advances regardless of the roll. The GM takes the scene somewhere interesting; the player is never punished with nothing.

**Fiction-first triggering.** Cards trigger when the fiction supports it, not when a mechanical condition is met. Triggers are soft gates — the table's social contract handles edge cases. A player should be able to look at a trigger and immediately know whether this scene qualifies.

**The north star (Ben, Playtest #1):**
> *"The core of the game is giving people funny excuses to use their cards in unexpected ways."*

Every rules decision should be measured against this. If a rule makes it harder to use cards unexpectedly, reconsider it.

**Conditions are narrative vocabulary.** Tags like **Exposed**, **Rooted**, and **Rattled** exist so players and GMs share a word to point at something happening in the fiction. What a tag means mechanically is adjudicated by the GM in real time. Cards may include a parenthetical *(here: [interpretation])* to signal this card's intended reading — this is a suggestion, not a rule.

---

## THE GAME LOOP

Three repeating steps:

1. **Narrate** — a player describes what their character does or says.
2. **Roll & Resolve** — if the outcome is uncertain, build a dice pool and roll. Read the result against the band ladder. The GM adjudicates.
3. **Story Moves** — the fiction advances based on the result. Miss? GM gains **[Toll]** and the scene moves. Hit? Narrate success. Crit? Spend [Crit] options.

---

## SCENES

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

## THE HAND & CARD DRAW

**Hand size:** Players draw a full hand of cards at the start of each scene. Standard hand size is not fixed — it is determined by the table (typically 5 cards). The GM sets the scene; players draw.

**Cards in hand = the character's current state.** An **Instinct** card in hand means that quality is alive right now. A **Bond** means that connection is active this scene. A **Flaw** means that pressure is being felt right now. A **Background** or **Ancestry** means past experience is being called upon.

**Playing cards:** A player plays a card by narrating the fictional action that triggers it, then resolving its effect. Playing a card does not automatically mean rolling — only uncertain actions call for a roll.

**Discarding:** Cards may be discarded without playing them. Some effects require discarding as a cost.

**Deck depletion:** When a player's deck runs out, the discard pile shuffles back in. This is automatic.

**Empty hand:** ⚠️ *Open design item — no rule currently exists for what happens when a player exhausts their full hand. See at-design-archive for proposed directions.*

**Card economy as spotlight:** As hands deplete, players naturally cede the scene to those with more cards. GMs should read card counts as a pacing signal — "read the room by reading the hands."

---

## MAKING A CHECK

Only rolls when outcome is uncertain. Do not call for a roll if the answer is obvious given the fiction.

**Three phases:**

### Phase 1 — Build
Assemble the dice pool:
- **Base dice** — determined by character stats and the action type
- **[Boost N]** — additional dice added by cards, effects, or ally assists. Boost dice are rolled and added to the result; they are removed from the pool if they roll the lowest face (1 on a d6). Boost dice expire at scene's end.

**Assist / Stacking:** An ally may add to a check by discarding a card, granting **[Boost 1]**. Multiple allies may assist the same roll. (This is called Stacking when the mechanic appears formally on cards.)

### Phase 2 — Roll
Roll all dice in the pool simultaneously.

**Attacks do not have a target number to hit.** When attacking, you roll and read the dice as damage. The roll IS the damage. There is no "miss" on an attack — the dice face values deal damage directly to enemy Hit Dice. Ones on attack rolls generate **[Toll]** as normal.

**Checks** (non-attack rolls) succeed or fail based on the result ladder (see Result Bands).

### Phase 3 — Read Your Dice
Interpret the result using the band ladder.

---

## RESULT BANDS

| Result | Meaning |
|---|---|
| **Crit** | Success + [Crit] spend options unlock (2–3 options, each 3–6 words) |
| **Success** | Clean hit or success — full effect, no cost |
| **Partial** | Success with a cost, complication, or reduced effect |
| **Miss** | Failure — scene advances, GM gains 1 **[Toll]** |

**[Crit] options:** When a roll Crits, players may spend [Crit] on available options from the card they played. Crit options are thematically native to the card — no generic rewards.

**Flourish:** The count of all maximum-face dice after dice have resolved (including explosive dice). "The Flourish" is the in-game term for spending Crit results. Do not use "Flourish" as a generic synonym for crit — it is mechanically specific.

---

## TOLL

**[Toll]** is a GM resource generated on any Miss die or full Miss roll. It accumulates over the scene.

**GM uses Toll to:** escalate the scene, trigger NPC reactions, activate enemy abilities, introduce complications. Toll is the game's pressure valve — failure creates narrative momentum, not dead stops.

Players may spend Toll via specific card effects. Some cards reference Toll explicitly.

---

## COMBAT RESOLUTION

### Simultaneous Damage Model (Locked, Playtest #1)

When players engage in combat, enemies reveal their damage threat **upfront before players commit.** The GM places enemy damage dice visibly in front of relevant players at combat start.

Players then choose: **fight** (knowing they will take the incoming damage), **flee**, or **negotiate**. Engaging means taking the damage — there is no avoiding it once you choose to fight.

This makes combat a genuine tactical decision with known stakes, not a surprise tax.

### Resolve Pool (Locked, replaces Guard)

At the start of any combat (physical or social), players set up a **[Resolve]** layer:
- Resolve is a temporary Hit Die pool placed in front of the player
- Resolve is lost before the health pool — it absorbs damage first
- When Resolve is depleted, damage starts hitting actual Hit Dice
- Resolve is narrated per class: *Bard's swashbuckling wit being worn down / Paladin's armor getting battered / Barbarian's rage fueling recklessness*

Cards that previously generated **Guard** now function as Resolve healing or reroll abilities. Guard is eliminated.

⚠️ *Exact mechanic for Resolve setup (how many dice to move, cost, free action) is still being refined. Working version: at combat start, move [X] Hit Dice forward as Resolve.*

⚠️ *Wave structure (whether damage can overflow between Resolve and health pools) was debated at Playtest #1 and left unresolved. Nathan's lean: allow overflow for simplicity. Needs playtesting.*

### Hit Dice (Health)

**Hit Dice** are the player's health resource. Not "HP" — always call them Hit Dice or Hit Die (singular).

- **At Level 1:** All Hit Dice start at their maximum face value. No rolling for health at level 1.
- **Damage:** Enemy dice deal damage equal to their face values. Damage removes Hit Dice or reduces their values.
- **Breather:** After combat, players may recover Hit Dice. Working version: recover dice *as ones* (minimum value), then reroll through cards or rest actions. Exact wording not locked.

**Enemies:** Use fixed or maximized Hit Die arrangements, visible to players at combat start. This creates tactical legibility — players can plan around "this guard has one D8 and two D4s."

### Physical Dice as Table Components

Dice are physical objects that stay on the table — not abstract numbers on a sheet.
- **Enemy Hit Dice:** Placed physically in front of players. Removing or reducing a die is satisfying and communicative.
- **Barbarian Rage pool:** d6s from failed checks and damage, placed on the table
- **Cleric Prayer:** Crit dice placed physically on the Prayer Core card
- **Druid Grove:** d6s accumulated on tended cards between scenes

Prefer d6s wherever possible. Players need a handful of d6s — not a full polyhedral set — for most mechanics.

---

## SOCIAL & NON-COMBAT RESOLUTION

Social encounters use the **same resolution engine** as physical combat (Playtest #1, locked).

- Both sides have a Resolve pool; "damage" chips at it
- When one side's pool is depleted, the confrontation ends (defeated in debate or in battle)
- The terms differ; the mechanics do not
- Social Resolve is narrated as: *composure, credibility, emotional momentum*

Cards work the same way in social scenes. "Attacks" in social contexts are verbal challenges, pressure, or emotional appeals. The roll IS the damage to the other side's Resolve.

---

## CARD PLAY RULES

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
| **Active** | Core cards, equipped Items | Always — never discards |
| **Equip** | Weapon, Armor, Item cards | Until unequipped |
| **Deck** | Undrawn cards | Reshuffles when empty |
| **Discard** | Played or discarded cards | Reshuffles into deck |

**Class-specific zones:** Druid Grove, Rogue Ace Pile — see at-class-quick-ref.

### Luck Check

When a card calls for a **Luck Check**, the player rolls a die (GM adjudicates the die size based on fiction) with no stats applied. Boost dice are eligible. The GM interprets the result in context.

---

## CONDITIONS & KEYWORDS (CANONICAL LOCKED TERMS)

These are the authoritative game terms. For formatting rules (pills vs. bold), see at-card-language.

### Effect Keywords (countable/trackable)
| Term | Meaning |
|---|---|
| **[Boost N]** | Additional dice added to a pool. Expire at scene end. Remove from pool if they show a 1. |
| **[Crit]** | The result tier above Success. Unlocks spend options on the played card. |
| **[Resolve]** | Temporary Hit Die pool set up at combat start. Lost before health pool. Replaces retired Guard. |
| **[Hit Die] / [Hit Dice]** | Player health resource. Always capitalized. Never called "HP." |
| **[Toll]** | GM resource. Generated on any Miss die. Used to escalate scenes. |
| **[Aid]** | Assistance mechanic — functionally similar to Boost. |

### Conditions (narrative vocabulary — GM adjudicates)
| Condition | Narrative Meaning | Fallback Mechanical Reading |
|---|---|---|
| **Exposed** | Vulnerable, open to attack | Next attack against this target gains [Boost 1] |
| **Rattled** | Shaken, off-balance, psychologically disrupted | Target must pass a check before acting next beat |
| **Rooted** | Cannot reposition | Target cannot Move until cleared |
| **Hidden** | Cannot be detected or targeted by normal means | Enemies cannot target without a check first |
| **Bolstered** | Strengthened, healed, fortified | Receive bonus Hit Dice or reroll dice |
| **Marked** | Designated target | Cannot be Hidden from whoever placed the Mark |
| **Sundered** | Structural damage — produced by Barbarian | Consumed by other classes for conditional effects |
| **Break** | Structural impact on an object or enemy | Produces Sundered on Crit when augmented by Barbarian |

### Declared Actions (Bold+Cap in card text)
**Action** · **Reaction** · **Draw** · **Discard** · **Shuffle** · **Cleanse** · **Luck Check** · **Scene**

### Retired Terms — Do Not Use
- ~~Guard~~ → use **[Resolve]**
- ~~Strong Roll~~ → use **[Crit]**
- ~~"while held, [negative effect]"~~ on Flaw cards → hand slot cost IS the consequence
- ~~"the fiction advances"~~ → designer-speak; do not put on player-facing materials

---

## CHARACTER CREATION PROCEDURE

### At the Table (Character Creation = Play)

Character creation is itself a form of play. It takes roughly one hour. Characters emerge from card stems — players are not filling out a stat sheet, they are being prompted into a backstory.

**Steps:**
1. **Draw 5 Instincts** at random from the Instinct card tableau
2. **Choose 1 Background** from the available set (12 options)
3. **Choose 1 Ancestry** from the available set (10 options)
4. **Bond cards:** Assigned or chosen based on party setup (~2 per character)
5. **Flaw cards:** Assigned or drawn; the fill-in stem is completed at the table
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
| Flaw(s) | As assigned |
| Class ability cards | Remaining to total 20 |

**Hypergeometric note:** With 6 Instincts in a 20-card deck, the median is 1 Instinct per 5-card hand (~13% chance of zero-Instinct scenes).

---

## CLASS MECHANICS SUMMARY

Each class has a locked identity, unique mechanic, and primary condition tags it produces. For full detail, load **at-class-quick-ref**.

**Tag ownership rule:** Overlapping production between classes is a design problem. One class owns each condition as primary producer. Others may consume or reference it.

**System-level locks (all classes):**
- Failure always advances the scene — never a dead stop
- Balance deferred to the table — no preemptive caps
- Passive OR active — never both on the same card
- Minimum 20-card deck size
- Tags appear inline in effect text — never in a separate header
- Crit "draw a card" is not a default option

---

## OPEN RULES ITEMS (Unresolved — Do Not Treat as Locked)

These are known gaps in the current rules. Do not present them as locked in any player-facing or GM-facing asset. See at-design-archive for proposed directions on each.

- [ ] **Empty hand rule** — No rule exists for when a player exhausts their full hand
- [ ] **Resolve setup mechanic** — Exact procedure for placing Resolve at combat start not locked
- [ ] **Wave structure** — Whether damage overflows between Resolve and health pool layers
- [ ] **Breather mechanic** — Post-combat recovery exact wording not locked
- [ ] **Cards mandatory vs. optional** — Current stance: "optional but strongly incentivized." Not formally decided.
- [ ] **React window naming** — Should be named in the teach; exact language not locked
- [ ] **Universal discard-to-React** — Proposed but not locked
- [ ] **Paladin identity** — Guard eliminated; new production mechanic TBD (leading direction: Resolve manipulation)
- [ ] **Distance bands** — Not yet defined; borrowing from Daggerheart or custom? Open.

---

## Changelog
- [June 2026] — Created. Synthesized from at-design-system, at-card-language, at-class-quick-ref, at-design-session, playtest-1-report, ability-card-design-reference, and project memory. Covers post-Playtest #1 locked decisions.
