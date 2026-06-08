with open('index.html', 'r') as f:
    content = f.read()

# Replace hardcoded config with window config
old_config = '''  // Firebase config is safe to be public - security is enforced by Firestore Rules
  const firebaseConfig = {
    apiKey: "AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0",
    authDomain: "afrivid-studio.firebaseapp.com",
    projectId: "afrivid-studio",
    storageBucket: "afrivid-studio.firebasestorage.app",
    messagingSenderId: "957196729758",
    appId: "1:957196729758:web:0a46ed103675f741e22a8f"
  };'''

new_config = '''  const firebaseConfig = window.AFRIVID_CONFIG;'''

content = content.replace(old_config, new_config, 1)

# Add config.js script tag in head before module script
content = content.replace(
    '<script type="module">',
    '<script src="config.js"></script>\n<script type="module">',
    1
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Config hidden!")
