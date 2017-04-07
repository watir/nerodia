from warnings import warn

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

import watir_snake
from watir_snake.browser import Browser
from ..elements.iframe import IFrame
from ..exception import UnknownObjectException, UnknownFrameException, Error, \
    ObjectDisabledException, ObjectReadOnlyException
from ..wait.timer import Timer
from ..wait.wait import Wait
from ..wait.wait import Waitable, TimeoutError


# class Element(AttributeHelper, Container, EventuallyPresent, Waitable, Adjacent):
class Element(Waitable):
    pass

    def __init__(self, query_scope, selector):
        self.query_scope = query_scope
        if not type(selector) == dict:
            raise TypeError('invalid argument: {!r}'.format(selector))
        self.element = selector.pop('element', None)
        self.selector = selector
        self.keyword = None
        self.id = None
        self.class_name = None
        # Temporarily add 'id' and 'class_name' since they're no longer specified in the HTML spec
        # self.attribute(str, 'id', 'id')  # TODO
        # self.attribute(str, 'class_name', 'className')  # TODO

    @property
    def exists(self):
        """
        Returns True if element exists, False otherwise
        :rtype: bool
        """
        try:
            # self.assert_exists()  # TODO
            return True
        except (UnknownObjectException, UnknownFrameException):
            return False

    exist = exists

    def __repl__(self):
        string = '#<#{}: '.format(self.__class__.__name__)
        if self.keyword:
            string += 'keyword: {} '.format(self.keyword)
        string += 'located: {}; '.format(self.element is not None)
        if not self.selector:
            string += '{element: (selenium element)}'
        else:
            string += self._selector_string
        string += '>'
        return string

    def __eq__(self, other):
        """
        Returns True if two elements are equal
        :param other: other element to compare
        :rtype: bool
        """
        return self.wd if type(other) == self.__class__ else other.wd

    eql = __eq__

    def __hash__(self):
        return self.element.__hash__() if self.element else super(Element, self).__hash__()

    @property
    def text(self):
        """
        Returns the text of the element
        :rtype: str
        """
        return self._element_call(self.element.text)

    def tag_name(self):
        """
        Returns the tag name of the element
        :rtype: str
        """
        return self._element_call(self.element.tag_name.lower)

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
                action.click(self.element)
                for mod in modifiers:
                    action.key_up(mod)
                action.perform()
            else:
                self.element.click()
        self._element_call(method, self._wait_for_enabled)
        self.browser.after_hooks.run()

    def double_click(self):
        """
        Double clicks the element.
        Note that browser support may vary.

        :Example: Double-click an element

        browser.element(name='new_user_button').double_click()
        """
        self._element_call(lambda _: ActionChains(self.driver).double_click(self.element)
                           .perform(), self._wait_for_present)
        self.browser.after_hooks.run()

    def right_click(self):
        """
        Right clicks the element
        Note that browser support may vary

        :Example: Right click an element

        browser.element(name='new_user_button').right_click()
        """
        self._element_call(lambda _: ActionChains(self.driver).context_click(self.element)
                           .perform(), self._wait_for_present)
        self.browser.after_hooks.run()

    def hover(self):
        """
        Moves the mouse to the middle of this element
        Note that browser support may vary

        :Example: Hover over an element

        browser.element(name='new_user_button').hover()
        """
        self._element_call(lambda _: ActionChains(self.driver).move_to_element(self.element)
                           .perform(), self._wait_for_present)
        self.browser.after_hooks.run()

    def drag_and_drop_on(self, other):
        """
        Drag and drop this element on to another element instance
        Note that browser support may vary

        :Example: Drag an element onto another

        a = browser.div(id='draggable')
        b = browser.div(id='droppable')
        a.drag_and_drop_on(b)
        """
        self._assert_is_element(other)
        
        self._element_call(lambda _: ActionChains(self.driver).drag_and_drop(self.element, other.wd)
                           .perform(), self._wait_for_present)
    #
    # #
    # # Drag and drop this element by the given offsets.
    # # Note that browser support may vary.
    # #
    # # @example
    # #   browser.div(id: "draggable").drag_and_drop_by 100, -200
    # #
    # # @param [Integer] right_by
    # # @param [Integer] down_by
    # #
    #
    # def drag_and_drop_by(right_by, down_by)
    #   element_call(:wait_for_present) do
    #     driver.action.
    #            drag_and_drop_by(@element, right_by, down_by).
    #            perform
    #   end
    # end
    #
    # #
    # # Flashes (change background color far a moment) element.
    # #
    # # @example
    # #   browser.text_field(name: "new_user_first_name").flash
    # #
    #
    # def flash
    #   background_color = style("backgroundColor")
    #   element_color = driver.execute_script("arguments[0].style.backgroundColor", @element)
    #
    #   10.times do |n|
    #     color = (n % 2 == 0) ? "red" : background_color
    #     driver.execute_script("arguments[0].style.backgroundColor = '#{color}'", @element)
    #   end
    #
    #   driver.execute_script("arguments[0].style.backgroundColor = arguments[1]", @element, element_color)
    #
    #   self
    # end
    #
    # #
    # # Returns value of the element.
    # #
    # # @return [String]
    # #
    #
    # def value
    #   attribute_value('value') || ''
    # rescue Selenium::WebDriver::Error::InvalidElementStateError
    #   ''
    # end
    #
    # #
    # # Returns given attribute value of element.
    # #
    # # @example
    # #   browser.a(id: "link_2").attribute_value "title"
    # #   #=> "link_title_2"
    # #
    # # @param [String] attribute_name
    # # @return [String, nil]
    # #
    #
    # def attribute_value(attribute_name)
    #   element_call { @element.attribute attribute_name }
    # end
    #
    # #
    # # Returns outer (inner + element itself) HTML code of element.
    # #
    # # @example
    # #   browser.div(id: 'foo').outer_html
    # #   #=> "<div id=\"foo\"><a href=\"#\">hello</a></div>"
    # #
    # # @return [String]
    # #
    #
    # def outer_html
    #   element_call { execute_atom(:getOuterHtml, @element) }.strip
    # end
    #
    # alias_method :html, :outer_html
    #
    # #
    # # Returns inner HTML code of element.
    # #
    # # @example
    # #   browser.div(id: 'foo').inner_html
    # #   #=> "<a href=\"#\">hello</a>"
    # #
    # # @return [String]
    # #
    #
    # def inner_html
    #   element_call { execute_atom(:getInnerHtml, @element) }.strip
    # end
    #
    # #
    # # Sends sequence of keystrokes to element.
    # #
    # # @example
    # #   browser.text_field(name: "new_user_first_name").send_keys "Watir", :return
    # #
    # # @param [String, Symbol] *args
    # #
    #
    # def send_keys(*args)
    #   element_call(:wait_for_writable) { @element.send_keys(*args) }
    # end
    #
    # #
    # # Focuses element.
    # # Note that Firefox queues focus events until the window actually has focus.
    # #
    # # @see http://code.google.com/p/selenium/issues/detail?id=157
    # #
    #
    # def focus
    #   element_call { driver.execute_script "return arguments[0].focus()", @element }
    # end
    #
    # #
    # # Returns true if this element is focused.
    # #
    # # @return [Boolean]
    # #
    #
    # def focused?
    #   element_call { @element == driver.switch_to.active_element }
    # end
    #
    # #
    # # Simulates JavaScript events on element.
    # # Note that you may omit "on" from event name.
    # #
    # # @example
    # #   browser.button(name: "new_user_button").fire_event :click
    # #   browser.button(name: "new_user_button").fire_event "mousemove"
    # #   browser.button(name: "new_user_button").fire_event "onmouseover"
    # #
    # # @param [String, Symbol] event_name
    # #
    #
    # def fire_event(event_name)
    #   event_name = event_name.to_s.sub(/^on/, '').downcase
    #
    #   element_call { execute_atom :fireEvent, @element, event_name }
    # end

    @property
    def driver(self):
        return self.query_scope.driver

    def wd(self):
        self._assert_exists()
        return self.element

    #
    # #
    # # Returns true if this element is visible on the page.
    # # Raises exception if element does not exist
    # #
    # # @return [Boolean]
    # #
    #
    # def visible?
    #   element_call(:assert_exists) { @element.displayed? }
    # end
    #
    # #
    # # Returns true if this element is present and enabled on the page.
    # #
    # # @return [Boolean]
    # # @see Watir::Wait
    # #
    #

    @property
    def enabled(self):
        return self._element_call(lambda _: self.element.enabled, self._assert_exists)

    # #
    # # Returns true if the element exists and is visible on the page.
    # # Returns false if element does not exist or exists but is not visible
    # #
    # # @return [Boolean]
    # # @see Watir::Wait
    # #
    #
    # def present?
    #   visible?
    # rescue UnknownObjectException
    #   false
    # end
    #
    # #
    # # Returns given style property of this element.
    # #
    # # @example
    # #   browser.button(value: "Delete").style           #=> "border: 4px solid red;"
    # #   browser.button(value: "Delete").style("border") #=> "4px solid rgb(255, 0, 0)"
    # #
    # # @param [String] property
    # # @return [String]
    # #
    #
    # def style(property = nil)
    #   if property
    #     element_call { @element.style property }
    #   else
    #     attribute_value("style").to_s.strip
    #   end
    # end
    #
    # #
    # # Cast this Element instance to a more specific subtype.
    # #
    # # @example
    # #   browser.element(xpath: "//input[@type='submit']").to_subtype
    # #   #=> #<Watir::Button>
    # #
    #
    # def to_subtype
    #   elem = wd()
    #   tag_name = elem.tag_name.downcase
    #
    #   klass = nil
    #
    #   if tag_name == "input"
    #     klass = case elem.attribute(:type)
    #       when *Button::VALID_TYPES
    #         Button
    #       when 'checkbox'
    #         CheckBox
    #       when 'radio'
    #         Radio
    #       when 'file'
    #         FileField
    #       else
    #         TextField
    #       end
    #   else
    #     klass = Watir.element_class_for(tag_name)
    #   end
    #
    #   klass.new(@query_scope, element: elem)
    # end
    #

    @property
    def browser(self):
        """
        Returns browser
        :rtype: watir_snake.browser.Browser
        """
        return self.query_scope.browser

    @property
    def stale(self):
        """
        Returns True if a previously located element is no longer attached to the DOM
        :rtype: bool
        """
        try:
            if self.element is None:
                raise Error('Can not check staleness of unused element')
            self.element.enabled # any wire call will check for staleness
            return False
        except StaleElementReferenceException:
            return True

    def reset(self):
        self.element = None

    # Private

    def _wait_for_exists(self):
        if not watir_snake.relaxed_locate:
            return self._assert_exists()
        if self.exists:  # Performance shortcut
            return

        try:
            self.query_scope.wait_for_exists()
            self.wait_until(self.exists)
        except TimeoutError:
            if watir_snake.default_timeout != 0:
                warn('This code has slept for the duration of the default timeout waiting for an '
                     'Element to exist. If the test is still passing, consider using '
                     'Element#exists instead of catching UnknownObjectException')
            raise UnknownObjectException('timed out after {} seconds, waiting for {} to be '
                                         'located'.format(watir_snake.default_timeout, self))

    def _wait_for_present(self):
        if not watir_snake.relaxed_locate:
            return self._assert_exists()

        try:
            self.query_scope.wait_for_present()
            self.wait_until(self.exists)
        except TimeoutError:
            if watir_snake.default_timeout != 0:
                warn('This code has slept for the duration of the default timeout waiting for an '
                     'Element to exist. If the test is still passing, consider using '
                     'Element#present instead of catching UnknownObjectException')
            raise UnknownObjectException('timed out after {} seconds, waiting for {} to be '
                                         'located'.format(watir_snake.default_timeout, self))

    def _wait_for_enabled(self):
        if not watir_snake.relaxed_locate:
            return self._assert_enabled()
        self._wait_for_present()

        try:
            self.wait_until(self.enabled)
        except TimeoutError:
            raise ObjectDisabledException('element present, but timed out after {} seconds, '
                                          'waiting for {} to be '
                                          'enabled'.format(watir_snake.default_timeout, self))


    def wait_for_writable(self):
        if not watir_snake.relaxed_locate:
            return self._assert_writable()
        self._wait_for_enabled()

        try:
            self.wait_until(lambda _: not getattr(self, 'read_only', None) or not self.read_only)
        except TimeoutError:
            raise ObjectReadOnlyException('element present and enabled, but timed out after {} '
                                          'seconds, waiting for {} to not be '
                                          'readonly'.format(watir_snake.default_timeout, self))

    def _assert_exists(self):
        """
        Ensure that the element exists, making sure that it is not stale and located if necessary
        """
        if self.element and not self.selector:
            self._ensure_context()
            if self.stale:
                self.reset()
        elif self.element and not self.stale:
            return
        else:
            self.element = self._locate()

        self._assert_element_found()

    def _assert_element_found(self):
        if self.element is None:
            raise UnknownObjectException('unable to locate element: {}'.format(self))

    def _locate(self):
        pass  # TODO
        # ensure_context
        #
        # element_validator = element_validator_class.new
        # selector_builder = selector_builder_class.new(@query_scope, @selector, self.class.attribute_list)
        # locator = locator_class.new(@query_scope, @selector, selector_builder, element_validator)
        #
        # locator.locate

    @property
    def _selector_string(self):
        if type(self.query_scope) == Browser:
            return self.selector.__repl__()
        else:
            return '{} --> {}'.format(self.query_scope.selector_string, self.selector)

    # private

    # def unknown_exception
    #   Watir::Exception::UnknownObjectException
    # end
    #
    # def locator_class
    #   Kernel.const_get("#{Watir.locator_namespace}::#{element_class_name}::Locator")
    # rescue NameError
    #   Kernel.const_get("#{Watir.locator_namespace}::Element::Locator")
    # end
    #
    # def element_validator_class
    #   Kernel.const_get("#{Watir.locator_namespace}::#{element_class_name}::Validator")
    # rescue NameError
    #   Kernel.const_get("#{Watir.locator_namespace}::Element::Validator")
    # end
    #
    # def selector_builder_class
    #   Kernel.const_get("#{Watir.locator_namespace}::#{element_class_name}::SelectorBuilder")
    # rescue NameError
    #   Kernel.const_get("#{Watir.locator_namespace}::Element::SelectorBuilder")
    # end
    #
    # def element_class_name
    #   self.class.name.split('::').last
    # end
    #

    # Ensure the driver is in the desired browser context
    def _ensure_context(self):
        if type(self.query_scope) == IFrame:
            self.query_scope.switch_to()
        else:
            self.query_scope.assert_exists()

    #
    # def attribute?(attribute_name)
    #   !attribute_value(attribute_name).nil?
    # end
    #

    def _assert_enabled(self):
        if not self._element_call(lambda _: self.element.enabled):
            raise ObjectDisabledException('object is disabled {}'.format(self))


    def _assert_writable(self):
        self._assert_enabled()

        if getattr(self, 'read_only', None) and self.read_only:
            raise ObjectReadOnlyException('object is read only {}'.format(self))

    @classmethod
    def _assert_is_element(cls, obj):
        if not type(obj) == Element:
            raise TypeError('execpted watir_snake.elements.Element, '
                            'got {}:{}'.format(obj, obj.__class__.__name__))

    def _element_call(self, method, exist_check=None):
        exist_check = exist_check or self._wait_for_exists
        if Wait.timer.locked is None:
            Wait.timer = Timer(timeout=watir_snake.default_timeout)
        try:
            exist_check()
            return method()
        except StaleElementReferenceException:
            exist_check()
            return method()
        finally:
            if Wait.timer.locked is None:
                Wait.timer.reset()
#
# def method_missing(meth, *args, &blk)
#   method = meth.to_s
#   if method =~ Locators::Element::SelectorBuilder::WILDCARD_ATTRIBUTE
#     attribute_value(method.tr('_', '-'), *args)
#   else
#     super
#   end
# end
#
# def respond_to_missing?(meth, *)
#   Locators::Element::SelectorBuilder::WILDCARD_ATTRIBUTE === meth.to_s || super
# end
