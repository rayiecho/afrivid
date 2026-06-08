with open('index.html', 'r') as f:
    content = f.read()

# 1. Add aspect ratio to enhancer
old_enhance_export = '''      <!-- ACTIONS -->
      <div class="card">
        <div class="card-title"><div class="card-title-icon">⚡</div>Export</div>
        <div class="btn-row">
          <button onclick="startEnhancing()">✨ Enhance & Export</button>
          <button onclick="resetEnhancer()">↺ Reset</button>
        </div>'''

new_enhance_export = '''      <!-- ACTIONS -->
      <div class="card">
        <div class="card-title"><div class="card-title-icon">⚡</div>Export</div>
        <div class="enhance-grid" style="margin-bottom:1rem;">
          <div class="form-group">
            <label class="form-label">Output Aspect Ratio</label>
            <select id="enhance-aspect" class="form-select">
              <option value="original">Original (Keep as is)</option>
              <option value="16:9">16:9 — Landscape (YouTube)</option>
              <option value="9:16">9:16 — Portrait (TikTok/Reels)</option>
              <option value="1:1">1:1 — Square (Instagram)</option>
              <option value="4:3">4:3 — Classic</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Output Quality</label>
            <select id="enhance-quality" class="form-select">
              <option value="high">🏆 High (Best quality)</option>
              <option value="medium" selected>⚡ Medium (Balanced)</option>
              <option value="low">💨 Low (Smaller file)</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Output Format</label>
            <select id="enhance-format" class="form-select">
              <option value="webm">WebM (Fast)</option>
              <option value="mp4">MP4 (Compatible) — via FFmpeg</option>
            </select>
          </div>
        </div>
        <div class="btn-row">
          <button onclick="startEnhancing()">✨ Enhance & Export</button>
          <button onclick="resetEnhancer()">↺ Reset</button>
        </div>'''

content = content.replace(old_enhance_export, new_enhance_export, 1)

# 2. Add FFmpeg.wasm script
old_mediapipe = '<script src="https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation/selfie_segmentation.js" crossorigin="anonymous"></script>'
new_mediapipe = '''<script src="https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation/selfie_segmentation.js" crossorigin="anonymous"></script>'''
# FFmpeg loaded dynamically to avoid blocking

# 3. Update finishEnhancing to handle MP4 via FFmpeg
old_finish_enhancing = '''function finishEnhancing() {
  enhancedBlob = new Blob(enhanceRecordedChunks, { type: 'video/webm' });
  const sizeMB = (enhancedBlob.size / 1024 / 1024).toFixed(1);
  addEnhanceLog('success', `✓ Enhanced video ready! Size: ${sizeMB}MB`);

  // Show download + YouTube buttons
  document.getElementById('enhance-export-btns').style.display = 'flex';
  
  document.getElementById('enhance-progress-label').textContent = 'Done!';
  document.getElementById('enhance-progress-pct').textContent = '100%';
  document.getElementById('enhance-progress-fill').style.width = '100%';
}'''

new_finish_enhancing = '''async function finishEnhancing() {
  enhancedBlob = new Blob(enhanceRecordedChunks, { type: 'video/webm' });
  const sizeMB = (enhancedBlob.size / 1024 / 1024).toFixed(1);
  addEnhanceLog('success', `✓ Enhanced video ready! Size: ${sizeMB}MB`);

  const format = document.getElementById('enhance-format')?.value || 'webm';

  if (format === 'mp4') {
    addEnhanceLog('info', '🔄 Converting to MP4 via FFmpeg...');
    try {
      await convertToMP4(enhancedBlob);
      addEnhanceLog('success', '✓ MP4 conversion complete!');
    } catch(e) {
      addEnhanceLog('error', '✗ MP4 conversion failed, downloading as WebM');
      downloadEnhanced();
    }
  } else {
    document.getElementById('enhance-export-btns').style.display = 'flex';
  }

  document.getElementById('enhance-progress-label').textContent = 'Done!';
  document.getElementById('enhance-progress-pct').textContent = '100%';
  document.getElementById('enhance-progress-fill').style.width = '100%';
}

async function convertToMP4(webmBlob) {
  // Dynamically load FFmpeg
  addEnhanceLog('info', '📦 Loading FFmpeg (first time may take 30s)...');
  
  const { FFmpeg } = await import('https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.6/dist/esm/index.js');
  const { fetchFile } = await import('https://cdn.jsdelivr.net/npm/@ffmpeg/util@0.12.1/dist/esm/index.js');
  
  const ffmpeg = new FFmpeg();
  ffmpeg.on('progress', ({ progress }) => {
    const pct = Math.round(progress * 100);
    addEnhanceLog('info', `🔄 Converting: ${pct}%`);
  });
  
  await ffmpeg.load();
  addEnhanceLog('success', '✓ FFmpeg loaded!');

  const quality = document.getElementById('enhance-quality')?.value || 'medium';
  const crf = quality === 'high' ? '18' : quality === 'medium' ? '23' : '28';

  await ffmpeg.writeFile('input.webm', await fetchFile(webmBlob));
  await ffmpeg.exec([
    '-i', 'input.webm',
    '-c:v', 'libx264',
    '-crf', crf,
    '-preset', 'fast',
    '-c:a', 'aac',
    '-b:a', '128k',
    'output.mp4'
  ]);

  const data = await ffmpeg.readFile('output.mp4');
  const mp4Blob = new Blob([data.buffer], { type: 'video/mp4' });
  const url = URL.createObjectURL(mp4Blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `AfriVid-Enhanced-${Date.now()}.mp4`;
  a.click();
  URL.revokeObjectURL(url);

  document.getElementById('enhance-export-btns').style.display = 'flex';
}'''

content = content.replace(old_finish_enhancing, new_finish_enhancing, 1)

# 4. Apply aspect ratio to enhance canvas
old_enhance_start = '''  video.currentTime = useClips ? clips[0].start : 0;
  video.play();
  addEnhanceLog('success', useClips ? `✓ Processing ${clips.length} clip(s)...` : '✓ Processing video frames...');'''

new_enhance_start = '''  // Apply aspect ratio crop
  const enhanceAR = document.getElementById('enhance-aspect')?.value || 'original';
  if (enhanceAR !== 'original') {
    const arParts = enhanceAR.split(':');
    const targetAR = parseInt(arParts[0]) / parseInt(arParts[1]);
    const videoAR = video.videoWidth / video.videoHeight;
    if (Math.abs(targetAR - videoAR) > 0.01) {
      if (targetAR > videoAR) {
        canvas.width = video.videoWidth;
        canvas.height = Math.round(video.videoWidth / targetAR);
      } else {
        canvas.height = video.videoHeight;
        canvas.width = Math.round(video.videoHeight * targetAR);
      }
      addEnhanceLog('info', `✓ Aspect ratio: ${enhanceAR} (${canvas.width}x${canvas.height})`);
    }
  }

  // Apply quality bitrate
  const quality = document.getElementById('enhance-quality')?.value || 'medium';
  const bitrates = { high: 6000000, medium: 3000000, low: 1000000 };

  video.currentTime = useClips ? clips[0].start : 0;
  video.play();
  addEnhanceLog('success', useClips ? `✓ Processing ${clips.length} clip(s)...` : '✓ Processing video frames...');'''

content = content.replace(old_enhance_start, new_enhance_start, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ FFmpeg MP4 + Aspect ratios added to enhancer!")
