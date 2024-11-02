import pytest

from pages.home_page import HomePage
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
        self.search_for_product(search_request)
        self.searchResultPage = SearchResultPage(self.driver)
        assert self.searchResultPage.is_search_result_page_visible()
        assert self.searchResultPage.are_search_results_for(search_request)
        assert self.searchResultPage.amount_of_products_found(expected_amount)

    def test_search_negative_result(self):
        search_request = "Volkswagen Golf"
        self.search_for_product(search_request)
        self.searchResultPage = SearchResultPage(self.driver)
        assert self.searchResultPage.is_search_result_page_visible()
        assert self.searchResultPage.are_search_results_for(search_request)
        assert self.searchResultPage.no_products_founds()

    def search_for_product(self, search_request):
        self.homePage = HomePage(self.driver)
        self.homePage.open_home_page()
        self.homePage.allow_all_cookies()
        assert self.homePage.is_home_page_visible()
        self.homePage.search(search_request)
