with open('index.html', 'r') as f:
    content = f.read()

# 1. Fix canvas size to 16:9
old_canvas_setup = '''  canvas.width = 1280;
  canvas.height = 720;'''
new_canvas_setup = '''  canvas.width = 1920;
  canvas.height = 1080;'''
content = content.replace(old_canvas_setup, new_canvas_setup, 1)

# 2. Fix transition to instant
content = content.replace(
    'const TRANSITION_DURATION = 250; // ms',
    'const TRANSITION_DURATION = 80; // ms - near instant'
)

# 3. Add aspect ratio selector to form
old_visual_style = '''          <div class="form-group">
            <label class="form-label">Video Style</label>
            <select id="video-visual-style" class="form-select">'''
new_visual_style = '''          <div class="form-group">
            <label class="form-label">Aspect Ratio</label>
            <select id="video-aspect-ratio" class="form-select">
              <option value="16:9">16:9 — Landscape (YouTube/Presentation)</option>
              <option value="9:16">9:16 — Portrait (TikTok/Reels)</option>
              <option value="1:1">1:1 — Square (Instagram)</option>
              <option value="4:3">4:3 — Classic</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Slide Theme</label>
            <select id="video-visual-style" class="form-select">'''
content = content.replace(old_visual_style, new_visual_style, 1)

# 4. Add Clean/Light slide themes
old_style_options = '''              <option value="slides">🖥 Slides (Default)</option>
              <option value="whiteboard">🖊 Whiteboard</option>
              <option value="cinematic">🎬 Cinematic</option>
              <option value="photobg">🌍 Photo Background</option>'''
new_style_options = '''              <option value="slides_light">☀️ Light (Clean White)</option>
              <option value="slides_dark">🌙 Dark (Professional)</option>
              <option value="slides_gold">✨ Gold (AfriVid Brand)</option>
              <option value="whiteboard">🖊 Whiteboard</option>
              <option value="cinematic">🎬 Cinematic</option>
              <option value="photobg">🌍 Photo Background</option>'''
content = content.replace(old_style_options, new_style_options, 1)

# 5. Rebuild the entire default slides drawScene
old_slides = '''  // Default slides style below
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const colors = COLORS[scene.background] || COLORS.navy;
  // Background
  ctx.fillStyle = colors.bg;
  ctx.fillRect(0, 0, W, H);
  // Grid pattern
  ctx.strokeStyle = 'rgba(245,166,35,0.04)';
  ctx.lineWidth = 1;
  for (let x = 0; x < W; x += 48) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
  for (let y = 0; y < H; y += 48) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
  // Glow
  const grd = ctx.createRadialGradient(W*0.8, H*0.2, 0, W*0.8, H*0.2, W*0.5);
  grd.addColorStop(0, 'rgba(245,166,35,0.06)');
  grd.addColorStop(1, 'transparent');
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, W, H);
  // YAN Logo area - top left
  ctx.fillStyle = 'rgba(245,166,35,0.1)';
  ctx.beginPath(); ctx.arc(60, 50, 24, 0, Math.PI*2); ctx.fill();
  ctx.strokeStyle = colors.accent;
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.arc(60, 50, 24, 0, Math.PI*2); ctx.stroke();
  ctx.fillStyle = colors.accent;
  ctx.font = 'bold 11px Syne, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('AfriVid', 60, 54);'''

