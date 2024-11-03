import pytest

from config.config import ConfigReader
from pages.home_page import HomePage


@pytest.mark.usefixtures("init_driver")
class BaseTest:
    """
    This class is used to give access to fixtures to all child classes and
    store all methods that make sense share between steps
    """

    @pytest.fixture(autouse=True)
    def setup_config_reader(self):
        self.config_reader = ConfigReader()

    """
    This method searches products through the website and 
    is being used in cart and search tests 
   
    Parameters:
    search_request (str): Product you would like to find 
    """

    def search_for_product(self, search_request):
        home_page = HomePage(self.driver)
        home_page.open_home_page()
        home_page.allow_all_cookies()
        assert home_page.is_home_page_visible()
        home_page.search(search_request)
