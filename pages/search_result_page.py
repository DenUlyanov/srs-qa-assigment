import re

from locators.locators import SearchResultPageLocators
from pages.base_page import BasePage


class SearchResultPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def is_search_result_page_visible(self):
        return self.is_visible(SearchResultPageLocators.SEARCH_REQUEST_DISPLAY)

    def are_search_results_for(self, search_request):
        return search_request.lower() in self.get_text(SearchResultPageLocators.SEARCH_REQUEST_DISPLAY).lower()

    def amount_of_products_found(self, expected_count):
        product_count_string = self.get_text(SearchResultPageLocators.SEARCH_RESULT_COUNTER).lower()
        match = re.search(r'\d+', product_count_string)
        if not match:
            raise ValueError("No item count found in the provided text")
        return int(match.group()) == expected_count

    def no_products_founds(self):
        return self.is_visible(SearchResultPageLocators.EMPTY_PRODUCT_LIST)

    def add_product_to_cart(self):
        self.click(SearchResultPageLocators.ADD_TO_CART_BUTTON)
