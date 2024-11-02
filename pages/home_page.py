from locators.locators import HomePageLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    # Locators

    def __init__(self, driver):
        super().__init__(driver)

    def is_home_page_visible(self):
        return self.is_visible(HomePageLocators.HOME_PAGE_INFO)
