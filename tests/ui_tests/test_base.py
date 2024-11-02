import pytest

from pages.home_page import HomePage
from utils.config_reader import ConfigReader


@pytest.mark.usefixtures("init_driver")
class BaseTest:

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
        self.homePage = HomePage(self.driver)
        self.homePage.open_home_page()
        self.homePage.allow_all_cookies()
        assert self.homePage.is_home_page_visible()
        self.homePage.search(search_request)
