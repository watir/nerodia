import re
from copy import copy

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
                elements = self._filter_elements_by_locator(found, tag_name=tag_name, filter=filter)
                return [el for el in elements if el is not None]
            else:
                found = self._locate_element(sel, value)
                if sel != 'tag_name' and tag_name and not self._validate([found], tag_name):
                    return None
                return found

    def _using_nerodia(self, filter='first'):
        selector = self.selector_builder.normalized_selector
        visible = selector.pop('visible', None)
        visible_text = selector.pop('visible_text', None)
        tag_name = selector.get('tag_name')
        validation_required = ('css' in selector or 'xpath' in selector) and tag_name

        if 'index' in selector and filter == 'all':
            raise ValueError("can't locate all elements by index")

        idx = selector.pop('index', None) if not selector.get('adjacent') else None
        built_selector = self.selector_builder.build(selector)

        needs_filtering = idx or \
            visible is not None \
            or visible_text is not None or \
            validation_required or \
            filter == 'all'

        if needs_filtering:
            matching = self._matching_elements(built_selector, selector)
            return self._filter_elements_by_locator(matching, visible, visible_text, idx,
                                                    tag_name=tag_name, filter=filter)
        elif built_selector:
            return self._locate_element(*built_selector)
        else:
            return self._wd_find_by_regexp_selector(selector, 'first')

    def _validate(self, elements, tag_name):
        return all(self.element_validator.validate(el, {'tag_name': tag_name})
                   for el in elements if el is not None)

    def _matching_elements(self, built_selector, selector=None):
        found = self._locate_elements(*built_selector) if built_selector \
            else self._wd_find_by_regexp_selector(selector, 'all')
        return found or []

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
        elif how == 'visible_text':
            return element.text
        elif how == 'tag_name':
            return element.tag_name.lower()
        elif how == 'href':
            href = element.get_attribute('href')
            return href and href.strip()
        else:
            return element.get_attribute(how.replace('_', '-')) or ''

    @property
    def _all_elements(self):
        return self._locate_elements(By.XPATH, './/*')

    def _wd_find_by_regexp_selector(self, selector, filter):
        query_scope = self._ensure_scope_context
        rx_selector = self._delete_regexps_from(selector)

        if 'label' in rx_selector and self.selector_builder.should_use_label_element:
            label = self._label_from_text(rx_selector.pop('label'))
            if not label:
                return None
            attr_id = label.get_attribute('for')
            if attr_id:
                selector['id'] = attr_id
            else:
                query_scope = label

        built_selector = self.selector_builder.build(selector)

        if not built_selector:
            raise Error('internal error: unable to build Selenium selector from'
                        ' {}'.format(selector))

        how, what = built_selector
        if how == By.XPATH and self._can_convert_regexp_to_contains:
            for key, value in rx_selector.items():
                if key == 'tag_name' or key == 'text':
                    continue

                predicates = self._regexp_selector_to_predicates(key, value)
                if predicates:
                    what = '({})[{}]'.format(what, ' and '.join(predicates))

        elements = self._locate_elements(how, what, query_scope)
        return self._filter_elements_by_regex(elements, rx_selector, filter)

    def _filter_elements_by_locator(self, elements, visible=None, visible_text=None, idx=None,
                                    tag_name=None, filter='first'):
        if visible is not None:
            elements = [el for el in elements if visible == el.is_displayed()]
        if visible_text is not None:
            elements = [el for el in elements
                        if Validator.match_str_or_regex(visible_text, el.text)]
        if tag_name is not None:
            elements = [el for el in elements
                        if self.element_validator.validate(el, {'tag_name': tag_name})]
        if filter == 'first':
            idx = idx or 0
            return elements[idx] if elements and idx < len(elements) else None
        else:
            return elements

    def _filter_elements_by_regex(self, elements, selector, filter):
        if filter == 'first':
            return next((el for el in elements if self._matches_selector(el, selector)), None)
        else:
            return [el for el in elements if self._matches_selector(el, selector)]

    @staticmethod
    def _delete_regexps_from(selector):
        rx_selector = {}

        for how, what in copy(selector).items():
            if not isinstance(what, re._pattern_type):
                continue
            rx_selector[how] = what
            selector.pop(how)

        return rx_selector

    def _label_from_text(self, label_exp):
        # TODO: this won't work correctly if @wd is a sub-element
        from selenium.webdriver.common.by import By
        elements = self._locate_elements(By.TAG_NAME, 'label')
        return next((el for el in elements if self._matches_selector(el, {'text': label_exp})), None)

    def _matches_selector(self, element, selector):
        return all(Validator.match_str_or_regex(what, self._fetch_value(element, how))
                   for how, what in selector.items())

    @property
    def _can_convert_regexp_to_contains(self):
        return True

    def _regexp_selector_to_predicates(self, key, regex):
        if regex.flags & re.IGNORECASE:
            return []

        match = self.CONVERTABLE_REGEXP.search(regex.pattern)
        if match is None:
            return None

        lhs = self.selector_builder.xpath_builder.lhs_for(None, key)

        return ['contains({}, {})'.format(lhs, XpathSupport.escape(group)) for
                group in match.groups() if group]

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
