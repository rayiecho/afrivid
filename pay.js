// AfriVid Payment Modal
const PAYMENTS_URL = 'https://afrivid-payments.afrividstudio.workers.dev';

window.showUpgradeModal = async function(feature) {
  // Remove existing modal
  document.getElementById('afrivid-pay-modal')?.remove();

  const modal = document.createElement('div');
  modal.id = 'afrivid-pay-modal';
  modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:99999;display:flex;align-items:center;justify-content:center;padding:1rem;';
  
  modal.innerHTML = `
  <div style="background:#0D1117;border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:2rem;max-width:420px;width:100%;position:relative;">
    <button onclick="document.getElementById('afrivid-pay-modal').remove()" style="position:absolute;top:1rem;right:1rem;background:none;border:none;color:rgba(255,255,255,0.4);font-size:1.2rem;cursor:pointer;">✕</button>
    
    <div style="text-align:center;margin-bottom:1.5rem;">
      <div style="background:linear-gradient(135deg,#F5A623,#E8950F);color:#050A14;font-weight:900;font-size:0.75rem;padding:0.3rem 0.75rem;border-radius:20px;display:inline-block;margin-bottom:0.75rem;">✦ PRO PLAN</div>
      <div style="font-size:2.5rem;font-weight:900;font-family:'Syne',sans-serif;">$5<span style="font-size:1rem;color:rgba(255,255,255,0.5);">/month</span></div>
      <div style="color:rgba(255,255,255,0.5);font-size:0.85rem;margin-top:0.25rem;">≈ KES 650/month</div>
    </div>

    <ul style="list-style:none;margin-bottom:1.5rem;">
      ${['Unlimited video generation','All slide styles','Tutorial Maker','Browser Demo Recording','AI Editor — trim, silence removal','Priority processing','No watermark'].map(f=>`
      <li style="padding:0.4rem 0;color:rgba(255,255,255,0.7);font-size:0.85rem;display:flex;gap:0.5rem;align-items:center;">
        <span style="color:#74C69D;font-weight:900;">✓</span> ${f}
      </li>`).join('')}
    </ul>

    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin-bottom:1.5rem;">

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-bottom:1rem;">
      <div onclick="selectPayMethod('mpesa')" id="pay-mpesa" style="background:rgba(255,255,255,0.05);border:2px solid #F5A623;border-radius:8px;padding:0.75rem;cursor:pointer;text-align:center;">
        <div style="font-size:1.5rem;">📱</div>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);font-family:'Space Mono',monospace;margin-top:0.25rem;">M-Pesa</div>
      </div>
      <div onclick="selectPayMethod('card')" id="pay-card" style="background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);border-radius:8px;padding:0.75rem;cursor:pointer;text-align:center;">
        <div style="font-size:1.5rem;">💳</div>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);font-family:'Space Mono',monospace;margin-top:0.25rem;">Card</div>
      </div>
    </div>

    <div id="mpesa-fields">
      <label style="font-size:0.65rem;color:rgba(255,255,255,0.4);font-family:'Space Mono',monospace;letter-spacing:1px;margin-bottom:0.4rem;display:block;">M-PESA PHONE NUMBER</label>
      <input id="mpesa-phone" type="tel" placeholder="254712345678" style="width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#fff;padding:0.75rem;border-radius:8px;font-family:'Syne',sans-serif;font-size:0.9rem;outline:none;box-sizing:border-box;">
      <div style="color:rgba(255,255,255,0.3);font-size:0.7rem;font-family:'Space Mono',monospace;margin-top:0.4rem;">Format: 254712345678 (include country code)</div>
    </div>

    <div id="card-fields" style="display:none;">
      <div style="background:rgba(245,166,35,0.08);border:1px solid rgba(245,166,35,0.2);border-radius:8px;padding:1rem;text-align:center;color:rgba(255,255,255,0.5);font-size:0.85rem;">
        Card payments coming soon.<br>Use M-Pesa for now.
      </div>
    </div>

    <button id="pay-btn" onclick="processPayment()" style="width:100%;background:#F5A623;border:none;color:#050A14;padding:1rem;border-radius:10px;font-weight:900;cursor:pointer;font-family:'Syne',sans-serif;font-size:1rem;margin-top:1rem;">
      Pay KES 650 with M-Pesa
    </button>

    <div id="pay-status" style="display:none;margin-top:1rem;text-align:center;">
      <div id="pay-status-text" style="color:#F5A623;font-family:'Space Mono',monospace;font-size:0.8rem;"></div>
    </div>
  </div>`;

  document.body.appendChild(modal);
};

