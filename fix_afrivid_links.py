with open('index.html', 'r') as f:
    content = f.read()

# Fix clickable links that redirect to the other platform
content = content.replace(
    '<a href="https://afrivid.com"',
    '<a href="https://rayiecho.github.io/afrivid"'
)
content = content.replace(
    'href="mailto:hello@afrivid.com"',
    'href="mailto:youngafricansn@gmail.com"'
)
content = content.replace(
    'const ADMIN_EMAILS = [\'hello@afrivid.com\'',
    'const ADMIN_EMAILS = [\'youngafricansn@gmail.com\''
)
content = content.replace(
    '🌍 afrivid.com\n\n#YAN #YoungAfricansNetwork #AIVideo',
    '🌍 rayiecho.github.io/afrivid\n\n#AfriVid #AIVideo'
)
content = content.replace(
    '🌍 afrivid.com\n\n#YAN #YoungAfricansNetwork',
    '🌍 rayiecho.github.io/afrivid\n\n#AfriVid'
)
content = content.replace(
    'https://afrivid.com',
    'https://rayiecho.github.io/afrivid'
)
# Fix watermark text on canvas
content = content.replace(
    "ctx.fillText('YAN | afrivid.com'",
    "ctx.fillText('AfriVid Studio'"
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ All afrivid.com links fixed!")
