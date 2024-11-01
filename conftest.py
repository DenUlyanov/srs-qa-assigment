import pytest
from driver.webdriver_factory import create_driver

@pytest.fixture(scope="function")
def driver_init(request):
    driver = create_driver()
    request.cls.driver = driver
    yield
    driver.quit()