window.selectPayMethod = function(method) {
  document.getElementById('pay-mpesa').style.borderColor = method === 'mpesa' ? '#F5A623' : 'rgba(255,255,255,0.1)';
  document.getElementById('pay-card').style.borderColor = method === 'card' ? '#F5A623' : 'rgba(255,255,255,0.1)';
  document.getElementById('mpesa-fields').style.display = method === 'mpesa' ? 'block' : 'none';
  document.getElementById('card-fields').style.display = method === 'card' ? 'block' : 'none';
  window._payMethod = method;
};
window._payMethod = 'mpesa';

window.processPayment = async function() {
  const user = window.currentUser;
  if (!user) { alert('Please sign in first'); return; }
  
  const btn = document.getElementById('pay-btn');
  const status = document.getElementById('pay-status');
  const statusText = document.getElementById('pay-status-text');
  
  if (window._payMethod === 'mpesa') {
    const phone = document.getElementById('mpesa-phone')?.value?.trim().replace(/\s/g,'');
    if (!phone || phone.length < 12) { alert('Enter valid phone: 254712345678'); return; }
    
    btn.disabled = true; btn.textContent = 'Sending STK Push...';
    status.style.display = 'block';
    statusText.textContent = '📱 Check your phone for M-Pesa prompt...';
    
    try {
      const r = await fetch(`${PAYMENTS_URL}/mpesa-pay`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ phone, amount: 650, user_id: user.uid, plan: 'pro' })
      });
      const d = await r.json();
      
      if (d.ResponseCode === '0') {
        const checkoutId = d.CheckoutRequestID;
        statusText.textContent = '📱 Enter your M-Pesa PIN on your phone...';
        
        // Poll for payment status
        let attempts = 0;
        const poll = setInterval(async () => {
          attempts++;
          const s = await fetch(`${PAYMENTS_URL}/payment-status?id=${checkoutId}`);
          const sd = await s.json();
          
          if (sd.status === 'completed') {
            clearInterval(poll);
            // Activate subscription
            await fetch(`${PAYMENTS_URL}/activate-subscription`, {
              method: 'POST',
              headers: {'Content-Type':'application/json'},
              body: JSON.stringify({ user_id: user.uid, plan: 'pro', receipt: sd.receipt })
            });
            statusText.textContent = '🎉 Payment successful! AfriVid Pro activated!';
            btn.textContent = '✓ Pro Activated';
            setTimeout(() => document.getElementById('afrivid-pay-modal')?.remove(), 3000);
          } else if (sd.status === 'failed' || attempts > 24) {
            clearInterval(poll);
            statusText.textContent = '❌ Payment failed or timed out. Try again.';
            btn.disabled = false; btn.textContent = 'Pay KES 650 with M-Pesa';
          } else {
            statusText.textContent = `📱 Waiting for payment... (${attempts * 5}s)`;
          }
        }, 5000);
      } else {
        statusText.textContent = '❌ Failed to send M-Pesa prompt. Try again.';
        btn.disabled = false; btn.textContent = 'Pay KES 650 with M-Pesa';
      }
    } catch(e) {
      statusText.textContent = '❌ Error: ' + e.message;
      btn.disabled = false; btn.textContent = 'Pay KES 650 with M-Pesa';
    }
  }
};
