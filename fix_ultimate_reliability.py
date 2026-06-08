with open('index.html', 'r') as f:
    content = f.read()

# ── FIX 1: FALLBACK VOICE (browser speechSynthesis) ──
old_generate_voice = '''  async function generateSceneVoice(i, retries = 3) {
    if (audioBuffers[i]) {
      addLog('success', `✓ Scene ${i+1} voice cached`);
      return; // Already generated - skip
    }
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 35000);
        const res = await fetch('https://yan-studio-worker.youngafricansn.workers.dev/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: scriptData.scenes[i].voiceover, voice: document.getElementById('voice-select').value }),
          signal: controller.signal
        });
        clearTimeout(timeout);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();
        audioBuffers[i] = await blob.arrayBuffer();
        addLog('success', `✓ Scene ${i+1} voice ready`);
        return;
      } catch(e) {
        clearTimeout && clearTimeout();
        if (attempt < retries) {
          addLog('info', `↺ Scene ${i+1} retry ${attempt}/${retries}...`);
          await new Promise(r => setTimeout(r, 1000 * attempt)); // wait before retry
        } else {
          addLog('error', `✗ Scene ${i+1} failed after ${retries} attempts`);
          audioBuffers[i] = null;
        }
      }
    }
  }'''

new_generate_voice = '''  async function generateSceneVoice(i, retries = 3) {
    if (audioBuffers[i]) {
      addLog('success', `✓ Scene ${i+1} voice cached`);
      return;
    }

    // Try Cloudflare TTS first
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 35000);
        const res = await fetch('https://yan-studio-worker.youngafricansn.workers.dev/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: scriptData.scenes[i].voiceover, voice: document.getElementById('voice-select').value }),
          signal: controller.signal
        });
        clearTimeout(timeout);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();
        audioBuffers[i] = await blob.arrayBuffer();
        addLog('success', `✓ Scene ${i+1} voice ready`);
        // Cache to IndexedDB
        saveVoiceToCache(i, audioBuffers[i]);
        return;
      } catch(e) {
        if (attempt < retries) {
          addLog('info', `↺ Scene ${i+1} retry ${attempt}/${retries} (waiting ${attempt}s)...`);
          await new Promise(r => setTimeout(r, 1000 * attempt));
        } else {
          addLog('error', `✗ Scene ${i+1} Cloudflare failed — using browser voice fallback`);
          // FALLBACK: Use browser speechSynthesis
          audioBuffers[i] = 'BROWSER_TTS_' + i; // marker for browser TTS
          addLog('info', `🔊 Scene ${i+1} will use browser voice (lower quality)`);
        }
      }
    }
  }

  // ── INDEXEDDB VOICE CACHE ──
  function getVoiceCacheKey() {
    return 'afrivid_voices_' + (scriptData?.title || '').replace(/[^a-z0-9]/gi, '_').toLowerCase();
  }

  async function saveVoiceToCache(i, buffer) {
    try {
      const key = getVoiceCacheKey() + '_scene_' + i;
      const db = await openVoiceDB();
      const tx = db.transaction('voices', 'readwrite');
      tx.objectStore('voices').put({ key, buffer, timestamp: Date.now() });
    } catch(e) {}
  }

  async function loadVoiceFromCache(i) {
    try {
      const key = getVoiceCacheKey() + '_scene_' + i;
      const db = await openVoiceDB();
      return new Promise((resolve) => {
        const tx = db.transaction('voices', 'readonly');
        const req = tx.objectStore('voices').get(key);
        req.onsuccess = () => resolve(req.result?.buffer || null);
        req.onerror = () => resolve(null);
      });
    } catch(e) { return null; }
  }

  function openVoiceDB() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open('AfriVidVoiceCache', 1);
      req.onupgradeneeded = e => e.target.result.createObjectStore('voices', { keyPath: 'key' });
      req.onsuccess = e => resolve(e.target.result);
      req.onerror = () => reject(req.error);
    });
  }'''

content = content.replace(old_generate_voice, new_generate_voice, 1)

# ── FIX 2: LOAD FROM CACHE BEFORE GENERATING ──
old_cache_init = '''  // ── RELIABLE VOICE GENERATION ──
  // Store buffers persistently so we can resume
  if (!window.cachedAudioBuffers || window.cachedAudioBuffers.length !== scriptData.scenes.length) {
    window.cachedAudioBuffers = new Array(scriptData.scenes.length).fill(null);
  }
  const audioBuffers = window.cachedAudioBuffers;'''

new_cache_init = '''  // ── RELIABLE VOICE GENERATION ──
  if (!window.cachedAudioBuffers || window.cachedAudioBuffers.length !== scriptData.scenes.length) {
    window.cachedAudioBuffers = new Array(scriptData.scenes.length).fill(null);
  }
  const audioBuffers = window.cachedAudioBuffers;

  // Load any previously cached voices from IndexedDB
  addLog('info', '🔍 Checking for cached voices...');
  let cachedCount = 0;
  for (let i = 0; i < scriptData.scenes.length; i++) {
    if (!audioBuffers[i]) {
      const cached = await loadVoiceFromCache(i);
      if (cached) {
        audioBuffers[i] = cached;
        cachedCount++;
      }
    }
  }
  if (cachedCount > 0) {
    addLog('success', `✓ Loaded ${cachedCount} cached voices from storage`);
  }'''

