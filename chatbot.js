(function() {
  // Kept broad and current — direct feedback was that answers felt narrow/stale, since this
  // previously listed only 5 pages and one pricing line. Mirrors the real tool list on the
  // homepage and the real pricing/FAQ copy on pricing.html, so answers stay accurate as long as
  // this is updated alongside those pages rather than drifting independently.
  const AFRIVID_CONTEXT = `You are AfriVid Assistant for afrivid.studio — Africa's AI video creation platform, built for African creators, in 6 African languages. Be brief, warm, and helpful. Answer in 1-4 sentences unless genuinely more detail is needed.

TOOLS (each is its own page, linked from the homepage/nav):
- Video Creator (create.html): type a topic, AfriVid writes the script, generates voice, builds slides, exports a full MP4 in any of 6 African languages.
- AI Video Editor (aieditor.html): viral clips, highlight reels, silence removal, voice translation from an uploaded video.
- Manual Editor (edit.html): frame-by-frame manual video editing.
- Tutorial Maker (create.html, Tutorial Maker tab): explain any concept as narrated slides, or auto-record a live walkthrough of any website.
- Ad Maker (create.html, Ad Maker tab): turns a business description into a short branded video ad.
- Design Studio (design.html): AI-fill flyers, posters, banners, logos from a short description.
- Image Generator (images.html): branded photorealistic images for a business, or "living" images with subtle motion for a website.
- Photo Editor (photo.html): background removal, African flag overlays, AI photo enhancement.
- Slides Generator (create.html, Slides Generator tab): a topic into a full slide deck, downloadable as images or PDF.
- Video Compressor (compress.html): shrink a video's file size, balancing size vs. quality.
- Studio/My Studio (studio.html): your library of everything you've created.
- Developer API (api-docs.html): send a topic or script via API, get back a finished, unbranded MP4.
- Careers (careers.html): open roles at AfriVid — applications reviewed within 14 working days.

PRICING (pricing.html — always quote this, not a guess): Free plan is $0/month forever, no payment info required. Pro is $5/month with higher limits. Pro payment currently works via emailing to arrange payment (M-Pesa/MTN Mobile Money support is planned, not live yet). Upgrading never deletes existing work — hitting a free-plan limit just prompts an upgrade or a wait until next month's reset.

VIDEO PROMPT EXAMPLES: "Sunday sermon: [topic] — key points and call to action" | "Why African businesses need [product]" | "[Topic] explained for African students"
AI EDIT PROMPT EXAMPLES: "Keep best 60 seconds" | "Remove first 30 seconds" | "Make it TikTok ready" | "Remove silences"
PHOTO PROMPT EXAMPLES: "Make professional with bright lighting" | "Warm African sunset tone" | "Passport photo style"

Give exact example prompts in quotes when relevant. Always guide the user to the correct page/tool by name. If asked something you genuinely don't know about AfriVid, say so plainly and suggest contacting support (info@afrivid.studio) rather than guessing.`;

  // Create widget HTML
  const widget = document.createElement('div');
  widget.id = 'afrivid-chat-widget';
  widget.innerHTML = `
    <div id="acw-btn" title="Chat With AfriVid Online" onclick="toggleAfriVidChat()">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    </div>
    <div id="acw-box" style="display:none;">
      <div id="acw-header">
        <div style="display:flex;align-items:center;gap:0.6rem;">
          <div id="acw-avatar">A</div>
          <div>
            <div id="acw-title">Chat With AfriVid Online</div>
            <div id="acw-status"><span id="acw-dot"></span>Online</div>
          </div>
        </div>
        <button onclick="toggleAfriVidChat()" id="acw-close">✕</button>
      </div>
      <div id="acw-messages">
        <div class="acw-msg acw-bot">
          <div class="acw-bubble">Hi! I'm your AfriVid assistant. Ask me anything — how to create videos, use AI editor, translate content, or anything about AfriVid Studio. 🌍</div>
        </div>
      </div>
      <div id="acw-suggestions">
        <button onclick="acwSuggest('Give me a prompt to create a church video')">Church video</button>
        <button onclick="acwSuggest('Give me prompts for AI video editing')">AI edit prompts</button>
        <button onclick="acwSuggest('Give me a prompt to create a business video')">Business video</button>
        <button onclick="acwSuggest('How do I translate my video to Swahili?')">Translate video</button>
      </div>
      <div id="acw-input-area">
        <textarea id="acw-input" placeholder="Ask anything about AfriVid..." rows="1" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendAfriVidChat();}"></textarea>
        <button id="acw-send" onclick="sendAfriVidChat()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
    </div>
  `;

  // Styles
  const style = document.createElement('style');
  style.textContent = `
    #afrivid-chat-widget { position:fixed; bottom:2rem; left:2rem; z-index:9990; font-family:'Syne',sans-serif; }
    #acw-btn { width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg,#F5A623,#E8931A); color:#050A14; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 4px 20px rgba(245,166,35,0.4); transition:transform 0.2s; }
    #acw-btn:hover { transform:scale(1.08); }
    #acw-box { position:absolute; bottom:64px; left:0; width:340px; background:#0D1117; border:1px solid rgba(245,166,35,0.2); border-radius:16px; overflow:hidden; box-shadow:0 16px 48px rgba(0,0,0,0.6); display:flex; flex-direction:column; max-height:500px; }
    #acw-header { background:linear-gradient(135deg,rgba(245,166,35,0.1),rgba(245,166,35,0.05)); padding:0.85rem 1rem; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.06); }
    #acw-avatar { width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#F5A623,#E8931A); display:flex; align-items:center; justify-content:center; font-weight:900; font-size:1rem; color:#050A14; flex-shrink:0; }
    #acw-title { color:#fff; font-weight:800; font-size:0.85rem; }
    #acw-status { color:rgba(255,255,255,0.4); font-size:0.7rem; display:flex; align-items:center; gap:0.3rem; margin-top:0.1rem; }
    #acw-dot { width:6px; height:6px; border-radius:50%; background:#74C69D; display:inline-block; }
    #acw-close { background:none; border:none; color:rgba(255,255,255,0.3); cursor:pointer; font-size:1rem; padding:0.2rem; }
    #acw-messages { flex:1; overflow-y:auto; padding:1rem; display:flex; flex-direction:column; gap:0.75rem; min-height:200px; max-height:280px; }
    .acw-msg { display:flex; }
    .acw-bot { justify-content:flex-start; }
    .acw-user { justify-content:flex-end; }
    .acw-bubble { max-width:85%; padding:0.65rem 0.9rem; border-radius:12px; font-size:0.82rem; line-height:1.5; }
    .acw-bot .acw-bubble { background:rgba(255,255,255,0.06); color:#fff; border-radius:4px 12px 12px 12px; }
    .acw-user .acw-bubble { background:linear-gradient(135deg,#F5A623,#E8931A); color:#050A14; font-weight:700; border-radius:12px 4px 12px 12px; }
    .acw-typing .acw-bubble { color:rgba(255,255,255,0.4); font-style:italic; }
    #acw-suggestions { padding:0 1rem 0.75rem; display:flex; flex-wrap:wrap; gap:0.4rem; }
    #acw-suggestions button { background:rgba(245,166,35,0.08); border:1px solid rgba(245,166,35,0.2); color:#F5A623; padding:0.3rem 0.65rem; border-radius:20px; font-size:0.7rem; cursor:pointer; font-family:'Syne',sans-serif; font-weight:700; transition:all 0.2s; white-space:nowrap; }
    #acw-suggestions button:hover { background:rgba(245,166,35,0.15); }
    #acw-input-area { padding:0.75rem; border-top:1px solid rgba(255,255,255,0.06); display:flex; gap:0.5rem; align-items:flex-end; }
    #acw-input { flex:1; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:#fff; padding:0.6rem 0.75rem; border-radius:10px; font-family:'Syne',sans-serif; font-size:0.82rem; resize:none; outline:none; max-height:80px; line-height:1.4; }
    #acw-input:focus { border-color:rgba(245,166,35,0.3); }
    #acw-send { background:linear-gradient(135deg,#F5A623,#E8931A); border:none; color:#050A14; width:36px; height:36px; border-radius:10px; cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
    #acw-send:hover { opacity:0.9; }
    @media(max-width:400px) { #acw-box { width:300px; } }
  `;

  document.head.appendChild(style);
  document.addEventListener('DOMContentLoaded', () => document.body.appendChild(widget));

  let chatHistory = [];
  let isOpen = false;

  window.toggleAfriVidChat = function() {
    isOpen = !isOpen;
    const box = document.getElementById('acw-box');
    if (box) box.style.display = isOpen ? 'flex' : 'none';
    if (isOpen) document.getElementById('acw-input')?.focus();
  };

  window.acwSuggest = function(text) {
    document.getElementById('acw-input').value = text;
    document.getElementById('acw-suggestions').style.display = 'none';
    sendAfriVidChat();
  };

  // Quick local responses for lazy chat — matched against the WHOLE message (after stripping
  // punctuation), not a substring search. The old `.includes(w)` check fired on any message
  // that merely *contained* one of these words anywhere — "thanks for the tutorial maker prompts,
  // bye" or a real question ending in "...right?" could get hijacked into a canned "you're
  // welcome"/goodbye reply instead of an actual answer. Real feedback ("problems in answers")
  // traced directly to this. Exact/near-exact short-message matching only, so a genuine question
  // that happens to contain "hi" or "bye" as a substring of a longer word/sentence is never
  // intercepted.
  const LOCAL_RESPONSES = {
    greet: ['hello','hi','hey','hola','habari','jambo','bonjour','sawa','what up','sup','yo'],
    thanks: ['thanks','thank you','asante','merci','thx','ty','cheers','thanks!','thank you!'],
    bye: ['bye','goodbye','later','kwaheri','au revoir','ciao','bye!','goodbye!'],
    who: ['who are you','what are you','are you ai','are you human','who made you','are you a bot'],
  };

  function normalizeForLocalMatch(text) {
    return text.toLowerCase().replace(/[.,!?;:]+$/g, '').trim();
  }

  function matchesLocalResponse(normalized, phrases) {
    return phrases.includes(normalized);
  }

  window.sendAfriVidChat = async function() {
    const input = document.getElementById('acw-input');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    addMessage(msg, 'user');

    // Check for lazy/irrelevant chat first — exact match on the whole (punctuation-stripped)
    // message only, never a substring search, so a real question that happens to contain one
    // of these words doesn't get hijacked into a canned reply instead of an actual answer.
    const normalized = normalizeForLocalMatch(msg);

    if (matchesLocalResponse(normalized, LOCAL_RESPONSES.greet)) {
      addMessage("Hey! I'm your AfriVid assistant. What would you like to create or edit today? 🌍", 'bot');
      return;
    }
    if (matchesLocalResponse(normalized, LOCAL_RESPONSES.thanks)) {
      addMessage("You're welcome! Anything else I can help you with on AfriVid?", 'bot');
      return;
    }
    if (matchesLocalResponse(normalized, LOCAL_RESPONSES.bye)) {
      addMessage("Goodbye! Come back anytime you need help creating content. 🔥", 'bot');
      return;
    }
    if (matchesLocalResponse(normalized, LOCAL_RESPONSES.who)) {
      addMessage("I'm the AfriVid AI assistant — built to help African creators get the most out of AfriVid Studio. Ask me how to create videos, edit, translate or design! 🌍", 'bot');
      return;
    }
    if (matchesLocalResponse(normalized, ['how are you','how r you','how are u','hows it going','how do you do'])) {
      addMessage("I'm always ready to help! What would you like to create today on AfriVid? 🔥", 'bot');
      return;
    }
    if (matchesLocalResponse(normalized, ['what is afrivid','what is afrivid studio','tell me about afrivid'])) {
      addMessage("AfriVid Studio is Africa's first AI video creation platform! Create videos from text, edit with AI, translate to African languages, design graphics and more — all at afrivid.studio 🌍", 'bot');
      return;
    }
    if (normalized.length < 2) {
      addMessage("Please ask me something about AfriVid — like how to create a video or use the AI editor!", 'bot');
      return;
    }

    // No sign-in gate, no plan gate — the assistant answers anyone, signed in or not, on any
    // plan. It previously required a Pro account (even the error message was wrong: the code
    // actually allowed 'beta' plan too, but any Firestore hiccup silently fell back to blocking
    // everyone with a "upgrade to Pro" message that often didn't even match their real plan).
    chatHistory.push({role:'user', content: msg});

    // Show typing
    const typingId = addTyping();

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000);
      // Self-hosted via Workers AI (same infrastructure every other AI feature on the site
      // already uses) instead of a separate external worker on a different Cloudflare account —
      // that dependency had its own auth/uptime risk disconnected from everything else here.
      // This endpoint takes a plain {messages, max_tokens} shape with no separate top-level
      // `system` field, so the system prompt goes in as the first message instead.
      const res = await fetch('https://afrivid-tts.reaganayiecho.workers.dev/ai-generate', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        signal: controller.signal,
        body: JSON.stringify({
          max_tokens: 400,
          messages: [{role:'system', content: AFRIVID_CONTEXT}, ...chatHistory.slice(-6)]
        })
      });
      clearTimeout(timeout);
      const data = await res.json();
      const reply = data.content?.[0]?.text || 'Sorry, I could not process that. Please try again.';

      removeTyping(typingId);
      addMessage(reply, 'bot');
      chatHistory.push({role:'assistant', content: reply});

      // Keep history manageable
      if (chatHistory.length > 20) chatHistory = chatHistory.slice(-20);
      
    } catch(e) {
      removeTyping(typingId);
      const errMsg = e.name === 'AbortError' 
        ? 'Taking too long. Try a shorter question or check your connection.'
        : 'Connection error. Please check your internet and try again.';
      addMessage(errMsg, 'bot');
    }
  };

  function addMessage(text, type) {
    const msgs = document.getElementById('acw-messages');
    const div = document.createElement('div');
    div.className = `acw-msg acw-${type}`;
    div.innerHTML = `<div class="acw-bubble">${text.replace(/\n/g,'<br>')}</div>`;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  function addTyping() {
    const msgs = document.getElementById('acw-messages');
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.className = 'acw-msg acw-bot acw-typing';
    div.id = id;
    div.innerHTML = '<div class="acw-bubble">AfriVid is thinking...</div>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return id;
  }

  function removeTyping(id) {
    document.getElementById(id)?.remove();
  }
})();
