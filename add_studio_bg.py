with open('index.html', 'r') as f:
    content = f.read()

# Add background to app layout
content = content.replace(
    '.app-layout { display:flex; min-height:100vh; background:var(--navy); }',
    '''.app-layout { 
    display:flex; 
    min-height:100vh; 
    background:var(--navy);
    position:relative;
  }
  .app-layout::before {
    content:'';
    position:fixed;
    inset:0;
    background:
      url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;
    opacity:0.04;
    pointer-events:none;
    z-index:0;
  }
  .app-layout::after {
    content:'';
    position:fixed;
    inset:0;
    background:radial-gradient(ellipse at top right, rgba(245,166,35,0.04) 0%, transparent 60%),
               radial-gradient(ellipse at bottom left, rgba(27,67,50,0.06) 0%, transparent 60%);
    pointer-events:none;
    z-index:0;
  }
  .sidebar { z-index:100; }
  .app-content { position:relative; z-index:1; }'''
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Studio background added!")
