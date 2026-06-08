with open('index.html', 'r') as f:
    content = f.read()

old_powerpoint = '''function drawPowerPointSlide(canvas, scene, progress, currentWord, theme) {
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

new_powerpoint = '''function drawPowerPointSlide(canvas, scene, progress, currentWord, theme) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;

  // ── SYNTHESIA-STYLE THEMES ──
  const themes = {
    slides_light: { bg: '#F8F9FC', text: '#0D1117', accent: '#F5A623', accent2: '#2D8A5E', sub: '#444444' },
    slides_dark:  { bg: '#0D1117', text: '#FFFFFF', accent: '#F5A623', accent2: '#74C69D', sub: '#8B949E' },
    slides_gold:  { bg: '#050A14', text: '#FFFFFF', accent: '#F5A623', accent2: '#74C69D', sub: '#9BA8C0' },
    slides:       { bg: '#F8F9FC', text: '#0D1117', accent: '#F5A623', accent2: '#2D8A5E', sub: '#444444' }
  };
  const t = themes[theme] || themes.slides_light;
  const isLight = theme === 'slides_light' || theme === 'slides';

  // ── FULL SCREEN BACKGROUND ──
  ctx.fillStyle = t.bg;
  ctx.fillRect(0, 0, W, H);

  // Subtle gradient overlay
  const grad = ctx.createLinearGradient(0, 0, W, H);
  if (isLight) {
    grad.addColorStop(0, 'rgba(245,166,35,0.04)');
    grad.addColorStop(1, 'rgba(45,138,94,0.03)');
  } else {
    grad.addColorStop(0, 'rgba(245,166,35,0.06)');
    grad.addColorStop(1, 'rgba(116,198,157,0.04)');
  }
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  // ── ACCENT STRIPE LEFT (full height) ──
  ctx.fillStyle = t.accent;
  ctx.fillRect(0, 0, W * 0.012, H);

  // ── BOTTOM ACCENT STRIPE ──
  ctx.fillStyle = t.accent2;
  ctx.fillRect(0, H - H*0.012, W, H*0.012);

  // ── SCENE NUMBER - TOP RIGHT ──
  ctx.fillStyle = isLight ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)';
  ctx.fillRect(W * 0.86, 0, W * 0.14, H * 0.1);
  ctx.fillStyle = t.accent;
  ctx.font = `800 ${H*0.05}px Syne, sans-serif`;
  ctx.textAlign = 'center';
  ctx.fillText(`${String(scene.sceneNumber || 1).padStart(2,'0')}`, W * 0.93, H * 0.068);

  // ── LOGO BOTTOM LEFT ──
  ctx.fillStyle = t.accent;
  ctx.font = `700 ${H*0.022}px Syne, sans-serif`;
  ctx.textAlign = 'left';
  ctx.fillText('AfriVid Studio', W * 0.03, H * 0.96);

  // ── MAIN TITLE - LARGE, FULL WIDTH ──
  const titleSize = H * 0.1;
  ctx.fillStyle = t.text;
  ctx.font = `800 ${titleSize}px Syne, sans-serif`;
  ctx.textAlign = 'left';

  const titleX = W * 0.06;
  const maxTitleW = W * 0.82;
  const titleWords = (scene.slideTitle || '').split(' ');
  let titleLine = '';
  let titleY = H * 0.22;
  const titleLines = [];

  titleWords.forEach((word, i) => {
    const test = titleLine + word + ' ';
    if (ctx.measureText(test).width > maxTitleW && titleLine) {
      titleLines.push(titleLine.trim());
      titleLine = word + ' ';
    } else {
      titleLine = test;
    }
    if (i === titleWords.length - 1) titleLines.push(titleLine.trim());
  });

  titleLines.forEach((line, i) => {
    ctx.fillText(line, titleX, titleY + i * titleSize * 1.15);
  });

  const afterTitle = titleY + titleLines.length * titleSize * 1.15;

  // ── SUBTITLE ──
  const subSize = H * 0.038;
  ctx.fillStyle = t.accent;
  ctx.font = `600 ${subSize}px Syne, sans-serif`;
  ctx.fillText(scene.slideSubtitle || '', titleX, afterTitle + subSize * 0.5);

  // ── THIN DIVIDER ──
  const divY = afterTitle + subSize * 1.4;
  ctx.fillStyle = t.accent;
  ctx.globalAlpha = 0.3;
  ctx.fillRect(titleX, divY, W * 0.15, 3);
  ctx.globalAlpha = 1;

  // ── BULLET POINTS — appear sentence by sentence as voice speaks ──
  if (scene.voiceover) {
    const sentences = scene.voiceover
      .replace(/([.!?])\s+/g, '$1|')
      .split('|')
      .map(s => s.trim())
      .filter(s => s.length > 10)
      .slice(0, 4);

    const totalWords = scene.voiceover.split(' ').length;
    const wordsPerSentence = Math.max(1, totalWords / sentences.length);
    const currentSentence = currentWord >= 0 ? Math.min(Math.floor(currentWord / wordsPerSentence), sentences.length - 1) : -1;

    const bulletStartY = divY + H * 0.07;
    const lineSpacing = H * 0.13;
    const bSize = H * 0.032;

    sentences.forEach((sentence, idx) => {
      // Only show sentences that have been spoken
      if (currentWord >= 0 && idx > currentSentence) return;

      const y = bulletStartY + idx * lineSpacing;
      const isActive = idx === currentSentence && currentWord >= 0;

      // Fade old sentences slightly
      ctx.globalAlpha = isActive ? 1 : 0.55;

      // Active highlight
      if (isActive) {
        ctx.fillStyle = isLight ? 'rgba(245,166,35,0.07)' : 'rgba(245,166,35,0.08)';
        ctx.globalAlpha = 1;
        ctx.fillRect(titleX - W*0.01, y - bSize * 1.1, W * 0.88, bSize * 1.8);
        ctx.globalAlpha = 1;
      }

      // Bullet
      ctx.fillStyle = isActive ? t.accent : t.accent2;
      ctx.globalAlpha = isActive ? 1 : 0.55;
      ctx.beginPath();
      ctx.arc(titleX + bSize * 0.4, y - bSize * 0.3, isActive ? bSize * 0.35 : bSize * 0.25, 0, Math.PI * 2);
      ctx.fill();

      // Text
      ctx.fillStyle = isActive ? t.text : t.sub;
      ctx.font = `${isActive ? '600' : '400'} ${isActive ? bSize * 1.05 : bSize}px Syne, sans-serif`;
      ctx.textAlign = 'left';

      // Wrap sentence
      const bWords = sentence.split(' ');
      let bLine = '';
      let bY = y;
      const bX = titleX + bSize * 1.1;
      const maxBW = W * 0.84;

      bWords.forEach((w, wi) => {
        const test = bLine + w + ' ';
        if (ctx.measureText(test).width > maxBW && bLine) {
          ctx.fillText(bLine.trim(), bX, bY);
          bLine = w + ' ';
          bY += bSize * 1.4;
        } else {
          bLine = test;
        }
        if (wi === bWords.length - 1) ctx.fillText(bLine.trim(), bX, bY);
      });

      ctx.globalAlpha = 1;
    });
  }

  // ── PROGRESS BAR BOTTOM ──
  ctx.fillStyle = isLight ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)';
  ctx.fillRect(0, H * 0.988, W, H * 0.012);
  ctx.fillStyle = t.accent;
  ctx.fillRect(0, H * 0.988, W * progress, H * 0.012);

  // Draw presenter photo if set
  drawPresenterPhoto(ctx, W, H);

  if (false) {'''

content = content.replace(old_powerpoint, new_powerpoint, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Synthesia-style slides rebuilt!")
