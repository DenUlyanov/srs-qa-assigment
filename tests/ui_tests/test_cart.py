from pages.cart_page import CartPage
from pages.search_result_page import SearchResultPage
from tests.ui_tests.test_base import BaseTest


class TestCart(BaseTest):
    """
    This test verifies that multiple products can be added to the cart and
    verifies that cart contains correct amount of correct products
    """

    def test_add_products_to_cart(self):
        products = [
            "OMP Archery Versa-Cradle Bow Vise Micro Tune",
            "Easton Archery Omni Tool by Fix It Sticks",
            "Hoyt Bow Square",
        ]

        search_result_page = SearchResultPage(self.driver)
        cart_page = CartPage(self.driver)

        for product in products:
            self.search_for_product(product)
            search_result_page.add_product_to_cart()

        cart_page.open_cart_page()
        cart_page.is_cart_page_visible()

        # Verify correct amount of items is in the cart
        assert cart_page.verify_cart_item_count(len(products))

        # Verify all products are in the cart
        for product in products:
            assert cart_page.is_product_in_cart(product)
