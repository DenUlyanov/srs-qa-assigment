from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.search_result_page import SearchResultPage
from tests.ui_tests.test_base import BaseTest


class TestCheckout(BaseTest):
    """
       This test verifies that product can be found via search, add to cart and checked out
       Test is not going to pay for the product
    """

    def test_checkout_product(self):
        product = "Rinehart 18-1 3D Target"

        # define all required pages
        search_result_page = SearchResultPage(self.driver)
        cart_page = CartPage(self.driver)
        checkout_page = CheckoutPage(self.driver)

        # find product to check out
        self.search_for_product(product)
        search_result_page.add_product_to_cart()

        # add product to cart
        cart_page.open_cart_page()
        cart_page.is_cart_page_visible()
        assert cart_page.is_product_in_cart(product)
        cart_page.proceed_to_checkout()

        # fill in complete form
        assert checkout_page.is_checkout_page_visible()
        checkout_page.fill_in_checkout_form()

        """ 
        I have decided to stop here since if I proceed to checkout order will be created in the shop backend 
        and I really don't want to mess up their statistics. I also added note in checkout form just in case. 
        
        Many more test for checkout page can be added that cover flow of existing customer, verify field validation, 
        test delivery options and so on.
        """
