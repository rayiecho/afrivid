with open('index.html', 'r') as f:
    content = f.read()

content = content.replace(
    '''Create <span style="background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Professional</span><br>
      Videos with <span style="background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AI</span>''',
    '''Professional <span style="background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Video Creator</span><br>
      <span style="background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">&</span> Editor'''
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Hero text updated!")
