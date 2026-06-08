with open('index.html', 'r') as f:
    content = f.read()

replacements = [
    ('young-africans-network.firebaseapp.com', 'afrivid-studio.firebaseapp.com'),
    ('young-africans-network', 'afrivid-studio'),
    ('young-africans-network.appspot.com', 'afrivid-studio.firebasestorage.app'),
    ('"224204618916"', '"957196729758"'),
    ('1:224204618916:web:8ddfd36c6f112b4912fa31', '1:957196729758:web:0a46ed103675f741e22a8f'),
    ('AIzaSyCs321YuksiFN3gUql_d880w48pf9Jq0Pk', 'AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0'),
    ("'youngafricansn@gmail.com', 'r.ayiecho@alustudent.com'", "'youngafricansn@gmail.com', 'r.ayiecho@alustudent.com'"),
    ('YAN Studio', 'AfriVid Studio'),
    ('YAN <span>Studio</span>', 'AfriVid <span>Studio</span>'),
    ('YAN <span style="color:var(--gold);">Studio</span>', 'AfriVid <span style="color:var(--gold);">Studio</span>'),
    ('Young Africans Network', 'AfriVid'),
    ('youngafricansnetwork.org', 'rayiecho.github.io/afrivid'),
    ('<title>AfriVid Studio — AI Video Generator</title>', '<title>AfriVid Studio — AI Video Creator</title>'),
    ('BUILDING THE FUTURE, TOGETHER', 'CREATE. ENHANCE. SHARE.'),
    ('yan-ai-worker.youngafricansn.workers.dev', 'yan-ai-worker.youngafricansn.workers.dev'),
    ('yan-studio-worker.youngafricansn.workers.dev', 'yan-studio-worker.youngafricansn.workers.dev'),
    ('// AI VIDEO GENERATION SYSTEM — BETA', '// AI VIDEO CREATION PLATFORM — BETA'),
    ('Beta v1.0 — Free during testing period', 'Beta v1.0 · Free during testing · afrivid'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Full rebrand complete!")
