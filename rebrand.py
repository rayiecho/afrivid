with open('index.html', 'r') as f:
    content = f.read()

# Rebrand YAN Studio to AfriVid Studio
replacements = [
    ('YAN <span>Studio</span>', 'AfriVid <span>Studio</span>'),
    ('YAN <span style="color:var(--gold);">Studio</span>', 'AfriVid <span style="color:var(--gold);">Studio</span>'),
    ('YAN Studio — AI Video Generator', 'AfriVid Studio — AI Video Generator'),
    ('YAN Studio Beta', 'AfriVid Studio Beta'),
    ('// AI VIDEO GENERATION SYSTEM — BETA', '// AI VIDEO CREATION PLATFORM — BETA'),
    ('Beta v1.0 — Free during testing period', 'Beta v1.0 — Free during testing period · afrivid.com'),
    ('<title>YAN Studio — AI Video Generator</title>', '<title>AfriVid Studio — AI Video Generator</title>'),
    ('youngafricansnetwork.org/yan-studio.html', 'afrivid.com'),
    ('youngafricansnetwork.org/images/logo.jpeg', 'https://youngafricansnetwork.org/images/logo.jpeg'),
    ('BUILDING THE FUTURE, TOGETHER', 'CREATE. ENHANCE. SHARE.'),
    ('Young Africans Network', 'AfriVid Studio'),
    ('youngafricansnetwork.org', 'afrivid.com'),
    ('© 2026 Young Africans Network · YAN Studio Beta', '© 2026 AfriVid Studio · Built in Africa'),
    ('Built in Africa. Built for the World.', 'Built in Africa. Built for the World.'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Update page description
content = content.replace(
    'Generate Professional<br><span style="color:var(--gold);">African Videos</span> with AI',
    'Generate Professional<br><span style="color:var(--gold);">Videos</span> with AI'
)

content = content.replace(
    'No camera. No editing. No cost.',
    'No camera. No editing. No cost. Built in Africa.'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Rebranded to AfriVid Studio!")
