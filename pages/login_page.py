from locators.login_locators import LoginLocators


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://www.europearchery.com/login")

    def is_login_page(self):

        current_url = self.driver.current_url
        assert "/login" in current_url, f"Expected URL to contain '/login', but got {current_url}"

        element = self.driver.find_element(*LoginLocators.USERNAME_INPUT)
        assert element.is_displayed()


    def login(self, username, password):
        self.driver.find_element(*LoginLocators.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*LoginLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginLocators.LOGIN_BUTTON).click()

    def is_login_successful(self):
        current_url = self.driver.current_url
        assert "/my-account/dashboard" in current_url, f"Expected URL to contain '/my-account/dashboard', but got {current_url}"

        element = self.driver.find_element(*LoginLocators.LOGOUT_BUTTON)
        assert element.is_displayed()
