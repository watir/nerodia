import re
from copy import copy
from itertools import islice
from time import sleep

import six
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

import nerodia
from ...exception import Error, LocatorException

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class Locator(object):
    W3C_FINDERS = {
        'css': By.CSS_SELECTOR,
        'link': By.LINK_TEXT,
        'link_text': By.LINK_TEXT,
        'partial_link_text': By.PARTIAL_LINK_TEXT,
        'tag_name': By.TAG_NAME,
        'xpath': By.XPATH
    }

    def __init__(self, query_scope, selector, selector_builder, element_validator):
        self.query_scope = query_scope  # either element or browser
        self.selector = selector
        self.selector_builder = selector_builder
        self.element_validator = element_validator
        self.normalized_selector = None
        self.driver_scope = None

    def locate(self):
        try:
            elements = self._using_selenium('first')
            return elements if elements else self._using_nerodia('first')
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def locate_all(self):
        if 'element' in self.selector:
            return [self.selector.get('element')]

        elements = self._using_selenium('all')
        return elements if elements else self._using_nerodia('all')

    # private

    def _using_selenium(self, filter='first'):
        selector = copy(self.selector)

        tag = selector.pop('tag_name', None)
        if len(self.selector) > 1:
            return

        how = list(selector)[0] if selector else 'tag_name'
        what = list(selector.values())[0] if selector else tag

        if not self._wd_is_supported(how, what, tag):
            return

        if filter == 'all':
            return self._locate_elements(how, what)
        else:
            return self._locate_element(how, what)

    def _using_nerodia(self, filter='first'):
        selector = copy(self.selector)
        if 'index' in self.selector and filter == 'all':
            raise ValueError("can't locate all elements by 'index'")

        self.driver_scope = self.driver_scope or self.query_scope.wd

        built = self.selector_builder.build(selector)
        self._validate_built_selector(built)

        wd_locator = {}
        values_to_match = {}
        for key, value in built.items():
            if key in ['css', 'xpath', 'link_text', 'partial_link_text']:
                wd_locator[key] = value
            else:
                values_to_match[key] = value

        if filter == 'all' or len(values_to_match) > 0:
            return self._locate_matching_elements(wd_locator, values_to_match, filter)
        else:
            first_key, first_value = list(wd_locator.items())[0]
            return self._locate_element(first_key, first_value, self.driver_scope)

    def _validate_built_selector(self, built):
        if not built:
            msg = "{} was unable to build selector from {}".format(self.selector_builder.__class__,
                                                                   self.selector)
            raise LocatorException(msg)

    def _fetch_value(self, element, how):
        if how == 'text':
            return element.text
        elif how == 'visible':
            return element.is_displayed()
        elif how == 'visible_text':
            return element.text
        elif how == 'tag_name':
            return element.tag_name.lower()
        elif how == 'href':
            href = element.get_attribute('href')
            return href and href.strip()
        else:
            return element.get_attribute(how.replace('_', '-')) or ''

    def _matching_labels(self, elements, values, scope):
        from nerodia.elements.html_elements import LabelCollection
        from nerodia.elements.input import Input
        label_key = 'label_element' if 'label_element' in values else 'visible_label_element'
        label_value = values.pop('label_element', None) or values.pop('visible_label_element', None)
        locator_key = label_key.replace('label', 'text').replace('_element', '')
        matching = []
        for label in LabelCollection(scope, {'tag_name': 'label'}):
            if self._matches_values(label.wd, {locator_key: label_value}):
                label_for = label.attribute('htmlFor')
                input = Input(scope, {'id': label_for}) if label_for else label.input()
                if input.wd in elements:
                    matching.append(input.wd)
        return matching

    def _matching_elements(self, elements, values, filter='first'):
        if filter == 'first':
            idx = self._element_index(elements, values)
            counter = 0

            # Generator + slice to avoid fetching values for elements that will be discarded
            matches = []
            for element in elements:
                counter += 1
                if self._matches_values(element, values) is not False:
                    matches.append(element)
            try:
                val = list(islice(matches, idx + 1))[idx]
                nerodia.logger.debug('Iterated through {} elements to locate '
                                     '{}'.format(counter, self.selector))
                return val
            except IndexError:
                return None
        else:
            nerodia.logger.debug('Iterated through {} elements to locate all '
                                 '{}'.format(len(elements), self.selector))
            return [el for el in elements if self._matches_values(el, values)]

    def _element_index(self, elements, values):
        idx = values.pop('index', 0)
        if idx < 0:
            elements.reverse()
            idx = abs(idx) - 1
        return idx

    def _matches_values(self, element, values):
        def check_match(how, what):
            if how == 'tag_name' and isinstance(what, six.string_types):
                return self.element_validator.validate(element, what)
            else:
                val = self._fetch_value(element, how)
                if isinstance(what, (Pattern, str)):
                    val_match = re.search(what, val) is not None
                else:
                    val_match = False
                return what == val or val_match

        matches = all(check_match(how, what) for how, what in values.items())

        if values.get('text'):
            self._text_regexp_deprecation(element, values, matches)

        return matches

    def _text_regexp_deprecation(self, element, selector, matches):
        from nerodia.elements.element import Element
        new_element = Element(self.query_scope, {'element': element})
        text_content = new_element._execute_js('getTextContent', element).strip()
        text_selector = selector.get('text', '')
        text_content_matches = re.search(text_selector, text_content) is not None
        if matches != text_content_matches:
            key = 'text' if 'text' in self.selector else 'label'
            nerodia.logger.deprecate('Using {!r} locator with RegExp: {!r} to match an element '
                                     'that includes hidden '
                                     'text'.format(key, text_selector.pattern),
                                     'visible_{}'.format(key),
                                     ids=['text_regexp'])

    def _locate_element(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_element(self._wd_finder(how), what)

    def _locate_elements(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_elements(self._wd_finder(how), what)

    def _wd_finder(self, how):
        return self.W3C_FINDERS.get(how, how)

    def _locate_matching_elements(self, selector, values, filter):
        retries = 0
        while True:
            try:
                if len(selector) > 0:
                    key, value = list(selector.items())[0]
                    elements = self._locate_elements(key, value, self.driver_scope) or []
                else:
                    elements = []
                if 'label_element' in values or 'visible_label_element' in values:
                    elements = self._matching_labels(elements, values, self.query_scope)
                return self._matching_elements(elements, values, filter=filter)
            except StaleElementReferenceException:
                retries += 1
                sleep(0.5)
                if retries < 2:
                    continue
                target = 'element collection' if filter == 'all' else 'element'
                raise Error('Unable to locate {} from {} due to changing '
                            'page'.format(target, self.selector))

    def _wd_is_supported(self, how, what, tag):
        if how not in self.W3C_FINDERS:
            return False
        if type(what) not in nerodia._str_types:
            return False

        if how in ['partial_link_text', 'link_text', 'link']:
            nerodia.logger.deprecate('{} locator'.format(how), 'visible_text', ids=['link_text'])
            if tag in ['link', None]:
                return True
            raise Exception('Can not use {} locator to find a {} element'.format(how, what))
        elif how == 'tag_name':
            return True
        else:
            if tag:
                return False
        return True
