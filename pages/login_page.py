import time

from locators.locators import LoginPageLocators
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def open_login_page(self):
        self.driver.get(self.getBaseUrl() + "/login")


    def is_login_page_visible(self):
        return self.is_visible(LoginPageLocators.EMAIL)

    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL, email)
        self.send_keys(LoginPageLocators.PASSWORD, password)
        self.click(LoginPageLocators.SIGN_IN_BUTTON)
