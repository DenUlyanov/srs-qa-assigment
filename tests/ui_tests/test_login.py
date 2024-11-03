from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.ui_tests.test_base import BaseTest


class TestLogin(BaseTest):

    def test_login(self):
        """Test the login functionality and verify the home page is visible after login."""
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)

        login_page.open_login_page()
        login_page.allow_all_cookies()
        assert login_page.is_login_page_visible(), "Login page is not visible."

        login_page.login(
            self.config_reader.get_website_email(),
            self.config_reader.get_website_password(),
        )

        assert home_page.is_home_page_visible(), "Home page is not visible after login."
