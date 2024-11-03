import os
import subprocess

from config.config import ConfigReader


def test_load():
    """
    This test verify performance of provided URL using locust load testing framework
    You can adjust URL and all other important parameters in performance section of config.yaml
    """

    config_reader = ConfigReader()
    locust_file_path = os.path.join(
        os.path.dirname(__file__), "../../locust/home_page_load.py"
    )

    try:
        result = subprocess.run(
            [
                "locust",
                "-f",
                locust_file_path,
                "--headless",
                "--host",
                config_reader.get_performance_url(),
                "--users",
                config_reader.get_performance_users(),
                "--spawn-rate",
                config_reader.get_performance_rate(),
                "--run-time",
                config_reader.get_performance_duration(),
                "--html",
                "reports/load_test_report.html",
            ],
            check=True,
        )

        assert result.returncode == 0
    except subprocess.CalledProcessError as e:
        assert False, f"Load test failed with return code {e.returncode}"
