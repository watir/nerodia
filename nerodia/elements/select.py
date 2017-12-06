import re

import six

import nerodia
from nerodia.exception import Error, NoValueFoundException, UnknownObjectException
from nerodia.wait.wait import TimeoutError
from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement
from ..wait.wait import Wait


@six.add_metaclass(MetaHTMLElement)
class Select(HTMLElement):
    def clear(self):
        """ Clears all selected options """
        if not self.multiple:
            raise Error('you can only clear multi-selects')

        for option in self.selected_options:
            option.click()

    def options(self, *args, **kwargs):
        """ Gets all the options in the select list
        :rtype: list[nerodia.elements.option.Option]
        """
        return self._element_call(lambda: super(Select, self).options(*args, **kwargs),
                                  self.wait_for_present)

    def includes(self, term):
        """
        Returns True if the select list has at least one option where text or label matches the
        given value
        :param term: string or regex to match against the option
        :rtype: bool
        """
        return self.option(text=term).exists or self.option(label=term).exists

    def select(self, term):
        """
        Select the option whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param term: string or regex to match against the option
        :return: The text of the option selected. If multiple options match, returns the first match
        :rtype: str
        """
        return self._select_by('text', term)

    def select_all(self, term):
        """
        Select all the options whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param term: string or regex to match against the option
        :return: The text of the first option selected.
        :rtype: str
        """
        return self._select_all_by('text', term)

    def select_value(self, value):
        """
        Selects the option(s) whose value attribute matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param value: string or regex to match against the option
        """
        return self._select_by('value', value)

    def is_selected(self, term):
        """
        Returns True if any of the selected options' text or label matches the given value
        :param term: string or regex to match against the option
        :rtype: bool
        :raises: UnknownObjectException
        """
        by_text = self.options(text=term)
        if any(option.is_selected for option in by_text):
            return True

        by_label = self.options(label=term)
        if any(option.is_selected for option in by_label):
            return True

        if len(by_text) + len(by_label) != 0:
            return False

        raise UnknownObjectException('Unable to locate option matching {}'.format(term))

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
        found = self._find_options(how, term)
        if found:
            if len(found) > 1:
                nerodia.logger.deprecate('Selecting Multiple Options with #select', '#select_all')
            return self._select_matching(found)

        raise NoValueFoundException('{} not found in select list'.format(term))

    def _select_all_by(self, how, term):
        if not self.multiple:
            raise Error('you can only use #select_all on multi-selects')

        found = self._find_options(how, term)
        if found:
            return self._select_matching(found)

        raise NoValueFoundException('{} not found in select list'.format(term))

    def _find_options(self, how, term):
        types = [six.text_type, six.binary_type, int, re._pattern_type]
        found = []

        def func(sel):
            elements = []
            if type(term) in types:
                opt = {how: term}
                elements.extend(sel.options(**opt))
                if not list(elements):
                    elements.extend(sel.options(label=term))
                if elements:
                    found.extend(elements)
                    return False
                else:
                    return not found and nerodia.relaxed_locate
            else:
                raise TypeError('expected {!r}, got {}:{}'.format(types, term, term.__class__))

        try:
            Wait.until_not(func, object=self)
            if found:
                return found
            raise NoValueFoundException('{} not found in select list'.format(term))
        except TimeoutError:
            raise NoValueFoundException('{} not found in select list'.format(term))

    def _select_matching(self, elements):
        if not self.multiple:
            elements = elements[:1]
        for element in elements:
            if not element.is_selected:
                element.click()
        return elements[0].text if elements[0].exist else ''

    def _matches_regexp(self, how, element, exp):
        if how == 'text':
            return (re.search(exp, self.el.text) or re.search(exp, self.el.label)) \
                is not None
        elif how == 'value':
            return re.search(exp, element.value) is not None
        else:
            raise Error('unknown how: {}'.format(how))
