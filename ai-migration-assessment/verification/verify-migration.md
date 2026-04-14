# Verification: Migration Anti-Pattern Checker

## Overview

`verify_migration.py` is a static analysis script that checks migrated Playwright files for
8 anti-patterns that AI tools commonly introduce during Selenium → Playwright migrations.
It produces structured pass/fail output per rule and exits with code 1 if any hard failures are found.

---

## Usage

```bash
# Check a single file
python verification/verify_migration.py tests/playwright/pages/login_page.py

# Check all migrated files at once
python verification/verify_migration.py tests/playwright/

# Output is written to migration_report.json alongside the human-readable summary
```

---

## Anti-Patterns Checked

| # | Rule ID | Level | What it catches |
|---|---------|-------|-----------------|
| 1 | `no-selenium-imports` | **FAIL** | Any `import selenium` or `from selenium` in a migrated file |
| 2 | `no-time-sleep` | **FAIL** | `time.sleep()` calls — Playwright auto-waits, explicit sleeps cause flakiness |
| 3 | `no-webdriverwait` | **FAIL** | `WebDriverWait` references — a common AI literal-translation mistake |
| 4 | `no-find-element` | **FAIL** | `.find_element()` / `.find_elements()` calls — Selenium locator API leaking through |
| 5 | `no-wait-for-timeout` | **FAIL** | `page.wait_for_timeout()` used as a drop-in sleep — almost always wrong |
| 6 | `no-plain-assert-element` | **FAIL** | `assert el.text ==` or `self.assertEqual` on element state — must use `expect()` |
| 7 | `no-xpath` | **WARN** | XPath locators without a `# TODO: replace XPath` comment — needs human review |
| 8 | `no-unittest-testcase` | **FAIL** | Test class still inherits from `unittest.TestCase` — blocks pytest-playwright fixtures |

**FAIL** = blocks merge.
**WARN** = PR comment required; human must sign off before merge.

---

## Sample Output

```
────────────────────────────────────────────────────────────
FILE: tests/playwright/pages/checkout_page.py
────────────────────────────────────────────────────────────
  PASS  [no-selenium-imports]: 
  FAIL  [no-time-sleep] — line 34: time.sleep() found — delete it; Playwright auto-waits
  PASS  [no-webdriverwait]: 
  FAIL  [no-find-element] — line 41: .find_element() found — replace with page.get_by_* or page.locator()
  PASS  [no-wait-for-timeout]: 
  PASS  [no-plain-assert-element]: 
  WARN  [no-xpath] — line 58: XPath locator found without '# TODO: replace XPath' comment
  PASS  [no-unittest-testcase]: 

════════════════════════════════════════════════════════════
SUMMARY: 6 passed · 2 failed · 1 warnings
RESULT:  FAIL
════════════════════════════════════════════════════════════

JSON report written to: migration_report.json
```

The JSON report (`migration_report.json`) is structured for CI consumption:

```json
[
  {
    "file": "tests/playwright/pages/checkout_page.py",
    "findings": [
      {"rule": "no-selenium-imports", "level": "PASS", "line": null, "detail": ""},
      {"rule": "no-time-sleep", "level": "FAIL", "line": 34, "detail": "time.sleep() found..."},
      {"rule": "no-find-element", "level": "FAIL", "line": 41, "detail": ".find_element() found..."},
      {"rule": "no-xpath", "level": "WARN", "line": 58, "detail": "XPath locator found..."}
    ],
    "passed": false
  }
]
```

---

## CI Integration

Add this step to your PR pipeline (GitHub Actions example) **before** the Playwright test run:

```yaml
# .github/workflows/pr-checks.yml

jobs:
  migration-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run migration verification
        run: python verification/verify_migration.py tests/playwright/
        # Exits with code 1 on any FAIL → blocks merge

      - name: Upload JSON report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: migration-report
          path: migration_report.json

      - name: Comment WARNs on PR
        if: always()
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python -c "
          import json, subprocess, sys
          data = json.load(open('migration_report.json'))
          warns = [
            f'- {f[\"file\"]}:{f[\"line\"]} [{f[\"rule\"]}]: {f[\"detail\"]}'
            for r in data for f in r['findings'] if f['level'] == 'WARN'
          ]
          if warns:
            body = '### Migration Warnings (WARN)\nThese need human review before merge:\n' + '\n'.join(warns)
            subprocess.run(['gh', 'pr', 'comment', '--body', body], check=True)
          "
```

**How it plugs into CI:**
The `migration-lint` job runs as a required status check — any FAIL finding causes an exit code 1,
which GitHub marks the check as failed and blocks the PR from merging. WARN-level findings post
a PR comment automatically via `gh pr comment`, but do not set a failing exit code; a human reviewer
must acknowledge the warning (via a PR approval or a specific sign-off comment) before the PR can merge.
This two-tier approach ensures hard migration errors are caught automatically while XPath fallbacks
and other soft issues get human eyes without blocking CI entirely.

---

## Running Against a Known-Bad File (Test the Verifier)

To confirm the verifier catches all 8 patterns, run it against the provided test fixture:

```bash
python verification/verify_migration.py verification/test_fixtures/bad_migration_example.py
```

Expected result: 7 FAIL, 1 WARN, exit code 1.

### `verification/test_fixtures/bad_migration_example.py`

```python
import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from tests.playwright.pages.login_page import LoginPage


class TestBadMigration(unittest.TestCase):  # anti-pattern 8: unittest.TestCase

    def setUp(self):
        pass

    def test_login(self, page):
        wait = WebDriverWait(page, 10)  # anti-pattern 3: WebDriverWait
        el = page.find_element(By.ID, "username")  # anti-pattern 4: find_element
        el.send_keys("admin")
        time.sleep(2)  # anti-pattern 2: time.sleep
        page.wait_for_timeout(1000)  # anti-pattern 5: wait_for_timeout
        result = page.find_element(By.XPATH, "//div[@class='msg']")  # anti-pattern 7: xpath
        assert result.text == "Welcome"  # anti-pattern 6: plain assert on element text
        # anti-pattern 1: selenium import is at top of file
```
