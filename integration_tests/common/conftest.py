import pytest
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from integration_tests.common import config
from integration_tests.common.driver_manager import DriverManager

def pytest_addoption(parser):
    """
    Defines custom command line options for pytest.

    Args:
        parser Parser: pytest command line parser
    """
    parser.addoption("--baseurl",
                     action = "store",
                     default = "https://www.hudl.com",
                     help = "Base URL for the application under test")
    parser.addoption("--browser",
                      action = "store",
                      default = "chrome",
                      help = "The name of the browser to test with"
                      )
    parser.addoption("--host",
                    action = "store",
                    default = "local",
                    help = "The name of the host to run tests in"
                    )
    parser.addoption("--headless",
                      action = "store",
                      default = False,
                      help = "Switch to run headlws or not"
                      )
    parser.addoption("--scope",
                      action = "store",
                      default = "session",
                      help = "Scope for which the driver exists"
                      )

def get_scope(config):
    config.scope = config.getoption("--scope")
    return config.scope

@pytest.fixture(scope=get_scope)
def driver(request):
    """
    Setup fixture that runs before and after each test that invokes it as an argument.
    Stores the values of the custom command line parameters in the applcable variables in config.py
    Gets a driver from the DriverManager in driver_manager.py
    Returns a driver to the test so it can be passed into pages.
    After the test it disposes of the driver and resets the shared driver instance _driver in DriverManager to None

    Args:
        request Request: Request object from pytest

    Returns:
        webdriver: The webdriver to beused in the test.
    """
    # Store command line parameter values in config.py
    config.baseurl = request.config.getoption("--baseurl")
    config.browser = request.config.getoption("--browser").lower()
    config.host = request.config.getoption("--host")
    config.headless = request.config.getoption("--headless")
    
    # Get a shared drive instance
    driver_ = DriverManager.get_driver()


    