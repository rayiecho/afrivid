with open('index.html', 'r') as f:
    content = f.read()

# Reduce overlay opacity on landing
content = content.replace(
    "background:linear-gradient(135deg,rgba(5,10,20,0.92) 0%,rgba(5,10,20,0.75) 50%,rgba(5,10,20,0.92) 100%)",
    "background:linear-gradient(135deg,rgba(5,10,20,0.65) 0%,rgba(5,10,20,0.45) 50%,rgba(5,10,20,0.65) 100%)"
)

# Increase image opacity on landing
content = content.replace(
    "url('https://images.unsplash.com/photo-1547658719-da2b51169166?w=1920&q=80') center/cover no-repeat;opacity:0.15",
    "url('https://images.unsplash.com/photo-1547658719-da2b51169166?w=1920&q=80') center/cover no-repeat;opacity:0.35"
)
content = content.replace(
    "url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;opacity:0.15",
    "url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;opacity:0.35"
)

# Reduce overlay on login
content = content.replace(
    "background:url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;opacity:0.12",
    "background:url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;opacity:0.25"
)
content = content.replace(
    "background:linear-gradient(135deg,rgba(5,10,20,0.95),rgba(5,10,20,0.88))",
    "background:linear-gradient(135deg,rgba(5,10,20,0.80),rgba(5,10,20,0.70))"
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Overlay reduced!")
