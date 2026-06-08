with open('index.html', 'r') as f:
    content = f.read()

# 1. Make Sign Up the default tab (swap active state)
content = content.replace(
    '''<button id="auth-tab-login" onclick="showAuthTab('login')" style="flex:1;padding:0.65rem;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>
        <button id="auth-tab-signup" onclick="showAuthTab('signup')" style="flex:1;padding:0.65rem;background:transparent;color:rgba(255,255,255,0.4);border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign Up</button>''',
    '''<button id="auth-tab-login" onclick="showAuthTab('login')" style="flex:1;padding:0.65rem;background:transparent;color:rgba(255,255,255,0.4);border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>
        <button id="auth-tab-signup" onclick="showAuthTab('signup')" style="flex:1;padding:0.65rem;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign Up</button>'''
)

# 2. Make Sign Up form visible by default, Sign In hidden
content = content.replace(
    '<div id="auth-login-form">',
    '<div id="auth-login-form" style="display:none;">'
)
content = content.replace(
    '<div id="auth-signup-form" style="display:none;">',
    '<div id="auth-signup-form">'
)

# 3. Update showAuthTab to handle new default
content = content.replace(
    '''  window.showAuthTab = function(tab) {
    document.getElementById('auth-login-form').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('auth-signup-form').style.display = tab === 'signup' ? 'block' : 'none';
    document.getElementById('auth-tab-login').style.background = tab === 'login' ? 'var(--gold)' : 'transparent';
    document.getElementById('auth-tab-login').style.color = tab === 'login' ? 'var(--navy)' : 'var(--muted)';
    document.getElementById('auth-tab-signup').style.background = tab === 'signup' ? 'var(--gold)' : 'transparent';
    document.getElementById('auth-tab-signup').style.color = tab === 'signup' ? 'var(--navy)' : 'var(--muted)';
  };''',
    '''  window.showAuthTab = function(tab) {
    document.getElementById('auth-login-form').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('auth-signup-form').style.display = tab === 'signup' ? 'block' : 'none';
    document.getElementById('auth-tab-login').style.background = tab === 'login' ? 'linear-gradient(135deg,#F5A623,#E8931A)' : 'transparent';
    document.getElementById('auth-tab-login').style.color = tab === 'login' ? '#050A14' : 'rgba(255,255,255,0.4)';
    document.getElementById('auth-tab-signup').style.background = tab === 'signup' ? 'linear-gradient(135deg,#F5A623,#E8931A)' : 'transparent';
    document.getElementById('auth-tab-signup').style.color = tab === 'signup' ? '#050A14' : 'rgba(255,255,255,0.4)';
    document.getElementById('login-error').style.display = 'none';
  };'''
)

# 4. Update Get Started Free button to go to signup tab
content = content.replace(
    "window.showLogin = function() {\n    document.getElementById('landing-screen').style.display = 'none';\n    document.getElementById('login-screen').style.display = 'flex';\n  };",
    "window.showLogin = function(tab) {\n    document.getElementById('landing-screen').style.display = 'none';\n    document.getElementById('login-screen').style.display = 'flex';\n    showAuthTab(tab || 'signup');\n  };"
)

# 5. Sign In button on landing goes to login tab
content = content.replace(
    '''<button onclick="showLogin()" style="background:transparent;border:1px solid rgba(245,166,35,0.4);color:#F5A623;padding:0.6rem 1.5rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>''',
    '''<button onclick="showLogin('login')" style="background:transparent;border:1px solid rgba(245,166,35,0.4);color:#F5A623;padding:0.6rem 1.5rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>'''
)

# 6. Add helpful hint below sign in form
content = content.replace(
    "      <button onclick=\"signIn()\" style=\"width:100%;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;\">Sign In →</button>\n      </div>",
    "      <button onclick=\"signIn()\" style=\"width:100%;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;\">Sign In →</button>\n      <div style=\"text-align:center;margin-top:1rem;font-size:0.78rem;color:rgba(255,255,255,0.35);\">Don't have an account? <button onclick=\"showAuthTab('signup')\" style=\"background:none;border:none;color:#F5A623;cursor:pointer;font-size:0.78rem;font-family:'Syne',sans-serif;font-weight:600;\">Sign Up Free →</button></div>\n      </div>"
)

# 7. Add hint below sign up form
content = content.replace(
    "      <button onclick=\"signUp()\" style=\"width:100%;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;\">Create Account →</button>\n      </div>",
    "      <button onclick=\"signUp()\" style=\"width:100%;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;\">Create Account →</button>\n      <div style=\"text-align:center;margin-top:1rem;font-size:0.78rem;color:rgba(255,255,255,0.35);\">Already have an account? <button onclick=\"showAuthTab('login')\" style=\"background:none;border:none;color:#F5A623;cursor:pointer;font-size:0.78rem;font-family:'Syne',sans-serif;font-weight:600;\">Sign In →</button></div>\n      </div>"
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Auth flow fixed - Sign Up first!")
