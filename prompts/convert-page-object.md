# Prompt: Convert Selenium Page Object → Playwright Page Object

## Role

You are migrating a Python Selenium Page Object to a Playwright equivalent.
Follow `rules/CLAUDE.md` exactly. Every rule there is a hard constraint.

---

## Input

Paste the full Selenium Page Object source below:

```python
{{SELENIUM_PAGE_OBJECT_SOURCE}}
```

---

## Conversion Instructions

Work through these steps in order. Do not skip any step.

### Step 1 — Imports
- Remove all `selenium` imports (`from selenium...`, `import selenium...`).
- Add `from playwright.sync_api import Page` at the top.
- Keep any non-selenium imports (e.g., `re`, `typing`, project utilities).

### Step 2 — Constructor
- Replace `self.driver: WebDriver` with `self._page: Page`.
- Remove any `WebDriverWait` or `expected_conditions` instance variables.
- Example:
  ```python
  # BEFORE
  def __init__(self, driver: WebDriver) -> None:
      self.driver = driver
      self.wait = WebDriverWait(driver, 10)

  # AFTER
  def __init__(self, page: Page) -> None:
      self._page = page
  ```

### Step 3 — Locators
For every `find_element` / `find_elements` call, apply the locator priority chain from `rules/CLAUDE.md`:
1. `self._page.get_by_role("...", name="...")`
2. `self._page.get_by_label("...")`
3. `self._page.get_by_placeholder("...")`
4. `self._page.get_by_text("...")`
5. `self._page.get_by_title("...")`
6. `self._page.get_by_test_id("...")`
7. `self._page.locator("css=...")`
8. `self._page.locator("xpath=...")` + `# TODO: replace XPath`

**Do not** keep `By.ID`, `By.CSS_SELECTOR`, `By.XPATH`, `By.CLASS_NAME`, `By.NAME`, `By.TAG_NAME`.
Map them:
- `By.ID, "x"` → `page.locator("#x")` (or semantic if possible)
- `By.CLASS_NAME, "x"` → `page.locator(".x")`
- `By.CSS_SELECTOR, "x"` → `page.locator("x")`
- `By.NAME, "x"` → `page.locator("[name='x']")`
- `By.XPATH, "x"` → `page.locator("x")` + `# TODO: replace XPath`

### Step 4 — Remove All Explicit Waits
- Delete every `WebDriverWait(...).until(...)` call entirely. Playwright auto-waits.
- Delete `time.sleep(...)` calls entirely.
- Delete `self.wait.until(...)` calls entirely.
- Do **not** replace them with `page.wait_for_selector()` unless the element is genuinely dynamic
  and the locator alone is insufficient (extremely rare).

### Step 5 — Element Interactions
| Selenium | Playwright |
|----------|------------|
| `element.click()` | `locator.click()` |
| `element.send_keys("text")` | `locator.fill("text")` |
| `element.send_keys(Keys.ENTER)` | `locator.press("Enter")` |
| `element.clear()` | `locator.clear()` |
| `element.text` | `locator.inner_text()` |
| `element.get_attribute("x")` | `locator.get_attribute("x")` |
| `element.is_displayed()` | `locator.is_visible()` |
| `element.is_enabled()` | `locator.is_enabled()` |
| `Select(el).select_by_visible_text(x)` | `locator.select_option(label=x)` |
| `driver.execute_script("...", el)` | `self._page.evaluate("...", locator)` |

### Step 6 — Navigation
- `self.driver.get(url)` → `self._page.goto(url)`
- `self.driver.back()` → `self._page.go_back()`
- `self.driver.refresh()` → `self._page.reload()`

### Step 7 — Return Types
- Methods that returned `WebElement` should now return a `Locator`.
- Import `from playwright.sync_api import Page, Locator` if returning locators.
- Keep method signatures identical (same name, same parameters).

### Step 8 — Assertions
- **Do not** include `assert` statements in the Page Object.
  Page Objects expose locators or values; assertions belong in tests.
