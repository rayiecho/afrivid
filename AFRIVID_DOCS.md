# AfriVid Studio — Complete Documentation
*Generated: June 13, 2026*

---

## 1. PLATFORM OVERVIEW

**Name:** AfriVid Studio  
**Tagline:** Africa's First AI Video Creation Platform  
**URL:** https://afrivid.studio  
**GitHub:** github.com/rayiecho/afrivid (branch: master)  
**Built by:** Regan Odhiambo Ayiecho  
**Status:** Live — Launched June 13, 2026  

---

## 2. PAGES & FEATURES

| Page | URL | Purpose |
|------|-----|---------|
| Landing | index.html | Homepage, signup, login |
| Video Creator | create.html | AI video generation from text |
| AI Video Editor | aieditor.html | AI-powered video editing |
| Video Editor | edit.html | Manual video editing |
| Photo Editor | photo.html | AI photo editing |
| Design Studio | design.html | AI graphic design |
| My Studio | studio.html | Personal content library |
| Admin Panel | admin.html | Platform management |
| Pricing | pricing.html | Free vs Pro plans |
| Contact | contact.html | Support & feedback |
| Privacy Policy | privacy.html | Legal |
| Terms of Service | terms.html | Legal |
| 404 | 404.html | Error page |

---

## 3. AI FEATURES

### Video Creator (create.html)
- AI script generation via Claude
- Text-to-Speech (14 voices, Google TTS)
- Slide-based and split-flow visual styles
- AI scene image generation (Cloudflare Flux)
- Background music (5 styles, Web Audio API)
- Multiple aspect ratios (16:9, 9:16, 1:1, 4:3)
- Download as WebM + Real MP4 (FFmpeg.wasm)
- Save to Studio

### AI Video Editor (aieditor.html)
- Natural language prompt editing
- Viral Clips Generator (AI scores clips)
- Highlight Reel (30s/60s/90s)
- Voice Translation (Swahili, French, Yoruba, Hausa, Amharic, Portuguese)
- Remove Silences (Web Audio API)
- Background Music + auto-duck
- Auto Captions (Whisper + karaoke)
- Noise Removal
- Thumbnail Generator
- Brand Kit
- Auto-download after export

### Video Editor (edit.html)
- Trim, enhance quality
- Audio adjustment
- CC Captions
- Combine multiple videos
- CapCut-style crop
- Export MP4/WebM

### Photo Editor (photo.html)
- AI background removal (MediaPipe)
- Smart AI edit instructions
- Filters and presets
- Flag overlays (African countries)
- Frames and borders
- Watermark
- Passport photo format

### Design Studio (design.html)
- AI design generation from prompt
- Text editor (inline)
- CapCut-style crop
- Canvas resize
- Download PNG

---

## 4. TECHNICAL INFRASTRUCTURE

### Hosting & Domain
- **Hosting:** GitHub Pages (free)
- **CDN/DNS:** Cloudflare (free)
- **Domain:** afrivid.studio (~$20/year)
- **Repository:** github.com/rayiecho/afrivid

### Backend
- **Authentication:** Firebase Auth
- **Database:** Firestore
- **Collections:**
  - studio_users — user profiles, plans, usage
  - studio_videos — saved videos
  - feedback — user feedback
  - afribrain_data — transcription dataset

### API Services
- **Cloudflare Worker:** afrivid-tts.mathsai666.workers.dev
  - /tts → Google Text-to-Speech
  - /transcribe → OpenAI Whisper
  - /generate-image → Cloudflare Flux AI
- **YAN Worker:** yan-ai-worker.youngafricansn.workers.dev
  - Claude API proxy (Haiku model)
- **Cloudflare R2:** 225 background images (15 categories × 15)

### AI Models
| Model | Provider | Used For |
|-------|----------|---------|
| Claude Haiku | Anthropic | Scripts, AI edit, chatbot |
| Google TTS | Google | Voice generation |
| Whisper | OpenAI/Cloudflare | Transcription |
| Flux AI | Cloudflare | Image generation |
| MediaPipe | Google | Background removal |

### Browser Technologies
- HTML5 Canvas API — video rendering
- MediaRecorder API — video capture
- Web Audio API — music + noise removal
- FFmpeg.wasm — MP4 conversion
- Service Worker — PWA offline

