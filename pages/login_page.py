from selenium.webdriver.common.by import By

from config.config import TestData
from pages.base_page import BasePage
from locators.locators import LoginPageLocators


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def open_login_page(self, base_url):
        self.driver.get(TestData.BASE_URL + "/login")

    def is_login_page_visible(self):
        return self.is_visible(LoginPageLocators.EMAIL)

    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL, email)
        self.send_keys(LoginPageLocators.PASSWORD, password)
        self.click(LoginPageLocators.SIGN_IN_BUTTON)

