// ── CHECKOUT ──────────────────────────────────────────────────────────────────
// Shared by pricing.html and every page with an Upgrade entry point.
//
// WHAT THIS FILE DOES NOT DO: grant anything. The Paystack `callback` below fires
// in the buyer's own browser and is trivially forgeable — a user could call it by
// hand from the console. It is used for one thing only, which is to change what is
// on screen. The real grant happens server-side in /webhooks/paystack (app.py),
// which verifies Paystack's HMAC signature before calling billing.apply_upgrade().
// So after a successful payment this file does not say "you're upgraded" — it polls
// /credits until the SERVER says so, and only then shows success.
//
// Paystack's inline.js is loaded on first checkout rather than in every page's
// <head>: most visitors never click Upgrade, and they should not pay for the
// script's download.
(function () {
  var API = 'https://afrivid-processor-222827815864.africa-south1.run.app';
  // v2 specifically — a real ES6 class exposing `new PaystackPop().checkout({...})`
  // with onSuccess/onCancel hooks. v1/inline.js (the old URL this pointed at) still
  // only exposes the static PaystackPop.setup({...}).openIframe() object form, which
  // is not a constructor — confirmed by actually loading both scripts and inspecting
  // what each assigns to window.PaystackPop, not assumed from documentation alone.
  // Apple Pay requires v2.
  var INLINE_JS = 'https://js.paystack.co/v2/inline.js';

  // ── CURRENCY ────────────────────────────────────────────────────────────────
  // Why this exists: the merchant account's default currency is KES, and Paystack
  // only offers Mobile Money (M-Pesa) and Bank Transfer on KES-denominated
  // charges. A USD charge shows Card and nothing else. Charging every Kenyan
  // buyer in dollars therefore hides the two methods most of them actually use.
  //
  // The buyer picks, explicitly, on pricing.html. Deliberately NOT geo-IP: a VPN
  // or a traveller gets guessed wrong, and a silent wrong guess about what
  // currency someone is being charged in is a bad way to be wrong.
  //
  // The rate is a plain constant on purpose. Checkout must never depend on a live
  // FX call — a rate API timing out would turn "open checkout" into a failure
  // mode this flow does not have today, and a rate that is a few percent stale is
  // a far smaller problem than an Upgrade button that does not work.
  //
  // Rate checked 2026-09-08 against two independent sources, which agreed:
  //   open.er-api.com (exchangerate-api.com)  1 USD = 129.4475 KES
  //   @fawazahmed0/currency-api via jsDelivr  1 USD = 129.4300 KES
  // Set to 130: about 0.4% over mid-market, which is well inside a card network's
  // own spread, and it lands the shown prices on clean figures (KSh 650, KSh 130).
  //
  // TO REFRESH: check mid-market USD/KES, change the number, update the date and
  // sources on this comment, and update PAYSTACK_AMOUNT_PLANS['KES'] in app.py
  // (afrivid-processor) so the webhook's amount fallback keeps telling the truth.
  var USD_TO_KES_RATE = 130;

  var CURRENCY_KEY = 'av_currency';
  var SUPPORTED = { USD: true, KES: true };

  // USD is the default so that anyone who never touches the toggle gets exactly
  // today's behaviour. The choice is remembered because it is made on
  // pricing.html but spent on the tool pages, where the upgrade prompt appears.
  function currency() {
    try {
      var v = localStorage.getItem(CURRENCY_KEY);
      if (v && SUPPORTED[v]) return v;
    } catch (e) { /* private windows throw on localStorage — fall through */ }
    return 'USD';
  }
  window.avGetCurrency = currency;

  window.avSetCurrency = function (cur) {
    cur = String(cur || '').toUpperCase();
    if (!SUPPORTED[cur]) return currency();
    try { localStorage.setItem(CURRENCY_KEY, cur); } catch (e) {}
    renderPrices();
    try {
      document.dispatchEvent(new CustomEvent('av:currency', { detail: { currency: cur } }));
    } catch (e) {}
    return cur;
  };

  // `amount` is USD cents — the smallest unit, which is what Paystack expects and
  // what PAYSTACK_AMOUNT_PLANS in app.py maps back from if metadata is ever lost.
  // These must stay in step with apply_upgrade()'s plan ids in credits.py.
  var PLANS = {
    pro_subscription: { amount: 500, label: 'Pro', period: '/month' },
    tool_compressor:  { amount: 100, label: 'Video Compressor', period: '' },
    tool_graphics:    { amount: 100, label: 'Graphics and Images', period: '' },
    tool_editor:      { amount: 100, label: 'Video Editor', period: '' },
    tool_video:       { amount: 100, label: 'Video Creation', period: '' },
    tool_api:         { amount: 100, label: 'Developer API', period: '' },
  };

  // Rounded to the whole shilling, not to a "nice" number: KES has a cent subunit
  // Paystack counts in, but nobody prices in cents here, and rounding $1 up to the
  // nearest ten shillings would be a double-digit percentage markup on the cheap
  // plans. At 130 this is exact anyway — 650 and 130.
  Object.keys(PLANS).forEach(function (id) {
    var p = PLANS[id];
    p.shillings = Math.round((p.amount / 100) * USD_TO_KES_RATE);
    p.kes = p.shillings * 100; // KES cents — Paystack's smallest unit, same as USD
  });
  window.AFRIVID_PLANS = PLANS;
  window.AFRIVID_USD_TO_KES = USD_TO_KES_RATE;

  // "$5" / "KSh 650". One owner for every price string on the site.
  function price(planId, cur) {
    var p = PLANS[planId];
    if (!p) return '';
    if ((cur || currency()) === 'KES') return 'KSh ' + p.shillings.toLocaleString('en-US');
    return '$' + (p.amount / 100);
  }
  window.avPrice = price;

  // "Pro — $5/month", for the success overlay and anywhere else naming a purchase.
  function planLabel(planId, cur) {
    var p = PLANS[planId];
    if (!p) return '';
    return p.label + ' — ' + price(planId, cur) + p.period;
  }
  window.avPlanLabel = planLabel;

  // Live price text, so no page hardcodes a figure that the toggle then contradicts.
  //   data-av-price="pro_subscription"                     -> "$5"
  //   data-av-price-alt="pro_subscription"                 -> the OTHER currency
  //   data-av-price-tpl="Go Pro — {price}/month"           -> templated
  // Elements the disabled-state path below has taken over are left alone.
  function renderPrices() {
    var cur = currency();
    var other = cur === 'KES' ? 'USD' : 'KES';
    var els = document.querySelectorAll('[data-av-price],[data-av-price-alt]');
    Array.prototype.forEach.call(els, function (el) {
      if (el.getAttribute('aria-disabled') === 'true') return;
      var alt = el.hasAttribute('data-av-price-alt');
      var id = el.getAttribute(alt ? 'data-av-price-alt' : 'data-av-price');
      if (!PLANS[id]) return;
      var tpl = el.getAttribute('data-av-price-tpl') || '{price}';
      el.textContent = tpl.replace('{price}', price(id, alt ? other : cur));
    });
  }
  window.avRenderPrices = renderPrices;

  var POLL_INTERVAL_MS = 2000;
  var POLL_TIMEOUT_MS = 20000;

  // ── One-shot loaders ────────────────────────────────────────────────────────
  // Each of these caches its PROMISE, not its result, so two fast clicks share one
  // network request instead of racing two.
  var keyPromise = null;
  var inlinePromise = null;
  var authPromise = null;

  // Also cache the settled VALUES, not just the promises — this is what lets
  // avStartCheckout() below open checkout with zero awaits on the common path.
  // Real bug this fixes: a user reported checkout consistently failing (never
  // reproduced in this sandbox's Chromium, which is lenient about it) while
  // several genuine network awaits sat between their click and the
  // .checkout() call — auth resolution, the public-key fetch, loading
  // Paystack's script. Safari (mobile especially, WebKit's documented
  // behaviour) revokes "this call came from a real user gesture" the moment
  // code awaits real I/O, and Apple Pay/payment popups require that gesture
  // to still be live at the moment checkout() is called. Fix: do all three
  // lookups eagerly at page load via prewarm() below, so that by the time a
  // real click happens they are already-resolved values — no I/O, no lost
  // gesture. The old async chain is kept as a slow-path fallback only for the
  // rare click that lands before prewarm finishes.
  var cachedUser = null, cachedKey = null, cachedPop = null;

  function prewarm() {
    currentUser().then(function (u) { cachedUser = u; }).catch(function () {});
    publicKey().then(function (k) { cachedKey = k; }).catch(function () {});
    paystackInline().then(function (P) { cachedPop = P; }).catch(function () {});
  }

  // support.html carries no [data-av-plan] buttons (a donation isn't a plan),
  // so wire()'s own prewarm() call below never fires for it. Exposed so that
  // page can warm the same three lookups itself at load — without this, its
  // first donate click would fall onto the slow (awaiting) path and risk the
  // exact gesture-loss bug documented above avStartCheckout.
  window.avPrewarmCheckout = prewarm;

  function publicKey() {
    if (!keyPromise) {
      keyPromise = fetch(API + '/config/paystack-public-key')
        .then(function (r) { return r.json(); })
        .then(function (d) { return (d && d.key) || null; })
        .catch(function (e) {
          console.warn('[Checkout] could not read the public key:', e && e.message);
          // Null, not a rejection: "we could not reach the server" and "payments are
          // not configured" land the user in the same honest disabled state.
          return null;
        });
    }
    return keyPromise;
  }

  function paystackInline() {
    if (!inlinePromise) {
      inlinePromise = new Promise(function (resolve, reject) {
        if (window.PaystackPop) { resolve(window.PaystackPop); return; }
        var s = document.createElement('script');
        s.src = INLINE_JS;
        s.async = true;
        s.onload = function () {
          if (window.PaystackPop) resolve(window.PaystackPop);
          else reject(new Error('Paystack loaded but did not start'));
        };
        s.onerror = function () { reject(new Error('Could not reach Paystack')); };
        document.head.appendChild(s);
      });
      // A failed load must not be cached forever — the next click should retry.
      inlinePromise.catch(function () { inlinePromise = null; });
    }
    return inlinePromise;
  }

  // The signed-in Firebase user. Most tool pages already keep one on
  // window.currentUser; pricing.html deliberately carries no auth stack at all, so
  // this falls back to reading the session straight from Firebase.
  function currentUser() {
    if (window.currentUser) return Promise.resolve(window.currentUser);
    if (!authPromise) {
      authPromise = (async function () {
        var cfg = window.AFRIVID_CONFIG || {
          apiKey: 'AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0',
          authDomain: 'afrivid-studio.firebaseapp.com',
          projectId: 'afrivid-studio',
        };
        var appMod = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js');
        var authMod = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js');
        var app = appMod.getApps().length ? appMod.getApps()[0] : appMod.initializeApp(cfg);
        var auth = authMod.getAuth(app);
        // onAuthStateChanged rather than auth.currentUser: restoring a persisted
        // session is asynchronous, and reading currentUser immediately after
        // getAuth() returns null for a user who is in fact signed in.
        return await new Promise(function (resolve) {
          var stop = authMod.onAuthStateChanged(auth, function (user) {
            if (stop) stop();
            if (user) window.currentUser = user;
            resolve(user || null);
          });
        });
      })();
      authPromise.catch(function () { authPromise = null; });
    }
    return authPromise;
  }

  async function authHeaders(user) {
    var headers = { 'Content-Type': 'application/json' };
    if (user && typeof user.getIdToken === 'function') {
      try { headers['Authorization'] = 'Bearer ' + (await user.getIdToken()); }
      catch (e) { console.warn('[Checkout] no ID token:', e && e.message); }
    }
    return headers;
  }

  function entitlements(user) {
    return authHeaders(user)
      .then(function (h) { return fetch(API + '/credits', { headers: h }); })
      .then(function (r) { return r.json(); })
      .catch(function () { return null; });
  }

  // ── Did the server actually apply it? ───────────────────────────────────────
  // Compared against a snapshot taken BEFORE checkout rather than against absolute
  // values, because "has editor access" is already true for someone buying a second
  // fortnight — only the CHANGE proves this payment landed.
  function applied(plan, before, after) {
    if (!after || !after.available) return false;
    // No usable "before" reading means there is nothing to compare against, and a
    // guess here would tell an already-Pro user their renewal landed the instant
    // they paid, whether or not it had. Better to fall through to the timeout
    // message, which is honest and still tells them not to pay twice.
    if (!before || !before.available) return false;
    var was = before;
    function grew(field) { return num(after[field]) > num(was[field]); }
    function num(v) { return typeof v === 'number' ? v : 0; }

    switch (plan) {
      case 'pro_subscription':
        return grew('subscription_expires') ||
               (after.tier === 'pro_subscription' && was.tier !== 'pro_subscription');
      case 'tool_compressor': return grew('compressor_expires');
      case 'tool_graphics':   return grew('graphics_expires');
      case 'tool_editor':     return grew('editor_expires');
      case 'tool_video':      return grew('credits_remaining');
      case 'tool_api':        return grew('api_seconds_left');
      default: return false;
    }
  }

  // ── The confirming/success overlay ──────────────────────────────────────────
  // Injected here rather than duplicated into eight pages' markup. Deliberately
  // inline-styled and self-contained so it looks the same on the light marketing
  // pages and the dark editor pages.
  function overlay() {
    var el = document.getElementById('av-checkout-overlay');
    if (el) return el;
    el = document.createElement('div');
    el.id = 'av-checkout-overlay';
    el.setAttribute('role', 'status');
    el.style.cssText = 'display:none;position:fixed;inset:0;z-index:100000;' +
      'background:rgba(10,8,5,0.72);backdrop-filter:blur(4px);' +
      'align-items:center;justify-content:center;padding:1.5rem;';
    el.innerHTML =
      '<div style="background:#FBF7EF;color:#17140F;max-width:420px;width:100%;' +
      'border-radius:16px;padding:1.75rem;text-align:center;' +
      'font-family:Syne,system-ui,sans-serif;box-shadow:0 24px 60px rgba(0,0,0,0.35);">' +
      '<div id="av-checkout-title" style="font-weight:800;font-size:1.15rem;margin-bottom:0.5rem;"></div>' +
      '<div id="av-checkout-body" style="font-size:0.9rem;line-height:1.55;color:rgba(23,20,15,0.72);"></div>' +
      '<div id="av-checkout-actions" style="margin-top:1.25rem;display:flex;gap:0.6rem;justify-content:center;flex-wrap:wrap;"></div>' +
      '</div>';
    document.body.appendChild(el);
    return el;
  }

  function show(title, body, actions) {
    var el = overlay();
    el.style.display = 'flex';
    el.querySelector('#av-checkout-title').textContent = title;
    el.querySelector('#av-checkout-body').textContent = body;
    var bar = el.querySelector('#av-checkout-actions');
    bar.innerHTML = '';
    (actions || []).forEach(function (a) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = a.label;
      b.style.cssText = 'font-family:inherit;font-weight:800;font-size:0.88rem;cursor:pointer;' +
        'padding:0.7rem 1.4rem;border-radius:10px;border:1px solid rgba(23,20,15,0.18);' +
        (a.primary ? 'background:#E08A2E;border-color:#E08A2E;color:#fff;' : 'background:transparent;color:#17140F;');
      b.addEventListener('click', a.onClick);
      bar.appendChild(b);
    });
  }

  function hide() {
    var el = document.getElementById('av-checkout-overlay');
    if (el) el.style.display = 'none';
  }
  window.avCloseCheckoutOverlay = hide;

  // ── After the money moves ───────────────────────────────────────────────────
  async function confirmUpgrade(plan, user, beforePromise, reference, cur) {
    show('Payment received',
         'Confirming with our servers and upgrading your account. This takes a few seconds.',
         []);

    // Awaited here, not before checkout() was called — this is a real network
    // fetch, and the whole point of the fast path above is that nothing like
    // it sits between the click and opening checkout. By the time payment has
    // gone through, gesture concerns are irrelevant, so it's free to wait here.
    var before = await beforePromise;

    var deadline = Date.now() + POLL_TIMEOUT_MS;
    while (Date.now() < deadline) {
      await new Promise(function (r) { setTimeout(r, POLL_INTERVAL_MS); });
      var after = await entitlements(user);
      if (applied(plan, before, after)) {
        show('You are upgraded',
             (PLANS[plan] ? planLabel(plan, cur) + ' is active on your account.' : 'Your upgrade is active.') +
             ' Everything it unlocks is available now.',
             [{ label: 'Continue', primary: true, onClick: function () { window.location.reload(); } }]);
        return;
      }
    }

    // Timed out. The payment is real and Paystack will keep retrying the webhook,
    // so this must never read as a failure — a user told "that didn't work" pays
    // twice, which is the one outcome worse than waiting.
    show('Payment went through',
         'Your payment succeeded. Our server has not finished applying it yet, which ' +
         'usually clears within a minute or two — reload this page shortly and it ' +
         'should be there. If it is not, contact us with reference ' + reference +
         ' and we will sort it out. Do not pay again.',
         [{ label: 'Reload', primary: true, onClick: function () { window.location.reload(); } },
          { label: 'Close', onClick: hide }]);
  }

  // Shared by both paths below. Opens the real Paystack popup — called either
  // with zero preceding awaits (the fast path) or after the slow path's own
  // async lookups finished. `before` is a PROMISE, not a value — never awaited
  // here, only inside confirmUpgrade(), well after the click's gesture window
  // stops mattering.
  function openCheckout(planId, plan, user, key, Pop) {
    var beforePromise = entitlements(user);

    // Paystack accepts only alphanumerics and - . = in a reference, so the plan id's
    // underscores are flattened rather than passed through.
    var reference = 'av-' + planId.replace(/_/g, '-') + '-' + Date.now() + '-' +
                    String(user.uid || '').replace(/[^A-Za-z0-9]/g, '').slice(0, 6);

    // InlineJS v2 (the `new PaystackPop().checkout()` object form) rather than the
    // older static `PaystackPop.setup({...}).openIframe()` — Apple Pay only renders
    // on v2, and Paystack picks which payment methods (card / Apple Pay / etc.) to
    // offer per device automatically, so nothing else here needs to branch on
    // device. Same payload shape as before; only the calling convention and the
    // two callback names (onSuccess/onCancel replacing callback/onClose) changed.
    // Both amounts are in their currency's smallest unit — USD cents and KES
    // cents — which is the one convention Paystack takes, so this is a swap of
    // two numbers and nothing else. Read once, here, so the amount and the
    // currency label can never come from two different reads of the toggle.
    var cur = currency();
    var amount = cur === 'KES' ? plan.kes : plan.amount;

    return new Pop().checkout({
      key: key,
      email: user.email,
      amount: amount,
      currency: cur,
      ref: reference,
      // The ONLY thing tying this payment back to an account. app.py's webhook
      // reads uid and plan from here; without them the charge lands as "PAID BUT
      // UNAPPLIED" and needs a human. Currency deliberately changes NOTHING in
      // here — the webhook keys off plan, and the amount fallback it drops to
      // when plan is missing is the thing that had to be made currency-aware,
      // not this.
      metadata: {
        uid: user.uid,
        plan: planId,
        custom_fields: [
          { display_name: 'Plan', variable_name: 'plan', value: planId },
          { display_name: 'Account', variable_name: 'uid', value: user.uid },
        ],
      },
      onSuccess: function (transaction) {
        // Client-side only. Grants nothing — see the note at the top of this file.
        var ref = (transaction && (transaction.reference || transaction.trxref)) || reference;
        confirmUpgrade(planId, user, beforePromise, ref, cur);
      },
      onCancel: function () {
        // Closing the Paystack window is not a failure and not a payment. Say
        // nothing and leave the page as it was.
      },
    }).catch(function (e) {
      console.warn('[Checkout] v2 checkout failed:', e && e.message);
      show('Could not open checkout',
           'We could not start Paystack checkout just now. Nothing was charged — please ' +
           'try again in a moment.',
           [{ label: 'Close', primary: true, onClick: hide }]);
    });
  }

  // The pre-checkout.checkout() gates — sign-in, email present, key configured,
  // script loaded — shared by both paths so they give the exact same messages
  // either way. Returns null (and has already shown whatever message applies)
  // if checkout should not proceed.
  function gate(user, key, Pop) {
    if (!user) {
      if (typeof window.showLogin === 'function') { window.showLogin('Sign in to upgrade'); return null; }
      return 'redirect';
    }
    if (!user.email) {
      show('We need your email', 'Your account has no email address on it, and Paystack ' +
           'requires one to send a receipt. Add one in My Studio and try again.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return null;
    }
    if (!key) {
      show('Payments coming online shortly',
           'Card payment is not switched on yet. Nothing was charged. Please check back soon.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return null;
    }
    if (!Pop) {
      show('Could not open checkout',
           'We could not reach Paystack just now. Nothing was charged — please check your ' +
           'connection and try again.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return null;
    }
    return 'ok';
  }

  // ── Entry point ─────────────────────────────────────────────────────────────
  // Two paths, same outcome. The fast path is the one that matters: by the time
  // a real click happens, prewarm() (called at page load, see wire() below) has
  // almost always already resolved user/key/Pop, so this branch calls
  // checkout() with NO await between the click and opening it — preserving the
  // browser's "this came from a real tap" state that Apple Pay and payment
  // popups require. The slow path below is only a fallback for a click that
  // somehow lands before prewarm finishes (a very fast click right after page
  // load, or a first-ever click before this script warmed anything).
  window.avStartCheckout = function (planId) {
    var plan = PLANS[planId];
    if (!plan) { console.error('[Checkout] unknown plan', planId); return; }

    if (cachedUser && cachedKey && cachedPop) {
      var g = gate(cachedUser, cachedKey, cachedPop);
      if (g === 'redirect') { window.location.href = 'studio.html?upgrade=' + encodeURIComponent(planId); return; }
      if (g !== 'ok') return;
      openCheckout(planId, plan, cachedUser, cachedKey, cachedPop);
      return;
    }

    slowStartCheckout(planId, plan);
  };

  async function slowStartCheckout(planId, plan) {
    var user = await currentUser();
    var key = await publicKey();
    var Pop = null;
    try { Pop = await paystackInline(); } catch (e) { Pop = null; }

    var g = gate(user, key, Pop);
    if (g === 'redirect') { window.location.href = 'studio.html?upgrade=' + encodeURIComponent(planId); return; }
    if (g !== 'ok') return;

    openCheckout(planId, plan, user, key, Pop);
  }

  // ── Donations ────────────────────────────────────────────────────────────────
  // A donation is NOT a plan purchase: it is not in PLANS, it grants nothing
  // (no credits, no tier, no tool unlock), and it works for a signed-in OR a
  // fully anonymous visitor. The one thing Paystack always requires is an
  // email — support.html supplies its own inline input for anyone who isn't
  // signed in and passes the value in here; a signed-in user's own email
  // always wins over it.
  //
  // metadata.donation = true (mirrored in metadata.plan = 'donation') is the
  // convention /webhooks/paystack (app.py) checks BEFORE it ever looks at a
  // real plan id, so this money is routed to credits.record_donation() and
  // never anywhere near apply_upgrade().
  function openDonation(amountUsdCents, email, user, key, Pop) {
    var donorEmail = (user && user.email) || (email || '').trim();
    if (!donorEmail) {
      show('We need your email', 'Paystack requires an email address to send a receipt. ' +
           'Enter one below and try again.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return;
    }
    if (!key) {
      show('Payments coming online shortly',
           'Card payment is not switched on yet. Nothing was charged. Please check back soon.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return;
    }
    if (!Pop) {
      show('Could not open checkout',
           'We could not reach Paystack just now. Nothing was charged — please check your ' +
           'connection and try again.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return;
    }

    var cur = currency();
    var kesAmount = Math.round((amountUsdCents / 100) * USD_TO_KES_RATE) * 100;
    var amount = cur === 'KES' ? kesAmount : amountUsdCents;

    // Same reference shape as avStartCheckout's — Paystack accepts only
    // alphanumerics and - . = in a reference.
    var reference = 'av-donate-' + Date.now() + '-' +
                    Math.random().toString(36).replace(/[^a-z0-9]/g, '').slice(0, 6);

    var metadata = {
      donation: true,
      plan: 'donation',
      amount: amountUsdCents,
      currency: cur,
      custom_fields: [
        { display_name: 'Donation', variable_name: 'donation', value: 'true' },
      ],
    };
    if (user && user.uid) metadata.uid = user.uid;
    if (user && user.email) metadata.email = user.email;

    return new Pop().checkout({
      key: key,
      email: donorEmail,
      amount: amount,
      currency: cur,
      ref: reference,
      metadata: metadata,
      onSuccess: function () {
        // Nothing to confirm server-side — a donation grants no entitlement to
        // poll for, unlike confirmUpgrade() above. Say thanks immediately.
        show('Thank you!',
             'Your support helps grow Africa’s tech infrastructure. We appreciate it.',
             [{ label: 'Close', primary: true, onClick: hide }]);
      },
      onCancel: function () {
        // Closing the Paystack window is not a failure and not a donation.
      },
    }).catch(function (e) {
      console.warn('[Donate] checkout failed:', e && e.message);
      show('Could not open checkout',
           'We could not start Paystack checkout just now. Nothing was charged — please ' +
           'try again in a moment.',
           [{ label: 'Close', primary: true, onClick: hide }]);
    });
  }

  // Same two-path shape as avStartCheckout above, and for the same reason:
  // the fast path calls .checkout() with ZERO awaits between the click and
  // opening it, so a real user gesture is still live when Apple Pay needs it.
  // Unlike avStartCheckout's gate(), a missing cachedUser does not block this
  // path — an anonymous donor is a normal case, not a fallback.
  window.avStartDonation = function (amountUsdCents, email) {
    amountUsdCents = parseInt(amountUsdCents, 10) || 0;
    if (amountUsdCents <= 0) { console.error('[Donate] bad amount', amountUsdCents); return; }

    if (cachedKey && cachedPop) {
      openDonation(amountUsdCents, email, cachedUser, cachedKey, cachedPop);
      return;
    }
    slowStartDonation(amountUsdCents, email);
  };

  async function slowStartDonation(amountUsdCents, email) {
    var user = await currentUser().catch(function () { return null; });
    var key = await publicKey();
    var Pop = null;
    try { Pop = await paystackInline(); } catch (e) { Pop = null; }
    openDonation(amountUsdCents, email, user, key, Pop);
  }

  // ── Fallback for the shared limit gate ──────────────────────────────────────
  // limits.js ends a blocked action with `if (window.showUpgradeModal)
  // showUpgradeModal(action)`. Only aieditor.html, edit.html and photo.html ever
  // defined that function, so on compress.html, graphics.html, images.html and
  // studio-editor.html hitting a limit did nothing at all — the tool simply
  // stopped, with no explanation and no way to pay. This gives those pages the
  // missing half. Pages with their own richer modal keep it: this only fills a gap.
  if (typeof window.showUpgradeModal !== 'function') {
    window.showUpgradeModal = function (reason) {
      var why = {
        video_compress: 'You have used your free compressions for this month.',
        image_brand: 'You have used your free brand images for this month.',
        image_motion: 'You have used your free motion images for this month.',
        studio_editor_export: 'You have used your free editor exports for this month.',
        editor_captions: 'You have used your free captions for this week.',
      }[reason] || 'You have reached the free limit for this tool.';
      var pro = price('pro_subscription');
      var one = price('tool_editor'); // every tool unlock is the same price
      show('Upgrade to keep going',
           why + ' Pro is ' + pro + ' a month and unlocks everything, or ' + one +
           ' unlocks this one tool.',
           [{ label: 'Go Pro — ' + pro + '/month', primary: true,
              onClick: function () { hide(); window.avStartCheckout('pro_subscription'); } },
            { label: 'See the $1 unlocks',
              onClick: function () { window.location.href = 'pricing.html#tools'; } },
            { label: 'Not now', onClick: hide }]);
    };
  }

  // ── The sitewide Upgrade button ─────────────────────────────────────────────
  // The markup is one <a class="av-upgrade"> in each page's nav; the styling is
  // defined once, here, because those navs are eleven separate <style> blocks and
  // the button has to look the same on all of them. Solid amber reads correctly on
  // both the light marketing bars and the dark editor bars, so it needs no theme
  // variant.
  function upgradeStyle() {
    if (document.getElementById('av-upgrade-style')) return;
    var s = document.createElement('style');
    s.id = 'av-upgrade-style';
    s.textContent =
      '.av-upgrade{display:inline-block;background:#E08A2E;color:#fff;' +
      'font-family:Syne,system-ui,sans-serif;font-weight:800;font-size:0.8rem;' +
      'padding:0.45rem 1rem;border-radius:9px;border:none;text-decoration:none;' +
      'white-space:nowrap;cursor:pointer;transition:background 0.18s;}' +
      '.av-upgrade:hover{background:#C4701E;color:#fff;}';
    document.head.appendChild(s);
  }

  // ── Wiring ──────────────────────────────────────────────────────────────────
  // Any element with data-av-plan="<plan id>" becomes a checkout button. Pages
  // carry no checkout logic of their own, and if the public key is not configured
  // the buttons say so instead of failing on click.
  function wire() {
    upgradeStyle();
    // Before the button wiring, and unconditionally: a page can show prices
    // without carrying a checkout button (the comparison table, for one).
    renderPrices();

    var els = document.querySelectorAll('[data-av-plan]');
    if (!els.length) return;

    // Only worth warming on pages that actually have a checkout button — see
    // the note above avStartCheckout's fast path for why this exists.
    prewarm();

    els.forEach(function (el) {
      if (el.dataset.avWired) return;
      el.dataset.avWired = '1';
      el.addEventListener('click', function (e) {
        e.preventDefault();
        if (el.getAttribute('aria-disabled') === 'true') return;
        window.avStartCheckout(el.getAttribute('data-av-plan'));
      });
    });

    publicKey().then(function (key) {
      if (key) return;
      els.forEach(function (el) {
        el.setAttribute('aria-disabled', 'true');
        el.style.opacity = '0.55';
        el.style.cursor = 'not-allowed';
        if (!el.dataset.avLabel) el.dataset.avLabel = el.textContent;
        el.textContent = 'Payments coming online shortly';
        el.title = 'Card payment is not switched on yet. Check back soon.';
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }
})();
