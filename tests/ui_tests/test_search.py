import pytest

from pages.search_result_page import SearchResultPage
from tests.ui_tests.test_base import BaseTest


class TestSearch(BaseTest):

    @pytest.mark.parametrize(
        "search_request, expected_amount",
        [
            ("Fletching Jig Phoenix", 1),
            ("Compound bow", 283),
        ]
    )
    def test_search(self, search_request, expected_amount):
        """
        Tests that searching for a product returns the expected number of results.
        :param search_request: The product to search for.
        :param expected_amount: The expected number of products found.
        """
        self.search_for_product(search_request)
        search_result_page = SearchResultPage(self.driver)
        assert search_result_page.is_search_result_page_visible(), "Search result page is not visible."
        assert search_result_page.are_search_results_for(
            search_request), f"Search results are not for '{search_request}'."
        assert search_result_page.amount_of_products_found(
            expected_amount), f"Expected {expected_amount} products, but found different number."

    def test_search_negative_result(self):
        """
        Tests that searching for a non-existent product returns no results.
        """
        search_request = "Volkswagen Golf"
        self.search_for_product(search_request)
        search_result_page = SearchResultPage(self.driver)
        assert search_result_page.is_search_result_page_visible(), "Search result page is not visible."
        assert search_result_page.are_search_results_for(
            search_request), f"Search results are not for '{search_request}'."
        assert search_result_page.no_products_founds(), "Expected no products to be found, but some were found."
