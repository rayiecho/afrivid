#!/usr/bin/env python3
"""
Patches aieditor.html with several coordinated changes:

1. Updates the AI action-parsing prompt in runAIEdit() to recognize
   compress, translate, and bgremove instructions.
2. Adds compress/translate/bgremove cases to runAIEdit()'s switch.
3. Adds an optional `bitrate` param to exportClips() (used by compress).
4. Adds a shared drawCaptionFrame() helper and wires it into the
   per-frame export loop, so captions get burned into the final
   downloaded/exported video file (not just shown live in-browser).
5. Auto-triggers transcription + captions right after a video is
   uploaded, instead of requiring a manual "Captions" click.

Each replacement is checked individually: if any expected block isn't
found exactly once, the script stops and makes NO changes at all,
so you never end up with a half-applied patch.

Makes a aieditor.html.bak backup before writing anything.

Run from inside ~/projects/afrivid:
    python3 patch_aieditor.py
"""

import shutil
import sys

FILE = "aieditor.html"

REPLACEMENTS = []

# 1. Expand the action-parsing prompt
REPLACEMENTS.append((
"""    const raw = await claudeAsk(`You are an AI video editor. Video is ${totalSecs}s long. User said: "${instructions}". Return ONLY valid JSON: {"summary":"what you will do","actions":[]} where action types are: trim (needs start,end in seconds), speed (needs factor: 0.5=slowmo 2=fast), silence, highlight (needs duration:60), noise, caption, aspect (needs ratio: 9:16 or 16:9 or 1:1), music (needs mood: inspirational/calm/upbeat), thumbnail. Only include actions the user asked for.`, 800);""",
"""    const raw = await claudeAsk(`You are an AI video editor. Video is ${totalSecs}s long. User said: "${instructions}". Return ONLY valid JSON: {"summary":"what you will do","actions":[]} where action types are: trim (needs start,end in seconds), speed (needs factor: 0.5=slowmo 2=fast), silence, highlight (needs duration:60), noise, caption, aspect (needs ratio: 9:16 or 16:9 or 1:1), music (needs mood: inspirational/calm/upbeat), thumbnail, compress (needs bitrate: pick 400000 for "a lot"/"heavily"/"max compression", 800000 for "compress"/moderate, 1500000 for "slightly"/"a little"), translate (needs lang: ISO code like sw/fr/es, default sw), bgremove (needs mode: blur or remove, default blur). Only include actions the user asked for.`, 800);"""
))

# 2. Add compress/translate/bgremove cases to the switch
REPLACEMENTS.append((
"""      case 'thumbnail':
        updateProcessingProgress(pct, 'Extracting best frame...', i+1);
        await doThumbnail();
        break;
      default:
        addLog('all', `[!] Unknown action: ${action.type}`);""",
"""      case 'thumbnail':
        updateProcessingProgress(pct, 'Extracting best frame...', i+1);
        await doThumbnail();
        break;
      case 'compress':
        updateProcessingProgress(pct, 'Compressing video...', i+1);
        await exportClips([{ start: 0, end: video.duration }], 'AfriVid-Compressed', action.bitrate || 800000);
        break;
      case 'translate':
        updateProcessingProgress(pct, `Translating to ${action.lang||'sw'}...`, i+1);
        await doTranslate(action.lang || 'sw');
        break;
      case 'bgremove':
        updateProcessingProgress(pct, 'Removing background...', i+1);
        await doBgRemove(action.mode || 'blur');
        break;
      default:
        addLog('all', `[!] Unknown action: ${action.type}`);"""
))

# 3. Add optional bitrate param to exportClips signature
REPLACEMENTS.append((
"""async function exportClips(clips, filename) {""",
"""async function exportClips(clips, filename, bitrate) {"""
))

# 4. Use the bitrate param in the recorder instead of the hardcoded value
REPLACEMENTS.append((
"""  const recorder = new MediaRecorder(stream, {mimeType, videoBitsPerSecond: 2500000});""",
"""  const recorder = new MediaRecorder(stream, {mimeType, videoBitsPerSecond: bitrate || 2500000});"""
))

# 5. Draw burned-in captions on every exported frame
REPLACEMENTS.append((
"""      function frame() {
        if (!video.paused && video.currentTime < clipEnd) {
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          animId = requestAnimationFrame(frame);""",
"""      function frame() {
        if (!video.paused && video.currentTime < clipEnd) {
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          if (window._captionWords && window._captionWords.length) {
            drawCaptionFrame(ctx, canvas, video.currentTime);
          }
          animId = requestAnimationFrame(frame);"""
))

