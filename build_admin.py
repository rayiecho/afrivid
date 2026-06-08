with open('index.html', 'r') as f:
    content = f.read()

# Replace old loadAdminDashboard with full system
old_admin = '''  window.loadAdminDashboard = async function() {
    // Switch to admin section
    ['create','enhance','library'].forEach(t => {
      const s = document.getElementById('section-'+t);
      const b = document.getElementById('tab-'+t);
      if(s) s.classList.remove('active');
      if(b) b.classList.remove('active');
    });
    document.getElementById('tab-admin').classList.add('active');

    // Load stats
    const usersSnap = await getDocs(query(collection(db, 'studio_users'), orderBy('videosGenerated', 'desc'), limit(50)));
    const videosSnap = await getDocs(query(collection(db, 'studio_videos'), orderBy('createdAt', 'desc'), limit(20)));
    const feedbackSnap = await getDocs(query(collection(db, 'studio_feedback'), orderBy('createdAt', 'desc'), limit(20)));

    let adminHTML = `
      <div class="card">
        <div class="card-title"><div class="card-title-icon">⚙️</div>Admin Dashboard</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem;">
          <div style="background:var(--navy3);border-radius:12px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:var(--gold);">${usersSnap.size}</div>
            <div style="font-size:0.78rem;color:var(--muted);font-family:var(--font-mono);">TOTAL USERS</div>
          </div>
          <div style="background:var(--navy3);border-radius:12px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:var(--gold);">${videosSnap.size}</div>
            <div style="font-size:0.78rem;color:var(--muted);font-family:var(--font-mono);">VIDEOS MADE</div>
          </div>
          <div style="background:var(--navy3);border-radius:12px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:var(--gold);">${feedbackSnap.size}</div>
            <div style="font-size:0.78rem;color:var(--muted);font-family:var(--font-mono);">FEEDBACKS</div>
          </div>
        </div>

        <div style="font-size:0.88rem;font-weight:700;margin-bottom:1rem;color:var(--gold);font-family:var(--font-mono);">TOP USERS</div>
        ${usersSnap.docs.map(d => {
          const u = d.data();
          return `<div style="display:flex;justify-content:space-between;padding:0.75rem;background:var(--navy3);border-radius:8px;margin-bottom:0.5rem;font-size:0.82rem;">
            <span>${u.name || u.email}</span>
            <span style="color:var(--gold);font-family:var(--font-mono);">${u.videosGenerated || 0} videos</span>
          </div>`;
        }).join('')}

        <div style="font-size:0.88rem;font-weight:700;margin:1.5rem 0 1rem;color:var(--gold);font-family:var(--font-mono);">RECENT FEEDBACK</div>
        ${feedbackSnap.docs.map(d => {
          const f = d.data();
          return `<div style="padding:0.75rem;background:var(--navy3);border-radius:8px;margin-bottom:0.5rem;font-size:0.82rem;">
            <div style="color:var(--gold);margin-bottom:0.25rem;">${'⭐'.repeat(f.rating || 0)} — ${f.userEmail}</div>
            <div style="color:var(--muted);">${f.message || ''}</div>
          </div>`;
        }).join('')}
      </div>`;

    let adminSection = document.getElementById('section-admin');
    if (!adminSection) {
      adminSection = document.createElement('div');
      adminSection.className = 'main-section active';
      adminSection.id = 'section-admin';
      document.querySelector('.main').appendChild(adminSection);
    } else {
      adminSection.className = 'main-section active';
    }
    adminSection.innerHTML = adminHTML;
  };'''

