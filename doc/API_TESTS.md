# API TEST CASES

Please note: normally test cases would be stored in separate test management tool

## Test Case 1: Checking Valid Weather Information for Popular Cities

Description: We want to verify that our weather service correctly provides weather information for a few popular cities:
Amsterdam, New York, and London.

### Steps:

- Send a request to the weather service for each of these cities.
- Use a valid API key to ensure we receive the correct data.

### Expected Results:

- The response from the service should indicate success (e.g., no errors).
- The city name returned by the service should match the one we requested.
- Current weather data (such as temperature, wind speed, etc.) should be present and not empty.

## Test Case 2: Checking Response with an Invalid API Key

Description: We want to verify what happens when someone tries to use the weather service with an invalid key, ensuring
that it properly denies access.

### Steps:

- Send a request to the weather service for the city "New York" using an incorrect API key.

### Expected Results:

- Even though the status code should be the same as for a valid request, the response should indicate failure.
- An error message should be returned, saying that the API key is invalid.
- The response should include an error code ("101") and an error type ("invalid_access_key") with a message explaining
that a valid API key was not provided.

## Additional Scenarios to Consider:

- Verify that the weather data returned for a city makes sense and falls within the expected range for that location.
- Check if the weather units (e.g., Celsius, Fahrenheit) are used correctly.
- Test if the language options for weather information work as expected.
- Ensure that a valid API key is always required to access the service.
- Confirm that there are limits on how many requests can be made using a single API key.
- Instead of using just a few fixed cities, use a larger variety of cities to make sure the service works broadly.