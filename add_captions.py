with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add captions section to video enhancer
old_enhance_controls = '''      <!-- ACTIONS -->
      <div class="card">
        <div class="card-title"><div class="card-title-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        </div>Export</div>'''

new_enhance_controls = '''      <!-- CAPTIONS -->
      <div class="card" style="margin-bottom:1rem;">
        <div class="card-title">
          <div class="card-title-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="15" rx="2"/><path d="M17 2l-5 5-5-5"/></svg>
          </div>
          Captions & Subtitles
        </div>

        <!-- Caption style picker -->
        <div style="margin-bottom:1rem;">
          <label class="form-label">Caption Style</label>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-bottom:0.75rem;">
            <div onclick="setCaptionStyle('classic')" id="cap-classic" style="padding:0.75rem;border-radius:8px;background:var(--navy3);border:2px solid var(--gold);cursor:pointer;text-align:center;">
              <div style="font-size:0.82rem;font-weight:700;color:#fff;margin-bottom:4px;">Classic</div>
              <div style="font-size:0.65rem;background:rgba(0,0,0,0.7);color:#fff;padding:2px 6px;border-radius:4px;display:inline-block;">White text, dark bg</div>
            </div>
            <div onclick="setCaptionStyle('bold')" id="cap-bold" style="padding:0.75rem;border-radius:8px;background:var(--navy3);border:2px solid transparent;cursor:pointer;text-align:center;">
              <div style="font-size:0.82rem;font-weight:700;color:#fff;margin-bottom:4px;">Bold</div>
              <div style="font-size:0.65rem;background:#F5A623;color:#000;padding:2px 6px;border-radius:4px;font-weight:700;display:inline-block;">Gold highlight</div>
            </div>
            <div onclick="setCaptionStyle('minimal')" id="cap-minimal" style="padding:0.75rem;border-radius:8px;background:var(--navy3);border:2px solid transparent;cursor:pointer;text-align:center;">
              <div style="font-size:0.82rem;font-weight:700;color:#fff;margin-bottom:4px;">Minimal</div>
              <div style="font-size:0.65rem;color:#fff;padding:2px 6px;border-radius:4px;display:inline-block;text-shadow:1px 1px 3px #000;">Clean white</div>
            </div>
            <div onclick="setCaptionStyle('tiktok')" id="cap-tiktok" style="padding:0.75rem;border-radius:8px;background:var(--navy3);border:2px solid transparent;cursor:pointer;text-align:center;">
              <div style="font-size:0.82rem;font-weight:700;color:#fff;margin-bottom:4px;">TikTok</div>
              <div style="font-size:0.65rem;background:#fff;color:#000;padding:2px 6px;border-radius:4px;font-weight:900;display:inline-block;">BIG & BOLD</div>
            </div>
          </div>
        </div>

        <!-- Caption position -->
        <div style="margin-bottom:1rem;">
          <label class="form-label">Position</label>
          <select id="caption-position" class="form-select">
            <option value="bottom">Bottom (Standard)</option>
            <option value="top">Top</option>
            <option value="middle">Middle</option>
          </select>
        </div>

        <!-- Caption language -->
        <div style="margin-bottom:1rem;">
          <label class="form-label">Language</label>
          <select id="caption-language" class="form-select">
            <option value="en">English</option>
            <option value="sw">Swahili</option>
            <option value="fr">French</option>
            <option value="ar">Arabic</option>
            <option value="pt">Portuguese</option>
            <option value="ha">Hausa</option>
            <option value="yo">Yoruba</option>
            <option value="zu">Zulu</option>
          </select>
        </div>

        <button onclick="generateCaptions()" id="btn-generate-captions" class="btn btn-gold" style="width:100%;margin-bottom:0.5rem;">
          [mic] Generate Auto-Captions (AI)
        </button>
        <button onclick="addManualCaption()" class="btn btn-outline" style="width:100%;font-size:0.82rem;">
          + Add Caption Manually
        </button>

        <!-- Caption list -->
        <div id="caption-list" style="display:none;margin-top:1rem;">
          <div style="font-size:0.75rem;color:var(--gold);font-family:var(--font-mono);margin-bottom:0.5rem;">CAPTIONS</div>
          <div id="caption-items"></div>
          <button onclick="clearCaptions()" style="font-size:0.72rem;color:var(--red);background:none;border:none;cursor:pointer;margin-top:0.5rem;font-family:var(--font-mono);">[del] Clear all captions</button>
        </div>

        <div id="caption-status" style="font-size:0.75rem;font-family:var(--font-mono);color:var(--gold);margin-top:0.5rem;"></div>
      </div>

      <!-- ACTIONS -->
      <div class="card">
        <div class="card-title"><div class="card-title-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        </div>Export</div>'''

