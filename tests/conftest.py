import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='class')
def init_driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Add incognito mode

    web_driver = webdriver.Chrome(options=chrome_options)
    request.cls.driver = web_driver
    yield
    web_driver.close()
