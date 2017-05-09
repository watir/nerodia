import pytest
from _pytest.skipping import MarkEvaluator

import watir_snake
from watir_snake.browser import Browser
from .support.webserver import WebServer

browsers = (
    'chrome',
    'edge',
    'firefox',
    'ie',
    'phantomjs'
    # 'remote',  TODO: just local for now
    'safari'
)

watir_snake.default_timeout = 3


def pytest_addoption(parser):
    parser.addoption(
        '--browser',
        action='store',
        choices=browsers,
        metavar='BROWSER',
        help='browser to run tests against ({})'.format(', '.join(browsers)))


@pytest.fixture(scope='session')
def browser(request):
    kwargs = {}

    try:
        browser_name = request.config.getoption('--browser')
    except AttributeError:
        raise Exception('This test requires a --browser to be specified.')

    # if driver_class == 'remote':
    #     capabilities = DesiredCapabilities.CHROME.copy()
    #     kwargs.update({'desired_capabilities': capabilities})
    browser = Browser(browser_name,
                      executable_path='/Users/lucast/Documents/HC-Mercurial/hc.qa.webdriver/hc/qa'
                                      '/webdriver/binaries/darwin/chromedriver')
    yield browser
    try:
        browser.quit()
    except:
        pass


@pytest.fixture
def page(browser, webserver):
    class Page(object):
        def url(self, name):
            return webserver.path_for(name)

        def load(self, name):
            browser.goto(self.url(name))

    return Page()


@pytest.fixture(autouse=True, scope='session')
def webserver():
    webserver = WebServer()
    webserver.start()
    yield webserver
    webserver.stop()
