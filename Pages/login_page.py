from selenium.webdriver.common.by import By

from Config.config import TestData
from Pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    SIGN_IN_BUTTON = (By.XPATH, "//*[@id='root']/div/section[2]/div/div/div[1]/form/div[3]/button")
    ALLOW_COOKIES_BUTTON = (By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(TestData.BASE_URL + "/login")

    def accept_all_cookies(self):
        self.click(self.ALLOW_COOKIES_BUTTON)

    # Page actions
    def is_login_page(self):
        return self.is_visible(self.EMAIL)

    def login(self, email, password):
        self.send_keys(self.EMAIL, email)
        self.send_keys(self.PASSWORD, password)
        self.click(self.SIGN_IN_BUTTON)
