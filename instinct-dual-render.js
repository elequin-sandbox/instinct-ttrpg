/**
 * Dual-purpose Instinct card HTML generator (June 2026 redesign).
 * layout: 'stack' = Strength top / Flaw bottom (production direction)
 * variant: v1 | v2 | v3 | v4 (visual experiments on Bold proof page)
 */
(function (root) {
  var INSTINCT_WORDS = [
    'Bold', 'Perceptive', 'Tenacious', 'Resourceful', 'Charismatic', 'Cunning',
    'Nimble', 'Steadfast', 'Intuitive', 'Fierce', 'Learned', 'Empathic',
    'Vigilant', 'Resilient', 'Subtle', 'Diplomatic', 'Commanding', 'Daring',
    'Resolute', 'Primal',
    'Stoic', 'Impulsive', 'Wistful', 'Sardonic', 'Devoted', 'Impish',
    'Brooding', 'Earnest', 'Guarded', 'Gregarious'
  ];

  function article(word) {
    return /^[aeiouAEIOU]/.test(word) ? 'an' : 'a';
  }

  function preambleHtml(word) {
    var art = article(word);
    return (
      '<div class="instinct-preamble">This instinct is driving your behavior this scene. ' +
      'When you <strong>Reveal</strong> this card, perform an <strong>Action</strong> ' +
      'in ' + art + ' <strong>' + word + '</strong> manner. <strong>Choose one:</strong></div>'
    );
  }

  function strengthText() {
    return (
      'Describe how it benefits your party. If the GM agrees, gain ' +
      '<span class="kw kw-boost">Boost 2</span> on the <strong>Action</strong>.'
    );
  }

  function flawText() {
    return (
      'Describe how it hinders you or your party. If the GM agrees, <strong>Draw 2</strong>.'
    );
  }

  function dividerHtml(variant) {
    if (variant === 'v2') {
      return '<div class="inst-divider"></div>';
    }
    if (variant === 'v3') {
      return '<div class="inst-divider"></div>';
    }
    if (variant === 'v4') {
      return '<div class="inst-divider"><span class="inst-divider-or">OR</span></div>';
    }
    /* v1 default */
    return '<div class="inst-divider"><span class="inst-divider-or">OR</span></div>';
  }

  function forkStackHtml(pos, neg, variant) {
    variant = variant || 'v1';
    return (
      '<div class="instinct-fork fork-' + variant + '">' +
      '<div class="inst-path inst-path-strength">' +
      '<div class="inst-path-lbl">Strength</div>' +
      '<div class="inst-path-txt">' + pos + '</div></div>' +
      dividerHtml(variant) +
      '<div class="inst-path inst-path-flaw">' +
      '<div class="inst-path-lbl">Flaw</div>' +
      '<div class="inst-path-txt">' + neg + '</div></div>' +
      '</div>'
    );
  }

  /** Production stack layout (variant v1 until Annie picks a winner) */
  function renderInstinctDual(word, layout, variant) {
    if (layout === 'b') {
      /* deprecated left/right — map to stack */
      layout = 'stack';
    }
    if (layout === 'a' || !layout) {
      layout = 'stack';
      variant = variant || 'v1';
    }
    var pos = strengthText();
    var neg = flawText();
    return (
      '<div class="card acc-instinct">' +
      '<div class="hdr">' +
      '<div class="hdr-top"><span class="cap cap-accent">Instinct</span>' +
      '<span class="cap cap-neutral">Act</span></div>' +
      '<div class="hdr-name">' + word + '</div></div>' +
      '<div class="cbody cbody-dual">' +
      preambleHtml(word) +
      forkStackHtml(pos, neg, variant) +
      '</div></div>'
    );
  }

  /** Bold-only design experiments for proof page */
  function renderInstinctVariant(word, variant) {
    return renderInstinctDual(word, 'stack', variant);
  }

  function renderInstinctLegacy(word) {
    return (
      '<div class="card acc-instinct">' +
      '<div class="hdr">' +
      '<div class="hdr-top"><span class="cap cap-accent">Instinct</span>' +
      '<span class="cap cap-neutral">Act</span></div>' +
      '<div class="hdr-name">' + word + '</div></div>' +
      '<div class="cbody">' +
      '<div class="elbl">Effect</div>' +
      '<div class="etxt">True to your character, perform any <strong>Action</strong> in a ' +
      word + ' manner. If the GM agrees it is ' + word + ', Gain ' +
      '<span class="kw kw-boost">Boost 2</span> on the <strong>Action</strong>.</div>' +
      '<div class="csec"><div class="clbl">Crit</div><div class="crow"><div class="ci">' +
      'For each <span class="kw kw-crit">Crit</span>, the result is one tier more ' +
      word + ' than you expected.</div></div></div>' +
      '</div></div>'
    );
  }

  /** Plain stack without variant skin (comparison baseline) */
  function renderInstinctMinimal(word) {
    var pos = strengthText();
    var neg = flawText();
    return (
      '<div class="card acc-instinct">' +
      '<div class="hdr">' +
      '<div class="hdr-top"><span class="cap cap-accent">Instinct</span>' +
      '<span class="cap cap-neutral">Act</span></div>' +
      '<div class="hdr-name">' + word + '</div></div>' +
      '<div class="cbody cbody-dual">' + preambleHtml(word) +
      '<div class="instinct-fork" style="flex:1;display:flex;flex-direction:column">' +
      '<div class="inst-path" style="flex:1;justify-content:center;padding:6px 10px">' +
      '<div class="inst-path-txt">' + pos + '</div></div>' +
      '<div style="height:2px;background:#c8a96e;margin:0 8px;opacity:.4"></div>' +
      '<div class="inst-path" style="flex:1;justify-content:center;padding:6px 10px">' +
      '<div class="inst-path-txt">' + neg + '</div></div></div></div></div>'
    );
  }

  root.renderInstinctDual = renderInstinctDual;
  root.renderInstinctVariant = renderInstinctVariant;
  root.renderInstinctLegacy = renderInstinctLegacy;
  root.renderInstinctMinimal = renderInstinctMinimal;
  root.INSTINCT_WORDS = INSTINCT_WORDS;
})(typeof window !== 'undefined' ? window : globalThis);
