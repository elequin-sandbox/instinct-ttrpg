// Local example cards for offline development.
// Only loaded on localhost — see the inline script in index.html <head>.
window.LOCAL_CARDS = [
  {
    k: "vanish-rogue",
    n: "Vanish",
    h: '<div class="card"><div class="ch"><span class="cn">Vanish</span><span class="cb">React</span></div><div class="cbody"><div class="flv">You were never quite where they thought.</div><div class="hr"></div><div class="elbl">Effect</div><div class="etxt">Perform a <span class="tp ts">Stealth</span> check. On success, remove yourself from your current position — you end up somewhere nearby.</div><div class="csec"><div class="clbl">Crit</div><div class="crow"><div class="ci"><span class="tp tc">1</span> Choose an ally — their next action is concealed.</div></div></div></div><div class="cf"><span class="fclass">Rogue</span><span class="fright">Tier 1 · React</span></div></div>',
    updated: "2024-03-01T00:00:00Z",
    rework: "2024-03-01"
  },
  {
    k: "into-the-fray-barbarian",
    n: "Into the Fray",
    h: '<div class="card"><div class="ch"><span class="cn">Into the Fray</span><span class="cb">Act</span></div><div class="cbody"><div class="flv">You don\'t approach. You arrive.</div><div class="hr"></div><div class="elbl">Effect</div><div class="etxt">Perform an <span class="tp ts">Athletics</span> check. On success, close any distance and <span class="tp tv">Strike</span> before anyone can react.</div><div class="csec"><div class="clbl">Crit</div><div class="crow"><div class="ci"><span class="tp tc">1</span> An ally gains a <span class="tp tb">Boost</span> die against this target.</div></div></div></div><div class="cf"><span class="fclass">Barbarian</span><span class="fright">Tier 1 · Act</span></div></div>',
    updated: "2024-03-01T00:00:00Z",
    rework: "2024-03-01"
  },
  {
    k: "called-to-respond-cleric",
    n: "Called to Respond",
    h: '<div class="card"><div class="ch"><span class="cn">Called to Respond</span><span class="cb">React</span></div><div class="cbody"><div class="flv">You never lead. You answer.</div><div class="hr"></div><div class="elbl">Effect</div><div class="etxt">When an ally fails a check, perform a <span class="tp ts">Faith</span> check. On success, they may reroll before the GM narrates consequences.</div><div class="csec"><div class="clbl">Crit</div><div class="crow"><div class="ci"><span class="tp tc">1</span> They also gain a <span class="tp tb">Boost</span> die on the reroll.</div></div></div></div><div class="cf"><span class="fclass">Cleric</span><span class="fright">Tier 1 · React</span></div></div>',
    updated: "2024-03-01T00:00:00Z",
    rework: "2024-03-01"
  },
  {
    k: "eldritch-strike-warlock",
    n: "Eldritch Strike",
    h: '<div class="card"><div class="ch"><span class="cn">Eldritch Strike</span><span class="cb">Act</span></div><div class="cbody"><div class="flv">The power is yours. So is the price.</div><div class="hr"></div><div class="elbl">Effect</div><div class="etxt">Remove a hit die from your pool and <span class="tp tv">Strike</span> at any range — add that die to your strike.</div><div class="csec"><div class="clbl">Crit</div><div class="crow"><div class="ci"><span class="tp tc">1</span> Target loses next defensive action.</div><div class="ci"><span class="tp tc">1</span> Regain the spent hit die.</div></div></div></div><div class="cf"><span class="fclass">Warlock</span><span class="fright">Tier 1 · Act</span></div></div>',
    updated: "2024-03-01T00:00:00Z",
    rework: "2024-03-01"
  },
  {
    k: "weapon-master-fighter-core",
    n: "Weapon Master",
    h: '<div class="card fighter"><div class="core-header"><span class="core-keyword">Core</span><span class="core-class-name">Fighter</span></div><div class="card-name-zone"><div class="card-name">Weapon Master</div><div class="card-subtitle">Your hands know the weight of everything.</div></div><div class="card-body"><div class="zone-label">Passive</div><div class="effect-text">Whenever you equip any Item card into your Equip zone, Draw 1.</div><div class="rule"></div><div class="zone-label">Note</div><div class="effect-text" style="font-size:8.5px; color:#5a4a20; font-style:italic;">Triggers on any equip — weapon, armor, or otherwise. Rewards active loadout management every scene.</div></div><div class="card-footer"><span class="footer-left">Fighter · Core</span><span class="footer-right">Weapon Master</span></div></div>',
    updated: "2024-03-01T00:00:00Z",
    rework: "2024-03-01"
  }
];

console.log('[DEV] local/file mode — ', window.LOCAL_CARDS.length, 'example cards loaded');
