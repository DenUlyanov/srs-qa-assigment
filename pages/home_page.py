from selenium.webdriver import Keys

from locators.locators import HomePageLocators
from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def open_home_page(self):
        self.driver.get(self.get_base_url())

    def is_home_page_visible(self):
        return self.is_visible(HomePageLocators.HOME_PAGE_INFO)

    def search(self, search_parameter):
        self.send_keys(HomePageLocators.SEARCH_BAR, search_parameter)
        self.find_element(HomePageLocators.SEARCH_BAR).send_keys(Keys.ENTER)
