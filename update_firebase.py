with open('index.html', 'r') as f:
    content = f.read()

old_config = '''  const firebaseConfig = {
    apiKey: "AIzaSyCs321YuksiFN3gUql_d880w48pf9Jq0Pk",
    authDomain: "young-africans-network.firebaseapp.com",
    projectId: "young-africans-network",
    storageBucket: "young-africans-network.appspot.com",
    messagingSenderId: "224204618916",
    appId: "1:224204618916:web:8ddfd36c6f112b4912fa31"
  };'''

new_config = '''  const firebaseConfig = {
    apiKey: "AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0",
    authDomain: "afrivid-studio.firebaseapp.com",
    projectId: "afrivid-studio",
    storageBucket: "afrivid-studio.firebasestorage.app",
    messagingSenderId: "957196729758",
    appId: "1:957196729758:web:0a46ed103675f741e22a8f"
  };'''

content = content.replace(old_config, new_config)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Firebase config updated to AfriVid!")
