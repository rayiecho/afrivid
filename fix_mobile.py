with open('index.html', 'r') as f:
    content = f.read()

old_css = """  @media (max-width:768px) {
    .sidebar { width:60px; }
    .sidebar-logo-text { display:none; }
    .sidebar-item span:not(.item-icon) { display:none; }
    .app-content { margin-left:60px; }
  }

  /* RESPONSIVE */
  @media (max-width: 768px) {
    .header { padding: 1rem 1.25rem; }
    .main { padding: 1.5rem 1rem; }
    .form-grid { grid-template-columns: 1fr; }
    .form-group.full { grid-column: span 1; }
    .steps-bar { flex-direction: column; border-radius: 14px; }
    .step-item { border-right: none; border-bottom: 1px solid var(--border2); }
    .step-item:last-child { border-bottom: none; }
  }"""

new_css = """  /* MOBILE NAV */
  .mobile-nav { display: none; }
  .mobile-topbar { display: none; }

  @media (max-width: 768px) {
    .sidebar { display: none !important; }
    .app-content { margin-left: 0 !important; padding: 0 0 80px 0 !important; }
    .main { padding: 1rem 0.75rem !important; }
    .mobile-topbar { display: block !important; }
    .header { padding: 0.85rem 1rem; }

    .steps-bar {
      flex-direction: row !important;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
      border-radius: 0 !important;
      background: transparent !important;
      border: none !important;
      gap: 8px;
      padding: 0 0 8px 0;
      margin-bottom: 1rem;
    }
    .steps-bar::-webkit-scrollbar { display: none; }
    .step-item {
      border-right: none !important;
      border-bottom: none !important;
      border: 1px solid var(--border2) !important;
      border-radius: 20px !important;
      padding: 0.5rem 1rem !important;
      flex-shrink: 0;
      white-space: nowrap;
      min-width: auto;
    }
    .step-item.active { border-color: rgba(245,166,35,0.4) !important; background: rgba(245,166,35,0.1) !important; }
    .step-item.done { border-color: rgba(45,138,94,0.3) !important; }
    .step-label { font-size: 0.75rem; }

    .form-grid { grid-template-columns: 1fr; }
    .form-group.full { grid-column: span 1; }
    .enhance-grid { grid-template-columns: 1fr; }
    .card { padding: 1rem; border-radius: 12px; }
    .btn-row { flex-direction: column; }
    .btn-row .btn { width: 100%; justify-content: center; }

    .mobile-nav {
      display: flex !important;
      position: fixed;
      bottom: 0; left: 0; right: 0;
      background: var(--navy2);
      border-top: 1px solid var(--border2);
      z-index: 200;
      padding-bottom: env(safe-area-inset-bottom, 0px);
    }
    .mobile-nav-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      padding: 10px 0 8px;
      background: none;
      border: none;
      color: rgba(248,249,252,0.35);
      font-family: var(--font-display);
      font-size: 10px;
      font-weight: 600;
      cursor: pointer;
      transition: color 0.2s;
      position: relative;
    }
    .mobile-nav-item.active { color: var(--gold); }
    .mobile-nav-item.active::after {
      content: '';
      position: absolute;
      top: 0; left: 50%;
      transform: translateX(-50%);
      width: 24px; height: 2px;
      background: var(--gold);
      border-radius: 0 0 2px 2px;
    }
    .mobile-nav-item svg { width: 22px; height: 22px; }
    #canvas-container { border-radius: 10px; }
    .download-card { padding: 1.25rem; }
    .upload-zone { padding: 2rem 1rem; }
    .mode-toggle { margin-bottom: 1rem; }
  }"""

if old_css in content:
    content = content.replace(old_css, new_css)
    with open('index.html', 'w') as f:
        f.write(content)
    print("✅ Mobile CSS updated successfully!")
else:
    print("❌ Still not found. Trying line count...")
    print("Total chars in file:", len(content))