- If the original PO had assertions inside it, move the assert logic to the return value:
  ```python
  # BEFORE (bad — assert in PO)
  def verify_logged_in(self):
      assert self.driver.find_element(By.ID, "dashboard").is_displayed()

  # AFTER (return locator, let test assert)
  def dashboard_panel(self) -> Locator:
      return self._page.get_by_role("main", name="Dashboard")
  ```

### Step 9 — Final Check
Before outputting, verify:
- [ ] No `selenium` imports remain
- [ ] No `WebDriverWait` or `expected_conditions` remain
- [ ] No `time.sleep()` remain
- [ ] No `By.*` locator constants remain
- [ ] All XPath locators have `# TODO: replace XPath`
- [ ] Method names are unchanged from the original
- [ ] `self._page` is used consistently (not `self.driver`)

---

## Output Format

Output **only** the migrated Python file. No explanations, no markdown wrapper.
Then output a JSON manifest on a new line after a `# ---MANIFEST---` comment:

```json
{
  "source": "tests/selenium/pages/login_page.py",
  "output": "tests/playwright/pages/login_page.py",
  "public_methods": ["navigate", "login", "error_message"],
  "xpath_todos": 0,
  "warnings": []
}
```

---

## Before / After Example

### BEFORE — `tests/selenium/pages/login_page.py`

```python
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    URL = "/login"

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self) -> None:
        self.driver.get(self.URL)

    def login(self, username: str, password: str) -> None:
        username_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(1)  # wait for redirect

    def get_error_message(self) -> str:
        error = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-msg"))
        )
        return error.text

    def is_logged_in(self) -> bool:
        try:
            self.driver.find_element(By.ID, "user-avatar")
            return True
        except Exception:
            return False
```

### AFTER — `tests/playwright/pages/login_page.py`

```python
from playwright.sync_api import Page, Locator


class LoginPage:
    URL = "/login"

    def __init__(self, page: Page) -> None:
        self._page = page

    def navigate(self) -> None:
        self._page.goto(self.URL)

    def login(self, username: str, password: str) -> None:
        self._page.get_by_label("Username").fill(username)
        self._page.get_by_label("Password").fill(password)
        self._page.get_by_role("button", name="Log in").click()
        # No sleep needed — Playwright waits for navigation automatically

    def error_message(self) -> Locator:
        # Renamed from get_error_message to return a Locator (let test assert)
        return self._page.get_by_role("alert")

    def user_avatar(self) -> Locator:
        # Renamed from is_logged_in — test calls expect(po.user_avatar()).to_be_visible()
        return self._page.get_by_role("img", name="User avatar")
```

**What changed and why:**
- `WebDriverWait` + `EC.element_to_be_clickable` → deleted. Playwright auto-waits before every interaction.
- `By.ID, "username"` → `get_by_label("Username")` — semantic locator preferred.
- `By.CSS_SELECTOR, "button[type='submit']"` → `get_by_role("button", name="Log in")` — role locator preferred.
- `By.CLASS_NAME, "error-msg"` → `get_by_role("alert")` — role locator preferred; falls back to `locator(".error-msg")` only if no ARIA role is set.
- `time.sleep(1)` → deleted entirely.
- `get_error_message()` now returns a `Locator` instead of a `str` — keeps assertions in tests, not POs.
- `is_logged_in()` → `user_avatar()` returning a `Locator` — tests use `expect(po.user_avatar()).to_be_visible()`.

---

## Context Limit Strategy

When this Page Object imports shared utilities or base classes, include only their **signatures**, not full source:

```python
# BasePage (tests/playwright/pages/base_page.py) — ALREADY MIGRATED
class BasePage:
    def __init__(self, page: Page) -> None: ...
    def wait_for_page_load(self) -> None: ...
    def scroll_to_bottom(self) -> None: ...
```

Paste this signature block at the top of `{{SELENIUM_PAGE_OBJECT_SOURCE}}` before sending.
This keeps even large dependency chains well under the 100K token limit.
