with open('index.html', 'r') as f:
    content = f.read()

# Fix sidebar to allow overflow for the toggle button
content = content.replace(
    '.sidebar { width:240px; min-height:100vh; background:var(--navy2); border-right:1px solid var(--border2); display:flex; flex-direction:column; padding:1.5rem 0; position:fixed; left:0; top:0; bottom:0; z-index:100; }',
    '.sidebar { width:240px; min-height:100vh; background:var(--navy2); border-right:1px solid var(--border2); display:flex; flex-direction:column; padding:1.5rem 0; position:fixed; left:0; top:0; bottom:0; z-index:100; overflow:visible; }'
)

# Move toggle button outside sidebar, into app-layout
old_toggle = '''    <!-- Toggle button -->
    <button class="sidebar-toggle" id="sidebar-toggle" onclick="toggleSidebar()" title="Toggle sidebar">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <line x1="3" y1="6" x2="21" y2="6"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>

    <div class="sidebar-logo">'''

new_toggle = '''    <div class="sidebar-logo">'''

content = content.replace(old_toggle, new_toggle, 1)

# Add toggle button as fixed element in app-layout
old_app_layout = '<div class="app-layout">'
new_app_layout = '''<div class="app-layout">
  <!-- HAMBURGER TOGGLE -->
  <button id="sidebar-toggle" onclick="toggleSidebar()" style="position:fixed;top:16px;left:16px;z-index:200;width:36px;height:36px;border-radius:8px;background:var(--navy2);border:1px solid var(--border2);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;" title="Toggle sidebar" onmouseover="this.style.background='var(--gold)';this.querySelector('svg').style.stroke='#050A14'" onmouseout="this.style.background='var(--navy2)';this.querySelector('svg').style.stroke='currentColor'">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
      <line x1="3" y1="6" x2="21" y2="6"/>
      <line x1="3" y1="12" x2="21" y2="12"/>
      <line x1="3" y1="18" x2="21" y2="18"/>
    </svg>
  </button>'''

content = content.replace(old_app_layout, new_app_layout, 1)

# Add padding to sidebar logo to account for toggle button
content = content.replace(
    '.sidebar-logo { display:flex; align-items:center; gap:10px; padding:0 1.5rem 1.5rem; border-bottom:1px solid var(--border2); margin-bottom:1rem; }',
    '.sidebar-logo { display:flex; align-items:center; gap:10px; padding:0 1.5rem 1.5rem; padding-top:0.5rem; border-bottom:1px solid var(--border2); margin-bottom:1rem; margin-top:3rem; }'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Toggle fixed!")
