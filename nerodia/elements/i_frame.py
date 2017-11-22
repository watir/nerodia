import six
from selenium.common.exceptions import NoSuchFrameException

from .html_elements import HTMLElement
from ..element_collection import ElementCollection
from ..exception import UnknownFrameException
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class IFrame(HTMLElement):
    def locate(self):
        if not self.selector:
            return None
        self.query_scope._ensure_context()

        selector = self.selector.copy()
        selector.update({'tag_name': self._frame_tag})
        element_validator = self._element_validator_class()
        selector_builder = self._selector_builder_class(self.query_scope,
                                                        selector, self.ATTRIBUTES)
        locator = self._locator_class(self.query_scope, selector, selector_builder,
                                      element_validator)

        element = locator.locate()
        if not element:
            raise self._unknown_exception(
                'unable to locate {} using {}'.format(self.selector['tag_name'],
                                                      self.selector_string))
        self.el = FramedDriver(element, self.browser)
        return self.el

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.wd == other.wd.wd if isinstance(other.wd, FramedDriver) else other.wd

    def switch_to(self):
        self.locate().switch()

    def assert_exists(self):
        if self.element and not self.selector:
            raise UnknownFrameException(
                'wrapping a Selenium element as a Frame is not currently supported')
        return super(IFrame, self).assert_exists()

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
        self.wait_for_exists()
        return self.el.page_source

    def execute_script(self, script, *args):
        """ Executes JavaScript in context of frame """
        from .element import Element
        args = [e.wd if isinstance(e, Element) else e for e in args]
        returned = self.driver.execute_script(script, *args)

        return self.browser._wrap_elements_in(self, returned)

    # private

    def _ensure_context(self):
        self.switch_to()

    @property
    def _frame_tag(self):
        return 'iframe'

    @property
    def _unknown_exception(self):
        return UnknownFrameException


@six.add_metaclass(MetaHTMLElement)
class IFrameCollection(ElementCollection):
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
        self.driver = browser.driver

    def __eq__(self, other):
        return self.wd == other.wd

    eql = __eq__

    def send_keys(self, *args):
        self.switch()
        self.driver.switch_to.active_element.send_keys(*args)

    @property
    def wd(self):
        return self.el

    def __getattr__(self, meth):
        if hasattr(self.driver, meth):
            self.switch()
            return getattr(self.driver, meth)
        else:
            return getattr(self.el, meth)

    def switch(self):
        try:
            self.driver.switch_to.frame(self.el)
            self.browser.default_context = False
        except NoSuchFrameException as e:
            raise UnknownFrameException(e)
