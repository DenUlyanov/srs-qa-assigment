# SHELL RECHARGE QA ASSIGNMENT

You can find original assignment [here][Assignment]

[Sources][GitHub] | [UI under test][SATLinkUi] | [API under test][SATLinkApi] | [Load test target][SATLinkLoad] |

## Tech info

This test framework is writen using [PyTest](https://docs.pytest.org/en/stable/)
used [Selenium Webdriver](https://www.selenium.dev/documentation/webdriver/) for UI test and
[Locust](https://docs.locust.io/en/stable/) for load testing. [Makefile](Makefile) is used to create virtual environment
and dependencies can be found in [toml](pyproject.toml) file.

## Test description

This test framework contains three different types of test: UI, API and Load tests.
You can find description and test cases below for each one of them.

### API Tests

Positive and negative test cases for weather API service [weatherstack](SATLinkApi) were added.
Test are using [requests library](https://pypi.org/project/requests/) to verify current weather information. 
You can find test scenarios [here](doc/API_TESTS.md)

### UI Test

Set of test created for popular e-commerce website for buying archery equipment [Europe archery][SATLinkUi]
Test are build with Page Object patter and verify basic functionality of login, search, and checkout process.
You can find test scenarios [here](doc/UI_TEST.md)

### Load tests

## How to run the tests

## How to view report

### UI and API

### Performance

## Prerequisites

## Project structure

## Adding new tests

## Test cases

[Assignment]: doc/SRS_EU_QA_Assignment_-_October_2024.pdf

[GitHub]: https://github.com/DenUlyanov/srs-qa-assigment

[SATLinkUi]: https://www.europearchery.com/

[SATLinkApi]:  https://weatherstack.com/

[SATLinkLoad]:  https://www.google.com/

[Makefile]

[]