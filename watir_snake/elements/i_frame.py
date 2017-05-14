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
        self.query_scope.assert_exists()

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

        return FramedDriver(self.element, self.driver)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.wd == other.wd.wd if isinstance(other.wd, FramedDriver) else other.wd

    def switch_to(self):
        self.locate().switch()

    def assert_exists(self):
        if 'element' in self.selector:
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
        return self.wd.page_source

    def execute_script(self, *args):
        return self.browser.execute_script(*args)

    # private

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
    def __init__(self, element, driver):
        self.element = element
        self.driver = driver

    def __eq__(self, other):
        return self.wd == other.wd

    eql = __eq__

    def send_keys(self, *args):
        self.switch()
        self.driver.switch_to.active_element.send_keys(*args)

    @property
    def wd(self):
        return self.element

    def __getattr__(self, meth):
        if hasattr(self.driver, meth):
            self.switch()
            return getattr(self.driver, meth)
        else:
            return getattr(self.element, meth)

    def switch(self):
        try:
            self.driver.switch_to.frame(self.element)
        except NoSuchFrameException as e:
            raise UnknownFrameException(e)
