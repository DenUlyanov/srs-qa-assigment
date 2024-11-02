import uuid

from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.ui_tests.test_base import BaseTest


class TestLogin(BaseTest):

    def test_login(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.open_login_page()
        self.loginPage.allow_all_cookies()
        assert self.loginPage.is_login_page_visible()
        self.loginPage.login(
            self.config_reader.get_website_email(),
            self.config_reader.get_website_password()
        )
        self.homePage = HomePage(self.driver)
        assert self.homePage.is_home_page_visible()



    # TODO Add examples of additional test
