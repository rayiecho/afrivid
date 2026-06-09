with open('index.html', 'r') as f:
    content = f.read()

old = """  .sidebar-logo { display:flex; align-items:center; gap:10px; padding:0 1.5rem 1.5rem; padding-top:0.5rem; border-bottom:1px solid var(--border2);margin-bottom:1rem; margin-top:3rem; }
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
  .app-content { margin-left:240px; flex:1; min-height:100vh; padding:2rem; }"""

new = """  .sidebar-logo { display:flex; align-items:center; gap:10px; padding:1.25rem 1.5rem; border-bottom:1px solid var(--border2); margin-bottom:0.5rem; }
  .sidebar-logo-icon { width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg,#F5A623,#E8931A); display:flex; align-items:center; justify-content:center; font-weight:900; font-size:1rem; color:#050A14; flex-shrink:0; }
  .sidebar-logo-text { font-size:0.95rem; font-weight:800; color:#fff; line-height:1.2; }
  .sidebar-logo-text span { color:var(--gold); }
  .sidebar-nav { flex:1; padding:0.5rem 0.75rem 0; }
  .sidebar-item { display:flex; align-items:center; gap:0.75rem; padding:0.7rem 1rem; border-radius:10px; cursor:pointer; color:var(--muted); font-size:0.85rem; font-weight:600; transition:all 0.2s; margin-bottom:0.15rem; border:none; border-left:3px solid transparent; background:none; width:100%; text-align:left; font-family:var(--font-display); }
  .sidebar-item:hover { background:rgba(245,166,35,0.06); color:var(--white); border-left-color:rgba(245,166,35,0.2); }
  .sidebar-item.active { background:rgba(245,166,35,0.1); color:var(--white); border-left-color:var(--gold); }
  .sidebar-item .item-icon { font-size:1rem; width:20px; text-align:center; flex-shrink:0; opacity:0.8; }
  .sidebar-item.active .item-icon { opacity:1; }
  .sidebar-divider { height:1px; background:var(--border2); margin:0.5rem 0.75rem; }
  .sidebar-bottom { padding:0 0.75rem 0.5rem; }
  .sidebar-user { padding:1rem 1.25rem; border-top:1px solid var(--border2); }
  .sidebar-user-name { font-size:0.82rem; font-weight:700; color:var(--white); margin-bottom:0.2rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .sidebar-user-plan { font-size:0.68rem; color:var(--gold); font-family:var(--font-mono); }
  .app-content { margin-left:240px; flex:1; min-height:100vh; padding:2rem 2.5rem; }
  .main { max-width:900px; }
  @media (min-width:1400px) {
    .app-content { padding:2.5rem 3.5rem; }
    .main { max-width:1060px; }
  }"""

if old in content:
    content = content.replace(old, new)
    with open('index.html', 'w') as f:
        f.write(content)
    print("✅ Desktop CSS updated!")
else:
    print("❌ Not found.")
