with open('index.html', 'r') as f:
    content = f.read()

old_admin_func = "  window.loadAdminDashboard = async function() {"

new_admin_func = '''  // ── FULL ADMIN SYSTEM ──
  let adminRefreshInterval = null;
  let paymentEnabled = false;

  window.loadAdminDashboard = async function() {
    ['create','enhance','library','photo'].forEach(t => {
      const s = document.getElementById('section-'+t);
      if(s) s.classList.remove('active');
    });
    ['create','enhance','library','photo','admin'].forEach(t => {
      const b = document.getElementById('sidebar-'+t);
      if(b) b.classList.toggle('active', t === 'admin');
    });

    let adminSection = document.getElementById('section-admin');
    if (!adminSection) {
      adminSection = document.createElement('div');
      adminSection.className = 'main-section active';
      adminSection.id = 'section-admin';
      document.querySelector('.main').appendChild(adminSection);
    } else {
      adminSection.className = 'main-section active';
    }

    adminSection.innerHTML = `
      <div class="card">
        <div class="card-title">
          <div class="card-title-icon">⚙</div>Admin Dashboard
          <div style="margin-left:auto;display:flex;gap:0.75rem;align-items:center;">
            <span id="admin-last-refresh" style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);"></span>
            <button onclick="loadAdminDashboard()" style="background:rgba(245,166,35,0.1);border:1px solid var(--border);color:var(--gold);padding:0.35rem 0.75rem;border-radius:6px;font-size:0.75rem;cursor:pointer;font-family:var(--font-mono);">↺ Refresh</button>
          </div>
        </div>
      </div>
      <div id="admin-content" style="display:flex;align-items:center;justify-content:center;padding:4rem;color:var(--muted);font-family:var(--font-mono);">Loading...</div>
    `;

    await renderAdminContent();

    // Auto refresh every 30s
    if (adminRefreshInterval) clearInterval(adminRefreshInterval);
    adminRefreshInterval = setInterval(renderAdminContent, 30000);
  };

  async function renderAdminContent() {
    const container = document.getElementById('admin-content');
    if (!container) return;

    try {
      const [usersSnap, videosSnap, feedbackSnap, configSnap] = await Promise.all([
        getDocs(query(collection(db, 'studio_users'), orderBy('videosGenerated', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_videos'), orderBy('createdAt', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_feedback'), orderBy('createdAt', 'desc'), limit(50))),
        getDoc(doc(db, 'studio_config', 'settings')).catch(() => null)
      ]);

      // Load config
      const config = configSnap?.exists() ? configSnap.data() : {};
      paymentEnabled = config.paymentEnabled || false;
      const betaLimit = config.globalBetaLimit || 10;
      const maintenanceMode = config.maintenanceMode || false;

      // Calculate stats
      const totalVideos = usersSnap.docs.reduce((s,d) => s + (d.data().videosGenerated||0), 0);
      const avgRating = feedbackSnap.docs.length ?
        (feedbackSnap.docs.reduce((s,d) => s+(d.data().rating||0), 0) / feedbackSnap.docs.length).toFixed(1) : '—';
      const paidUsers = usersSnap.docs.filter(d => d.data().plan === 'paid').length;
      const today = new Date().toDateString();
      const activeToday = usersSnap.docs.filter(d => {
        const last = d.data().lastVideoAt?.toDate?.();
        return last && last.toDateString() === today;
      }).length;

      // Videos per day (last 7 days)
      const now = Date.now();
      const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
      const videosPerDay = Array(7).fill(0);
      videosSnap.docs.forEach(d => {
        const created = d.data().createdAt?.toDate?.();
        if (created) {
          const daysAgo = Math.floor((now - created.getTime()) / 86400000);
          if (daysAgo < 7) videosPerDay[6 - daysAgo]++;
        }
      });
      const dayLabels = Array.from({length:7}, (_,i) => {
        const d = new Date(now - (6-i)*86400000);
        return days[d.getDay()];
      });
      const maxBar = Math.max(...videosPerDay, 1);

      document.getElementById('admin-last-refresh').textContent = 'Last: ' + new Date().toLocaleTimeString();

      container.innerHTML = `
        <!-- STATS GRID -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;">
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${usersSnap.size}</div>
            <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">TOTAL USERS</div>
          </div>
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${totalVideos}</div>
            <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">VIDEOS CREATED</div>
          </div>
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${activeToday}</div>
            <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">ACTIVE TODAY</div>
          </div>
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:${avgRating >= 4 ? '#74C69D' : '#F5A623'};">${avgRating}⭐</div>
            <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">AVG RATING</div>
          </div>
        </div>

        <!-- CHART + CONTROLS ROW -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.5rem;">

          <!-- VIDEOS PER DAY CHART -->
          <div class="card">
            <div class="card-title"><div class="card-title-icon">📊</div>Videos This Week</div>
            <div style="display:flex;align-items:flex-end;gap:8px;height:120px;padding:0.5rem 0;">
              ${videosPerDay.map((v,i) => `
                <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;">
                  <span style="font-size:0.65rem;color:var(--gold);font-family:var(--font-mono);">${v||''}</span>
                  <div style="width:100%;background:${v > 0 ? 'linear-gradient(180deg,#F5A623,#E8931A)' : 'var(--border2)'};border-radius:4px 4px 0 0;height:${Math.max((v/maxBar)*80,4)}px;transition:height 0.3s;"></div>
                  <span style="font-size:0.65rem;color:var(--muted);font-family:var(--font-mono);">${dayLabels[i]}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- SYSTEM CONTROLS -->
          <div class="card">
            <div class="card-title"><div class="card-title-icon">🔧</div>System Controls</div>
            <div style="display:flex;flex-direction:column;gap:1rem;">

              <!-- Payment Toggle -->
              <div style="display:flex;align-items:center;justify-content:space-between;padding:0.85rem;background:var(--navy3);border-radius:10px;">
                <div>
                  <div style="font-size:0.85rem;font-weight:700;color:var(--white);">Payment System</div>
                  <div style="font-size:0.72rem;color:var(--muted);margin-top:2px;">${paymentEnabled ? '✅ Enabled — users can pay' : '⏸ Disabled — beta mode'}</div>
                </div>
                <button onclick="togglePayment(${paymentEnabled})" style="padding:0.5rem 1rem;border-radius:8px;border:none;font-weight:700;font-size:0.78rem;cursor:pointer;font-family:var(--font-mono);background:${paymentEnabled ? 'rgba(230,51,41,0.2)' : 'rgba(116,198,157,0.2)'};color:${paymentEnabled ? '#E63329' : '#74C69D'};">
                  ${paymentEnabled ? 'DISABLE' : 'ENABLE'}
                </button>
              </div>

              <!-- Maintenance Mode -->
              <div style="display:flex;align-items:center;justify-content:space-between;padding:0.85rem;background:var(--navy3);border-radius:10px;">
                <div>
                  <div style="font-size:0.85rem;font-weight:700;color:var(--white);">Maintenance Mode</div>
                  <div style="font-size:0.72rem;color:var(--muted);margin-top:2px;">${maintenanceMode ? '🔴 ON — users see maintenance page' : '🟢 OFF — platform is live'}</div>
                </div>
                <button onclick="toggleMaintenance(${maintenanceMode})" style="padding:0.5rem 1rem;border-radius:8px;border:none;font-weight:700;font-size:0.78rem;cursor:pointer;font-family:var(--font-mono);background:${maintenanceMode ? 'rgba(230,51,41,0.2)' : 'rgba(245,166,35,0.1)'};color:${maintenanceMode ? '#E63329' : '#F5A623'};">
                  ${maintenanceMode ? 'TURN OFF' : 'TURN ON'}
                </button>
              </div>

              <!-- Global Beta Limit -->
              <div style="display:flex;align-items:center;justify-content:space-between;padding:0.85rem;background:var(--navy3);border-radius:10px;">
                <div>
                  <div style="font-size:0.85rem;font-weight:700;color:var(--white);">Global Beta Limit</div>
                  <div style="font-size:0.72rem;color:var(--muted);margin-top:2px;">Videos per user during beta</div>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                  <button onclick="adjustGlobalLimit(${betaLimit}, -5)" style="background:var(--border2);border:none;color:var(--white);width:28px;height:28px;border-radius:6px;cursor:pointer;font-weight:700;">−</button>
                  <span style="font-family:var(--font-mono);font-size:1rem;font-weight:700;color:var(--gold);min-width:28px;text-align:center;">${betaLimit}</span>
                  <button onclick="adjustGlobalLimit(${betaLimit}, 5)" style="background:var(--gold);border:none;color:var(--navy);width:28px;height:28px;border-radius:6px;cursor:pointer;font-weight:700;">+</button>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- USERS TABLE -->
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-title"><div class="card-title-icon">👥</div>Users
            <span style="margin-left:auto;font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">${usersSnap.size} registered · ${paidUsers} paid</span>
          </div>
          <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
              <thead>
                <tr style="border-bottom:1px solid var(--border2);">
                  <th style="text-align:left;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">NAME</th>
                  <th style="text-align:left;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">EMAIL</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">VIDEOS</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">LIMIT</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">PLAN</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">JOINED</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.68rem;">ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                ${usersSnap.docs.map(d => {
                  const u = d.data();
                  const uid = d.id;
                  const used = u.videosGenerated || 0;
                  const limit = u.betaLimit || betaLimit;
                  const pct = Math.min(Math.round((used/limit)*100), 100);
                  const barColor = pct >= 90 ? '#E63329' : pct >= 70 ? '#F5A623' : '#74C69D';
                  const joined = u.joinedAt?.toDate?.()?.toLocaleDateString() || '—';
                  const lastVideo = u.lastVideoAt?.toDate?.()?.toLocaleDateString() || '—';
                  return `<tr style="border-bottom:1px solid rgba(255,255,255,0.03);" onmouseover="this.style.background='rgba(245,166,35,0.03)'" onmouseout="this.style.background='none'">
                    <td style="padding:0.85rem 0.5rem;font-weight:600;color:var(--white);">${u.name || '—'}</td>
                    <td style="padding:0.85rem 0.5rem;color:var(--muted);font-size:0.75rem;">${u.email || ''}</td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <div style="font-weight:700;color:var(--gold);font-family:var(--font-mono);">${used}/${limit}</div>
                      <div style="height:3px;background:var(--border2);border-radius:2px;margin-top:4px;"><div style="height:100%;width:${pct}%;background:${barColor};border-radius:2px;"></div></div>
                    </td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <div style="display:flex;align-items:center;gap:4px;justify-content:center;">
                        <button onclick="adjustLimit('${uid}',${limit},-5)" style="background:var(--border2);border:none;color:var(--white);width:22px;height:22px;border-radius:4px;cursor:pointer;font-size:0.8rem;">−</button>
                        <span style="font-family:var(--font-mono);font-size:0.78rem;min-width:20px;text-align:center;color:var(--white);">${limit}</span>
                        <button onclick="adjustLimit('${uid}',${limit},5)" style="background:var(--gold);border:none;color:var(--navy);width:22px;height:22px;border-radius:4px;cursor:pointer;font-size:0.8rem;font-weight:700;">+</button>
                      </div>
                    </td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <select onchange="changePlan('${uid}',this.value)" style="background:var(--navy3);border:1px solid var(--border2);color:var(--white);padding:0.25rem 0.5rem;border-radius:6px;font-size:0.72rem;font-family:var(--font-mono);cursor:pointer;">
                        <option value="beta" ${u.plan==='beta'?'selected':''}>beta</option>
                        <option value="paid" ${u.plan==='paid'?'selected':''}>paid</option>
                        <option value="blocked" ${u.plan==='blocked'?'selected':''}>blocked</option>
                      </select>
                    </td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);">${joined}</td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <button onclick="resetUserVideos('${uid}')" style="font-size:0.68rem;padding:0.25rem 0.5rem;background:rgba(245,166,35,0.1);border:1px solid rgba(245,166,35,0.3);color:var(--gold);border-radius:4px;cursor:pointer;font-family:var(--font-mono);">Reset</button>
                    </td>
                  </tr>`;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- RECENT VIDEOS -->
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-title"><div class="card-title-icon">🎬</div>Recent Videos</div>
          ${videosSnap.docs.length === 0 ?
            '<div style="text-align:center;color:var(--muted);padding:2rem;font-family:var(--font-mono);font-size:0.78rem;">// No videos yet</div>' :
            `<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:0.75rem;">
              ${videosSnap.docs.slice(0,10).map(d => {
                const v = d.data();
                const date = v.createdAt?.toDate?.()?.toLocaleDateString() || '—';
                return `<div style="padding:0.85rem;background:var(--navy3);border-radius:10px;border:1px solid var(--border2);">
                  <div style="font-size:0.85rem;font-weight:600;color:var(--white);margin-bottom:4px;">${v.title || 'Untitled'}</div>
                  <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">${v.userEmail||''}</div>
                  <div style="display:flex;justify-content:space-between;margin-top:6px;">
                    <span style="font-size:0.68rem;color:var(--gold);font-family:var(--font-mono);">${v.duration||0}s</span>
                    <span style="font-size:0.68rem;color:var(--muted);font-family:var(--font-mono);">${date}</span>
                  </div>
                </div>`;
              }).join('')}
            </div>`
          }
        </div>

        <!-- PAYMENT SECTION -->
        <div class="card" style="margin-bottom:1.5rem;border:1px solid ${paymentEnabled ? 'rgba(116,198,157,0.3)' : 'var(--border2)'};">
          <div class="card-title"><div class="card-title-icon">💳</div>Payment System
            <span style="margin-left:0.75rem;font-size:0.7rem;padding:0.2rem 0.6rem;border-radius:50px;font-family:var(--font-mono);background:${paymentEnabled ? 'rgba(116,198,157,0.15)' : 'rgba(245,166,35,0.1)'};color:${paymentEnabled ? '#74C69D' : '#F5A623'};">${paymentEnabled ? 'LIVE' : 'BETA — DISABLED'}</span>
          </div>
          ${paymentEnabled ? `
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem;">
              <div style="background:var(--navy3);border-radius:12px;padding:1.25rem;text-align:center;">
                <div style="font-size:1.8rem;font-weight:800;color:#74C69D;">$${paidUsers * 5}</div>
                <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">MONTHLY REVENUE</div>
              </div>
              <div style="background:var(--navy3);border-radius:12px;padding:1.25rem;text-align:center;">
                <div style="font-size:1.8rem;font-weight:800;color:var(--gold);">${paidUsers}</div>
                <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">PAID USERS</div>
              </div>
              <div style="background:var(--navy3);border-radius:12px;padding:1.25rem;text-align:center;">
                <div style="font-size:1.8rem;font-weight:800;color:var(--white);">${usersSnap.size - paidUsers}</div>
                <div style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">FREE USERS</div>
              </div>
            </div>
          ` : `
            <div style="padding:1.5rem;background:var(--navy3);border-radius:12px;text-align:center;">
              <div style="font-size:0.88rem;color:var(--muted);margin-bottom:1rem;line-height:1.6;">Payment is disabled during beta. Enable it when you're ready to charge users.<br>Plans: <strong style="color:var(--white);">Free (10 videos)</strong> · <strong style="color:var(--gold);">$5/month (unlimited)</strong></div>
              <button onclick="togglePayment(false)" style="background:linear-gradient(135deg,#74C69D,#2D8A5E);border:none;color:#fff;padding:0.85rem 2rem;border-radius:10px;font-weight:700;cursor:pointer;font-family:var(--font-display);font-size:0.9rem;">🚀 Enable Payment System</button>
            </div>
          `}
        </div>

        <!-- FEEDBACK -->
        <div class="card">
          <div class="card-title"><div class="card-title-icon">💬</div>Feedback
            <span style="margin-left:auto;font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">${feedbackSnap.size} responses · avg ${avgRating}⭐</span>
          </div>
          ${feedbackSnap.docs.length === 0 ?
            '<div style="text-align:center;color:var(--muted);padding:2rem;font-family:var(--font-mono);font-size:0.78rem;">// No feedback yet</div>' :
            feedbackSnap.docs.map(d => {
              const f = d.data();
              const date = f.createdAt?.toDate?.()?.toLocaleDateString() || '';
              return `<div style="padding:1rem;background:var(--navy3);border-radius:10px;margin-bottom:0.75rem;border-left:3px solid ${(f.rating||0)>=4?'#74C69D':(f.rating||0)>=3?'#F5A623':'#E63329'};">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                  <span style="font-size:0.82rem;font-weight:600;color:var(--white);">${f.userEmail||'Anonymous'}</span>
                  <div style="display:flex;align-items:center;gap:0.75rem;">
                    <span style="font-size:0.82rem;">${'⭐'.repeat(f.rating||0)}</span>
                    <span style="font-size:0.7rem;color:var(--muted);font-family:var(--font-mono);">${date}</span>
                  </div>
                </div>
                <div style="font-size:0.82rem;color:var(--muted);line-height:1.6;">${f.message||'No message'}</div>
              </div>`;
            }).join('')
          }
        </div>
      `;

    } catch(e) {
      if (container) container.innerHTML = `<div class="card"><div style="color:#E63329;font-family:var(--font-mono);font-size:0.82rem;">Error: ${e.message}</div></div>`;
    }
  }

  // ── ADMIN CONTROLS ──
  window.togglePayment = async function(current) {
    const msg = current ? 'Disable payment system? Users will not be charged.' : 'Enable payment system? Users will be asked to pay after beta limit.';
    if (!confirm(msg)) return;
    try {
      await setDoc(doc(db, 'studio_config', 'settings'), { paymentEnabled: !current }, { merge: true });
      await renderAdminContent();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.toggleMaintenance = async function(current) {
    if (!confirm(current ? 'Turn off maintenance mode?' : 'Turn on maintenance mode? Users will see a maintenance page.')) return;
    try {
      await setDoc(doc(db, 'studio_config', 'settings'), { maintenanceMode: !current }, { merge: true });
      await renderAdminContent();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.adjustGlobalLimit = async function(current, delta) {
    const newLimit = Math.max(1, current + delta);
    try {
      await setDoc(doc(db, 'studio_config', 'settings'), { globalBetaLimit: newLimit }, { merge: true });
      await renderAdminContent();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.adjustLimit = async function(uid, current, delta) {
    try {
      await updateDoc(doc(db, 'studio_users', uid), { betaLimit: Math.max(1, current + delta) });
      await renderAdminContent();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.changePlan = async function(uid, plan) {
    try {
      await updateDoc(doc(db, 'studio_users', uid), { plan });
      await renderAdminContent();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.resetUserVideos = async function(uid) {
    if (!confirm('Reset this user video count to 0?')) return;
    try {
      await updateDoc(doc(db, 'studio_users', uid), { videosGenerated: 0 });
      await renderAdminContent();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.loadAdminDashboard = async function() {'''

content = content.replace(
    '  window.loadAdminDashboard = async function() {',
    new_admin_func
)

# Add setDoc to imports
content = content.replace(
    "import { getFirestore, doc, setDoc, getDoc, updateDoc, increment, collection, addDoc, serverTimestamp, query, orderBy, limit, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';",
    "import { getFirestore, doc, setDoc, getDoc, updateDoc, increment, collection, addDoc, serverTimestamp, query, orderBy, limit, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';"
)

# Add studio_config rule to Firestore
with open('index.html', 'w') as f:
    f.write(content)
print("✅ Full admin system built!")
