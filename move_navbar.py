with open('index.html', 'r') as f:
    content = f.read()

# Remove navbar from top
old_nav = '''  <nav style="position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:1.25rem 4rem;background:rgba(5,10,20,0.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.06);">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1rem;color:#050A14;animation:glow 3s ease-in-out infinite;">A</div>
      <span style="font-size:1.1rem;font-weight:800;color:#fff;">AfriVid</span>
      <span style="font-size:1.1rem;font-weight:800;color:#F5A623;">Studio</span>
      <span style="font-size:0.65rem;background:rgba(245,166,35,0.15);border:1px solid rgba(245,166,35,0.3);color:#F5A623;padding:0.2rem 0.6rem;border-radius:50px;font-family:'Space Mono',monospace;letter-spacing:1px;">BETA</span>
    </div>
    <div style="display:flex;gap:2rem;align-items:center;">
      <a href="#features" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;">Features</a>
      <a href="#pricing" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;">Pricing</a>
      <button onclick="showLogin()" style="background:transparent;border:1px solid rgba(245,166,35,0.4);color:#F5A623;padding:0.6rem 1.5rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>
      <button onclick="showLogin()" class="land-btn-primary" style="padding:0.6rem 1.5rem;font-size:0.85rem;">Get Started Free →</button>
    </div>
  </nav>'''

new_nav = ''

content = content.replace(old_nav, new_nav, 1)

# Add it below stats section
old_after_stats = '''  <div id="features"'''

new_after_stats = '''  <!-- MOVED NAV -->
  <div style="position:relative;z-index:1;max-width:900px;margin:0 auto 4rem;padding:0 4rem;">
    <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.25rem 2rem;backdrop-filter:blur(20px);">
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1rem;color:#050A14;">A</div>
        <span style="font-size:1.1rem;font-weight:800;color:#fff;">AfriVid</span>
        <span style="font-size:1.1rem;font-weight:800;color:#F5A623;">Studio</span>
        <span style="font-size:0.65rem;background:rgba(245,166,35,0.15);border:1px solid rgba(245,166,35,0.3);color:#F5A623;padding:0.2rem 0.6rem;border-radius:50px;font-family:'Space Mono',monospace;letter-spacing:1px;">BETA</span>
      </div>
      <div style="display:flex;gap:1.5rem;align-items:center;">
        <a href="#features" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;">Features</a>
        <a href="#pricing" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;">Pricing</a>
        <button onclick="showLogin()" style="background:transparent;border:1px solid rgba(245,166,35,0.4);color:#F5A623;padding:0.5rem 1.2rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>
        <button onclick="showLogin()" class="land-btn-primary" style="padding:0.5rem 1.2rem;font-size:0.85rem;">Get Started Free →</button>
      </div>
    </div>
  </div>

  <div id="features"'''

content = content.replace(old_after_stats, new_after_stats, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Navbar moved below stats!")
