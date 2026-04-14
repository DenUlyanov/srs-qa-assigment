# Migration Plan: Selenium → Playwright (srs-qa-assigment UI Tests)

This document contains step-by-step instructions to migrate all UI tests in this project
from pytest-selenium to pytest-playwright using Claude Code as the AI assistant.

**Scope:** 5 Page Objects (+ BasePage), 4 test files, 5 tests, 24 locators  
**AI tool:** Claude Code with `rules/CLAUDE.md` loaded automatically  
**Target location:** `tests/playwright/` (Selenium tests stay untouched in `tests/ui_tests/`)

---

## Before You Start

### Install pytest-playwright

```bash
pip install pytest-playwright
playwright install chromium
```

### Add to pyproject.toml

```toml
[tool.poetry.dependencies]
pytest-playwright = ">=0.4.0"
```

### Create the target directory structure

```
tests/
├── ui_tests/          # Selenium — DO NOT TOUCH
└── playwright/
    ├── __init__.py
    ├── conftest.py    # Playwright fixtures (created in Phase 0)
    └── pages/
        ├── __init__.py
        └── ...        # Migrated Page Objects go here
```

---

## Phase 0 — Shared Infrastructure (do first, sequential)

### 0.1 — Create `tests/playwright/conftest.py`

Paste the following prompt into Claude Code:

```
Read config/config.py and config/config.yaml.
Create tests/playwright/conftest.py with the following:

1. A `base_url` fixture (scope="session") that returns the website URL from config/config.yaml
2. A `login_page` fixture (scope="function") that accepts `page` and `base_url`, instantiates LoginPage, and returns it
3. A `home_page` fixture (scope="function") that accepts `page` and `base_url`, instantiates HomePage, and returns it
4. A `search_result_page` fixture that accepts `page`, instantiates SearchResultPage, returns it
5. A `cart_page` fixture that accepts `page` and `base_url`, instantiates CartPage, returns it
6. A `checkout_page` fixture that accepts `page`, instantiates CheckoutPage, returns it

All Page Object imports come from tests/playwright/pages/.
Do not import from selenium or the old pages/ directory.
Follow rules/CLAUDE.md exactly.
```

### 0.2 — Migrate `pages/base_page.py` → `tests/playwright/pages/base_page.py`

Paste into Claude Code:

```
Migrate pages/base_page.py to a Playwright equivalent at tests/playwright/pages/base_page.py.
Follow rules/CLAUDE.md exactly.

Key notes for this specific file:
- BasePage.__init__ takes `driver` → replace with `page: Page`
- Remove all WebDriverWait, expected_conditions, and timeout logic — Playwright auto-waits
- find_element(locator) → remove entirely; callers will use self._page.get_by_* directly
- find_elements(locator) → remove entirely; callers will use self._page.locator().all()
- click(locator) → remove; callers call locator.click() directly
- send_keys(locator, text) → remove; callers call locator.fill() directly
- get_text(locator) → remove; callers call locator.inner_text() directly
- is_visible(locator) → remove; callers use expect(locator).to_be_visible() in tests
- allow_all_cookies() → keep, but rewrite: self._page.get_by_role("button", name="Allow all cookies") or similar; wrap in try/except using locator.is_visible() check instead of NoSuchElementException
- get_base_url() → keep, read from config/config.yaml using ConfigReader
- Remove all selenium imports
- Keep ConfigReader dependency (it has no selenium imports)
```

---

## Phase 1 — Page Objects (run all in parallel after Phase 0)

For each Page Object below, open a new Claude Code session with `rules/CLAUDE.md` loaded,
then paste the prompt. All 5 can be run simultaneously.

---

### 1.1 — Migrate `pages/login_page.py`

```
Migrate pages/login_page.py to tests/playwright/pages/login_page.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of pages/login_page.py]

Already-migrated BasePage signature:
# BasePage (tests/playwright/pages/base_page.py) — ALREADY MIGRATED
class BasePage:
    def __init__(self, page: Page) -> None: ...
    def get_base_url(self) -> str: ...
    def allow_all_cookies(self) -> None: ...

Locator mapping guidance:
- LoginPageLocators.EMAIL (By.ID, "email") → page.get_by_label("Email") or page.locator("#email")
- LoginPageLocators.PASSWORD (By.ID, "password") → page.get_by_label("Password") or page.locator("#password")
- LoginPageLocators.SIGN_IN_BUTTON (By.XPATH, "//*[@id='root']/...") → page.get_by_role("button", name="Sign in")
  NOTE: The original XPath is explicitly marked "terrible" in the source — use get_by_role instead.
```

