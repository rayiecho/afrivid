with open('index.html', 'r') as f:
    content = f.read()

# 1. Add sendEmailVerification to imports
content = content.replace(
    "import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut, updateProfile } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';",
    "import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut, updateProfile, sendEmailVerification } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';"
)

# 2. Update onAuthStateChanged to check email verification
old_auth_state = '''  onAuthStateChanged(auth, async (user) => {
    if (user) {
      currentUser = user;
      await loadUserProfile(user);
      const landingEl = document.getElementById('landing-screen');
      const loginEl = document.getElementById('login-screen');
      const appEl = document.getElementById('app');
      if (landingEl) landingEl.style.display = 'none';
      if (loginEl) loginEl.style.display = 'none';
      if (appEl) appEl.style.display = 'block';
      updateUserUI();
      console.log("Logged in as:", user.email);
      console.log("Is admin:", ADMIN_EMAILS.includes(user.email));
      if (ADMIN_EMAILS.includes(user.email)) {
        setTimeout(() => showAdminTab(), 500);
      }
    } else {
      currentUser = null;
      const landingEl = document.getElementById('landing-screen');
      const loginEl = document.getElementById('login-screen');
      const appEl = document.getElementById('app');
      if (landingEl) landingEl.style.display = 'flex';
      if (loginEl) loginEl.style.display = 'none';
      if (appEl) appEl.style.display = 'none';
    }
  });'''

new_auth_state = '''  onAuthStateChanged(auth, async (user) => {
    if (user) {
      // Check email verification
      if (!user.emailVerified && !ADMIN_EMAILS.includes(user.email)) {
        // Show verification screen
        document.getElementById('landing-screen').style.display = 'none';
        document.getElementById('login-screen').style.display = 'none';
        const appEl = document.getElementById('app');
        if (appEl) appEl.style.display = 'none';
        showVerificationScreen(user);
        return;
      }
      currentUser = user;
      await loadUserProfile(user);
      const landingEl = document.getElementById('landing-screen');
      const loginEl = document.getElementById('login-screen');
      const verifyEl = document.getElementById('verify-screen');
      const appEl = document.getElementById('app');
      if (landingEl) landingEl.style.display = 'none';
      if (loginEl) loginEl.style.display = 'none';
      if (verifyEl) verifyEl.style.display = 'none';
      if (appEl) appEl.style.display = 'block';
      updateUserUI();
      if (ADMIN_EMAILS.includes(user.email)) setTimeout(() => showAdminTab(), 500);
    } else {
      currentUser = null;
      const landingEl = document.getElementById('landing-screen');
      const loginEl = document.getElementById('login-screen');
      const verifyEl = document.getElementById('verify-screen');
      const appEl = document.getElementById('app');
      if (landingEl) landingEl.style.display = 'flex';
      if (loginEl) loginEl.style.display = 'none';
      if (verifyEl) verifyEl.style.display = 'none';
      if (appEl) appEl.style.display = 'none';
    }
  });

  function showVerificationScreen(user) {
    let verifyEl = document.getElementById('verify-screen');
    if (!verifyEl) {
      verifyEl = document.createElement('div');
      verifyEl.id = 'verify-screen';
      document.body.appendChild(verifyEl);
    }
    verifyEl.style.cssText = 'position:fixed;inset:0;z-index:1001;display:flex;align-items:center;justify-content:center;background:#050A14;padding:2rem;';
    verifyEl.innerHTML = `
      <div style="width:100%;max-width:420px;text-align:center;">
        <div style="width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-size:2rem;margin:0 auto 1.5rem;box-shadow:0 0 30px rgba(245,166,35,0.3);">📧</div>
        <div style="font-size:1.5rem;font-weight:800;color:#fff;margin-bottom:0.75rem;">Verify Your Email</div>
        <div style="font-size:0.88rem;color:rgba(255,255,255,0.5);line-height:1.7;margin-bottom:2rem;">We sent a verification link to<br><strong style="color:#F5A623;">${user.email}</strong><br>Click the link in your email to access AfriVid Studio.</div>
        <div style="display:flex;flex-direction:column;gap:0.75rem;">
          <button onclick="checkVerification()" style="background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;">✓ I've Verified My Email</button>
          <button onclick="resendVerification()" style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.6);padding:0.75rem;border-radius:10px;font-size:0.85rem;cursor:pointer;font-family:'Syne',sans-serif;">↺ Resend Verification Email</button>
          <button onclick="logout()" style="background:none;border:none;color:rgba(255,255,255,0.3);font-size:0.78rem;cursor:pointer;font-family:'Syne',sans-serif;margin-top:0.5rem;">← Sign out and use different email</button>
        </div>
        <div id="verify-msg" style="margin-top:1rem;font-size:0.78rem;font-family:'Space Mono',monospace;color:rgba(255,255,255,0.4);"></div>
      </div>
    `;
  }'''

content = content.replace(old_auth_state, new_auth_state, 1)

# 3. Update signUp to send verification email
old_signup = '''  window.signUp = async function() {
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    if (!name || !email || !password) { alert('Please fill all fields'); return; }
    try {
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(cred.user, { displayName: name });
    } catch(e) {
      document.getElementById('login-error').style.display = 'block';
      document.getElementById('login-error').textContent = '⚠ ' + e.message.replace('Firebase: ', '');
    }
  };'''

new_signup = '''  window.signUp = async function() {
    const name = document.getElementById('signup-name').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    if (!name || !email || !password) {
      document.getElementById('login-error').style.display = 'block';
      document.getElementById('login-error').textContent = '⚠ Please fill all fields';
      return;
    }
    if (password.length < 6) {
      document.getElementById('login-error').style.display = 'block';
      document.getElementById('login-error').textContent = '⚠ Password must be at least 6 characters';
      return;
    }
    try {
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(cred.user, { displayName: name });
      await sendEmailVerification(cred.user);
      // Show verification screen immediately
      showVerificationScreen(cred.user);
      document.getElementById('login-screen').style.display = 'none';
    } catch(e) {
      document.getElementById('login-error').style.display = 'block';
      document.getElementById('login-error').textContent = '⚠ ' + e.message.replace('Firebase: ', '').replace('Error (', '').replace(').', '');
    }
  };

  window.checkVerification = async function() {
    const msg = document.getElementById('verify-msg');
    try {
      await auth.currentUser.reload();
      if (auth.currentUser.emailVerified) {
        msg.textContent = '✅ Verified! Loading studio...';
        msg.style.color = '#74C69D';
        // Trigger auth state change
        const user = auth.currentUser;
        currentUser = user;
        await loadUserProfile(user);
        document.getElementById('verify-screen').style.display = 'none';
        document.getElementById('app').style.display = 'block';
        updateUserUI();
        if (ADMIN_EMAILS.includes(user.email)) setTimeout(() => showAdminTab(), 500);
      } else {
        msg.textContent = '⚠ Email not verified yet. Please check your inbox.';
        msg.style.color = '#F5A623';
      }
    } catch(e) {
      if (msg) msg.textContent = '✗ Error: ' + e.message;
    }
  };

  window.resendVerification = async function() {
    const msg = document.getElementById('verify-msg');
    try {
      await sendEmailVerification(auth.currentUser);
      msg.textContent = '✅ Verification email sent! Check your inbox.';
      msg.style.color = '#74C69D';
    } catch(e) {
      msg.textContent = '✗ ' + e.message;
      msg.style.color = '#E63329';
    }
  };'''

content = content.replace(old_signup, new_signup, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Email verification added!")
