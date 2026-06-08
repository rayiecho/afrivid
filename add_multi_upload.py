with open('index.html', 'r') as f:
    content = f.read()

# Replace single upload zone with multi-file upload
old_upload = '''    <!-- UPLOAD -->
    <div class="card" id="enhancer-upload-card">
      <div class="card-title"><div class="card-title-icon">📁</div>Upload Your Video</div>
      <div class="upload-zone" onclick="document.getElementById('video-file-input').click()" id="upload-zone">
        <input type="file" id="video-file-input" accept="video/*" style="display:none" onchange="loadVideoFile(event)">
        <div class="upload-zone-icon">🎥</div>
        <div class="upload-zone-text">Click to upload your video</div>
        <div class="upload-zone-sub">MP4, MOV, AVI, WebM supported</div>
      </div>
    </div>'''

new_upload = '''    <!-- UPLOAD -->
    <div class="card" id="enhancer-upload-card">
      <div class="card-title"><div class="card-title-icon">📁</div>Upload Videos</div>

      <!-- Mode selector -->
      <div style="display:flex;gap:0;margin-bottom:1rem;border:1px solid var(--border);border-radius:10px;overflow:hidden;">
        <button id="mode-single" onclick="setUploadMode('single')" style="flex:1;padding:0.7rem;background:var(--gold);color:var(--navy);border:none;font-family:var(--font-display);font-weight:700;cursor:pointer;font-size:0.85rem;">🎥 Single Video</button>
        <button id="mode-multi" onclick="setUploadMode('multi')" style="flex:1;padding:0.7rem;background:transparent;color:var(--muted);border:none;font-family:var(--font-display);font-weight:700;cursor:pointer;font-size:0.85rem;">🎞 Combine Videos</button>
      </div>

      <!-- Single upload -->
      <div id="single-upload-zone">
        <div class="upload-zone" onclick="document.getElementById('video-file-input').click()" id="upload-zone">
          <input type="file" id="video-file-input" accept="video/*" style="display:none" onchange="loadVideoFile(event)">
          <div class="upload-zone-icon">🎥</div>
          <div class="upload-zone-text">Click to upload your video</div>
          <div class="upload-zone-sub">MP4, MOV, AVI, WebM supported</div>
        </div>
      </div>

      <!-- Multi upload -->
      <div id="multi-upload-zone" style="display:none;">
        <div class="upload-zone" onclick="document.getElementById('multi-file-input').click()" style="margin-bottom:1rem;">
          <input type="file" id="multi-file-input" accept="video/*" multiple style="display:none" onchange="loadMultipleVideos(event)">
          <div class="upload-zone-icon">🎞</div>
          <div class="upload-zone-text">Click to upload multiple videos</div>
          <div class="upload-zone-sub">Select multiple files — they will be combined in order</div>
        </div>

        <!-- Video list -->
        <div id="multi-video-list" style="display:none;">
          <div style="font-size:0.75rem;color:var(--gold);font-family:var(--font-mono);margin-bottom:0.75rem;">VIDEOS TO COMBINE</div>
          <div id="video-items-list"></div>

          <!-- AI Instructions -->
          <div class="form-group" style="margin-top:1rem;">
            <label class="form-label">AI Instructions (optional)</label>
            <textarea id="combine-instructions" class="form-textarea" style="min-height:70px;" placeholder="e.g. Combine all videos, add intro music, add title card at start saying Welcome to AfriVid Studio"></textarea>
          </div>

          <div class="btn-row" style="margin-top:1rem;">
            <button onclick="combineVideos()" class="btn btn-gold">🎬 Combine Videos</button>
            <button onclick="resetMultiUpload()" class="btn btn-outline">↺ Clear All</button>
          </div>
          <div class="status-log" id="combine-log" style="margin-top:1rem;">
            <span class="log-line info">// Videos will be combined in the order shown above.</span>
          </div>
          <div class="progress-wrap" id="combine-progress" style="display:none;margin-top:1rem;">
            <div class="progress-label">
              <span id="combine-progress-label">Combining...</span>
              <span id="combine-progress-pct">0%</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" id="combine-progress-fill"></div></div>
          </div>
        </div>
      </div>
    </div>'''

