import logging
from selenium.common import ElementNotInteractableException
from selenium.common import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config.config import ConfigReader
from locators.locators import HomePageLocators

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    """
    This is class that contains basic functions to interact with UI
    """

    def __init__(self, driver):
        self.driver = driver
        self.config_reader = ConfigReader()
        self.timeout = self.config_reader.get_website_timeout()

    def get_base_url(self):
        return self.config_reader.get_website_url()

    def allow_all_cookies(self):
        """
        Attempts to click the "Allow Cookies" button if it is present and visible.
        """
        try:
            allow_button = WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_element_located(HomePageLocators.ALLOW_COOKIES_BUTTON)
            )
            if allow_button.is_displayed():
                allow_button.click()
        except (TimeoutException, NoSuchElementException):
            logger.info("Allow cookies button not found or not visible.")

    def find_element(self, locator):
        """
        Finds an element that is visible on the page.
        :param locator: Locator for the element to find.
        :return: The located WebElement, or None if not found.
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_element_located(locator)
            )
        except TimeoutException as e:
            logger.error(
                f"Element with locator {locator} was not found or not visible within the timeout period."
            )
            raise e

    def find_elements(self, locator):
        """
        Finds all elements that are visible on the page.
        :param locator: Locator for the elements to find.
        :return: A list of located WebElements, or an empty list if none are found.
        """
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_all_elements_located(locator)
            )
        except TimeoutException as e:
            logger.error(
                f"Elements with locator {locator} were not found or not visible"
            )
            raise e

    def click(self, locator):
        """
        Clicks on an element that is visible on the page.
        :param locator: Locator for the element to click.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_element_located(locator)
            )
            element.click()
        except TimeoutException:
            logger.error(f"Element with locator {locator} was not found or not visible")
        except ElementClickInterceptedException as e:
            logger.error(
                f"Element with locator {locator} was visible but could not be clicked"
            )
            raise e

    def send_keys(self, locator, text):
        """
        Sends keys to an element that is visible on the page.
        :param locator: Locator for the element to send keys to.
        :param text: The text to send to the element.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_element_located(locator)
            )
            element.send_keys(text)
        except TimeoutException:
            logger.error(f"Element with locator {locator} was not found or not visible")
        except ElementNotInteractableException as e:
            logger.error(
                f"Element with locator {locator} was found but is not interactable"
            )
            raise e

    def get_text(self, locator):
        """
        Gets the text from an element that is visible on the page.
        :param locator: Locator for the element to get text from.
        :return: The text of the element, or None if not found.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return element.text
        except TimeoutException as e:
            logger.error(
                f"Element with locator {locator} was not found or not visible within the timeout period."
            )
            raise e

    def is_visible(self, locator):
        """
        Checks if an element is visible on the page.
        :param locator: Locator for the element to check.
        :return: True if the element is visible, False otherwise.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                ec.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException as e:
            logger.error(
                f"Element with locator {locator} was not visible within the timeout period."
            )
            raise e
