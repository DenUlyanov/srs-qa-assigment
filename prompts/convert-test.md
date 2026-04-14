# Prompt: Convert Selenium Test File → Playwright Test File

## Role

You are migrating a Python pytest-selenium test file to pytest-playwright.
Follow `rules/CLAUDE.md` exactly. Every rule there is a hard constraint.
The Page Objects this test depends on have already been migrated.

---

## Input

### Test file to migrate:

```python
{{TEST_FILE_SOURCE}}
```

### Already-migrated Page Object signatures (do not include full source):

```python
{{MIGRATED_PAGE_OBJECT_SIGNATURES}}
```

---

## Conversion Instructions

Work through these steps in order.

### Step 1 — Remove Test Class Base & Lifecycle Methods

If the test class extends `unittest.TestCase`:
- Remove the base class: `class TestLogin(unittest.TestCase)` → `class TestLogin`
- Or convert to plain pytest functions (preferred if the class has no shared setup state).

**setUp / tearDown → pytest fixtures:**

| Selenium pattern | Playwright equivalent |
|------------------|-----------------------|
| `def setUp(self)` with `webdriver.Chrome()` | Delete entirely — `page` fixture is injected by pytest-playwright |
| `def tearDown(self)` with `driver.quit()` | Delete entirely — pytest-playwright closes the browser automatically |
| `@classmethod setUpClass` with browser setup | Delete — use `browser` fixture from pytest-playwright if truly needed |
| `@pytest.fixture` that creates a WebDriver | Replace with PO fixture that accepts `page: Page` |

**Example fixture migration:**

```python
# BEFORE — conftest.py (Selenium)
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# AFTER — conftest.py (Playwright)
# No fixture needed — pytest-playwright provides `page` automatically.
# Only add fixtures for Page Object construction:
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)
```

### Step 2 — Imports

Remove:
- `import unittest`
- `from selenium...`
- `import webdriver`
- `from pytest_selenium...`

Add:
- `from playwright.sync_api import Page, expect`
- Imports for migrated Page Objects from `tests.playwright.pages.*`

### Step 3 — Page Object Instantiation

Replace `driver`-based instantiation with `page`:

```python
# BEFORE
def setUp(self):
    self.driver = webdriver.Chrome()
    self.login_page = LoginPage(self.driver)

# AFTER — as a fixture in conftest.py or at top of test
def test_login(login_page: LoginPage):
    ...
# OR inline if no conftest fixture:
def test_login(page: Page):
    login_page = LoginPage(page)
    ...
```

### Step 4 — Assertions

Replace every sync assertion with a Playwright web-first assertion:

| Selenium / unittest | Playwright |
|---------------------|------------|
| `self.assertEqual(el.text, "foo")` | `expect(locator).to_have_text("foo")` |
| `self.assertIn("foo", el.text)` | `expect(locator).to_contain_text("foo")` |
| `self.assertTrue(el.is_displayed())` | `expect(locator).to_be_visible()` |
| `self.assertFalse(el.is_displayed())` | `expect(locator).to_be_hidden()` |
| `self.assertEqual(driver.title, "Home")` | `expect(page).to_have_title("Home")` |
| `self.assertIn("/dashboard", driver.current_url)` | `expect(page).to_have_url(re.compile("/dashboard"))` |
| `self.assertEqual(el.get_attribute("class"), "active")` | `expect(locator).to_have_class("active")` |
| `assert el.is_enabled()` | `expect(locator).to_be_enabled()` |
| `self.assertEqual(len(driver.find_elements(...)), 3)` | `expect(locator).to_have_count(3)` |

**Use `expect()` not `assert`** for element state. Plain `assert` is only acceptable for non-DOM values (e.g., `assert response_data["status"] == 200`).

### Step 5 — Remove Explicit Waits

- Delete all `time.sleep()` calls.
- Delete all `WebDriverWait(...).until(...)` blocks.
- Playwright assertions (`expect(...)`) have built-in retry with a default timeout of 5 seconds.
  To change timeout: `expect(locator).to_be_visible(timeout=10000)` (milliseconds).

### Step 6 — Test Isolation

- Each test function must be independent — no shared mutable state.
- If the original used `self.driver` shared across tests, convert so each test gets its own `page` fixture.
- Do not assign `page` to a class variable or module variable.

### Step 7 — Final Check

