with open('index.html', 'r') as f:
    content = f.read()

# 1. Add sidebar CSS
old_css = '  /* RESPONSIVE */'
new_css = '''  /* SIDEBAR LAYOUT */
  .app-layout { display:flex; min-height:100vh; background:var(--navy); }
  .sidebar { width:240px; min-height:100vh; background:var(--navy2); border-right:1px solid var(--border2); display:flex; flex-direction:column; padding:1.5rem 0; position:fixed; left:0; top:0; bottom:0; z-index:100; }
  .sidebar-logo { display:flex; align-items:center; gap:10px; padding:0 1.5rem 1.5rem; border-bottom:1px solid var(--border2); margin-bottom:1rem; }
  .sidebar-logo-icon { width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#F5A623,#E8931A); display:flex; align-items:center; justify-content:center; font-weight:900; font-size:1rem; color:#050A14; flex-shrink:0; }
  .sidebar-logo-text { font-size:1rem; font-weight:800; color:#fff; }
  .sidebar-logo-text span { color:var(--gold); }
  .sidebar-nav { flex:1; padding:0 0.75rem; }
  .sidebar-item { display:flex; align-items:center; gap:0.75rem; padding:0.75rem 1rem; border-radius:10px; cursor:pointer; color:var(--muted); font-size:0.88rem; font-weight:600; transition:all 0.2s; margin-bottom:0.25rem; border:none; background:none; width:100%; text-align:left; font-family:var(--font-display); }
  .sidebar-item:hover { background:rgba(245,166,35,0.06); color:var(--white); }
  .sidebar-item.active { background:rgba(245,166,35,0.1); color:var(--white); border-left:3px solid var(--gold); }
  .sidebar-item .item-icon { font-size:1.1rem; width:20px; text-align:center; flex-shrink:0; }
  .sidebar-divider { height:1px; background:var(--border2); margin:0.75rem 0.75rem; }
  .sidebar-bottom { padding:0 0.75rem; }
  .sidebar-user { padding:1rem 1.5rem; border-top:1px solid var(--border2); margin-top:auto; }
  .sidebar-user-name { font-size:0.82rem; font-weight:700; color:var(--white); margin-bottom:0.15rem; }
  .sidebar-user-plan { font-size:0.7rem; color:var(--gold); font-family:var(--font-mono); }
  .app-content { margin-left:240px; flex:1; min-height:100vh; padding:2rem; }
  @media (max-width:768px) {
    .sidebar { width:60px; }
    .sidebar-logo-text { display:none; }
    .sidebar-item span:not(.item-icon) { display:none; }
    .app-content { margin-left:60px; }
  }

  /* RESPONSIVE */'''

content = content.replace(old_css, new_css, 1)

# 2. Replace the app div structure
old_app = '''<!-- APP -->
<div id="app" style="display:none;">
  <!-- HEADER -->
  <header class="header">
    <div class="header-brand">'''

new_app = '''<!-- APP -->
<div id="app" style="display:none;">
<div class="app-layout">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="sidebar-logo-icon">A</div>
      <div class="sidebar-logo-text">AfriVid <span>Studio</span></div>
    </div>

    <nav class="sidebar-nav">
      <button class="sidebar-item active" id="sidebar-create" onclick="switchTab('create')">
        <span class="item-icon">🎬</span>
        <span>Create Video</span>
      </button>
      <button class="sidebar-item" id="sidebar-enhance" onclick="switchTab('enhance')">
        <span class="item-icon">✂️</span>
        <span>Edit Video</span>
      </button>
      <button class="sidebar-item" id="sidebar-photo" onclick="switchTab('photo')">
        <span class="item-icon">🖼</span>
        <span>Photo Editor</span>
      </button>
      <button class="sidebar-item" id="sidebar-library" onclick="switchTab('library')">
        <span class="item-icon">📚</span>
        <span>Library</span>
      </button>
    </nav>

    <div class="sidebar-divider"></div>

    <div class="sidebar-bottom">
      <button class="sidebar-item" id="sidebar-admin" onclick="switchTab('admin')" style="display:none;">
        <span class="item-icon">⚙️</span>
        <span>Admin</span>
      </button>
      <button class="sidebar-item" onclick="openFeedback()">
        <span class="item-icon">💬</span>
        <span>Feedback</span>
      </button>
      <button class="sidebar-item" onclick="logout()">
        <span class="item-icon">🚪</span>
        <span>Sign Out</span>
      </button>
    </div>

    <div class="sidebar-user">
      <div class="sidebar-user-name" id="user-name-display">Loading...</div>
      <div class="sidebar-user-plan" id="user-videos-remaining"></div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <div class="app-content">
  <!-- HEADER (hidden - sidebar replaces it) -->
  <header class="header" style="display:none;">
    <div class="header-brand">'''

content = content.replace(old_app, new_app, 1)

# 3. Close the app-content and app-layout divs at end of app
old_app_close = '</div>\n\n<!-- FEEDBACK'
new_app_close = '</div><!-- end app-content -->\n</div><!-- end app-layout -->\n\n<!-- FEEDBACK'
content = content.replace(old_app_close, new_app_close, 1)

# 4. Hide old tabs bar
content = content.replace(
    '<div class="main-tabs" id="main-tabs">',
    '<div class="main-tabs" id="main-tabs" style="display:none;">'
)

# 5. Update switchTab to use sidebar
old_switch = '''function switchTab(tab) {
  if (tab === 'library') renderLibrary();
  ['create','enhance','library','photo'].forEach(t => {
    document.getElementById('section-'+t).classList.toggle('active', t === tab);
    document.getElementById('tab-'+t).classList.toggle('active', t === tab);
  });
}'''

new_switch = '''function switchTab(tab) {
  if (tab === 'library') renderLibrary();
  if (tab === 'admin') { loadAdminDashboard(); return; }
  ['create','enhance','library','photo'].forEach(t => {
    const sec = document.getElementById('section-'+t);
    if (sec) sec.classList.toggle('active', t === tab);
  });
  // Update sidebar active state
  ['create','enhance','library','photo','admin'].forEach(t => {
    const btn = document.getElementById('sidebar-'+t);
    if (btn) btn.classList.toggle('active', t === tab);
  });
}'''

content = content.replace(old_switch, new_switch, 1)

# 6. Update showAdminTab to show sidebar button
old_admin_tab = '''  window.showAdminTab = function() {
    const tabs = document.getElementById('main-tabs');
    if (tabs && !document.getElementById('tab-admin')) {
      const btn = document.createElement('button');
      btn.className = 'main-tab';
      btn.id = 'tab-admin';
      btn.onclick = () => loadAdminDashboard();
      btn.textContent = '⚙️ Admin';
      tabs.appendChild(btn);
    }
  };'''

new_admin_tab = '''  window.showAdminTab = function() {
    const adminBtn = document.getElementById('sidebar-admin');
    if (adminBtn) adminBtn.style.display = 'flex';
  };'''

content = content.replace(old_admin_tab, new_admin_tab, 1)

# 7. Rename Enhance to Edit in the tab
content = content.replace(
    'id="tab-enhance" onclick="switchTab(\'enhance\')">✂️ Enhance Video',
    'id="tab-enhance" onclick="switchTab(\'enhance\')">✂️ Edit Video'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Sidebar layout added!")
