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

  // Amounts are USD cents — the smallest unit, which is what Paystack expects and
  // what PAYSTACK_AMOUNT_PLANS in app.py maps back from if metadata is ever lost.
  // These must stay in step with apply_upgrade()'s plan ids in credits.py.
  var PLANS = {
    pro_subscription: { amount: 500, label: 'Pro — $5/month' },
    tool_compressor:  { amount: 100, label: 'Video Compressor — $1' },
    tool_graphics:    { amount: 100, label: 'Graphics and Images — $1' },
    tool_editor:      { amount: 100, label: 'Video Editor — $1' },
    tool_video:       { amount: 100, label: 'Video Creation — $1' },
    tool_api:         { amount: 100, label: 'Developer API — $1' },
  };
  window.AFRIVID_PLANS = PLANS;

  var POLL_INTERVAL_MS = 2000;
  var POLL_TIMEOUT_MS = 20000;

  // ── One-shot loaders ────────────────────────────────────────────────────────
  // Each of these caches its PROMISE, not its result, so two fast clicks share one
  // network request instead of racing two.
  var keyPromise = null;
  var inlinePromise = null;
  var authPromise = null;

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
  async function confirmUpgrade(plan, user, before, reference) {
    show('Payment received',
         'Confirming with our servers and upgrading your account. This takes a few seconds.',
         []);

    var deadline = Date.now() + POLL_TIMEOUT_MS;
    while (Date.now() < deadline) {
      await new Promise(function (r) { setTimeout(r, POLL_INTERVAL_MS); });
      var after = await entitlements(user);
      if (applied(plan, before, after)) {
        show('You are upgraded',
             (PLANS[plan] ? PLANS[plan].label + ' is active on your account.' : 'Your upgrade is active.') +
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

  // ── Entry point ─────────────────────────────────────────────────────────────
  window.avStartCheckout = async function (planId) {
    var plan = PLANS[planId];
    if (!plan) { console.error('[Checkout] unknown plan', planId); return; }

    var user = await currentUser();
    if (!user) {
      // Same gate every other paid action uses: sign in where the page knows how,
      // otherwise send them to the page that signs people in.
      if (typeof window.showLogin === 'function') { window.showLogin('Sign in to upgrade'); return; }
      window.location.href = 'studio.html?upgrade=' + encodeURIComponent(planId);
      return;
    }
    if (!user.email) {
      show('We need your email', 'Your account has no email address on it, and Paystack ' +
           'requires one to send a receipt. Add one in My Studio and try again.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return;
    }

    var key = await publicKey();
    if (!key) {
      show('Payments coming online shortly',
           'Card payment is not switched on yet. Nothing was charged. Please check back soon.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return;
    }

    var Pop;
    try { Pop = await paystackInline(); }
    catch (e) {
      show('Could not open checkout',
           'We could not reach Paystack just now. Nothing was charged — please check your ' +
           'connection and try again.',
           [{ label: 'Close', primary: true, onClick: hide }]);
      return;
    }

    // The "before" reading, taken while the user is still looking at the page, is
    // what confirmUpgrade() later compares against to know the webhook landed.
    var before = await entitlements(user);

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
    try {
      await new Pop().checkout({
        key: key,
        email: user.email,
        amount: plan.amount,
        currency: 'USD',
        ref: reference,
        // The ONLY thing tying this payment back to an account. app.py's webhook
        // reads uid and plan from here; without them the charge lands as "PAID BUT
        // UNAPPLIED" and needs a human.
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
          confirmUpgrade(planId, user, before, ref);
        },
        onCancel: function () {
          // Closing the Paystack window is not a failure and not a payment. Say
          // nothing and leave the page as it was.
        },
      });
    } catch (e) {
      console.warn('[Checkout] v2 checkout failed:', e && e.message);
      show('Could not open checkout',
           'We could not start Paystack checkout just now. Nothing was charged — please ' +
           'try again in a moment.',
           [{ label: 'Close', primary: true, onClick: hide }]);
    }
  };

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
      show('Upgrade to keep going',
           why + ' Pro is $5 a month and unlocks everything, or $1 unlocks this one tool.',
           [{ label: 'Go Pro — $5/month', primary: true,
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

    var els = document.querySelectorAll('[data-av-plan]');
    if (!els.length) return;

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
