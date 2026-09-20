#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
Antigravity RTL & Smart Typography Unified Patcher
پچ جامع و هوشمند راست‌چین‌سازی چت و تنظیم فونت در آنتی‌گراویتی
====================================================================
"""

import os
import sys
import json
import struct
import shutil
import hashlib
import subprocess
import time
import re

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

RTL_CSS = """/**
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
body:not(.ag-rtl-disabled) #antigravity\.agentSidePanelInputBox [contenteditable="true"] {
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
body:not(.ag-rtl-disabled) #antigravity\.agentSidePanelInputBox [contenteditable="true"] {
  direction: rtl !important;
  text-align: right !important;
  unicode-bidi: plaintext !important;
  font-family: var(--ag-font-family) !important;
}

body:not(.ag-rtl-disabled) #antigravity\.agentSidePanelInputBox p.pointer-events-none {
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
body.ag-rtl-disabled #antigravity\.agentSidePanelInputBox p.pointer-events-none {
  direction: ltr !important;
  text-align: left !important;
  left: 0.5rem !important;
  right: auto !important;
}
body.ag-rtl-disabled button[aria-label*="Send"] svg {
  transform: none !important;
}
"""
# Enable ANSI support on Windows
if sys.platform == "win32":
    os.system('')

CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"
CLR_DIM = "\033[2m"
CLR_CYAN = "\033[96m"
CLR_BLUE = "\033[94m"
CLR_GREEN = "\033[92m"
CLR_YELLOW = "\033[93m"
CLR_RED = "\033[91m"
CLR_MAGENTA = "\033[95m"
CLR_WHITE = "\033[97m"
CLR_GRAY = "\033[90m"

ANSI_RE = re.compile(r'\x1b\[[0-9;]*[mGKH]')

def visible_len(s):
    return len(ANSI_RE.sub('', s))

def render_shadow_card(title, lines, width=74, border_color="\033[96m"):
    title_str = f" [ {title} ] "
    dash_len = width - visible_len(title_str) - 1
    top = f"  {border_color}┌─{title_str}" + ("─" * max(0, dash_len)) + f"┐{CLR_RESET}"
    
    result = [top]
    for line in lines:
        vlen = visible_len(line)
        pad = max(0, width - 2 - vlen)
        result.append(f"  {border_color}│{CLR_RESET}  {line}" + (" " * pad) + f"{border_color}│{CLR_RESET}")
        
    bot = f"  {border_color}└" + ("─" * width) + f"┘{CLR_RESET}"
    result.append(bot)
    return "\n".join(result)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_gradient_logo():
    raw_logo = r'''    ___    _   ___________ ________  ___ _    ___________ __  __
   /   |  / | / /_  __/  _/ ____/ __ \/   | |  / /  _/_  __/\ \/ /
  / /| | /  |/ / / /  / // / __/ /_/ / /| | | / // /  / /    \  / 
 / ___ |/ /|  / / / _/ // /_/ / _, _/ ___ | |/ // /  / /     / /  
/_/  |_/_/ |_/ /_/ /___/\____/_/ |_/_/  |_|___/___/ /_/     /_/   
                      ____  _____  __     
                     / __ \/_  __/ /      
                    / /_/ / / / / /       
                   / _, _/ / / / /___     
                  /_/ |_| /_/ /_____/     '''
    
    stops = [
        (0, 242, 254),    # Cyber Cyan
        (79, 110, 247),   # Royal Indigo
        (247, 37, 133)    # Neon Magenta
    ]
    
    def interpolate(s, t):
        t = max(0.0, min(1.0, t))
        idx = t * (len(s) - 1)
        i = int(idx)
        if i >= len(s) - 1:
            return s[-1]
        sub = idx - i
        c1, c2 = s[i], s[i + 1]
        return (
            int(c1[0] + (c2[0] - c1[0]) * sub),
            int(c1[1] + (c2[1] - c1[1]) * sub),
            int(c1[2] + (c2[2] - c1[2]) * sub)
        )
    
    lines = raw_logo.strip('\n').split('\n')
    max_w = max(len(l) for l in lines)
    out = []
    for line in lines:
        line_chars = []
        for col, ch in enumerate(line):
            if ch == ' ':
                line_chars.append(' ')
            else:
                t = col / max(1, max_w - 1)
                r, g, b = interpolate(stops, t)
                line_chars.append(f"\033[38;2;{r};{g};{b};1m{ch}")
        line_chars.append(CLR_RESET)
        out.append(''.join(line_chars))
    return '\n'.join(out)

def print_banner():
    logo = get_gradient_logo()
    print(logo)
    print(f"  {CLR_GRAY}──────────────────────────────────────────────────────────────────────────{CLR_RESET}")
    print(f"      {CLR_WHITE}{CLR_BOLD}:::  Smart RTL & Modern Appearance Engine for Antigravity  :::{CLR_RESET}")
    print(f"             {CLR_DIM}https://github.com/yasin-saeedi/antigravity-rtl{CLR_RESET}\n")

def get_system_status(target_dir):
    is_patched = False
    if target_dir:
        asar = os.path.join(target_dir, "resources", "app.asar")
        preload = extract_file_from_asar(asar, "dist/preload.js")
        is_patched = "__ANTIGRAVITY_RTL_INJECTED__" in (preload or "")
    is_running = is_antigravity_running()
    return is_patched, is_running

def find_antigravity_path(custom_path=None):
    """Detect Antigravity installation directory"""
    if custom_path:
        cp = os.path.abspath(custom_path.strip().strip('"'))
        asar = os.path.join(cp, "resources", "app.asar")
        exe = os.path.join(cp, "Antigravity.exe")
        if os.path.isfile(asar) and os.path.isfile(exe):
            return cp
        if os.path.isfile(cp):
            parent = os.path.dirname(cp)
            if os.path.basename(parent) == "resources":
                parent = os.path.dirname(parent)
            asar = os.path.join(parent, "resources", "app.asar")
            exe = os.path.join(parent, "Antigravity.exe")
            if os.path.isfile(asar) and os.path.isfile(exe):
                return parent

    candidates = []

    # 1. Active running processes
    try:
        ps_cmd = 'Get-Process Antigravity -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Path'
        res = subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd], capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and res.stdout.strip():
            for line in res.stdout.strip().splitlines():
                p = line.strip()
                if os.path.isfile(p) and p.lower().endswith("antigravity.exe"):
                    d = os.path.dirname(p)
                    if d not in candidates: candidates.append(d)
    except Exception:
        pass

    # 2. LocalAppData standard installation
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        std_path = os.path.join(local_app_data, "Programs", "antigravity")
        if os.path.isdir(std_path) and std_path not in candidates:
            candidates.append(std_path)

    # 3. Registry search
    try:
        import winreg
        for root_key in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
            try:
                with winreg.OpenKey(root_key, r"Software\Microsoft\Windows\CurrentVersion\Uninstall") as key:
                    count, _, _ = winreg.QueryInfoKey(key)
                    for i in range(count):
                        try:
                            app_guid = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, app_guid) as app_key:
                                try:
                                    name, _ = winreg.QueryValueEx(app_key, "DisplayName")
                                    if name and "antigravity" in name.lower():
                                        loc, _ = winreg.QueryValueEx(app_key, "InstallLocation")
                                        if loc and os.path.isdir(loc) and loc not in candidates:
                                            candidates.append(loc)
                                        icon, _ = winreg.QueryValueEx(app_key, "DisplayIcon")
                                        if icon and os.path.isfile(icon):
                                            d = os.path.dirname(icon)
                                            if d not in candidates: candidates.append(d)
                                except Exception:
                                    pass
                        except Exception:
                            pass
            except Exception:
                pass
    except Exception:
        pass

    # 4. Program Files & AppData variants
    for env_var in ["ProgramFiles", "ProgramFiles(x86)", "ProgramW6432"]:
        pf = os.environ.get(env_var, "")
        if pf:
            p1 = os.path.join(pf, "Antigravity")
            p2 = os.path.join(pf, "antigravity")
            if os.path.isdir(p1) and p1 not in candidates: candidates.append(p1)
            if os.path.isdir(p2) and p2 not in candidates: candidates.append(p2)

    roaming = os.environ.get("APPDATA", "")
    if roaming:
        p_roam = os.path.join(roaming, "Programs", "antigravity")
        if os.path.isdir(p_roam) and p_roam not in candidates:
            candidates.append(p_roam)

    for c in candidates:
        asar = os.path.join(c, "resources", "app.asar")
        exe = os.path.join(c, "Antigravity.exe")
        if os.path.isfile(asar) and os.path.isfile(exe):
            return c

    return None

def is_antigravity_running():
    try:
        res = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Antigravity.exe'], capture_output=True, text=True)
        return 'antigravity.exe' in res.stdout.lower()
    except Exception:
        return False

def close_antigravity():
    print("[*] در حال بستن فرآیندهای در حال اجرای Antigravity...")
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'Antigravity.exe', '/T'], capture_output=True)
        time.sleep(1.5)
    except Exception:
        pass

def sha256_blocks(data, block_size=4*1024*1024):
    blocks = []
    for i in range(0, len(data), block_size):
        chunk = data[i:i+block_size]
        blocks.append(hashlib.sha256(chunk).hexdigest())
    return {
        "algorithm": "SHA256",
        "hash": hashlib.sha256(data).hexdigest(),
        "blockSize": block_size,
        "blocks": blocks
    }

def patch_asar(input_asar, output_asar, replacements):
    with open(input_asar, "rb") as f:
        header_raw = f.read(16)
        magic, size_total, size_header, json_len = struct.unpack('<IIII', header_raw)
        if magic != 4:
            raise ValueError(f"قالب نامعتبر ASAR (Magic: {magic})")

        json_bytes = f.read(json_len)
        header = json.loads(json_bytes.decode('utf-8'))

        padding = (4 - (json_len % 4)) % 4
        payload_start = 16 + json_len + padding

        file_entries = []
        def traverse(curr, parts):
            if "files" in curr:
                for name, child in curr["files"].items():
                    traverse(child, parts + [name])
            else:
                is_unpacked = curr.get("unpacked", False)
                file_entries.append((parts, is_unpacked, curr))

        traverse(header, [])

        new_payload = bytearray()
        current_offset = 0

        for parts, is_unpacked, node in file_entries:
            path_str = "/".join(parts)
            if is_unpacked:
                continue

            if path_str in replacements:
                content = replacements[path_str]
                if isinstance(content, str):
                    content = content.encode('utf-8')
                print(f"  [+] به‌روزرسانی در پکیج: {path_str} ({len(content):,} بایت)")
            else:
                old_offset = int(node["offset"])
                old_size = node["size"]
                f.seek(payload_start + old_offset)
                content = f.read(old_size)

            node["offset"] = str(current_offset)
            node["size"] = len(content)
            node["integrity"] = sha256_blocks(content)
            new_payload.extend(content)
            current_offset += len(content)

    new_json_bytes = json.dumps(header, separators=(',', ':')).encode('utf-8')
    new_json_len = len(new_json_bytes)
    new_padding_len = (4 - (new_json_len % 4)) % 4
    new_padding = b'\0' * new_padding_len

    new_size_header = new_json_len + new_padding_len + 4
    new_size_total = new_size_header + 4
    new_header_prefix = struct.pack('<IIII', 4, new_size_total, new_size_header, new_json_len)

    with open(output_asar, "wb") as out:
        out.write(new_header_prefix)
        out.write(new_json_bytes)
        out.write(new_padding)
        out.write(new_payload)

def extract_file_from_asar(asar_path, target_rel_path):
    with open(asar_path, "rb") as f:
        header_raw = f.read(16)
        magic, size_total, size_header, json_len = struct.unpack('<IIII', header_raw)
        json_bytes = f.read(json_len)
        header = json.loads(json_bytes.decode('utf-8'))
        padding = (4 - (json_len % 4)) % 4
        payload_start = 16 + json_len + padding

        parts = target_rel_path.split("/")
        curr = header
        for p in parts:
            if "files" in curr and p in curr["files"]:
                curr = curr["files"][p]
            else:
                return None

        offset = int(curr["offset"])
        size = curr["size"]
        f.seek(payload_start + offset)
        return f.read(size).decode('utf-8', errors='ignore')

def get_asar_metadata(asar_path):
    if not asar_path or not os.path.isfile(asar_path):
        return None
    try:
        mtime = os.path.getmtime(asar_path)
        pkg_str = extract_file_from_asar(asar_path, "package.json")
        version_str = "0.0.0"
        if pkg_str:
            try:
                version_str = json.loads(pkg_str).get("version", "0.0.0")
            except Exception:
                pass
        v_parts = []
        for part in re.split(r'[-+.]', version_str):
            if part.isdigit():
                v_parts.append(int(part))
            else:
                break
        while len(v_parts) < 3:
            v_parts.append(0)
        version_tuple = tuple(v_parts)
        preload_str = extract_file_from_asar(asar_path, "dist/preload.js")
        is_patched = bool(preload_str and "__ANTIGRAVITY_RTL_INJECTED__" in preload_str)
        return {
            "version_str": version_str,
            "version_tuple": version_tuple,
            "is_patched": is_patched,
            "mtime": mtime
        }
    except Exception:
        return None

def get_injection_snippet():
    clean_css = RTL_CSS.replace("\\", "\\\\").replace("`", "\`")
    return f"""
/* __ANTIGRAVITY_RTL_INJECTED__ */
try {{
(function() {{
    window.__AG_RTL_DISABLED__ = false;
    const rtlCSS = `{clean_css}`;

    function applyRTL() {{
        try {{
            if (typeof electron_1 !== 'undefined' && electron_1.webFrame && electron_1.webFrame.insertCSS) {{
                electron_1.webFrame.insertCSS(rtlCSS);
            }}
        }} catch(e) {{}}

        function injectTag() {{
            if (!document.head) {{
                setTimeout(injectTag, 20);
                return;
            }}
            let s = document.getElementById('antigravity-chat-rtl-style');
            if (!s) {{
                s = document.createElement('style');
                s.id = 'antigravity-chat-rtl-style';
                document.head.appendChild(s);
            }}
            s.textContent = rtlCSS;
        }}

        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', injectTag);
        }} else {{
            injectTag();
        }}
    }}

    applyRTL();

    // --- Settings & Appearance Subsystem ---
    const STORAGE_KEY = 'antigravity_appearance_settings';
    const DEFAULT_SETTINGS = {{
        rtlEnabled: true,
        fontFamily: 'Vazirmatn',
        customFont: '',
        fontSize: 15,
        lineHeight: 1.75
    }};

    function getSettings() {{
        try {{
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) return Object.assign({{}}, DEFAULT_SETTINGS, JSON.parse(raw));
        }} catch(e) {{}}
        return Object.assign({{}}, DEFAULT_SETTINGS);
    }}

    function saveSettings(s) {{
        try {{
            localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
        }} catch(e) {{}}
    }}

    let currentSettings = getSettings();

    function getFontFamilyValue(fontName, customName) {{
        switch(fontName) {{
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
                return (customName ? `'${{customName}}', ` : "") + "'Vazirmatn', sans-serif";
            case 'Vazirmatn':
            default:
                return "'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        }}
    }}

    function applySettings(s) {{
        if (!document.documentElement) return;
        const root = document.documentElement;
        root.style.setProperty('--ag-font-size', s.fontSize + 'px');
        root.style.setProperty('--ag-line-height', s.lineHeight.toString());
        root.style.setProperty('--ag-font-family', getFontFamilyValue(s.fontFamily, s.customFont));

        if (!document.body) return;
        if (s.rtlEnabled) {{
            document.body.classList.remove('ag-rtl-disabled');
            processAllSmartRTL(document.body);
        }} else {{
            document.body.classList.add('ag-rtl-disabled');
        }}
    }}

    // --- Smart Direction Subsystem ---
    function detectSmartDirection(text, fallbackDir) {{
        if (!text) return null;
        const trimmed = text.trim();
        if (!trimmed) return null;

        const hasPersian = /[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(trimmed);
        const hasLatin = /[a-zA-Z]/.test(trimmed);

        if (hasPersian && !hasLatin) return 'rtl';
        if (!hasPersian && !hasLatin) return fallbackDir !== undefined ? fallbackDir : 'rtl';
        if (!hasPersian && hasLatin) return 'ltr';

        let s = trimmed.replace(/^[\s\d٠-٩۰-۹*#\-_+–—•.:,;!?/\|~<>]+/, '');
        s = s.replace(/^\[[ xX]\]\s*/, '');

        const tagMatch = s.match(/^(\([^\)]+\)|\[[^\]]+\]|`[^`]+`|[a-zA-Z0-9_.\-]+\.(?:zip|bat|py|js|ts|css|json|txt|md|exe|sh|html)\s*:?)\s*/);
        if (tagMatch) {{
            const afterTag = s.slice(tagMatch[0].length).trim();
            if (/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(afterTag)) {{
                return 'rtl';
            }}
        }}

        const letterMatch = s.match(/[\p{{L}}]/u);
        if (letterMatch) {{
            const char = letterMatch[0];
            if (/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/.test(char)) return 'rtl';
            if (/[a-zA-Z]/.test(char)) {{
                const persianCount = (s.match(/[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/g) || []).length;
                const latinCount = (s.match(/[a-zA-Z]/g) || []).length;
                if (persianCount > latinCount * 1.1) return 'rtl';
                return 'ltr';
            }}
            if (/[\p{{sc=Arabic}}\p{{sc=Hebrew}}\p{{sc=Syriac}}\p{{sc=Thaana}}]/u.test(char)) return 'rtl';
        }}
        return 'rtl';
    }}

    function applySmartDirectionToElement(el) {{
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        if (!el || el.nodeType !== 1) return;
        if (el.matches('pre, pre *, .monaco-editor, .monaco-editor *, .terminal, .terminal-wrapper, [data-testid*="tool"], [data-testid*="collapsible"], button.review-button, button.review-button *, .files-changed-header, .files-changed-header *')) return;

        if (el.tagName === 'CODE') {{
            if (/[؀-ۿ]/.test(el.textContent || '')) el.setAttribute('dir', 'rtl');
            else el.setAttribute('dir', 'ltr');
            return;
        }}

        if (el.classList && el.classList.contains('artifact-card')) {{
            const desc = el.querySelector('.text-secondary-foreground, span.line-clamp-3');
            if (desc) {{
                const dir = detectSmartDirection(desc.textContent || '');
                if (dir) desc.setAttribute('dir', dir);
            }}
            return;
        }}

        if ((el.classList && el.classList.contains('line-clamp-3')) || (el.classList && el.classList.contains('text-secondary-foreground'))) {{
            if (el.closest('.artifact-card')) {{
                const dir = detectSmartDirection(el.textContent || '');
                if (dir) el.setAttribute('dir', dir);
                return;
            }}
        }}

        if (el.tagName === 'TABLE') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) {{
                el.setAttribute('dir', dir);
                const cells = el.querySelectorAll('th, td');
                for (let i = 0; i < cells.length; i++) {{
                    const cellDir = detectSmartDirection(cells[i].textContent || '', dir);
                    if (cellDir) cells[i].setAttribute('dir', cellDir);
                }}
            }}
            return;
        }}

        if (el.tagName === 'LI') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) {{
                el.setAttribute('dir', dir);
                const parentList = el.parentElement;
                if (parentList && (parentList.tagName === 'UL' || parentList.tagName === 'OL')) {{
                    if (!parentList.getAttribute('dir')) parentList.setAttribute('dir', dir);
                }}
            }}
            return;
        }}

        if (el.tagName === 'UL' || el.tagName === 'OL') {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (/^(H[1-6]|P|BLOCKQUOTE)$/.test(el.tagName)) {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (el.classList && el.classList.contains('whitespace-pre-wrap') && el.closest('[data-testid="user-input-step"]')) {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
            return;
        }}

        if (el.classList && el.classList.contains('leading-relaxed')) {{
            const dir = detectSmartDirection(el.textContent || '');
            if (dir) el.setAttribute('dir', dir);
        }}
    }}

    function processAllSmartRTL(root) {{
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        const base = root || document.body;
        if (!base) return;
        applySmartDirectionToElement(base);
        const selector = 'p, h1, h2, h3, h4, h5, h6, li, ul, ol, blockquote, table, .artifact-card, span.line-clamp-3, [data-testid="user-input-step"] .whitespace-pre-wrap, .leading-relaxed';
        try {{
            const elements = base.querySelectorAll(selector);
            for (let i = 0; i < elements.length; i++) {{
                applySmartDirectionToElement(elements[i]);
            }}
        }} catch(e) {{}}
    }}

    // --- Menubar Button & Settings Popover ---
    let popoverInstance = null;

    function initAppearanceMenu() {{
        if (window.__AG_RTL_DISABLED__) {{
            const c = document.getElementById('ag-appearance-menu-container');
            if (c) c.remove();
            return;
        }}
        const bar = document.querySelector('[data-testid="title-menu-bar"]');
        if (!bar) return;

        let container = document.getElementById('ag-appearance-menu-container');
        if (!container) {{
            container = document.createElement('div');
            container.id = 'ag-appearance-menu-container';
            container.className = 'relative';
            container.style.appRegion = 'no-drag';
            bar.appendChild(container);
        }}

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

        function closePopover() {{
            if (popoverInstance) {{
                popoverInstance.remove();
                popoverInstance = null;
                btn.classList.remove('bg-secondary', 'text-foreground');
            }}
        }}

        function openPopover() {{
            if (popoverInstance) {{
                closePopover();
                return;
            }}

            btn.classList.add('bg-secondary', 'text-foreground');
            const rect = btn.getBoundingClientRect();

            popoverInstance = document.createElement('div');
            popoverInstance.id = 'ag-appearance-popover';
            popoverInstance.style.cssText = `
                position: fixed;
                top: ${{rect.bottom + 4}}px;
                left: ${{Math.min(rect.left, window.innerWidth - 330)}}px;
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
            `;

            popoverInstance.innerHTML = `
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
                    <div id="ag-toggle-rtl" style="width: 44px; height: 24px; background: ${{currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46'}}; border-radius: 12px; position: relative; cursor: pointer; transition: background .2s;">
                        <div id="ag-toggle-knob" style="position: absolute; width: 18px; height: 18px; background: white; border-radius: 50%; top: 3px; right: ${{currentSettings.rtlEnabled ? '4px' : '22px'}}; transition: right .2s;"></div>
                    </div>
                </div>

                <!-- Font Family Selection -->
                <div style="margin-bottom: 12px;">
                    <label style="display: block; font-size: 12px; font-weight: 500; color: #d4d4d8; margin-bottom: 6px;">قلم فارسی (Font Family):</label>
                    <select id="ag-font-family-select" style="width: 100%; background: #27272a; color: #f4f4f5; border: 1px solid rgba(255,255,255,0.14); border-radius: 6px; padding: 6px 10px; font-size: 12.5px; outline: none; font-family: inherit; cursor: pointer;">
                        <option value="Vazirmatn" ${{currentSettings.fontFamily === 'Vazirmatn' ? 'selected' : ''}}>وزیرمتن (Vazirmatn - پیش‌فرض)</option>
                        <option value="Shabnam" ${{currentSettings.fontFamily === 'Shabnam' ? 'selected' : ''}}>شبنم (Shabnam)</option>
                        <option value="Sahel" ${{currentSettings.fontFamily === 'Sahel' ? 'selected' : ''}}>ساحل (Sahel)</option>
                        <option value="Samim" ${{currentSettings.fontFamily === 'Samim' ? 'selected' : ''}}>صمیم (Samim)</option>
                        <option value="Tahoma" ${{currentSettings.fontFamily === 'Tahoma' ? 'selected' : ''}}>تاهما (Tahoma)</option>
                        <option value="System" ${{currentSettings.fontFamily === 'System' ? 'selected' : ''}}>فونت سیستم (System Font)</option>
                        <option value="Custom" ${{currentSettings.fontFamily === 'Custom' ? 'selected' : ''}}>فونت دلخواه (سفارشی)...</option>
                    </select>
                    <div id="ag-custom-font-container" style="display: ${{currentSettings.fontFamily === 'Custom' ? 'block' : 'none'}}; margin-top: 6px;">
                        <input type="text" id="ag-custom-font-input" placeholder="نام فونت (مثلاً: B Yekan, Dana)" value="${{currentSettings.customFont || ''}}" style="width: 100%; background: #202023; color: #fff; border: 1px solid rgba(59,130,246,0.5); border-radius: 6px; padding: 5px 8px; font-size: 12px; outline: none; box-sizing: border-box;">
                    </div>
                </div>

                <!-- Font Size Stepper & Slider -->
                <div style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 12px; font-weight: 500; color: #d4d4d8;">اندازه متن چت (Font Size):</span>
                        <span id="ag-font-size-badge" style="font-size: 12px; font-weight: 600; color: #60a5fa; background: rgba(59, 130, 246, 0.15); padding: 1px 8px; border-radius: 4px; direction: ltr;">${{currentSettings.fontSize}}px</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; direction: ltr;">
                        <button id="ag-font-dec" style="width: 32px; height: 28px; background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 600;">-</button>
                        <input type="range" id="ag-font-size-slider" min="12" max="22" value="${{currentSettings.fontSize}}" step="1" style="flex: 1; accent-color: #3b82f6; cursor: pointer;">
                        <button id="ag-font-inc" style="width: 32px; height: 28px; background: #27272a; border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 600;">+</button>
                    </div>
                </div>

                <!-- Line Height -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 12px; font-weight: 500; color: #d4d4d8;">فاصله خطوط (Line Height):</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px;">
                        <button class="ag-lh-btn" data-lh="1.5" style="background: ${{currentSettings.lineHeight === 1.5 ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.lineHeight === 1.5 ? '#3b82f6' : 'rgba(255,255,255,0.1)'}}; color: ${{currentSettings.lineHeight === 1.5 ? '#fff' : '#a1a1aa'}}; border-radius: 6px; padding: 4px 0; font-size: 11.5px; cursor: pointer; font-family: inherit;">فشرده</button>
                        <button class="ag-lh-btn" data-lh="1.75" style="background: ${{currentSettings.lineHeight === 1.75 ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.lineHeight === 1.75 ? '#3b82f6' : 'rgba(255,255,255,0.1)'}}; color: ${{currentSettings.lineHeight === 1.75 ? '#fff' : '#a1a1aa'}}; border-radius: 6px; padding: 4px 0; font-size: 11.5px; font-weight: 500; cursor: pointer; font-family: inherit;">معمولی</button>
                        <button class="ag-lh-btn" data-lh="2.0" style="background: ${{currentSettings.lineHeight === 2.0 ? '#3b82f6' : '#27272a'}}; border: 1px solid ${{currentSettings.lineHeight === 2.0 ? '#3b82f6' : 'rgba(255,255,255,0.1)'}}; color: ${{currentSettings.lineHeight === 2.0 ? '#fff' : '#a1a1aa'}}; border-radius: 6px; padding: 4px 0; font-size: 11.5px; cursor: pointer; font-family: inherit;">باز</button>
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
            `;

            document.body.appendChild(popoverInstance);

            const toggleBtn = popoverInstance.querySelector('#ag-toggle-rtl');
            const knob = popoverInstance.querySelector('#ag-toggle-knob');
            toggleBtn.onclick = () => {{
                currentSettings.rtlEnabled = !currentSettings.rtlEnabled;
                toggleBtn.style.background = currentSettings.rtlEnabled ? '#3b82f6' : '#3f3f46';
                knob.style.right = currentSettings.rtlEnabled ? '4px' : '22px';
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const fontSelect = popoverInstance.querySelector('#ag-font-family-select');
            const customContainer = popoverInstance.querySelector('#ag-custom-font-container');
            const customInput = popoverInstance.querySelector('#ag-custom-font-input');
            fontSelect.onchange = () => {{
                currentSettings.fontFamily = fontSelect.value;
                if (fontSelect.value === 'Custom') {{
                    customContainer.style.display = 'block';
                    customInput.focus();
                }} else {{
                    customContainer.style.display = 'none';
                }}
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            customInput.oninput = () => {{
                currentSettings.customFont = customInput.value.trim();
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }};

            const sizeSlider = popoverInstance.querySelector('#ag-font-size-slider');
            const sizeBadge = popoverInstance.querySelector('#ag-font-size-badge');
            const decBtn = popoverInstance.querySelector('#ag-font-dec');
            const incBtn = popoverInstance.querySelector('#ag-font-inc');

            function updateFontSize(val) {{
                val = Math.max(12, Math.min(22, parseInt(val) || 15));
                currentSettings.fontSize = val;
                sizeSlider.value = val;
                sizeBadge.textContent = val + 'px';
                applySettings(currentSettings);
                saveSettings(currentSettings);
            }}

            sizeSlider.oninput = () => updateFontSize(sizeSlider.value);
            decBtn.onclick = () => updateFontSize(currentSettings.fontSize - 1);
            incBtn.onclick = () => updateFontSize(currentSettings.fontSize + 1);

            const lhButtons = popoverInstance.querySelectorAll('.ag-lh-btn');
            lhButtons.forEach(b => {{
                b.onclick = () => {{
                    const lh = parseFloat(b.getAttribute('data-lh'));
                    currentSettings.lineHeight = lh;
                    lhButtons.forEach(btnEl => {{
                        const active = parseFloat(btnEl.getAttribute('data-lh')) === lh;
                        btnEl.style.background = active ? '#3b82f6' : '#27272a';
                        btnEl.style.borderColor = active ? '#3b82f6' : 'rgba(255,255,255,0.1)';
                        btnEl.style.color = active ? '#fff' : '#a1a1aa';
                    }});
                    applySettings(currentSettings);
                    saveSettings(currentSettings);
                }};
            }});

            popoverInstance.querySelector('#ag-reset-defaults').onclick = () => {{
                currentSettings = Object.assign({{}}, DEFAULT_SETTINGS);
                applySettings(currentSettings);
                saveSettings(currentSettings);
                closePopover();
                openPopover();
            }};

            popoverInstance.querySelector('#ag-close-popover').onclick = closePopover;
        }}

        btn.onclick = (e) => {{
            e.stopPropagation();
            if (popoverInstance) closePopover();
            else openPopover();
        }};

        document.addEventListener('pointerdown', (e) => {{
            if (!popoverInstance) return;
            if (popoverInstance.contains(e.target) || container.contains(e.target)) return;
            closePopover();
        }});

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape' && popoverInstance) closePopover();
        }});
    }}

    function initAll() {{
        const override = document.getElementById('ag-rtl-disable-override');
        if (override) override.remove();
        applySettings(currentSettings);
        initAppearanceMenu();
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initAll);
    }} else {{
        initAll();
    }}

    if (window.__ag_appearance_interval__) {{
        clearInterval(window.__ag_appearance_interval__);
    }}
    window.__ag_appearance_interval__ = setInterval(initAppearanceMenu, 800);

    // --- Dynamic Observer for Chat Messages ---
    let scheduled = false;
    const pendingNodes = new Set();
    const flushPending = () => {{
        scheduled = false;
        const nodes = Array.from(pendingNodes);
        pendingNodes.clear();
        for (let i = 0; i < nodes.length; i++) {{
            const node = nodes[i];
            if (node && node.nodeType === 1) {{
                applySmartDirectionToElement(node);
                processAllSmartRTL(node);
            }}
        }}
    }};

    const observer = new MutationObserver((mutations) => {{
        if (document.body && document.body.classList.contains('ag-rtl-disabled')) return;
        for (let i = 0; i < mutations.length; i++) {{
            const mut = mutations[i];
            if (mut.type === 'childList') {{
                for (let j = 0; j < mut.addedNodes.length; j++) {{
                    const n = mut.addedNodes[j];
                    if (n && n.nodeType === 1) pendingNodes.add(n);
                }}
            }} else if (mut.type === 'characterData') {{
                const p = mut.target.parentElement;
                if (p && p.nodeType === 1) pendingNodes.add(p);
            }}
        }}
        if (!scheduled && pendingNodes.size > 0) {{
            scheduled = true;
            requestAnimationFrame(flushPending);
        }}
    }});

    function startObserver() {{
        if (document.body) {{
            observer.observe(document.body, {{ childList: true, subtree: true, characterData: true }});
            processAllSmartRTL(document.body);
        }} else {{
            setTimeout(startObserver, 50);
        }}
    }}

    startObserver();
}})();
}} catch(e) {{
    console.error("[Antigravity-RTL] Injection error:", e);
}}
"""

def setup_shortcuts(antigravity_dir, launcher_path):
    dest_launcher = os.path.join(antigravity_dir, "AntigravityLauncher.exe")
    try:
        shutil.copy2(launcher_path, dest_launcher)
        target_exe = dest_launcher
    except Exception:
        target_exe = launcher_path

    icon_source = os.path.join(antigravity_dir, "Antigravity.exe")
    ps_code = f"""
    $wsh = New-Object -ComObject WScript.Shell
    $paths = @(
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonDesktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonStartMenu'), 'Programs', 'Antigravity.lnk')
    )
    $found = $false
    foreach ($p in $paths) {{
        if (Test-Path $p) {{
            $sc = $wsh.CreateShortcut($p)
            $sc.TargetPath = '{target_exe}'
            $sc.IconLocation = '{icon_source},0'
            $sc.WorkingDirectory = '{antigravity_dir}'
            $sc.Save()
            $found = $true
        }}
    }}
    if (-not $found) {{
        $desktopP = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk')
        $sc = $wsh.CreateShortcut($desktopP)
        $sc.TargetPath = '{target_exe}'
        $sc.IconLocation = '{icon_source},0'
        $sc.WorkingDirectory = '{antigravity_dir}'
        $sc.Save()
    }}
    """
    try:
        subprocess.run(['powershell', '-NoProfile', '-Command', ps_code], capture_output=True)
        print("  [OK] Auto-Shield launcher installed & shortcuts protected.")
    except Exception:
        pass

def restore_shortcuts(antigravity_dir):
    real_exe = os.path.join(antigravity_dir, "Antigravity.exe")
    ps_code = f"""
    $wsh = New-Object -ComObject WScript.Shell
    $paths = @(
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonDesktop'), 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('StartMenu'), 'Programs', 'Antigravity.lnk'),
        [System.IO.Path]::Combine([System.Environment]::GetFolderPath('CommonStartMenu'), 'Programs', 'Antigravity.lnk')
    )
    foreach ($p in $paths) {{
        if (Test-Path $p) {{
            $sc = $wsh.CreateShortcut($p)
            $sc.TargetPath = '{real_exe}'
            $sc.IconLocation = '{real_exe},0'
            $sc.WorkingDirectory = '{antigravity_dir}'
            $sc.Save()
        }}
    }}
    """
    try:
        subprocess.run(['powershell', '-NoProfile', '-Command', ps_code], capture_output=True)
        print("  [OK] Desktop shortcuts restored to original Antigravity.exe.")
    except Exception:
        pass

def deploy_permanent_engine(antigravity_dir):
    """
    Deploys the patch engine permanently to Antigravity directories so it survives updates:
    1. %APPDATA%\\Antigravity\\rtl-patch
    2. %LOCALAPPDATA%\\Programs\\antigravity\\resources\\rtl-patch
    3. %LOCALAPPDATA%\\Programs\\antigravity\\AntigravityLauncher.exe
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir) if os.path.basename(script_dir).lower() == "src" else script_dir
    src_dir = os.path.join(root_dir, "src") if os.path.isdir(os.path.join(root_dir, "src")) else root_dir

    files_to_copy = [
        (os.path.join(src_dir, "patcher.py"), "patcher.py"),
        (os.path.join(src_dir, "patcher.js"), "patcher.js"),
        (os.path.join(src_dir, "antigravity-chat-rtl.css"), "antigravity-chat-rtl.css"),
        (os.path.join(root_dir, "patch.bat"), "patch.bat")
    ]

    target_dirs = [
        os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch"),
        os.path.join(antigravity_dir, "resources", "rtl-patch")
    ]

    for tdir in target_dirs:
        try:
            os.makedirs(tdir, exist_ok=True)
            for src_f, fname in files_to_copy:
                if os.path.isfile(src_f):
                    shutil.copy2(src_f, os.path.join(tdir, fname))
        except Exception:
            pass

    # Copy and setup Launcher
    launcher_src = os.path.join(src_dir, "AntigravityLauncher.exe")
    if not os.path.isfile(launcher_src):
        launcher_src = os.path.join(root_dir, "AntigravityLauncher.exe")
    
    if os.path.isfile(launcher_src):
        setup_shortcuts(antigravity_dir, launcher_src)

def do_patch(antigravity_dir, interactive=False, kill=False):
    resources_dir = os.path.join(antigravity_dir, "resources")
    asar_path = os.path.join(resources_dir, "app.asar")
    backup_path = os.path.join(resources_dir, "app.asar.original_backup")
    temp_asar = os.path.join(resources_dir, "app.asar.patching.tmp")

    if not os.path.isfile(asar_path):
        print(f"[-] خطا: فایل app.asar در مسیر {asar_path} یافت نشد.")
        return False

    # Close Antigravity only if explicitly requested
    if kill and is_antigravity_running():
        close_antigravity()

    # 1. Inspect metadata and backup original app.asar
    asar_meta = get_asar_metadata(asar_path)
    backup_meta = get_asar_metadata(backup_path) if os.path.isfile(backup_path) else None

    # Detect if app.asar is a fresh official release (unpatched and newer than or equal to backup)
    is_official_update = False
    if asar_meta and not asar_meta["is_patched"]:
        if not backup_meta:
            is_official_update = True
        elif asar_meta["version_tuple"] > backup_meta["version_tuple"]:
            is_official_update = True
        elif asar_meta["version_tuple"] == backup_meta["version_tuple"] and asar_meta["mtime"] > backup_meta["mtime"]:
            is_official_update = True
        elif asar_meta["mtime"] > backup_meta["mtime"]:
            is_official_update = True

    if is_official_update or not os.path.isfile(backup_path):
        ver_info = f" (v{asar_meta['version_str']})" if asar_meta else ""
        print(f"[*] Updating factory backup with official pristine build{ver_info}...")
        try:
            shutil.copy2(asar_path, backup_path)
            print(f"  [✓] پشتیبان کارخانه با موفقیت ذخیره شد:\n      {backup_path}")
        except Exception as e:
            print(f"[-] خطا در ایجاد فایل پشتیبان: {e}")
            return False
        source_asar = asar_path
    else:
        print(f"  [i] نسخه پشتیبان اصلی کارخانه موجود است.")
        if backup_meta and asar_meta and backup_meta["version_tuple"] >= asar_meta["version_tuple"]:
            source_asar = backup_path
        elif os.path.isfile(backup_path):
            source_asar = backup_path
        else:
            source_asar = asar_path

    # 2. Extract preload and updater
    preload_code = extract_file_from_asar(source_asar, "dist/preload.js")
    updater_code = extract_file_from_asar(source_asar, "dist/updater.js")
    nsis_code = extract_file_from_asar(source_asar, "node_modules/electron-updater/out/NsisUpdater.js")
    base_code = extract_file_from_asar(source_asar, "node_modules/electron-updater/out/BaseUpdater.js")

    if not preload_code:
        print("[-] خطا در استخراج dist/preload.js از آرشیو.")
        return False

    injection_snippet = get_injection_snippet()

    if "/* __ANTIGRAVITY_RTL_INJECTED__ */" in preload_code:
        preload_code = preload_code.split("/* __ANTIGRAVITY_RTL_INJECTED__ */")[0]

    patched_preload = preload_code + "\n" + injection_snippet
    replacements = {"dist/preload.js": patched_preload}

    # Hook updater files to automatically re-patch after future updates
    hook_body = """
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
"""

    if updater_code and "function quitAndInstall() {" in updater_code:
        replacements["dist/updater.js"] = updater_code.replace(
            "function quitAndInstall() {",
            "function quitAndInstall() {" + hook_body
        )

    if nsis_code and "doInstall(options) {" in nsis_code:
        replacements["node_modules/electron-updater/out/NsisUpdater.js"] = nsis_code.replace(
            "doInstall(options) {",
            "doInstall(options) {" + hook_body
        )

    if base_code and "install(isSilent = false, isForceRunAfter = false) {" in base_code:
        replacements["node_modules/electron-updater/out/BaseUpdater.js"] = base_code.replace(
            "install(isSilent = false, isForceRunAfter = false) {",
            "install(isSilent = false, isForceRunAfter = false) {" + hook_body
        )

    print("\n[*] در حال بازسازی و جایگذاری پکیج برنامه (app.asar)...")
    try:
        patch_asar(source_asar, temp_asar, replacements)
        try:
            shutil.move(temp_asar, asar_path)
        except Exception:
            with open(temp_asar, "rb") as tf:
                data = tf.read()
            with open(asar_path, "r+b") as out:
                out.seek(0)
                out.write(data)
                out.truncate()
            if os.path.exists(temp_asar):
                os.remove(temp_asar)

        # Deploy permanent engine and Auto-Shield
        deploy_permanent_engine(antigravity_dir)

        print("\n" + "=" * 68)
        print("[OK] Smart RTL & Permanent Auto-Shield Successfully Installed!")
        print("=" * 68)
        print("  * Intelligent auto-direction (Persian: RTL | English: LTR)")
        print("  * Modern typography & Appearance menu integrated into top bar")
        print("  * Engine deployed permanently to Antigravity directory")
        print("  * Auto-Shield active: Automatically re-patches on official updates")
        print("=" * 68)

        if is_antigravity_running():
            live_ok = try_sync_live_window("apply")
            if live_ok:
                print("  [OK] Changes synchronized live into open Antigravity window.")
            else:
                print("  [!] Restart Antigravity to reflect changes in current window.")

        return True
    except Exception as e:
        print(f"[-] Patch error: {e}")
        if os.path.exists(temp_asar):
            try:
                os.remove(temp_asar)
            except Exception:
                pass
        return False

def try_sync_live_window(action="restore"):
    """
    Synchronizes the live open window without restarting Antigravity.
    """
    try:
        appdata = os.environ.get("APPDATA", "")
        port_file = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
        if not os.path.isfile(port_file):
            return False

        with open(port_file, "r", encoding="utf-8") as f:
            port = f.readline().strip()

        import urllib.request
        import json

        req = urllib.request.Request(f"http://127.0.0.1:{port}/json")
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            targets = json.loads(resp.read().decode("utf-8"))

        pages = [p for p in targets if p.get("type") == "page" and "webSocketDebuggerUrl" in p]
        if not pages:
            return False

        if action == "restore":
            js_code = """(() => {
                window.__AG_RTL_DISABLED__ = true;
                if (window.__ag_appearance_interval__) {
                    clearInterval(window.__ag_appearance_interval__);
                    window.__ag_appearance_interval__ = null;
                }
                let override = document.getElementById('ag-rtl-disable-override');
                if (!override) {
                    override = document.createElement('style');
                    override.id = 'ag-rtl-disable-override';
                    document.head.appendChild(override);
                }
                override.textContent = `
                    #ag-appearance-menu-container,
                    #ag-appearance-menu-btn,
                    #ag-appearance-popover {
                        display: none !important;
                        visibility: hidden !important;
                        pointer-events: none !important;
                    }
                `;
                const c = document.getElementById('ag-appearance-menu-container');
                if (c) c.remove();
                const btn = document.getElementById('ag-appearance-menu-btn');
                if (btn) btn.remove();
                const pop = document.getElementById('ag-appearance-popover');
                if (pop) pop.remove();
                const style = document.getElementById('antigravity-chat-rtl-style');
                if (style) style.remove();
                document.documentElement.classList.remove('ag-rtl-enabled');
                document.documentElement.classList.add('ag-rtl-disabled');
                document.querySelectorAll('[dir="rtl"]').forEach(el => el.removeAttribute('dir'));
                return true;
            })()"""
        else:
            js_code = get_injection_snippet()

        try:
            import asyncio
            import websockets

            async def eval_page(ws_url, code):
                async with websockets.connect(ws_url, max_size=None) as ws:
                    msg = {
                        "id": 1,
                        "method": "Runtime.evaluate",
                        "params": {"expression": code, "returnByValue": True}
                    }
                    await ws.send(json.dumps(msg))
                    await ws.recv()

            for page in pages:
                asyncio.run(eval_page(page["webSocketDebuggerUrl"], js_code))
            return True
        except Exception:
            return False
    except Exception:
        return False

def do_restore(antigravity_dir, kill=False):
    resources_dir = os.path.join(antigravity_dir, "resources")
    asar_path = os.path.join(resources_dir, "app.asar")
    backup_path = os.path.join(resources_dir, "app.asar.original_backup")

    # Fallback to alternate backup name if original_backup wasn't found
    if not os.path.isfile(backup_path):
        alt_backup = os.path.join(resources_dir, "app.asar.backup")
        if os.path.isfile(alt_backup):
            backup_path = alt_backup

    if not os.path.isfile(backup_path):
        print(f"[-] Backup file not found: {backup_path}")
        return False

    asar_meta = get_asar_metadata(asar_path) if os.path.isfile(asar_path) else None
    backup_meta = get_asar_metadata(backup_path)

    # Prevent restoring over a newer unpatched official release
    if asar_meta and not asar_meta["is_patched"]:
        print("[i] app.asar is already clean and unpatched. No restoration needed.")
        restore_shortcuts(antigravity_dir)
        try:
            launcher_exe = os.path.join(antigravity_dir, "AntigravityLauncher.exe")
            if os.path.isfile(launcher_exe):
                os.remove(launcher_exe)
            res_patch = os.path.join(antigravity_dir, "resources", "rtl-patch")
            if os.path.isdir(res_patch):
                shutil.rmtree(res_patch, ignore_errors=True)
            appdata_patch = os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch")
            if os.path.isdir(appdata_patch):
                shutil.rmtree(appdata_patch, ignore_errors=True)
        except Exception:
            pass
        return True

    # Prevent silent downgrade if backup is older than current app.asar
    if asar_meta and backup_meta:
        if backup_meta["version_tuple"] < asar_meta["version_tuple"]:
            print(f"[-] ERROR: Restoration aborted to prevent silent application downgrade!")
            print(f"    Current application: v{asar_meta['version_str']}")
            print(f"    Outdated backup:     v{backup_meta['version_str']}")
            return False

    if kill and is_antigravity_running():
        close_antigravity()

    print("[*] Restoring app.asar from factory backup...")
    try:
        try:
            shutil.copy2(backup_path, asar_path)
        except Exception:
            with open(backup_path, "rb") as bf:
                data = bf.read()
            with open(asar_path, "r+b") as out:
                out.seek(0)
                out.write(data)
                out.truncate()

        print("\n" + "=" * 65)
        print("[OK] Successfully restored to 100% factory original state.")
        print("=" * 65)

        # Restore shortcuts if modified
        restore_shortcuts(antigravity_dir)

        # Remove launcher and permanent patch directories
        try:
            launcher_exe = os.path.join(antigravity_dir, "AntigravityLauncher.exe")
            if os.path.isfile(launcher_exe):
                os.remove(launcher_exe)
            res_patch = os.path.join(antigravity_dir, "resources", "rtl-patch")
            if os.path.isdir(res_patch):
                shutil.rmtree(res_patch, ignore_errors=True)
            appdata_patch = os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch")
            if os.path.isdir(appdata_patch):
                shutil.rmtree(appdata_patch, ignore_errors=True)
        except Exception:
            pass

        if is_antigravity_running():
            live_ok = try_sync_live_window("restore")
            if live_ok:
                print("  [OK] Changes synchronized live into open Antigravity window.")
            else:
                print("  [!] Restart Antigravity to reflect changes in current window.")
        return True
    except Exception as e:
        print(f"[-] Restore error: {e}")
        return False

def wait_for_update_then_patch(antigravity_dir):
    asar_path = os.path.join(antigravity_dir, "resources", "app.asar")
    init_mtime = os.path.getmtime(asar_path) if os.path.isfile(asar_path) else 0

    # 1. Wait for installer.exe / update processes or asar modification (up to 90 seconds)
    for _ in range(45):
        time.sleep(2)
        try:
            res = subprocess.run(['tasklist'], capture_output=True, text=True)
            out = res.stdout.lower()
            if 'installer.exe' in out or 'setup.exe' in out:
                for _ in range(60):
                    time.sleep(2)
                    res2 = subprocess.run(['tasklist'], capture_output=True, text=True)
                    if 'installer.exe' not in res2.stdout.lower() and 'setup.exe' not in res2.stdout.lower():
                        break
                break
            if os.path.isfile(asar_path):
                curr_mtime = os.path.getmtime(asar_path)
                if curr_mtime != init_mtime:
                    break
        except Exception:
            pass

    # Wait for file writes to flush
    time.sleep(3)

    # Patch new version in-place without killing
    do_patch(antigravity_dir, interactive=False, kill=False)

def launch_antigravity(antigravity_dir):
    exe_path = os.path.join(antigravity_dir, "Antigravity.exe")
    if os.path.isfile(exe_path):
        print(f"[*] Launching Antigravity IDE...")
        try:
            subprocess.Popen([exe_path], cwd=antigravity_dir, close_fds=True)
        except Exception as e:
            print(f"[-] Failed to launch Antigravity: {e}")

def interactive_menu(target_dir):
    while True:
        clear_screen()
        print_banner()

        is_patched, is_running = get_system_status(target_dir)

        if is_patched:
            status_pill = "\033[42;30;1m ACTIVE \033[0m   Patch Status  : \033[92;1mPatched & Live-Enabled\033[0m"
        else:
            status_pill = "\033[43;30;1m FACTORY \033[0m  Patch Status  : \033[93;1mOriginal Untouched app.asar\033[0m"

        if is_running:
            proc_pill = "\033[46;30;1m ONLINE \033[0m   Process State : \033[96;1mRunning (CDP Live Sync Ready)\033[0m"
        else:
            proc_pill = "\033[100;37;1m CLOSED \033[0m   Process State : \033[90mOffline (Changes apply on start)\033[0m"

        short_dir = target_dir if len(target_dir) <= 40 else "..." + target_dir[-37:]
        path_pill = f"\033[44;97;1m TARGET \033[0m   Install Path  : \033[90m{short_dir}\033[0m"

        status_lines = [status_pill, proc_pill, path_pill]

        shield_ok = os.path.isfile(os.path.join(target_dir, "AntigravityLauncher.exe"))
        patch_dir_ok = os.path.isdir(os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "rtl-patch"))

        action_lines = [
            f"\033[42;30;1m 1 \033[0m  \033[97;1mInstall Permanent RTL & Auto-Shield\033[0m  \033[96m>> [PERMANENT SHIELD]\033[0m",
            f"\033[43;30;1m 2 \033[0m  \033[97;1mRestore 100% Factory Original\033[0m        \033[93m<< [FACTORY REVERT]\033[0m",
            f"\033[44;97;1m 3 \033[0m  \033[97;1mSystem Diagnostics & Health Check\033[0m    \033[94m== [HEALTH CHECK]\033[0m",
            f"\033[41;97;1m 0 \033[0m  \033[97;1mExit Patcher\033[0m                         \033[90m-- [EXIT]\033[0m"
        ]

        print(render_shadow_card("SYSTEM TELEMETRY", status_lines, width=74, border_color="\033[38;2;0;242;254m"))
        print()
        print(render_shadow_card("COMMAND CENTER", action_lines, width=74, border_color="\033[38;2;79;110;247m"))
        print()

        try:
            choice = input(f"  \033[38;2;0;242;254m-->\033[0m {CLR_WHITE}Select action [1, 2, 3, 0] (Default: 1 - Permanent Install): {CLR_RESET}").strip().replace('\ufeff', '')
            for p_digit, e_digit in [('۰','0'), ('۱','1'), ('۲','2'), ('۳','3'), ('۴','4'), ('۵','5'), ('۶','6')]:
                choice = choice.replace(p_digit, e_digit)
            if not choice:
                choice = "1"
        except (KeyboardInterrupt, EOFError):
            print(f"\n{CLR_GREEN}Exiting.{CLR_RESET}")
            break

        def pause_menu():
            try:
                input(f"\n{CLR_DIM}Press Enter to return to main menu...{CLR_RESET}")
            except (KeyboardInterrupt, EOFError):
                pass

        if choice == "1":
            print(f"\n{CLR_CYAN}[*] Installing Permanent RTL & Auto-Shield on Antigravity...{CLR_RESET}")
            do_patch(target_dir, interactive=False, kill=False)
            pause_menu()
        elif choice == "2":
            print(f"\n{CLR_YELLOW}[*] Restoring 100% factory original state and removing shield...{CLR_RESET}")
            do_restore(target_dir, kill=False)
            pause_menu()
        elif choice == "3":
            backup = os.path.join(target_dir, "resources", "app.asar.original_backup")
            port_file = os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "DevToolsActivePort")
            short_p = target_dir if len(target_dir) <= 40 else "..." + target_dir[-37:]
            diag_lines = [
                f"\033[44;97;1m PATH \033[0m   Installation   : \033[37m{short_p}\033[0m",
                f"\033[42;30;1m ASAR \033[0m   Package State  : \033[92;1m{'Found & Valid' if os.path.isfile(os.path.join(target_dir, 'resources', 'app.asar')) else 'Not Found'}\033[0m",
                f"\033[46;30;1m BACK \033[0m   Factory Backup : \033[96;1m{'Healthy (app.asar.original_backup)' if os.path.isfile(backup) else 'Not Found'}\033[0m",
                f"\033[45;97;1m RTL  \033[0m   Patch Engine   : \033[95;1m{'ACTIVE (Patched)' if is_patched else 'INACTIVE (Original)'}\033[0m",
                f"\033[42;30;1m SHLD \033[0m   Auto-Shield    : \033[92;1m{'ACTIVE (Protected against updates)' if shield_ok and patch_dir_ok else 'INACTIVE'}\033[0m",
                f"\033[43;30;1m PROC \033[0m   Process State  : \033[93;1m{'RUNNING (Live Sync Available)' if is_running else 'CLOSED'}\033[0m",
                f"\033[47;30;1m SYNC \033[0m   DevTools CDP   : \033[97;1m{'Connected (Ready)' if os.path.isfile(port_file) else 'Inactive (restart Antigravity to enable)'}\033[0m"
            ]
            print()
            print(render_shadow_card("DIAGNOSTICS & SYSTEM HEALTH", diag_lines, width=74, border_color="\033[38;2;0;242;254m"))
            pause_menu()
        elif choice in ["0", "exit", "quit", "q"]:
            print(f"\n{CLR_GREEN}Goodbye!{CLR_RESET}\n")
            break
        else:
            print(f"{CLR_RED}Invalid choice.{CLR_RESET}")
            time.sleep(1)

def main():
    custom_path = None
    for i, arg in enumerate(sys.argv):
        if arg in ["--path", "-p"] and i + 1 < len(sys.argv):
            custom_path = sys.argv[i + 1]

    if "--wait-for-update" in sys.argv:
        target = find_antigravity_path(custom_path)
        if target:
            wait_for_update_then_patch(target)
        sys.exit(0)

    if "--check-only" in sys.argv:
        target = find_antigravity_path(custom_path)
        if target:
            asar = os.path.join(target, "resources", "app.asar")
            preload = extract_file_from_asar(asar, "dist/preload.js")
            is_patched = "__ANTIGRAVITY_RTL_INJECTED__" in (preload or "")
            print("1" if is_patched else "0")
        else:
            print("0")
        sys.exit(0)

    target_dir = find_antigravity_path(custom_path)
    if not target_dir:
        if sys.stdin.isatty():
            print_banner()
            print("[-] Antigravity installation path could not be detected automatically.")
            try:
                inp = input("Please enter Antigravity installation directory manually (or press Enter to exit): ").strip()
                if inp:
                    target_dir = find_antigravity_path(inp)
            except Exception:
                pass

    if not target_dir:
        print("[-] Error: Cannot proceed without a valid Antigravity installation path.")
        sys.exit(1)

    no_kill = "--no-kill" in sys.argv
    kill = ("--kill" in sys.argv) and not no_kill

    if any(x in sys.argv for x in ["2", "--restore", "-r"]):
        print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        do_restore(target_dir, kill=kill)
        if "--launch" in sys.argv:
            launch_antigravity(target_dir)
        return

    is_apply = any(x in sys.argv for x in ["1", "--apply", "-a", "--no-kill"])
    if is_apply or not sys.stdin.isatty():
        print_banner()
        print(f"[OK] Detected Antigravity path:\n     {target_dir}\n")
        success = do_patch(target_dir, interactive=False, kill=kill)
        if success and "--launch" in sys.argv:
            launch_antigravity(target_dir)
        return

    interactive_menu(target_dir)

if __name__ == "__main__":
    main()
