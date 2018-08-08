import pytest

from nerodia.browser import Browser
from nerodia.capabilities import Capabilities


@pytest.mark.parametrize('driver', ['chrome', 'firefox', 'ie', 'safari', 'edge'])
class TestWebDriverArgs(object):
    def test_can_pass_port(self, mocker, driver):
        mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver')
        port = 5678
        Browser(driver, port=port)
        mock.assert_called_once()
        assert mock.call_args_list[0][1].get('command_executor') == \
            Capabilities.DEFAULT_URL.format(port)

    def test_can_pass_url(self, mocker, driver):
        from selenium.webdriver import DesiredCapabilities
        name = driver.upper() if driver != 'ie' else 'INTERNETEXPLORER'
        caps = getattr(DesiredCapabilities, name)
        mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver')
        Browser(driver, url='spam')
        mock.assert_called_once()
        assert mock.call_args_list[0][1].get('command_executor') == 'spam'
        assert mock.call_args_list[0][1]['desired_capabilities'].get('browserName') == \
            caps['browserName']

    def test_can_pass_executable_path(self, mocker, driver):
        mock = mocker.patch('selenium.webdriver.{}.webdriver.WebDriver'.format(driver))
        Browser(driver, executable_path='spam')
        mock.assert_called_once()
        assert mock.call_args_list[0][1].get('executable_path') == 'spam'
