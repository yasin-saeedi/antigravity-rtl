/**
 * Antigravity RTL & Smart Typography Unified Patcher (Node.js version)
 * پچ جامع و هوشمند راست‌چین‌سازی چت و تنظیم فونت در آنتی‌گراویتی (نسخه جاوااسکریپت)
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync, spawn } = require('child_process');
const readline = require('readline');

const RTL_CSS = `/**
 * Antigravity IDE Chat & Markdown RTL Support (Smart Auto-Direction & Tool Isolation)
 * https://github.com/yasin-saeedi/antigravity-rtl
 * 
 * استایل هوشمند راست‌چین/چپ‌چین خودکار با فونت‌های فارسی، متغیرهای پویا و مصون‌سازی کامل بخش ابزارها و لاگ‌ها
 */

/* =========================================================
   ۰. ایمپورت فونت‌های فارسی استاندارد
   ========================================================= */
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/shabnam-font@v5.0.1/dist/font-face.css');
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/sahel-font@v3.4.0/dist/font-face.css');
@import url('https://cdn.jsdelivr.net/gh/rastikerdar/samim-font@v4.0.5/dist/font-face.css');

:root {
  --ag-font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Tahoma, Arial, sans-serif;
  --ag-font-size: 15px;
  --ag-line-height: 1.75;
}

/* =========================================================
   ۱. متون پیام‌های کاربر، پاسخ‌های مدل، پنل راست (Artifact & Markdown) و کادر تایپ
   ========================================================= */
body:not(.ag-rtl-disabled) .leading-relaxed,
body:not(.ag-rtl-disabled) .leading-relaxed p,
body:not(.ag-rtl-disabled) .leading-relaxed li,
body:not(.ag-rtl-disabled) .leading-relaxed blockquote,
body:not(.ag-rtl-disabled) .leading-relaxed h1,
body:not(.ag-rtl-disabled) .leading-relaxed h2,
body:not(.ag-rtl-disabled) .leading-relaxed h3,
body:not(.ag-rtl-disabled) .leading-relaxed h4,
body:not(.ag-rtl-disabled) .leading-relaxed h5,
body:not(.ag-rtl-disabled) .leading-relaxed h6,
body:not(.ag-rtl-disabled) .leading-relaxed table,
body:not(.ag-rtl-disabled) .leading-relaxed th,
body:not(.ag-rtl-disabled) .leading-relaxed td,
body:not(.ag-rtl-disabled) .artifact-card,
body:not(.ag-rtl-disabled) .artifact-card span,
body:not(.ag-rtl-disabled) .artifact-card .text-secondary-foreground,
body:not(.ag-rtl-disabled) [data-testid="user-input-step"] .whitespace-pre-wrap,
body:not(.ag-rtl-disabled) #conversation [role="article"] p,
body:not(.ag-rtl-disabled) #conversation [role="article"] li,
body:not(.ag-rtl-disabled) #conversation [role="article"] blockquote,
body:not(.ag-rtl-disabled) div[data-lexical-editor="true"],
body:not(.ag-rtl-disabled) #antigravity\\.agentSidePanelInputBox [contenteditable="true"] {
  font-family: var(--ag-font-family) !important;
}

body:not(.ag-rtl-disabled) .leading-relaxed {
  font-size: var(--ag-font-size) !important;
  line-height: var(--ag-line-height) !important;
}

body:not(.ag-rtl-disabled) [data-testid="user-input-step"] [class*="text-xs"] {
  font-size: calc(var(--ag-font-size) * 0.77) !important;
}

body:not(.ag-rtl-disabled) .leading-relaxed h1 { font-size: calc(var(--ag-font-size) * 1.33) !important; }
body:not(.ag-rtl-disabled) .leading-relaxed h2 { font-size: calc(var(--ag-font-size) * 1.2) !important; }
body:not(.ag-rtl-disabled) .leading-relaxed h3 { font-size: calc(var(--ag-font-size) * 1.1) !important; }
body:not(.ag-rtl-disabled) .leading-relaxed h4 { font-size: var(--ag-font-size) !important; }

