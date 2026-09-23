import json
import sys
import subprocess
import pytest
from pathlib import Path

from tests.helpers import SRC_DIR
from tests.test_css import run_node_eval

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import patcher


class TestSmartDirectionDetection:
    """
    Verifies that detectSmartDirection accurately classifies bilingual Persian/English sentences,
    paths, markdown headings, numbered lists, and sidebar conversation titles without false LTR penalties.
    """

    def test_smart_direction_bilingual_and_edge_cases(self):
        snippet = patcher.get_injection_snippet()
        test_cases = [
            "1. این گزینه هاش چی ان!",
            "token_ABC123EXAMPLETOKEN456\nبدون ریدمی و... با این توکنِ گیتهاب پروژه رو لانچ کن.",
            "Git commit و push انجام شد.",
            "فایل C:\\Users\\Farasystem\\AppData\\Local\\Programs\\antigravity\\resources\\app.asar را بررسی کن.",
            "پروژه را با دستور python src/patcher.py --apply --no-kill اجرا کن.",
            "Setup PythonAnywhere Project Folders",
            "Quasar System Prompts Overview",
            "Untitled Conversation",
            "[DONE] تست‌ها با موفقیت پاس شدند.",
            "* تست شماره ۱: بررسی فونت وزیرمتن",
            "### ۳. نقشه راه رفع ریشه‌ای و اصولی",
            "Antigravity به درستی کار می‌کند.",
            "This is a simple English test sentence.",
            "1. this is an english test",
            "2. another english test with numbers",
            "`patcher.py` بهینه‌سازی شد.",
            "تغییرات ربات جستجوی موزیک",
            "عیب‌یابی ابزارهای ربات",
            "فعال‌سازی ربات مهمان",
            "گزارش تحلیل کاربران کوازار",
            "بررسی کندی ربات",
        ]
        expected = [
            "rtl",
            "rtl",
            "rtl",
            "rtl",
            "rtl",
            "ltr",
            "ltr",
            "ltr",
            "rtl",
            "rtl",
            "rtl",
            "rtl",
            "ltr",
            "ltr",
            "ltr",
            "rtl",
            "rtl",
            "rtl",
            "rtl",
            "rtl",
            "rtl",
        ]

        eval_script = """
        const snippetCode = """ + json.dumps(snippet) + """;
        const cases = """ + json.dumps(test_cases) + """;

        // Extract detectSmartDirection function using lookahead for next function
        const match = snippetCode.match(new RegExp("function\\\\s+detectSmartDirection[\\\\s\\\\S]*?(?=\\\\s*function\\\\s+applySmartDirectionToElement)"));
        if (!match) {
            console.error("Failed to find detectSmartDirection in snippet");
            process.exit(1);
        }
        const fn = new Function('return (' + match[0] + ')')();
        const results = cases.map(c => fn(c));
        console.log(JSON.stringify(results));
        """

        stdout = run_node_eval(eval_script)
        results = json.loads(stdout)
        assert results == expected, f"Direction mismatch: {list(zip(test_cases, results, expected))}"

    def test_sidebar_selector_in_process_all_smart_rtl(self):
        snippet = patcher.get_injection_snippet()
        assert '[data-testid="conversation-row-sidebar"]' in snippet, (
            'processAllSmartRTL selector must include [data-testid="conversation-row-sidebar"]'
        )

    def test_70_percent_ratio_threshold(self):
        snippet = patcher.get_injection_snippet()
        ratio_cases = [
            # Under 70% Latin: should be RTL
            ("Docker container در حال اجراست.", "rtl"),
            ("Antigravity IDE یک ابزار فوق‌العاده است.", "rtl"),
            ("این یک متن با 12345 عدد و علائم: !@#$%^&*() است.", "rtl"),
            # Over 70% Latin: should be LTR
            ("This is an English sentence that mentions کاربر once.", "ltr"),
            ("The quick brown fox jumps over the lazy dog و گربه.", "ltr"),
        ]

        eval_script = """
        const snippetCode = """ + json.dumps(snippet) + """;
        const cases = """ + json.dumps([c[0] for c in ratio_cases]) + """;

        const match = snippetCode.match(new RegExp("function\\\\s+detectSmartDirection[\\\\s\\\\S]*?(?=\\\\s*function\\\\s+applySmartDirectionToElement)"));
        if (!match) {
            console.error("Failed to find detectSmartDirection in snippet");
            process.exit(1);
        }
        const fn = new Function('return (' + match[0] + ')')();
        const results = cases.map(c => fn(c));
        console.log(JSON.stringify(results));
        """

        stdout = run_node_eval(eval_script)
        results = json.loads(stdout)
        expected = [c[1] for c in ratio_cases]
        assert results == expected, f"Ratio mismatch: {list(zip(ratio_cases, results))}"

