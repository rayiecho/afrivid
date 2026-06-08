with open('index.html', 'r') as f:
    content = f.read()

# Replace the entire audio generation + recording section
old_gen = '''  addLog('info', `🎤 Generating ${scriptData.scenes.length} scene voices...`);
  const audioBuffers = new Array(scriptData.scenes.length).fill(null);
  
  // Generate in batches of 3 to avoid overloading
  const batchSize = 3;
  for (let b = 0; b < scriptData.scenes.length; b += batchSize) {
    const batch = scriptData.scenes.slice(b, b + batchSize);
    await Promise.all(batch.map(async (scene, j) => {
      const i = b + j;
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 30000); // 30s timeout
        try {
          const res = await fetch('https://yan-studio-worker.youngafricansn.workers.dev/tts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: scene.voiceover, voice: document.getElementById('voice-select').value }),
            signal: controller.signal
          });
          clearTimeout(timeout);
          const blob = await res.blob();
          audioBuffers[i] = await blob.arrayBuffer();
          addLog('success', `✓ Scene ${i+1} voice ready`);
        } catch(e) {
          clearTimeout(timeout);
          addLog('error', `✗ Scene ${i+1} skipped: ${e.message}`);
          audioBuffers[i] = null; // Continue without this scene's audio
        }
      } catch(e) {
        addLog('error', `✗ Scene ${i+1} failed: ${e.message}`);
        audioBuffers[i] = null;
      }
    }));
    addLog('info', `⏳ ${Math.min(b+batchSize, scriptData.scenes.length)}/${scriptData.scenes.length} scenes done...`);
  }
  addLog('success', '✓ All voices generated!');'''

new_gen = '''  // ── RELIABLE VOICE GENERATION ──
  // Store buffers persistently so we can resume
  if (!window.cachedAudioBuffers || window.cachedAudioBuffers.length !== scriptData.scenes.length) {
    window.cachedAudioBuffers = new Array(scriptData.scenes.length).fill(null);
  }
  const audioBuffers = window.cachedAudioBuffers;

  async function generateSceneVoice(i, retries = 3) {
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
          body: JSON.stringify({ text: scene.voiceover, voice: document.getElementById('voice-select').value }),
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
  }

  // Step 1: Generate all voices with retry
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
  }

  // Step 2: Check which scenes failed
  const failedScenes = audioBuffers.map((b,i) => b === null ? i+1 : null).filter(x => x !== null);
  if (failedScenes.length > 0) {
    addLog('error', `⚠ ${failedScenes.length} scene(s) failed: ${failedScenes.join(', ')}`);
    addLog('info', 'These scenes will play silently. You can stop and retry.');
    // Show retry button
    const retryBtn = document.createElement('button');
    retryBtn.textContent = '↺ Retry Failed Scenes';
    retryBtn.className = 'btn btn-gold';
    retryBtn.style.marginTop = '0.5rem';
    retryBtn.onclick = async () => {
      retryBtn.remove();
      // Only retry failed scenes
      for (const i of failedScenes.map(n => n-1)) {
        await generateSceneVoice(i, 3);
      }
      addLog('success', '✓ Retry complete!');
    };
    document.getElementById('status-log').appendChild(retryBtn);
  } else {
    addLog('success', `✓ All ${scriptData.scenes.length} voices ready!`);
  }

  // Step 3: Show confirmation before recording
  const readyCount = audioBuffers.filter(x => x !== null).length;
  addLog('info', `📋 ${readyCount}/${scriptData.scenes.length} scenes ready. Starting recording...`);'''

content = content.replace(old_gen, new_gen, 1)

# Fix scene reference in generateSceneVoice - need to pass scene
content = content.replace(
    'body: JSON.stringify({ text: scene.voiceover, voice: document.getElementById(\'voice-select\').value }),',
    'body: JSON.stringify({ text: scriptData.scenes[i].voiceover, voice: document.getElementById(\'voice-select\').value }),'
)

# Fix resume from where it left - save sceneIndex to window
old_scene_advance = '''      // Advance scene
      if (sceneElapsed >= sceneDurations[sceneIndex]) {
        sceneIndex++;
        sceneStart = now;
        window.currentWord = 0;
        startTransition();
        if (sceneIndex < scriptData.scenes.length) {
          playSceneAudio(sceneIndex);
        }
      }'''

new_scene_advance = '''      // Advance scene
      if (sceneElapsed >= sceneDurations[sceneIndex]) {
        sceneIndex++;
        sceneStart = now;
        window.currentWord = 0;
        window.lastCompletedScene = sceneIndex; // Save progress
        startTransition();
        if (sceneIndex < scriptData.scenes.length) {
          playSceneAudio(sceneIndex);
        }
      }'''

content = content.replace(old_scene_advance, new_scene_advance, 1)

# Clear cache when making new video
old_clear = '''function makeAnother() {
  scriptData = null;
  videoBlob = null;
  recordedChunks = [];
  document.getElementById('video-topic').value = '';'''

new_clear = '''function makeAnother() {
  scriptData = null;
  videoBlob = null;
  recordedChunks = [];
  window.cachedAudioBuffers = null; // Clear voice cache for new video
  window.lastCompletedScene = 0;
  document.getElementById('video-topic').value = '';'''

content = content.replace(old_clear, new_clear, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Reliability fixes applied!")
