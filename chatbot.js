(function() {
  const AFRIVID_CONTEXT = `You are AfriVid Assistant for afrivid.studio - Africa's AI video platform. Be brief and helpful.

PAGES: create.html (make videos), aieditor.html (AI edit), edit.html (manual edit), photo.html (photos), design.html (graphics), studio.html (library), pricing.html (Free/Pro $5/month)

VIDEO PROMPTS: "Sunday sermon: [topic] — key points and call to action" | "Why African businesses need [product]" | "[Topic] explained for African students"

AI EDIT PROMPTS: "Keep best 60 seconds" | "Remove first 30 seconds" | "Make it TikTok ready" | "Remove silences"

PHOTO PROMPTS: "Make professional with bright lighting" | "Warm African sunset tone" | "Passport photo style"

Answer in 1-3 sentences. Give exact prompts in quotes. Guide to correct page.`;;

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

  window.sendAfriVidChat = async function() {
    const input = document.getElementById('acw-input');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    // Add user message
    addMessage(msg, 'user');
    chatHistory.push({role:'user', content: msg});

    // Show typing
    const typingId = addTyping();

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000);
      const res = await fetch('https://yan-ai-worker.youngafricansn.workers.dev', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        signal: controller.signal,
        body: JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 300,
          system: AFRIVID_CONTEXT,
          messages: chatHistory.slice(-6)
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
