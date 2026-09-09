(function () {
  'use strict';

  // ─────────────────────────────────────────────────────────────────────────
  // AFRIVID ASSISTANT
  //
  // WHY THIS WAS REBUILT (2026-09-09)
  // ---------------------------------
  // The previous version kept every fact it knew as one hardcoded string, and it
  // had gone badly stale. Driven live against index.html it said, verbatim:
  //
  //   Q "How much does this cost?"
  //   A "the Free plan is $0/month forever ... Pro plan is $5/month ... you can
  //      always wait until next month's reset if you hit a free-plan limit."
  //   Q "How do I upgrade?"
  //   A "you'll need to email us to arrange payment, as our M-Pesa and MTN
  //      Mobile Money support is still in the works."
  //   Q "What currencies can I pay in?"
  //   A "I'm not sure about the specific currencies we support ... our payment
  //      options are still being developed."
  //   Q "What does Studio Editor do?"
  //   A "There is no 'Studio Editor' tool on our platform."
  //
  // Every one of those is wrong now. The product runs on credits (16 per minute
  // of finished video); free is a ONE-TIME 1,000 credits that never resets;
  // there is a live Paystack checkout taking USD by card and KES by M-Pesa,
  // bank transfer or card; and studio-editor.html is the Video Editor sitting
  // in the homepage nav. The bot was also still sending people to aieditor.html,
  // edit.html, photo.html and design.html — pages nothing on the site links to
  // any more.
  //
  // THE ACTUAL DEFECT is not the wrong figures, it is that the figures were
  // hardcoded here at all. Pricing changed and this file had no way to find out.
  // Editing the strings would have bought exactly one pricing cycle before the
  // same complaint came back.
  //
  // SO: money facts are no longer stored in this file. They are read at runtime
  // out of pricing.html — same origin, the page the owner actually edits when
  // pricing changes, and the page whose own copy says "always quote this, not a
  // guess". buildPricingDigest() lifts the rate, the plan cards, the $1 unlocks,
  // the currency options, the degraded-state list, the comparison table and the
  // FAQ (questions AND their collapsed answers) straight out of it and feeds
  // them to the model as the only permitted source for any figure.
  //
  // If that fetch fails, the assistant is told it has NO pricing data and must
  // refuse to quote a number — a bot that says "I can't confirm today's price,
  // here is the pricing page" is correct, and one that recites last quarter's
  // price from memory is the bug we just removed. There is deliberately no
  // hardcoded price fallback anywhere in this file.
  //
  // What stays hardcoded is only what this file can see is true from the site's
  // own structure: which tools exist and which page each lives on. That is
  // checked against index.html's nav and footer, and retired pages are listed
  // explicitly so the model refuses to recommend them.
  // ─────────────────────────────────────────────────────────────────────────

  var AI_ENDPOINT = 'https://afrivid-tts.reaganayiecho.workers.dev/ai-generate';
  var SUPPORT_EMAIL = 'info@afrivid.studio';

  // Pages the assistant is allowed to name and link. Anything outside this list
  // renders as plain text rather than a link, so a hallucinated page name can
  // never become a clickable 404. Taken from index.html's nav + footer.
  var LIVE_PAGES = {
    'index.html': 1, 'create.html': 1, 'graphics.html': 1, 'studio-editor.html': 1,
    'compress.html': 1, 'studio.html': 1, 'api-docs.html': 1, 'pricing.html': 1,
    'support.html': 1, 'contact.html': 1, 'careers.html': 1, 'terms.html': 1,
    'privacy.html': 1,
  };

  // Structural facts only — no prices, no credit amounts, no plan limits. Those
  // come from the live digest below and nowhere else.
  var STATIC_FACTS = [
    'You are the AfriVid assistant on afrivid.studio — Africa\'s AI video creation platform,',
    'built for African creators. Be warm and brief: 1-4 sentences unless more is genuinely needed.',
    '',
    'TOOLS THAT EXIST TODAY (each is a real page; always name the page):',
    '- Video Creator — create.html. Type a topic and AfriVid writes the script, generates the voice,',
    '  builds the visuals and exports a finished MP4. Three modes are tabs on this same page:',
    '  Short Videos, Ad Maker and Tutorial Maker. Tutorial Maker can also auto-record a live',
    '  walkthrough of any website.',
    '- Graphics and Images — graphics.html. Posters, flyers, banners, social graphics, logos,',
    '  certificates and photorealistic brand images. The AI makes the artwork and writes the words',
    '  as real, legible type, then hands you a canvas where you can move, retype and recolour every',
    '  piece. Photo tools (background removal, enhancement) live here too. It also has a Prompt',
    '  Builder — a chat that interviews you and writes a full prompt you can edit before generating.',
    '- Video Editor — studio-editor.html. This is what the site calls the Studio Editor. Brand your',
    '  background, add a mic overlay, clean the sound with noise reduction and volume boost,',
    '  auto-captions and cut-by-caption, crop, cut and grade. Every change previews instantly in the',
    '  browser; you only wait once, at export.',
    '- Video Compressor — compress.html. Shrink a video\'s file size, trading size against quality.',
    '- My Studio — studio.html. Your library of everything you have made, plus the Billing & Usage',
    '  panel: your credit balance, your current plan, and self-serve payment recovery.',
    '- Developer API — api-docs.html. Send a topic or a finished script, get back an unbranded MP4.',
    '- Pricing — pricing.html. Support AfriVid (donations) — support.html.',
    '- Contact — contact.html. Careers — careers.html (applications reviewed within 14 working days).',
    '- Terms — terms.html. Privacy — privacy.html.',
    '',
    'RETIRED — never recommend, never link, never mention these: design.html (Design Studio),',
    'images.html (Image Generator), aieditor.html (old AI Editor), edit.html (Classic Editor),',
    'photo.html (old Photo Editor). Graphics and Images replaced the design, image and photo tools.',
    'studio-editor.html replaced the old editors. If someone asks for one of these by name, point',
    'them at the tool that replaced it.',
    '',
    'LANGUAGES: 6 — Swahili, Yoruba, Hausa, French, Arabic and Portuguese.',
    'Videos can be created and dubbed in these natively.',
    '',
    'PROMPT EXAMPLES you may offer, in quotes:',
    'Video — "Sunday sermon: [topic] — key points and call to action" | "Why African businesses',
    'need [product]" | "[Topic] explained for African students".',
    'Editing — "Keep the best 60 seconds" | "Remove the first 30 seconds" | "Make it TikTok ready".',
    '',
    'SUPPORT: contact.html, or email ' + SUPPORT_EMAIL + '.',
  ].join('\n');

  // Deliberately worded as "use the block" first and "refuse" second. An earlier
  // draft led with the prohibition and the model over-applied it — asked "how much
  // does this cost?" it answered "I don't know the current cost, see pricing.html"
  // while holding the entire price list in its context. Refusing to read out facts
  // it has been handed is just a politer failure than making them up.
  var RULES = [
    '',
    'RULES — these override everything else:',
    '1. The LIVE PRICING block above is today\'s real, current pricing, read from the site minutes',
    '   ago. It is complete and you are expected to USE it. Cost, credits, the free plan, Pro, the',
    '   $1 unlocks, currencies and payment methods are ALL answered there — answer those questions',
    '   directly and with the actual numbers. Do not deflect to "see the pricing page" for something',
    '   the block already tells you; you may add the pricing.html link after the answer.',
    '2. Every figure you give must be one that literally appears in that block. Do not calculate,',
    '   round, convert between currencies, or recall a figure from anywhere else. If a specific',
    '   number genuinely is not written there, say so rather than producing one.',
    '3. NEVER invent a feature or a page. If something is not in the facts above, say plainly that',
    '   you are not sure and point the person at contact.html or ' + SUPPORT_EMAIL + '.',
    '4. "I do not know" is a correct answer for things outside these facts. A confident wrong price',
    '   is the worst thing you can do — but so is refusing to answer one you were just given.',
    '5. Always name the exact page for what the person wants, e.g. "graphics.html".',
    '6. Plain sentences. No markdown headings, no tables, no bullet lists longer than three items.',
    '',
    'WHEN ASKED WHAT AFRIVID COSTS, lead with the shape of it: free to start with a one-time credit',
    'allowance, Pro monthly, or a single tool unlocked for $1 — with the real figures from the block.',
  ].join('\n');

  // Short on purpose. A long "you must refuse" block here made the model degenerate
  // into repeated punctuation instead of refusing (reproduced by blocking the
  // pricing fetch in Chromium). Money questions never reach the model on this path
  // anyway — see MONEY_RE and the deterministic answer in send() — so this only has
  // to keep a non-money answer from wandering into figures.
  var NO_PRICING_NOTICE =
    '\nYou have no pricing data loaded right now. Do not mention any price, credit amount or plan ' +
    'limit; for anything about money, say the figures are on pricing.html.';

  // A question about money gets a deterministic answer when the live figures are
  // missing, rather than a generated one. There is nothing for a language model to
  // add to "I could not load today's prices", and quite a lot for it to get wrong.
  var MONEY_RE = new RegExp(
    '\\$|\\bksh\\b|\\bkes\\b|\\bprice|\\bpricing\\b|\\bcosts?\\b|how much|\\bcredits?\\b|' +
    '\\bplans?\\b|\\bfree\\b|\\bpro\\b|\\bupgrade|\\bpay\\b|\\bpaying\\b|\\bpayment|\\bbilling\\b|' +
    '\\bsubscri|\\bcharge|\\bdollar|\\bshilling|\\bm-?pesa\\b|\\brefund|\\btier\\b|\\bcheap|' +
    '\\bexpensive\\b|\\bdiscount\\b|\\bmoney\\b|\\bbuy\\b|\\bcurrency\\b|\\bcurrencies\\b', 'i'
  );

  var NO_PRICING_REPLY =
    'I could not load today\'s pricing just now, and I will not guess at a price. ' +
    'The current figures — the free allowance, Pro, and the $1 single-tool unlocks — are all on ' +
    'pricing.html. If that page will not load for you either, ' + SUPPORT_EMAIL + ' reaches a person.';

  // A small model very occasionally returns a 200 with text that has collapsed into
  // repeated punctuation. It is not empty, so the retry loop's emptiness check did
  // not catch it; this does, and the loop tries again.
  function looksBroken(t) {
    if (!t || t.length < 2) return true;
    var letters = (t.match(/[A-Za-z]/g) || []).length;
    if (letters / t.length < 0.5) return true;
    return /([}\]"”.])\s*\1\s*\1\s*\1/.test(t);
  }

  // ── Live pricing, read out of pricing.html ────────────────────────────────
  // Selector-based rather than regex-on-HTML, with a whole-page text fallback if
  // the page is ever restructured, so a redesign of pricing.html degrades this to
  // "noisier but still current" instead of "silently wrong".
  var PRICING_CACHE_KEY = 'av_chat_pricing_v1';
  var PRICING_TTL_MS = 15 * 60 * 1000;
  var pricingDigest = null;
  var pricingPromise = null;

  function tidy(s) {
    return String(s || '')
      .replace(/ /g, ' ')
      .replace(/‑/g, '-')
      .replace(/[ \t]+/g, ' ')
      .replace(/\s*\n\s*/g, '\n')
      .replace(/\n{2,}/g, '\n')
      .trim();
  }

  function textOf(root, sel) {
    var el = root.querySelector(sel);
    return el ? tidy(el.textContent) : '';
  }

  function buildPricingDigest(html) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var parts = [];

    var rate = doc.querySelector('.rate');
    if (rate) {
      parts.push('THE CREDIT RATE\n' +
        tidy(textOf(rate, '.rate-eq') + '\n' + textOf(rate, '.rate-note')));
    }

    // Currency / payment methods. Live, because which methods are offered is tied
    // to the currency and both have changed inside a single week before.
    var cur = [].map.call(doc.querySelectorAll('.cur-opt'), function (o) {
      return tidy(textOf(o, '.cur-lead') + ' — ' + textOf(o, '.cur-sub'));
    }).filter(Boolean);
    if (cur.length) {
      parts.push('CURRENCIES AND PAYMENT METHODS (the buyer chooses on pricing.html)\n' +
        cur.join('\n'));
    }

    var plans = [].map.call(doc.querySelectorAll('.plan'), function (p) {
      var name = textOf(p, '.plan-name');
      var price = tidy(textOf(p, '.plan-price')).replace(/\n/g, ' ');
      var alt = textOf(p, '.plan-alt');
      var desc = textOf(p, '.plan-desc');
      var feats = [].map.call(p.querySelectorAll('li'), function (li) {
        return tidy(li.textContent);
      }).filter(Boolean);
      if (!name && !price) return '';
      return tidy(
        name + ': ' + price + (alt ? ' (' + alt + ')' : '') + '\n' +
        desc + (feats.length ? '\n- ' + feats.join('\n- ') : '')
      );
    }).filter(Boolean);
    if (plans.length) parts.push('PLANS\n' + plans.join('\n\n'));

    var tools = [].map.call(doc.querySelectorAll('.tool'), function (t) {
      var n = textOf(t, '.tool-name');
      if (!n) return '';
      return n + ' — ' + textOf(t, '.tool-window') + '. ' + textOf(t, '.tool-note');
    }).filter(Boolean);
    if (tools.length) parts.push('WHAT ONE DOLLAR BUYS (per-tool unlocks, nothing recurring)\n' + tools.join('\n'));

    var deg = doc.querySelector('.degraded');
    if (deg) {
      var items = [].map.call(deg.querySelectorAll('.deg-item'), function (d) {
        return '- ' + tidy(d.textContent);
      });
      parts.push('WHEN THE FREE ALLOWANCE RUNS OUT\n' +
        tidy(textOf(deg, 'p')) + (items.length ? '\n' + items.join('\n') : ''));
    }

    var table = doc.querySelector('table');
    if (table) {
      var rows = [].map.call(table.querySelectorAll('tr'), function (tr) {
        return [].map.call(tr.querySelectorAll('th,td'), function (c) {
          return tidy(c.textContent) || '-';
        }).join(' | ');
      }).filter(function (r) { return r.replace(/[|\-\s]/g, ''); });
      if (rows.length) parts.push('SIDE BY SIDE\n' + rows.join('\n'));
    }

    // textContent, not innerText: the answers are inside collapsed accordions and
    // an unrendered DOMParser document has no layout anyway. Reading them the lazy
    // way would have shipped the questions with none of the answers.
    var faq = [].map.call(doc.querySelectorAll('.faq-item'), function (f) {
      var q = textOf(f, '.faq-q');
      var a = textOf(f, '.faq-a');
      return q && a ? 'Q: ' + q + '\nA: ' + a : '';
    }).filter(Boolean);
    if (faq.length) parts.push('PRICING FAQ\n' + faq.join('\n'));

    if (parts.length >= 3) return parts.join('\n\n');

    // Structure unrecognised — hand over the page's own words rather than nothing.
    var body = doc.body ? tidy(doc.body.textContent) : '';
    return body.length > 200 ? 'PRICING PAGE TEXT\n' + body.slice(0, 6000) : '';
  }

  function loadPricing() {
    if (pricingDigest) return Promise.resolve(pricingDigest);
    if (pricingPromise) return pricingPromise;

    try {
      var raw = sessionStorage.getItem(PRICING_CACHE_KEY);
      if (raw) {
        var hit = JSON.parse(raw);
        if (hit && hit.digest && (Date.now() - hit.t) < PRICING_TTL_MS) {
          pricingDigest = hit.digest;
          return Promise.resolve(pricingDigest);
        }
      }
    } catch (e) { /* private windows throw on sessionStorage — just refetch */ }

    pricingPromise = fetch('/pricing.html', { credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error('pricing ' + r.status);
        return r.text();
      })
      .then(function (html) {
        var d = buildPricingDigest(html);
        if (!d) throw new Error('empty digest');
        pricingDigest = d;
        try {
          sessionStorage.setItem(PRICING_CACHE_KEY, JSON.stringify({ t: Date.now(), digest: d }));
        } catch (e) { /* quota or private mode — memory cache still holds it */ }
        return d;
      })
      .catch(function () {
        pricingPromise = null;   // let the next question try again
        return null;
      });

    return pricingPromise;
  }

  function systemPrompt() {
    if (!pricingDigest) return STATIC_FACTS + '\n' + NO_PRICING_NOTICE + '\n' + RULES;
    return STATIC_FACTS +
      '\n\n=== LIVE PRICING — read from pricing.html just now. This is the ONLY source you may\n' +
      'use for any figure. It is current; anything you remember about AfriVid pricing is not. ===\n' +
      pricingDigest +
      '\n=== END LIVE PRICING ===\n' + RULES;
  }

  // ── Widget ────────────────────────────────────────────────────────────────
  // Cream, not the near-black panel this used to be. The site is a committed
  // light design — pricing.html says so in its own tokens ("no dark variant
  // anywhere") — and a #0D1117 box sitting on #FBF7EF read as a widget bolted on
  // from another product. Bubbles, labels and the amber are the same values the
  // Prompt Builder chat on graphics.html uses (.pb-msg / .pb-who), so the two
  // chat surfaces on this site now behave and read the same way.
  var widget = document.createElement('div');
  widget.id = 'afrivid-chat-widget';
  widget.innerHTML =
    '<button type="button" id="acw-btn" aria-label="Ask the AfriVid assistant" aria-expanded="false">' +
      '<img src="images/logo.png" alt="" id="acw-btn-logo">' +
    '</button>' +
    '<div id="acw-box" role="dialog" aria-label="AfriVid assistant" hidden>' +
      '<div id="acw-header">' +
        '<div id="acw-ident">' +
          '<div id="acw-avatar" aria-hidden="true">A</div>' +
          '<div>' +
            '<div id="acw-title">AfriVid Assistant</div>' +
            '<div id="acw-status"><span id="acw-dot"></span>Answers from today\'s pricing page</div>' +
          '</div>' +
        '</div>' +
        '<button type="button" id="acw-close" aria-label="Close the assistant">&#10005;</button>' +
      '</div>' +
      '<div id="acw-messages" role="log" aria-live="polite"></div>' +
      '<div id="acw-suggestions"></div>' +
      '<div id="acw-input-area">' +
        '<textarea id="acw-input" rows="1" placeholder="Ask about pricing, credits or any tool…" ' +
          'aria-label="Your question"></textarea>' +
        '<button type="button" id="acw-send" aria-label="Send">' +
          '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
          '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>' +
          '</svg></button>' +
      '</div>' +
    '</div>';

  var style = document.createElement('style');
  style.textContent = [
    '#afrivid-chat-widget{--acw-ink:#17140F;--acw-ink-70:rgba(23,20,15,0.82);',
    '--acw-ink-50:rgba(23,20,15,0.72);--acw-line:rgba(23,20,15,0.10);--acw-card:#FFFFFF;',
    '--acw-amber:#E08A2E;--acw-amber-deep:#C4701E;--acw-amber-text:#9C5918;',
    '--acw-amber-line:rgba(224,138,46,0.30);--acw-ai:#F3EDE0;',
    "position:fixed;bottom:1.5rem;left:1.5rem;z-index:9990;font-family:'Syne',system-ui,sans-serif;}",
    '#acw-btn{width:54px;height:54px;border-radius:50%;background:var(--acw-card);padding:3px;',
    'border:1px solid var(--acw-amber-line);display:flex;align-items:center;justify-content:center;',
    'cursor:pointer;box-shadow:0 6px 22px rgba(23,20,15,0.18);transition:transform .18s,box-shadow .18s;}',
    '#acw-btn:hover{transform:scale(1.06);box-shadow:0 10px 28px rgba(224,138,46,0.30);}',
    '#acw-btn-logo{width:100%;height:100%;object-fit:cover;border-radius:50%;display:block;}',
    '#acw-box{position:fixed;bottom:5.75rem;left:1.5rem;width:min(384px,calc(100vw - 3rem));',
    'max-height:min(600px,calc(100vh - 8rem));background:var(--acw-card);border:1px solid var(--acw-line);',
    'border-radius:18px;overflow:hidden;box-shadow:0 24px 64px rgba(23,20,15,0.22);',
    'display:flex;flex-direction:column;color:var(--acw-ink);}',
    '#acw-box[hidden]{display:none;}',
    '#acw-header{background:rgba(224,138,46,0.08);padding:.85rem 1rem;display:flex;align-items:center;',
    'justify-content:space-between;gap:.5rem;border-bottom:1px solid var(--acw-line);flex-shrink:0;}',
    '#acw-ident{display:flex;align-items:center;gap:.6rem;min-width:0;}',
    '#acw-avatar{width:34px;height:34px;border-radius:10px;background:var(--acw-amber);color:#fff;',
    'display:flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0;}',
    '#acw-title{font-weight:800;font-size:.9rem;letter-spacing:-0.01em;}',
    "#acw-status{font-family:'Space Mono',monospace;font-size:.6rem;letter-spacing:.06em;",
    'text-transform:uppercase;color:var(--acw-ink-50);display:flex;align-items:center;gap:.35rem;margin-top:.15rem;}',
    '#acw-dot{width:6px;height:6px;border-radius:50%;background:#2F7D53;flex-shrink:0;}',
    '#acw-close{background:none;border:none;color:var(--acw-ink-50);cursor:pointer;font-size:.95rem;',
    'padding:.3rem;line-height:1;border-radius:6px;flex-shrink:0;}',
    '#acw-close:hover{background:rgba(23,20,15,0.06);color:var(--acw-ink);}',
    '#acw-messages{flex:1 1 auto;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;',
    'gap:.6rem;min-height:150px;}',
    '.acw-msg{max-width:88%;padding:.6rem .8rem;border-radius:12px;font-size:.83rem;line-height:1.55;',
    'word-wrap:break-word;overflow-wrap:anywhere;}',
    '.acw-msg.acw-bot{align-self:flex-start;background:var(--acw-ai);border:1px solid rgba(23,20,15,0.08);',
    'border-bottom-left-radius:4px;color:var(--acw-ink-70);}',
    '.acw-msg.acw-user{align-self:flex-end;background:rgba(224,138,46,0.16);',
    'border:1px solid rgba(224,138,46,0.32);border-bottom-right-radius:4px;color:var(--acw-ink);}',
    '.acw-msg.acw-err{align-self:flex-start;background:rgba(230,51,41,0.09);',
    'border:1px solid rgba(230,51,41,0.28);color:#AF3427;border-bottom-left-radius:4px;}',
    "#afrivid-chat-widget .acw-who{font-family:'Space Mono',monospace;font-size:.6rem;letter-spacing:1px;",
    'text-transform:uppercase;color:var(--acw-ink-50);margin-bottom:.2rem;}',
    '#afrivid-chat-widget .acw-msg a{color:var(--acw-amber-text);font-weight:700;}',
    '.acw-msg.acw-typing{color:var(--acw-ink-50);font-style:italic;}',
    '#acw-suggestions{padding:0 1rem .75rem;display:flex;flex-wrap:wrap;gap:.35rem;flex-shrink:0;}',
    '#acw-suggestions:empty{display:none;}',
    '#acw-suggestions button{background:rgba(224,138,46,0.08);border:1px solid var(--acw-amber-line);',
    "color:var(--acw-amber-text);padding:.32rem .65rem;border-radius:20px;font-size:.7rem;cursor:pointer;",
    "font-family:'Syne',system-ui,sans-serif;font-weight:700;transition:background .18s;}",
    '#acw-suggestions button:hover{background:rgba(224,138,46,0.18);}',
    '#acw-input-area{padding:.7rem;border-top:1px solid var(--acw-line);display:flex;gap:.5rem;',
    'align-items:flex-end;flex-shrink:0;background:var(--acw-card);}',
    '#acw-input{flex:1;background:#FBF7EF;border:1px solid var(--acw-line);color:var(--acw-ink);',
    "padding:.55rem .7rem;border-radius:10px;font-family:'Syne',system-ui,sans-serif;font-size:.83rem;",
    'resize:none;outline:none;max-height:90px;line-height:1.45;}',
    '#acw-input:focus{border-color:var(--acw-amber-line);box-shadow:0 0 0 3px rgba(224,138,46,0.12);}',
    '#acw-send{background:var(--acw-amber);border:none;color:#fff;width:36px;height:36px;border-radius:10px;',
    'cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .18s;}',
    '#acw-send:hover{background:var(--acw-amber-deep);}',
    '#acw-send:disabled{opacity:.5;cursor:default;}',
    // The old panel was a fixed 340px anchored to a button 2rem off the corner, so on a
    // small phone it hung off the edge. Full-bleed with a gutter below 520px instead.
    '@media(max-width:520px){#afrivid-chat-widget{bottom:1rem;left:1rem;}',
    '#acw-box{left:.75rem;right:.75rem;width:auto;bottom:5rem;max-height:calc(100vh - 7rem);',
    'max-height:calc(100dvh - 7rem);}}',
    '@media(prefers-reduced-motion:reduce){#acw-btn{transition:none;}#acw-btn:hover{transform:none;}}',
  ].join('');

  document.head.appendChild(style);

  function mount() {
    if (!document.body || document.getElementById('acw-btn')) return;
    document.body.appendChild(widget);
    wire();
  }
  // Not DOMContentLoaded-only: if this file is ever loaded async, deferred, or
  // injected after load, that event has already fired and the widget would never
  // have appeared at all.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();

  // ── Rendering ─────────────────────────────────────────────────────────────
  var ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return ESCAPES[c]; });
  }

  // Model output was previously written straight into innerHTML. That rendered any
  // "<" in an answer as broken markup and made every reply a script-injection path
  // through a third-party endpoint. Escape first, then add back only the links and
  // the one markdown form the model actually emits.
  var LINK_RE =
    /(https?:\/\/[^\s<>()]+)|([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})|\b([a-z0-9-]+\.html)(#[A-Za-z0-9_-]*)?/g;

  function render(text) {
    var out = esc(String(text).trim());
    out = out.replace(LINK_RE, function (m, url, mail, page, hash) {
      if (url) return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
      if (mail) return '<a href="mailto:' + mail + '">' + mail + '</a>';
      // Unknown or retired page names stay as plain text — never a clickable 404.
      if (page && LIVE_PAGES[page]) return '<a href="/' + page + (hash || '') + '">' + page + (hash || '') + '</a>';
      return m;
    });
    out = out.replace(/\*\*([^*<>]+)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/^[ \t]*[-*][ \t]+/gm, '• ');
    return out.replace(/\n/g, '<br>');
  }

  function bubble(text, kind) {
    var msgs = document.getElementById('acw-messages');
    if (!msgs) return null;
    var div = document.createElement('div');
    div.className = 'acw-msg acw-' + kind;
    var label = kind === 'user' ? 'You' : kind === 'err' ? 'Something went wrong' : 'AfriVid';
    div.innerHTML = '<div class="acw-who">' + esc(label) + '</div>' +
      (kind === 'user' ? esc(text).replace(/\n/g, '<br>') : render(text));
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  // ── Suggestions ───────────────────────────────────────────────────────────
  // The old chips were all prompt-writing ("Church video", "AI edit prompts") and
  // vanished permanently after one click. These are the questions people actually
  // arrive with, and they stay put.
  var SUGGESTIONS = [
    ['What does it cost?', 'How much does AfriVid cost?'],
    ['What is free?', 'What exactly do I get on the free plan?'],
    ['How do I pay?', 'How do I upgrade, and what payment methods can I use?'],
    ['How credits work', 'How do credits work and how many does a video cost?'],
    ['Which tool?', 'Which AfriVid tool should I use to edit a video I already have?'],
  ];

  function paintSuggestions() {
    var box = document.getElementById('acw-suggestions');
    if (!box) return;
    box.innerHTML = '';
    SUGGESTIONS.forEach(function (s) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = s[0];
      b.addEventListener('click', function () { ask(s[1]); });
      box.appendChild(b);
    });
  }

  // ── Small talk ────────────────────────────────────────────────────────────
  // Whole-message matches only. A substring check here used to hijack real
  // questions ("...thanks!") into a canned reply instead of answering them.
  var SMALL_TALK = [
    [['hello', 'hi', 'hey', 'habari', 'jambo', 'bonjour', 'sup', 'yo', 'mambo'],
     'Hey! I can tell you what AfriVid costs, how credits work, or which tool you need. What are you after?'],
    [['thanks', 'thank you', 'asante', 'merci', 'thx', 'ty', 'cheers'],
     'Anytime. Anything else you want to know about AfriVid?'],
    [['bye', 'goodbye', 'later', 'kwaheri', 'au revoir', 'ciao'],
     'Goodbye — come back whenever you need a hand.'],
    [['who are you', 'what are you', 'are you ai', 'are you human', 'are you a bot', 'who made you'],
     'I am AfriVid\'s assistant — an AI. I read the live pricing page before I answer, so the ' +
     'numbers I give you are today\'s, and I will tell you when I do not know something.'],
    [['how are you', 'how r you', 'how are u', 'hows it going'],
     'Ready to help. What would you like to know about AfriVid?'],
  ];

  function smallTalk(normalized) {
    for (var i = 0; i < SMALL_TALK.length; i++) {
      if (SMALL_TALK[i][0].indexOf(normalized) !== -1) return SMALL_TALK[i][1];
    }
    return null;
  }

  // ── Conversation ──────────────────────────────────────────────────────────
  var history = [];
  var busy = false;

  function setBusy(v) {
    busy = v;
    var send = document.getElementById('acw-send');
    if (send) send.disabled = v;
  }

  function ask(text) {
    var input = document.getElementById('acw-input');
    if (input) input.value = text;
    send();
  }

  async function send() {
    if (busy) return;
    var input = document.getElementById('acw-input');
    if (!input) return;
    var msg = input.value.trim();
    if (!msg) return;
    input.value = '';
    input.style.height = '';
    bubble(msg, 'user');

    var normalized = msg.toLowerCase().replace(/[.,!?;:]+$/g, '').trim();
    var canned = smallTalk(normalized);
    if (canned) {
      bubble(canned, 'bot');
      // Kept in history so a follow-up like "what did you just say" still makes
      // sense to the model — the old build dropped these turns on the floor.
      history.push({ role: 'user', content: msg }, { role: 'assistant', content: canned });
      return;
    }
    if (normalized.length < 2) {
      bubble('Ask me something about AfriVid — pricing, credits, or which tool to use.', 'bot');
      return;
    }

    setBusy(true);
    history.push({ role: 'user', content: msg });
    var typing = bubble('Checking today\'s pricing…', 'bot');
    if (typing) typing.classList.add('acw-typing');

    // Facts first, always. Answering before the digest lands is how the old bot
    // ended up confidently reciting a price that had not been true since morning.
    await loadPricing();

    // No live figures + a money question = answer it in code and stop. Sending it
    // to the model here produced literal gibberish in testing, and even a clean
    // refusal would only be a slower way of saying this.
    if (!pricingDigest && MONEY_RE.test(msg)) {
      if (typing) typing.remove();
      bubble(NO_PRICING_REPLY, 'bot');
      history.push({ role: 'assistant', content: NO_PRICING_REPLY });
      setBusy(false);
      return;
    }
    if (typing) typing.innerHTML = '<div class="acw-who">AfriVid</div>Thinking…';

    var reply = null;
    var timedOut = false;
    for (var attempt = 1; attempt <= 3 && !reply; attempt++) {
      try {
        var controller = new AbortController();
        var t = setTimeout(function () { controller.abort(); }, 22000);
        var res = await fetch(AI_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal,
          body: JSON.stringify({
            max_tokens: 400,
            messages: [{ role: 'system', content: systemPrompt() }].concat(history.slice(-6)),
          }),
        });
        clearTimeout(t);
        if (res.ok) {
          var data = await res.json();
          var text = data && data.content && data.content[0] && data.content[0].text;
          if (text && !looksBroken(text.trim())) { reply = text.trim(); break; }
        }
      } catch (e) {
        timedOut = (e && e.name === 'AbortError');
      }
      // Workers AI occasionally returns a 200 with no text at all. One unlucky
      // request used to look like a permanent failure; retry instead.
      if (!reply && attempt < 3) await new Promise(function (r) { setTimeout(r, 400 * attempt); });
    }

    if (typing) typing.remove();
    if (reply) {
      bubble(reply, 'bot');
      history.push({ role: 'assistant', content: reply });
      if (history.length > 20) history = history.slice(-20);
    } else {
      history.pop();
      bubble(
        timedOut
          ? 'That took too long to answer. Try a shorter question, or read it directly on pricing.html.'
          : 'I could not reach the assistant just now. Pricing is on pricing.html, and ' +
            SUPPORT_EMAIL + ' always reaches a person.',
        'err'
      );
    }
    setBusy(false);
    var i2 = document.getElementById('acw-input');
    if (i2) i2.focus();
  }

  // ── Wiring ────────────────────────────────────────────────────────────────
  var open = false;

  function toggle(force) {
    var box = document.getElementById('acw-box');
    var btn = document.getElementById('acw-btn');
    if (!box) return;
    open = (typeof force === 'boolean') ? force : !open;
    box.hidden = !open;
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      // Warm the facts the moment the panel opens, so the first answer does not
      // pay for the fetch. Never on page load — most visitors never open this.
      loadPricing();
      var msgs = document.getElementById('acw-messages');
      if (msgs && !msgs.children.length) {
        bubble('Hi! I am the AfriVid assistant. I read the live pricing page before I answer, ' +
          'so ask me what things cost, how credits work, or which tool does what. ' +
          'If I do not know something, I will say so.', 'bot');
      }
      var input = document.getElementById('acw-input');
      if (input) input.focus();
    }
  }

  function wire() {
    document.getElementById('acw-btn').addEventListener('click', function () { toggle(); });
    document.getElementById('acw-close').addEventListener('click', function () { toggle(false); });
    document.getElementById('acw-send').addEventListener('click', function () { send(); });
    var input = document.getElementById('acw-input');
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    });
    input.addEventListener('input', function () {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 90) + 'px';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && open) toggle(false);
    });
    paintSuggestions();
  }

  // Kept for any page still calling the old global names inline.
  window.toggleAfriVidChat = function () { toggle(); };
  window.sendAfriVidChat = function () { send(); };
  window.acwSuggest = function (text) { ask(text); };
})();
