import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.locators import HomePageLocators
from utils.config_reader import ConfigReader


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.config_reader = ConfigReader()

    def getBaseUrl(self):
        return self.config_reader.get_website_url()

    def allow_all_cookies(self):
        try:
            allow_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(HomePageLocators.ALLOW_COOKIES_BUTTON)
            )
            if allow_button.is_displayed():
                allow_button.click()
        except (TimeoutException, NoSuchElementException):
            #TODO add proper logs
            print("Allow cookies button not found or not visible.")

    # TODO add try catch mechanism
    def findElement(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    def findElements(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))

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

    # TODO Delete me
    def wait(self):
        time.sleep(5)
