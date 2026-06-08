with open('index.html', 'r') as f:
    content = f.read()

# 1. Add Design Studio tab to sidebar
old_sidebar_library = '''      <button class="sidebar-item" id="sidebar-library" onclick="switchTab('library')" title="Library">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
        <span class="sidebar-item-label">Library</span>
      </button>'''

new_sidebar_library = '''      <button class="sidebar-item" id="sidebar-library" onclick="switchTab('library')" title="Library">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
        <span class="sidebar-item-label">Library</span>
      </button>
      <button class="sidebar-item" id="sidebar-design" onclick="switchTab('design')" title="Design Studio">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>
        <span class="sidebar-item-label">Design Studio</span>
      </button>'''

content = content.replace(old_sidebar_library, new_sidebar_library, 1)

# 2. Update switchTab to include design
content = content.replace(
    "  ['create','enhance','library','photo','admin'].forEach(t => {\n    const b = document.getElementById('sidebar-'+t);\n    if (b) b.classList.toggle('active', t === tab);\n  });",
    "  ['create','enhance','library','photo','design','admin'].forEach(t => {\n    const b = document.getElementById('sidebar-'+t);\n    if (b) b.classList.toggle('active', t === tab);\n  });"
)

content = content.replace(
    "  ['create','enhance','library','photo'].forEach(t => {\n    const sec = document.getElementById('section-'+t);\n    if (sec) { sec.classList.toggle('active', t === tab); sec.style.display = t === tab ? 'block' : 'none'; }\n  });",
    "  ['create','enhance','library','photo','design'].forEach(t => {\n    const sec = document.getElementById('section-'+t);\n    if (sec) { sec.classList.toggle('active', t === tab); sec.style.display = t === tab ? 'block' : 'none'; }\n  });"
)