content = content.replace(old_cache_init, new_cache_init, 1)

# ── FIX 3: BROWSER TTS PLAYBACK IN playSceneAudio ──
old_play = '''  async function playSceneAudio(index) {
    if (!audioBuffers[index]) return;
    try {
      const decoded = await audioCtx.decodeAudioData(audioBuffers[index].slice(0));'''

new_play = '''  async function playSceneAudio(index) {
    if (!audioBuffers[index]) return;

    // Handle browser TTS fallback
    if (typeof audioBuffers[index] === 'string' && audioBuffers[index].startsWith('BROWSER_TTS_')) {
      const scene = scriptData.scenes[index];
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utt = new SpeechSynthesisUtterance(scene.voiceover);
        utt.rate = 0.95;
        utt.pitch = 1;
        utt.volume = 0.9;
        // Try to find a good voice
        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v => v.lang.startsWith('en') && !v.name.includes('Google'));
        if (preferred) utt.voice = preferred;
        window.speechSynthesis.speak(utt);
      }
      return;
    }

    try {
      const decoded = await audioCtx.decodeAudioData(audioBuffers[index].slice(0));'''

content = content.replace(old_play, new_play, 1)

# ── FIX 4: AUTO-RECONNECT - retry on network error ──
old_batch = '''  // Step 1: Generate all voices with retry
  addLog('info', `🎤 Generating ${scriptData.scenes.length} scene voices...`);
  const batchSize = 3;
  for (let b = 0; b < scriptData.scenes.length; b += batchSize) {
    const batch = [];
    for (let j = 0; j < batchSize && b+j < scriptData.scenes.length; j++) {
      const i = b + j;
      const scene = scriptData.scenes[i];
      batch.push(generateSceneVoice(i));
    }
    await Promise.all(batch);
    const done = audioBuffers.filter(x => x !== null).length;
    const failed = audioBuffers.filter((x, i) => x === null && i < b + batchSize).length;
    addLog('info', `⏳ ${b + batchSize > scriptData.scenes.length ? scriptData.scenes.length : b + batchSize}/${scriptData.scenes.length} processed...`);
  }'''

new_batch = '''  // Step 1: Generate all voices with retry + auto-reconnect
  addLog('info', `🎤 Generating ${scriptData.scenes.length} scene voices...`);
  const batchSize = 3;

  // Check internet connectivity
  async function waitForInternet() {
    while (!navigator.onLine) {
      addLog('error', '📵 No internet. Waiting to reconnect...');
      await new Promise(r => setTimeout(r, 3000));
    }
    addLog('success', '✓ Internet connected');
  }

  for (let b = 0; b < scriptData.scenes.length; b += batchSize) {
    await waitForInternet();
    const batch = [];
    for (let j = 0; j < batchSize && b+j < scriptData.scenes.length; j++) {
      batch.push(generateSceneVoice(b + j));
    }
    await Promise.all(batch);
    const total = Math.min(b + batchSize, scriptData.scenes.length);
    addLog('info', `⏳ ${total}/${scriptData.scenes.length} scenes processed...`);
  }'''

content = content.replace(old_batch, new_batch, 1)

# ── FIX 5: SAVE PROGRESS TO LOCALSTORAGE ──
old_make_another = '''function makeAnother() {
  scriptData = null;
  videoBlob = null;
  recordedChunks = [];
  window.cachedAudioBuffers = null; // Clear voice cache for new video
  window.lastCompletedScene = 0;
  document.getElementById('video-topic').value = '';'''

new_make_another = '''function saveGenerationProgress() {
  if (!scriptData) return;
  try {
    localStorage.setItem('afrivid_last_script', JSON.stringify({
      title: scriptData.title,
      duration: scriptData.duration,
      sceneCount: scriptData.scenes.length,
      savedAt: Date.now()
    }));
  } catch(e) {}
}

function checkResumePrompt() {
  try {
    const saved = localStorage.getItem('afrivid_last_script');
    if (!saved) return;
    const data = JSON.parse(saved);
    const age = Date.now() - data.savedAt;
    if (age < 3600000) { // Less than 1 hour old
      const resumeDiv = document.createElement('div');
      resumeDiv.style.cssText = 'padding:0.75rem 1rem;background:rgba(245,166,35,0.1);border:1px solid rgba(245,166,35,0.3);border-radius:8px;margin-bottom:1rem;font-size:0.82rem;display:flex;justify-content:space-between;align-items:center;';
      resumeDiv.innerHTML = `<span style="color:var(--gold);">↺ Resume: "${data.title}" (${data.sceneCount} scenes)</span><button onclick="this.parentElement.remove()" style="background:none;border:none;color:var(--muted);cursor:pointer;">✕</button>`;
      const form = document.querySelector('#panel-1 .card');
      if (form) form.prepend(resumeDiv);
    }
  } catch(e) {}
}

function makeAnother() {
  scriptData = null;
  videoBlob = null;
  recordedChunks = [];
  window.cachedAudioBuffers = null;
  window.lastCompletedScene = 0;
  localStorage.removeItem('afrivid_last_script');
  document.getElementById('video-topic').value = '';'''

content = content.replace(old_make_another, new_make_another, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Ultimate reliability fixes applied!")
