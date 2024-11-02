from tests.ui_tests.test_base import BaseTest

class TestCart(BaseTest):

    def test_add_products_to_cart(self):
        products = ["Prod_1", "Prod_2"]
        for product in products:
            self.search_for_product(product)