# 3. Add Design Studio section HTML
old_section_end = "  </div><!-- end section-photo -->"
new_section_end = """  </div><!-- end section-photo -->

  <!-- DESIGN STUDIO SECTION -->
  <div class="main-section" id="section-design" style="display:none;">

    <!-- CANVAS AREA -->
    <div style="display:grid;grid-template-columns:280px 1fr;gap:1.5rem;min-height:80vh;">

      <!-- LEFT PANEL - CONTROLS -->
      <div>

        <!-- AI INSTRUCTIONS -->
        <div class="card" style="margin-bottom:1rem;">
          <div class="card-title"><div class="card-title-icon">🤖</div>AI Design</div>
          <div class="form-group">
            <textarea id="design-ai-prompt" class="form-textarea" style="min-height:90px;" placeholder="Describe your design:
- Logo for AfriVid Studio, gold and dark
- Event poster for YAN conference
- Certificate of participation
- Social media post announcing scholarship
- Flyer for tech training program"></textarea>
            <button onclick="generateDesign()" class="btn btn-gold" style="width:100%;margin-top:0.75rem;">✨ Generate Design</button>
          </div>
        </div>

        <!-- TEMPLATES -->
        <div class="card" style="margin-bottom:1rem;">
          <div class="card-title"><div class="card-title-icon">📋</div>Templates</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
            <button onclick="loadTemplate('logo')" class="preset-btn" style="font-size:0.75rem;padding:0.6rem;">🎯 Logo</button>
            <button onclick="loadTemplate('poster')" class="preset-btn" style="font-size:0.75rem;padding:0.6rem;">📢 Poster</button>
            <button onclick="loadTemplate('flyer')" class="preset-btn" style="font-size:0.75rem;padding:0.6rem;">📄 Flyer</button>
            <button onclick="loadTemplate('certificate')" class="preset-btn" style="font-size:0.75rem;padding:0.6rem;">🏆 Certificate</button>
            <button onclick="loadTemplate('social')" class="preset-btn" style="font-size:0.75rem;padding:0.6rem;">📱 Social</button>
            <button onclick="loadTemplate('banner')" class="preset-btn" style="font-size:0.75rem;padding:0.6rem;">🖼 Banner</button>
          </div>
        </div>

        <!-- CANVAS SIZE -->
        <div class="card" style="margin-bottom:1rem;">
          <div class="card-title"><div class="card-title-icon">📐</div>Canvas Size</div>
          <select id="design-size" class="form-select" onchange="resizeCanvas()">
            <option value="800x800">Square (800×800) — Logo/Social</option>
            <option value="1080x1920">Portrait (1080×1920) — Story/Flyer</option>
            <option value="1920x1080">Landscape (1920×1080) — Banner</option>
            <option value="1240x1754">A4 Portrait — Certificate/Poster</option>
            <option value="1200x628">Facebook Cover</option>
            <option value="1500x500">Twitter Banner</option>
          </select>
        </div>

        <!-- BACKGROUND -->
        <div class="card" style="margin-bottom:1rem;">
          <div class="card-title"><div class="card-title-icon">🎨</div>Background</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.5rem;margin-bottom:0.75rem;">
            <div onclick="setDesignBg('#050A14')" style="height:32px;background:#050A14;border-radius:6px;cursor:pointer;border:2px solid var(--border2);"></div>
            <div onclick="setDesignBg('#F5A623')" style="height:32px;background:#F5A623;border-radius:6px;cursor:pointer;"></div>
            <div onclick="setDesignBg('#74C69D')" style="height:32px;background:#74C69D;border-radius:6px;cursor:pointer;"></div>
            <div onclick="setDesignBg('#ffffff')" style="height:32px;background:#ffffff;border-radius:6px;cursor:pointer;border:1px solid var(--border2);"></div>
            <div onclick="setDesignBg('linear-gradient(135deg,#050A14,#0D1F35)')" style="height:32px;background:linear-gradient(135deg,#050A14,#0D1F35);border-radius:6px;cursor:pointer;"></div>
            <div onclick="setDesignBg('linear-gradient(135deg,#F5A623,#E8931A)')" style="height:32px;background:linear-gradient(135deg,#F5A623,#E8931A);border-radius:6px;cursor:pointer;"></div>
            <div onclick="setDesignBg('linear-gradient(135deg,#0D1F35,#2D8A5E)')" style="height:32px;background:linear-gradient(135deg,#0D1F35,#2D8A5E);border-radius:6px;cursor:pointer;"></div>
            <div onclick="setDesignBg('linear-gradient(135deg,#1a0a00,#F5A623)')" style="height:32px;background:linear-gradient(135deg,#1a0a00,#F5A623);border-radius:6px;cursor:pointer;"></div>
          </div>
          <input type="color" id="design-bg-color" onchange="setDesignBg(this.value)" style="width:100%;height:36px;border-radius:8px;border:1px solid var(--border2);background:var(--navy3);cursor:pointer;">
        </div>

        <!-- ADD ELEMENTS -->
        <div class="card" style="margin-bottom:1rem;">
          <div class="card-title"><div class="card-title-icon">➕</div>Add Elements</div>
          <div style="display:flex;flex-direction:column;gap:0.5rem;">
            <button onclick="addDesignText()" class="preset-btn" style="text-align:left;padding:0.6rem 0.75rem;">T Add Text</button>
            <button onclick="addDesignShape('rect')" class="preset-btn" style="text-align:left;padding:0.6rem 0.75rem;">▭ Rectangle</button>
            <button onclick="addDesignShape('circle')" class="preset-btn" style="text-align:left;padding:0.6rem 0.75rem;">○ Circle</button>
            <button onclick="addDesignShape('line')" class="preset-btn" style="text-align:left;padding:0.6rem 0.75rem;">— Line</button>
            <label class="preset-btn" style="text-align:left;padding:0.6rem 0.75rem;cursor:pointer;">
              🖼 Upload Image
              <input type="file" accept="image/*" onchange="addDesignImage(event)" style="display:none;">
            </label>
          </div>
        </div>

        <!-- DOWNLOAD -->
        <div class="card">
          <div class="card-title"><div class="card-title-icon">⬇</div>Export</div>
          <div style="display:flex;flex-direction:column;gap:0.5rem;">
            <button onclick="downloadDesign('png')" class="btn btn-green" style="width:100%;">⬇ Download PNG</button>
            <button onclick="downloadDesign('jpeg')" class="btn btn-outline" style="width:100%;">⬇ Download JPG</button>
          </div>
        </div>

      </div>

      <!-- RIGHT PANEL - CANVAS -->
      <div>
        <div class="card" style="height:100%;">
          <div class="card-title">
            <div class="card-title-icon">🖼</div>Canvas
            <div style="margin-left:auto;display:flex;gap:0.75rem;">
              <button onclick="clearDesignCanvas()" style="background:rgba(230,51,41,0.1);border:1px solid rgba(230,51,41,0.3);color:#E63329;padding:0.35rem 0.75rem;border-radius:6px;font-size:0.75rem;cursor:pointer;">Clear</button>
              <button onclick="undoDesign()" style="background:var(--navy3);border:1px solid var(--border2);color:var(--white);padding:0.35rem 0.75rem;border-radius:6px;font-size:0.75rem;cursor:pointer;">↩ Undo</button>
            </div>
          </div>

          <!-- Selected element controls -->
          <div id="design-element-controls" style="display:none;padding:0.75rem;background:var(--navy3);border-radius:10px;margin-bottom:1rem;display:flex;gap:1rem;flex-wrap:wrap;align-items:center;">
            <input type="color" id="design-element-color" onchange="updateSelectedElement('color',this.value)" style="width:36px;height:28px;border-radius:4px;border:none;cursor:pointer;" title="Color">
            <input type="range" id="design-element-size" min="8" max="120" value="24" oninput="updateSelectedElement('size',this.value)" style="width:80px;accent-color:var(--gold);" title="Size">
            <select id="design-element-font" onchange="updateSelectedElement('font',this.value)" style="background:var(--navy2);border:1px solid var(--border2);color:var(--white);padding:0.25rem;border-radius:4px;font-size:0.75rem;">
              <option value="Syne">Syne</option>
              <option value="Space Mono">Mono</option>
              <option value="Arial">Arial</option>
              <option value="Georgia">Georgia</option>
            </select>
            <select id="design-element-weight" onchange="updateSelectedElement('weight',this.value)" style="background:var(--navy2);border:1px solid var(--border2);color:var(--white);padding:0.25rem;border-radius:4px;font-size:0.75rem;">
              <option value="400">Normal</option>
              <option value="700">Bold</option>
              <option value="800">Extra Bold</option>
            </select>
            <button onclick="deleteSelectedElement()" style="background:rgba(230,51,41,0.15);border:1px solid rgba(230,51,41,0.3);color:#E63329;padding:0.25rem 0.5rem;border-radius:4px;font-size:0.75rem;cursor:pointer;">🗑 Delete</button>
          </div>

          <div style="overflow:auto;display:flex;align-items:center;justify-content:center;min-height:500px;background:repeating-conic-gradient(rgba(255,255,255,0.03) 0% 25%, transparent 0% 50%) 0 0 / 20px 20px;border-radius:10px;">
            <canvas id="design-canvas" style="box-shadow:0 20px 60px rgba(0,0,0,0.5);cursor:crosshair;max-width:100%;"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>"""

