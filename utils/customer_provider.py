import random
import string


class CustomerGenerator:
    """
    This is util simple util class that provides random test customer
    It is extremely simple and has a lot of potential for improvements
    Temp random email can be used, different address information can be provided
    and so on but for our simple test this should suffice
    """

    # static data
    STATIC_EMAIL = 'fakeemail@test.com'
    STATIC_STREET_NAME = 'Teststraat'
    STATIC_HOUSE_NUMBER = '123'
    STATIC_POSTCODE = '1234AB'
    STATIC_PLACE = '1234AB'
    STATIC_MESSAGE = (
        "This is a test order, I have used your website for a test assignment I am working on.\n"
        "Hope it's not going to affect your statistics to much, I am sorry if it does.\n"
        "You can filter all related activities by the email fakeemail@test.com."
    )

    # dynamic data
    @staticmethod
    def generate_first_name():
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6)).capitalize()

    @staticmethod
    def generate_last_name():
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8)).capitalize()

    @staticmethod
    def generate_dutch_phone():
        return '+31 6 ' + ''.join(random.choices(string.digits, k=8))

    @staticmethod
    def create_test_user():
        return {
            'first_name': CustomerGenerator.generate_first_name(),
            'last_name': CustomerGenerator.generate_last_name(),
            'phone': CustomerGenerator.generate_dutch_phone(),
            'email': CustomerGenerator.STATIC_EMAIL,
            'street_name': CustomerGenerator.STATIC_STREET_NAME,
            'house_number': CustomerGenerator.STATIC_HOUSE_NUMBER,
            'postcode': CustomerGenerator.STATIC_POSTCODE,
            'place': CustomerGenerator.STATIC_PLACE,
            'message': CustomerGenerator.STATIC_MESSAGE
        }