---

### 1.2 — Migrate `pages/home_page.py`

```
Migrate pages/home_page.py to tests/playwright/pages/home_page.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of pages/home_page.py]

Already-migrated BasePage signature:
# BasePage (tests/playwright/pages/base_page.py) — ALREADY MIGRATED
class BasePage:
    def __init__(self, page: Page) -> None: ...
    def get_base_url(self) -> str: ...
    def allow_all_cookies(self) -> None: ...

Locator mapping guidance:
- HomePageLocators.HOME_PAGE_INFO (By.ID, "...") → page.get_by_role or page.locator("#...")
- HomePageLocators.SEARCH_BAR (By.ID, "...") → page.get_by_role("searchbox") or page.get_by_placeholder("Search")
- HomePageLocators.ALLOW_COOKIES_BUTTON → already handled in BasePage.allow_all_cookies()
- search() method uses Keys.ENTER → replace with locator.press("Enter")
```

---

### 1.3 — Migrate `pages/search_result_page.py`

```
Migrate pages/search_result_page.py to tests/playwright/pages/search_result_page.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of pages/search_result_page.py]

Already-migrated BasePage signature:
# BasePage (tests/playwright/pages/base_page.py) — ALREADY MIGRATED
class BasePage:
    def __init__(self, page: Page) -> None: ...
    def get_base_url(self) -> str: ...
    def allow_all_cookies(self) -> None: ...

Locator mapping guidance (all CSS_SELECTOR):
- SearchResultPageLocators.SEARCH_REQUEST_DISPLAY → page.locator(".search-request-display") or semantic equivalent
- SearchResultPageLocators.SEARCH_RESULT_COUNTER → page.locator(".search-result-counter")
- SearchResultPageLocators.PRODUCTS_LIST → page.locator(".products-list")
- SearchResultPageLocators.EMPTY_PRODUCT_LIST → page.locator(".empty-product-list")
- SearchResultPageLocators.ADD_TO_CART_BUTTON → page.get_by_role("button", name="Add to cart")

Method notes:
- amount_of_products_found() uses regex to parse count text — keep the regex, just change how you get the text
- are_search_results_for() checks text content — return a Locator, let the test use expect().to_contain_text()
- no_products_found() → return a Locator, let the test use expect().to_be_visible()
- add_product_to_cart() → locator.click() directly, no wait needed
```

---

### 1.4 — Migrate `pages/cart_page.py`

```
Migrate pages/cart_page.py to tests/playwright/pages/cart_page.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of pages/cart_page.py]

Already-migrated BasePage signature:
# BasePage (tests/playwright/pages/base_page.py) — ALREADY MIGRATED
class BasePage:
    def __init__(self, page: Page) -> None: ...
    def get_base_url(self) -> str: ...
    def allow_all_cookies(self) -> None: ...

Locator mapping guidance (all CSS_SELECTOR):
- CartPageLocators.CART_CONTENT → page.locator(".cart-content")
- CartPageLocators.CART_ROWS → page.locator(".cart-rows")  [used for count]
- CartPageLocators.PROCEED_TO_CHECKOUT → page.get_by_role("button", name="Proceed to checkout")

Method notes:
- verify_cart_item_count() uses len(find_elements(...)) → use locator.count()
- is_product_in_cart() currently returns a tuple with assertion message — refactor to return a Locator
  so the test can use expect(locator).to_contain_text(product_name)
- proceed_to_checkout() → locator.click() directly
```

---

### 1.5 — Migrate `pages/checkout_page.py`

