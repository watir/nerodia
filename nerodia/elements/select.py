import re

import six

import nerodia
from nerodia.exception import Error, NoValueFoundException, ObjectDisabledException, \
    UnknownObjectException
from nerodia.wait.wait import TimeoutError
from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement
from ..wait.wait import Wait

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


@six.add_metaclass(MetaHTMLElement)
class Select(HTMLElement):
    def clear(self):
        """ Clears all selected options """
        if not self.multiple:
            raise Error('you can only clear multi-selects')

        for option in self.selected_options:
            option.click()

    def includes(self, term):
        """
        Returns True if the select list has at least one option where text or label matches the
        given value
        :param term: string or regex to match against the option
        :rtype: bool
        """
        return self.option(text=term).exists or self.option(label=term).exists

    def select(self, *terms):
        """
        Select the option whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param terms: string or regex or list to match against the option
        :return: The text of the option selected. If multiple options match, returns the first match
        :rtype: str
        """
        if len(terms) > 1 or isinstance(terms[0], list):
            return [self._select_all_by(t) for t in self._flatten(terms)][0]
        else:
            return [self._select_by(t) for t in self._flatten(terms)][0]

    def select_all(self, *terms):
        """
        Select all the options whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param term: string or regex or list to match against the option
        :return: The text of the first option selected.
        :rtype: str
        """
        nerodia.logger.deprecate('Select.select_all', 'Select.select with list instance',
                                 ids=['select_all'])
        return [self._select_all_by(t) for t in self._flatten(terms)][0]

    def js_select(self, *terms):
        """
        Uses JavaScript to select the option whose text matches the given string.
        :param term: string or regex or list to match against the option
        """
        if len(terms) > 1 or isinstance(terms[0], list):
            return [self._js_select_by(t, 'multiple') for t in self._flatten(terms)][0]
        else:
            return [self._js_select_by(t, 'single') for t in self._flatten(terms)][0]

    def js_select_all(self, *terms):
        """
        Uses JavaScript to select all options whose text matches the given string.
        :param term: string or regex or list to match against the option
        """
        nerodia.logger.deprecate('Select.js_select_all', 'Select.js_select with list instance',
                                 ids=['select_all'])
        return [self._js_select_by(t, 'multiple') for t in self._flatten(terms)][0]

    def select_value(self, value):
        """
        Selects the option(s) whose value attribute matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param value: string or regex to match against the option
        """
        nerodia.logger.deprecate('#select_value', '#select', ids=['select_value'])
        return self._select_by(value)

    def js_select_value(self, value):
        """
        Uses JavaScript to select the option whose value attribute matches the given string
        :param value: string or regex to match against the option
        """
        return self._js_select_by(value, 'single')

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
        return self._element_call(lambda: self._execute_js('selectedOptions', self))

    # private

    def _select_by(self, term):
        found = self._find_options('value', term)
        if len(found) > 1:
            nerodia.logger.deprecate('Selecting Multiple Options with Select.select using a str or '
                                     'regex value',
                                     'Select.select with the desired values in a list instance',
                                     ids=['select_by'])
        return self._select_matching(found)

    def _js_select_by(self, term, number):
        if isinstance(term, Pattern):
            js_rx = term.pattern
            js_rx = js_rx.replace('\\A', '^', 1)
            js_rx = js_rx.replace('\\Z', '$', 1)
            js_rx = js_rx.replace('\\z', '$', 1)
            js_rx = re.sub(r'\(\?#.+\)', '', js_rx)
            js_rx = re.sub(r'\(\?-\w+:', '(', js_rx)
        elif type(term) in [six.text_type, six.binary_type]:
            js_rx = '^{}$'.format(term)
        else:
            raise TypeError('expected String or Regexp, got {}'.format(term))

        for way in ['text', 'label', 'value']:
            self._element_call(lambda: self._execute_js('selectOptions{}'.format(way.capitalize()),
                                                        self, js_rx, str(number)))
            if self._is_matching_option(way, term):
                return self.selected_options[0].text

        self._raise_no_value_found(term)

    def _is_matching_option(self, how, what):
        for opt in self.selected_options:
            value = getattr(opt, how)
            if (type(what) in [six.text_type, six.binary_type] and value == what) or \
                    (type(what) not in [six.text_type, six.binary_type] and re.search(what, value)):
                if opt.enabled:
                    return True
                raise ObjectDisabledException('option matching {} by {} on {}'
                                              ' is disabled'.format(what, how, self))

    def _select_all_by(self, term):
        if not self.multiple:
            raise Error('you can only use #select_all on multi-selects')

        found = self._find_options('text', term)
        return self._select_matching(found)

    def _find_options(self, how, term):
        types = [six.text_type, six.binary_type, int, Pattern]
        found = []

        def func(sel):
            if type(term) in types:
                collection = sel.options(value=term) if how == 'value' else []
                if not list(collection):
                    collection = sel.options(text=term)
                if not list(collection):
                    collection = sel.options(label=term)
                if collection:
                    found.append(collection)
                    return False
                else:
                    return not found and nerodia.relaxed_locate
            else:
                raise TypeError('expected {!r}, got {}:{}'.format(types, term, term.__class__))

        try:
            Wait.until_not(func, object=self)
            if found:
                return found[0]
            self._raise_no_value_found(term)
        except TimeoutError:
            self._raise_no_value_found(term)

    def _raise_no_value_found(self, term):
        raise NoValueFoundException('{} not found in {}'.format(term, self))

    def _select_matching(self, elements):
        if not self.multiple:
            elements = elements[:1]
        for element in elements:
            if not element.is_selected:
                element.click()
        return '' if elements[0].stale else elements[0].text