/* جهت‌بندی صریح راست‌چین */
body:not(.ag-rtl-disabled) [dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed [dir="rtl"] {
  direction: rtl !important;
  text-align: right !important;
}

/* جهت‌بندی صریح چپ‌چین */
[dir="ltr"],
.leading-relaxed[dir="ltr"],
.leading-relaxed [dir="ltr"] {
  direction: ltr !important;
  text-align: left !important;
}

/* مشخصه‌های منطقی برای لیست‌ها و نقل‌قول‌ها در جهت راست‌به‌چپ (خنثی‌سازی کامل pl-10 و pl-4 تیل‌ویند) */
body:not(.ag-rtl-disabled) ul[dir="rtl"],
body:not(.ag-rtl-disabled) ol[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed ul[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed ol[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed [dir="rtl"] > ul,
body:not(.ag-rtl-disabled) .leading-relaxed [dir="rtl"] > ol {
  direction: rtl !important;
  text-align: right !important;
  padding-right: 1.75rem !important;
  padding-left: 0 !important;
  margin-right: 0 !important;
  margin-left: 0 !important;
  list-style-position: outside !important;
}

body:not(.ag-rtl-disabled) li[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed li[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed [dir="rtl"] > li {
  direction: rtl !important;
  text-align: right !important;
  margin-right: 0.25rem !important;
  margin-left: 0 !important;
}

ul[dir="ltr"],
ol[dir="ltr"],
.leading-relaxed ul[dir="ltr"],
.leading-relaxed ol[dir="ltr"] {
  direction: ltr !important;
  text-align: left !important;
  padding-left: 1.75rem !important;
  padding-right: 0 !important;
}

li[dir="ltr"],
.leading-relaxed li[dir="ltr"] {
  direction: ltr !important;
  text-align: left !important;
}

/* نقل‌قول‌ها */
body:not(.ag-rtl-disabled) blockquote[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed blockquote[dir="rtl"],
body:not(.ag-rtl-disabled) [dir="rtl"] blockquote {
  direction: rtl !important;
  text-align: right !important;
  border-right: 3px solid rgba(140, 140, 140, 0.4) !important;
  border-left: none !important;
  padding-right: 1rem !important;
  padding-left: 0 !important;
  margin-right: 0 !important;
  margin-left: 0 !important;
}

blockquote[dir="ltr"],
.leading-relaxed blockquote[dir="ltr"] {
  direction: ltr !important;
  text-align: left !important;
  border-left: 3px solid rgba(140, 140, 140, 0.4) !important;
  border-right: none !important;
  padding-left: 1rem !important;
  padding-right: 0 !important;
}

/* جدول‌ها در حالت RTL */
body:not(.ag-rtl-disabled) table[dir="rtl"],
body:not(.ag-rtl-disabled) .leading-relaxed table[dir="rtl"],
body:not(.ag-rtl-disabled) [dir="rtl"] table {
  direction: rtl !important;
  text-align: right !important;
  width: 100% !important;
}

body:not(.ag-rtl-disabled) table[dir="rtl"] th,
body:not(.ag-rtl-disabled) table[dir="rtl"] td,
body:not(.ag-rtl-disabled) .leading-relaxed table[dir="rtl"] th,
body:not(.ag-rtl-disabled) .leading-relaxed table[dir="rtl"] td,
body:not(.ag-rtl-disabled) [dir="rtl"] table th,
body:not(.ag-rtl-disabled) [dir="rtl"] table td {
  direction: rtl !important;
  text-align: right !important;
}

table[dir="ltr"],
.leading-relaxed table[dir="ltr"] {
  direction: ltr !important;
  text-align: left !important;
}

table[dir="ltr"] th,
table[dir="ltr"] td {
  direction: ltr !important;
  text-align: left !important;
}

/* =========================================================
   ۲. بهینه‌سازی کارت‌های آرتیفکت در چت (Artifact Preview Cards)
   ========================================================= */
body:not(.ag-rtl-disabled) .artifact-card {
  width: 100% !important;
}

body:not(.ag-rtl-disabled) .artifact-card > div:first-child {
  width: 100% !important;
}

body:not(.ag-rtl-disabled) .artifact-card .text-secondary-foreground,
body:not(.ag-rtl-disabled) .artifact-card span.line-clamp-3 {
  width: 100% !important;
  display: block !important;
  font-family: var(--ag-font-family) !important;
  font-size: calc(var(--ag-font-size) * 0.9) !important;
  line-height: 1.6 !important;
}

body:not(.ag-rtl-disabled) .artifact-card .text-secondary-foreground[dir="rtl"],
body:not(.ag-rtl-disabled) .artifact-card span.line-clamp-3[dir="rtl"] {
  direction: rtl !important;
  text-align: right !important;
}

body:not(.ag-rtl-disabled) .artifact-card .text-secondary-foreground[dir="ltr"],
body:not(.ag-rtl-disabled) .artifact-card span.line-clamp-3[dir="ltr"] {
  direction: ltr !important;
  text-align: left !important;
}

/* =========================================================
   ۳. کادر تایپ کاربر (Lexical Editor)
   ========================================================= */
body:not(.ag-rtl-disabled) div[data-lexical-editor="true"],
body:not(.ag-rtl-disabled) #antigravity\\.agentSidePanelInputBox [contenteditable="true"] {
  direction: rtl !important;
  text-align: right !important;
  unicode-bidi: plaintext !important;
  font-family: var(--ag-font-family) !important;
}

body:not(.ag-rtl-disabled) #antigravity\\.agentSidePanelInputBox p.pointer-events-none {
  direction: rtl !important;
  text-align: right !important;
  left: auto !important;
  right: 0.5rem !important;
}

/* =========================================================
   ۴. معکوس‌سازی و چینش راست‌به‌چپ نوار دکمه‌های کادر ورودی (Input Toolbar RTL Flip)
   ========================================================= */
body:not(.ag-rtl-disabled) div.flex.w-full.items-center.justify-between:has(button[data-testid="model-selector-trigger"]),
body:not(.ag-rtl-disabled) div.flex.w-full.items-center.justify-between:has(button[data-testid="model-selector-trigger"]) > div {
  direction: rtl !important;
}

body:not(.ag-rtl-disabled) button[data-testid="model-selector-trigger"] {
  padding-inline-start: 0.5rem !important;
  padding-inline-end: 0.25rem !important;
}

body:not(.ag-rtl-disabled) button[aria-label*="Send"] svg {
  transform: scaleX(-1);
}

/* =========================================================
   ۵. مصون‌سازی ۱۰۰٪ کادر ابزارها، دکمه‌های ریویو، Thought، ترمینال و کدهای برنامه (همواره LTR)
   ========================================================= */
code,
pre,
pre *,
.monaco-workbench .part.editor,
.monaco-editor,
.monaco-editor *,
.terminal,
.terminal-wrapper,
[role="article"] pre,
[role="article"] pre *,
[role="article"] [class*="code-line"],
[role="article"] [class*="code-block"],
[aria-label="Agent response"] > div:first-child,
[aria-label="Agent response"] > div:first-child *,
[data-testid*="collapsible"],
[data-testid*="collapsible"] *,
[data-testid*="tool"],
[data-testid*="tool"] *,
[class*="tabular-nums"],
[class*="tabular-nums"] *,
button.review-button,
button.review-button *,
.files-changed-header,
.files-changed-header *,
button[class*="text-left"],
button[class*="text-left"] * {
  direction: ltr !important;
  text-align: left !important;
  justify-content: flex-start !important;
  unicode-bidi: isolate !important;
}

/* کدهای اینلاین */
code:not(pre code),
[role="article"] code:not(pre code) {
  font-size: calc(var(--ag-font-size) * 0.9) !important;
  display: inline-block !important;
  unicode-bidi: isolate !important;
}

code:not(pre code):not([dir="rtl"]) {
  direction: ltr !important;
  text-align: left !important;
}

body:not(.ag-rtl-disabled) code:not(pre code)[dir="rtl"] {
  direction: rtl !important;
  text-align: right !important;
  font-family: var(--ag-font-family) !important;
}

/* =========================================================
   ۶. بازگردانی کامل در صورت غیرفعال بودن RTL
   ========================================================= */
body.ag-rtl-disabled [dir="rtl"] {
  direction: ltr !important;
  text-align: left !important;
}
body.ag-rtl-disabled div[data-lexical-editor="true"] {
  direction: ltr !important;
  text-align: left !important;
}
body.ag-rtl-disabled #antigravity\\.agentSidePanelInputBox p.pointer-events-none {
  direction: ltr !important;
  text-align: left !important;
  left: 0.5rem !important;
  right: auto !important;
}
body.ag-rtl-disabled button[aria-label*="Send"] svg {
  transform: none !important;
}`;

function printBanner() {
    console.log(`
====================================================================
    ✦ Antigravity Smart RTL & Typography Unified Patcher ✦
      پچ جامع راست‌چین هوشمند، فونت وزیرمتن و مصون‌سازی ابزارها
====================================================================
`);
}

function findAntigravityPath(customPath) {
    if (customPath) {
        let cp = path.resolve(customPath.trim().replace(/^"|"$/g, ''));
        if (fs.existsSync(path.join(cp, 'resources', 'app.asar')) && fs.existsSync(path.join(cp, 'Antigravity.exe'))) {
            return cp;
        }
        if (fs.existsSync(cp) && fs.statSync(cp).isFile()) {
            let parent = path.dirname(cp);
            if (path.basename(parent) === 'resources') parent = path.dirname(parent);
            if (fs.existsSync(path.join(parent, 'resources', 'app.asar')) && fs.existsSync(path.join(parent, 'Antigravity.exe'))) {
                return parent;
            }
        }
    }

    const candidates = [];

    // 1. Running processes
    try {
        const psCmd = 'Get-Process Antigravity -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Path';
        const out = execSync(`powershell -NoProfile -Command "${psCmd}"`, { encoding: 'utf8', timeout: 3000 });
        for (const line of out.split(/\r?\n/)) {
            const p = line.trim();
            if (p && p.toLowerCase().endsWith('antigravity.exe') && fs.existsSync(p)) {
                const d = path.dirname(p);
                if (!candidates.includes(d)) candidates.push(d);
            }
        }
    } catch (e) {}

    // 2. LocalAppData standard installation
    const localAppData = process.env.LOCALAPPDATA || '';
    if (localAppData) {
        const stdPath = path.join(localAppData, 'Programs', 'antigravity');
        if (!candidates.includes(stdPath)) candidates.push(stdPath);
    }

    // 3. Program Files
    for (const pf of [process.env.ProgramFiles, process.env['ProgramFiles(x86)'], process.env.ProgramW6432]) {
        if (pf) {
            candidates.push(path.join(pf, 'Antigravity'));
            candidates.push(path.join(pf, 'antigravity'));
        }
    }

    // 4. Roaming AppData
    const roaming = process.env.APPDATA || '';
    if (roaming) {
        candidates.push(path.join(roaming, 'Programs', 'antigravity'));
    }

    for (const c of candidates) {
        if (fs.existsSync(path.join(c, 'resources', 'app.asar')) && fs.existsSync(path.join(c, 'Antigravity.exe'))) {
            return c;
        }
    }
    return null;
}

function isRunning() {
    try {
        const out = execSync('tasklist /FI "IMAGENAME eq Antigravity.exe"', { encoding: 'utf8' });
        return out.toLowerCase().includes('antigravity.exe');
    } catch (e) {
        return false;
    }
}

function closeAntigravity() {
    console.log('[*] در حال بستن فرآیندهای در حال اجرای Antigravity...');
    try {
        execSync('taskkill /F /IM Antigravity.exe /T', { stdio: 'ignore' });
        const start = Date.now();
        while (Date.now() - start < 1500) {}
    } catch (e) {}
}

function sha256Blocks(buf, blockSize = 4 * 1024 * 1024) {
    const blocks = [];
    for (let i = 0; i < buf.length; i += blockSize) {
        const chunk = buf.subarray(i, i + blockSize);
        blocks.push(crypto.createHash('sha256').update(chunk).digest('hex'));
    }
    return {
        algorithm: 'SHA256',
        hash: crypto.createHash('sha256').update(buf).digest('hex'),
        blockSize: blockSize,
        blocks: blocks
    };
}

function patchAsar(inputAsar, outputAsar, replacements) {
    const fd = fs.openSync(inputAsar, 'r');
    const headerBuf = Buffer.alloc(16);
    fs.readSync(fd, headerBuf, 0, 16, 0);

    const magic = headerBuf.readUInt32LE(0);
    const jsonLen = headerBuf.readUInt32LE(12);

    const jsonBuf = Buffer.alloc(jsonLen);
    fs.readSync(fd, jsonBuf, 0, jsonLen, 16);
    const header = JSON.parse(jsonBuf.toString('utf8'));

    const padding = (4 - (jsonLen % 4)) % 4;
    const payloadStart = 16 + jsonLen + padding;

    const fileEntries = [];
    function traverse(curr, parts) {
        if (curr.files) {
            for (const name of Object.keys(curr.files)) {
                traverse(curr.files[name], parts.concat(name));
            }
        } else {
            fileEntries.push({ parts, node: curr });
        }
    }
    traverse(header, []);

    const newChunks = [];
    let currentOffset = 0;

    for (const item of fileEntries) {
        const pathStr = item.parts.join('/');
        if (item.node.unpacked) continue;

        let content;
        if (replacements[pathStr]) {
            content = Buffer.isBuffer(replacements[pathStr])
                ? replacements[pathStr]
                : Buffer.from(replacements[pathStr], 'utf8');
            console.log(`  [+] به‌روزرسانی در پکیج: ${pathStr} (${content.length.toLocaleString()} بایت)`);
        } else {
            const oldOffset = parseInt(item.node.offset, 10);
            const oldSize = item.node.size;
            content = Buffer.alloc(oldSize);
            fs.readSync(fd, content, 0, oldSize, payloadStart + oldOffset);
        }

        item.node.offset = currentOffset.toString();
        item.node.size = content.length;
        item.node.integrity = sha256Blocks(content);

        newChunks.push(content);
        currentOffset += content.length;
    }
    fs.closeSync(fd);

    const newJsonBuf = Buffer.from(JSON.stringify(header), 'utf8');
    const newJsonLen = newJsonBuf.length;
    const newPaddingLen = (4 - (newJsonLen % 4)) % 4;
    const newPadding = Buffer.alloc(newPaddingLen, 0);

    const newSizeHeader = newJsonLen + newPaddingLen + 4;
    const newSizeTotal = newSizeHeader + 4;

    const newHeaderPrefix = Buffer.alloc(16);
    newHeaderPrefix.writeUInt32LE(4, 0);
    newHeaderPrefix.writeUInt32LE(newSizeTotal, 4);
    newHeaderPrefix.writeUInt32LE(newSizeHeader, 8);
    newHeaderPrefix.writeUInt32LE(newJsonLen, 12);

    const outFd = fs.openSync(outputAsar, 'w');
    fs.writeSync(outFd, newHeaderPrefix);
    fs.writeSync(outFd, newJsonBuf);
    if (newPaddingLen > 0) fs.writeSync(outFd, newPadding);
    for (const c of newChunks) {
        fs.writeSync(outFd, c);
    }
    fs.closeSync(outFd);
}

function extractFromAsar(asarPath, targetRelPath) {
    const fd = fs.openSync(asarPath, 'r');
    const headerBuf = Buffer.alloc(16);
    fs.readSync(fd, headerBuf, 0, 16, 0);
    const jsonLen = headerBuf.readUInt32LE(12);
    const jsonBuf = Buffer.alloc(jsonLen);
    fs.readSync(fd, jsonBuf, 0, jsonLen, 16);
    const header = JSON.parse(jsonBuf.toString('utf8'));
    const padding = (4 - (jsonLen % 4)) % 4;
    const payloadStart = 16 + jsonLen + padding;

    let curr = header;
    for (const p of targetRelPath.split('/')) {
        if (curr.files && curr.files[p]) {
            curr = curr.files[p];
        } else {
            fs.closeSync(fd);
            return null;
        }
    }
    const offset = parseInt(curr.offset, 10);
    const size = curr.size;
    const buf = Buffer.alloc(size);
    fs.readSync(fd, buf, 0, size, payloadStart + offset);
    fs.closeSync(fd);
    return buf.toString('utf8');
}

function doPatch(targetDir, kill = false) {
    const resourcesDir = path.join(targetDir, 'resources');
    const asarPath = path.join(resourcesDir, 'app.asar');
    const backupPath = path.join(resourcesDir, 'app.asar.original_backup');
    const tempAsar = path.join(resourcesDir, 'app.asar.patching.tmp');

    if (!fs.existsSync(asarPath)) {
        console.log(`[-] خطا: فایل app.asar در مسیر ${asarPath} یافت نشد.`);
        return false;
    }

    if (kill && isRunning()) {
        closeAntigravity();
    }

    if (!fs.existsSync(backupPath)) {
        console.log('[*] در حال تهیه نسخه پشتیبان کارخانه (app.asar.original_backup)...');
        try {
            fs.copyFileSync(asarPath, backupPath);
            console.log(`  [✓] پشتیبان ذخیره شد:\n      ${backupPath}`);
        } catch (e) {
            console.log(`[-] خطا در ایجاد فایل پشتیبان: ${e.message}`);
            return false;
        }
    } else {
        console.log('  [i] نسخه پشتیبان اصلی کارخانه موجود است.');
    }

    const sourceAsar = fs.existsSync(backupPath) ? backupPath : asarPath;
    let preloadCode = extractFromAsar(sourceAsar, 'dist/preload.js');
    let updaterCode = extractFromAsar(sourceAsar, 'dist/updater.js');
    let nsisCode = extractFromAsar(sourceAsar, 'node_modules/electron-updater/out/NsisUpdater.js');
    let baseCode = extractFromAsar(sourceAsar, 'node_modules/electron-updater/out/BaseUpdater.js');

    if (!preloadCode) {
        console.log('[-] خطا در استخراج dist/preload.js');
        return false;
    }

    const cleanCss = RTL_CSS.replace(/`/g, '\\`');
    const injection = `
/* __ANTIGRAVITY_RTL_INJECTED__ */
try {
(function() {
    const rtlCSS = \`${cleanCss}\`;

    function applyRTL() {
        try {
            if (typeof electron_1 !== 'undefined' && electron_1.webFrame && electron_1.webFrame.insertCSS) {
                electron_1.webFrame.insertCSS(rtlCSS);
            }
        } catch(e) {}

        function injectTag() {
            if (!document.head) {
                setTimeout(injectTag, 20);
                return;
            }
            let s = document.getElementById('antigravity-chat-rtl-style');
            if (!s) {
                s = document.createElement('style');
                s.id = 'antigravity-chat-rtl-style';
                document.head.appendChild(s);
            }
            s.textContent = rtlCSS;
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', injectTag);
        } else {
            injectTag();
        }
    }

    applyRTL();

    // --- Settings & Appearance Subsystem ---
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
        } catch(e) {}
        return Object.assign({}, DEFAULT_SETTINGS);
    }

    function saveSettings(s) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
        } catch(e) {}
    }

    let currentSettings = getSettings();

    function getFontFamilyValue(fontName, customName) {
        switch(fontName) {
            case 'Shabnam':
                return "'Shabnam', 'Vazirmatn', sans-serif";
            case 'Sahel':
                return "'Sahel', 'Vazirmatn', sans-serif";
            case 'Samim':
                return "'Samim', 'Vazirmatn', sans-serif";
            case 'Tahoma':
                return "'Tahoma', 'Vazirmatn', -apple-system, sans-serif";
            case 'System':
                return "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
            case 'Custom':
                return (customName ? \`'\${customName}', \` : "") + "'Vazirmatn', sans-serif";
            case 'Vazirmatn':
            default:
                return "'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        }
    }

    function applySettings(s) {
        if (!document.documentElement) return;
        const root = document.documentElement;
        root.style.setProperty('--ag-font-size', s.fontSize + 'px');
        root.style.setProperty('--ag-line-height', s.lineHeight.toString());
        root.style.setProperty('--ag-font-family', getFontFamilyValue(s.fontFamily, s.customFont));

        if (!document.body) return;
        if (s.rtlEnabled) {
            document.body.classList.remove('ag-rtl-disabled');
            processAllSmartRTL(document.body);
        } else {
            document.body.classList.add('ag-rtl-disabled');
        }
    }

    // --- Smart Direction Subsystem ---
    function detectSmartDirection(text, fallbackDir) {
        if (!text) return null;
        const trimmed = text.trim();
        if (!trimmed) return null;

        const hasPersian = /[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(trimmed);
        const hasLatin = /[a-zA-Z]/.test(trimmed);

        if (hasPersian && !hasLatin) return 'rtl';
        if (!hasPersian && !hasLatin) return fallbackDir !== undefined ? fallbackDir : 'rtl';
        if (!hasPersian && hasLatin) return 'ltr';

        let s = trimmed.replace(/^[\\s\\d٠-٩۰-۹*#\\-_+–—•.:,;!?/\\|~<>]+/, '');
        s = s.replace(/^\\[[ xX]\\]\\s*/, '');

        const tagMatch = s.match(/^(\\([^\\)]+\\)|\\[[^\\]]+\\]|\`[^\`]+\`|[a-zA-Z0-9_.\\-]+\\.(?:zip|bat|py|js|ts|css|json|txt|md|exe|sh|html)\\s*:?)\\s*/);
        if (tagMatch) {
            const afterTag = s.slice(tagMatch[0].length).trim();
            if (/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(afterTag)) {
                return 'rtl';
            }
        }

        const letterMatch = s.match(/[\\p{L}]/u);
        if (letterMatch) {
            const char = letterMatch[0];
            if (/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(char)) return 'rtl';
            if (/[a-zA-Z]/.test(char)) {
                const persianCount = (s.match(/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/g) || []).length;
                const latinCount = (s.match(/[a-zA-Z]/g) || []).length;
                if (persianCount > latinCount * 1.1) return 'rtl';
                return 'ltr';
            }
            if (/[\\p{sc=Arabic}\\p{sc=Hebrew}\\p{sc=Syriac}\\p{sc=Thaana}]/u.test(char)) return 'rtl';
        }
        return 'rtl';
    }

    function applySmartDirectionToElement(el) {
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        if (!el || el.nodeType !== 1) return;
        if (el.matches('pre, pre *, .monaco-editor, .monaco-editor *, .terminal, .terminal-wrapper, [data-testid*="tool"], [data-testid*="collapsible"], button.review-button, button.review-button *, .files-changed-header, .files-changed-header *')) return;

        if (el.tagName === 'CODE') {
            if (/[؀-ۿ]/.test(el.innerText || el.textContent)) el.setAttribute('dir', 'rtl');
            else el.setAttribute('dir', 'ltr');
            return;
        }

        if (el.classList && el.classList.contains('artifact-card')) {
            const desc = el.querySelector('.text-secondary-foreground, span.line-clamp-3');
            if (desc) {
                const dir = detectSmartDirection(desc.innerText || desc.textContent);
                if (dir) desc.setAttribute('dir', dir);
            }
            return;
        }

        if ((el.classList && el.classList.contains('line-clamp-3')) || (el.classList && el.classList.contains('text-secondary-foreground'))) {
            if (el.closest('.artifact-card')) {
                const dir = detectSmartDirection(el.innerText || el.textContent);
                if (dir) el.setAttribute('dir', dir);
                return;
            }
        }

        if (el.tagName === 'TABLE') {
            const dir = detectSmartDirection(el.innerText || el.textContent);
            if (dir) {
                el.setAttribute('dir', dir);
                const cells = el.querySelectorAll('th, td');
                for (let i = 0; i < cells.length; i++) {
                    const cellDir = detectSmartDirection(cells[i].innerText || cells[i].textContent, dir);
                    if (cellDir) cells[i].setAttribute('dir', cellDir);
                }
            }
            return;
        }

        if (el.tagName === 'LI') {
            const dir = detectSmartDirection(el.innerText || el.textContent);
            if (dir) {
                el.setAttribute('dir', dir);
                const parentList = el.parentElement;
                if (parentList && (parentList.tagName === 'UL' || parentList.tagName === 'OL')) {
                    if (!parentList.getAttribute('dir')) parentList.setAttribute('dir', dir);
                }
            }
            return;
        }

        if (el.tagName === 'UL' || el.tagName === 'OL') {
            const dir = detectSmartDirection(el.innerText || el.textContent);
            if (dir) el.setAttribute('dir', dir);
            return;
        }

        if (/^(H[1-6]|P|BLOCKQUOTE)$/.test(el.tagName)) {
            const dir = detectSmartDirection(el.innerText || el.textContent);
            if (dir) el.setAttribute('dir', dir);
            return;
        }

        if (el.classList && el.classList.contains('whitespace-pre-wrap') && el.closest('[data-testid="user-input-step"]')) {
            const dir = detectSmartDirection(el.innerText || el.textContent);
            if (dir) el.setAttribute('dir', dir);
            return;
        }

        if (el.classList && el.classList.contains('leading-relaxed')) {
            const dir = detectSmartDirection(el.innerText || el.textContent);
            if (dir) el.setAttribute('dir', dir);
        }
    }

    function processAllSmartRTL(root) {
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        const base = root || document.body;
        if (!base) return;
        applySmartDirectionToElement(base);
        const selector = 'p, h1, h2, h3, h4, h5, h6, li, ul, ol, blockquote, table, .artifact-card, span.line-clamp-3, [data-testid="user-input-step"] .whitespace-pre-wrap, .leading-relaxed';
        try {
            const elements = base.querySelectorAll(selector);
            for (let i = 0; i < elements.length; i++) {
                applySmartDirectionToElement(elements[i]);
            }
        } catch(e) {}
    }

    // --- Menubar Button & Settings Popover ---
    let popoverInstance = null;

    function initAppearanceMenu() {
        const bar = document.querySelector('[data-testid="title-menu-bar"]');
        if (!bar) return;

        let container = document.getElementById('ag-appearance-menu-container');
        if (container) return;

        container = document.createElement('div');
        container.id = 'ag-appearance-menu-container';
        container.className = 'relative';
        container.style.appRegion = 'no-drag';

        const btn = document.createElement('button');
        btn.id = 'ag-appearance-menu-btn';
        btn.className = 'inline-flex items-center font-medium transition-colors select-none outline-none cursor-pointer justify-center disabled:opacity-50 bg-transparent text-muted-foreground hover:text-foreground hover:bg-secondary focus-visible:text-foreground focus-visible:bg-secondary h-7 text-sm rounded-md gap-1.5 px-2.5 select-none';
        btn.setAttribute('data-testid', 'title-menu-bar-item');
        btn.title = 'تنظیمات ظاهر و راست‌چین (Appearance & RTL Settings)';
        btn.innerHTML = \`
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.85;">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Appearance</span>
        \`;
        container.appendChild(btn);
        bar.appendChild(container);

        function closePopover() {
            if (popoverInstance) {
                popoverInstance.remove();
                popoverInstance = null;
                btn.classList.remove('bg-secondary', 'text-foreground');
            }
        }

        function openPopover() {
            if (popoverInstance) {
                closePopover();
                return;
            }

            btn.classList.add('bg-secondary', 'text-foreground');
            const rect = btn.getBoundingClientRect();

            popoverInstance = document.createElement('div');
            popoverInstance.id = 'ag-appearance-popover';
            popoverInstance.style.cssText = \`
                position: fixed;
                top: \${rect.bottom + 4}px;
                left: \${Math.min(rect.left, window.innerWidth - 330)}px;
                width: 320px;
                background: #18181b;
                border: 1px solid rgba(255, 255, 255, 0.14);
                color: #f4f4f5;
                font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                direction: rtl;
                padding: 14px;
                border-radius: 12px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
                z-index: 999999;
                user-select: none;
            \`;

            popoverInstance.innerHTML = \`
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 14px; font-weight: 600; color: #fff;">تنظیمات ظاهر و راست‌چین</span>
                    </div>
                    <span style="font-size: 11px; padding: 2px 7px; background: rgba(59, 130, 246, 0.2); color: #60a5fa; border-radius: 4px; font-weight: 500;">v2.5</span>
                </div>

                <!-- RTL Toggle -->
                <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.03); padding: 10px 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.06);">
                    <div>
                        <div style="font-size: 13px; font-weight: 500; color: #fff;">راست‌چین هوشمند (RTL)</div>
                        <div style="font-size: 11px; color: #a1a1aa; margin-top: 2px;">متن‌های فارسی، پنل‌ها و کادر تایپ</div>
                    </div>
                    <div id="ag-toggle-rtl" style="width: 44px; height: 24px; background: \${currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46'}; border-radius: 12px; position: relative; cursor: pointer; transition: background .2s;">
                        <div id="ag-toggle-knob" style="position: absolute; width: 18px; height: 18px; background: white; border-radius: 50%; top: 3px; right: \${currentSettings.rtlEnabled ? '4px' : '22px'}; transition: right .2s;"></div>
                    </div>
                </div>

                <!-- Font Family Selection -->
                <div style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 12px; font-weight: 500; color: #d4d4d8; margin-bottom: 6px;">قلم فارسی (Font Family):</label>
                    <select id="ag-font-family-select" style="width: 100%; background: #27272a; color: #f4f4f5; border: 1px solid rgba(255,255,255,0.14); border-radius: 6px; padding: 6px 10px; font-size: 12.5px; outline: none; font-family: inherit; cursor: pointer;">
                        <option value="Vazirmatn" \${currentSettings.fontFamily === 'Vazirmatn' ? 'selected' : ''}>وزیرمتن (Vazirmatn - پیش‌فرض)</option>
                        <option value="Shabnam" \${currentSettings.fontFamily === 'Shabnam' ? 'selected' : ''}>شبنم (Shabnam)</option>
                        <option value="Sahel" \${currentSettings.fontFamily === 'Sahel' ? 'selected' : ''}>ساحل (Sahel)</option>
                        <option value="Samim" \${currentSettings.fontFamily === 'Samim' ? 'selected' : ''}>صمیم (Samim)</option>
                        <option value="Tahoma" \${currentSettings.fontFamily === 'Tahoma' ? 'selected' : ''}>تاهما (Tahoma)</option>
                        <option value="System" \${currentSettings.fontFamily === 'System' ? 'selected' : ''}>فونت سیستم (System Font)</option>
                        <option value="Custom" \${currentSettings.fontFamily === 'Custom' ? 'selected' : ''}>فونت دلخواه (سفارشی)...</option>
                    </select>
                    <div id="ag-custom-font-container" style="display: \${currentSettings.fontFamily === 'Custom' ? 'block' : 'none'}; margin-top: 6px;">
                        <input type="text" id="ag-custom-font-input" placeholder="نام فونت (مثلاً: B Yekan, Dana)" value="\${currentSettings.customFont || ''}" style="width: 100%; background: #202023; color: #fff; border: 1px solid rgba(59,130,246,0.5); border-radius: 6px; padding: 5px 8px; font-size: 12px; outline: none; box-sizing: border-box;">
                    </div>
                </div>

                <!-- Font Size Stepper & Slider -->
                <div style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 12px; font-weight: 500; color: #d4d4d8;">اندازه متن چت (Font Size):</span>
                        <span id="ag-font-size-badge" style="font-size: 12px; font-weight: 600; color: #60a5fa; background: rgba(59, 130, 246, 0.15); padding: 1px 8px; border-radius: 4px; direction: ltr;">\${currentSettings.fontSize}px</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; direction: ltr;">
                        <button id="ag-font-dec" style="width: 32px; height: 28px; background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 600;">-</button>
                        <input type="range" id="ag-font-size-slider" min="12" max="22" value="\${currentSettings.fontSize}" step="1" style="flex: 1; accent-color: #3b82f6; cursor: pointer;">
                        <button id="ag-font-inc" style="width: 32px; height: 28px; background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 600;">+</button>
                    </div>
                </div>

                <!-- Line Height -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 12px; font-weight: 500; color: #d4d4d8;">فاصله خطوط (Line Height):</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px;">
                        <button class="ag-lh-btn" data-lh="1.5" style="background: \${currentSettings.lineHeight === 1.5 ? '#3b82f6' : '#27272a'}; border: 1px solid \${currentSettings.lineHeight === 1.5 ? '#3b82f6' : 'rgba(255,255,255,0.1)'}; color: \${currentSettings.lineHeight === 1.5 ? '#fff' : '#a1a1aa'}; border-radius: 6px; padding: 4px 0; font-size: 11.5px; cursor: pointer; font-family: inherit;">فشرده</button>
                        <button class="ag-lh-btn" data-lh="1.75" style="background: \${currentSettings.lineHeight === 1.75 ? '#3b82f6' : '#27272a'}; border: 1px solid \${currentSettings.lineHeight === 1.75 ? '#3b82f6' : 'rgba(255,255,255,0.1)'}; color: \${currentSettings.lineHeight === 1.75 ? '#fff' : '#a1a1aa'}; border-radius: 6px; padding: 4px 0; font-size: 11.5px; font-weight: 500; cursor: pointer; font-family: inherit;">معمولی</button>
                        <button class="ag-lh-btn" data-lh="2.0" style="background: \${currentSettings.lineHeight === 2.0 ? '#3b82f6' : '#27272a'}; border: 1px solid \${currentSettings.lineHeight === 2.0 ? '#3b82f6' : 'rgba(255,255,255,0.1)'}; color: \${currentSettings.lineHeight === 2.0 ? '#fff' : '#a1a1aa'}; border-radius: 6px; padding: 4px 0; font-size: 11.5px; cursor: pointer; font-family: inherit;">باز</button>
                    </div>
                </div>

                <!-- Footer Actions -->
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px;">
                    <button id="ag-reset-defaults" style="background: transparent; border: none; color: #a1a1aa; font-size: 11.5px; cursor: pointer; padding: 4px 6px; border-radius: 4px; display: flex; align-items: center; gap: 4px; font-family: inherit;">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
                        <span>پیش‌فرض</span>
                    </button>
                    <button id="ag-close-popover" style="background: #27272a; border: 1px solid rgba(255,255,255,0.15); color: #f4f4f5; font-size: 11.5px; cursor: pointer; padding: 4px 14px; border-radius: 6px; font-weight: 500; font-family: inherit;">
                        بستن
                    </button>
                </div>
            \`;

            document.body.appendChild(popoverInstance);

            const toggleBtn = popoverInstance.querySelector('#ag-toggle-rtl');
            const knob = popoverInstance.querySelector('#ag-toggle-knob');
            toggleBtn.onclick = () => {
                currentSettings.rtlEnabled = !currentSettings.rtlEnabled;
                toggleBtn.style.background = currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46';
                knob.style.right = currentSettings.rtlEnabled ? '4px' : '22px';
                applySettings(currentSettings);
                saveSettings(currentSettings);
            };

            const fontSelect = popoverInstance.querySelector('#ag-font-family-select');
            const customContainer = popoverInstance.querySelector('#ag-custom-font-container');
            const customInput = popoverInstance.querySelector('#ag-custom-font-input');
            fontSelect.onchange = () => {
                currentSettings.fontFamily = fontSelect.value;
                if (fontSelect.value === 'Custom') {
                    customContainer.style.display = 'block';
                    customInput.focus();
                } else {
                    customContainer.style.display = 'none';
                }
                applySettings(currentSettings);
                saveSettings(currentSettings);
            };

            customInput.oninput = () => {
                currentSettings.customFont = customInput.value.trim();
                applySettings(currentSettings);
                saveSettings(currentSettings);
            };

            const sizeSlider = popoverInstance.querySelector('#ag-font-size-slider');
            const sizeBadge = popoverInstance.querySelector('#ag-font-size-badge');
            const decBtn = popoverInstance.querySelector('#ag-font-dec');
            const incBtn = popoverInstance.querySelector('#ag-font-inc');

            function updateFontSize(val) {
                val = Math.max(12, Math.min(22, parseInt(val) || 15));
                currentSettings.fontSize = val;
                sizeSlider.value = val;
                sizeBadge.textContent = val + 'px';
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }

            sizeSlider.oninput = () => updateFontSize(sizeSlider.value);
            decBtn.onclick = () => updateFontSize(currentSettings.fontSize - 1);
            incBtn.onclick = () => updateFontSize(currentSettings.fontSize + 1);

            const lhButtons = popoverInstance.querySelectorAll('.ag-lh-btn');
            lhButtons.forEach(b => {
                b.onclick = () => {
                    const lh = parseFloat(b.getAttribute('data-lh'));
                    currentSettings.lineHeight = lh;
                    lhButtons.forEach(btnEl => {
                        const active = parseFloat(btnEl.getAttribute('data-lh')) === lh;
                        btnEl.style.background = active ? '#3b82f6' : '#27272a';
                        btnEl.style.borderColor = active ? '#3b82f6' : 'rgba(255,255,255,0.1)';
                        btnEl.style.color = active ? '#fff' : '#a1a1aa';
                    });
                    applySettings(currentSettings);
                    saveSettings(currentSettings);
                };
            });

            popoverInstance.querySelector('#ag-reset-defaults').onclick = () => {
                currentSettings = Object.assign({}, DEFAULT_SETTINGS);
                applySettings(currentSettings);
                saveSettings(currentSettings);
                closePopover();
                openPopover();
            };

            popoverInstance.querySelector('#ag-close-popover').onclick = closePopover;
        }

        btn.onclick = (e) => {
            e.stopPropagation();
            if (popoverInstance) closePopover();
            else openPopover();
        };

        document.addEventListener('pointerdown', (e) => {
            if (!popoverInstance) return;
            if (popoverInstance.contains(e.target) || container.contains(e.target)) return;
            closePopover();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && popoverInstance) closePopover();
        });
    }

    function initAll() {
        applySettings(currentSettings);
        initAppearanceMenu();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        initAll();
    }

    setInterval(initAppearanceMenu, 800);

    // --- Dynamic Observer for Chat Messages ---
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
        } else {
            setTimeout(startObserver, 50);
        }
    }

    startObserver();
})();
} catch(e) {
    console.error("[Antigravity-RTL] Injection error:", e);
}
`;

    if (preloadCode.includes('/* __ANTIGRAVITY_RTL_INJECTED__ */')) {
        preloadCode = preloadCode.split('/* __ANTIGRAVITY_RTL_INJECTED__ */')[0];
    }

    const patchedPreload = preloadCode + '\n' + injection;
    const replacements = { 'dist/preload.js': patchedPreload };

    const thisScript = path.resolve(__filename);
    let patchBat = path.join(path.dirname(thisScript), 'patch.bat');
    if (!fs.existsSync(patchBat)) {
        patchBat = path.join(path.dirname(path.dirname(thisScript)), 'patch.bat');
    }function setupShortcuts(targetDir, launcherPath) {
    const destLauncher = path.join(targetDir, 'AntigravityLauncher.exe');
    try {
        fs.copyFileSync(launcherPath, destLauncher);
    } catch(e) {}
    const targetExe = fs.existsSync(destLauncher) ? destLauncher : launcherPath;
    const iconSource = path.join(targetDir, 'Antigravity.exe');
    const psCode = `
    $wsh = New-Object -ComObject WScript.Shell
    $paths = @(
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonDesktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonStartMenu'), 'Programs', 'Antigravity.lnk')
    )
    $found = $false
    foreach ($p in $paths) {
        if (Test-Path $p) {
            $sc = $wsh.CreateShortcut($p)
            $sc.TargetPath = '${targetExe.replace(/'/g, "''")}'
            $sc.IconLocation = '${iconSource.replace(/'/g, "''")},0'
            $sc.WorkingDirectory = '${targetDir.replace(/'/g, "''")}'
            $sc.Save()
            $found = $true
        }
    }
    if (-not $found) {
        $desktopP = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk')
        $sc = $wsh.CreateShortcut($desktopP)
        $sc.TargetPath = '${targetExe.replace(/'/g, "''")}'
        $sc.IconLocation = '${iconSource.replace(/'/g, "''")},0'
        $sc.WorkingDirectory = '${targetDir.replace(/'/g, "''")}'
        $sc.Save()
    }
    `;
    try {
        execSync(`powershell -NoProfile -Command "${psCode.replace(/\r?\n/g, ' ')}"`, { stdio: 'ignore' });
        console.log('  [✓] شیلد ضدآپدیت و شورت‌کات‌ها با موفقیت محافظت شدند.');
    } catch(e) {}
}

function restoreShortcuts(targetDir) {
    const realExe = path.join(targetDir, 'Antigravity.exe');
    const psCode = `
    $wsh = New-Object -ComObject WScript.Shell
    $paths = @(
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonDesktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonStartMenu'), 'Programs', 'Antigravity.lnk')
    )
    foreach ($p in $paths) {
        if (Test-Path $p) {
            $sc = $wsh.CreateShortcut($p)
            $sc.TargetPath = '${realExe.replace(/'/g, "''")}'
            $sc.IconLocation = '${realExe.replace(/'/g, "''")},0'
            $sc.WorkingDirectory = '${targetDir.replace(/'/g, "''")}'
            $sc.Save()
        }
    }
    `;
    try {
        execSync(`powershell -NoProfile -Command "${psCode.replace(/\r?\n/g, ' ')}"`, { stdio: 'ignore' });
    } catch(e) {}
}

function deployPermanentEngine(targetDir) {
    const scriptDir = __dirname;
    const rootDir = path.basename(scriptDir).toLowerCase() === 'src' ? path.dirname(scriptDir) : scriptDir;
    const srcDir = fs.existsSync(path.join(rootDir, 'src')) ? path.join(rootDir, 'src') : rootDir;

    const files = [
        [path.join(srcDir, 'patcher.py'), 'patcher.py'],
        [path.join(srcDir, 'patcher.js'), 'patcher.js'],
        [path.join(srcDir, 'antigravity-chat-rtl.css'), 'antigravity-chat-rtl.css'],
        [path.join(rootDir, 'patch.bat'), 'patch.bat']
    ];

    const targetDirs = [
        path.join(process.env.APPDATA || '', 'Antigravity', 'rtl-patch'),
        path.join(targetDir, 'resources', 'rtl-patch')
    ];

    for (const tdir of targetDirs) {
        try {
            if (!fs.existsSync(tdir)) fs.mkdirSync(tdir, { recursive: true });
            for (const [srcF, fname] of files) {
                if (fs.existsSync(srcF)) fs.copyFileSync(srcF, path.join(tdir, fname));
            }
        } catch(e) {}
    }

    let launcherSrc = path.join(srcDir, 'AntigravityLauncher.exe');
    if (!fs.existsSync(launcherSrc)) launcherSrc = path.join(rootDir, 'AntigravityLauncher.exe');
    if (fs.existsSync(launcherSrc)) {
        setupShortcuts(targetDir, launcherSrc);
    }
}

    // Hook updater files to automatically re-patch after future updates
    const hookBody = `
    /* __ANTIGRAVITY_UPDATE_HOOK__ */
    try {
        const cp = require("child_process");
        const path = require("path");
        const fs = require("fs");
        const appData = process.env.APPDATA || "";
        const appDataPatch = path.join(appData, "Antigravity", "rtl-patch", "patcher.py");
        const resPatch = path.join(process.resourcesPath, "rtl-patch", "patcher.py");
        const patchPy = fs.existsSync(appDataPatch) ? appDataPatch : resPatch;
        const patchJs = patchPy.replace(/\\.py$/, ".js");
        const patchBat = path.join(path.dirname(patchPy), "patch.bat");

        try {
            cp.spawn("pythonw.exe", [patchPy, "--wait-for-update"], { detached: true, stdio: "ignore" }).unref();
        } catch(e1) {
            try {
                cp.spawn(process.execPath, [patchJs, "--wait-for-update"], {
                    env: Object.assign({}, process.env, { ELECTRON_RUN_AS_NODE: "1" }),
                    detached: true,
                    stdio: "ignore"
                }).unref();
            } catch(e2) {
                cp.spawn("cmd.exe", ["/c", patchBat, "--wait-for-update"], { detached: true, stdio: "ignore" }).unref();
            }
        }
    } catch(e) {}
`;

    if (updaterCode && updaterCode.includes('function quitAndInstall() {')) {
        replacements['dist/updater.js'] = updaterCode.replace(
            'function quitAndInstall() {',
            'function quitAndInstall() {' + hookBody
        );
    }

    if (nsisCode && nsisCode.includes('doInstall(options) {')) {
        replacements['node_modules/electron-updater/out/NsisUpdater.js'] = nsisCode.replace(
            'doInstall(options) {',
            'doInstall(options) {' + hookBody
        );
    }

    if (baseCode && baseCode.includes('install(isSilent = false, isForceRunAfter = false) {')) {
        replacements['node_modules/electron-updater/out/BaseUpdater.js'] = baseCode.replace(
            'install(isSilent = false, isForceRunAfter = false) {',
            'install(isSilent = false, isForceRunAfter = false) {' + hookBody
        );
    }

    console.log('\n[*] در حال بازسازی و جایگذاری پکیج برنامه (app.asar)...');
    try {
        patchAsar(sourceAsar, tempAsar, replacements);
        try {
            fs.renameSync(tempAsar, asarPath);
        } catch (err) {
            const data = fs.readFileSync(tempAsar);
            const fd = fs.openSync(asarPath, 'r+');
            fs.writeSync(fd, data, 0, data.length, 0);
            fs.ftruncateSync(fd, data.length);
            fs.closeSync(fd);
            if (fs.existsSync(tempAsar)) fs.unlinkSync(tempAsar);
        }

        deployPermanentEngine(targetDir);

        console.log('\n' + '='.repeat(65));
        console.log('[✓] پچ جامع راست‌چین و شیلد ضدآپدیت با موفقیت اعمال شد!');
        console.log('='.repeat(65));
        console.log('  • جهت‌بندی هوشمند خودکار خط‌به‌خط (فارسی: راست‌چین | انگلیسی: چپ‌چین)');
        console.log('  • فونت یکدست و منوی Appearance در نوار بالای برنامه');
        console.log('  • استقرار دائم موتور پچ در پوشه آنتی‌گراویتی (محافظت در برابر آپدیت)');
        console.log('  • مصون‌سازی ۱۰۰٪ کادر ابزارها، لاگ‌ها، Thought، تایمرها و بخش‌های فنی');
        console.log('='.repeat(65));

        return true;
    } catch (e) {
        console.log(`[-] خطا در اعمال پچ: ${e.message}`);
        if (fs.existsSync(tempAsar)) {
            try { fs.unlinkSync(tempAsar); } catch (ex) {}
        }
        return false;
    }
}

function doRestore(targetDir, kill = false) {
    const resourcesDir = path.join(targetDir, 'resources');
    const asarPath = path.join(resourcesDir, 'app.asar');
    let backupPath = path.join(resourcesDir, 'app.asar.original_backup');

    if (!fs.existsSync(backupPath)) {
        const alt = path.join(resourcesDir, 'app.asar.backup');
        if (fs.existsSync(alt)) backupPath = alt;
    }

    if (!fs.existsSync(backupPath)) {
        console.log(`[-] خطا: فایل نسخه پشتیبان اولیه (${backupPath}) یافت نشد.`);
        return false;
    }

    if (kill && isRunning()) closeAntigravity();

    console.log('[*] در حال بازگردانی فایل app.asar از نسخه پشتیبان کارخانه...');
    try {
        try {
            fs.copyFileSync(backupPath, asarPath);
        } catch (e) {
            const data = fs.readFileSync(backupPath);
            const fd = fs.openSync(asarPath, 'r+');
            fs.writeSync(fd, data, 0, data.length, 0);
            fs.ftruncateSync(fd, data.length);
            fs.closeSync(fd);
        }

        restoreShortcuts(targetDir);
        try {
            const launcherExe = path.join(targetDir, 'AntigravityLauncher.exe');
            if (fs.existsSync(launcherExe)) fs.unlinkSync(launcherExe);
            const resPatch = path.join(targetDir, 'resources', 'rtl-patch');
            if (fs.existsSync(resPatch)) fs.rmdirSync(resPatch, { recursive: true });
            const appdataPatch = path.join(process.env.APPDATA || '', 'Antigravity', 'rtl-patch');
            if (fs.existsSync(appdataPatch)) fs.rmdirSync(appdataPatch, { recursive: true });
        } catch(e) {}

        console.log('\n' + '='.repeat(65));
        console.log('[✓] نرم‌افزار با موفقیت به نسخه اصلی و اولیه کارخانه بازگردانده شد.');
        console.log('='.repeat(65));
        return true;
    } catch (e) {
        console.log(`[-] خطا در بازگردانی: ${e.message}`);
        return false;
    }
}

function waitForUpdateThenPatch(targetDir) {
    let installerFound = false;
    for (let i = 0; i < 15; i++) {
        try {
            const out = execSync('tasklist /FI "IMAGENAME eq installer.exe"', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
            if (out.toLowerCase().includes('installer.exe')) {
                installerFound = true;
                break;
            }
        } catch(e) {}
        try { execSync('ping 127.0.0.1 -n 3 >nul'); } catch(e) {}
    }

    if (installerFound) {
        for (let i = 0; i < 60; i++) {
            try {
                const out = execSync('tasklist /FI "IMAGENAME eq installer.exe"', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
                if (!out.toLowerCase().includes('installer.exe')) break;
            } catch(e) {
                break;
            }
            try { execSync('ping 127.0.0.1 -n 3 >nul'); } catch(e) {}
        }
    } else {
        try { execSync('ping 127.0.0.1 -n 6 >nul'); } catch(e) {}
    }

    try { execSync('ping 127.0.0.1 -n 4 >nul'); } catch(e) {}
    doPatch(targetDir, false);
}

function launchAntigravity(targetDir) {
    const exe = path.join(targetDir, 'Antigravity.exe');
    if (fs.existsSync(exe)) {
        console.log('[*] در حال اجرای Antigravity...');
        const child = spawn(exe, [], { detached: true, stdio: 'ignore', cwd: targetDir });
        child.unref();
    }
}

function main() {
    const args = process.argv.slice(2);
    let customPath = null;
    const pathIdx = args.findIndex(a => a === '--path' || a === '-p');
    if (pathIdx !== -1 && args[pathIdx + 1]) {
        customPath = args[pathIdx + 1];
    }

    const targetDir = findAntigravityPath(customPath);

    if (args.includes('--wait-for-update')) {
        if (targetDir) waitForUpdateThenPatch(targetDir);
        process.exit(0);
    }

    if (args.includes('--check-only')) {
        if (targetDir) {
            const asarPath = path.join(targetDir, 'resources', 'app.asar');
            const preload = extractFromAsar(asarPath, 'dist/preload.js');
            const isPatched = preload && preload.includes('__ANTIGRAVITY_RTL_INJECTED__');
            console.log(isPatched ? '1' : '0');
        } else {
            console.log('0');
        }
        process.exit(0);
    }

    printBanner();

    if (!targetDir) {
        console.log('[-] مسیر نصب Antigravity پیدا نشد.');
        process.exit(1);
    }

    console.log(`[✓] مسیر نصب شناسایی‌شده:\n    ${targetDir}\n`);

    if (args.includes('2') || args.includes('--restore') || args.includes('-r')) {
        doRestore(targetDir);
        if (args.includes('--launch')) launchAntigravity(targetDir);
        return;
    }

    const noKill = args.includes('--no-kill');

    if (args.includes('1') || args.includes('--apply') || args.includes('-a')) {
        const ok = doPatch(targetDir, noKill);
        if (ok && args.includes('--launch')) launchAntigravity(targetDir);
        return;
    }

    // Default action: apply patch
    const ok = doPatch(targetDir, noKill);
    if (ok) {
        console.log('\n[i] برای اجرای برنامه کلید اینتر را بزنید.');
    }
}

if (require.main === module) {
    main();
}
