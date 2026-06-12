import re, subprocess, sys

files = ['create.html', 'edit.html', 'photo.html', 'design.html', 'studio.html']
errors = 0

for fname in files:
    try:
        with open(f'/home/ayiecho/projects/afrivid/{fname}', 'r') as f:
            content = f.read()
    except: continue
    
    # Check non-module scripts
    scripts = re.findall(r'<script(?! type="module")(?! type="application/ld\+json")[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, s in enumerate(scripts):
        if not s.strip(): continue
        r = subprocess.run(['node'], input=s, capture_output=True, text=True)
        if 'SyntaxError' in r.stderr:
            print(f"❌ {fname} Script {i+1}: {r.stderr.splitlines()[0]}")
            errors += 1

    # Check module script
    m = re.search(r'<script type="module">(.*?)</script>', content, re.DOTALL)
    if m:
        # Strip imports for node check
        code = '\n'.join('// '+l if l.strip().startswith('import ') else l for l in m.group(1).split('\n'))
        r = subprocess.run(['node','--check','--input-type=commonjs'], input=code, capture_output=True, text=True)
        if 'SyntaxError' in r.stderr:
            print(f"❌ {fname} Module: {r.stderr.splitlines()[1] if len(r.stderr.splitlines())>1 else r.stderr}")
            errors += 1

if errors == 0:
    print("✅ All files syntax clean!")
else:
    print(f"\n❌ {errors} syntax error(s) found")
    sys.exit(1)
