import uuid

from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.ui_tests.test_base import BaseTest


class TestLogin(BaseTest):

    def test_verify_login_page_visible(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.open_login_page()
        self.loginPage.allow_all_cookies()
        assert self.loginPage.is_login_page_visible()

    def test_positive_login(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.open_login_page()
        self.loginPage.allow_all_cookies()
        self.loginPage.login(
            self.config_reader.get_website_email(),
            self.config_reader.get_website_password()
        )
        self.homePage = HomePage(self.driver)
        assert self.homePage.is_home_page_visible()

    def test_negative_login(self):
        self.loginPage = LoginPage(self.driver)
        self.loginPage.open_login_page()
        self.loginPage.allow_all_cookies()
        # generate random string and use it for email and password
        random_customer_name = str(uuid.uuid4())
        self.loginPage.login(
            f"{random_customer_name}@test.com",
            random_customer_name
        )
        # verify login page is still visible
        assert self.loginPage.is_login_page_visible()
