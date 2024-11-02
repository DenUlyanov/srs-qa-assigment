from selenium.webdriver import Keys

from locators.locators import HomePageLocators, CartPageLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    # Locators

    def __init__(self, driver):
        super().__init__(driver)

    def open_cart_page(self):
        self.driver.get(f"{self.get_base_url()}/cart")

    def is_cart_page_visible(self):
        return self.is_visible(CartPageLocators.CART_CONTENT)

    def verify_cart_item_count(self, expected_count):
        cart_rows = self.find_elements(CartPageLocators.CART_ROWS)
        return expected_count == len(cart_rows)

    def is_product_in_cart(self, product_name):
        cart_content = self.find_element(CartPageLocators.CART_CONTENT).text
        return product_name in cart_content, f"Expected product '{product_name}' not found in the cart."
