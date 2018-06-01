from inspect import stack
from re import search, sub

from selenium.common.exceptions import InvalidElementStateException, \
    StaleElementReferenceException, \
    ElementNotVisibleException, ElementNotInteractableException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains

import nerodia
from nerodia.browser import Browser
from ..adjacent import Adjacent
from ..container import Container
from ..exception import Error, ObjectDisabledException, ObjectReadOnlyException, \
    UnknownFrameException, UnknownObjectException, NoMatchingWindowFoundException
from ..js_execution import JSExecution
from ..js_snippet import JSSnippet
from ..locators.class_helpers import ClassHelpers
from ..locators.element.selector_builder import SelectorBuilder
from ..wait.wait import TimeoutError, Wait, Waitable
from ..window import Dimension, Point


class Element(ClassHelpers, JSExecution, Container, JSSnippet, Waitable, Adjacent):
    ATTRIBUTES = []

    def __init__(self, query_scope, selector):
        self.query_scope = query_scope
        if not isinstance(selector, dict):
            raise TypeError('invalid argument: {!r}'.format(selector))

        self.el = selector.pop('element', None)
        self.selector = selector
        self.keyword = None
        self.locator = None

    @property
    def exists(self):
        """
        Returns True if element exists, False otherwise
        :rtype: bool
        """
        try:
            if self.el and self.stale:
                return False
            self.assert_exists()
            return True
        except (UnknownObjectException, UnknownFrameException):
            return False

    exist = exists

    def __repr__(self):
        string = '#<{}: '.format(self.__class__.__name__)
        if self.keyword:
            string += 'keyword: {} '.format(self.keyword)
        string += 'located: {}; '.format(self.el is not None)
        if not self.selector:
            string += '{element: (selenium element)}'
        else:
            string += self.selector_string
        string += '>'
        return string

    def __eq__(self, other):
        """
        Returns True if two elements are equal
        :param other: other element to compare
        :rtype: bool
        """
        return isinstance(other, self.__class__) and self.wd == other.wd

    eql = __eq__

    def __hash__(self):
        return self.el.__hash__() if self.el else super(Element, self).__hash__()

    @property
    def text(self):
        """
        Returns the text of the element
        :rtype: str
        """
        return self._element_call(lambda: self.el.text)

    @property
    def tag_name(self):
        """
        Returns the tag name of the element
        :rtype: str
        """
        return self._element_call(lambda: self.el.tag_name).lower()

    def click(self, *modifiers):
        """
        Clicks the element, optionally while pressing the given modifier keys.
        Note that support for holding a modifier key is currently experimental, and may not work
        at all.

        :param modifiers: modifier keys to press while clicking
        :Example: Click an element

        browser.element(name='new_user_button').click()

        :Example: Click an element with shift key pressed
        from selenium.webdriver.common.keys import Keys
        browser.element(name='new_user_button').click(Keys.SHIFT)

        :Example: Click an element with several modifier keys pressed
        from selenium.webdriver.common.keys import Keys
        browser.element(name='new_user_button').click(Keys.SHIFT, Keys.CONTROL)
        """

        def method():
            if modifiers:
                action = ActionChains(self.driver)
                for mod in modifiers:
                    action.key_down(mod)
                action.click(self.el)
                for mod in modifiers:
                    action.key_up(mod)
                action.perform()
            else:
                self.el.click()

        self._element_call(method, self.wait_for_enabled)
        self.browser.after_hooks.run()

    def js_click(self):
        """
        Simulates JavaScript click event on element.

        :Example: Click an element
        browser.element(name='new_user_button').js_click()
        """
        self.fire_event('click')
        self.browser.after_hooks.run()

    def double_click(self):
        """
        Double clicks the element.
        Note that browser support may vary.

        :Example: Double-click an element

        browser.element(name='new_user_button').double_click()
        """
        self._element_call(lambda: ActionChains(self.driver).double_click(self.el)
                           .perform(), self.wait_for_present)
        self.browser.after_hooks.run()

    def js_double_click(self):
        """
        Simulates JavaScript double click event on element.

        :Example: Click an element
        browser.element(name='new_user_button').js_double_click()
        """
        self.fire_event('dblclick')
        self.browser.after_hooks.run()

    def right_click(self):
        """
        Right clicks the element
        Note that browser support may vary

        :Example: Right click an element

        browser.element(name='new_user_button').right_click()
        """
        self._element_call(lambda: ActionChains(self.driver).context_click(self.el)
                           .perform(), self.wait_for_present)
        self.browser.after_hooks.run()

    def hover(self):
        """
        Moves the mouse to the middle of this element
        Note that browser support may vary

        :Example: Hover over an element

        browser.element(name='new_user_button').hover()
        """
        self._element_call(lambda: ActionChains(self.driver).move_to_element(self.el)
                           .perform(), self.wait_for_present)
        self.browser.after_hooks.run()

    def drag_and_drop_on(self, other):
        """
        Drag and drop this element on to another element instance
        Note that browser support may vary

        :param other: element to drop on

        :Example: Drag an element onto another

        a = browser.div(id='draggable')
        b = browser.div(id='droppable')
        a.drag_and_drop_on(b)
        """
        self._assert_is_element(other)

        value = self._element_call(lambda: ActionChains(self.driver)
                                   .drag_and_drop(self.el, other.wd).perform(),
                                   self.wait_for_present)
        self.browser.after_hooks.run()
        return value

    def drag_and_drop_by(self, xoffset, yoffset):
        """
        Drag and drop this element by the given offsets.
        Note that browser support may vary.

        :param xoffset: amount to move horizontally
        :param yoffset: amount to move vertically

        :Example: Drag an element onto another

        browser.div(id='draggable').drag_and_drop_by(100, -200)
        """
        self._element_call(lambda: ActionChains(self.driver).
                           drag_and_drop_by_offset(self.el, xoffset, yoffset).perform(),
                           self.wait_for_present)

    def select_text(self, string):
        """
        Selects text on page (as if dragging clicked mouse across provided text)

        :param string: string to select

        :Example:

        browser.legend().select_text('information')
        """
        self._element_call(lambda: self._execute_js('selectText', self.el, string))

    @property
    def value(self):
        """
        Returns value of the element
        :rtype: str
        """
        try:
            return self.attribute_value('value') or ''
        except InvalidElementStateException:
            return ''

    def attribute_value(self, attribute_name):
        """
        Returns given attribute value of the element

        :param attribute_name: attribute to retrieve
        :type attribute_name: str
        :rtype: str

        :Example:

        browser.a(id='link_2').attribute_value('title')  #=> 'link_title_2'
        """
        return self._element_call(lambda: self.el.get_attribute(attribute_name))

    get_attriubte = attribute_value

    attribute = attribute_value

    def send_keys(self, *args):
        """
        Sends sequence of keystrokes to the element
        :param args: keystrokes to send

        :Example:

        browser.text_field(name='new_user_first_name').send_keys('nerodia')
        """
        return self._element_call(lambda: self.el.send_keys(*args), self.wait_for_writable)

    @property
    def focused(self):
        """
        Returns True if the element is focused
        :rtype: bool
        """
        return self._element_call(lambda: self.el == self.driver.switch_to.active_element)

    def fire_event(self, event_name):
        """
        Simulates JavaScript events on element
        Note that you may omit 'on' from event name

        :param event_name: event to fire

        :Example:

        browser.button(name='new_user_button').fire_event('click')
        browser.button(name='new_user_button').fire_event('mousemove')
        browser.button(name='new_user_button').fire_event('onmouseover')
        """
        event_name = sub(r'^on', '', str(event_name)).lower()

        self._element_call(lambda: self._execute_js('fireEvent', self.el, event_name))

    def scroll_into_view(self):
        """
        Scroll until the element is in the view screen
        :rtype: Point

        :Example:

        browser.button(name='new_user_button').scroll_into_view()
        """
        return Point(**self._element_call(lambda: self.el.location_once_scrolled_into_view))

    @property
    def location(self):
        """
        Get the location of the element (x, y)
        :rtype: Point

        :Example:

        browser.button(name='new_user_button').location
        """
        return Point(**self._element_call(lambda: self.el.location))

    @property
    def size(self):
        """
        Get the size of the element (width, height)
        :rtype: Dimension

        :Example:

        browser.button(name='new_user_button').size
        """
        return Dimension(**self._element_call(lambda: self.el.size))

    @property
    def height(self):
        """
        Get the height of the element
        :rtype: int

        :Example:

        browser.button(name='new_user_button').height
        """
        return self.size.height

    @property
    def width(self):
        """
        Get the width of the element
        :rtype: int

        :Example:

        browser.button(name='new_user_button').width
        """
        return self.size.width

    @property
    def center(self):
        """
        Get the center coordinates of the element
        :rtype: Point

        :Example:

        browser.button(name='new_user_button').center
        """
        location = self.location
        size = self.size
        return Point(round(location.x + size.width / 2), round(location.y + size.height / 2))

    centre = center

    @property
    def driver(self):
        return self.query_scope.driver

    @property
    def wd(self):
        from .i_frame import FramedDriver
        if self.el is None:
            self.assert_exists()
        if isinstance(self.el, FramedDriver):
            return self.driver
        return self.el

    @property
    def visible(self):
        """
        Returns true if this element is visible on the page
        Raises exception if element does not exist

        :rtype: bool
        """
        try:
            self.assert_exists()
            return self.el.is_displayed()
        except StaleElementReferenceException:
            self.reset()
            raise self._unknown_exception

    @property
    def enabled(self):
        """
        Returns True if the element is present and enabled on the page

        :rtype: bool
        """
        return self._element_call(lambda: self.el.is_enabled(), self.assert_exists)

    @property
    def present(self):
        """
        Returns True if the element exists and is visible on the page
        Returns False if the element does not exist or exists but is not visible

        :rtype: bool
        """
        try:
            return self.visible
        except (UnknownObjectException, UnknownFrameException):
            return False

    def style(self, prop=None):
        """
        Returns given style property of this element

        :param prop: property to get
        :type prop: str
        :rtype: str

        :Example:

        browser.button(value='Delete').style           #=> "border: 4px solid red;"
        browser.button(value='Delete').style('border') #=> "4px solid rgb(255, 0, 0)"
        """
        if prop:
            return self._element_call(lambda: self.el.value_of_css_property(prop))
        else:
            return str(self.attribute_value('style')).strip()

    def to_subtype(self):
        """
        Cast this Element instance to a more specific subtype
        :Example:

        browser.element(xpath="//input[@type='submit']").to_subtype()  #=> #<Button>
        """
        tag = self.tag_name
        from .button import Button
        from .check_box import CheckBox
        from .file_field import FileField
        from .html_elements import HTMLElement
        from .radio import Radio
        from .text_field import TextField

        if tag == 'input':
            elem_type = self.attribute_value('type')
            if elem_type in Button.VALID_TYPES:
                klass = Button
            elif elem_type == 'checkbox':
                klass = CheckBox
            elif elem_type == 'radio':
                klass = Radio
            elif elem_type == 'file':
                klass = FileField
            else:
                klass = TextField
        else:
            klass = nerodia.element_class_for(tag) or HTMLElement

        return klass(self.query_scope, selector=dict(self.selector, element=self.wd))

    @property
    def browser(self):
        """
        Returns browser
        :rtype: nerodia.browser.Browser
        """
        return self.query_scope.browser

    @property
    def stale(self):
        """
        Returns True if a previously located element is no longer attached to the DOM
        :rtype: bool
        """
        if self.el is None:
            raise Error('Can not check staleness of unused element')
        if self.stale_in_context:
            self.query_scope._ensure_context()
            return self.stale_in_context
        else:
            return False

    @property
    def stale_in_context(self):
        try:
            self.el.is_enabled()  # any wire call will check for staleness
            return False
        except StaleElementReferenceException:
            return True

    def reset(self):
        self.el = None

    def wait_for_exists(self):
        if not nerodia.relaxed_locate:
            return self.assert_exists()
        if self.exists:  # Performance shortcut
            return None

        try:
            if not isinstance(self.query_scope, Browser):
                self.query_scope.wait_for_exists()
            self.wait_until(lambda e: e.exists)
        except TimeoutError:
            raise self._unknown_exception('timed out after {} seconds, waiting for {} to be '
                                          'located'.format(nerodia.default_timeout, self))

    def wait_for_present(self):
        if not nerodia.relaxed_locate:
            return self.visible
        if self.present:
            return True

        try:
            if not isinstance(self.query_scope, Browser):
                self.query_scope.wait_for_present()
            self.wait_until_present()
        except TimeoutError as e:
            raise self._unknown_exception('element located, but {}'.format(e))

    def wait_for_enabled(self):
        from .button import Button
        from .input import Input
        from .option import Option
        from .select import Select
        if not nerodia.relaxed_locate:
            return self._assert_enabled()

        self.wait_for_exists()
        if not any(isinstance(self, klass) for klass in [Input, Button, Select, Option]):
            return

        try:
            self.wait_until(lambda e: e.enabled)
        except TimeoutError:
            raise ObjectDisabledException('element present, but timed out after {} seconds, '
                                          'waiting for {} to be '
                                          'enabled'.format(nerodia.default_timeout, self))

    def wait_for_writable(self):
        self.wait_for_exists()

        self.wait_for_enabled()
        if not nerodia.relaxed_locate:
            if hasattr(self, 'readonly') and self.readonly:
                self._raise_writable()

        try:
            self.wait_until(lambda e: not getattr(e, 'readonly', None) or not e.readonly)
        except TimeoutError:
            raise ObjectReadOnlyException('element present and enabled, but timed out after {} '
                                          'seconds, waiting for {} to not be '
                                          'readonly'.format(nerodia.default_timeout, self))

    def assert_exists(self):
        """
        Ensure that the element exists, making sure that it is not stale and located if necessary
        """
        if not self.el:
            self.locate()
        if self.el is None:
            raise UnknownObjectException('unable to locate element: {}'.format(self))

    def locate(self):
        self.locator = self._build_locator()

        self.el = self.locator.locate()
        return self.el

    @property
    def selector_string(self):
        from ..browser import Browser
        if isinstance(self.query_scope, Browser):
            return self.selector.__repr__()
        else:
            return '{} --> {}'.format(self.query_scope.selector_string, self.selector)

    # Private

    def _raise_writable(self):
        raise ObjectReadOnlyException('element present and enabled, but timed out after {} '
                                      'seconds, waiting for {} to not be '
                                      'readonly'.format(nerodia.default_timeout, self))

    def _raise_disabled(self):
        raise ObjectReadOnlyException('element present and enabled, but timed out after {} '
                                      'seconds, waiting for {} to not be '
                                      'disabled'.format(nerodia.default_timeout, self))

    def _raise_present(self):
        raise UnknownObjectException('element located, but timed out after {} seconds, waiting '
                                     'for {} to be present'.format(nerodia.default_timeout, self))

    @property
    def _unknown_exception(self):
        return UnknownObjectException

    @property
    def _element_class(self):
        return self.__class__

    # Ensure the driver is in the desired browser context
    def _ensure_context(self):
        if not self.exists:
            self.locate()

    def _is_attribute(self, attribute_name):
        return self.attribute_value(attribute_name) is not None

    def _assert_enabled(self):
        if not self._element_call(lambda: self.el.is_enabled()):
            raise ObjectDisabledException('object is disabled {}'.format(self))

    @classmethod
    def _assert_is_element(cls, obj):
        if not isinstance(obj, Element):
            raise TypeError('execpted nerodia.Element, '
                            'got {}:{}'.format(obj, obj.__class__.__name__))

    def _element_call(self, method, precondition=None):
        caller = stack()[1][3]
        already_locked = Wait.timer.locked
        if not already_locked:
            from ..wait.timer import Timer
            Wait.timer = Timer(timeout=nerodia.default_timeout)
        try:
            return self._element_call_check(precondition, method, caller)
        finally:
            nerodia.logger.info('<- `Completed {}#{}`'.format(self, caller))
            if not already_locked:
                Wait.timer.reset()

    def _check_condition(self, condition):
        nerodia.logger.info('<- `Verifying precondition {}#{}`'.format(self, condition))
        try:
            if not condition:
                self.assert_exists()
            else:
                condition()
            nerodia.logger.info('<- `Verified precondition '
                                '{}#{!r}`'.format(self, condition or 'assert_exists'))
        except self._unknown_exception:
            if condition is None:
                nerodia.logger.info('<- `Unable to satisfy precondition '
                                    '{}#{}`'.format(self, condition))
                self._check_condition(self.wait_for_exists)
            else:
                raise

    def _element_call_check(self, precondition, method, caller):
        nerodia.logger.info('-> `Executing {}#{}`'.format(self, caller))
        while True:
            try:
                self._check_condition(precondition)
                return method()
            except self._unknown_exception as e:
                if precondition is None:
                    self._element_call(method, self.wait_for_exists)
                msg = str(e)
                if self.query_scope._ensure_context() and len(self.query_scope.iframes()) > 0:
                    msg += '; Maybe look in an iframe?'
                custom_attributes = []
                if self.locator:
                    custom_attributes = self.locator.selector_builder.custom_attributes
                if custom_attributes:
                    msg += '; Nerodia treated {!r} as a non-HTML compliant attribute, ' \
                           'ensure that was intended'.format(custom_attributes)
                raise self._unknown_exception(msg)
            except StaleElementReferenceException:
                self.query_scope._ensure_context()
                self.reset()
                self._check_condition(precondition)
                return method()
            except (ElementNotVisibleException, ElementNotInteractableException):
                if (Wait.timer.remaining_time <= 0) or \
                        (precondition not in [self.wait_for_present, self.wait_for_enabled]):
                    self._raise_present()
                continue
            except InvalidElementStateException:
                if (Wait.timer.remaining_time <= 0) or \
                        (precondition in [self.wait_for_writable, self.wait_for_enabled]):
                    self._raise_disabled()
                continue
            except NoSuchWindowException:
                raise NoMatchingWindowFoundException('browser window was closed')

    def __getattribute__(self, name):
        if search(SelectorBuilder.WILDCARD_ATTRIBUTE, name):
            return self.attribute_value(name.replace('_', '-'))
        else:
            return object.__getattribute__(self, name)
