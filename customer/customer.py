import random
import string
from dataclasses import dataclass, field


@dataclass
class TestUser:
    first_name: str = field(default_factory=lambda: ''.join(
        random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6)).capitalize())
    last_name: str = field(default_factory=lambda: ''.join(
        random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8)).capitalize())
    phone: str = field(default_factory=lambda: '+31 6 ' + ''.join(random.choices(string.digits, k=8)))
    email: str = "fakeemail@test.com"
    street_name: str = "Teststraat"
    house_number: str = "123"
    postcode: str = "1234AB"
    place: str = "1234AB"
    message: str = (
        "This is a test order, I have used your website for a test assignment I am working on.\n"
        "Hope it's not going to affect your statistics too much, I am sorry if it does.\n"
        "You can filter all related activities by the email fakeemail@test.com."
    )


class CustomerGenerator:
    """
    Utility class to provide random test customer data.
    """

    @staticmethod
    def create_test_user() -> TestUser:
        return TestUser()
