with open('index.html', 'r') as f:
    content = f.read()

# Remove the powered by line
content = content.replace(
    '''    <div style="display:inline-flex;align-items:center;gap:0.5rem;background:rgba(245,166,35,0.1);border:1px solid rgba(245,166,35,0.2);border-radius:50px;padding:0.4rem 1rem;margin-bottom:2rem;animation:fadeUp 0.6s ease forwards;">
      <span style="width:8px;height:8px;border-radius:50%;background:#F5A623;animation:pulse 2s ease-in-out infinite;display:inline-block;"></span>
      <span style="font-size:0.75rem;color:#F5A623;font-family:'Space Mono',monospace;letter-spacing:1px;">POWERED BY CLAUDE AI + CLOUDFLARE</span>
    </div>''',
    '''    <div style="display:inline-flex;align-items:center;gap:0.5rem;background:rgba(245,166,35,0.1);border:1px solid rgba(245,166,35,0.2);border-radius:50px;padding:0.4rem 1rem;margin-bottom:2rem;animation:fadeUp 0.6s ease forwards;">
      <span style="width:8px;height:8px;border-radius:50%;background:#F5A623;animation:pulse 2s ease-in-out infinite;display:inline-block;"></span>
      <span style="font-size:0.75rem;color:#F5A623;font-family:'Space Mono',monospace;letter-spacing:1px;">AI VIDEO CREATION PLATFORM</span>
    </div>'''
)

# Also remove from login screen
content = content.replace(
    'Beta v1.0 · Free during testing · afrivid.com',
    'Beta v1.0 · Free during testing'
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Removed tech stack references!")
