import os

import yaml


class ConfigReader:
    def __init__(self):
        self.config_data = self._load_config()

    def _load_config(self):
        try:
            self.config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
            self.config_path = os.path.abspath(self.config_path)  # Optional: Get the absolute path for safety
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Config file '{self.config_path}' not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error reading YAML file: {e}")

    def get_website_url(self):
        return self.config_data.get('website', {}).get('url')

    def get_website_email(self):
        return self.config_data.get('website', {}).get('credentials', {}).get('username')

    def get_website_password(self):
        return self.config_data.get('website', {}).get('credentials', {}).get('password')

    def get_website_timeout(self):
        return self.config_data.get('website', {}).get('timeout')

    def get_weatherstack_url(self):
        return self.config_data.get('weatherstack', {}).get('url')

    def get_weatherstack_key(self):
        return self.config_data.get('weatherstack', {}).get('key')
