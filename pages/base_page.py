import time

from selenium.common import ElementNotInteractableException
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.locators import HomePageLocators
from utils.config_reader import ConfigReader


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.config_reader = ConfigReader()

    def get_base_url(self):
        return self.config_reader.get_website_url()

    def allow_all_cookies(self):
        """
        Attempts to click the "Allow Cookies" button if it is present and visible.
        """
        try:
            allow_button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(HomePageLocators.ALLOW_COOKIES_BUTTON)
            )
            if allow_button.is_displayed():
                allow_button.click()
        except (TimeoutException, NoSuchElementException):
            # TODO add proper logs
            print("Allow cookies button not found or not visible.")

    def find_element(self, locator):
        """
        Finds an element that is visible on the page.
        :param locator: Locator for the element to find.
        :return: The located WebElement, or None if not found.
        """
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            # TODO add proper logs
            print(f"Element with locator {locator} was not found or not visible within the timeout period.")
            return None

    def find_elements(self, locator):
        """
        Finds all elements that are visible on the page.
        :param locator: Locator for the elements to find.
        :return: A list of located WebElements, or an empty list if none are found.
        """
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            # TODO add proper logs
            print(f"Elements with locator {locator} were not found or not visible within the timeout period.")
            return []

    def click(self, locator):
        """
        Clicks on an element that is visible on the page.
        :param locator: Locator for the element to click.
        """
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
            element.click()
        except TimeoutException:
            # TODO add proper logs
            print(f"Element with locator {locator} was not found or not visible within the timeout period.")
        except ElementClickInterceptedException:
            # TODO add proper logs
            print(
                f"Element with locator {locator} was visible but could not be clicked, possibly due to overlay issues.")

    def send_keys(self, locator, text):
        """
        Sends keys to an element that is visible on the page.
        :param locator: Locator for the element to send keys to.
        :param text: The text to send to the element.
        """
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
            element.send_keys(text)
        except TimeoutException:
            # TODO add proper logs
            print(f"Element with locator {locator} was not found or not visible within the timeout period.")
        except ElementNotInteractableException:
            # TODO add proper logs
            print(
                f"Element with locator {locator} was found but is not interactable, possibly due to being disabled or not ready.")

    def get_text(self, locator):
        """
        Gets the text from an element that is visible on the page.
        :param locator: Locator for the element to get text from.
        :return: The text of the element, or None if not found.
        """
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
            return element.text
        except TimeoutException:
            # TODO add proper logs
            print(f"Element with locator {locator} was not found or not visible within the timeout period.")
            return None

    def is_visible(self, locator):
        """
        Checks if an element is visible on the page.
        :param locator: Locator for the element to check.
        :return: True if the element is visible, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            # TODO add proper logs
            print(f"Element with locator {locator} was not visible within the timeout period.")
            return False

    def wait(self, seconds=5):
        """
        Waits for a specified number of seconds.
        :param seconds: Number of seconds to wait (default is 5 seconds).
        """
        time.sleep(seconds)  # Consider using explicit waits instead of fixed sleeps where possible.