new_slides = '''  // ── POWERPOINT-STYLE SLIDES ──
  const style2 = document.getElementById('video-visual-style') ?
    document.getElementById('video-visual-style').value : 'slides_light';
  drawPowerPointSlide(canvas, scene, progress, currentWord, style2);
  applyTransition(canvas);
  return;
}

function drawPowerPointSlide(canvas, scene, progress, currentWord, theme) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;

  // ── THEME COLORS ──
  const themes = {
    slides_light: { bg: '#FFFFFF', text: '#1a1a2e', accent: '#F5A623', accent2: '#74C69D', sub: '#555555', bar: '#F5A623' },
    slides_dark:  { bg: '#0D1117', text: '#F8F9FC', accent: '#F5A623', accent2: '#74C69D', sub: '#8B949E', bar: '#F5A623' },
    slides_gold:  { bg: '#050A14', text: '#F8F9FC', accent: '#F5A623', accent2: '#74C69D', sub: '#9BA8C0', bar: '#F5A623' },
    slides:       { bg: '#FFFFFF', text: '#1a1a2e', accent: '#F5A623', accent2: '#74C69D', sub: '#555555', bar: '#F5A623' }
  };
  const t = themes[theme] || themes.slides_light;

  // Background
  ctx.fillStyle = t.bg;
  ctx.fillRect(0, 0, W, H);

  // Subtle texture for light theme
  if (theme === 'slides_light' || theme === 'slides') {
    ctx.fillStyle = 'rgba(245,166,35,0.02)';
    for (let x = 0; x < W; x += 60) {
      for (let y = 0; y < H; y += 60) {
        ctx.fillRect(x, y, 1, 1);
      }
    }
  }

  // ── TOP BAR ──
  ctx.fillStyle = t.accent;
  ctx.fillRect(0, 0, W, 8);

  // ── LOGO TOP LEFT ──
  ctx.fillStyle = t.accent;
  ctx.font = `bold ${H*0.03}px Syne, sans-serif`;
  ctx.textAlign = 'left';
  ctx.fillText('AfriVid', W*0.04, H*0.065);
  ctx.fillStyle = theme === 'slides_light' || theme === 'slides' ? '#333' : t.sub;
  ctx.font = `${H*0.018}px Space Mono, monospace`;
  ctx.fillText('STUDIO', W*0.04 + ctx.measureText('AfriVid').width + 8, H*0.065);

  // ── SCENE NUMBER TOP RIGHT ──
  ctx.fillStyle = theme === 'slides_light' || theme === 'slides' ? 'rgba(0,0,0,0.12)' : 'rgba(255,255,255,0.1)';
  ctx.beginPath();
  ctx.roundRect(W*0.88, H*0.03, W*0.08, H*0.06, 8);
  ctx.fill();
  ctx.fillStyle = t.accent;
  ctx.font = `bold ${H*0.025}px Space Mono, monospace`;
  ctx.textAlign = 'center';
  ctx.fillText(`${scene.sceneNumber || 1}`, W*0.92, H*0.07);

  // ── ACCENT LINE LEFT ──
  ctx.fillStyle = t.accent;
  ctx.fillRect(W*0.04, H*0.15, 6, H*0.7);

  // ── MAIN TITLE ──
  const titleSize = H * 0.072;
  ctx.fillStyle = t.text;
  ctx.font = `800 ${titleSize}px Syne, sans-serif`;
  ctx.textAlign = 'left';
  
  // Wrap title
  const titleWords = (scene.slideTitle || '').split(' ');
  let titleLine = '';
  let titleY = H * 0.28;
  const titleX = W * 0.08;
  const maxTitleW = W * 0.85;
  
  titleWords.forEach((word, i) => {
    const test = titleLine + word + ' ';
    if (ctx.measureText(test).width > maxTitleW && titleLine) {
      ctx.fillText(titleLine.trim(), titleX, titleY);
      titleLine = word + ' ';
      titleY += titleSize * 1.2;
    } else {
      titleLine = test;
    }
    if (i === titleWords.length - 1) ctx.fillText(titleLine.trim(), titleX, titleY);
  });

  // ── SUBTITLE ──
  const subSize = H * 0.035;
  ctx.fillStyle = t.accent2;
  ctx.font = `600 ${subSize}px Syne, sans-serif`;
  ctx.fillText(scene.slideSubtitle || '', W * 0.08, titleY + titleSize * 1.4);

  // ── DIVIDER LINE ──
  ctx.fillStyle = theme === 'slides_light' || theme === 'slides' ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.08)';
  ctx.fillRect(W * 0.08, titleY + titleSize * 1.7, W * 0.88, 1);

  // ── BULLET POINTS (PowerPoint style - appear as voice speaks) ──
  if (scene.voiceover) {
    const sentences = scene.voiceover
      .split(/(?<=[.!?])\s+/)
      .filter(s => s.trim().length > 0)
      .slice(0, 5);

    const totalWords = scene.voiceover.split(' ').length;
    const wordsPerSentence = totalWords / sentences.length;
    const currentSentence = currentWord >= 0 ? Math.floor(currentWord / wordsPerSentence) : -1;

    const bulletY = titleY + titleSize * 2.2;
    const lineH = H * 0.082;
    const bulletSize = H * 0.028;

    sentences.forEach((sentence, idx) => {
      if (idx > currentSentence && currentWord >= 0) return; // Only show spoken sentences

      const y = bulletY + idx * lineH;
      const isActive = idx === currentSentence;
      const alpha = isActive ? 1 : 0.6;

      // Bullet dot
      ctx.globalAlpha = alpha;
      ctx.fillStyle = isActive ? t.accent : t.accent2;
      ctx.beginPath();
      ctx.arc(W * 0.08 + 8, y - 6, isActive ? 7 : 5, 0, Math.PI * 2);
      ctx.fill();

      // Highlight bar for active sentence
      if (isActive) {
        ctx.fillStyle = theme === 'slides_light' || theme === 'slides' ?
          'rgba(245,166,35,0.08)' : 'rgba(245,166,35,0.06)';
        ctx.fillRect(W * 0.075, y - bulletSize - 4, W * 0.88, bulletSize + 12);
      }

      // Sentence text
      ctx.fillStyle = isActive ? t.text : t.sub;
      ctx.font = `${isActive ? '600' : '400'} ${isActive ? bulletSize * 1.05 : bulletSize}px Syne, sans-serif`;
      ctx.textAlign = 'left';
      ctx.globalAlpha = alpha;

      // Wrap long sentences
      const bWords = sentence.trim().split(' ');
      let bLine = '';
      let bY = y;
      const bX = W * 0.095;
      const maxBW = W * 0.82;
      bWords.forEach((w, wi) => {
        const test = bLine + w + ' ';
        if (ctx.measureText(test).width > maxBW && bLine) {
          ctx.fillText(bLine.trim(), bX, bY);
          bLine = w + ' ';
          bY += bulletSize * 1.3;
        } else {
          bLine = test;
        }
        if (wi === bWords.length - 1) ctx.fillText(bLine.trim(), bX, bY);
      });

      ctx.globalAlpha = 1;
    });
  }

  // ── BOTTOM BAR ──
  ctx.fillStyle = t.accent;
  ctx.fillRect(0, H - 6, W, 6);

  // ── PROGRESS BAR ──
  ctx.fillStyle = theme === 'slides_light' || theme === 'slides' ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)';
  ctx.fillRect(0, H - 6, W, 6);
  ctx.fillStyle = t.accent;
  ctx.fillRect(0, H - 6, W * progress, 6);

  // Dummy return to close the if block
  if (false) {'''

content = content.replace(old_slides, new_slides, 1)

# 6. Update canvas setup to respect aspect ratio
old_canvas_init = '''  canvas.width = 1920;
  canvas.height = 1080;'''

new_canvas_init = '''  // Set canvas size based on aspect ratio
  const ar = document.getElementById('video-aspect-ratio')?.value || '16:9';
  if (ar === '16:9') { canvas.width = 1920; canvas.height = 1080; }
  else if (ar === '9:16') { canvas.width = 1080; canvas.height = 1920; }
  else if (ar === '1:1') { canvas.width = 1080; canvas.height = 1080; }
  else if (ar === '4:3') { canvas.width = 1440; canvas.height = 1080; }
  else { canvas.width = 1920; canvas.height = 1080; }'''

content = content.replace(old_canvas_init, new_canvas_init, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Slides engine rebuilt!")