# 6. Share caption timing globally + add canvas caption renderer
REPLACEMENTS.append((
"""  const words = text.split(' ');
  const wps = words.length / (video.duration || 60);
  video.addEventListener('timeupdate', () => {
    const wi = Math.floor(video.currentTime * wps);
    const cs = 8, start = Math.floor(wi/cs)*cs;
    const chunk = words.slice(start, start+cs);
    const active = wi - start;
    const cs2 = currentCaptionStyle;
    let bg='rgba(0,0,0,0.75)',color='#fff',fs='1rem',fw='700';
    if(cs2==='bold'){fs='1.2rem';fw='900';bg='rgba(0,0,0,0.9)';}
    else if(cs2==='minimal'){bg='transparent';}
    else if(cs2==='tiktok'){bg='transparent';color='#fffc00';fs='1.3rem';fw='900';}
    overlay.innerHTML = chunk.length ? `<span style="background:${bg};color:${color};font-size:${fs};font-weight:${fw};padding:0.4rem 0.85rem;border-radius:6px;font-family:Syne,sans-serif;display:inline-block;">${chunk.map((w,i)=>i===active?`<span style="color:#F5A623;font-weight:900;">${w}</span>`:w).join(' ')}</span>` : '';
  });
  video.addEventListener('ended', ()=>{ overlay.innerHTML=''; });
}""",
"""  const words = text.split(' ');
  const wps = words.length / (video.duration || 60);
  window._captionWords = words;
  window._captionWps = wps;
  video.addEventListener('timeupdate', () => {
    const wi = Math.floor(video.currentTime * wps);
    const cs = 8, start = Math.floor(wi/cs)*cs;
    const chunk = words.slice(start, start+cs);
    const active = wi - start;
    const cs2 = currentCaptionStyle;
    let bg='rgba(0,0,0,0.75)',color='#fff',fs='1rem',fw='700';
    if(cs2==='bold'){fs='1.2rem';fw='900';bg='rgba(0,0,0,0.9)';}
    else if(cs2==='minimal'){bg='transparent';}
    else if(cs2==='tiktok'){bg='transparent';color='#fffc00';fs='1.3rem';fw='900';}
    overlay.innerHTML = chunk.length ? `<span style="background:${bg};color:${color};font-size:${fs};font-weight:${fw};padding:0.4rem 0.85rem;border-radius:6px;font-family:Syne,sans-serif;display:inline-block;">${chunk.map((w,i)=>i===active?`<span style="color:#F5A623;font-weight:900;">${w}</span>`:w).join(' ')}</span>` : '';
  });
  video.addEventListener('ended', ()=>{ overlay.innerHTML=''; });
}

function drawCaptionFrame(ctx, canvas, currentTime) {
  const words = window._captionWords;
  const wps = window._captionWps;
  if (!words || !wps) return;
  const wi = Math.floor(currentTime * wps);
  const cs = 8, start = Math.floor(wi/cs)*cs;
  const chunk = words.slice(start, start+cs);
  if (!chunk.length) return;
  const cs2 = currentCaptionStyle;
  let color = '#ffffff', fs = Math.round(canvas.height*0.045), fw = '700', bgAlpha = 0.75, showBg = true;
  if (cs2 === 'bold') { fs = Math.round(canvas.height*0.055); fw = '900'; bgAlpha = 0.9; }
  else if (cs2 === 'minimal') { showBg = false; }
  else if (cs2 === 'tiktok') { showBg = false; color = '#fffc00'; fs = Math.round(canvas.height*0.06); fw = '900'; }
  const text = chunk.join(' ');
  ctx.save();
  ctx.font = `${fw} ${fs}px Syne, sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'alphabetic';
  const x = canvas.width / 2;
  const y = canvas.height - Math.round(canvas.height*0.1);
  const metrics = ctx.measureText(text);
  if (showBg) {
    const padX = 20, padY = 14;
    const bw = metrics.width + padX*2, bh = fs + padY*2;
    ctx.fillStyle = `rgba(0,0,0,${bgAlpha})`;
    if (ctx.roundRect) {
      ctx.beginPath();
      ctx.roundRect(x-bw/2, y-fs-padY+4, bw, bh, 8);
      ctx.fill();
    } else {
      ctx.fillRect(x-bw/2, y-fs-padY+4, bw, bh);
    }
  }
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}"""
))

# 7. Reset per-upload caption state at the top of loadVideo
REPLACEMENTS.append((
"""function loadVideo(file) {
  currentVideoFile = file;
  window.currentVideoFile = file;""",
"""function loadVideo(file) {
  currentVideoFile = file;
  window.currentVideoFile = file;
  window._autoCaptionsTriggered = false;
  window._captionWords = null;
  window._captionWps = null;"""
))

# 8. Auto-trigger transcription + captions right after upload
REPLACEMENTS.append((
"""    addLog('all', `[ok] Loaded: ${file.name} (${formatTime(video.duration)})`);""",
"""    addLog('all', `[ok] Loaded: ${file.name} (${formatTime(video.duration)})`);
    if (!window._autoCaptionsTriggered) {
      window._autoCaptionsTriggered = true;
      (async () => {
        try {
          addLog('captions', '[~] Auto-generating captions...');
          const text = await transcribe();
          if (text) {
            startKaraokeCaptions(text);
            addLog('captions', '[ok] Captions ready!');
          }
        } catch(e) { console.log('[AutoCaptions]', e.message); }
      })();
    }"""
))


def main():
    with open(FILE, "r", encoding="utf-8") as f:
        content = f.read()

    problems = []
    for i, (old, new) in enumerate(REPLACEMENTS, 1):
        count = content.count(old)
        if count != 1:
            problems.append((i, count))

    if problems:
        print("ERROR: One or more expected blocks were not found exactly once.")
        print("No changes have been made to the file.")
        for i, count in problems:
            print(f"  Replacement #{i}: found {count} occurrence(s), expected 1")
        print("\nThis usually means the file has changed since we last inspected it.")
        print("Paste the current relevant sections back to Claude before editing.")
        sys.exit(1)

    shutil.copy(FILE, FILE + ".bak")
    print(f"Backup written to {FILE}.bak")

    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{FILE} patched successfully. Applied {len(REPLACEMENTS)} changes.")
    print("Next: run 'diff aieditor.html.bak aieditor.html' to review, then publish/deploy as usual.")

if __name__ == "__main__":
    main()
