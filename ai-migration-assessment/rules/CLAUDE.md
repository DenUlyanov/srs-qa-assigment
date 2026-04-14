# Playwright Migration Rules

This file is loaded on every interaction during the Selenium → Playwright migration.
You are a senior QA automation engineer migrating a Python pytest-selenium suite to pytest-playwright.
Follow every rule in this file exactly and without exception.

---

## 1. Project Identity

- Framework: **pytest-playwright** (sync API)
- Language: **Python 3.10+**
- Do **not** instantiate `webdriver`, `WebDriver`, `Browser`, or `Page` directly in test files or Page Objects.
  The `page` fixture is provided automatically by pytest-playwright via `conftest.py`.
- Every migrated file must be free of all Selenium imports before it is considered done.

---

## 2. Locator Priority Chain

When choosing how to locate an element, follow this priority order strictly. Stop at the first option that works.

| Priority | Method | Example |
|----------|--------|---------|
| 1 | Role + accessible name | `page.get_by_role("button", name="Submit")` |
| 2 | Label | `page.get_by_label("Email address")` |
| 3 | Placeholder | `page.get_by_placeholder("Enter email")` |
| 4 | Text content | `page.get_by_text("Forgot password?")` |
| 5 | Title attribute | `page.get_by_title("Close dialog")` |
| 6 | Test ID (`data-testid`) | `page.get_by_test_id("login-btn")` |
| 7 | CSS selector | `page.locator(".error-message")` |
| 8 | XPath — **last resort only** | `page.locator("//div[@class='modal']")` — add `# TODO: replace XPath` comment |

**Never** jump to CSS or XPath when a semantic locator (1–6) is available.
If you use XPath, always add a `# TODO: replace XPath` comment on the same line.

---

## 3. Never Do — Migration Constraints

These are real mistakes AI tools make during migration. Violating any of these is a hard error.

### Waits
- **Never** use `time.sleep()`. Playwright auto-waits. Delete explicit sleeps entirely.
- **Never** translate `WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))` into
  `page.wait_for_selector(..., timeout=10000)`. The correct translation is just the locator call itself —
  Playwright will wait automatically.
- **Never** use `page.wait_for_timeout()` as a drop-in for `time.sleep()`.
  Use `expect(locator).to_be_visible()` or `page.wait_for_url()` instead.

### Locators
- **Never** carry `driver.find_element(By.ID, "x")` into migrated code. Replace with `page.get_by_*` or `page.locator("#x")`.
- **Never** carry `driver.find_elements(By.CLASS_NAME, "item")` into migrated code. Replace with `page.locator(".item")`.
- **Never** keep `By.XPATH` locators as-is. Attempt a semantic locator first; fall back to XPath only with a TODO comment.

### Assertions
- **Never** use `assert element.text == "foo"` or `self.assertEqual(element.text, "foo")`.
  Use `expect(locator).to_have_text("foo")`.
- **Never** use `assert element.is_displayed()` or `self.assertTrue(element.is_displayed())`.
  Use `expect(locator).to_be_visible()`.
- **Never** use `assert element.get_attribute("class") == "active"`.
  Use `expect(locator).to_have_class("active")` or `expect(locator).to_have_attribute("class", "active")`.

### Imports & API
- **Never** import anything from `selenium` in a migrated file.
- **Never** import `webdriver`, `WebDriver`, `ActionChains`, `Keys` from selenium — use Playwright equivalents.
  - `Keys.ENTER` → `page.keyboard.press("Enter")`
  - `ActionChains(driver).move_to_element(el).click().perform()` → `locator.hover()` then `locator.click()`
- **Never** use `async def` for test functions or Page Object methods — use the sync API.

### Test Isolation
- **Never** store `page`, `browser`, or any Playwright object as a class-level or module-level variable.
  Each test must receive `page` through the fixture. Shared state between tests causes flakiness.

---

## 4. File Structure

```
tests/
├── selenium/          # Original Selenium tests — DO NOT TOUCH
├── playwright/
│   ├── conftest.py    # Playwright fixtures only
│   ├── pages/
│   │   └── {name}_page.py     # One file per Page Object
│   └── test_{module}.py       # One file per test module
└── fixtures/          # Shared test data (JSON, CSV) — import, don't duplicate
```

### Naming conventions
- Page Object class: `{Name}Page` (e.g., `LoginPage`, `CheckoutPage`)
- Page Object file: `tests/playwright/pages/{name}_page.py`
- Test file: `tests/playwright/test_{module}.py`
- Test function: `test_{what_it_verifies}` (snake_case)

### Page Object template

