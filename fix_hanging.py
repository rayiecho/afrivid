with open('index.html', 'r') as f:
    content = f.read()

# FIX 1: Generation hanging - add timeout to TTS requests
old_tts = '''        const res = await fetch('https://yan-studio-worker.youngafricansn.workers.dev/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: scene.voiceover, voice: document.getElementById('voice-select').value })
        });
        const blob = await res.blob();
        audioBuffers[i] = await blob.arrayBuffer();
        addLog('success', `✓ Scene ${i+1} voice ready`);
      } catch(e) {
        addLog('error', `✗ Scene ${i+1} failed: ${e.message}`);
        audioBuffers[i] = null;
      }'''

new_tts = '''        const controller = new AbortController();
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
        }'''

content = content.replace(old_tts, new_tts, 1)

# FIX 2: Canvas freezing between scenes - fix renderLoop
old_render = '''  function renderLoop() {
    if (!isRecording) return;
    const now = Date.now();
    const totalElapsed = now - totalStart;
    const sceneElapsed = now - sceneStart;
    const totalProgress = Math.min(totalElapsed / totalDuration, 1);
    const pct = Math.round(totalProgress * 100);
    document.getElementById('progress-fill').style.width = pct + '%';
    document.getElementById('progress-pct').textContent = pct + '%';
    document.getElementById('progress-label-text').textContent = `Scene ${sceneIndex + 1} of ${scriptData.scenes.length}`;
    drawScene(canvas, scriptData.scenes[sceneIndex], totalProgress, window.currentWord || 0);
    if (sceneElapsed >= sceneDurations[sceneIndex]) {
      sceneIndex++;
      sceneStart = now;
      startTransition();
      if (sceneIndex < scriptData.scenes.length) {
        playSceneAudio(sceneIndex);
      }
    }
    if (totalProgress >= 1) {
      isRecording = false;
      mediaRecorder.stop();
      return;
    }
    requestAnimationFrame(renderLoop);
  }
  renderLoop();'''

new_render = '''  function renderLoop() {
    if (!isRecording) return;
    try {
      const now = Date.now();
      const totalElapsed = now - totalStart;
      const sceneElapsed = now - sceneStart;
      const totalProgress = Math.min(totalElapsed / totalDuration, 1);
      const pct = Math.round(totalProgress * 100);

      // Safe UI updates
      const pf = document.getElementById('progress-fill');
      const pp = document.getElementById('progress-pct');
      const pl = document.getElementById('progress-label-text');
      if (pf) pf.style.width = pct + '%';
      if (pp) pp.textContent = pct + '%';
      if (pl) pl.textContent = `Scene ${Math.min(sceneIndex + 1, scriptData.scenes.length)} of ${scriptData.scenes.length}`;

      // Draw current scene safely
      if (scriptData.scenes[sceneIndex]) {
        drawScene(canvas, scriptData.scenes[sceneIndex], totalProgress, window.currentWord || 0);
      }

      // Advance scene
      if (sceneElapsed >= sceneDurations[sceneIndex]) {
        sceneIndex++;
        sceneStart = now;
        window.currentWord = 0;
        startTransition();
        if (sceneIndex < scriptData.scenes.length) {
          playSceneAudio(sceneIndex);
        }
      }

      // Check completion
      if (totalProgress >= 1 || sceneIndex >= scriptData.scenes.length) {
        isRecording = false;
        setTimeout(() => {
          if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
          }
        }, 500);
        return;
      }
    } catch(e) {
      console.error('Render error:', e);
      // Don't stop - keep rendering
    }
    requestAnimationFrame(renderLoop);
  }
  renderLoop();'''

content = content.replace(old_render, new_render, 1)

# FIX 3: Download hanging - add safety check on finishVideo
old_finish = '''function finishVideo() {
  const blob = new Blob(recordedChunks, { type: 'video/webm' });'''

new_finish = '''function finishVideo() {
  if (!recordedChunks || recordedChunks.length === 0) {
    addLog('error', '✗ No video data recorded. Please try again.');
    document.getElementById('generate-btn') && (document.getElementById('generate-btn').disabled = false);
    return;
  }
  const blob = new Blob(recordedChunks, { type: 'video/webm' });'''

content = content.replace(old_finish, new_finish, 1)

# FIX 4: Add stop button during generation
old_stop = '''          <button class="btn btn-outline" id="btn-stop" onclick="stopRecording()" style="display:none;">⏹ Stop</button>'''
new_stop = '''          <button class="btn btn-outline" id="btn-stop" onclick="stopRecording()" style="background:rgba(230,51,41,0.15);border-color:rgba(230,51,41,0.4);color:#E63329;">⏹ Stop Recording</button>'''
content = content.replace(old_stop, new_stop, 1)

# FIX 5: Make stopRecording more robust
old_stop_fn = '''function stopRecording() {
  isRecording = false;
  if (mediaRecorder && mediaRecorder.state !== \'inactive\') {
    mediaRecorder.stop();
  }
}'''

new_stop_fn = '''function stopRecording() {
  isRecording = false;
  if (window.wordTimer) clearInterval(window.wordTimer);
  setTimeout(() => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
    }
  }, 300);
  addLog('info', '⏹ Recording stopped');
}'''

content = content.replace(old_stop_fn, new_stop_fn, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ All hanging fixes applied!")
