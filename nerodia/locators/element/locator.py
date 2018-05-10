import re
from copy import copy
from itertools import islice

import six
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

import nerodia
from .validator import Validator
from ...exception import Error
from ...xpath_support import XpathSupport


class Locator(object):
    W3C_FINDERS = {
        'css': By.CSS_SELECTOR,
        'link': By.LINK_TEXT,
        'link_text': By.LINK_TEXT,
        'partial_link_text': By.PARTIAL_LINK_TEXT,
        'tag_name': By.TAG_NAME,
        'xpath': By.XPATH
    }

    # Regular expressions that can be reliably converted to xpath `contains`
    # expressions in order to optimize the locator.
    CONVERTABLE_REGEXP = re.compile(r'\A'
                                    r'([^\[\]\\^$.|?*+()]*)'  # leading literal characters
                                    r'[^|]*?'  # do not try to convert expressions with alternates
                                    r'([^\[\]\\^$.|?*+()]*)'  # trailing literal characters
                                    r'\Z',
                                    re.X)

    def __init__(self, query_scope, selector, selector_builder, element_validator):
        self.query_scope = query_scope  # either element or browser
        self.selector = copy(selector)
        self.selector_builder = selector_builder
        self.element_validator = element_validator
        self.filter_selector = None
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

        self._create_filter_selector()

        built_selector = self.selector_builder.build(self.normalized_selector.copy())
        if not built_selector:
            raise Error('internal error: unable to build Selenium selector from '
                        '{}'.format(self.normalized_selector))

        how, what = built_selector
        if how == 'xpath':
            what = self._add_regexp_predicates(what)

        if filter == 'all' or len(self.filter_selector) > 0:
            elements = self._locate_elements(how, what, self.driver_scope) or []
            return self._filter_elements(elements, filter=filter)
        else:
            return self._locate_element(how, what, self.driver_scope)

    def _validate(self, elements, tag_name):
        return all(self.element_validator.validate(el, {'tag_name': tag_name})
                   for el in elements if el is not None)

    def _fetch_value(self, element, how):
        if how == 'text':
            from nerodia.elements.element import Element
            vis = element.text
            all = Element(self.query_scope,
                          {'element': element})._execute_js('getTextContent', element).strip()
            if all != vis.strip():
                nerodia.logger.deprecate("'text' locator with RegExp values to find elements "
                                         "based on only visible text", 'visible_text')
            return vis
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

    def _filter_elements(self, elements, filter='first'):
        selector = self.filter_selector.copy()
        if filter == 'first':
            idx = selector.pop('index', 0)
            if idx < 0:
                elements.reverse()
                idx = abs(idx) - 1
            # Generator + slice to avoid fetching values for elements that will be discarded
            matches = (el for el in elements if self._matches_selector(el, selector))
            try:
                return list(islice(matches, idx + 1))[idx]
            except IndexError:
                return None
        else:
            return [el for el in elements if self._matches_selector(el, selector)]

    def _create_normalized_selector(self, filter):
        if self.normalized_selector is not None:
            return self.normalized_selector
        self.driver_scope = self._ensure_scope_context()

        self.normalized_selector = self.selector_builder.normalized_selector

        if 'label' in self.normalized_selector:
            self._process_label()
            if self.normalized_selector is None:
                return None

        if 'index' in self.normalized_selector and filter == 'all':
            raise ValueError("can't locate all elements by index")
        return self.normalized_selector

    def _create_filter_selector(self):
        if self.filter_selector:
            return self.filter_selector
        self.filter_selector = {}

        # Remove selectors that can never be used in XPath builder
        for how in ('visible', 'visible_text'):
            if how in self.normalized_selector:
                self.filter_selector[how] = self.normalized_selector.pop(how, None)

        if self._tag_vaildation_required(self.normalized_selector):
            self.filter_selector['tag_name'] = self.normalized_selector.get('tag_name')

        # Regexp locators currently need to be validated even if they are included in the XPath
        # builder
        # TODO: Identify Regexp that can have an exact equivalent using XPath contains (ie would
        # not require filtering) vs approximations (ie would still require filtering)
        for how, what in self.normalized_selector.copy().items():
            if isinstance(what, re._pattern_type):
                self.filter_selector[how] = self.normalized_selector.pop(how, None)

        if self.normalized_selector.get('index') is not None and \
                self.normalized_selector.get('adjacent') is None:
            idx = self.normalized_selector.pop('index')

            # Do not add {'index': 0} filter if the only filter. This will allow using #find_element
            # instead of #find_elements
            implicit_idx_filter = not self.filter_selector and idx == 0
            if not implicit_idx_filter:
                self.filter_selector['index'] = idx

        return self.filter_selector

    def _process_label(self):
        if isinstance(self.normalized_selector.get('label'), re._pattern_type) and \
                self.selector_builder.should_use_label_element:

            label = self._label_from_text
            if not label:
                self.normalized_selector = None
                return None

            _id = label.get_attribute('for')
            if _id:
                self.normalized_selector['id'] = _id
            else:
                self.driver_scope = label

    @property
    def _label_from_text(self):
        # TODO: this won't work correctly if @wd is a sub-element
        # TODO: figure out how to do this with find_element
        label_text = self.normalized_selector.pop('label', None)
        elements = self._locate_elements('tag_name', 'label', self.driver_scope)
        return next((e for e in elements if self._matches_selector(e, {'text': label_text})), None)

    def _matches_selector(self, element, selector):
        def check_match(how, what):
            if how == 'tag_name' and isinstance(what, six.string_types):
                return self.element_validator.validate(element, {'tag_name': what})
            else:
                return Validator.match_str_or_regex(what, self._fetch_value(element, how))

        return all(check_match(how, what) for how, what in selector.items())

    @property
    def _can_convert_regexp_to_contains(self):
        return True

    def _add_regexp_predicates(self, what):
        if not self._can_convert_regexp_to_contains:
            return what

        for key, value in self.filter_selector.items():
            if key in ['tag_name', 'text', 'visible_text', 'visible', 'index']:
                continue

            predicates = self._regexp_selector_to_predicates(key, value)
            if predicates:
                what = "({})[{}]".format(what, ' and '.join(predicates))

        return what

    def _regexp_selector_to_predicates(self, key, regex):
        if regex.flags & re.IGNORECASE:
            return []

        match = self.CONVERTABLE_REGEXP.search(regex.pattern)
        if match is None:
            return None

        lhs = self.selector_builder.xpath_builder.lhs_for(None, key)

        return ['contains({}, {})'.format(lhs, XpathSupport.escape(group)) for
                group in match.groups() if group]

    def _tag_vaildation_required(self, selector):
        return any(x in selector for x in ('css', 'xpath')) and 'tag_name' in selector

    def _ensure_scope_context(self):
        return self.query_scope.wd

    def _locate_element(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_element(self._wd_finder(how), what)

    def _locate_elements(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_elements(self._wd_finder(how), what)

    def _wd_finder(self, how):
        return self.W3C_FINDERS.get(how, how)

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
