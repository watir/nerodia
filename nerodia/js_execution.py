import re
from time import sleep

import nerodia


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

    def flash(self, preset='default', color='red', flashes=10, delay=0.05):
        """
        Flashes (change background color to a new color and back a few times) element

        :param preset: choice from preset values
        :type param: str:
        :param color: what color or colors to flash with
        :type color: str or list
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
        presets = {
            'fast': {'delay': 0.04},
            'slow': {'delay': 0.2},
            'long': {'flashes': 5, 'delay': 0.5},
            'rainbow': {'flashes': 5, 'color': ['red', 'orange', 'yellow', 'green', 'blue',
                                                'indigo', 'violet']}
        }
        # TODO: remove this sooner than later
        if preset in presets:
            return self.flash(**presets[preset])
        elif isinstance(color, int):
            nerodia.logger.deprecate('Using color as first argument to #flash',
                                     'Specify with keyword or add preset')
            if isinstance(flashes, float):
                delay = flashes
            flashes = color
            color = preset

        background_color = self.style('background-color')
        original_color = background_color
        if not background_color:
            background_color = 'white'

        if not isinstance(color, list):
            colors = [color]
        else:
            colors = color[:]
        colors.append(background_color)

        for next_color in colors * flashes:
            self._element_call(lambda: self._execute_js('backgroundColor', self.el, next_color))
            sleep(delay)

        self._element_call(lambda: self._execute_js('backgroundColor', self.el, original_color))

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

    @property
    def selected_text(self):
        """
        Returns selected text

        :Example:

        browser.li(id='non_link_1').selected_text
        """
        return self._element_call(lambda: self._execute_js('selectedText'))