new_admin = '''  window.loadAdminDashboard = async function() {
    // Hide all sections
    ['create','enhance','library','photo'].forEach(t => {
      const s = document.getElementById('section-'+t);
      if(s) s.classList.remove('active');
    });
    ['create','enhance','library','photo','admin'].forEach(t => {
      const b = document.getElementById('sidebar-'+t);
      if(b) b.classList.toggle('active', t === 'admin');
    });

    // Get or create admin section
    let adminSection = document.getElementById('section-admin');
    if (!adminSection) {
      adminSection = document.createElement('div');
      adminSection.className = 'main-section active';
      adminSection.id = 'section-admin';
      document.querySelector('.main').appendChild(adminSection);
    } else {
      adminSection.className = 'main-section active';
    }

    adminSection.innerHTML = `<div class="card"><div class="card-title"><div class="card-title-icon">⚙</div>Loading admin data...</div></div>`;

    try {
      const [usersSnap, videosSnap, feedbackSnap] = await Promise.all([
        getDocs(query(collection(db, 'studio_users'), orderBy('videosGenerated', 'desc'), limit(100))),
        getDocs(query(collection(db, 'studio_videos'), orderBy('createdAt', 'desc'), limit(50))),
        getDocs(query(collection(db, 'studio_feedback'), orderBy('createdAt', 'desc'), limit(50)))
      ]);

      const totalVideos = usersSnap.docs.reduce((sum, d) => sum + (d.data().videosGenerated || 0), 0);
      const avgRating = feedbackSnap.docs.length ? 
        (feedbackSnap.docs.reduce((sum, d) => sum + (d.data().rating || 0), 0) / feedbackSnap.docs.length).toFixed(1) : 'N/A';

      adminSection.innerHTML = `
        <!-- STATS ROW -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;">
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${usersSnap.size}</div>
            <div style="font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">TOTAL USERS</div>
          </div>
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${totalVideos}</div>
            <div style="font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">VIDEOS CREATED</div>
          </div>
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${feedbackSnap.size}</div>
            <div style="font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">FEEDBACKS</div>
          </div>
          <div style="background:var(--navy2);border:1px solid var(--border2);border-radius:14px;padding:1.5rem;text-align:center;">
            <div style="font-size:2.2rem;font-weight:800;color:var(--gold);">${avgRating}⭐</div>
            <div style="font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);margin-top:0.25rem;">AVG RATING</div>
          </div>
        </div>

        <!-- USERS TABLE -->
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-title"><div class="card-title-icon">👥</div>Registered Users
            <span style="margin-left:auto;font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);">${usersSnap.size} total</span>
          </div>
          <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
              <thead>
                <tr style="border-bottom:1px solid var(--border2);">
                  <th style="text-align:left;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.7rem;font-weight:600;">USER</th>
                  <th style="text-align:left;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.7rem;font-weight:600;">EMAIL</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.7rem;font-weight:600;">VIDEOS</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.7rem;font-weight:600;">LIMIT</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.7rem;font-weight:600;">PLAN</th>
                  <th style="text-align:center;padding:0.75rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.7rem;font-weight:600;">ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                ${usersSnap.docs.map(d => {
                  const u = d.data();
                  const uid = d.id;
                  const used = u.videosGenerated || 0;
                  const limit = u.betaLimit || 10;
                  const pct = Math.round((used/limit)*100);
                  const barColor = pct >= 90 ? '#E63329' : pct >= 70 ? '#F5A623' : '#74C69D';
                  return `<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                    <td style="padding:0.85rem 0.5rem;font-weight:600;color:var(--white);">${u.name || 'Unknown'}</td>
                    <td style="padding:0.85rem 0.5rem;color:var(--muted);font-family:var(--font-mono);font-size:0.75rem;">${u.email || ''}</td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <div style="font-weight:700;color:var(--gold);">${used}/${limit}</div>
                      <div style="height:4px;background:var(--border2);border-radius:2px;margin-top:4px;width:60px;margin-left:auto;margin-right:auto;">
                        <div style="height:100%;width:${pct}%;background:${barColor};border-radius:2px;"></div>
                      </div>
                    </td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <div style="display:flex;align-items:center;gap:4px;justify-content:center;">
                        <button onclick="adjustLimit('${uid}', ${limit}, -5)" style="background:var(--border2);border:none;color:var(--white);width:24px;height:24px;border-radius:4px;cursor:pointer;font-size:0.85rem;">-</button>
                        <span style="font-family:var(--font-mono);font-size:0.82rem;min-width:24px;text-align:center;">${limit}</span>
                        <button onclick="adjustLimit('${uid}', ${limit}, 5)" style="background:var(--gold);border:none;color:var(--navy);width:24px;height:24px;border-radius:4px;cursor:pointer;font-size:0.85rem;font-weight:700;">+</button>
                      </div>
                    </td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <span style="font-size:0.72rem;padding:0.2rem 0.6rem;border-radius:50px;background:rgba(116,198,157,0.15);color:#74C69D;font-family:var(--font-mono);">${u.plan || 'beta'}</span>
                    </td>
                    <td style="padding:0.85rem 0.5rem;text-align:center;">
                      <button onclick="resetUserVideos('${uid}')" style="font-size:0.72rem;padding:0.3rem 0.6rem;background:rgba(245,166,35,0.1);border:1px solid rgba(245,166,35,0.3);color:var(--gold);border-radius:6px;cursor:pointer;font-family:var(--font-mono);">Reset</button>
                    </td>
                  </tr>`;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- RECENT VIDEOS -->
        <div class="card" style="margin-bottom:1.5rem;">
          <div class="card-title"><div class="card-title-icon">🎬</div>Recent Videos
            <span style="margin-left:auto;font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);">${videosSnap.size} recent</span>
          </div>
          ${videosSnap.docs.length === 0 ? '<div style="text-align:center;color:var(--muted);padding:2rem;font-family:var(--font-mono);font-size:0.78rem;">// No videos generated yet</div>' :
          videosSnap.docs.map(d => {
            const v = d.data();
            const date = v.createdAt?.toDate?.()?.toLocaleDateString() || 'Unknown';
            return `<div style="display:flex;justify-content:space-between;align-items:center;padding:0.85rem;background:var(--navy3);border-radius:8px;margin-bottom:0.5rem;">
              <div>
                <div style="font-size:0.85rem;font-weight:600;color:var(--white);">${v.title || 'Untitled'}</div>
                <div style="font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);margin-top:2px;">${v.userEmail || ''} · ${date}</div>
              </div>
              <span style="font-size:0.72rem;color:var(--gold);font-family:var(--font-mono);">${v.duration || 0}s</span>
            </div>`;
          }).join('')}
        </div>

        <!-- FEEDBACK -->
        <div class="card">
          <div class="card-title"><div class="card-title-icon">💬</div>User Feedback
            <span style="margin-left:auto;font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);">${feedbackSnap.size} responses · avg ${avgRating}⭐</span>
          </div>
          ${feedbackSnap.docs.length === 0 ? '<div style="text-align:center;color:var(--muted);padding:2rem;font-family:var(--font-mono);font-size:0.78rem;">// No feedback yet</div>' :
          feedbackSnap.docs.map(d => {
            const f = d.data();
            const date = f.createdAt?.toDate?.()?.toLocaleDateString() || '';
            const stars = '⭐'.repeat(f.rating || 0);
            return `<div style="padding:1rem;background:var(--navy3);border-radius:10px;margin-bottom:0.75rem;border-left:3px solid ${f.rating >= 4 ? '#74C69D' : f.rating >= 3 ? '#F5A623' : '#E63329'};">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                <span style="font-size:0.82rem;font-weight:600;color:var(--white);">${f.userEmail || 'Anonymous'}</span>
                <span style="font-size:0.72rem;color:var(--muted);font-family:var(--font-mono);">${date}</span>
              </div>
              <div style="font-size:0.88rem;margin-bottom:0.25rem;">${stars}</div>
              <div style="font-size:0.82rem;color:var(--muted);line-height:1.6;">${f.message || ''}</div>
            </div>`;
          }).join('')}
        </div>
      `;
    } catch(e) {
      adminSection.innerHTML = `<div class="card"><div style="color:var(--red);font-family:var(--font-mono);">Error loading admin data: ${e.message}</div></div>`;
    }
  };

  // ── ADMIN CONTROLS ──
  window.adjustLimit = async function(uid, currentLimit, delta) {
    try {
      const newLimit = Math.max(1, currentLimit + delta);
      await updateDoc(doc(db, 'studio_users', uid), { betaLimit: newLimit });
      loadAdminDashboard();
    } catch(e) { alert('Failed: ' + e.message); }
  };

  window.resetUserVideos = async function(uid) {
    if (!confirm('Reset this user\\'s video count to 0?')) return;
    try {
      await updateDoc(doc(db, 'studio_users', uid), { videosGenerated: 0 });
      loadAdminDashboard();
    } catch(e) { alert('Failed: ' + e.message); }
  };'''

content = content.replace(old_admin, new_admin, 1)

# Update checkVideoLimit to respect betaLimit field
old_limit = '''  async function checkVideoLimit() {
    if (!currentUser) return false;
    if (ADMIN_EMAILS.includes(currentUser.email)) return true;
    const used = userProfile?.videosGenerated || 0;
    if (used >= BETA_LIMIT) {
      alert(`You have reached the beta limit of ${BETA_LIMIT} videos. Thank you for testing AfriVid Studio! Full access coming soon.`);
      return false;
    }
    return true;
  }'''

new_limit = '''  async function checkVideoLimit() {
    if (!currentUser) return false;
    if (ADMIN_EMAILS.includes(currentUser.email)) return true;
    const used = userProfile?.videosGenerated || 0;
    const limit = userProfile?.betaLimit || BETA_LIMIT;
    if (used >= limit) {
      alert(`You have reached your limit of ${limit} videos. Contact support to increase your limit.`);
      return false;
    }
    return true;
  }'''

content = content.replace(old_limit, new_limit, 1)

with open('index.html', 'w') as f:
    f.write(content)
print("✅ Full admin dashboard built!")
