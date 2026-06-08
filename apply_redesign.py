with open('index.html', 'r') as f:
    content = f.read()

# Replace old landing screen
old_landing = '''<!-- LANDING PAGE -->
<div id="landing-screen">
  <div class="landing-content">
    <div class="landing-logo">
      <img src="https://youngafricansnetwork.org/images/logo.jpeg" alt="YAN" onerror="this.style.display='none'">
    </div>
    <div class="landing-title">AfriVid <span>Studio</span></div>
    <div class="landing-sub">AI VIDEO CREATION PLATFORM — BETA</div>'''

# Find the actual landing content in file
import re
landing_match = re.search(r'<!-- LANDING PAGE -->.*?<!-- LOGIN -->', content, re.DOTALL)
login_match = re.search(r'<!-- LOGIN -->.*?<!-- FEEDBACK', content, re.DOTALL)

if landing_match:
    print(f"Found landing: chars {landing_match.start()} to {landing_match.end()}")
if login_match:
    print(f"Found login: chars {login_match.start()} to {login_match.end()}")

new_landing = '''<!-- LANDING PAGE -->
<div id="landing-screen" style="position:fixed;inset:0;z-index:999;overflow-y:auto;background:#050A14;font-family:'Syne',sans-serif;">

  <div style="position:fixed;inset:0;pointer-events:none;z-index:0;">
    <div style="position:absolute;top:0;left:0;width:50%;height:100%;background:url('https://images.unsplash.com/photo-1547658719-da2b51169166?w=1920&q=80') center/cover no-repeat;opacity:0.35;"></div>
    <div style="position:absolute;top:0;right:0;width:50%;height:100%;background:url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;opacity:0.35;"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(5,10,20,0.65) 0%,rgba(5,10,20,0.45) 50%,rgba(5,10,20,0.65) 100%);"></div>
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(245,166,35,0.04) 1px,transparent 1px);background-size:40px 40px;"></div>
    <div style="position:absolute;top:0;left:50%;width:1px;height:100%;background:linear-gradient(180deg,transparent,rgba(245,166,35,0.15),transparent);"></div>
  </div>

  <style>
    @keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
    @keyframes glow{0%,100%{box-shadow:0 0 20px rgba(245,166,35,0.3)}50%{box-shadow:0 0 40px rgba(245,166,35,0.6)}}
    @keyframes blink{0%,100%{opacity:1}50%{opacity:0.5}}
    .land-btn-primary{background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:1rem 2.5rem;border-radius:12px;font-weight:800;font-size:1rem;cursor:pointer;transition:all 0.3s;font-family:'Syne',sans-serif;}
    .land-btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(245,166,35,0.4);}
    .land-btn-secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.2);padding:1rem 2.5rem;border-radius:12px;font-weight:600;font-size:1rem;cursor:pointer;transition:all 0.3s;font-family:'Syne',sans-serif;}
    .land-btn-secondary:hover{border-color:rgba(245,166,35,0.5);background:rgba(245,166,35,0.05);}
    .feature-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.5rem;transition:all 0.3s;}
    .feature-card:hover{background:rgba(245,166,35,0.05);border-color:rgba(245,166,35,0.2);transform:translateY(-4px);}
    .stat-num{font-size:2.5rem;font-weight:800;background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
  </style>

  <nav style="position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:1.25rem 4rem;background:rgba(5,10,20,0.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.06);">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1rem;color:#050A14;animation:glow 3s ease-in-out infinite;">A</div>
      <span style="font-size:1.1rem;font-weight:800;color:#fff;">AfriVid</span>
      <span style="font-size:1.1rem;font-weight:800;color:#F5A623;">Studio</span>
      <span style="font-size:0.65rem;background:rgba(245,166,35,0.15);border:1px solid rgba(245,166,35,0.3);color:#F5A623;padding:0.2rem 0.6rem;border-radius:50px;font-family:'Space Mono',monospace;letter-spacing:1px;">BETA</span>
    </div>
    <div style="display:flex;gap:2rem;align-items:center;">
      <a href="#features" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;">Features</a>
      <a href="#pricing" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;">Pricing</a>
      <button onclick="showLogin()" style="background:transparent;border:1px solid rgba(245,166,35,0.4);color:#F5A623;padding:0.6rem 1.5rem;border-radius:8px;font-weight:600;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>
      <button onclick="showLogin()" class="land-btn-primary" style="padding:0.6rem 1.5rem;font-size:0.85rem;">Get Started Free →</button>
    </div>
  </nav>

  <div style="position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:7rem 4rem 5rem;text-align:center;">
    <div style="display:inline-flex;align-items:center;gap:0.5rem;background:rgba(245,166,35,0.1);border:1px solid rgba(245,166,35,0.2);border-radius:50px;padding:0.4rem 1rem;margin-bottom:2rem;">
      <span style="width:8px;height:8px;border-radius:50%;background:#F5A623;animation:blink 2s ease-in-out infinite;display:inline-block;"></span>
      <span style="font-size:0.75rem;color:#F5A623;font-family:'Space Mono',monospace;letter-spacing:1px;">AI VIDEO CREATION PLATFORM</span>
    </div>
    <h1 style="font-size:clamp(3rem,7vw,5.5rem);font-weight:800;line-height:1.05;margin-bottom:1.5rem;color:#fff;">
      Create <span style="background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Professional</span><br>
      Videos with <span style="background:linear-gradient(135deg,#F5A623,#74C69D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">AI</span>
    </h1>
    <p style="font-size:1.15rem;color:rgba(255,255,255,0.55);max-width:580px;margin:0 auto 3rem;line-height:1.8;">Type a topic. Get a complete video with AI voice, animated slides, background music and subtitles — in minutes. Built in Africa, for the world.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
      <button onclick="showLogin()" class="land-btn-primary">🚀 Start Creating Free</button>
      <button onclick="document.getElementById('features').scrollIntoView({behavior:'smooth'})" class="land-btn-secondary">See Features ↓</button>
    </div>
    <div style="margin-top:2rem;display:flex;align-items:center;justify-content:center;gap:2rem;">
      <span style="font-size:0.78rem;color:rgba(255,255,255,0.35);font-family:'Space Mono',monospace;">✓ Free during beta</span>
      <span style="font-size:0.78rem;color:rgba(255,255,255,0.35);font-family:'Space Mono',monospace;">✓ No credit card</span>
      <span style="font-size:0.78rem;color:rgba(255,255,255,0.35);font-family:'Space Mono',monospace;">✓ Built for Africa</span>
    </div>
  </div>

  <div style="position:relative;z-index:1;max-width:900px;margin:0 auto 6rem;padding:0 4rem;">
    <div style="border-radius:20px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.02);box-shadow:0 40px 80px rgba(0,0,0,0.4);">
      <div style="background:rgba(255,255,255,0.04);padding:0.75rem 1rem;display:flex;align-items:center;gap:0.5rem;border-bottom:1px solid rgba(255,255,255,0.06);">
        <div style="width:10px;height:10px;border-radius:50%;background:#ff5f56;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#ffbd2e;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#27c93f;"></div>
        <div style="flex:1;background:rgba(255,255,255,0.06);border-radius:4px;padding:0.3rem 1rem;margin:0 1rem;font-size:0.72rem;color:rgba(255,255,255,0.3);font-family:'Space Mono',monospace;">afrivid.studio</div>
      </div>
      <div style="aspect-ratio:16/9;background:linear-gradient(135deg,#0A1628,#0D2B1A);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;padding:2rem;">
        <div style="text-align:center;">
          <div style="font-size:3rem;margin-bottom:0.5rem;">🎬</div>
          <div style="font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:0.25rem;">What is Leadership?</div>
          <div style="font-size:0.82rem;color:#F5A623;font-family:'Space Mono',monospace;">▶ AI voice + music playing...</div>
        </div>
        <div style="position:absolute;top:15%;left:5%;font-size:1.1rem;font-weight:700;color:rgba(255,255,255,0.7);">Leadership</div>
        <div style="position:absolute;top:27%;left:8%;font-size:1.1rem;font-weight:700;color:rgba(255,255,255,0.6);">starts with</div>
        <div style="position:absolute;top:39%;left:5%;font-size:1.2rem;font-weight:700;color:#F5A623;">vision</div>
        <div style="position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#F5A623,#74C69D);"></div>
      </div>
    </div>
  </div>

  <div style="position:relative;z-index:1;max-width:900px;margin:0 auto 6rem;padding:0 4rem;">
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);border-radius:16px;overflow:hidden;">
      <div style="background:#050A14;padding:2rem;text-align:center;"><div class="stat-num">12</div><div style="font-size:0.78rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;margin-top:0.25rem;">AI VOICES</div></div>
      <div style="background:#050A14;padding:2rem;text-align:center;"><div class="stat-num">4</div><div style="font-size:0.78rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;margin-top:0.25rem;">VIDEO STYLES</div></div>
      <div style="background:#050A14;padding:2rem;text-align:center;"><div class="stat-num">20</div><div style="font-size:0.78rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;margin-top:0.25rem;">MIN MAX LENGTH</div></div>
      <div style="background:#050A14;padding:2rem;text-align:center;"><div class="stat-num">$0</div><div style="font-size:0.78rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;margin-top:0.25rem;">DURING BETA</div></div>
    </div>
  </div>

  <div id="features" style="position:relative;z-index:1;max-width:1100px;margin:0 auto 6rem;padding:0 4rem;">
    <div style="text-align:center;margin-bottom:3rem;">
      <div style="font-size:0.72rem;letter-spacing:3px;color:#F5A623;font-family:'Space Mono',monospace;margin-bottom:0.75rem;">EVERYTHING YOU NEED</div>
      <h2 style="font-size:2.5rem;font-weight:800;color:#fff;">One platform. Complete videos.</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;">
      <div class="feature-card"><div style="font-size:2rem;margin-bottom:1rem;">🤖</div><div style="font-weight:700;color:#fff;margin-bottom:0.5rem;">AI Script Generator</div><div style="font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.7;">Type a topic — AI writes a complete script with scenes and voiceover automatically</div></div>
      <div class="feature-card"><div style="font-size:2rem;margin-bottom:1rem;">🎤</div><div style="font-weight:700;color:#fff;margin-bottom:0.5rem;">12 AI Voices</div><div style="font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.7;">Natural speech with male and female voices. No recording equipment needed</div></div>
      <div class="feature-card"><div style="font-size:2rem;margin-bottom:1rem;">🎬</div><div style="font-weight:700;color:#fff;margin-bottom:0.5rem;">4 Video Styles</div><div style="font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.7;">Slides, Whiteboard, Cinematic or Photo Background — each auto-matches your content</div></div>
      <div class="feature-card"><div style="font-size:2rem;margin-bottom:1rem;">✂️</div><div style="font-weight:700;color:#fff;margin-bottom:0.5rem;">Video Enhancer</div><div style="font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.7;">Upload any video — enhance quality, remove noise, trim clips, add subtitles</div></div>
      <div class="feature-card"><div style="font-size:2rem;margin-bottom:1rem;">🖼</div><div style="font-weight:700;color:#fff;margin-bottom:0.5rem;">Photo Editor</div><div style="font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.7;">Edit photos with AI instructions or manual controls. Remove backgrounds instantly</div></div>
      <div class="feature-card"><div style="font-size:2rem;margin-bottom:1rem;">▶️</div><div style="font-weight:700;color:#fff;margin-bottom:0.5rem;">YouTube Upload</div><div style="font-size:0.82rem;color:rgba(255,255,255,0.45);line-height:1.7;">Upload directly to any YouTube channel with one click after generating</div></div>
    </div>
  </div>

  <div id="pricing" style="position:relative;z-index:1;max-width:700px;margin:0 auto 6rem;padding:0 4rem;text-align:center;">
    <div style="font-size:0.72rem;letter-spacing:3px;color:#F5A623;font-family:'Space Mono',monospace;margin-bottom:0.75rem;">PRICING</div>
    <h2 style="font-size:2.5rem;font-weight:800;color:#fff;margin-bottom:3rem;">Free during beta</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;">
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:2rem;text-align:left;">
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;margin-bottom:0.5rem;">BETA</div>
        <div style="font-size:3rem;font-weight:800;color:#fff;margin-bottom:0.25rem;">Free</div>
        <div style="font-size:0.82rem;color:rgba(255,255,255,0.4);margin-bottom:1.5rem;">During testing period</div>
        <div style="font-size:0.82rem;color:rgba(255,255,255,0.6);line-height:2.2;"><div>✓ 10 videos</div><div>✓ All styles</div><div>✓ AI voice</div><div>✓ Video enhancer</div><div>✓ Photo editor</div></div>
        <button onclick="showLogin()" class="land-btn-primary" style="width:100%;margin-top:1.5rem;">Get Started Free</button>
      </div>
      <div style="background:linear-gradient(135deg,rgba(245,166,35,0.08),rgba(116,198,157,0.08));border:1px solid rgba(245,166,35,0.3);border-radius:20px;padding:2rem;text-align:left;">
        <div style="font-size:0.72rem;color:#F5A623;font-family:'Space Mono',monospace;margin-bottom:0.5rem;">COMING SOON</div>
        <div style="font-size:3rem;font-weight:800;color:#fff;margin-bottom:0.25rem;">$5<span style="font-size:1rem;color:rgba(255,255,255,0.4);">/mo</span></div>
        <div style="font-size:0.82rem;color:rgba(255,255,255,0.4);margin-bottom:1.5rem;">After beta period</div>
        <div style="font-size:0.82rem;color:rgba(255,255,255,0.6);line-height:2.2;"><div>✓ Unlimited videos</div><div>✓ Priority voice</div><div>✓ No watermark</div><div>✓ Team access</div><div>✓ Priority support</div></div>
        <button disabled style="width:100%;margin-top:1.5rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.3);padding:0.85rem;border-radius:10px;font-weight:700;cursor:not-allowed;font-family:'Syne',sans-serif;">Coming Soon</button>
      </div>
    </div>
  </div>

  <div style="position:relative;z-index:1;border-top:1px solid rgba(255,255,255,0.06);padding:2rem 4rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.85rem;color:#050A14;">A</div>
      <span style="font-size:0.85rem;color:rgba(255,255,255,0.4);">© 2026 AfriVid Studio · Built in Africa</span>
    </div>
    <a href="mailto:youngafricansn@gmail.com" style="font-size:0.82rem;color:rgba(255,255,255,0.3);text-decoration:none;">Contact</a>
  </div>

</div>

<!-- LOGIN -->'''

