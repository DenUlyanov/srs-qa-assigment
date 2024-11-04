# LOAD TEST CASES

## Important note

The test assignment specifies a load of 1000 requests over 15 seconds, which is considered a substantial load. It would
not be ethical to run such a test against a website we do not own. These types of tests should be well-coordinated to
reduce the impact on the target application. Instead, I have created a script that can take a URL, user count, arrival
rate, and duration, which can be easily updated in config.yaml for flexibility.

## Test Case: Load Performance Test

Verify the performance of the provided URL by executing a load test using the Locust load testing tool.

### Steps:

- Prepare the load test configuration by ensuring all relevant parameters are set in the config.yaml file.
- Run the Locust load test script with the specified configuration.
- Generate an HTML report to capture the test results.

### Expected Results:

- The load test should complete successfully without errors.
- An HTML report should be generated with the results of the load test.

## Questions:

### Did the load test have an impact on web application response time?

Since I reduce amount of request to bare minimum this test would not have any effect on performance of the application.
If I would use original requeirments taht can cause some degradation of performance if no protective measure were taken
on serverside.
The best way to see this during performance testing is to monitor bot information from load test tool and live metrics
of you application.

### What is the optimal application response time for modern-day web applications?

- 100 - excellent performance, not noticeable
- 100 - 1000 ms - comfortable for user
- 1000 - 2000 ms - noticeable response time# LOAD TEST CASES

## Important note

Test assignment specify load of 1000 request for 15 seconds considered quite substantial load it
would not be ethical to run such test against website we don't own. Such tests should be well coordinated to reduce
impact. I have created a script that can take url, user count, arrival rate and duration that can be easily updated in
config.yaml

## Test Case: Load Performance Test

Verify the performance of the provided URL by executing a load test using the Locust load testing tool.

### Steps:

- Prepare the load test configuration by ensuring all relevant parameters are set in the config.yaml file.
- Run the Locust load test script with the specified configuration.
- Generate an HTML report to capture the test results.

### Expected Results:

- The load test should complete successfully without errors.
- An HTML report should be generated with the results of the load test.

## Questions:

### Did the load test have an impact on web application response time?

Since I reduced the number of requests to the bare minimum, this test should not have any effect on the performance of
the application. However, running the original requirements could potentially cause degradation of performance if no
protective measures are implemented on the server side. The best way to assess this during performance testing is to
monitor both the information from the load test tool and the live metrics of the application.

### What is the optimal application response time for modern-day web applications?

- 100 - excellent performance, not noticeable
- 100 - 1000 ms - comfortable for user
- 1000 - 2000 ms - noticeable response time
- 2000 - 10,000 ms - delayed response time
- 10,000 ms - unacceptable response time

### Analyse a few HTTP/S responses

Looking on one of our test reports

![LOAD](screenshots/load_results.png)

- Number of Requests Sent: 26

- Success Rate: All requests succeeded.

- Average Response Time: 138 ms, which is quite good.

- Maximum Response Time: 272 ms, still well within acceptable norms.

- Maximum Transactions Per Second (TPS): Nearly 7 requests per second.