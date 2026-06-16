// AfriVid Global Limit System v2
// Independent monthly counters per tool

window.AFRIVID_LIMITS = {
  creator_video:      { max: 3, period: 'month', field: 'creator_video' },
  aieditor_session:   { max: 3, period: 'month', field: 'aieditor_session' },
  aieditor_translate: { max: 3, period: 'month', field: 'aieditor_translate' },
  aieditor_captions:  { max: 3, period: 'week',  field: 'aieditor_captions' },
  editor_session:     { max: 3, period: 'month', field: 'editor_session' },
  editor_captions:    { max: 3, period: 'week',  field: 'editor_captions' },
  editor_combine:     { max: 3, period: 'month', field: 'editor_combine' },
  editor_youtube:     { max: 3, period: 'month', field: 'editor_youtube' },
  editor_noise:       { max: 3, period: 'month', field: 'editor_noise' },
};

function _getMonthKey() {
  const n = new Date();
  return `lim_${n.getFullYear()}_${String(n.getMonth()+1).padStart(2,'0')}`;
}

function _getWeekKey() {
  const n = new Date();
  const start = new Date(n.getFullYear(), 0, 1);
  const week = Math.ceil(((n - start) / 86400000 + start.getDay() + 1) / 7);
  return `lim_w_${n.getFullYear()}_${String(week).padStart(2,'0')}`;
}

window.checkAfriVidLimit = async function(action) {
  console.log("[Limit] Checking:", action, "User:", window.currentUser?.email);
  // Wait for auth to be ready
  if (!window.currentUser) {
    // Check if user is stored elsewhere
    const user = window.currentUser || window._currentUser;
    if (!user) {
      if (window.showLogin) showLogin('Sign in to continue');
      return false;
    }
  }
  // Block unverified emails from using any tool
  if (!window.currentUser.emailVerified) {
    alert('⚠ Please verify your email first. Check your inbox for the verification link from AfriVid Studio.');
    return false;
  }

  try {
    const {initializeApp, getApps} = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js');
    const {getFirestore, doc, getDoc, updateDoc, increment} = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
    const cfg = {apiKey:"AIzaSyBDgcY4SYAOdG2QCPZYCEJRPaQNQZm6BI0",authDomain:"afrivid-studio.firebaseapp.com",projectId:"afrivid-studio"};
    const app = getApps().length ? getApps()[0] : initializeApp(cfg);
    const db = getFirestore(app);

    // Fetch fresh user data
    const snap = await getDoc(doc(db, 'studio_users', window.currentUser.uid));
    if (!snap.exists()) return true;
    const data = snap.data();

    // Pro users — unlimited
    if (data.plan === 'pro') return true;

    // Get limit config
    const limitCfg = window.AFRIVID_LIMITS[action];
    if (!limitCfg) return true;

    // Get period key
    const periodKey = limitCfg.period === 'week' ? _getWeekKey() : _getMonthKey();
    const fieldKey = `${periodKey}_${limitCfg.field}`;

    // Custom admin limit
    const customMax = data[`custom_${limitCfg.field}_limit`] || limitCfg.max;

    // Get current usage
    let used = data[fieldKey] || 0;

    // Fallback for creator_video - check old videosGenerated for existing users
    if (action === 'creator_video' && data.videosGenerated) {
      const totalUsed = data.videosGenerated || 0;
      const oldLimit = data.betaLimit || 3;
      // Use whichever is higher - old total or new monthly
      if (totalUsed >= oldLimit) used = customMax;
    }

    if (used >= customMax) {
      if (window.showUpgradeModal) showUpgradeModal(action);
      return false;
    }

    // Increment usage
    await updateDoc(doc(db, 'studio_users', window.currentUser.uid), {
      [fieldKey]: increment(1)
    });

    // Refresh usage display if available
    if (window.loadAIEditorUsage) loadAIEditorUsage();
    if (window.loadEditorUsage) loadEditorUsage();
    if (window.loadCreatorUsage) loadCreatorUsage();

    return true;

  } catch(e) {
    console.error('[AfriVid Limit]', e.message);
    return true;
  }
};
// AfriVid Limit System v2.1
