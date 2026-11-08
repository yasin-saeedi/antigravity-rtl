/**
 * Antigravity RTL & Smart Typography In-DOM Engine
 * Injected into the Antigravity desktop renderer window via CDP.
 * https://github.com/yasin-saeedi/antigravity-rtl
 */

(function () {
  window.__AG_RTL_LOADED__ = true;

  // 1. Settings & Appearance Subsystem
  const STORAGE_KEY = 'antigravity_appearance_settings';
  const DEFAULT_SETTINGS = {
    rtlEnabled: true,
    fontFamily: 'Vazirmatn',
    customFont: '',
    fontSize: 15,
    lineHeight: 1.75
  };

  function getSettings() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return Object.assign({}, DEFAULT_SETTINGS, JSON.parse(raw));
    } catch (e) {}
    return Object.assign({}, DEFAULT_SETTINGS);
  }

  function saveSettings(s) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
    } catch (e) {}
  }

  let currentSettings = getSettings();

  function getFontFamilyValue(fontName, customName) {
    switch (fontName) {
      case 'Shabnam':
        return "'Shabnam', 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
      case 'Sahel':
        return "'Sahel', 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
      case 'Samim':
        return "'Samim', 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
      case 'Custom':
        return customName ? `'${customName}', 'Vazirmatn', sans-serif` : "'Vazirmatn', sans-serif";
      case 'Vazirmatn':
      default:
        return "'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    }
  }

  function applySettingsToDOM(settings) {
    if (!settings.rtlEnabled) {
      document.body.classList.add('ag-rtl-disabled');
      window.__AG_RTL_DISABLED__ = true;
    } else {
      document.body.classList.remove('ag-rtl-disabled');
      window.__AG_RTL_DISABLED__ = false;
    }

    const root = document.documentElement;
    root.style.setProperty('--ag-font-family', getFontFamilyValue(settings.fontFamily, settings.customFont));
    root.style.setProperty('--ag-font-size', `${settings.fontSize}px`);
    root.style.setProperty('--ag-line-height', `${settings.lineHeight}`);
  }

  // 2. Inject Styles
  function injectStyles(cssContent) {
    let s = document.getElementById('antigravity-chat-rtl-style');
    if (!s) {
      s = document.createElement('style');
      s.id = 'antigravity-chat-rtl-style';
      (document.head || document.documentElement).appendChild(s);
    }
    s.textContent = cssContent;
    applySettingsToDOM(currentSettings);
  }

  // 3. Smart Direction Detection (70% letter ratio threshold)
  function detectSmartDirection(text, fallbackDir) {
    if (!text) return null;
    const trimmed = text.trim();
    if (!trimmed) return null;

    const latinMatches = trimmed.match(/[a-zA-Z]/g);
    const latinCount = latinMatches ? latinMatches.length : 0;

    const persianMatches = trimmed.match(/[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/g);
    const persianCount = persianMatches ? persianMatches.length : 0;

    const totalLetters = latinCount + persianCount;
    if (totalLetters === 0) {
      return fallbackDir !== undefined ? fallbackDir : 'rtl';
    }

    if (persianCount === 0) return 'ltr';
    if (latinCount === 0) return 'rtl';

    // If first alphabetic letter is Persian, it is always a Persian sentence (RTL)
    const firstLetterMatch = trimmed.match(/[a-zA-Z\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/);
    if (firstLetterMatch && /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/.test(firstLetterMatch[0])) {
      return 'rtl';
    }

    // When starting with Latin or symbols: only LTR if Latin letters are >= 70% of all letters
    const latinRatio = latinCount / totalLetters;
    if (latinRatio >= 0.7) {
      return 'ltr';
    }
    return 'rtl';
  }

  // 4. Apply Direction to Elements
  function applySmartDirectionToElement(el) {
    if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
    if (!el || el.nodeType !== 1) return;

    // Strict isolation of Code blocks, terminals, and tools
    if (el.matches && el.matches('pre, pre *, .monaco-editor, .monaco-editor *, .terminal, .terminal-wrapper, [data-testid*="tool"], [data-testid*="collapsible"], button.review-button, button.review-button *, .files-changed-header, .files-changed-header *, .code-line, .line-content')) {
      return;
    }

    // Conversation list in sidebar
    if (el.matches && el.matches('[data-testid="conversation-row-sidebar"]')) {
      const titleEl = el.querySelector('span.truncate, .truncate');
      const dir = detectSmartDirection((titleEl ? titleEl.textContent : el.textContent) || '');
      if (dir) {
        el.setAttribute('dir', dir);
        if (titleEl) titleEl.setAttribute('dir', dir);
      }
      return;
    }

    // Inline code tags
    if (el.tagName === 'CODE') {
      if (/[\u0600-\u06FF]/.test(el.textContent || '')) el.setAttribute('dir', 'rtl');
      else el.setAttribute('dir', 'ltr');
      return;
    }

    // Artifact cards
    if (el.classList && el.classList.contains('artifact-card')) {
      const desc = el.querySelector('.text-secondary-foreground, span.line-clamp-3');
      if (desc) {
        const dir = detectSmartDirection(desc.textContent || '');
        if (dir) desc.setAttribute('dir', dir);
      }
      return;
    }

    if ((el.classList && el.classList.contains('line-clamp-3')) || (el.classList && el.classList.contains('text-secondary-foreground'))) {
      if (el.closest('.artifact-card')) {
        const dir = detectSmartDirection(el.textContent || '');
        if (dir) el.setAttribute('dir', dir);
        return;
      }
    }

    // Tables
    if (el.tagName === 'TABLE') {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) {
        el.setAttribute('dir', dir);
        const cells = el.querySelectorAll('th, td');
        for (let i = 0; i < cells.length; i++) {
          const cellDir = detectSmartDirection(cells[i].textContent || '', dir);
          if (cellDir) cells[i].setAttribute('dir', cellDir);
        }
      }
      return;
    }

    // Lists (UL / OL / LI)
    if (el.tagName === 'LI') {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) {
        el.setAttribute('dir', dir);
        const ps = el.querySelectorAll('p');
        for (let i = 0; i < ps.length; i++) {
          const pDir = detectSmartDirection(ps[i].textContent || '', dir);
          if (pDir) ps[i].setAttribute('dir', pDir);
        }
        const parentList = el.parentElement;
        if (parentList && (parentList.tagName === 'UL' || parentList.tagName === 'OL')) {
          if (!parentList.getAttribute('dir')) parentList.setAttribute('dir', dir);
        }
      }
      return;
    }

    if (el.tagName === 'UL' || el.tagName === 'OL') {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) el.setAttribute('dir', dir);
      return;
    }

    // Blockquotes
    if (el.tagName === 'BLOCKQUOTE') {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) {
        el.setAttribute('dir', dir);
        const ps = el.querySelectorAll('p');
        for (let i = 0; i < ps.length; i++) {
          const pDir = detectSmartDirection(ps[i].textContent || '', dir);
          if (pDir) ps[i].setAttribute('dir', pDir);
        }
      }
      return;
    }

    // Headings and Paragraphs
    if (/^H[1-6]|P$/.test(el.tagName)) {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) el.setAttribute('dir', dir);
      return;
    }

    // User prompt blocks
    if (el.classList && el.classList.contains('whitespace-pre-wrap')) {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) el.setAttribute('dir', dir);
      return;
    }

    // Message container .leading-relaxed
    if (el.classList && el.classList.contains('leading-relaxed')) {
      const dir = detectSmartDirection(el.textContent || '');
      if (dir) el.setAttribute('dir', dir);
      return;
    }

    // Live input box
    if (el.getAttribute && (el.getAttribute('data-lexical-editor') === 'true' || el.getAttribute('contenteditable') === 'true')) {
      if (!el.__ag_rtl_bound__) {
        el.__ag_rtl_bound__ = true;
        el.addEventListener('input', () => {
          const d = detectSmartDirection(el.innerText || '');
          if (d) el.setAttribute('dir', d);
        });
      }
      const initialDir = detectSmartDirection(el.innerText || '');
      if (initialDir) el.setAttribute('dir', initialDir);
    }
  }

  function processAllSmartRTL(root) {
    if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
    const base = root || document.body;
    if (!base) return;

    applySmartDirectionToElement(base);
    const selector = 'p, h1, h2, h3, h4, h5, h6, li, ul, ol, blockquote, table, .artifact-card, span.line-clamp-3, .whitespace-pre-wrap, .leading-relaxed, [data-testid="conversation-row-sidebar"], [contenteditable="true"]';
    const elements = base.querySelectorAll(selector);
    for (let i = 0; i < elements.length; i++) {
      applySmartDirectionToElement(elements[i]);
    }
  }

  // 5. Dynamic MutationObserver for Chat Streaming
  let scheduled = false;
  const pendingNodes = new Set();
  const flushPending = () => {
    scheduled = false;
    const nodes = Array.from(pendingNodes);
    pendingNodes.clear();
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      if (node && node.nodeType === 1) {
        applySmartDirectionToElement(node);
        processAllSmartRTL(node);
      }
    }
  };

  const observer = new MutationObserver((mutations) => {
    if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
    for (let i = 0; i < mutations.length; i++) {
      const mut = mutations[i];
      if (mut.type === 'childList') {
        for (let j = 0; j < mut.addedNodes.length; j++) {
          const n = mut.addedNodes[j];
          if (n && n.nodeType === 1) pendingNodes.add(n);
        }
      } else if (mut.type === 'characterData') {
        const p = mut.target.parentElement;
        if (p && p.nodeType === 1) pendingNodes.add(p);
      }
    }
    if (!scheduled && pendingNodes.size > 0) {
      scheduled = true;
      requestAnimationFrame(flushPending);
    }
  });

  function startObserver() {
    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
      processAllSmartRTL(document.body);
    }
  }

  // 6. Top Menu Bar Appearance Button
  function initAppearanceMenu() {
    if (window.__AG_RTL_DISABLED__) {
      const c = document.getElementById('ag-appearance-menu-container');
      if (c) c.remove();
      return;
    }
    const bar = document.querySelector('[data-testid="title-menu-bar"]');
    if (!bar) return;

    let container = document.getElementById('ag-appearance-menu-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'ag-appearance-menu-container';
      container.className = 'relative';
      container.style.appRegion = 'no-drag';
      bar.appendChild(container);
    }

    let btn = document.getElementById('ag-appearance-menu-btn');
    if (btn) return;

    btn = document.createElement('button');
    btn.id = 'ag-appearance-menu-btn';
    btn.className = 'inline-flex items-center font-medium transition-colors select-none outline-none cursor-pointer justify-center disabled:opacity-50 bg-transparent text-muted-foreground hover:text-foreground hover:bg-secondary focus-visible:text-foreground focus-visible:bg-secondary h-7 text-sm rounded-md gap-1.5 px-2.5 select-none';
    btn.setAttribute('data-testid', 'title-menu-bar-item');
    btn.title = 'تنظیمات ظاهر و راست‌چین (Appearance & RTL Settings)';
    btn.innerHTML = `
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.85;">
        <circle cx="12" cy="12" r="3"></circle>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
      </svg>
      <span>Appearance</span>
    `;
    container.appendChild(btn);

    // Modal structure
    const modal = document.createElement('div');
    modal.id = 'ag-appearance-modal';
    modal.style.cssText = 'display:none; position:fixed; top:36px; left:220px; z-index:999999; width:330px; background:#1e1e1e; color:#e0e0e0; border:1px solid #3c3c3c; border-radius:10px; box-shadow:0 12px 32px rgba(0,0,0,0.6); padding:16px; font-family:var(--ag-font-family); direction:rtl; text-align:right; font-size:13px;';
    
    function renderModalContent() {
      modal.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:10px; margin-bottom:14px;">
          <strong style="font-size:14px; color:#fff;">تنظیمات ظاهر و تایپوگرافی</strong>
          <span id="ag-modal-close" style="cursor:pointer; font-size:16px; color:#aaa; line-height:1; padding:2px 6px;">&times;</span>
        </div>
        <div style="margin-bottom:14px; display:flex; justify-content:space-between; align-items:center;">
          <span>فعال‌سازی راست‌چین و استایل:</span>
          <input type="checkbox" id="ag-rtl-toggle" ${currentSettings.rtlEnabled ? 'checked' : ''} style="cursor:pointer; accent-color:#007acc; width:16px; height:16px;" />
        </div>
        <div style="margin-bottom:14px;">
          <label style="display:block; margin-bottom:5px; color:#bbb;">فونت فارسی:</label>
          <select id="ag-font-select" style="width:100%; background:#2d2d2d; color:#fff; border:1px solid #444; border-radius:6px; padding:6px; outline:none; font-family:inherit;">
            <option value="Vazirmatn" ${currentSettings.fontFamily === 'Vazirmatn' ? 'selected' : ''}>وزیرمتن (پیش‌فرض)</option>
            <option value="Shabnam" ${currentSettings.fontFamily === 'Shabnam' ? 'selected' : ''}>شبنم (Shabnam)</option>
            <option value="Sahel" ${currentSettings.fontFamily === 'Sahel' ? 'selected' : ''}>ساحل (Sahel)</option>
            <option value="Samim" ${currentSettings.fontFamily === 'Samim' ? 'selected' : ''}>صمیم (Samim)</option>
            <option value="Custom" ${currentSettings.fontFamily === 'Custom' ? 'selected' : ''}>فونت دلخواه (نصب شده در سیستم)...</option>
          </select>
        </div>
        <div id="ag-custom-font-container" style="margin-bottom:14px; display:${currentSettings.fontFamily === 'Custom' ? 'block' : 'none'};">
          <label style="display:block; margin-bottom:5px; color:#bbb;">نام فونت سیستمی:</label>
          <input type="text" id="ag-custom-font-input" value="${currentSettings.customFont}" placeholder="e.g. B Yekan, IranSans..." style="width:100%; background:#2d2d2d; color:#fff; border:1px solid #444; border-radius:6px; padding:6px; outline:none;" />
        </div>
        <div style="margin-bottom:14px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="color:#bbb;">اندازه قلم:</span>
            <span id="ag-fontsize-val" style="color:#007acc; font-weight:bold;">${currentSettings.fontSize}px</span>
          </div>
          <input type="range" id="ag-fontsize-slider" min="12" max="22" step="1" value="${currentSettings.fontSize}" style="width:100%; accent-color:#007acc; cursor:pointer;" />
        </div>
        <div style="margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="color:#bbb;">فاصله خطوط:</span>
            <span id="ag-lineheight-val" style="color:#007acc; font-weight:bold;">${currentSettings.lineHeight}</span>
          </div>
          <input type="range" id="ag-lineheight-slider" min="1.3" max="2.4" step="0.05" value="${currentSettings.lineHeight}" style="width:100%; accent-color:#007acc; cursor:pointer;" />
        </div>
        <div style="display:flex; gap:8px;">
          <button id="ag-save-btn" style="flex:1; background:#007acc; color:#fff; border:none; border-radius:6px; padding:7px; cursor:pointer; font-weight:bold;">ذخیره و اعمال</button>
          <button id="ag-reset-btn" style="background:#3a3a3a; color:#ccc; border:none; border-radius:6px; padding:7px 12px; cursor:pointer;">بازنشانی</button>
        </div>
      `;
      bindModalEvents();
    }

    function bindModalEvents() {
      const closeBtn = document.getElementById('ag-modal-close');
      if (closeBtn) closeBtn.onclick = () => { modal.style.display = 'none'; };

      const fontSelect = document.getElementById('ag-font-select');
      const customCont = document.getElementById('ag-custom-font-container');
      if (fontSelect) {
        fontSelect.onchange = () => {
          if (customCont) customCont.style.display = fontSelect.value === 'Custom' ? 'block' : 'none';
        };
      }

      const sizeSlider = document.getElementById('ag-fontsize-slider');
      const sizeVal = document.getElementById('ag-fontsize-val');
      if (sizeSlider && sizeVal) {
        sizeSlider.oninput = () => { sizeVal.textContent = `${sizeSlider.value}px`; };
      }

      const lhSlider = document.getElementById('ag-lineheight-slider');
      const lhVal = document.getElementById('ag-lineheight-val');
      if (lhSlider && lhVal) {
        lhSlider.oninput = () => { lhVal.textContent = lhSlider.value; };
      }

      const saveBtn = document.getElementById('ag-save-btn');
      if (saveBtn) {
        saveBtn.onclick = () => {
          currentSettings = {
            rtlEnabled: document.getElementById('ag-rtl-toggle').checked,
            fontFamily: document.getElementById('ag-font-select').value,
            customFont: (document.getElementById('ag-custom-font-input') || {}).value || '',
            fontSize: parseInt(document.getElementById('ag-fontsize-slider').value, 10),
            lineHeight: parseFloat(document.getElementById('ag-lineheight-slider').value)
          };
          saveSettings(currentSettings);
          applySettingsToDOM(currentSettings);
          processAllSmartRTL(document.body);
          modal.style.display = 'none';
        };
      }

      const resetBtn = document.getElementById('ag-reset-btn');
      if (resetBtn) {
        resetBtn.onclick = () => {
          currentSettings = Object.assign({}, DEFAULT_SETTINGS);
          saveSettings(currentSettings);
          applySettingsToDOM(currentSettings);
          processAllSmartRTL(document.body);
          renderModalContent();
        };
      }
    }

    document.body.appendChild(modal);

    btn.onclick = (e) => {
      e.stopPropagation();
      if (modal.style.display === 'none' || !modal.style.display) {
        const rect = btn.getBoundingClientRect();
        modal.style.top = `${rect.bottom + 6}px`;
        modal.style.left = `${Math.max(12, rect.left - 100)}px`;
        renderModalContent();
        modal.style.display = 'block';
      } else {
        modal.style.display = 'none';
      }
    };

    document.addEventListener('click', (e) => {
      if (modal.style.display === 'block' && !modal.contains(e.target) && e.target !== btn && !btn.contains(e.target)) {
        modal.style.display = 'none';
      }
    });
  }

  // 7. Global Lifecycle
  window.__AG_RTL__ = {
    init: function (cssContent) {
      injectStyles(cssContent);
      startObserver();
      initAppearanceMenu();
      if (window.__AG_RTL_MENU_INTERVAL__) clearInterval(window.__AG_RTL_MENU_INTERVAL__);
      window.__AG_RTL_MENU_INTERVAL__ = setInterval(initAppearanceMenu, 2500);
    },
    processAll: function () {
      processAllSmartRTL(document.body);
    }
  };

  // Auto-start observer if DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      startObserver();
      initAppearanceMenu();
    });
  } else {
    startObserver();
    initAppearanceMenu();
  }
})();
