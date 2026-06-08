with open('index.html', 'r') as f:
    content = f.read()

# Replace local image paths with direct Unsplash URLs
content = content.replace(
    "url('images/bg-workspace.jpg')",
    "url('https://images.unsplash.com/photo-1547658719-da2b51169166?w=1920&q=80')"
)
content = content.replace(
    "url('images/bg-editor.jpg')",
    "url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80')"
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Unsplash backgrounds applied!")
