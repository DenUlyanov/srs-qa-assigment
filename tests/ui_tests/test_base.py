import pytest

from utils.config_reader import ConfigReader


@pytest.mark.usefixtures("init_driver")
class BaseTest:

    @pytest.fixture(autouse=True)
    def setup_config_reader(self):
        self.config_reader = ConfigReader()