content = content.replace(old_enhance_controls, new_enhance_controls, 1)

# Add caption JS functions
old_reset = 'function _resetEnhancer() {'
new_reset = '''// ── CAPTIONS SYSTEM ──
let captions = []; // [{start, end, text}]
let currentCaptionStyle = 'classic';

const captionStyles = {
  classic: {
    font: '600 18px Syne, sans-serif',
    color: '#ffffff',
    bg: 'rgba(0,0,0,0.75)',
    padding: 8,
    radius: 4
  },
  bold: {
    font: '800 22px Syne, sans-serif',
    color: '#050A14',
    bg: '#F5A623',
    padding: 10,
    radius: 6
  },
  minimal: {
    font: '600 18px Syne, sans-serif',
    color: '#ffffff',
    bg: 'transparent',
    shadow: true,
    padding: 4,
    radius: 0
  },
  tiktok: {
    font: '900 28px Syne, sans-serif',
    color: '#000000',
    bg: '#ffffff',
    padding: 12,
    radius: 4
  }
};

function setCaptionStyle(style) {
  currentCaptionStyle = style;
  ['classic','bold','minimal','tiktok'].forEach(s => {
    const el = document.getElementById('cap-'+s);
    if (el) el.style.borderColor = s === style ? 'var(--gold)' : 'transparent';
  });
}

async function generateCaptions() {
  const video = document.getElementById('original-video');
  if (!video || !video.src) { alert('Please upload a video first'); return; }

  const btn = document.getElementById('btn-generate-captions');
  const status = document.getElementById('caption-status');
  btn.textContent = '[..] Transcribing...';
  btn.disabled = true;
  status.textContent = '[mic] Sending audio to AI...';

  try {
    // Extract audio from video as blob
    const response = await fetch(video.src);
    const blob = await response.blob();

    const formData = new ArrayBuffer(await blob.arrayBuffer());
    
    const lang = document.getElementById('caption-language').value;
    
    const res = await fetch('https://afrivid-tts.mathsai666.workers.dev/transcribe', {
      method: 'POST',
      headers: { 'Content-Type': 'audio/webm' },
      body: formData
    });

    if (!res.ok) throw new Error('Transcription failed');
    const data = await res.json();
    
    if (!data.text) throw new Error('No text returned');

    status.textContent = '[ok] Transcribed! Creating captions...';

    // Split into caption segments (roughly every 5 words)
    const words = data.text.split(' ').filter(w => w.trim());
    const duration = video.duration || 60;
    const wordsPerSecond = words.length / duration;
    const wordsPerCaption = Math.max(4, Math.min(8, Math.round(wordsPerSecond * 3)));

    captions = [];
    for (let i = 0; i < words.length; i += wordsPerCaption) {
      const chunk = words.slice(i, i + wordsPerCaption).join(' ');
      const start = (i / words.length) * duration;
      const end = Math.min(((i + wordsPerCaption) / words.length) * duration, duration);
      captions.push({ start: parseFloat(start.toFixed(2)), end: parseFloat(end.toFixed(2)), text: chunk });
    }

    renderCaptionList();
    status.textContent = `[ok] ${captions.length} captions generated!`;
    status.style.color = '#74C69D';

  } catch(e) {
    status.textContent = '[x] Failed: ' + e.message;
    status.style.color = 'var(--red)';
  }

  btn.textContent = '[mic] Generate Auto-Captions (AI)';
  btn.disabled = false;
}

function addManualCaption() {
  const video = document.getElementById('original-video');
  const currentTime = video ? video.currentTime : 0;
  const text = prompt('Enter caption text:');
  if (!text) return;
  captions.push({
    start: parseFloat(currentTime.toFixed(2)),
    end: parseFloat((currentTime + 3).toFixed(2)),
    text: text.trim()
  });
  captions.sort((a,b) => a.start - b.start);
  renderCaptionList();
}

function renderCaptionList() {
  const list = document.getElementById('caption-items');
  const container = document.getElementById('caption-list');
  if (!list || !captions.length) return;
  container.style.display = 'block';
  list.innerHTML = captions.map((c,i) => `
    <div style="display:flex;gap:0.5rem;align-items:center;padding:0.5rem;background:var(--navy3);border-radius:6px;margin-bottom:0.35rem;font-size:0.75rem;">
      <span style="color:var(--gold);font-family:var(--font-mono);min-width:50px;">${formatTime(c.start)}</span>
      <span style="flex:1;color:var(--white);">${c.text}</span>
      <button onclick="deleteCaption(${i})" style="background:none;border:none;color:var(--red);cursor:pointer;font-size:0.8rem;">[x]</button>
    </div>
  `).join('');
}

function formatTime(s) {
  const m = Math.floor(s/60);
  const sec = Math.floor(s%60);
  return `${m}:${sec.toString().padStart(2,'0')}`;
}

function deleteCaption(idx) {
  captions.splice(idx, 1);
  renderCaptionList();
}

function clearCaptions() {
  captions = [];
  document.getElementById('caption-list').style.display = 'none';
  document.getElementById('caption-status').textContent = '';
}

function drawCaptionsOnFrame(ctx, W, H, currentTime) {
  const caption = captions.find(c => currentTime >= c.start && currentTime <= c.end);
  if (!caption) return;

  const style = captionStyles[currentCaptionStyle] || captionStyles.classic;
  const position = document.getElementById('caption-position')?.value || 'bottom';

  ctx.font = style.font;
  ctx.textAlign = 'center';

  const maxWidth = W * 0.85;
  const words = caption.text.split(' ');
  let lines = [];
  let line = '';
  words.forEach(word => {
    const test = line + word + ' ';
    if (ctx.measureText(test).width > maxWidth && line) {
      lines.push(line.trim());
      line = word + ' ';
    } else { line = test; }
  });
  if (line) lines.push(line.trim());

  const lineH = parseInt(style.font) * 1.4;
  const totalH = lines.length * lineH + style.padding * 2;
  const x = W / 2;
  let y = position === 'top' ? 40 : position === 'middle' ? H/2 - totalH/2 : H - totalH - 30;

  // Background
  if (style.bg !== 'transparent') {
    const maxLineW = Math.max(...lines.map(l => ctx.measureText(l).width));
    ctx.fillStyle = style.bg;
    ctx.beginPath();
    const bx = x - maxLineW/2 - style.padding;
    const by = y - style.padding;
    const bw = maxLineW + style.padding * 2;
    const bh = totalH;
    if (ctx.roundRect) ctx.roundRect(bx, by, bw, bh, style.radius);
    else ctx.rect(bx, by, bw, bh);
    ctx.fill();
  }

  // Text shadow for minimal style
  if (style.shadow) {
    ctx.shadowColor = 'rgba(0,0,0,0.8)';
    ctx.shadowBlur = 4;
  }

  ctx.fillStyle = style.color;
  lines.forEach((l, i) => {
    ctx.fillText(l, x, y + style.padding + (i + 0.8) * lineH);
  });
  ctx.shadowBlur = 0;
}

function _resetEnhancer() {'''

content = content.replace(old_reset, new_reset, 1)

# Hook captions into the enhance render loop
old_draw_frame = '''    ctx.drawImage(video, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);'''
new_draw_frame = '''    ctx.drawImage(video, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);
    // Draw captions
    if (captions && captions.length > 0) {
      drawCaptionsOnFrame(ctx, canvas.width, canvas.height, video.currentTime);
    }'''
content = content.replace(old_draw_frame, new_draw_frame, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Captions system added!")
