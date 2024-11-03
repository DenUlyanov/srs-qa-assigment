from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    # This locator is terrible but since I don't have any control over the website I have to use it
    SIGN_IN_BUTTON = (
        By.XPATH,
        "//*[@id='root']/div/section[2]/div/div/div[1]/form/div[3]/button",
    )


class HomePageLocators:
    ALLOW_COOKIES_BUTTON = (
        By.ID,
        "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll",
    )
    HOME_PAGE_INFO = (By.CSS_SELECTOR, ".HomePageInfo")
    SEARCH_BAR = (By.ID, "search-field")


class SearchResultPageLocators:
    SEARCH_REQUEST_DISPLAY = (By.CSS_SELECTOR, ".CategoryDetails-Description")
    SEARCH_RESULT_COUNTER = (By.CSS_SELECTOR, ".CategoryPage-ItemsCount")
    PRODUCTS_LIST = (By.CSS_SELECTOR, ".ProductListPage")
    EMPTY_PRODUCT_LIST = (By.CSS_SELECTOR, ".ProductList-ProductsMissing")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".AddToCart")


class CartPageLocators:
    CART_CONTENT = (By.CSS_SELECTOR, ".CartPage-Items")
    CART_ROWS = (By.CSS_SELECTOR, ".CartItem_isEditing")
    PROCEED_TO_CHECKOUT = (By.CSS_SELECTOR, ".CartPage-CheckoutButton")


class CheckoutPageLocators:
    EMAIL = (By.ID, "guest_email")
    FIRST_NAME = (By.ID, "firstname")
    LAST_NAME = (By.ID, "lastname")
    STREET = (By.ID, "street0")
    HOUSE = (By.ID, "street1")
    POSTCODE = (By.ID, "postcode")
    PHONE = (By.ID, "telephone")
    PLACE = (By.ID, "city")
    NOTES = (By.ID, "customer_notes")
    PROCEED_TO_BILLING = (By.CSS_SELECTOR, ".CheckoutShipping-Button")