```
Migrate pages/checkout_page.py to tests/playwright/pages/checkout_page.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of pages/checkout_page.py]

Already-migrated BasePage signature:
# BasePage (tests/playwright/pages/base_page.py) — ALREADY MIGRATED
class BasePage:
    def __init__(self, page: Page) -> None: ...
    def get_base_url(self) -> str: ...
    def allow_all_cookies(self) -> None: ...

Locator mapping guidance (all By.ID):
- CheckoutPageLocators.EMAIL → page.locator("#email") or page.get_by_label("Email")
- CheckoutPageLocators.FIRST_NAME → page.get_by_label("First name")
- CheckoutPageLocators.LAST_NAME → page.get_by_label("Last name")
- CheckoutPageLocators.STREET → page.get_by_label("Street")
- CheckoutPageLocators.HOUSE → page.get_by_label("House number")
- CheckoutPageLocators.POSTCODE → page.get_by_label("Postcode")
- CheckoutPageLocators.PHONE → page.get_by_label("Phone")
- CheckoutPageLocators.PLACE → page.get_by_label("Place")
- CheckoutPageLocators.NOTES → page.get_by_label("Notes") or page.get_by_placeholder("Notes")
- CheckoutPageLocators.PROCEED_TO_BILLING → page.get_by_role("button", name="Proceed to billing")

Method notes:
- fill_in_checkout_form() uses CustomerGenerator — keep the dependency, it has no selenium imports
- Replace each send_keys call with locator.fill(value)
```

---

## Phase 2 — Test Files (run in parallel after Phase 1)

For each test file, open a new Claude Code session with `rules/CLAUDE.md` loaded.

---

### 2.1 — Migrate `tests/ui_tests/test_login.py`

```
Migrate tests/ui_tests/test_login.py to tests/playwright/test_login.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of tests/ui_tests/test_login.py]

Migrated Page Object signatures:
# LoginPage (tests/playwright/pages/login_page.py) — ALREADY MIGRATED
class LoginPage(BasePage):
    def __init__(self, page: Page) -> None: ...
    def open_login_page(self) -> None: ...
    def is_login_page_visible(self) -> Locator: ...
    def login(self, email: str, password: str) -> None: ...

# HomePage (tests/playwright/pages/home_page.py) — ALREADY MIGRATED
class HomePage(BasePage):
    def __init__(self, page: Page) -> None: ...
    def open_home_page(self) -> None: ...
    def is_home_page_visible(self) -> Locator: ...

Migration notes:
- Remove unittest.TestCase and BaseTest inheritance
- Remove @pytest.mark.usefixtures("init_driver")
- Use login_page and home_page fixtures from tests/playwright/conftest.py
- Credentials come from ConfigReader (no change needed)
- self.assertTrue(x.is_displayed()) → expect(locator).to_be_visible()
```

---

### 2.2 — Migrate `tests/ui_tests/test_search.py`

```
Migrate tests/ui_tests/test_search.py to tests/playwright/test_search.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of tests/ui_tests/test_search.py]

Migrated Page Object signatures:
# HomePage (tests/playwright/pages/home_page.py) — ALREADY MIGRATED
class HomePage(BasePage):
    def __init__(self, page: Page) -> None: ...
    def open_home_page(self) -> None: ...
    def allow_all_cookies(self) -> None: ...
    def is_home_page_visible(self) -> Locator: ...
    def search(self, search_parameter: str) -> None: ...

# SearchResultPage (tests/playwright/pages/search_result_page.py) — ALREADY MIGRATED
class SearchResultPage(BasePage):
    def __init__(self, page: Page) -> None: ...
    def is_search_result_page_visible(self) -> Locator: ...
    def are_search_results_for(self, search_request: str) -> Locator: ...
    def amount_of_products_found(self, expected_count: int) -> bool: ...
    def no_products_found(self) -> Locator: ...

Migration notes:
- Keep @pytest.mark.parametrize — it works the same in pytest-playwright
- Replace BaseTest.search_for_product() helper with inline fixture calls
- self.assertEqual / self.assertTrue → expect(locator).to_* assertions
```

---

### 2.3 — Migrate `tests/ui_tests/test_cart.py`

```
Migrate tests/ui_tests/test_cart.py to tests/playwright/test_cart.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of tests/ui_tests/test_cart.py]

Migrated Page Object signatures:
# HomePage — (see 2.2 signatures above)
# SearchResultPage — (see 2.2 signatures above)

# CartPage (tests/playwright/pages/cart_page.py) — ALREADY MIGRATED
class CartPage(BasePage):
    def __init__(self, page: Page) -> None: ...
    def open_cart_page(self) -> None: ...
    def is_cart_page_visible(self) -> Locator: ...
    def verify_cart_item_count(self, expected_count: int) -> bool: ...
    def is_product_in_cart(self, product_name: str) -> Locator: ...
    def proceed_to_checkout(self) -> None: ...

Migration notes:
- test_add_products_to_cart adds 3 products in sequence — each add_product_to_cart() click
  may trigger a cart overlay/confirmation; use expect(locator).to_be_visible() to wait for it
  before proceeding to the next product
- is_product_in_cart now returns a Locator → use expect(locator).to_contain_text(product_name)
```

