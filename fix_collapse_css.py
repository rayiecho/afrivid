with open('index.html', 'r') as f:
    content = f.read()

old_sidebar_css = '  .sidebar { width:240px; min-height:100vh; background:var(--navy2); border-right:1px solid var(--border2); display:flex; flex-direction:column; padding:1.5rem 0; position:fixed; left:0; top:0; bottom:0; z-index:100; overflow:visible; }'

new_sidebar_css = '''  .sidebar { width:240px; min-height:100vh; background:var(--navy2); border-right:1px solid var(--border2); display:flex; flex-direction:column; padding:1.5rem 0; position:fixed; left:0; top:0; bottom:0; z-index:100; overflow:visible; transition:width 0.25s ease; }
  .sidebar.collapsed { width:64px; }
  .sidebar.collapsed .sidebar-logo-text { display:none; }
  .sidebar.collapsed .sidebar-item-label { display:none; }
  .sidebar.collapsed .sidebar-user { display:none; }
  .sidebar.collapsed .sidebar-logo { justify-content:center; }
  .sidebar.collapsed .sidebar-item { justify-content:center; padding:0.75rem; }
  .app-content { transition:margin-left 0.25s ease; }
  .app-content.expanded { margin-left:64px; }'''

content = content.replace(old_sidebar_css, new_sidebar_css, 1)

# Also make sure sidebar-item-label class is used
content = content.replace(
    '<span class="sidebar-item-label">Create Video</span>',
    '<span class="sidebar-item-label">Create Video</span>'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Collapse CSS fixed!")
