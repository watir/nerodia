from importlib import import_module

import six
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

import nerodia
from nerodia.elements.scroll import Scrolling
from . import locators
from .after_hooks import AfterHooks
from .alert import Alert
from .capabilities import Capabilities
from .container import Container
from .cookies import Cookies
from .exception import Error
from .has_window import HasWindow
from .wait.timer import Timer
from .wait.wait import Waitable

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class Browser(Container, HasWindow, Waitable, Scrolling):
    def __init__(self, browser='chrome', *args, **kwargs):
        """
        Creates a nerodia.browser.Browser instance
        :param browser: firefox, ie, chrome, remote or Selenium WebDriver instance
        :type browser: selenium.webdriver.remote.webdriver.WebDriver or str
        :param args: args passed to the underlying driver
        :param kwargs: kwargs passed to the underlying driver
        """
        if isinstance(browser, six.string_types[0]):
            caps = Capabilities(browser, **kwargs)
            module = import_module('selenium.webdriver.{}'
                                   '.webdriver'.format(caps.selenium_browser.lower()))
            self.driver = module.WebDriver(**caps.kwargs)
        elif isinstance(browser, WebDriver):
            self.driver = browser
        else:
            raise TypeError('A browser name or WebDriver instance must be supplied, '
                            'got {}'.format(type(browser)))

        if 'listener' in kwargs:
            self.driver = EventFiringWebDriver(self.driver, kwargs.get('listener'))

        self.after_hooks = AfterHooks(self)
        self.current_frame = None
        self.closed = False
        self.default_context = True
        self._original_window = None
        self._locator_namespace = locators
        self._timer = Timer()

    @property
    def locator_namespace(self):
        """
        Whether the locators should be used from a different namespace. Defaults to nerodia.locators
        :return:
        """
        return self._locator_namespace

    @locator_namespace.setter
    def locator_namespace(self, namespace):
        self._locator_namespace = namespace

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, timer):
        self._timer = timer

    @property
    def wd(self):
        return self.driver

    @staticmethod
    def start(url, browser='chrome', *args, **kwargs):
        """
        Creates a Browser instance
        :param url: url to navigate to after starting browser
        :type url: str
        :param browser: firefox, ie, chrome, remote or Selenium WebDriver instance
        :type browser: selenium.webdriver.remote.webdriver.WebDriver or str
        :param args: args passed to the underlying driver
        :param kwargs: kwargs passed to the underlying driver
        """
        b = Browser(browser, *args, **kwargs)
        b.goto(url)
        return b

    def __repr__(self):
        try:
            if self.alert.exists:
                return '#<{}:0x{:x} alert=True>'.format(self.__class__.__name__,
                                                        self.__hash__() * 2)
            else:
                return '#<{}:0x{:x} url={!r} title={!r}>'.format(self.__class__.__name__,
                                                                 self.__hash__() * 2, self.url,
                                                                 self.title)
        except:  # noqa
            return '#<{}:0x{:x} closed={}>'.format(self.__class__.__name__, self.__hash__() * 2,
                                                   self.closed)

    selector_string = __repr__

    def goto(self, uri):
        """
        Goes to the given URL
        :param uri: the URL
        :type uri: str
        :return: the url you end up at
        :rtype: str
        """
        scheme = urlparse(uri).scheme
        if scheme == '' or '.' in scheme:
            uri = 'http://{}'.format(uri)

        self.driver.get(uri)
        self.after_hooks.run()
        return uri

    def back(self):
        """ Navigates back in history """
        self.driver.back()
        self.after_hooks.run()

    def forward(self):
        """ Navigates forward in history """
        self.driver.forward()
        self.after_hooks.run()

    @property
    def url(self):
        """
        Returns the URL of the current page
        :rtype: str
        """
        return self.driver.current_url

    @property
    def title(self):
        """
        Returns the title of the current page
        :rtype: str
        """
        return self.driver.title

    def close(self):
        """ Closes the browser """
        if not self.closed:
            self.driver.quit()
            self.closed = True

    quit = close

    @property
    def cookies(self):
        """
        Handles cookies
        :rtype: nerodia.cookies.Cookies
        """
        return Cookies(self.driver)

    @property
    def name(self):
        """
        Returns the browser name
        :rtype: str
        """
        return self.driver.name

    @property
    def text(self):
        """
        Returns the text of the page body
        :return:
        """
        return self.body().text

    @property
    def html(self):
        """
        Returns HTML code of the current page
        :rtype: str
        """
        return self.driver.page_source

    @property
    def alert(self):
        """
        Handles Javascript alerts, confirms and prompts
        :rtype: nerodia.alert.Alert
        """
        return Alert(self)

    def refresh(self):
        """ Refreshes the current page """
        self.driver.refresh()
        self.after_hooks.run()

    def wait(self, timeout=5):
        """
        Waits until the readyState of document is complete, raises a TimeoutException if timeout is
        exceeded
        :param timeout: time to wait
        :type timeout: int
        """
        return self.wait_until(lambda b: b.ready_state == "complete", timeout=timeout,
                               message="waiting for document.readyState == 'complete'")

    @property
    def ready_state(self):
        """
        Returns the readyState of the document
        :rtype: str
        """
        return self.execute_script('return document.readyState;')

    @property
    def status(self):
        """
        Returns the text of the status bar
        :return:
        """
        return self.execute_script('return window.status;')

    def execute_script(self, script, *args, function_name=None):
        """
        Executes JavaScript snippet
        :param script: Javascript Snippet to execute
        :type script: str
        :param args: Arguments will be available in the given script in the 'arguments' pseudo-array
        :param function_name: name of function being executed
        :type function_name: str or None
        :return: result of script
        """
        from .elements.element import Element
        args = [e.wait_until(lambda x: x.exists).wd if isinstance(e, Element) else e for e in args]
        if function_name:
            nerodia.logger.info(f'Executing Script on Browser: {function_name}')
        returned = self.driver.execute_script(script, *args)

        return self._wrap_elements_in(self, returned)

    def send_keys(self, *args):
        """
        Sends sequence of keystrokes to currently active element
        :param args: keystrokes
        """
        self.driver.switch_to.active_element.send_keys(*args)

    @property
    def screenshot(self):
        """
        Handles screenshots of current pages
        :rtype: nerodia.screenshot.Screenshot
        """
        from .screenshot import Screenshot
        return Screenshot(self)

    @property
    def exist(self):
        """
        True if browser is not closed and False otherwise
        :rtype: bool
        """
        return not self.closed and self.window().present

    exists = exist

    @property
    def browser(self):
        return self

    def locate(self):
        if self.closed:
            raise Error('browser was closed')
        self._ensure_context()

    # private

    def _ensure_context(self):
        if self.default_context:
            return

        self.driver.switch_to.default_content()
        self.default_context = True
        self.after_hooks.run()

    @staticmethod
    def _wrap_elements_in(scope, obj):
        if isinstance(obj, WebElement):
            return Browser._wrap_element(scope, obj)
        elif isinstance(obj, list):
            return [Browser._wrap_elements_in(scope, e) for e in obj]
        elif isinstance(obj, dict):
            for k, v in obj.items():
                obj[k] = Browser._wrap_elements_in(scope, v)
            return obj
        else:
            return obj

    @staticmethod
    def _wrap_element(scope, element):
        from .elements.html_elements import HTMLElement
        klass = nerodia.element_class_for(element.tag_name.lower()) or HTMLElement
        return klass(scope, {'element': element})
