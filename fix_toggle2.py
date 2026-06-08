with open('index.html', 'r') as f:
    content = f.read()

# Remove floating toggle button
old_toggle = '''  <!-- HAMBURGER TOGGLE -->
  <button id="sidebar-toggle" onclick="toggleSidebar()" style="position:fixed;top:16px;left:16px;z-index:200;width:36px;height:36px;border-radius:8px;background:var(--navy2);border:1px solid var(--border2);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;" title="Toggle sidebar" onmouseover="this.style.background='var(--gold)';this.querySelector('svg').style.stroke='#050A14'" onmouseout="this.style.background='var(--navy2)';this.querySelector('svg').style.stroke='currentColor'">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
      <line x1="3" y1="6" x2="21" y2="6"/>
      <line x1="3" y1="12" x2="21" y2="12"/>
      <line x1="3" y1="18" x2="21" y2="18"/>
    </svg>
  </button>'''

new_toggle = ''
content = content.replace(old_toggle, new_toggle, 1)

# Add toggle inside sidebar logo row
old_logo = '''    <div class="sidebar-logo">
      <div class="sidebar-logo-icon">A</div>
      <div class="sidebar-logo-text">AfriVid <span>Studio</span></div>
    </div>'''

new_logo = '''    <div class="sidebar-logo" style="display:flex;align-items:center;justify-content:space-between;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div class="sidebar-logo-icon">A</div>
        <div class="sidebar-logo-text">AfriVid <span>Studio</span></div>
      </div>
      <button id="sidebar-toggle" onclick="toggleSidebar()" style="background:rgba(255,255,255,0.06);border:1px solid var(--border2);color:var(--muted);width:30px;height:30px;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;" title="Toggle sidebar">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
    </div>'''

content = content.replace(old_logo, new_logo, 1)

# Update collapsed state to hide logo text but keep toggle visible
content = content.replace(
    '.sidebar.collapsed .sidebar-logo { justify-content:center; padding:0 0 1.5rem; }',
    '.sidebar.collapsed .sidebar-logo { justify-content:center; padding:0 0.5rem 1.5rem; }'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Toggle moved inside sidebar logo!")
