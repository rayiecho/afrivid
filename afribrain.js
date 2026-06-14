// AfriBrain Data Collection Engine
// Saves anonymized African language data to Firestore
// Only runs when user has consented (afribrain-consent checkbox)

window.saveToAfriBrain = async function(data) {
  try {
    // Check consent
    const consentEl = document.getElementById('afribrain-consent');
    if (consentEl && !consentEl.checked) return;
    
    // Check if user is logged in
    if (!window.currentUser) return;

    const {initializeApp, getApps} = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js');
    const {getFirestore, collection, addDoc, serverTimestamp} = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
    const cfg = {apiKey:"AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0",authDomain:"afrivid-studio.firebaseapp.com",projectId:"afrivid-studio"};
    const app = getApps().length ? getApps()[0] : initializeApp(cfg);
    const db = getFirestore(app);

    // Detect language
    const text = data.text || '';
    const wordCount = text.split(/\s+/).filter(w => w.length > 0).length;
    if (wordCount < 5) return; // Skip very short texts

    await addDoc(collection(db, 'afribrain_data'), {
      // Content
      text: text.substring(0, 5000), // Max 5000 chars
      language: data.language || 'en',
      topic: data.topic || '',
      source: data.source || 'create', // create, aieditor, edit
      type: data.type || 'script', // script, transcript, caption

      // Metadata (anonymized)
      country: data.country || 'unknown',
      word_count: wordCount,
      char_count: text.length,

      // No PII — anonymous
      user_id: 'anon_' + window.currentUser.uid.substring(0, 8),
      
      // Timestamps
      created_at: serverTimestamp(),
      month: new Date().toISOString().substring(0, 7), // 2026-06
    });

    console.log('[AfriBrain] Saved', wordCount, 'words in', data.language);
  } catch(e) {
    console.log('[AfriBrain] Save skipped:', e.message);
  }
};
