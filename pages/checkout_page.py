from locators.locators import CheckoutPageLocators
from pages.base_page import BasePage
from utils.customer_provider import CustomerGenerator


class CheckoutPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def is_checkout_page_visible(self):
        return self.is_visible(CheckoutPageLocators.PROCEED_TO_BILLING)

    def fill_in_checkout_form(self):
        user = CustomerGenerator.create_test_user()

        self.send_keys(CheckoutPageLocators.EMAIL, user["email"])
        self.send_keys(CheckoutPageLocators.FIRST_NAME, user["first_name"])
        self.send_keys(CheckoutPageLocators.LAST_NAME, user["last_name"])
        self.send_keys(CheckoutPageLocators.PHONE, user["phone"])
        self.send_keys(CheckoutPageLocators.STREET, user["street_name"])
        self.send_keys(CheckoutPageLocators.HOUSE, user["house_number"])
        self.send_keys(CheckoutPageLocators.POSTCODE, user["postcode"])
        self.send_keys(CheckoutPageLocators.PLACE, user["place"])
        self.send_keys(CheckoutPageLocators.NOTES, user["message"])
