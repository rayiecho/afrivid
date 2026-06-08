with open('index.html', 'r') as f:
    content = f.read()

content = content.replace(
    '''      currentUser = null;
      document.getElementById('landing-screen').style.display = 'flex';
      document.getElementById('login-screen').style.display = 'none';
      document.getElementById('app').style.display = 'none';''',
    '''      currentUser = null;
      const landingEl = document.getElementById('landing-screen');
      const loginEl = document.getElementById('login-screen');
      const appEl = document.getElementById('app');
      if (landingEl) landingEl.style.display = 'flex';
      if (loginEl) loginEl.style.display = 'none';
      if (appEl) appEl.style.display = 'none';'''
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Null error fixed!")
