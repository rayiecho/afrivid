with open('index.html', 'r') as f:
    content = f.read()

old_mobile = '''  @media (max-width:768px) {
    .sidebar { width:60px; }
    .sidebar-logo-text { display:none; }
    .sidebar-item span:not(.item-icon) { display:none; }
    .app-content { margin-left:60px; }
  }
  /* RESPONSIVE */
  @media (max-width: 768px) {
    .header { padding: 1rem 1.25rem; }
    .main { padding: 1.5rem 1rem; }
    .form-grid { grid-template-columns: 1fr; }
    .form-group.full { grid-column: span 1; }
    .steps-bar { flex-direction: column; border-radius: 14px; }
    .step-item { border-right: none; border-bottom: 1px solid var(--border2); }
    .step-item:last-child { border-bottom: none; }
  }'''

new_mobile = '''  /* RESPONSIVE - DESKTOP */
  @media (max-width:1024px) {
    .sidebar { width:200px; }
    .app-content { margin-left:200px; }
  }

  /* RESPONSIVE - TABLET & MOBILE */
  @media (max-width:768px) {
    /* Hide sidebar on mobile */
    .sidebar { display:none; }
    .app-content { margin-left:0; padding:1rem 0.75rem 80px; }

    /* Bottom nav bar */
    .mobile-nav { display:flex !important; }

    /* Content adjustments */
    .main { padding:1rem 0.75rem; }
    .form-grid { grid-template-columns:1fr; }
    .form-group.full { grid-column:span 1; }
    .steps-bar { flex-direction:column; border-radius:14px; }
    .step-item { border-right:none; border-bottom:1px solid var(--border2); }
    .step-item:last-child { border-bottom:none; }
    .card { padding:1.25rem; }
    .card-title { font-size:0.95rem; }
    .enhance-grid { grid-template-columns:1fr; }
    .btn-row { flex-direction:column; }
    .btn { width:100%; text-align:center; }

    /* Landing page mobile */
    .land-btn-primary, .land-btn-secondary { width:100%; text-align:center; padding:0.9rem 1rem; }
  }

  /* MOBILE NAV BAR */
  .mobile-nav {
    display:none;
    position:fixed;
    bottom:0;
    left:0;
    right:0;
    background:var(--navy2);
    border-top:1px solid var(--border2);
    padding:0.5rem 0;
    z-index:200;
    justify-content:space-around;
    align-items:center;
  }
  .mobile-nav-item {
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:3px;
    padding:0.4rem 0.75rem;
    border-radius:8px;
    cursor:pointer;
    background:none;
    border:none;
    color:var(--muted);
    font-size:0.62rem;
    font-weight:600;
    font-family:var(--font-display);
    transition:all 0.2s;
    flex:1;
  }
  .mobile-nav-item .nav-icon { font-size:1.3rem; }
  .mobile-nav-item.active { color:var(--gold); }
  .mobile-nav-item.active .nav-icon { transform:scale(1.1); }'''

content = content.replace(old_mobile, new_mobile, 1)

# Add mobile nav HTML inside app div after sidebar
old_app_content = '  <!-- MAIN CONTENT -->\n  <div class="app-content">'
new_app_content = '''  <!-- MAIN CONTENT -->
  <div class="app-content">

  <!-- MOBILE TOP BAR -->
  <div style="display:none;" class="mobile-topbar" id="mobile-topbar">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:1rem;background:var(--navy2);border-bottom:1px solid var(--border2);margin:-1rem -0.75rem 1rem;position:sticky;top:0;z-index:50;">
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.8rem;color:#050A14;">A</div>
        <span style="font-size:0.95rem;font-weight:800;color:#fff;">AfriVid <span style="color:var(--gold);">Studio</span></span>
      </div>
      <div style="text-align:right;">
        <div style="font-size:0.75rem;font-weight:600;color:#fff;" id="mobile-user-name"></div>
        <div style="font-size:0.65rem;color:var(--gold);font-family:var(--font-mono);" id="mobile-videos-remaining"></div>
      </div>
    </div>
  </div>'''

content = content.replace(old_app_content, new_app_content, 1)

# Add mobile nav bar before closing app div
old_close = '</div><!-- end app-content -->\n</div><!-- end app-layout -->'
new_close = '''</div><!-- end app-content -->
</div><!-- end app-layout -->

<!-- MOBILE BOTTOM NAV -->
<nav class="mobile-nav" id="mobile-nav">
  <button class="mobile-nav-item active" id="mobile-create" onclick="switchTab('create')">
    <span class="nav-icon">🎬</span>Create
  </button>
  <button class="mobile-nav-item" id="mobile-enhance" onclick="switchTab('enhance')">
    <span class="nav-icon">✂️</span>Edit
  </button>
  <button class="mobile-nav-item" id="mobile-photo" onclick="switchTab('photo')">
    <span class="nav-icon">🖼</span>Photo
  </button>
  <button class="mobile-nav-item" id="mobile-library" onclick="switchTab('library')">
    <span class="nav-icon">📚</span>Library
  </button>
  <button class="mobile-nav-item" onclick="openFeedback()">
    <span class="nav-icon">💬</span>More
  </button>
</nav>'''

content = content.replace(old_close, new_close, 1)

# Update switchTab to also update mobile nav
old_switch = '''function switchTab(tab) {
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

new_switch = '''function switchTab(tab) {
  if (tab === 'library') renderLibrary();
  if (tab === 'admin') { loadAdminDashboard(); return; }
  ['create','enhance','library','photo'].forEach(t => {
    const sec = document.getElementById('section-'+t);
    if (sec) sec.classList.toggle('active', t === tab);
  });
  // Update sidebar
  ['create','enhance','library','photo','admin'].forEach(t => {
    const btn = document.getElementById('sidebar-'+t);
    if (btn) btn.classList.toggle('active', t === tab);
  });
  // Update mobile nav
  ['create','enhance','library','photo'].forEach(t => {
    const btn = document.getElementById('mobile-'+t);
    if (btn) btn.classList.toggle('active', t === tab);
  });
  // Sync mobile user info
  const mun = document.getElementById('mobile-user-name');
  const mur = document.getElementById('mobile-videos-remaining');
  const un = document.getElementById('user-name-display');
  const ur = document.getElementById('user-videos-remaining');
  if (mun && un) mun.textContent = un.textContent;
  if (mur && ur) mur.textContent = ur.textContent;
  // Show mobile topbar on mobile
  const topbar = document.getElementById('mobile-topbar');
  if (topbar && window.innerWidth <= 768) topbar.style.display = 'block';
}'''

content = content.replace(old_switch, new_switch, 1)

# Landing page mobile fixes
old_land_nav = '''  <nav style="position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:1.25rem 4rem;background:rgba(5,10,20,0.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.06);">'''
new_land_nav = '''  <nav style="position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:1.25rem 2rem;background:rgba(5,10,20,0.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.06);flex-wrap:wrap;gap:1rem;">'''
content = content.replace(old_land_nav, new_land_nav, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Mobile responsiveness added!")
