with open('index.html', 'r') as f:
    content = f.read()

# Fix getDoc for studio_config - it fails if collection doesn't exist
old_config = '''      const [usersSnap, videosSnap, feedbackSnap, configSnap] = await Promise.all([
        getDocs(query(collection(db, 'studio_users'), orderBy('videosGenerated', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_videos'), orderBy('createdAt', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_feedback'), orderBy('createdAt', 'desc'), limit(50))),
        getDoc(doc(db, 'studio_config', 'settings')).catch(() => null)
      ]);'''

new_config = '''      const [usersSnap, videosSnap, feedbackSnap] = await Promise.all([
        getDocs(query(collection(db, 'studio_users'), orderBy('videosGenerated', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_videos'), orderBy('createdAt', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_feedback'), orderBy('createdAt', 'desc'), limit(50)))
      ]);
      let configSnap = null;
      try { configSnap = await getDoc(doc(db, 'studio_config', 'settings')); } catch(e) {}'''

content = content.replace(old_config, new_config, 1)

# Also make sure admin section becomes active correctly
old_sections = '''    ['create','enhance','library','photo'].forEach(t => {
      const s = document.getElementById('section-'+t);
      if(s) s.classList.remove('active');
    });
    ['create','enhance','library','photo','admin'].forEach(t => {
      const b = document.getElementById('sidebar-'+t);
      if(b) b.classList.toggle('active', t === 'admin');
    });'''

new_sections = '''    ['create','enhance','library','photo'].forEach(t => {
      const s = document.getElementById('section-'+t);
      if(s) { s.classList.remove('active'); s.style.display = 'none'; }
    });
    ['create','enhance','library','photo','admin'].forEach(t => {
      const b = document.getElementById('sidebar-'+t);
      if(b) b.classList.toggle('active', t === 'admin');
    });'''

content = content.replace(old_sections, new_sections, 1)

# Make admin section visible
old_admin_section = '''    let adminSection = document.getElementById('section-admin');
    if (!adminSection) {
      adminSection = document.createElement('div');
      adminSection.className = 'main-section active';
      adminSection.id = 'section-admin';
      document.querySelector('.main').appendChild(adminSection);
    } else {
      adminSection.className = 'main-section active';
    }'''

new_admin_section = '''    let adminSection = document.getElementById('section-admin');
    if (!adminSection) {
      adminSection = document.createElement('div');
      adminSection.id = 'section-admin';
      document.querySelector('.main').appendChild(adminSection);
    }
    adminSection.style.display = 'block';
    adminSection.className = 'main-section active';'''

content = content.replace(old_admin_section, new_admin_section, 1)

# Update switchTab to show/hide properly
old_switch_hide = "    const sec = document.getElementById('section-'+t);\n    if (sec) sec.classList.toggle('active', t === tab);"
new_switch_hide = "    const sec = document.getElementById('section-'+t);\n    if (sec) { sec.classList.toggle('active', t === tab); sec.style.display = t === tab ? 'block' : 'none'; }"
content = content.replace(old_switch_hide, new_switch_hide, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Admin render fixed!")
