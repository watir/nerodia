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
    WD_FINDERS = {
        'class_name': By.CLASS_NAME,
        'css': By.CSS_SELECTOR,
        'id': By.ID,
        'link': By.LINK_TEXT,
        'link_text': By.LINK_TEXT,
        'name': By.NAME,
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
        tag_name = selector.get('tag_name')
        if len(selector) > 1:
            selector.pop('tag_name', None)

        for sel in self.WD_FINDERS:
            value = selector.pop(sel, None)
            if not value:
                continue
            if not (len(selector) == 0 and self._wd_is_supported(sel, value)):
                return
            if filter == 'all':
                found = self._locate_elements(sel, value)
                if sel == 'tag_name':
                    return found
                filter_selector = {'tag_name': tag_name} if tag_name else {}
                elements = self._filter_elements(found, filter_selector, filter=filter)
                return [el for el in elements if el is not None]
            else:
                found = self._locate_element(sel, value)
                if sel != 'tag_name' and tag_name and not self._validate([found], tag_name):
                    return None
                return found

    def _using_nerodia(self, filter='first'):
        query_scope = self._ensure_scope_context
        selector = self.selector_builder.normalized_selector

        if 'label' in selector:
            query_scope = self._convert_label_to_scope_or_selector(query_scope, selector)
            if not query_scope:
                return

        if 'index' in selector and filter == 'all':
            raise ValueError("can't locate all elements by index")

        filter_selector = self._delete_filters_from(selector)

        built_selector = self.selector_builder.build(selector)
        if not built_selector:
            raise Error('internal error: unable to build Selenium selector from '
                        '{}'.format(selector))

        how, what = built_selector
        if how == 'xpath':
            what = self._add_regexp_predicates(what, filter_selector)

        needs_filtering = filter == 'all' or len(filter_selector) > 0

        if needs_filtering:
            elements = self._locate_elements(how, what, query_scope) or []
            return self._filter_elements(elements, filter_selector, filter=filter)
        else:
            return self._locate_element(how, what)

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

    def _filter_elements(self, elements, selector, filter='first'):
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

    def _delete_filters_from(self, selector):
        filter_selector = {}

        # Remove selectors that can never be used in XPath builder
        for how in ('visible', 'visible_text'):
            if how in selector:
                filter_selector[how] = selector.pop(how)

        if self._tag_vaildation_required(selector):
            filter_selector['tag_name'] = selector.get('tag_name')

        # Regexp locators currently need to be validated even if they are included in the XPath
        # builder
        # TODO: Identify Regexp that can have an exact equivalent using XPath contains (ie would
        # not require filtering) vs approximations (ie would still require filtering)
        for how, what in copy(selector).items():
            if isinstance(what, re._pattern_type):
                filter_selector[how] = selector.pop(how)

        if selector.get('index') is not None and selector.get('adjacent') is None:
            idx = selector.pop('index')

            # Do not add {'index': 0} filter if the only filter. This will allow using #find_element
            # instead of #find_elements
            implicit_idx_filter = not filter_selector and idx == 0
            if not implicit_idx_filter:
                filter_selector['index'] = idx

        return filter_selector

    def _convert_label_to_scope_or_selector(self, query_scope, selector):
        if isinstance(selector.get('label'), re._pattern_type) and \
                self.selector_builder.should_use_label_element:
            label = self._label_from_text(selector.pop('label', None))
            if not label:
                return
            _id = label.get_attribute('for')
            if _id:
                selector['id'] = _id
                return query_scope
            else:
                return label
        else:
            return query_scope

    def _label_from_text(self, label_exp):
        # TODO: this won't work correctly if @wd is a sub-element
        from selenium.webdriver.common.by import By
        elements = self._locate_elements(By.TAG_NAME, 'label')
        return next((el for el in elements if self._matches_selector(el, {'text': label_exp})), None)

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

    def _add_regexp_predicates(self, what, filter_selector):
        if not self._can_convert_regexp_to_contains:
            return what

        for key, value in filter_selector.items():
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

    @property
    def _ensure_scope_context(self):
        return self.query_scope.wd

    def _locate_element(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_element(self._wd_finder(how), what)

    def _locate_elements(self, how, what, scope=None):
        scope = scope or self.query_scope.wd
        return scope.find_elements(self._wd_finder(how), what)

    def _wd_finder(self, how):
        return self.WD_FINDERS.get(how, how)

    def _wd_is_supported(self, how, what):
        if type(what) not in nerodia._str_types:
            return False
        if how in ['class', 'class_name'] and ' ' in what:
            return False
        for loc in ['partial_link_text', 'link_text', 'link']:
            if how == loc:
                nerodia.logger.deprecate(':{} locator'.format(loc), 'visible_text')
        return True