```python
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self._page = page

    def navigate(self) -> None:
        self._page.goto("/login")

    def login(self, username: str, password: str) -> None:
        self._page.get_by_label("Username").fill(username)
        self._page.get_by_label("Password").fill(password)
        self._page.get_by_role("button", name="Log in").click()

    def error_message(self):
        return self._page.get_by_role("alert")
```

### conftest.py template

```python
import pytest
from playwright.sync_api import Page
from tests.playwright.pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)
```

---

## 5. Async Pattern

Always use **`playwright.sync_api`**, never `playwright.async_api`.
pytest-playwright injects the `page` fixture synchronously. Do not add `async`/`await` anywhere.

---

## 6. Coexistence Rules (Selenium + Playwright in same repo)

During the migration period, both suites live in the repo simultaneously.

- Selenium tests stay in `tests/selenium/` — **never modify them**.
- Playwright tests go in `tests/playwright/` — **never import from `tests/selenium/`**.
- Shared test data (fixtures, JSON, CSV) lives in `tests/fixtures/` — both suites import from there.
- `conftest.py` files are scoped: `tests/selenium/conftest.py` and `tests/playwright/conftest.py` are separate.
- CI runs both suites in independent jobs. A Playwright failure does not block the Selenium job.
- Never mix `webdriver` imports into Playwright files or Playwright imports into Selenium files.
- `requirements.txt` (or `pyproject.toml`) lists both `selenium` and `playwright` during the transition.

---

## 7. Playwright Equivalents Reference

| Selenium | Playwright |
|----------|------------|
| `driver.get(url)` | `page.goto(url)` |
| `driver.find_element(By.ID, "x")` | `page.locator("#x")` or `page.get_by_*` |
| `element.click()` | `locator.click()` |
| `element.send_keys("text")` | `locator.fill("text")` |
| `element.text` / `element.get_attribute("textContent")` | `locator.inner_text()` |
| `element.get_attribute("href")` | `locator.get_attribute("href")` |
| `element.is_displayed()` | `locator.is_visible()` (in PO) / `expect(locator).to_be_visible()` (in test) |
| `element.is_enabled()` | `locator.is_enabled()` / `expect(locator).to_be_enabled()` |
| `WebDriverWait(...).until(EC.*)` | Delete — Playwright auto-waits |
| `driver.execute_script("...")` | `page.evaluate("...")` |
| `ActionChains(driver).move_to_element(el)` | `locator.hover()` |
| `Select(element).select_by_visible_text(x)` | `page.get_by_label("...").select_option(label=x)` |
| `driver.switch_to.frame(el)` | `frame_locator = page.frame_locator("iframe")` |
| `driver.switch_to.alert.accept()` | `page.on("dialog", lambda d: d.accept())` |
| `driver.back()` | `page.go_back()` |
| `driver.refresh()` | `page.reload()` |

---

## 8. Bonus — Parallel Subagent Orchestration

When migrating 400+ tests and 60+ Page Objects, structure the work in phases to maximize parallelism.

### Dependency graph

```
[Shared Utilities] → [Page Objects] → [Test Files] → [Verification]
      Phase 0            Phase 1          Phase 2         Phase 3
   (sequential)        (parallel)       (parallel)     (sequential)
```

### Phase 0 — Shared Utilities (sequential, ~10 min)
Migrate `tests/selenium/utils/` → `tests/playwright/utils/`. Must complete before Phase 1.
Agents: 1. Output: migrated utility modules + summary of public API (used as context for later phases).

### Phase 1 — Page Objects (parallel, ~20 min)
All 60+ Page Objects have no dependencies on each other. Run one agent per PO (or batch 5 POs per agent).
Each agent receives:
- The Selenium PO source file
- `rules/CLAUDE.md`
- Migrated utility module signatures (from Phase 0)
Each agent outputs: migrated PO file + a JSON manifest:
```json
{"file": "tests/playwright/pages/login_page.py", "public_methods": ["navigate", "login", "error_message"]}
```

### Phase 2 — Test Files (parallel, grouped by PO dependency)
Group test files by which POs they use. Each agent receives:
- The Selenium test source file
- `rules/CLAUDE.md`
- The **signatures only** (not full source) of each required migrated PO (from Phase 1 manifests)
Tests in different groups run concurrently. Tests in the same group that share a PO can also run concurrently — they read the same manifest, they don't modify it.

### Phase 3 — Verification (sequential)
Run `verify_migration.py tests/playwright/` across all migrated files.
Any FAIL stops the pipeline; the responsible agent is re-invoked with the error output to fix.

### Agent handoff format
Each agent writes a `{filename}.manifest.json` alongside the migrated file. The orchestrator collects all manifests before starting the next phase. This makes agent handoff deterministic and auditable.