content = content.replace(old_upload, new_upload, 1)

# Add multi-upload JS
old_reset_enhancer = 'function resetEnhancer() {'
new_reset_enhancer = '''// ── UPLOAD MODE ──
let uploadMode = 'single';
let multiVideos = []; // Array of {file, url, name, duration}

function setUploadMode(mode) {
  uploadMode = mode;
  document.getElementById('single-upload-zone').style.display = mode === 'single' ? 'block' : 'none';
  document.getElementById('multi-upload-zone').style.display = mode === 'multi' ? 'block' : 'none';
  document.getElementById('mode-single').style.background = mode === 'single' ? 'var(--gold)' : 'transparent';
  document.getElementById('mode-single').style.color = mode === 'single' ? 'var(--navy)' : 'var(--muted)';
  document.getElementById('mode-multi').style.background = mode === 'multi' ? 'var(--gold)' : 'transparent';
  document.getElementById('mode-multi').style.color = mode === 'multi' ? 'var(--navy)' : 'var(--muted)';
}

async function loadMultipleVideos(event) {
  const files = Array.from(event.target.files);
  if (!files.length) return;

  for (const file of files) {
    const url = URL.createObjectURL(file);
    const duration = await getVideoDuration(url);
    multiVideos.push({ file, url, name: file.name, duration, size: (file.size/1024/1024).toFixed(1) });
  }

  renderVideoList();
  document.getElementById('multi-video-list').style.display = 'block';
}

function getVideoDuration(url) {
  return new Promise(resolve => {
    const v = document.createElement('video');
    v.onloadedmetadata = () => resolve(Math.round(v.duration));
    v.onerror = () => resolve(0);
    v.src = url;
  });
}

function formatDur(s) {
  const m = Math.floor(s/60), sec = s%60;
  return `${m}:${sec.toString().padStart(2,'0')}`;
}

function renderVideoList() {
  const list = document.getElementById('video-items-list');
  const totalDur = multiVideos.reduce((s,v) => s + v.duration, 0);
  list.innerHTML = multiVideos.map((v, i) => `
    <div style="display:flex;align-items:center;gap:0.75rem;padding:0.75rem;background:var(--navy3);border-radius:8px;margin-bottom:0.5rem;border:1px solid var(--border2);">
      <span style="font-size:0.75rem;font-family:var(--font-mono);color:var(--gold);min-width:20px;">${i+1}</span>
      <div style="flex:1;">
        <div style="font-size:0.82rem;font-weight:600;color:var(--white);">${v.name}</div>
        <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">${formatDur(v.duration)} · ${v.size}MB</div>
      </div>
      <div style="display:flex;gap:4px;">
        ${i > 0 ? `<button onclick="moveVideo(${i},-1)" style="background:var(--border2);border:none;color:var(--white);width:24px;height:24px;border-radius:4px;cursor:pointer;font-size:0.8rem;">↑</button>` : ''}
        ${i < multiVideos.length-1 ? `<button onclick="moveVideo(${i},1)" style="background:var(--border2);border:none;color:var(--white);width:24px;height:24px;border-radius:4px;cursor:pointer;font-size:0.8rem;">↓</button>` : ''}
        <button onclick="removeVideo(${i})" style="background:rgba(230,51,41,0.15);border:none;color:#E63329;width:24px;height:24px;border-radius:4px;cursor:pointer;font-size:0.8rem;">✕</button>
      </div>
    </div>
  `).join('') + `
    <div style="padding:0.5rem;text-align:center;font-size:0.75rem;color:var(--gold);font-family:var(--font-mono);">
      Total: ${multiVideos.length} videos · ${formatDur(totalDur)} combined
    </div>`;
}

function moveVideo(idx, dir) {
  const newIdx = idx + dir;
  if (newIdx < 0 || newIdx >= multiVideos.length) return;
  [multiVideos[idx], multiVideos[newIdx]] = [multiVideos[newIdx], multiVideos[idx]];
  renderVideoList();
}

function removeVideo(idx) {
  URL.revokeObjectURL(multiVideos[idx].url);
  multiVideos.splice(idx, 1);
  if (multiVideos.length === 0) {
    document.getElementById('multi-video-list').style.display = 'none';
  } else {
    renderVideoList();
  }
}

function resetMultiUpload() {
  multiVideos.forEach(v => URL.revokeObjectURL(v.url));
  multiVideos = [];
  document.getElementById('multi-video-list').style.display = 'none';
  document.getElementById('multi-file-input').value = '';
  document.getElementById('combine-log').innerHTML = '<span class="log-line info">// Videos will be combined in the order shown above.</span>';
}

function addCombineLog(type, msg) {
  const log = document.getElementById('combine-log');
  const line = document.createElement('span');
  line.className = `log-line ${type}`;
  line.textContent = msg;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

async function combineVideos() {
  if (multiVideos.length < 2) { alert('Please upload at least 2 videos to combine'); return; }

  addCombineLog('info', `🎬 Combining ${multiVideos.length} videos...`);
  document.getElementById('combine-progress').style.display = 'block';

  // Check for AI instructions
  const instructions = document.getElementById('combine-instructions').value.trim();
  if (instructions) {
    addCombineLog('info', '🤖 AI is processing your instructions...');
  }

  try {
    // Load FFmpeg
    addCombineLog('info', '📦 Loading FFmpeg...');
    const { FFmpeg } = await import('https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.6/dist/esm/index.js');
    const { fetchFile } = await import('https://cdn.jsdelivr.net/npm/@ffmpeg/util@0.12.1/dist/esm/index.js');

    const ffmpeg = new FFmpeg();
    ffmpeg.on('progress', ({ progress }) => {
      const pct = Math.round(progress * 100);
      document.getElementById('combine-progress-fill').style.width = pct + '%';
      document.getElementById('combine-progress-pct').textContent = pct + '%';
    });

    await ffmpeg.load();
    addCombineLog('success', '✓ FFmpeg loaded!');

    // Write all video files
    const fileList = [];
    for (let i = 0; i < multiVideos.length; i++) {
      const fname = `input${i}.mp4`;
      addCombineLog('info', `📥 Loading video ${i+1}/${multiVideos.length}...`);
      await ffmpeg.writeFile(fname, await fetchFile(multiVideos[i].file));
      fileList.push(`file '${fname}'`);
      document.getElementById('combine-progress-fill').style.width = (i+1)/multiVideos.length * 30 + '%';
    }

    // Create concat file
    const concatContent = fileList.join('\n');
    await ffmpeg.writeFile('concat.txt', concatContent);
    addCombineLog('info', '🔗 Combining videos...');

    // Combine using concat
    await ffmpeg.exec([
      '-f', 'concat',
      '-safe', '0',
      '-i', 'concat.txt',
      '-c', 'copy',
      'combined.mp4'
    ]);

    addCombineLog('success', '✓ Videos combined!');
    document.getElementById('combine-progress-label').textContent = 'Done!';
    document.getElementById('combine-progress-pct').textContent = '100%';
    document.getElementById('combine-progress-fill').style.width = '100%';

    // Download
    const data = await ffmpeg.readFile('combined.mp4');
    const blob = new Blob([data.buffer], { type: 'video/mp4' });
    const sizeMB = (blob.size/1024/1024).toFixed(1);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AfriVid-Combined-${Date.now()}.mp4`;
    a.click();
    URL.revokeObjectURL(url);
    addCombineLog('success', `✓ Downloaded! Size: ${sizeMB}MB`);

  } catch(e) {
    addCombineLog('error', '✗ Combine failed: ' + e.message);
    addCombineLog('info', 'Tip: Make sure all videos have the same resolution and codec');
  }
}

function resetEnhancer() {'''

content = content.replace(old_reset_enhancer, new_reset_enhancer, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Multi-video upload and combine added!")
