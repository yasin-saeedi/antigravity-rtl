# Antigravity Smart RTL & Offline Typography Suite 🚀

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Version: 2.0.0](https://img.shields.io/badge/Release-v2.0.0-8A2BE2?style=for-the-badge)](https://github.com/yasin-saeedi/antigravity-rtl/releases/tag/v2.0.0)
[![Install: 1--Line PowerShell](https://img.shields.io/badge/Install-1--Line%20PowerShell-0078D6?style=for-the-badge&logo=powershell&logoColor=white)](#quick-start--installation)
[![Tests: 47 Passed](https://img.shields.io/badge/Automated%20Tests-47%20Passed-brightgreen?style=for-the-badge&logo=pytest)](tests/)
[![Offline Fonts](https://img.shields.io/badge/Persian%20Fonts-100%25%20Offline-FF6B6B?style=for-the-badge)](fonts/)

**Professional, intelligent bidirectional text direction (RTL/LTR) engine with native Antigravity Plugin & Sidecar architecture, fully offline embedded Persian fonts, and live hot-reloading for Google Antigravity IDE.**

[English](#english) • [فارسی (Persian)](#فارسی-persian)

---

</div>

<a name="english"></a>

## Overview

**Antigravity Smart RTL** transforms the text presentation experience in Google DeepMind's Antigravity IDE. It delivers enterprise-grade right-to-left (RTL) typography for Persian, Arabic, and bilingual environments while rigorously preserving left-to-right (LTR) orientation for source code, terminals, tool panels, thoughts, and technical identifiers.

Starting with **v2.0.0**, Antigravity Smart RTL features a **dual-architecture engine**:
1. **Native Antigravity Plugin & Persistent Sidecar Daemon** (`~/.gemini/config/plugins/antigravity-rtl`): Deployed directly into Antigravity's native plugin ecosystem with automatic background recovery (`restart_policy: always`), rendering it **100% immune to official Antigravity application updates**.
2. **Classic Standalone ASAR Patcher & CLI** (`patch.bat`, `src/patcher.py`, `src/patcher.js`): Hardened against Electron ASAR boundary restrictions for offline, enterprise, and air-gapped environments.

---

## Key Features & Strengths

### ⚡ 1-Line Zero-Dependency PowerShell Installation
- Install and activate instantly with a single PowerShell line:
  ```powershell
  irm https://raw.githubusercontent.com/yasin-saeedi/antigravity-rtl/main/install.ps1 | iex
  ```
- **Zero prerequisites**: Does not require Git, npm, or Python. Automatically integrates into Antigravity and hot-reloads running windows via CDP.

### 🌌 Native Antigravity Plugin & Sidecar Architecture
- Deployed to `~/.gemini/config/plugins/antigravity-rtl` with native [plugin.json](plugin.json) manifest.
- Antigravity 2.0 automatically spawns and manages the persistent background sidecar daemon (`sidecars/rtl/sidecar.json`) with `restart_policy: always`.
- **Update Resilience**: Because plugins reside in the user configuration directory rather than the installation folder, official IDE updates never erase your RTL configuration.

### 🎯 Intelligent Bidirectional Engine (Smart RTL with 70% Letter Ratio)
- **Letter-Only Density Ratio**: Strips punctuation, symbols, and digits to analyze purely alphabetical characters. Lines are rendered LTR only if Latin letters constitute $\ge 70\%$ of all letters, guaranteeing that Persian sentences with English terms, package names, or commands remain perfectly aligned to the right.
- **Flawless Bilingual Rendering**: Persian sentences align to the right with proper punctuation placement, while English technical phrases, inline code, and symbols remain perfectly oriented.

### 📦 100% Offline Embedded Typography
- **Zero Internet / Zero CDN Dependency**: High-quality WOFF2 Persian fonts are embedded directly via Base64 data URIs inside the engine.
- **Bundled Fonts**:
  - **Vazirmatn** (Regular 400, Medium 500, Bold 700) — Default modern sans-serif
  - **Shabnam** (Regular 400, Bold 700)
  - **Sahel** (Regular 400, Bold 700)
  - **Samim** (Regular 400, Bold 700)
- **Instantaneous Rendering**: Eliminates Flash of Unstyled Text (FOUT), CDN latency, and DNS lookup delays entirely. Works in completely air-gapped or restricted offline environments.

### 🛡️ Ironclad Technical Isolation
- **Preserved Coding Environments**: Strict LTR isolation enforced on:
  - Monaco Editor instances & syntax-highlighted code blocks
  - Integrated terminal buffers and command logs
  - Agent Thought streams, tool invocation cards, and execution metadata
  - Numerical metrics, tabular data, JSON payloads, and Git diffs

### ⚙️ Interactive In-App Appearance Control Center
- **Floating Toolbar Menu**: Directly accessible from the Antigravity IDE top bar (`Appearance`).
- **Real-Time Customization**:
  - Toggle Smart RTL on/off in real-time
  - Select between Vazirmatn, Shabnam, Sahel, Samim, Tahoma, System, or a Custom font
  - Adjust typography font size (`12px` – `22px`) with instant visual feedback
  - Adjust line height (`Compact 1.5`, `Normal 1.75`, `Relaxed 2.0`)
- **Persistent Preferences**: Automatically saved to `localStorage` and restored across window refreshes and IDE restarts.

### 🔄 Live Hot-Reload via Chrome DevTools Protocol (CDP)
- Connects directly to the active Antigravity IDE window using the internal DevTools WebSocket bridge.
- Applies style injection, DOM direction adjustments, and menu bar mounting **instantly without closing or restarting the IDE**.

### 🔒 Dual-Engine Stability & Downgrade Prevention
- Custom 16-byte binary ASAR parser and serializer with `process.noAsar = true` and CommonJS module isolation.
- Automatic creation of untouched factory backups (`app.asar.original_backup`).
- Version-aware metadata guards prevent accidental application downgrades.

---

## Architecture & File Structure

```
antigravity-rtl/
├── bin/
│   └── cli.js                         # Cross-platform CLI runner (install / uninstall / status)
├── fonts/                             # Raw offline WOFF2 webfonts
│   ├── Vazirmatn-Regular.woff2
│   ├── Vazirmatn-Medium.woff2
│   ├── Vazirmatn-Bold.woff2
│   ├── Shabnam.woff2 & Shabnam-Bold.woff2
│   ├── Sahel.woff2 & Sahel-Bold.woff2
│   └── Samim.woff2 & Samim-Bold.woff2
├── scripts/
│   ├── install-plugin.js              # Native plugin deployment & live hot-reload trigger
│   └── uninstall-plugin.js            # Plugin removal & DOM cleanup utility
├── sidecars/
│   └── rtl/
│       └── sidecar.json               # Antigravity persistent background sidecar definition
├── src/
│   ├── injector/
│   │   └── rtl-engine.js              # In-DOM smart direction engine & Appearance menu
│   ├── sidecar/
│   │   ├── cdp-bridge.js              # Pure Node.js DevTools WebSocket client
│   │   └── index.js                   # Persistent background daemon process
│   ├── antigravity-chat-rtl.css       # Standalone stylesheet with embedded Base64 fonts
│   ├── patcher.py                     # High-performance Python patch engine & CLI
│   ├── patcher.js                     # Zero-dependency Node.js patch engine (CommonJS)
│   └── AntigravityLauncher.exe        # Optional Auto-Shield background launcher
├── tests/                             # Enterprise automated test suite (47 tests)
│   ├── test_asar.py                   # 16-byte ASAR header & binary round-trip tests
│   ├── test_cli.py                    # CLI args, closed-stdin, & shortcut opt-in tests
│   ├── test_css.py                    # CSS selector escaping & offline font tests
│   ├── test_direction.py              # Bilingual smart direction accuracy tests
│   ├── test_downgrade.py              # Downgrade prevention & factory restore tests
│   ├── test_performance.py            # Zero-reflow DOM mutation & non-blocking tests
│   └── test_plugin_sidecar.py         # Native plugin & sidecar daemon verification tests
├── install.ps1                        # 1-line native Windows PowerShell installer
├── package.json                       # NPM package manifest (v2.0.0)
├── plugin.json                        # Native Antigravity Plugin manifest
├── patch.bat                          # Universal one-click Windows launcher
└── run_tests.py                       # Automated multi-tier test runner
```

---

## Quick Start & Installation

### Option 1: 1-Line PowerShell Installation (Recommended)
Run the following command in Windows PowerShell (no administrative rights, Git, or Python required):

```powershell
irm https://raw.githubusercontent.com/yasin-saeedi/antigravity-rtl/main/install.ps1 | iex
```

This downloads the plugin, links it into Antigravity's native plugin manager, and hot-reloads running editor windows immediately.

---

### Option 2: CLI & Local Installation
If you have cloned this repository locally:

```powershell
# Using the bundled CLI
node bin/cli.js install

# Check plugin status
node bin/cli.js status

# Uninstall plugin
node bin/cli.js uninstall
```

---

### Option 3: Universal Windows Launcher (`patch.bat`)
Double-click `patch.bat` or execute in Command Prompt / PowerShell:

```cmd
patch.bat
```

The interactive Command Center will launch:
```
  [1] Install Smart RTL (Safe Default - Shortcuts Preserved)
  [2] Restore 100% Factory Original
  [3] Install Smart RTL with Auto-Shield Shortcuts (Opt-in)
  [4] System Diagnostics & Health Check
  [0] Exit Patcher
```
Simply press `Enter` to install with safe defaults (shortcuts unchanged).

---

### Option 4: Python & Node.js Standalone CLI Execution

```powershell
# Python engine
python src/patcher.py

# Python restore to factory state
python src/patcher.py --restore

# Node.js engine
node src/patcher.js

# Node.js restore to factory state
node src/patcher.js --restore
```

---

## CLI Flags & Options

| Flag | Shorthand | Description |
|---|---|---|
| `--install-shortcuts` | `--shortcuts`, `-s`, `3` | **Opt-in**: Protects desktop & start menu shortcuts using `AntigravityLauncher.exe` for automatic update healing. Default is disabled (safe mode). |
| `--restore` | `-r`, `2` | Fully restores `app.asar` from original factory backup and reverts shortcuts. |
| `--diagnostics` | `--diag`, `4` | Displays system telemetry, patch status, live CDP port, and installation health check. |
| `--path <dir>` | `-p <dir>` | Explicitly targets an Antigravity installation path. |
| `--no-kill` | | Applies the patch without closing running Antigravity processes; synchronizes via live CDP. |
| `--kill` | | Forces closing Antigravity IDE processes before patching. |
| `--launch` | | Automatically launches Antigravity IDE upon successful patching. |
| `--check-only` | | Silent check: returns `1` if patched, `0` if original. |
| `--wait-for-update` | | Background daemon mode: monitors updater processes and re-patches automatically. |

---

## Verification & Automated Test Suite

The project includes an enterprise-grade automated test suite with **47 verified tests** across 6 tiers:

```powershell
python run_tests.py
```

### Test Coverage Highlights
- **Tier 1 (CLI Interface)**: Tests non-interactive execution, closed `stdin` (`DEVNULL`) resilience, `--install-shortcuts` opt-in semantics, option `3` / `4` shortcuts & diagnostics, and default disabled shortcuts.
- **Tier 2 (CSS & Offline Fonts)**: Validates `#antigravity\\.agentSidePanelInputBox` selector escaping in runtime V8 environments and verifies complete offline Base64 font embedding across all 4 font families.
- **Tier 3 (ASAR Integrity)**: Tests 16-byte ASAR binary header generation, file extraction, chunked round-trip reconstruction, and cross-engine Python/Node compatibility.
- **Tier 4 (Downgrade Prevention)**: Proves that restoring an older backup never silently downgrades a newer official application release across both Python and Node.js engines.
- **Tier 5 (Zero-Reflow Performance)**: Verifies 0 occurrences of synchronous `.innerText` layout thrashing, enforcing non-reflow `.textContent` DOM reads.
- **Tier 6 (Plugin & Sidecar Daemon)**: Verifies `plugin.json` schema, `sidecars/rtl/sidecar.json` always-restart daemon configuration, PowerShell syntax integrity in `install.ps1`, DOM engine 70% threshold, and CLI status execution.

---

<a name="فارسی-persian"></a>

## فارسی (Persian)

### پچ جامع راست‌چین هوشمند و قلم‌های فارسی آفلاین آنتی‌گراویتی

**پروژه Antigravity Smart RTL** یک راهکار حرفه‌ای، مهندسی‌شده و فوق‌العاده سریع برای فعال‌سازی کامل پشتیبانی از زبان فارسی، چیدمان راست‌به‌چپ (RTL) و فونت‌های استاندارد فارسی در محیط توسعه **Antigravity IDE** (محصول هوش مصنوعی پیشرفته Google DeepMind) است.

از نسخه **v2.0.0** به بعد، این پروژه با معماری مدرن **Native Plugin & Sidecar Daemon** عرضه می‌شود که به صورت یکپارچه درون اکوسیستم بومی پلاگین‌های آنتی‌گراویتی قرار می‌گیرد و **به طور کامل در برابر آپدیت‌های رسمی نرم‌افزار مصون است**.

---

### قابلیت‌های برجسته

1. **نصب فوق‌العاده آسان و تک‌خطی (بدون هیچ پیش‌نیاز)**:
   - امکان نصب فوری در محیط PowerShell تنها با اجرای یک دستور ساده، بدون نیاز به نصب Git، npm یا Python:
     ```powershell
     irm https://raw.githubusercontent.com/yasin-saeedi/antigravity-rtl/main/install.ps1 | iex
     ```

2. **معماری بومی پلاگین و سایدکار همیشه فعال (Sidecar Daemon)**:
   - استقرار در پوشه `~/.gemini/config/plugins/antigravity-rtl` با ساختار رسمی پلاگین‌های آنتی‌گراویتی.
   - دیمون پس‌زمینه با سیاست `restart_policy: always` به صورت خودکار توسط هسته برنامه کنترل شده و در صورت آپدیت نرم‌افزار حذف نمی‌شود.

3. **اعمال زنده بدون بستن یا ری‌استارت برنامه (Live CDP Hot-Reload)**:
   - اعمال مستقیم و آنی استایل‌ها و موتور راست‌چین روی پنجره‌های فعال برنامه از طریق وب‌سوکت پروتکل ابزارهای توسعه‌دهنده (Chrome DevTools Protocol)، بدون نیاز به بستن پنجره‌ها یا ری‌استارت سیستم.

4. **جهت‌بندی هوشمند با فرمول نسبت ۷۰ درصدی حروف (70% Letter Ratio)**:
   - حذف کامل اعداد، علائم نگارشی و کاراکترهای خاص در هنگام تحلیل متن و محاسبه خالص نسبت حروف.
   - خطوط متنی تنها در صورتی چپ‌چین (LTR) می‌شوند که حداقل ۷۰٪ از کل حروف، الفبای انگلیسی باشند؛ در نتیجه جملات فارسی که با کلمات انگلیسی، نام متغیرها، پکیج‌ها یا دستورات طولانی شروع می‌شوند با قطعیت کامل راست‌چین (RTL) باقی می‌مانند.

5. **فونت‌های ۱۰۰٪ آفلاین تعبیه‌شده (بدون نیاز به اینترنت)**:
   - تمامی فونت‌ها (شامل **وزیرمتن** در ۳ وزن، **شبنم**، **ساحل** و **صمیم**) به صورت فایل‌های بهینه‌سازی‌شده WOFF2 در پروژه ذخیره شده و از طریق کدهای Base64 مستقیماً درون استایل تعبیه شده‌اند.
   - هیچ وابستگی به اینترنت یا CDN وجود ندارد و سرعت لود فونت‌ها صفر ثانیه است.

6. **منوی تنظیمات ظاهری در نوار بالای برنامه (Appearance Control Center)**:
   - دسترسی آسان به منوی تنظیمات از طریق نوار بالای برنامه (`Appearance`) جهت تغییر درلحظه فونت، اندازه متن (`12px` تا `22px`)، فاصله خطوط و فعال/غیرفعال‌سازی راست‌چین همراه با ذخیره‌سازی دائمی تنظیمات در حافظه محلی.

7. **مصون‌سازی کامل بخش‌های فنی و کدها**:
   - محیط‌های ادیتور موناکو (Monaco Editor)، لاگ‌های ترمینال، کدهای چندخطی و درون‌متنی، بخش تفکرات مدل (Thought Process)، کارت‌های اجرای ابزارها و خروجی‌های Git همواره با جهت استاندارد چپ‌به‌راست (LTR) نمایش داده می‌شوند.

8. **پایداری دوگانه و پچرهای کلاسیک (Dual-Engine Stability)**:
   - علاوه بر پلاگین بومی، پچرهای سنتی ASAR (`patch.bat`, `src/patcher.py`, `src/patcher.js`) همچنان پابرجا بوده و با رفع محدودیت‌های Electron ASAR برای محیط‌های ایزوله کامپایل شده‌اند.

---

### روش‌های نصب و استفاده

#### روش اول: نصب تک‌خطی در پاورشل (پیشنهادی)
ترمینال PowerShell را باز کرده و دستور زیر را اجرا کنید:

```powershell
irm https://raw.githubusercontent.com/yasin-saeedi/antigravity-rtl/main/install.ps1 | iex
```

---

#### روش دوم: اجرای لانچر تعاملی ویندوز (`patch.bat`)
کافیست روی فایل `patch.bat` دو بار کلیک کنید یا در محیط CMD / PowerShell آن را اجرا نمایید:

```cmd
patch.bat
```

منوی زیر باز خواهد شد:
```
  [1] Install Smart RTL (Safe Default - Shortcuts Preserved)
  [2] Restore 100% Factory Original
  [3] Install Smart RTL with Auto-Shield Shortcuts (Opt-in)
  [4] System Diagnostics & Health Check
  [0] Exit Patcher
```
فشردن کلید `Enter` گزینه پیش‌فرض ۱ (نصب ایمن با حفظ شرت‌کات‌ها) را اعمال می‌کند.

---

#### روش سوم: اجرای CLI پایتون یا نودجی‌اس

```powershell
# اجرای پچر پایتون
python src/patcher.py

# بازگردانی به نسخه اصلی با پایتون
python src/patcher.py --restore

# اجرای پچر Node.js
node src/patcher.js

# بازگردانی با Node.js
node src/patcher.js --restore
```

---

## License

This project is licensed under the [MIT License](LICENSE). Built for the developer community with focus on speed, typography quality, and zero-compromise stability.
