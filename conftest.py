import os

import pytest
from _pytest.skipping import MarkEvaluator

import nerodia
from nerodia.browser import Browser
from nerodia.support.webserver import WebServer

browsers = (
    'chrome',
    'edge',
    'firefox',
    'ie',
    # 'remote',  TODO: just local for now
    'safari'
)

nerodia.default_timeout = 3


browser_instance = None


def pytest_addoption(parser):
    parser.addoption(
        '--browser',
        action='store',
        choices=browsers,
        metavar='BROWSER',
        help='browser to run tests against ({})'.format(', '.join(browsers)))
    parser.addoption(
        '--not_relaxed',
        action='store_true',
        help='whether to not use relaxed_locate for tests')


def pytest_collection_modifyitems(session, config, items):
    """ called after collection has been performed, may filter or re-order the items in-place
    :param session: pytest session instance
    :param config: configuration of pytest
    :param items: items collected
    """
    nerodia.relaxed_locate = not config.getoption('--not_relaxed')


@pytest.fixture(scope='session')
def bkwargs(request):
    kwargs = {}

    try:
        kwargs['browser'] = request.config.getoption('--browser')
    except AttributeError:
        raise Exception('This test requires a --browser to be specified.')

    if os.environ.get('DRIVER_PATH'):
        kwargs['executable_path'] = os.environ.get('DRIVER_PATH')
    yield kwargs


@pytest.fixture(scope='session')
def browser_manager(bkwargs):
    manager = BrowserManager(bkwargs)
    yield manager
    manager.quit()


@pytest.fixture(scope='function')
def browser(request, browser_manager):
    # conditionally mark tests as expected to fail based on driver
    request.node._evalxfail = request.node._evalxfail or MarkEvaluator(
        request.node, 'xfail_{}'.format(browser_manager.name))
    if request.node._evalxfail.istrue():
        def fin():
            global driver_instance
            if driver_instance is not None:
                driver_instance.quit()
            driver_instance = None
        request.addfinalizer(fin)

    # skip driver instantiation if xfail(run=False)
    if not request.config.getoption('runxfail'):
        if request.node._evalxfail.istrue():
            if request.node._evalxfail.get('run') is False:
                yield
                return

    yield browser_manager.browser

    if MarkEvaluator(request.node, 'quits_browser').istrue():
        browser_manager.quit()


@pytest.fixture(scope='session')
def page(browser_manager, webserver):
    class Page(object):
        def url(self, name):
            return webserver.path_for(name)

        def load(self, name):
            browser_manager.browser.goto(self.url(name))
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


@pytest.fixture
def temp_file():
    import tempfile
    tmp = tempfile.NamedTemporaryFile()
    yield tmp
    tmp.close()


class BrowserManager(object):
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.name = kwargs['browser'].lower()
        self.instance = None

    @property
    def browser(self):
        if not self.instance:
            self.create_session()
        return self.instance

    def create(self):
        return Browser(**self.kwargs)

    def create_session(self):
        self.instance = self.create()

    def clear(self):
        self.instance = None

    def quit(self):
        if self.instance:
            self.instance.quit()
            self.instance = None