---

## 5. FIREBASE CONFIGURATION

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0",
  authDomain: "afrivid-studio.firebaseapp.com",
  projectId: "afrivid-studio",
  storageBucket: "afrivid-studio.appspot.com",
  messagingSenderId: "957196729758",
  appId: "1:957196729758:web:0a46ed103675f741e22a8f"
};
```

**Admin Account:** afrividstudio@gmail.com  
**Admin Panel:** afrivid.studio/admin.html  
**Secret Admin Link:** Tiny dot (·) in studio.html footer  

---

## 6. PRICING & PLANS

| Feature | Free | Pro ($5/month) |
|---------|------|----------------|
| Videos/month | 3 | Unlimited |
| Max video length | 2 min | 20 min |
| AI Editor sessions | 3/month | Unlimited |
| Voice translations | 3/month | Unlimited |
| Captions | 3/week | Unlimited |
| Watermark | Yes | No |
| AI Chatbot | No | Yes |
| Support | Email | Priority |

**Payment:** Manual via email (afrividstudio@gmail.com)  
**Future:** Flutterwave (M-Pesa + Card)  

---

## 7. SOCIAL MEDIA & PRESENCE

| Platform | Handle/URL |
|----------|-----------|
| Website | afrivid.studio |
| Facebook | facebook.com/profile.php?id=61590870207039 |
| Instagram | @afrividstudio |
| TikTok | @afrividstudio |
| YouTube | @AfrividStudio |
| Twitter/X | @afrividstudio |
| Wikidata | Q140194899 |
| GitHub | github.com/rayiecho/afrivid |

---

## 8. SEO & DISCOVERY

- **Google Search Console:** Submitted
- **Sitemap:** afrivid.studio/sitemap.xml (11 pages)
- **Schema:** JSON-LD with Wikidata link
- **OG Images:** afrivid.studio/images/logo.png
- **PWA:** Installable as app (manifest.json + sw.js)
- **Wikidata:** Q140194899

---

## 9. COSTS (Monthly at 100 free users)

| Service | Cost |
|---------|------|
| GitHub Pages | $0 |
| Firebase | $0 |
| Cloudflare | $0 |
| Google TTS | $0 |
| Claude API | ~$0.10 |
| Domain | $1.67 |
| **TOTAL** | **~$2/month** |

**Break-even:** 9 Pro users × $5 = $45/month

---

## 10. AAFRIBRAIN VISION

Every video processed by AfriVid contributes to AfriBrain:
- Transcriptions saved to `afribrain_data` Firestore collection
- Target: 1M African language words
- Goal: Africa's first multilingual AI model
- Languages: Swahili, Yoruba, Hausa, Amharic, French, Portuguese

---

## 11. CHATBOT

**Name:** Chat With AfriVid Online  
**File:** chatbot.js (loaded on all pages)  
**Model:** Claude Haiku via YAN Worker  
**Access:** Pro users only  
**Local responses:** Greetings, thanks, bye (no API call)  

---

## 12. KNOWN ISSUES (As of Launch)

1. Design studio text sometimes cuts off
2. Video export on some MP4 files needs rename to .webm
3. Photo editor flags/watermark features need polish
4. Mobile experience on create.html needs improvement
5. Safari (iPhone) limited support for some features

---

## 13. ROADMAP

### Tier 1 (Now) — AfriVid Studio
- ✅ Video Creator
- ✅ AI Video Editor
- ✅ Photo Editor
- ✅ Design Studio
- ✅ My Studio

### Tier 2 (Next) — Growth
- Flutterwave payment integration
- Mobile app (PWA improvement)
- More African languages
- AI Chatbot enhancement

### Tier 3 (Future) — Platform
- AfriVid API for developers
- Team collaboration
- Brand accounts

### Tier 4 (Vision) — AfriBrain
- Africa's first AI model
- Trained on African language data
- Powers all AfriVid features natively

---

## 14. CONTACT & SUPPORT

- **Email:** afrividstudio@gmail.com
- **Response time:** 24-48 hours
- **Admin:** afrividstudio@gmail.com / Regan6440

---

*Built by Regan Odhiambo Ayiecho — ALU Kigali, Mastercard Foundation Scholar*  
*"Built for Africa. By Africa." 🌍*