new_login = '''<!-- LOGIN -->
<div id="login-screen" style="display:none;position:fixed;inset:0;z-index:1000;align-items:center;justify-content:center;background:#050A14;padding:2rem;">
  <div style="position:fixed;inset:0;pointer-events:none;">
    <div style="position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1920&q=80') center/cover no-repeat;opacity:0.25;"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(5,10,20,0.80),rgba(5,10,20,0.70));"></div>
    <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(245,166,35,0.03) 1px,transparent 1px);background-size:40px 40px;"></div>
    <div style="position:absolute;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(245,166,35,0.06),transparent 70%);top:50%;left:50%;transform:translate(-50%,-50%);"></div>
  </div>
  <div style="position:relative;z-index:1;width:100%;max-width:420px;">
    <div style="text-align:center;margin-bottom:2rem;">
      <div style="width:56px;height:56px;border-radius:14px;background:linear-gradient(135deg,#F5A623,#E8931A);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.5rem;color:#050A14;margin:0 auto 1rem;box-shadow:0 0 30px rgba(245,166,35,0.3);">A</div>
      <div style="font-size:1.5rem;font-weight:800;color:#fff;">AfriVid <span style="color:#F5A623;">Studio</span></div>
      <div style="font-size:0.75rem;color:rgba(255,255,255,0.35);font-family:'Space Mono',monospace;margin-top:0.25rem;letter-spacing:2px;">AI VIDEO CREATION PLATFORM</div>
    </div>
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:2rem;backdrop-filter:blur(20px);">
      <div style="display:flex;background:rgba(255,255,255,0.04);border-radius:10px;padding:3px;margin-bottom:1.75rem;">
        <button id="auth-tab-login" onclick="showAuthTab('login')" style="flex:1;padding:0.65rem;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign In</button>
        <button id="auth-tab-signup" onclick="showAuthTab('signup')" style="flex:1;padding:0.65rem;background:transparent;color:rgba(255,255,255,0.4);border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:0.85rem;font-family:'Syne',sans-serif;">Sign Up</button>
      </div>
      <div id="auth-login-form">
        <div style="margin-bottom:1rem;">
          <label style="font-size:0.75rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;letter-spacing:1px;display:block;margin-bottom:0.5rem;">EMAIL</label>
          <input type="email" id="login-email" style="width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.85rem 1rem;border-radius:10px;font-size:0.9rem;outline:none;font-family:'Syne',sans-serif;box-sizing:border-box;" placeholder="you@example.com" onfocus="this.style.borderColor='rgba(245,166,35,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
        </div>
        <div style="margin-bottom:1.5rem;">
          <label style="font-size:0.75rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;letter-spacing:1px;display:block;margin-bottom:0.5rem;">PASSWORD</label>
          <input type="password" id="login-password" style="width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.85rem 1rem;border-radius:10px;font-size:0.9rem;outline:none;font-family:'Syne',sans-serif;box-sizing:border-box;" placeholder="••••••••" onfocus="this.style.borderColor='rgba(245,166,35,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'" onkeydown="if(event.key==='Enter')signIn()">
        </div>
        <button onclick="signIn()" style="width:100%;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;">Sign In →</button>
      </div>
      <div id="auth-signup-form" style="display:none;">
        <div style="margin-bottom:1rem;">
          <label style="font-size:0.75rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;letter-spacing:1px;display:block;margin-bottom:0.5rem;">FULL NAME</label>
          <input type="text" id="signup-name" style="width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.85rem 1rem;border-radius:10px;font-size:0.9rem;outline:none;font-family:'Syne',sans-serif;box-sizing:border-box;" placeholder="Your full name" onfocus="this.style.borderColor='rgba(245,166,35,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
        </div>
        <div style="margin-bottom:1rem;">
          <label style="font-size:0.75rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;letter-spacing:1px;display:block;margin-bottom:0.5rem;">EMAIL</label>
          <input type="email" id="signup-email" style="width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.85rem 1rem;border-radius:10px;font-size:0.9rem;outline:none;font-family:'Syne',sans-serif;box-sizing:border-box;" placeholder="you@example.com" onfocus="this.style.borderColor='rgba(245,166,35,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'">
        </div>
        <div style="margin-bottom:1.5rem;">
          <label style="font-size:0.75rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;letter-spacing:1px;display:block;margin-bottom:0.5rem;">PASSWORD</label>
          <input type="password" id="signup-password" style="width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.85rem 1rem;border-radius:10px;font-size:0.9rem;outline:none;font-family:'Syne',sans-serif;box-sizing:border-box;" placeholder="Min 6 characters" onfocus="this.style.borderColor='rgba(245,166,35,0.5)'" onblur="this.style.borderColor='rgba(255,255,255,0.1)'" onkeydown="if(event.key==='Enter')signUp()">
        </div>
        <button onclick="signUp()" style="width:100%;background:linear-gradient(135deg,#F5A623,#E8931A);color:#050A14;border:none;padding:0.9rem;border-radius:10px;font-weight:800;font-size:0.95rem;cursor:pointer;font-family:'Syne',sans-serif;">Create Account →</button>
      </div>
      <div class="login-error" id="login-error" style="display:none;margin-top:1rem;padding:0.75rem 1rem;background:rgba(230,51,41,0.1);border:1px solid rgba(230,51,41,0.3);border-radius:8px;font-size:0.82rem;color:#ff6b6b;"></div>
      <div style="text-align:center;margin-top:1.25rem;">
        <button onclick="showLanding()" style="background:none;border:none;color:rgba(255,255,255,0.3);font-size:0.78rem;cursor:pointer;font-family:'Syne',sans-serif;">← Back to home</button>
      </div>
    </div>
    <div style="text-align:center;margin-top:1rem;font-size:0.72rem;color:rgba(255,255,255,0.2);font-family:'Space Mono',monospace;">Beta v1.0 · Free during testing</div>
  </div>
</div>'''

# Replace landing
content = re.sub(r'<!-- LANDING PAGE -->.*?<!-- LOGIN -->', new_landing, content, flags=re.DOTALL)

# Replace login
content = re.sub(r'<!-- LOGIN -->.*?<!-- FEEDBACK', new_login + '\n\n<!-- FEEDBACK', content, flags=re.DOTALL)

# Add showLogin/showLanding functions
content = content.replace(
    'window.showAuthTab = function(tab) {',
    '''window.showLogin = function() {
    document.getElementById('landing-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'flex';
  };
  window.showLanding = function() {
    document.getElementById('landing-screen').style.display = 'flex';
    document.getElementById('login-screen').style.display = 'none';
  };
  window.showAuthTab = function(tab) {'''
)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Full redesign applied!")
