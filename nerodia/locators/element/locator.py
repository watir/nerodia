from copy import copy
from itertools import islice
from time import sleep

import six
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

import nerodia
from .validator import Validator
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
        self.selector = copy(selector)
        self.selector_builder = selector_builder
        self.element_validator = element_validator
        self.values_to_match = None
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
        tag = self.selector.pop('tag_name', None)
        if len(self.selector) > 1:
            return

        how = list(self.selector.keys())[0] if self.selector else 'tag_name'
        what = list(self.selector.values())[0] if self.selector else tag

        if not self._wd_is_supported(how, what, tag):
            return

        if filter == 'all':
            return self._locate_elements(how, what)
        else:
            return self._locate_element(how, what)

    def _using_nerodia(self, filter='first'):
        self._create_normalized_selector(filter)
        if self.normalized_selector is None:
            return

        built_selector = self.selector_builder.build(self.normalized_selector,
                                                     self._values_to_match)
        if not built_selector:
            raise LocatorException('{} was unable to build selector from '
                                   '{}'.format(self.selector_builder.__class__.__name__,
                                               self.normalized_selector))

        how, what = built_selector

        if filter == 'all' or len(self._values_to_match) > 0:
            return self._locate_matching_elements(how, what, filter)
        else:
            return self._locate_element(how, what, self.driver_scope)

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
        elif isinstance(how, six.string_types):
            return element.get_attribute(how.replace('_', '-')) or ''
        else:
            raise Exception('Unable to fetch value for {}'.format(how))

    def _matching_elements(self, elements, filter='first'):
        if filter == 'first':
            idx = self._element_index(elements, self._values_to_match)
            counter = 0

            # Generator + slice to avoid fetching values for elements that will be discarded
            matches = []
            for element in elements:
                counter += 1
                if self._matches_values(element, self._values_to_match) is not False:
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
            return [el for el in elements if self._matches_values(el, self._values_to_match)]

    def _element_index(self, elements, values):
        idx = values.pop('index', 0)
        if idx < 0:
            elements.reverse()
            idx = abs(idx) - 1
        return idx

    def _create_normalized_selector(self, filter):
        if self.normalized_selector is not None:
            return self.normalized_selector
        self.driver_scope = self.query_scope.wd

        self.normalized_selector = self.selector_builder.normalized_selector

        label_key = None
        if 'label' in self.normalized_selector:
            label_key = 'label'
        elif 'visible_label' in self.normalized_selector:
            label_key = 'visible_label'

        if label_key:
            self._process_label(label_key)
            if self.normalized_selector is None:
                return None

        if 'index' in self.normalized_selector and filter == 'all':
            raise ValueError("can't locate all elements by index")
        return self.normalized_selector

    @property
    def _values_to_match(self):
        if self.values_to_match is not None:
            return self.values_to_match
        self.values_to_match = {}

        # Remove locators that can never be used in XPath builder
        for how in ('visible', 'visible_text'):
            if how in self.normalized_selector:
                self.values_to_match[how] = self.normalized_selector.pop(how, None)

        if self._tag_vaildation_required(self.normalized_selector):
            self._values_to_match['tag_name'] = self.normalized_selector.get('tag_name')

        # Regexp locators currently need to be validated even if they are included in the XPath
        # builder
        # TODO: Identify Regexp that can have an exact equivalent using XPath contains (ie would
        # not require additional matching) vs approximations (ie would still require additional
        # matching)
        for how, what in self.normalized_selector.copy().items():
            if isinstance(what, Pattern):
                self.values_to_match[how] = self.normalized_selector.pop(how, None)

        if self.normalized_selector.get('index') is not None and \
                self.normalized_selector.get('adjacent') is None:
            idx = self.normalized_selector.pop('index')

            # Do not add {'index': 0} if the only value to match. This will allow using
            # #find_element instead of #find_elements
            implicit_idx_match = not self.values_to_match and idx == 0
            if not implicit_idx_match:
                self.values_to_match['index'] = idx

        return self.values_to_match

    def _process_label(self, label_key):
        regexp = isinstance(self.normalized_selector.get(label_key), Pattern)

        if (regexp or label_key == 'visible_label') and \
                self.selector_builder.should_use_label_element:

            label = self._label_from_text(label_key)
            if not label:
                self.normalized_selector = None
                return None

            _id = label.get_attribute('for')
            if _id:
                self.normalized_selector['id'] = _id
            else:
                self.driver_scope = label

    def _label_from_text(self, label_key):
        # TODO: this won't work correctly if @wd is a sub-element
        # TODO: figure out how to do this with find_element
        label_text = self.normalized_selector.pop(label_key, None)
        locator_key = label_key.replace('label', 'text')
        elements = self._locate_elements('tag_name', 'label', self.driver_scope)
        return next((e for e in elements if self._matches_values(e, {locator_key: label_text})),
                    None)

    def _matches_values(self, element, values):
        def check_match(how, what):
            if how == 'tag_name' and isinstance(what, six.string_types):
                return self.element_validator.validate(element, {'tag_name': what})
            else:
                return Validator.match_str_or_regex(what, self._fetch_value(element, how))

        matches = all(check_match(how, what) for how, what in values.items())

        if values.get('text'):
            self._text_regexp_deprecation(element, values, matches)

        return matches

    def _text_regexp_deprecation(self, element, selector, matches):
        text_selector = selector.get('text')
        if text_selector is not None:
            from nerodia.elements.element import Element
            text_content = Element(self.query_scope, {'element': element}).\
                _execute_js('getTextContent', element).strip()
            text_content_matches = Validator.match_str_or_regex(text_selector, text_content)
            if matches != text_content_matches:
                key = 'text' if 'text' in self.selector else 'label'
                nerodia.logger.deprecate('Using {!r} locator with RegExp: {!r} to match an element '
                                         'that includes hidden '
                                         'text'.format(key, text_selector.pattern),
                                         'visible_{}'.format(key),
                                         ids=['visible_text'])

    def _tag_vaildation_required(self, selector):
        return any(x in selector for x in ('css', 'xpath')) and 'tag_name' in selector

    def _locate_element(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_element(self._wd_finder(how), what)

    def _locate_elements(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_elements(self._wd_finder(how), what)

    def _wd_finder(self, how):
        return self.W3C_FINDERS.get(how, how)

    def _locate_matching_elements(self, how, what, filter):
        retries = 0
        while True:
            try:
                elements = self._locate_elements(how, what, self.driver_scope) or []
                return self._matching_elements(elements, filter=filter)
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
            nerodia.logger.deprecate('{} locator'.format(how), 'visible_text')
            if tag in ['link', None]:
                return True
            raise Exception('Can not use {} locator to find a {} element'.format(how, what))
        elif how == 'tag_name':
            return True
        else:
            if tag:
                return False
        return True
