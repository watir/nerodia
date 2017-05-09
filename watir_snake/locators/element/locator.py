from copy import copy, Error

import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from ...exception import Error
from ...xpath_support import XpathSupport


class Locator(object):
    WD_FINDERS = [
        'class',
        'class_name',
        'css',
        'id',
        'link',
        'link_text',
        'name',
        'partial_link_text',
        'tag_name',
        'xpath'
    ]

    # Regular expressions that can be reliably converted to xpath `contains`
    # expressions in order to optimize the .
    CONVERTABLE_REGEXP = re.compile(r'\A'
                                    r'([^\[\]\\^$.|?*+()]*)'  # leading literal characters
                                    r'[^|]*?'  # do not try to convert expressions with alternates
                                    r'([^\[\]\\^$.|?*+()]*)'  # trailing literal characters
                                    r'\z',
                                    re.X)

    def __init__(self, query_scope, selector, selector_builder, element_validator):
        self.query_scope = query_scope  # either element or browser
        self.selector = copy(selector)
        self.selector_builder = selector_builder
        self.element_validator = element_validator

    def locate(self):
        try:
            e = self._by_id()  # short-circuit if :id is given
            if e:
                return e

            if len(self.selector) == 1:
                element = self._find_first_by_one()
            else:
                element = self._find_first_by_multiple()

            # This actually only applies when finding by xpath/css -
            # browser.text_field(xpath="//input[@type='radio']")
            # We don't need to validate the element if we built the xpath ourselves.
            # It is also used to alter behavior of methods locating more than one type of element
            # (e.g. text_field locates both input and textarea)
            if element:
                return self.element_validator.validate(element, self.selector)
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def locate_all(self):
        if len(self.selector) == 1:
            return self._find_all_by_one()
        else:
            return self._find_all_by_multiple()

    # private

    def _by_id(self):
        selector = copy(self.selector)
        attr_id = selector.pop('id', None)
        if not isinstance(attr_id, str):
            return None

        tag_name = selector.pop('tag_name', None)
        if selector:  # Multiple attributes
            return None

        element = self.query_scope.wd.find_element_by_id(attr_id)
        if tag_name and not self.element_validator.validate(element, {'tag_name': tag_name}):
            return None

        return element

    def _find_first_by_one(self):
        how, what = self.selector.items()[0]
        self.selector_builder.check_type(how, what)

        if how in self.WD_FINDERS:
            return self._wd_find_first_by(how, what)
        else:
            return self._find_first_by_multiple()

    def _find_first_by_multiple(self):
        selector = self.selector_builder.normalized_selector

        idx = selector.pop('index', None)
        visible = selector.pop('visible', None)

        how, what = self.selector_builder.build(selector)

        if how:
            # could build xpath/css for selector
            if idx or visible:
                idx = idx or 0
                elements = self.query_scope.wd.find_elements(how, what)
                if visible:
                    elements = [el for el in elements if visible == el.is_displayed()]
                return elements[idx] if elements else None
            else:
                return self.query_scope.wd.find_element(how, what)
        else:
            # can't use xpath, probably a regexp in there
            if idx or visible:
                idx = idx or 0
                elements = self._wd_find_by_regexp_selector(selector, 'select')
                if visible:
                    elements = [el for el in elements if visible == el.is_displayed()]
                return elements[idx] if elements else None
            else:
                return self._wd_find_by_regexp_selector(selector, 'find')

    def _find_all_by_one(self):
        how, what = self.selector.items().first
        self.selector_builder.check_type(how, what)

        if how in self.WD_FINDERS:
            return self._wd_find_all_by(how, what)
        else:
            return self._find_all_by_multiple()

    def _find_all_by_multiple(self):
        selector = self.selector_builder.normalized_selector
        visible = selector.pop('visible')

        if 'index' in selector:
            raise ValueError("can't locate all elements by index")

        how, what = self.selector_builder.build(selector)
        if how:
            found = self.query_scope.wd.find_elements(how, what)
        else:
            found = self._wd_find_by_regexp_selector(selector, 'select')
        if visible:
            return [el for el in found if visible == el.is_displayed()]
        else:
            return found

    def _wd_find_all_by(self, how, what):
        if isinstance(what, str):
            return self.query_scope.wd.find_elements(how, what)
        else:
            return [el for el in self._all_elements if what.search(self._fetch_value(el, how))]

    @staticmethod
    def _fetch_value(element, how):
        if how == 'text':
            return element.text
        elif how == 'tag_name':
            return element.tag_name.downcase
        elif how == 'href':
            href = element.attribute('href')
            return href and href.strip()
        else:
            return element.attribute(how.replace('_', '-'))

    @property
    def _all_elements(self):
        return self.query_scope.wd.find_elements(xpath='.//*')

    def _wd_find_first_by(self, how, what):
        if isinstance(what, str):
            return self.query_scope.wd.find_element(how, what)
        else:
            return next((x for x in self._all_elements if what.search(self._fetch_value(x, how))),
                        None)

    def _wd_find_by_regexp_selector(self, selector, method='find'):
        query_scope = self.query_scope.wd
        rx_selector = self._delete_regexps_from(selector)

        if 'label' in rx_selector and self.selector_builder.should_use_label_element:
            label = self._label_from_text(rx_selector.pop('label'))
            if not label:
                return None
            attr_id = label.attribute('for')
            if attr_id:
                selector[attr_id] = attr_id
            else:
                query_scope = label

        how, what = self.selector_builder.build(selector)

        if not how:
            raise Error('internal error: unable to build Selenium selector from'
                        ' {}'.format(selector))

        if how == 'xpath' and self._can_convert_regexp_to_contains:
            for key, value in rx_selector.items():
                if key == 'tag_name' or key == 'text':
                    continue

                predicates = self._regexp_selector_to_predicates(key, value)
                if predicates:
                    what = "({})[{}]".format(what, ' and '.join(predicates))

        elements = query_scope.find_elements(how, what)
        if method == 'find':
            return next((el for el in elements if self._matches_selector(el, rx_selector)))
        elif method == 'select':
            return [el for el in elements if self._matches_selector(el, rx_selector)]
        else:
            return None

    @staticmethod
    def _delete_regexps_from(selector):
        rx_selector = {}

        selector = copy(selector)

        for how, what in selector.items():
            if not isinstance(what, re._pattern_type):
                continue
            rx_selector[how] = what
            selector.pop(how)

        return rx_selector

    def _label_from_text(self, label_exp):
        # TODO: this won't work correctly if @wd is a sub-element
        elements = self.query_scope.wd.find_elements(tag_name='label')
        return next((el for el in elements if self._matches_selector(el, {'text': label_exp})))

    def _matches_selector(self, element, selector):
        return all(what == self._fetch_value(element, how) for how, what in selector.items())

    @property
    def _can_convert_regexp_to_contains(self):
        return True

    def _regexp_selector_to_predicates(self, key, regex):
        if regex.flags & re.IGNORECASE:
            return []

        match = self.CONVERTABLE_REGEXP.search(regex.pattern)
        if match is None:
            return None

        lhs = self.selector_builder.xpath_builder.lhs_for(key)

        return ['contains({}, {})'.format(lhs, XpathSupport.escape(group)) for
                group in match.groups() if group]
