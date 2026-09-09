/* AfriVid — branded download filenames (client side).
 *
 * The one place the browser decides what a saved file is called. It mirrors
 * branded_filename() in the backend's app.py, so a video named on the server and
 * a design named here come out looking like the same product:
 *
 *     AfriVid - <up to 6 real words from what the user made> - <tool>.<ext>
 *
 * Used only where the page itself produces the bytes (a canvas export, or a blob
 * it already fetched). Anything the user pulls straight off the R2 bucket is
 * named by the Content-Disposition stored on the object instead — a cross-origin
 * <a download="..."> is silently ignored by every browser, so the page genuinely
 * cannot name those files.
 */
(function () {
  'use strict';

  // Illegal in a Windows filename; \ and / would split a path anywhere.
  var ILLEGAL = /[<>:"/\\|?*\x00-\x1f]/g;

  // Cutting a topic at exactly N words regularly lands on a dangling connective
  // — "How to start a business in Kenya" -> "...a business in". Trailing words
  // from this set are dropped after the cut so the name ends on something real.
  var TRAILING_STOPWORDS = {
    a: 1, an: 1, and: 1, are: 1, as: 1, at: 1, be: 1, but: 1, by: 1, for: 1,
    from: 1, how: 1, 'in': 1, into: 1, is: 1, it: 1, of: 1, on: 1, or: 1,
    over: 1, per: 1, so: 1, that: 1, the: 1, their: 1, then: 1, 'this': 1,
    to: 1, up: 1, via: 1, was: 1, were: 1, why: 1, 'with': 1, without: 1,
    your: 1
  };

  function words(text, maxWords, maxChars) {
    maxWords = maxWords || 6;
    maxChars = maxChars || 52;
    if (text === null || text === undefined) return '';
    var s = String(text);
    if (s.normalize) s = s.normalize('NFKC');
    // Keep letters/digits/space/apostrophe/hyphen. Everything else — emoji,
    // punctuation, newlines, path separators, the Windows-illegal set — is a
    // space. \p{L}\p{N} needs the u flag; fall back for very old engines.
    try {
      s = s.replace(/[^\p{L}\p{N}\s'-]/gu, ' ');
    } catch (e) {
      s = s.replace(/[^A-Za-z0-9\s'-]/g, ' ');
    }
    s = s.replace(/\s+/g, ' ').trim();
    if (!s) return '';

    var list = s.split(' ').filter(function (w) { return w.replace(/^['-]+|['-]+$/g, ''); });
    // "AfriVid - AfriVid Promo - Ad" reads like a bug. If the user's own text
    // already opens with the brand, drop it; the template re-adds it.
    while (list.length && /^afrivids?$/i.test(list[0].replace(/^['-]+|['-]+$/g, ''))) list.shift();
    if (!list.length) return '';

    var kept = list.slice(0, maxWords);
    // Only trim a dangling connective when the cut actually dropped something —
    // a title the user deliberately ended that way ("Before and After") keeps it.
    if (list.length > kept.length) {
      while (kept.length > 1 &&
             TRAILING_STOPWORDS[kept[kept.length - 1].replace(/^['-]+|['-]+$/g, '').toLowerCase()]) {
        kept.pop();
      }
    }
    var out = kept.join(' ');
    if (out.length > maxChars) {
      var head = out.slice(0, maxChars).replace(/\s+\S*$/, '');
      out = head || out.slice(0, maxChars);
    }
    out = out.replace(/^[\s\-']+|[\s\-']+$/g, '');
    // ALL-CAPS input (a pasted headline) is shouty as a filename; anything with
    // real mixed case is the user's own styling and is left alone.
    if (out && out === out.toUpperCase() && /[A-Z]/.test(out)) {
      out = out.toLowerCase().replace(/\b[a-z]/g, function (c) { return c.toUpperCase(); });
    }
    return out;
  }

  function shortDate() {
    var d = new Date();
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return ('0' + d.getDate()).slice(-2) + ' ' + months[d.getMonth()] + ' ' + d.getFullYear();
  }

  /**
   * afrividFilename('How to start a business in Kenya', 'Tutorial', 'mp4')
   *   -> 'AfriVid - How to start a business - Tutorial.mp4'
   * afrividFilename('', 'Studio Export', 'mp4')
   *   -> 'AfriVid Studio Export - 10 Sep 2026.mp4'
   */
  function afrividFilename(subject, kind, ext) {
    var subj = words(subject, 6, 52);
    var k = words(kind, 3, 24);

    ext = String(ext == null ? '' : ext).replace(/^\./, '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 5) || 'mp4';

    var stem = subj
      ? 'AfriVid - ' + subj + (k ? ' - ' + k : '')
      : (k ? 'AfriVid ' + k : 'AfriVid Export') + ' - ' + shortDate();

    stem = stem.replace(ILLEGAL, '').replace(/\s+/g, ' ').replace(/^[\s.]+|[\s.]+$/g, '');
    // Every stem starts with "AfriVid", so a Windows reserved device name
    // (CON, NUL, LPT1...) can never come out of here.
    return (stem.slice(0, 110).replace(/^[\s.]+|[\s.]+$/g, '') || 'AfriVid Export') + '.' + ext;
  }

  window.afrividFilename = afrividFilename;
})();
