// ── CHUNKED UPLOAD ────────────────────────────────────────────────────────────
// Shared by compress.html and studio-editor.html.
//
// A direct browser PUT straight to R2's own storage domain (the old /presign-upload flow)
// was failing to send any data at all for some users on connections otherwise confirmed
// stable — something about that specific cross-origin destination, not bandwidth. This
// routes the upload through our own Cloud Run server instead, in small pieces:
//   /upload-init      -> starts a real S3 multipart upload on R2, returns an upload_id
//   /upload-chunk     -> one piece (each its own short request, retried on its own)
//   /upload-complete  -> assembles the parts into the final object, returns its public URL
// Every chunk goes to the same host every other call on these pages already reaches
// successfully, so a bad chunk costs a quick retry instead of restarting a multi-hundred-MB
// transfer from zero. R2's multipart API requires every part but the last to be >= 5MB.
(function () {
  const CHUNK_SIZE = 6 * 1024 * 1024;
  const CHUNK_RETRY_ATTEMPTS = 4;
  const CHUNK_TIMEOUT_MS = 30000;

  function postJSON(url, body) {
    return fetch(url, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    }).then((r) => r.json());
  }

  function uploadChunkOnce(apiBase, job) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const qs = `job_id=${job.jobId}&key=${encodeURIComponent(job.key)}&upload_id=${encodeURIComponent(job.uploadId)}&part_number=${job.partNumber}`;
      xhr.open('POST', `${apiBase}/upload-chunk?${qs}`);
      xhr.timeout = CHUNK_TIMEOUT_MS;
      xhr.ontimeout = () => reject(new Error('Piece timed out'));
      xhr.onload = () => {
        if (xhr.status < 200 || xhr.status >= 300) { reject(new Error('Piece failed: ' + xhr.status)); return; }
        try {
          const data = JSON.parse(xhr.responseText);
          if (data.error) { reject(new Error(data.error)); return; }
          resolve(data.etag);
        } catch (e) { reject(new Error('Bad response for piece')); }
      };
      xhr.onerror = () => reject(new Error('Piece failed — network error'));
      xhr.send(job.blob);
    });
  }

  async function uploadChunkWithRetry(apiBase, job, onStatus) {
    let lastErr;
    for (let attempt = 0; attempt < CHUNK_RETRY_ATTEMPTS; attempt++) {
      try {
        if (attempt > 0 && onStatus) onStatus(`Retrying piece ${job.partNumber} (attempt ${attempt + 1}/${CHUNK_RETRY_ATTEMPTS})...`);
        return await uploadChunkOnce(apiBase, job);
      } catch (e) {
        lastErr = e;
        await new Promise((r) => setTimeout(r, 1500 * (attempt + 1)));
      }
    }
    throw lastErr;
  }

  // onProgress(pct 0-100), onStatus(string) are both optional.
  async function chunkedUpload(apiBase, file, onProgress, onStatus) {
    const init = await postJSON(`${apiBase}/upload-init`, {
      filename: file.name, content_type: file.type || 'video/mp4',
    });
    if (init.error) throw new Error(init.error);
    const { job_id: jobId, key, upload_id: uploadId } = init;

    const totalParts = Math.max(1, Math.ceil(file.size / CHUNK_SIZE));
    const parts = [];
    try {
      for (let i = 0; i < totalParts; i++) {
        const start = i * CHUNK_SIZE;
        const blob = file.slice(start, Math.min(file.size, start + CHUNK_SIZE));
        const partNumber = i + 1;
        const etag = await uploadChunkWithRetry(apiBase, { jobId, key, uploadId, partNumber, blob }, onStatus);
        parts.push({ part_number: partNumber, etag });
        if (onProgress) onProgress(Math.round((partNumber / totalParts) * 100));
      }
    } catch (e) {
      // Best-effort cleanup — never blocks surfacing the real error to the user.
      postJSON(`${apiBase}/upload-abort`, { job_id: jobId, key, upload_id: uploadId }).catch(() => {});
      throw new Error(`Upload failed at piece ${parts.length + 1} of ${totalParts}: ${e.message}`);
    }

    const complete = await postJSON(`${apiBase}/upload-complete`, { job_id: jobId, key, upload_id: uploadId, parts });
    if (complete.error) throw new Error(complete.error);
    return { job_id: jobId, public_url: complete.public_url };
  }

  window.chunkedUpload = chunkedUpload;
})();
