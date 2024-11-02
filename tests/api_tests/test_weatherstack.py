import os

import pytest
import requests
import yaml


# Fixture to load configuration from config.yaml. This is showcase of alternative to using Config Reader utils
@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture
def base_url(config):
    return config['weatherstack']['url']


@pytest.fixture
def valid_api_key(config):
    return config['weatherstack']['key']


# Test Case 1: Valid API Response Test
@pytest.mark.parametrize("location", [
    ("Amsterdam"),
    ("New York"),
    ("London")
])
def test_valid_response(location, valid_api_key, base_url):
    params = {
        "access_key": valid_api_key,
        "query": location
    }

    response = get_weather(base_url, params)

    # Validate response status
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Verify provided data
    data = response.json()

    # Verify location is matching requested one
    assert data["location"]["name"] == location

    # Verify current weather forecast is not missing or empty
    current_weather = data["current"]
    assert current_weather is not None, "'current' weather data is missing"
    assert len(current_weather) > 0, "'current' weather data is empty"


# Test Case 2: Invalid API Key Test
def test_invalid_api_key(base_url):
    params = {
        "access_key": "this_is_invalid_key",
        "query": "New York"
    }

    response = get_weather(base_url, params)

    # Validate that an error is returned
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Verify error codes
    data = response.json()

    assert data["success"] == False
    assert data["error"]["code"] == 101
    assert data["error"]["type"] == "invalid_access_key"
    assert "You have not supplied a valid API Access Key" in data["error"]["info"]


def get_weather(base_url, params):
    return requests.get(base_url + "/current", params=params)

#    DISCLAIMER: Above scenarios is just a showcase, in production grade project I would add scenarios like:
#    1. Verify weather is within the norm for the region/city
#    2. Verify units used correctly
#    3. Verify language can be used correctly
#    4. Verify valid access key is required
#    5. Verify usage limits per API key
#    6. Use pull of random cities instead of hardcoded one
#    and many other possible scenarios
