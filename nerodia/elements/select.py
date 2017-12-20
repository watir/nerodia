import re

import six

import nerodia
from nerodia.exception import Error, NoValueFoundException, UnknownObjectException, \
    ObjectDisabledException
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

    def select(self, *terms):
        """
        Select the option whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param terms: string or regex or list to match against the option
        :return: The text of the option selected. If multiple options match, returns the first match
        :rtype: str
        """
        return [self._select_by(t) for t in self._flatten(terms)][0]

    def select_all(self, *terms):
        """
        Select all the options whose text or label matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param term: string or regex or list to match against the option
        :return: The text of the first option selected.
        :rtype: str
        """
        return [self._select_all_by(t) for t in self._flatten(terms)][0]

    def js_select(self, *terms):
        """
        Uses JavaScript to select the option whose text matches the given string.
        :param term: string or regex or list to match against the option
        """
        return [self._js_select_by(t, 'single') for t in self._flatten(terms)][0]

    def js_select_all(self, *terms):
        """
        Uses JavaScript to select all options whose text matches the given string.
        :param term: string or regex or list to match against the option
        """
        return [self._js_select_by(t, 'multiple') for t in self._flatten(terms)][0]

    def select_value(self, value):
        """
        Selects the option(s) whose value attribute matches the given string
        If this is a multi-select and several options match the value given, all will be selected
        :param value: string or regex to match against the option
        """
        nerodia.logger.deprecate('#select_value', '#select')
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
        if found:
            if len(found) > 1:
                nerodia.logger.deprecate('Selecting Multiple Options with #select', '#select_all')
            return self._select_matching(found)

        raise NoValueFoundException('{} not found in select list'.format(term))

    def _js_select_by(self, term, number):
        if isinstance(term, re._pattern_type):
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

        raise NoValueFoundException('{} not found in select list'.format(term))

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
        if found:
            return self._select_matching(found)

        raise NoValueFoundException('{} not found in select list'.format(term))

    def _find_options(self, how, term):
        types = [six.text_type, six.binary_type, int, re._pattern_type]
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

    @staticmethod
    def _flatten(term):
        for x in term:
            if isinstance(x, list):
                for y in x:
                    yield y
            else:
                yield x
