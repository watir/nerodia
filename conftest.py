import os
import pytest

import watir_snake
from watir_snake.browser import Browser
from watir_snake.support.webserver import WebServer

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
def bkwargs(request):
    kwargs = {}

    try:
        kwargs['browser'] = request.config.getoption('--browser')
    except AttributeError:
        raise Exception('This test requires a --browser to be specified.')

    # if driver_class == 'remote':
    #     capabilities = DesiredCapabilities.CHROME.copy()
    #     kwargs.update({'desired_capabilities': capabilities})
    if os.environ.get('DRIVER_PATH'):
        kwargs['executable_path'] = os.environ.get('DRIVER_PATH')
    yield kwargs


@pytest.fixture(scope='session')
def browser(bkwargs):
    browser = Browser(**bkwargs)
    yield browser
    try:
        browser.quit()
    except:
        pass


@pytest.fixture(scope='session')
def page(browser, webserver):
    class Page(object):
        def url(self, name):
            return webserver.path_for(name)

        def load(self, name):
            browser.goto(self.url(name))
    return Page()


@pytest.fixture(autouse=True)
def start_page(request, page):
    marker = request.node.get_marker('page')
    if marker:
        page.load(marker.args[0])


@pytest.fixture(scope='session')
def messages(browser):
    class Messages(object):
        @property
        def list(self):
            return [el.text for el in browser.div(id='messages').divs()]
    yield Messages()


@pytest.fixture(autouse=True, scope='session')
def webserver():
    webserver = WebServer()
    webserver.start()
    yield webserver
    webserver.stop()
