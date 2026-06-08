with open('index.html', 'r') as f:
    content = f.read()

import re

# Extract the three blocks
video_mock = re.search(r'(<div style="position:relative;z-index:1;max-width:900px;margin:0 auto 6rem;padding:0 4rem;">\s*<div style="border-radius:20px.*?</div>\s*</div>)', content, re.DOTALL)
stats = re.search(r'(<div style="position:relative;z-index:1;max-width:900px;margin:0 auto 6rem;padding:0 4rem;">\s*<div style="display:grid;grid-template-columns:repeat\(4,1fr\).*?</div>\s*</div>)', content, re.DOTALL)
nav = re.search(r'(  <!-- MOVED NAV -->.*?</div>\s*\n)', content, re.DOTALL)

if video_mock and stats and nav:
    print("Found all 3 blocks")
    vm = video_mock.group(1)
    st = stats.group(1)
    nv = nav.group(1)
    
    # Remove all three from current positions
    content = content.replace(vm, '___VIDEO___')
    content = content.replace(st, '___STATS___')
    content = content.replace(nv, '___NAV___')
    
    # Put them back in correct order: video → stats → nav
    content = content.replace('___VIDEO___', vm)
    content = content.replace('___STATS___', st)
    content = content.replace('___NAV___', nv)
    print("✅ Order fixed!")
else:
    print(f"video: {bool(video_mock)}, stats: {bool(stats)}, nav: {bool(nav)}")

with open('index.html', 'w') as f:
    f.write(content)
