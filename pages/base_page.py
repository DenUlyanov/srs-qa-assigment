import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.locators import HomePageLocators
from utils.config_reader import ConfigReader


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.config_reader = ConfigReader()


    def allow_all_cookies(self):
        # TODO add try mechanism to see if cookies are not accepted
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(HomePageLocators.ALLOW_COOKIES_BUTTON)).click()

    # TODO add try catch mechanism
    def click(self, locator):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def send_keys(self, locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_text(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def is_visible(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return bool(element)
