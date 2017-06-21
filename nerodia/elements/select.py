import re

import six

from nerodia.exception import Error, NoValueFoundException, UnknownObjectException
from nerodia.wait.wait import TimeoutError
from .html_elements import HTMLElement
from .option import Option
from ..meta_elements import MetaHTMLElement
from ..wait.wait import Wait


@six.add_metaclass(MetaHTMLElement)
class Select(HTMLElement):
    def clear(self):
        """ Clears all selected options """
        if not self.multiple:
            raise Error('you can only clear multi-selects')

        for option in self.options():
            if option.selected:
                self.click_option(option)

    def options(self, *args, **kwargs):
        """
        Gets all the options in the select list

        :rtype: nerodia.elements.option.OptionColletion
        """
        return self._element_call(lambda: super(Select, self).options(*args, **kwargs),
                                  self.wait_for_exists)

    def includes(self, term):
        """
        Returns True if the select list has at least one option where text or label matches the
        given value
        :param term: string or regex to match against the option
        :rtype: bool
        """
        def func():
            elements = self.el.find_elements_by_css_selector('option')
            for e in elements:
                text = e.text
                label = e.get_attribute('label')
                if term in [text, label] or re.search(term, text) or re.search(term, label):
                    return True
            return False
        return self._element_call(func)

    def select(self, term):
        """
        Select the option(s) whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param term: string or regex to match against the option
        :return:
        """
        self._select_by('text', term)

    def select_value(self, value):
        """
        Selects the option(s) whose value attribute matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param value: string or regex to match against the option
        """
        self._select_by('value', value)

    def is_selected(self, term):
        """
        Returns True if any of the selected options' text or label matches the given value
        :param term: string or regex to match against the option
        :rtype: bool
        :raises: UnknownObjectException
        """
        def func():
            elements = self.el.find_elements_by_css_selector('option')
            for e in elements:
                text = e.text
                label = e.get_attribute('label')
                if term in [text, label] or re.search(term, text) or re.search(term, label):
                    if e.is_selected():
                        return True
            return False
        result = self._element_call(func)
        if result is not True:
            raise UnknownObjectException('Unable to locate option matching {}'.format(term))
        return result

    @property
    def value(self):
        """
        Returns the value of the first selected option in the select list
        Returns None if no option is selected
        :rtype: str or None
        """
        selected = self.selected_options
        return selected[0].value if selected else None

    @property
    def text(self):
        # Returns the text of the first selected option in the select list
        # Returns nil if no option is selected
        # :rtype: str or None
        selected = self.selected_options
        return selected[0].text if selected else None

    @property
    def selected_options(self):
        """
        Returns an array of currently selected options
        :rtype: list[nerodia.elements.option.Option]
        """
        script = 'var result = [];' \
                 'var options = arguments[0].options;' \
                 'for (var i = 0; i < options.length; i++) {' \
                 '  var option = options[i];' \
                 '  if (option.selected) { result.push(option) }' \
                 '}' \
                 'return result;'
        return self._element_call(lambda: self.query_scope.execute_script(script, self.el))

    # private

    def _select_by(self, how, term):
        found = []

        def func(sel):
            if type(term) in [str, int, re._pattern_type]:
                opt = {how: term}
                found.extend(sel.options(**opt))
                if not list(found):
                    found.extend(self.options(label=term))
            else:
                raise TypeError('expected str, got {}:{}'.format(term, term.__class__))

            return found

        try:
            Wait.until(func, object=self)
        except TimeoutError:
            self._no_value_found(term)
        return self._select_matching(found)

    def select_matching(self, elements):
        if not self.multiple:
            elements = elements[:1]
        for element in elements:
            if not element.is_selected():
                self._click_option(element)
        return elements[0].text if elements[0].exist else ''

    def _matches_regexp(self, how, element, exp):
        if how == 'text':
            return (re.search(exp, self.el.text) or re.search(exp, self.el.label)) \
                is not None
        elif how == 'value':
            return re.search(exp, element.value) is not None
        else:
            raise Error('unknown how: {}'.format(how))

    def _click_option(self, element):
        if not isinstance(element, Option):
            element = Option(self, element=element)
        element.click()

    @staticmethod
    def _no_value_found(arg, msg=None):
        raise (NoValueFoundException(msg or '{} not found in select list'.format(arg)))
