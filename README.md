# Antigravity Smart RTL & Offline Typography Suite 🚀

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Node.js 16+](https://img.shields.io/badge/Node.js-16+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org)
[![Tests: 40 Passed](https://img.shields.io/badge/Automated%20Tests-40%20Passed-brightgreen?style=for-the-badge&logo=pytest)](tests/)
[![Offline Fonts](https://img.shields.io/badge/Persian%20Fonts-100%25%20Offline-FF6B6B?style=for-the-badge)](fonts/)

**Professional, intelligent bidirectional text direction (RTL/LTR) engine with fully offline embedded Persian fonts and zero-reflow layout architecture for Antigravity IDE.**

[English](#english) • [فارسی (Persian)](#فارسی-persian)

---

</div>

<a name="english"></a>

## Overview

**Antigravity Smart RTL** transforms the text presentation experience in Google DeepMind's Antigravity IDE. It delivers enterprise-grade right-to-left (RTL) typography for Persian, Arabic, and bilingual environments while rigorously preserving left-to-right (LTR) orientation for source code, terminals, tool panels, thoughts, and technical identifiers.

Engineered for performance and resilience, it features a dual-engine architecture (Python & Node.js), 100% offline embedded Persian fonts, live hot-reloading via the Chrome DevTools Protocol, and strict non-destructive shortcut handling by default.

---

## Key Features & Strengths

### 🎯 Intelligent Bidirectional Engine (Smart RTL)
- **Granular Block & Paragraph Inspection**: Evaluates text direction per-element (messages, paragraphs, list items, headers, and prompts) using the First Strong Directional Character algorithm.
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
- **Floating Glassmorphism Toolbar Menu**: Directly accessible from the Antigravity IDE top bar (`Appearance`).
- **Real-Time Customization**:
  - Toggle Smart RTL on/off in real-time
  - Select between Vazirmatn, Shabnam, Sahel, Samim, Tahoma, System, or a Custom font
  - Adjust typography font size (`12px` – `22px`) with instant visual feedback
  - Adjust line height (`Compact 1.5`, `Normal 1.75`, `Relaxed 2.0`)
- **Persistent Preferences**: Automatically saved to `localStorage` and restored across window refreshes and IDE restarts.

### ⚡ Live Sync via Chrome DevTools Protocol (CDP)
- Detects running Antigravity IDE instances and synchronizes CSS/DOM modifications live into open editor windows without requiring an application restart.

### 🔒 Safe by Default: Preserved Windows Shortcuts
- **Non-Destructive Execution**: By default, the patcher never modifies your Windows Desktop or Start Menu shortcuts.
- **Opt-in Auto-Shield**: Users who desire automatic background re-patching after official IDE updates can easily opt in using the `--install-shortcuts` flag or interactive menu option 3.

### 🛡️ Atomic ASAR Packaging & Downgrade Prevention
- Custom 16-byte binary ASAR parser and serializer supporting chunked streaming and round-trip verification.
- Automatically creates an untouched factory backup (`app.asar.original_backup`).
- Version-aware metadata guards prevent accidental application downgrades.

---

## Architecture & File Structure

```
antigravity-rtl/
├── fonts/                             # Raw offline WOFF2 webfonts
│   ├── Vazirmatn-Regular.woff2
│   ├── Vazirmatn-Medium.woff2
│   ├── Vazirmatn-Bold.woff2
│   ├── Shabnam.woff2 & Shabnam-Bold.woff2
│   ├── Sahel.woff2 & Sahel-Bold.woff2
│   └── Samim.woff2 & Samim-Bold.woff2
├── src/
│   ├── antigravity-chat-rtl.css       # Standalone stylesheet with embedded Base64 fonts
│   ├── patcher.py                     # High-performance Python patch engine & CLI
│   ├── patcher.js                     # Zero-dependency Node.js patch engine
│   ├── AntigravityLauncher.exe        # Optional Auto-Shield background launcher
│   └── fonts/                         # Engine-local font distribution
├── tests/                             # Enterprise automated test suite (40 tests)
│   ├── test_asar.py                   # 16-byte ASAR header & binary round-trip tests
│   ├── test_cli.py                    # CLI args, closed-stdin, & shortcut opt-in tests
│   ├── test_css.py                    # CSS selector escaping & offline font tests
│   ├── test_direction.py              # Bilingual smart direction accuracy tests
│   ├── test_downgrade.py              # Downgrade prevention & factory restore tests
│   └── test_performance.py            # Zero-reflow DOM mutation & non-blocking tests
├── patch.bat                          # Universal one-click Windows launcher
└── run_tests.py                       # Automated multi-tier test runner
```

---

## Quick Start & Installation

### Option A: One-Click Launcher (Recommended)
Double-click `patch.bat` or execute in PowerShell / Command Prompt:

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

### Option B: Python CLI Execution
```powershell
# Standard safe install (Windows shortcuts remain untouched)
python src/patcher.py

# Opt-in: Install with Auto-Shield & Windows shortcuts
python src/patcher.py --install-shortcuts

# Specify custom installation path
python src/patcher.py --path "C:\Users\<User>\AppData\Local\Programs\antigravity"

# Restore factory untouched state
python src/patcher.py --restore
```

### Option C: Node.js CLI Execution
```powershell
# Standard safe install
node src/patcher.js

# Opt-in: Install with shortcuts
node src/patcher.js --install-shortcuts

# Restore original factory state
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

The project includes an enterprise-grade automated test suite with **40 verified tests** across 5 tiers:

```powershell
python run_tests.py
```

### Test Coverage Highlights
- **Tier 1 (CLI Interface)**: Tests non-interactive execution, closed `stdin` (`DEVNULL`) resilience, `--install-shortcuts` opt-in semantics, option `3` / `4` shortcuts & diagnostics, and default disabled shortcuts.
- **Tier 2 (CSS & Offline Fonts)**: Validates `#antigravity\\.agentSidePanelInputBox` selector escaping in runtime V8 environments and verifies complete offline Base64 font embedding across all 4 font families.
- **Tier 3 (ASAR Integrity)**: Tests 16-byte ASAR binary header generation, file extraction, chunked round-trip reconstruction, and cross-engine Python/Node compatibility.
- **Tier 4 (Downgrade Prevention)**: Proves that restoring an older backup never silently downgrades a newer official application release across both Python and Node.js engines.
- **Tier 5 (Zero-Reflow Performance)**: Verifies 0 occurrences of synchronous `.innerText` layout thrashing, enforcing non-reflow `.textContent` DOM reads.

---

<a name="فارسی-persian"></a>

## فارسی (Persian)

### پچ جامع راست‌چین هوشمند و قلم‌های فارسی آفلاین آنتی‌گراویتی

**پروژه Antigravity Smart RTL** یک راهکار حرفه‌ای، مهندسی‌شده و فوق‌العاده سریع برای فعال‌سازی کامل پشتیبانی از زبان فارسی، چیدمان راست‌به‌چپ (RTL) و فونت‌های استاندارد فارسی در محیط توسعه **Antigravity IDE** (محصول هوش مصنوعی پیشرفته Google DeepMind) است.

### قابلیت‌های برجسته

1. **جهت‌بندی هوشمند و خودکار (Smart Dynamic RTL)**:
   - تشخیص خودکار جهت متن خط‌به‌خط و پاراگراف‌به‌پاراگراف.
   - جملات فارسی راست‌چین و متون انگلیسی، متغیرها و کدهای داخل متن چپ‌چین باقی می‌مانند.

2. **فونت‌های ۱۰۰٪ آفلاین تعبیه‌شده (بدون نیاز به اینترنت)**:
   - تمامی فونت‌ها (شامل **وزیرمتن** در ۳ وزن، **شبنم**، **ساحل** و **صمیم**) به صورت فایل‌های بهینه‌سازی‌شده WOFF2 در پروژه ذخیره شده و از طریق کدهای Base64 مستقیماً درون استایل تعبیه شده‌اند.
   - هیچ وابستگی به اینترنت یا CDN وجود ندارد و سرعت لود فونت‌ها صفر ثانیه است.

3. **حفظ کامل شرت‌کات‌ها به صورت پیش‌فرض (Safe by Default)**:
   - به صورت پیش‌فرض، شرت‌کات‌های ویندوز، دسکتاپ و استارت منوی شما هیچ تغییری نمی‌کنند.
   - در صورت تمایل کاربر، قابلیت شیلد ضدآپدیت و اتصال به لانچر از طریق فلگ `--install-shortcuts` یا گزینه ۳ در منوی تعاملی در دسترس است.

4. **مصون‌سازی کامل بخش‌های فنی و کدها**:
   - محیط‌های ادیتور موناکو (Monaco Editor)، لاگ‌های ترمینال، کدهای چندخطی و درون‌متنی، بخش تفکرات مدل (Thought Process)، کارت‌های اجرای ابزارها و خروجی‌های Git همواره با جهت استاندارد چپ‌به‌راست (LTR) نمایش داده می‌شوند.

5. **منوی تنظیمات ظاهری (Appearance Control Center)**:
   - اضافه شدن یک دکمه مدرن در نوار بالای آنتی‌گراویتی جهت تغییر درلحظه فونت، اندازه متن (`12px` تا `22px`)، فاصله خطوط و فعال/غیرفعال‌سازی راست‌چین همراه با ذخیره‌سازی دائمی تنظیمات.

6. **همگام‌سازی زنده پنجره (Live CDP Sync)**:
   - اعمال مستقیم تغییرات در پنجره‌های باز برنامه بدون نیاز به بستن یا راه‌اندازی مجدد نرم‌افزار.

### نحوه اجرای سریع

کافیست فایل `patch.bat` را با دو بار کلیک اجرا کنید، یا دستور زیر را در ترمینال وارد نمایید:

```powershell
python src/patcher.py
```

برای اعمال پچ همراه با شیلد محافظتی شرت‌کات‌ها:
```powershell
python src/patcher.py --install-shortcuts
```

برای بازگردانی کامل به نسخه اولیه کارخانه:
```powershell
python src/patcher.py --restore
```

---

## License

This project is licensed under the [MIT License](LICENSE). Built for the developer community with focus on speed, typography quality, and zero-compromise stability.
