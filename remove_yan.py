with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    ('Young Africans Network', 'AfriVid'),
    ('youngafricansnetwork.org', 'afrivid.com'),
    ('youngafricansn@gmail.com', 'hello@afrivid.com'),
    ('YAN | youngafricansnetwork.org', 'AfriVid Studio'),
    ('YAN Branded Intro (3s)', 'AfriVid Branded Intro (3s)'),
    ('YAN Branded Outro (3s)', 'AfriVid Branded Outro (3s)'),
    ('YAN Logo', 'AfriVid Logo'),
    ('YAN watermark', 'AfriVid watermark'),
    ('YAN Studio', 'AfriVid Studio'),
    ('YAN branding', 'AfriVid branding'),
    ('YAN intro', 'AfriVid intro'),
    ('YAN outro', 'AfriVid outro'),
    ('© 2026 AfriVid · Built in Africa', '© 2026 AfriVid Studio · Built in Africa'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ YAN references removed!")
