import re
from time import sleep


class JSExecution(object):
    def execute_script(self, script, *args):
        """
        Delegates script execution to Browser or IFrame

        :param script: script to execute
        """
        return self.query_scope.execute_script(script, *args)

    def fire_event(self, event_name):
        """
        Simulates JavaScript events on element.
        Note that you may omit "on" from event name.

        :param event_name: event to fire

        :Example:

        browser.button(name: 'new_user_button').fire_event('click')
        browser.button(name: 'new_user_button').fire_event('mousemove')
        browser.button(name: 'new_user_button').fire_event('onmouseover')
        """
        event_name = re.sub(r'^on', '', event_name).lower()
        return self._element_call(lambda: self._execute_js('fireEvent', self, event_name))

    def flash(self, color='red', flashes=5, delay=0.2):
        """
        Flashes (change background color to a new color and back a few times) element

        :param color: what color to flash with
        :type color: str
        :param flashes: number of times element should be flashed
        :type flashes: int
        :param delay: how long to wait between flashes
        :type delay: int or float

        :returns: nerodia.elements.element.Element

        :Example:

        browser.li(id='non_link_1').flash()
        browser.li(id='non_link_1').flash(color='green', flashes=3, delay=0.05)
        browser.li(id='non_link_1').flash(color='yellow')
        browser.li(id='non_link_1').flash(flashes=4)
        browser.li(id='non_link_1').flash(delay=0.1)
        """
        background_color = self.style('backgroundColor')
        element_color = self._element_call(lambda: self._execute_js('backgroundColor',
                                                                    self.el)).strip()

        for n in range(flashes * 2):
            nextcolor = color if n % 2 == 0 else background_color
            self._element_call(lambda: self._execute_js('backgroundColor', self.el, nextcolor))
            sleep(delay)

        self._element_call(lambda: self._execute_js('backgroundColor', self.el, element_color))

        return self

    def focus(self):
        """
        Focuses the element
        Note that Firefox queues focus events until the window actually has focus
        """
        return self._element_call(lambda: self._execute_js('focus', self.el))

    @property
    def inner_html(self):
        """
        Returns inner HTML code of element

        :rtype: str

        :Example:

        browser.div(id='shown').inner_html
        #=> '<div id="hidden" style="display: none;">Not shown</div><div>Not hidden</div>'
        """
        return self._element_call(lambda: self._execute_js('getInnerHtml', self.el)).strip()

    @property
    def inner_text(self):
        """
        Returns inner Text code of element

        :rtype: str:

        :Example:

        browser.div(id: 'shown').inner_text
        #=> "Not hidden"
        """
        return self._element_call(lambda: self._execute_js('getInnerText', self)).strip()

    @property
    def outer_html(self):
        """
        Returns outer (inner + element itself) HTML code of element

        :rtype: str

        :Example:

        browser.div(id='shown').outer_html
        #=> '<div id="shown"><div id="hidden" style="display: none;">Not shown</div><div>Not hidden</div></div>'
        """
        return self._element_call(lambda: self._execute_js('getOuterHtml', self.el)).strip()

    html = outer_html

    @property
    def text_content(self):
        """
        Returns text content of element

        :rtype: str

        :Example:

        browser.div(id='shown').text_content
        #=> 'Not shownNot hidden'
        """
        return self._element_call(lambda: self._execute_js('getTextContent', self.el)).strip()

    def select_text(self, string):
        """
        Selects text on page (as if dragging clicked mouse across provided text)

        :param string: string to select

        :Example:

        browser.li(id='non_link_1').select_text('Non-link')
        """
        return self._element_call(lambda: self._execute_js('selectText', self.el, string))
