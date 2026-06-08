with open('index.html', 'r') as f:
    content = f.read()

# Apply workspace bg to landing hero section
content = content.replace(
    '<div id="landing-screen" style="position:fixed;inset:0;z-index:999;overflow-y:auto;background:#050A14;font-family:\'Syne\',sans-serif;">',
    '<div id="landing-screen" style="position:fixed;inset:0;z-index:999;overflow-y:auto;background:#050A14;font-family:\'Syne\',sans-serif;">'
)

# Replace hero background with full bleed image
old_hero_bg = '''  <!-- Animated background -->
  <div style="position:fixed;inset:0;pointer-events:none;z-index:0;">
    <div style="position:absolute;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(245,166,35,0.08),transparent 70%);top:-100px;right:-100px;animation:pulse 6s ease-in-out infinite;"></div>
    <div style="position:absolute;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(27,67,50,0.15),transparent 70%);bottom:-100px;left:-100px;animation:pulse 8s ease-in-out infinite reverse;"></div>
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(245,166,35,0.03) 1px,transparent 1px);background-size:40px 40px;"></div>
  </div>'''

new_hero_bg = '''  <!-- Split background -->
  <div style="position:fixed;inset:0;pointer-events:none;z-index:0;">
    <!-- Left half - workspace photo -->
    <div style="position:absolute;top:0;left:0;width:50%;height:100%;background:url('images/bg-workspace.jpg') center/cover no-repeat;opacity:0.15;"></div>
    <!-- Right half - editor photo -->
    <div style="position:absolute;top:0;right:0;width:50%;height:100%;background:url('images/bg-editor.jpg') center/cover no-repeat;opacity:0.15;"></div>
    <!-- Gradient overlay -->
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(5,10,20,0.92) 0%,rgba(5,10,20,0.75) 50%,rgba(5,10,20,0.92) 100%);"></div>
    <!-- Dot grid -->
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(245,166,35,0.04) 1px,transparent 1px);background-size:40px 40px;"></div>
    <!-- Gold accent line -->
    <div style="position:absolute;top:0;left:50%;width:1px;height:100%;background:linear-gradient(180deg,transparent,rgba(245,166,35,0.15),transparent);"></div>
  </div>'''

content = content.replace(old_hero_bg, new_hero_bg, 1)

# Apply editor bg to login screen
old_login_bg = '''  <!-- Background effects -->
  <div style="position:fixed;inset:0;pointer-events:none;">
    <div style="position:absolute;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(245,166,35,0.06),transparent 70%);top:50%;left:50%;transform:translate(-50%,-50%);"></div>
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(245,166,35,0.02) 1px,transparent 1px);background-size:40px 40px;"></div>
  </div>'''

new_login_bg = '''  <!-- Background effects -->
  <div style="position:fixed;inset:0;pointer-events:none;">
    <div style="position:absolute;inset:0;background:url('images/bg-editor.jpg') center/cover no-repeat;opacity:0.12;"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(5,10,20,0.95),rgba(5,10,20,0.88));"></div>
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(245,166,35,0.03) 1px,transparent 1px);background-size:40px 40px;"></div>
    <div style="position:absolute;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(245,166,35,0.06),transparent 70%);top:50%;left:50%;transform:translate(-50%,-50%);"></div>
  </div>'''

content = content.replace(old_login_bg, new_login_bg, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Backgrounds applied!")
