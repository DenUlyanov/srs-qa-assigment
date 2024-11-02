from tests.ui_tests.test_base import BaseTest

class TestCart(BaseTest):

    def test_add_products_to_cart(self):
        self.search_for_product("TEST")
