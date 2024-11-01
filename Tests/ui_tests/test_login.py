from Config.config import TestData
from Pages.login_page import LoginPage
from Tests.ui_tests.test_base import BaseTest


class TestLogin(BaseTest):

    def test_verify_login_page(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.accept_all_cookies()
        assert self.loginPage.is_login_page()

    def test_login(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.accept_all_cookies()
        self.loginPage.login(TestData.EMAIL, TestData.PASSWORD)