---

### 2.4 — Migrate `tests/ui_tests/test_checkout.py`

```
Migrate tests/ui_tests/test_checkout.py to tests/playwright/test_checkout.py.
Follow rules/CLAUDE.md exactly.

Source file content:
[paste full contents of tests/ui_tests/test_checkout.py]

Migrated Page Object signatures:
# HomePage — (see 2.2 signatures above)
# SearchResultPage — (see 2.2 signatures above)
# CartPage — (see 2.3 signatures above)

# CheckoutPage (tests/playwright/pages/checkout_page.py) — ALREADY MIGRATED
class CheckoutPage(BasePage):
    def __init__(self, page: Page) -> None: ...
    def is_checkout_page_visible(self) -> Locator: ...
    def fill_in_checkout_form(self) -> None: ...

Migration notes:
- CustomerGenerator (data/customer.py) has no selenium imports — import it directly, no changes
- The test stops before payment — no additional handling needed
```

---

## Phase 3 — Verification (sequential, after all migrations)

Run the anti-pattern checker across all migrated files:

```bash
python ai-migration-assessment/verification/verify_migration.py tests/playwright/
```

All files must pass before opening a PR. Fix any FAIL findings, review WARN findings.

---

## Phase 4 — CI Update

Add a new job to `.github/workflows/main.yml` to run Playwright tests alongside Selenium:

```yaml
playwright-tests:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Install dependencies
      run: |
        pip install pytest pytest-playwright pytest-html
        playwright install --with-deps chromium

    - name: Verify migration
      run: python ai-migration-assessment/verification/verify_migration.py tests/playwright/

    - name: Run Playwright UI tests
      run: |
        pytest tests/playwright/ \
          --browser chromium \
          --html=reports/playwright_report.html \
          --self-contained-html

    - name: Upload Playwright report
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: playwright-report
        path: reports/playwright_report.html
```

---

## Locator Cheat Sheet (project-specific)

Based on the actual locators in this project:

| Original (Selenium) | Playwright equivalent |
|---------------------|-----------------------|
| `By.ID, "email"` | `page.get_by_label("Email")` or `page.locator("#email")` |
| `By.ID, "password"` | `page.get_by_label("Password")` or `page.locator("#password")` |
| `By.XPATH, "//*[@id='root']/...button"` | `page.get_by_role("button", name="Sign in")` |
| `By.CSS_SELECTOR, ".search-bar"` | `page.get_by_role("searchbox")` or `page.locator(".search-bar")` |
| `By.CSS_SELECTOR, ".product-list"` | `page.locator(".product-list")` |
| `By.CSS_SELECTOR, ".cart-content"` | `page.locator(".cart-content")` |
| `By.ID, "first-name"` | `page.get_by_label("First name")` |
| `Keys.ENTER` | `locator.press("Enter")` |
| `len(find_elements(locator))` | `locator.count()` |
| `element.text` | `locator.inner_text()` |
| `element.is_displayed()` | `expect(locator).to_be_visible()` |
| `WebDriverWait(driver, 10).until(...)` | delete — Playwright auto-waits |
| `time.sleep(x)` | delete |

---

## Checklist

- [ ] Phase 0: `conftest.py` + `base_page.py` created
- [ ] Phase 1.1: `login_page.py` migrated
- [ ] Phase 1.2: `home_page.py` migrated
- [ ] Phase 1.3: `search_result_page.py` migrated
- [ ] Phase 1.4: `cart_page.py` migrated
- [ ] Phase 1.5: `checkout_page.py` migrated
- [ ] Phase 2.1: `test_login.py` migrated
- [ ] Phase 2.2: `test_search.py` migrated
- [ ] Phase 2.3: `test_cart.py` migrated
- [ ] Phase 2.4: `test_checkout.py` migrated
- [ ] Phase 3: `verify_migration.py` passes with no FAILs
- [ ] Phase 4: CI updated and green
