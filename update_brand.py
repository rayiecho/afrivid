with open('index.html', 'r') as f:
    content = f.read()

# Update CSS variables with refined brand colors
old_vars = ''':root {
  --navy: #0A1628;
  --navy2: #0D1F35;
  --navy3: #112540;
  --gold: #F5A623;
  --green: #2D8A5E;
  --red: #E63329;
  --white: #F8F9FC;
  --muted: #6B7A99;
  --border: rgba(255,255,255,0.08);
  --border2: rgba(255,255,255,0.06);
  --font-display: 'Syne', sans-serif;
  --font-mono: 'Space Mono', monospace;
}'''

new_vars = ''':root {
  /* AfriVid Studio — Brand Colors */
  --navy: #050A14;        /* Midnight — deep, premium */
  --navy2: #0A1628;       /* Deep Navy */
  --navy3: #0D1F35;       /* Card background */
  --gold: #F5A623;        /* African Gold — primary */
  --gold2: #E8931A;       /* Sunset Orange — gradient end */
  --green: #74C69D;       /* Savanna Green — accent */
  --green2: #2D8A5E;      /* Deep Green */
  --red: #E63329;         /* Alert red */
  --white: #F8F9FC;       /* Off white */
  --muted: #6B7A99;       /* Muted text */
  --border: rgba(245,166,35,0.08);   /* Gold-tinted border */
  --border2: rgba(255,255,255,0.06); /* Subtle border */
  --font-display: 'Syne', sans-serif;
  --font-mono: 'Space Mono', monospace;

  /* Gradients */
  --gradient-gold: linear-gradient(135deg, #F5A623, #E8931A);
  --gradient-green: linear-gradient(135deg, #74C69D, #2D8A5E);
  --gradient-dark: linear-gradient(135deg, #050A14, #0D1F35);
}'''

content = content.replace(old_vars, new_vars, 1)

# Update tagline in landing hero
content = content.replace(
    '<span style="font-size:0.75rem;color:#F5A623;font-family:\'Space Mono\',monospace;letter-spacing:1px;">AI VIDEO CREATION PLATFORM</span>',
    '<span style="font-size:0.75rem;color:#F5A623;font-family:\'Space Mono\',monospace;letter-spacing:1px;">AFRICA\'S FIRST AI VIDEO CREATION SUITE</span>'
)

# Update subtitle text
content = content.replace(
    'Type a topic. Get a complete video with AI voice, animated slides, background music and subtitles — in minutes. Built in Africa, for the world.',
    'Africa\'s first all-in-one AI video creation suite. Generate, edit, and enhance professional videos in minutes — built by Africans, for the world.'
)

# Update footer tagline
content = content.replace(
    '© 2026 AfriVid Studio · Built in Africa',
    '© 2026 AfriVid Studio · Africa\'s First AI Video Suite'
)

# Update login screen tagline
content = content.replace(
    '<div style="font-size:0.75rem;color:rgba(255,255,255,0.35);font-family:\'Space Mono\',monospace;margin-top:0.25rem;letter-spacing:2px;">AI VIDEO CREATION PLATFORM</div>',
    '<div style="font-size:0.75rem;color:rgba(255,255,255,0.35);font-family:\'Space Mono\',monospace;margin-top:0.25rem;letter-spacing:2px;">AFRICA\'S FIRST AI VIDEO SUITE</div>'
)

# Update sidebar logo area
content = content.replace(
    '<div class="sidebar-logo-text">AfriVid <span>Studio</span></div>',
    '<div><div class="sidebar-logo-text">AfriVid <span>Studio</span></div><div style="font-size:0.55rem;color:rgba(245,166,35,0.6);font-family:var(--font-mono);letter-spacing:1px;margin-top:1px;">AFRICA\'S FIRST AI VIDEO SUITE</div></div>'
)

# Enhance gold gradient buttons
content = content.replace(
    'background:linear-gradient(135deg,#F5A623,#E8931A)',
    'background:linear-gradient(135deg,#F5A623,#E8931A)'
)

# Update body background
content = content.replace(
    'background-color: #0A1628;',
    'background-color: #050A14;'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Brand updated!")