content = content.replace(old_section_end, new_section_end, 1)

# 4. Add Design Studio JS
old_make_another = 'function makeAnother() {'
new_make_another = '''// ── DESIGN STUDIO ──
let designElements = [];
let designHistory = [];
let selectedElement = null;
let isDragging = false;
let dragOffset = { x: 0, y: 0 };
let designBg = '#050A14';
let designW = 800, designH = 800;

function initDesignCanvas() {
  const canvas = document.getElementById('design-canvas');
  if (!canvas) return;
  canvas.width = designW;
  canvas.height = designH;
  renderDesign();
  
  canvas.addEventListener('mousedown', onDesignMouseDown);
  canvas.addEventListener('mousemove', onDesignMouseMove);
  canvas.addEventListener('mouseup', onDesignMouseUp);
  canvas.addEventListener('dblclick', onDesignDblClick);
}

function resizeCanvas() {
  const size = document.getElementById('design-size').value;
  const parts = size.split('x');
  designW = parseInt(parts[0]);
  designH = parseInt(parts[1]);
  const canvas = document.getElementById('design-canvas');
  canvas.width = designW;
  canvas.height = designH;
  renderDesign();
}

function setDesignBg(color) {
  designBg = color;
  renderDesign();
}

function renderDesign() {
  const canvas = document.getElementById('design-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;

  // Background
  if (designBg.includes('gradient')) {
    const grad = parseGradient(ctx, designBg, W, H);
    ctx.fillStyle = grad;
  } else {
    ctx.fillStyle = designBg;
  }
  ctx.fillRect(0, 0, W, H);

  // Draw elements
  designElements.forEach((el, idx) => {
    ctx.save();
    const isSelected = selectedElement === idx;

    if (el.type === 'text') {
      ctx.fillStyle = el.color || '#ffffff';
      ctx.font = `${el.weight || 700} ${el.size || 32}px ${el.font || 'Syne'}, sans-serif`;
      ctx.textAlign = el.align || 'left';
      ctx.fillText(el.text, el.x, el.y);
    } else if (el.type === 'rect') {
      ctx.fillStyle = el.color || '#F5A623';
      ctx.fillRect(el.x, el.y, el.w || 200, el.h || 100);
    } else if (el.type === 'circle') {
      ctx.fillStyle = el.color || '#F5A623';
      ctx.beginPath();
      ctx.arc(el.x, el.y, el.r || 50, 0, Math.PI * 2);
      ctx.fill();
    } else if (el.type === 'line') {
      ctx.strokeStyle = el.color || '#F5A623';
      ctx.lineWidth = el.size || 3;
      ctx.beginPath();
      ctx.moveTo(el.x, el.y);
      ctx.lineTo(el.x2 || el.x + 200, el.y2 || el.y);
      ctx.stroke();
    } else if (el.type === 'image' && el.img) {
      ctx.drawImage(el.img, el.x, el.y, el.w || 200, el.h || 200);
    }

    // Selection indicator
    if (isSelected) {
      ctx.strokeStyle = '#F5A623';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 3]);
      const bounds = getElementBounds(el);
      ctx.strokeRect(bounds.x - 5, bounds.y - 5, bounds.w + 10, bounds.h + 10);
      ctx.setLineDash([]);
    }
    ctx.restore();
  });
}

function parseGradient(ctx, gradStr, W, H) {
  const grad = ctx.createLinearGradient(0, 0, W, H);
  const colors = gradStr.match(/#[a-fA-F0-9]{6}/g) || ['#050A14', '#0D1F35'];
  colors.forEach((c, i) => grad.addColorStop(i / (colors.length - 1), c));
  return grad;
}

function getElementBounds(el) {
  if (el.type === 'text') return { x: el.x, y: el.y - (el.size || 32), w: 200, h: el.size || 32 };
  if (el.type === 'rect') return { x: el.x, y: el.y, w: el.w || 200, h: el.h || 100 };
  if (el.type === 'circle') return { x: el.x - (el.r || 50), y: el.y - (el.r || 50), w: (el.r || 50) * 2, h: (el.r || 50) * 2 };
  if (el.type === 'image') return { x: el.x, y: el.y, w: el.w || 200, h: el.h || 200 };
  return { x: el.x, y: el.y, w: 100, h: 30 };
}

function onDesignMouseDown(e) {
  const canvas = document.getElementById('design-canvas');
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const x = (e.clientX - rect.left) * scaleX;
  const y = (e.clientY - rect.top) * scaleY;

  // Find clicked element (reverse order - top first)
  selectedElement = null;
  for (let i = designElements.length - 1; i >= 0; i--) {
    const bounds = getElementBounds(designElements[i]);
    if (x >= bounds.x - 10 && x <= bounds.x + bounds.w + 10 &&
        y >= bounds.y - 10 && y <= bounds.y + bounds.h + 10) {
      selectedElement = i;
      isDragging = true;
      dragOffset = { x: x - designElements[i].x, y: y - designElements[i].y };
      break;
    }
  }
  
  updateElementControls();
  renderDesign();
}

function onDesignMouseMove(e) {
  if (!isDragging || selectedElement === null) return;
  const canvas = document.getElementById('design-canvas');
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const x = (e.clientX - rect.left) * scaleX;
  const y = (e.clientY - rect.top) * scaleY;
  designElements[selectedElement].x = x - dragOffset.x;
  designElements[selectedElement].y = y - dragOffset.y;
  renderDesign();
}

function onDesignMouseUp() {
  if (isDragging) saveDesignHistory();
  isDragging = false;
}

function onDesignDblClick(e) {
  if (selectedElement !== null && designElements[selectedElement].type === 'text') {
    const newText = prompt('Edit text:', designElements[selectedElement].text);
    if (newText !== null) {
      designElements[selectedElement].text = newText;
      saveDesignHistory();
      renderDesign();
    }
  }
}

function updateElementControls() {
  const controls = document.getElementById('design-element-controls');
  if (!controls) return;
  if (selectedElement !== null) {
    controls.style.display = 'flex';
    const el = designElements[selectedElement];
    document.getElementById('design-element-color').value = el.color || '#ffffff';
    document.getElementById('design-element-size').value = el.size || el.r || 24;
  } else {
    controls.style.display = 'none';
  }
}

function updateSelectedElement(prop, value) {
  if (selectedElement === null) return;
  const el = designElements[selectedElement];
  if (prop === 'color') el.color = value;
  if (prop === 'size') { el.size = parseInt(value); el.r = parseInt(value); }
  if (prop === 'font') el.font = value;
  if (prop === 'weight') el.weight = value;
  saveDesignHistory();
  renderDesign();
}

function deleteSelectedElement() {
  if (selectedElement === null) return;
  designElements.splice(selectedElement, 1);
  selectedElement = null;
  updateElementControls();
  saveDesignHistory();
  renderDesign();
}

function addDesignText() {
  designElements.push({
    type: 'text', text: 'Your Text Here',
    x: designW / 2 - 100, y: designH / 2,
    color: '#ffffff', size: 48, font: 'Syne', weight: 700, align: 'left'
  });
  selectedElement = designElements.length - 1;
  saveDesignHistory();
  renderDesign();
}

function addDesignShape(type) {
  if (type === 'rect') designElements.push({ type: 'rect', x: designW/2-100, y: designH/2-50, w: 200, h: 100, color: '#F5A623' });
  if (type === 'circle') designElements.push({ type: 'circle', x: designW/2, y: designH/2, r: 60, color: '#F5A623' });
  if (type === 'line') designElements.push({ type: 'line', x: designW/2-100, y: designH/2, x2: designW/2+100, y2: designH/2, color: '#F5A623', size: 3 });
  selectedElement = designElements.length - 1;
  saveDesignHistory();
  renderDesign();
}

function addDesignImage(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      designElements.push({ type: 'image', img, x: designW/2-100, y: designH/2-100, w: 200, h: 200 });
      selectedElement = designElements.length - 1;
      saveDesignHistory();
      renderDesign();
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function clearDesignCanvas() {
  if (!confirm('Clear all elements?')) return;
  designElements = [];
  selectedElement = null;
  saveDesignHistory();
  renderDesign();
}

function saveDesignHistory() {
  designHistory.push(JSON.stringify(designElements.map(e => ({...e, img: e.img ? 'img' : null}))));
  if (designHistory.length > 20) designHistory.shift();
}

function undoDesign() {
  if (designHistory.length < 2) return;
  designHistory.pop();
  const prev = JSON.parse(designHistory[designHistory.length - 1]);
  designElements = prev.filter(e => e.img !== 'img');
  renderDesign();
}

function downloadDesign(format) {
  const canvas = document.getElementById('design-canvas');
  selectedElement = null;
  renderDesign();
  const url = canvas.toDataURL(`image/${format}`, format === 'jpeg' ? 0.92 : 1);
  const a = document.createElement('a');
  a.href = url;
  a.download = `AfriVid-Design-${Date.now()}.${format}`;
  a.click();
}

function loadTemplate(type) {
  designElements = [];
  selectedElement = null;

  const templates = {
    logo: {
      bg: '#050A14', size: '800x800',
      elements: [
        { type: 'circle', x: 400, y: 340, r: 120, color: '#F5A623' },
        { type: 'text', text: 'A', x: 355, y: 380, color: '#050A14', size: 120, font: 'Syne', weight: 900 },
        { type: 'text', text: 'AfriVid Studio', x: 400, y: 520, color: '#ffffff', size: 52, font: 'Syne', weight: 800, align: 'center' },
        { type: 'text', text: "AFRICA'S FIRST AI VIDEO SUITE", x: 400, y: 570, color: '#F5A623', size: 18, font: 'Space Mono', weight: 400, align: 'center' },
      ]
    },
    poster: {
      bg: 'linear-gradient(135deg,#050A14,#0D2B1A)', size: '1080x1920',
      elements: [
        { type: 'rect', x: 0, y: 0, w: 1080, h: 8, color: '#F5A623' },
        { type: 'text', text: 'EVENT TITLE', x: 100, y: 300, color: '#F5A623', size: 80, font: 'Syne', weight: 800 },
        { type: 'text', text: 'Subtitle or description goes here', x: 100, y: 400, color: '#ffffff', size: 40, font: 'Syne', weight: 400 },
        { type: 'text', text: '📅 Date · 📍 Location', x: 100, y: 500, color: '#74C69D', size: 36, font: 'Syne', weight: 600 },
        { type: 'rect', x: 0, y: 1912, w: 1080, h: 8, color: '#F5A623' },
      ]
    },
    certificate: {
      bg: '#ffffff', size: '1240x1754',
      elements: [
        { type: 'rect', x: 0, y: 0, w: 1240, h: 12, color: '#F5A623' },
        { type: 'rect', x: 0, y: 1742, w: 1240, h: 12, color: '#F5A623' },
        { type: 'rect', x: 0, y: 0, w: 12, h: 1754, color: '#F5A623' },
        { type: 'rect', x: 1228, y: 0, w: 12, h: 1754, color: '#F5A623' },
        { type: 'text', text: 'CERTIFICATE OF PARTICIPATION', x: 620, y: 250, color: '#050A14', size: 54, font: 'Syne', weight: 800, align: 'center' },
        { type: 'text', text: 'This is to certify that', x: 620, y: 450, color: '#6B7A99', size: 32, font: 'Syne', weight: 400, align: 'center' },
        { type: 'text', text: 'RECIPIENT NAME', x: 620, y: 600, color: '#F5A623', size: 72, font: 'Syne', weight: 800, align: 'center' },
        { type: 'rect', x: 320, y: 640, w: 600, h: 4, color: '#F5A623' },
        { type: 'text', text: 'has successfully participated in', x: 620, y: 730, color: '#6B7A99', size: 32, font: 'Syne', weight: 400, align: 'center' },
        { type: 'text', text: 'PROGRAM NAME', x: 620, y: 830, color: '#050A14', size: 52, font: 'Syne', weight: 700, align: 'center' },
        { type: 'text', text: 'AfriVid Studio', x: 620, y: 1500, color: '#050A14', size: 36, font: 'Syne', weight: 700, align: 'center' },
      ]
    },
    flyer: {
      bg: 'linear-gradient(135deg,#050A14,#F5A623)', size: '1080x1920',
      elements: [
        { type: 'text', text: '🚀', x: 490, y: 400, color: '#ffffff', size: 120, font: 'Syne', weight: 400 },
        { type: 'text', text: 'JOIN US', x: 540, y: 600, color: '#ffffff', size: 100, font: 'Syne', weight: 900, align: 'center' },
        { type: 'text', text: 'for something amazing', x: 540, y: 700, color: 'rgba(255,255,255,0.8)', size: 44, font: 'Syne', weight: 400, align: 'center' },
        { type: 'rect', x: 200, y: 780, w: 680, h: 3, color: 'rgba(255,255,255,0.4)' },
        { type: 'text', text: 'Date · Time · Location', x: 540, y: 870, color: 'rgba(255,255,255,0.9)', size: 38, font: 'Syne', weight: 600, align: 'center' },
      ]
    },
    social: {
      bg: '#050A14', size: '1080x1920',
      elements: [
        { type: 'rect', x: 0, y: 0, w: 1080, h: 6, color: '#F5A623' },
        { type: 'text', text: 'YOUR HEADLINE', x: 80, y: 500, color: '#ffffff', size: 90, font: 'Syne', weight: 800 },
        { type: 'text', text: 'Supporting text goes here', x: 80, y: 620, color: '#74C69D', size: 44, font: 'Syne', weight: 400 },
        { type: 'text', text: '@AfriVidStudio', x: 80, y: 1800, color: '#F5A623', size: 36, font: 'Space Mono', weight: 400 },
      ]
    },
    banner: {
      bg: 'linear-gradient(135deg,#050A14,#0D1F35)', size: '1920x1080',
      elements: [
        { type: 'circle', x: 200, y: 540, r: 150, color: 'rgba(245,166,35,0.15)' },
        { type: 'text', text: 'AfriVid Studio', x: 400, y: 480, color: '#ffffff', size: 96, font: 'Syne', weight: 800 },
        { type: 'text', text: "Africa's First AI Video Creation Suite", x: 400, y: 580, color: '#F5A623', size: 42, font: 'Syne', weight: 400 },
        { type: 'rect', x: 400, y: 620, w: 200, h: 4, color: '#74C69D' },
      ]
    }
  };

  const t = templates[type];
  if (!t) return;

  designBg = t.bg;
  const sizeParts = t.size.split('x');
  designW = parseInt(sizeParts[0]);
  designH = parseInt(sizeParts[1]);
  document.getElementById('design-size').value = t.size;

  const canvas = document.getElementById('design-canvas');
  canvas.width = designW;
  canvas.height = designH;

  designElements = t.elements.map(e => ({...e}));
  saveDesignHistory();
  renderDesign();
}

async function generateDesign() {
  const prompt = document.getElementById('design-ai-prompt').value.trim();
  if (!prompt) { alert('Describe your design first'); return; }

  const btn = document.querySelector('#section-design .btn-gold');
  if (btn) { btn.textContent = '⏳ Generating...'; btn.disabled = true; }

  try {
    const response = await fetch('https://yan-ai-worker.youngafricansn.workers.dev', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1500,
        messages: [{
          role: 'user',
          content: `You are a graphic design AI. Create a design based on: "${prompt}"

Canvas is ${designW}x${designH} pixels.

Return ONLY a JSON object:
{
  "background": "#hex or linear-gradient(135deg, #hex1, #hex2)",
  "elements": [
    {"type": "text", "text": "...", "x": 100, "y": 200, "color": "#hex", "size": 48, "font": "Syne", "weight": 700},
    {"type": "rect", "x": 0, "y": 0, "w": 400, "h": 8, "color": "#hex"},
    {"type": "circle", "x": 200, "y": 200, "r": 80, "color": "#hex"}
  ]
}

Use AfriVid brand colors: gold #F5A623, dark #050A14, green #74C69D.
Make it professional and visually striking. Max 10 elements.`
        }]
      })
    });

    const data = await response.json();
    const text = data.content[0].text.trim();
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error('No JSON');
    const design = JSON.parse(jsonMatch[0]);

    designBg = design.background || '#050A14';
    designElements = design.elements || [];
    saveDesignHistory();
    renderDesign();

  } catch(e) {
    alert('Generation failed: ' + e.message);
  }

  if (btn) { btn.textContent = '✨ Generate Design'; btn.disabled = false; }
}

// Initialize design canvas when tab is opened
const origSwitchTab = window.switchTab;

function makeAnother() {'''

content = content.replace(old_make_another, new_make_another, 1)

# Initialize design canvas when switching to design tab
old_switch = 'function switchTab(tab) {'
new_switch = '''function switchTab(tab) {
  if (tab === 'design') {
    setTimeout(() => {
      initDesignCanvas();
      if (designElements.length === 0) loadTemplate('logo');
    }, 100);
  }'''
content = content.replace(old_switch, new_switch, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Design Studio added!")
