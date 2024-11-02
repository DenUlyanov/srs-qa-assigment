from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    # This locator is terrible but since I don't have any control over the website I have to use it
    SIGN_IN_BUTTON = (By.XPATH, "//*[@id='root']/div/section[2]/div/div/div[1]/form/div[3]/button")


class HomePageLocators:
    ALLOW_COOKIES_BUTTON = (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    HOME_PAGE_INFO = (By.CSS_SELECTOR, ".HomePageInfo")