Before outputting, verify:
- [ ] No `selenium` imports remain
- [ ] No `unittest.TestCase` base class remains
- [ ] No `setUp`/`tearDown` methods remain (or they've been converted to fixtures)
- [ ] No `webdriver.*` calls remain
- [ ] No `time.sleep()` calls remain
- [ ] No `WebDriverWait` calls remain
- [ ] All assertions use `expect(...)` for element state
- [ ] `page` is not stored as class/module-level state
- [ ] Each test function is independently runnable

---

## Output Format

Output **only** the migrated Python test file. No explanations, no markdown wrapper.
If a `conftest.py` change is required, output it as a second block after `# ---CONFTEST---`.

---

## Before / After Example

### BEFORE — `tests/selenium/test_login.py`

```python
import time
import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.selenium.pages.login_page import LoginPage


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://localhost:3000")
        self.login_page = LoginPage(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_successful_login(self):
        self.login_page.navigate()
        self.login_page.login("admin@example.com", "secret123")
        time.sleep(2)  # wait for redirect
        avatar = self.wait.until(
            EC.visibility_of_element_located((By.ID, "user-avatar"))
        )
        self.assertTrue(avatar.is_displayed())
        self.assertIn("/dashboard", self.driver.current_url)

    def test_invalid_password_shows_error(self):
        self.login_page.navigate()
        self.login_page.login("admin@example.com", "wrong")
        error = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-msg"))
        )
        self.assertEqual(error.text, "Invalid credentials")

    def test_empty_username_disabled_submit(self):
        self.login_page.navigate()
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertFalse(submit_btn.is_enabled())
```

### Migrated PO signatures provided as context:

```python
# LoginPage (tests/playwright/pages/login_page.py) — ALREADY MIGRATED
class LoginPage:
    def __init__(self, page: Page) -> None: ...
    def navigate(self) -> None: ...
    def login(self, username: str, password: str) -> None: ...
    def error_message(self) -> Locator: ...
    def user_avatar(self) -> Locator: ...
```

### AFTER — `tests/playwright/test_login.py`

```python
import re
import pytest
from playwright.sync_api import Page, expect
from tests.playwright.pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.navigate()
    return lp


def test_successful_login(login_page: LoginPage, page: Page):
    login_page.login("admin@example.com", "secret123")
    expect(login_page.user_avatar()).to_be_visible()
    expect(page).to_have_url(re.compile("/dashboard"))


def test_invalid_password_shows_error(login_page: LoginPage):
    login_page.login("admin@example.com", "wrong")
    expect(login_page.error_message()).to_have_text("Invalid credentials")


def test_empty_username_disabled_submit(page: Page):
    LoginPage(page).navigate()
    expect(page.get_by_role("button", name="Log in")).to_be_disabled()
```

**What changed and why:**
- `unittest.TestCase` + `setUp`/`tearDown` → plain pytest functions with `page` fixture (injected by pytest-playwright).
- `webdriver.Chrome()` + `driver.quit()` → deleted; pytest-playwright manages browser lifecycle.
- `time.sleep(2)` → deleted; `expect(locator).to_be_visible()` retries automatically.
- `WebDriverWait(...).until(EC.visibility_of_element_located(...))` → deleted; `expect()` handles this.
- `self.assertTrue(avatar.is_displayed())` → `expect(login_page.user_avatar()).to_be_visible()`.
- `self.assertEqual(error.text, "...")` → `expect(login_page.error_message()).to_have_text("...")`.
- `self.assertFalse(submit_btn.is_enabled())` → `expect(...).to_be_disabled()`.
- `self.assertIn("/dashboard", driver.current_url)` → `expect(page).to_have_url(re.compile("/dashboard"))`.
- Each test is now independent — no shared `self.driver` state.

---

## Context Limit Strategy

A test file may depend on 5+ Page Objects, shared config, and custom utilities. When the combined source
exceeds what fits comfortably in one prompt, use this chunking approach:

**1. Feed PO signatures, not full source.**
Generate a summary block for each dependency:
```python
# CheckoutPage (tests/playwright/pages/checkout_page.py) — ALREADY MIGRATED
class CheckoutPage:
    def __init__(self, page: Page) -> None: ...
    def fill_shipping(self, name: str, address: str) -> None: ...
    def select_payment(self, method: str) -> None: ...
    def place_order(self) -> None: ...
    def confirmation_number(self) -> Locator: ...
```
A 5-PO suite typically adds ~2KB of signatures vs ~20KB of full source.

**2. Maintain a `migration-context.md` file** (checked into the repo root during migration):
```markdown
# Migration Context
- Base URL: http://localhost:3000
- Auth: test user = admin@example.com / secret123
- All POs inherit from BasePage (navigate, scroll_to_bottom)
- Shared fixtures in tests/playwright/conftest.py: login_page, checkout_page
- data-testid attributes use kebab-case: data-testid="submit-btn"
```
Paste this file at the start of every prompt. It costs ~500 tokens and prevents repeated questions.

**3. Split large test files.** If a test file has 30+ tests across multiple features, split the migration into 2–3 prompts grouped by feature. Feed one group at a time with the same PO signatures and context file.

**4. Process bottom-up.** Always migrate in this order: utilities → base classes → page objects → tests.
Never send a test file before its POs are migrated — the signatures you feed must be from the actual migrated PO, not the Selenium version.
