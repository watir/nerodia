import six
from selenium.common.exceptions import NoSuchFrameException

from .html_elements import HTMLElement, HTMLElementCollection
from ..exception import UnknownFrameException
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class IFrame(HTMLElement):
    def switch_to(self):
        if not self._located:
            self.locate()
        self.wd.switch()

    @property
    def text(self):
        """
        Returns text of iFrame body
        :rtype: str
        """
        return self.body().text

    @property
    def html(self):
        """
        Returns HTML code of iFrame
        :rtype: str
        """
        return self.wd.page_source

    def send_keys(self, *args):
        """
        Delegate sending keystrokes to FramedDriver
        """
        self.wd.send_keys(*args)

    def execute_script(self, script, *args):
        """ Executes JavaScript in context of frame """
        from .element import Element
        args = [e.wd if isinstance(e, Element) else e for e in args]
        returned = self.driver.execute_script(script, *args)

        return self.browser._wrap_elements_in(self, returned)

    @property
    def wd(self):
        """
        Provides access to underlying Selenium Objects as delegated by FramedDriver
        :rtype: FramedDriver
        """
        return FramedDriver(super(IFrame, self).wd, self.browser)

    # private

    @property
    def _should_relocate(self):
        return True

    @property
    def _unknown_exception(self):
        return UnknownFrameException


@six.add_metaclass(MetaHTMLElement)
class IFrameCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Frame(IFrame):
    # private

    @property
    def _frame_tag(self):
        return 'frame'


@six.add_metaclass(MetaHTMLElement)
class FrameCollection(IFrameCollection):
    pass


class FramedDriver(object):
    def __init__(self, element, browser):
        self.el = element
        self.browser = browser
        self.driver = browser.wd

    def __eq__(self, other):
        return self.wd == other.wd

    eql = __eq__

    def switch(self):
        try:
            self.driver.switch_to.frame(self.el)
            self.browser.default_context = False
        except NoSuchFrameException as e:
            raise UnknownFrameException(e)

    def send_keys(self, *args):
        self.switch()
        self.driver.switch_to.active_element.send_keys(*args)

    @property
    def wd(self):
        return self.el

    def __getattr__(self, meth):
        if meth.startswith('find_element'):
            return getattr(self.driver, meth)
        elif hasattr(self.driver, meth):
            self.switch()
            return getattr(self.driver, meth)
        else:
            return getattr(self.el, meth)
