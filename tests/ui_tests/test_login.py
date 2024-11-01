import pytest
from pages.login_page import LoginPage
from data.test_data import TestData

@pytest.mark.usefixtures("driver_init")
class TestLogin:

    def test_valid_login(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        assert login_page.is_login_successful(), "Login was not successful"

    def test_invalid_login(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(TestData.INVALID_USERNAME, TestData.INVALID_PASSWORD)
        assert login_page.is_login_page(), "Expected login failure, but login was successful"
