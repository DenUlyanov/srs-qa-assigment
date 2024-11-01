import pytest
from selenium import webdriver
from urllib3 import request
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from Config.config import TestData


@pytest.fixture(scope='class')
def init_driver(request):

    web_driver = webdriver.Chrome()
    request.cls.driver = web_driver
    yield
    web_driver.close()
