with open('index.html', 'r') as f:
    content = f.read()

# 1. Add toggle CSS
old_css = '  /* RESPONSIVE - DESKTOP */'
new_css = '''  /* SIDEBAR TOGGLE */
  .sidebar { transition: width 0.25s ease; overflow:hidden; }
  .sidebar.collapsed { width:64px; }
  .sidebar.collapsed .sidebar-logo-text { display:none; }
  .sidebar.collapsed .sidebar-item-label { display:none; }
  .sidebar.collapsed .sidebar-user { display:none; }
  .sidebar.collapsed .sidebar-logo { justify-content:center; padding:0 0 1.5rem; }
  .sidebar.collapsed .sidebar-item { justify-content:center; padding:0.75rem; }
  .sidebar-toggle { position:absolute; top:1.25rem; right:-14px; width:28px; height:28px; border-radius:50%; background:var(--navy2); border:1px solid var(--border2); cursor:pointer; display:flex; align-items:center; justify-content:center; z-index:101; transition:all 0.2s; }
  .sidebar-toggle:hover { background:var(--gold); }
  .sidebar-toggle:hover svg { stroke:#050A14; }
  .app-content { transition: margin-left 0.25s ease; }
  .app-content.expanded { margin-left:64px; }

  /* RESPONSIVE - DESKTOP */'''

content = content.replace(old_css, new_css, 1)

# 2. Replace emoji icons with SVGs and add toggle button
old_sidebar = '''  <aside class="sidebar">
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
  </aside>'''

new_sidebar = '''  <aside class="sidebar" id="sidebar">

    <!-- Toggle button -->
    <button class="sidebar-toggle" id="sidebar-toggle" onclick="toggleSidebar()" title="Toggle sidebar">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <line x1="3" y1="6" x2="21" y2="6"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>

    <div class="sidebar-logo">
      <div class="sidebar-logo-icon">A</div>
      <div class="sidebar-logo-text">AfriVid <span>Studio</span></div>
    </div>

    <nav class="sidebar-nav">
      <button class="sidebar-item active" id="sidebar-create" onclick="switchTab('create')" title="Create Video">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
        <span class="sidebar-item-label">Create Video</span>
      </button>
      <button class="sidebar-item" id="sidebar-enhance" onclick="switchTab('enhance')" title="Edit Video">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        <span class="sidebar-item-label">Edit Video</span>
      </button>
      <button class="sidebar-item" id="sidebar-photo" onclick="switchTab('photo')" title="Photo Editor">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        <span class="sidebar-item-label">Photo Editor</span>
      </button>
      <button class="sidebar-item" id="sidebar-library" onclick="switchTab('library')" title="Library">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
        <span class="sidebar-item-label">Library</span>
      </button>
    </nav>

    <div class="sidebar-divider"></div>

    <div class="sidebar-bottom">
      <button class="sidebar-item" id="sidebar-admin" onclick="switchTab('admin')" style="display:none;" title="Admin">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>
        <span class="sidebar-item-label">Admin</span>
      </button>
      <button class="sidebar-item" onclick="openFeedback()" title="Feedback">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <span class="sidebar-item-label">Feedback</span>
      </button>
      <button class="sidebar-item" onclick="logout()" title="Sign Out">
        <svg class="item-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        <span class="sidebar-item-label">Sign Out</span>
      </button>
    </div>

    <div class="sidebar-user">
      <div class="sidebar-user-name" id="user-name-display">Loading...</div>
      <div class="sidebar-user-plan" id="user-videos-remaining"></div>
    </div>
  </aside>'''

content = content.replace(old_sidebar, new_sidebar, 1)

# 3. Add toggleSidebar JS function
old_switchtab = 'function switchTab(tab) {'
new_switchtab = '''// ── SIDEBAR TOGGLE ──
let sidebarCollapsed = false;
function toggleSidebar() {
  sidebarCollapsed = !sidebarCollapsed;
  const sidebar = document.getElementById('sidebar');
  const content = document.querySelector('.app-content');
  sidebar.classList.toggle('collapsed', sidebarCollapsed);
  if (content) content.classList.toggle('expanded', sidebarCollapsed);
}

function switchTab(tab) {'''

content = content.replace(old_switchtab, new_switchtab, 1)

# 4. Update mobile nav SVG icons too
content = content.replace(
    '<span class="nav-icon">🎬</span>Create',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>Create'
)
content = content.replace(
    '<span class="nav-icon">✂️</span>Edit',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>Edit'
)
content = content.replace(
    '<span class="nav-icon">🖼</span>Photo',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>Photo'
)
content = content.replace(
    '<span class="nav-icon">📚</span>Library',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>Library'
)
content = content.replace(
    '<span class="nav-icon">💬</span>More',
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>More'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Hamburger toggle + SVG icons added!")
