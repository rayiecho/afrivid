with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    ("'YAN@Admin2026'", "'AfriVid@Admin2026'"),
    ("ctx.fillText('YAN STUDIO'", "ctx.fillText('AfriVid Studio'"),
    ("ctx.fillText('YAN'", "ctx.fillText('AfriVid'"),
    ('`YAN-${entry.title', '`AfriVid-${entry.title'),
    ('`YAN-Enhanced-', '`AfriVid-Enhanced-'),
    ('`YAN-Photo-', '`AfriVid-Photo-'),
    ("tags: ['YAN', 'YoungAfricansNetwork', 'Africa', 'Education']", "tags: ['AfriVid', 'AfriVidStudio', 'Africa', 'AIVideo']"),
    ('- YAN Program:', '- Program:'),
    ('href="mailto:youngafricansn@gmail.com"', 'href="mailto:youngafricansn@gmail.com"'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Final YAN cleanup done!")
