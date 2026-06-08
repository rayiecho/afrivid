with open('index.html', 'r') as f:
    content = f.read()

# Find the main studio content - it should be wrapped in id="app"
# Check what's between feedback modal and script tag
old = '''</div>
<script>
// ── AUTH ──'''

new = '''</div>

<!-- MAIN APP -->
<div id="app" style="display:none;">
  <div class="studio-wrap">
    <!-- HEADER -->
    <header class="header">
      <div class="header-brand">
        <div style="width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.9rem;color:#050A14;">A</div>
        <span class="header-title">AfriVid <span style="color:var(--gold);">Studio</span></span>
        <span class="tag tag-gold">BETA</span>
      </div>
      <div style="display:flex;align-items:center;gap:1rem;">
        <div style="text-align:right;">
          <div style="font-size:0.82rem;font-weight:600;" id="user-name-display">Loading...</div>
          <div style="font-size:0.7rem;color:var(--gold);font-family:var(--font-mono);" id="user-videos-remaining"></div>
        </div>
        <button onclick="openFeedback()" style="background:rgba(245,166,35,0.12);border:1px solid var(--border);color:var(--gold);padding:0.4rem 1rem;border-radius:8px;font-family:var(--font-display);font-size:0.78rem;cursor:pointer;">💬 Feedback</button>
        <button class="header-logout" onclick="logout()">Sign Out</button>
      </div>
    </header>

    <div class="main">
      <!-- MAIN TABS -->
      <div class="main-tabs" id="main-tabs">
        <button class="main-tab active" id="tab-create" onclick="switchTab('create')">🎬 Create Video</button>
        <button class="main-tab" id="tab-enhance" onclick="switchTab('enhance')">✂️ Enhance Video</button>
        <button class="main-tab" id="tab-library" onclick="switchTab('library')">📚 Video Library</button>
        <button class="main-tab" id="tab-photo" onclick="switchTab('photo')">🖼 Photo Editor</button>
      </div>

      <!-- CREATE SECTION -->
      <div class="main-section active" id="section-create">
        <!-- STEPS -->
        <div class="steps-bar">
          <div class="step-item active" id="step-1">
            <div class="step-num">1</div>
            <div class="step-label">Setup</div>
          </div>
          <div class="step-item" id="step-2">
            <div class="step-num">2</div>
            <div class="step-label">Review Script</div>
          </div>
          <div class="step-item" id="step-3">
            <div class="step-num">3</div>
            <div class="step-label">Generate Video</div>
          </div>
          <div class="step-item" id="step-4">
            <div class="step-num">4</div>
            <div class="step-label">Download</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// ── AUTH ──'''

content = content.replace(old, new, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ App div added!")
