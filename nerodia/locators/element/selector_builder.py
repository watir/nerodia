import logging
import re
from importlib import import_module

import six
from selenium.webdriver.common.by import By

import nerodia
from ...xpath_support import XpathSupport

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern

STRING_TYPES = [six.text_type, six.binary_type]


class SelectorBuilder(object):
    VALID_WHATS = [list, Pattern, bool] + STRING_TYPES
    WILDCARD_ATTRIBUTE = re.compile(r'^(aria|data)_(.+)$')

    def __init__(self, query_scope, selector, valid_attributes):
        self.query_scope = query_scope  # either element or browser
        self.selector = selector
        self.valid_attributes = valid_attributes
        self.custom_attributes = []
        self.xpath_builder = None

    @property
    def normalized_selector(self):
        selector = {}

        for how, what in self.selector.items():
            self.check_type(how, what)

            how, what = self._normalize_selector(how, what)
            selector[how] = what

        return selector

    def check_type(self, how, what):
        if how == 'index':
            if not isinstance(what, int):
                raise TypeError('expected {}, got {!r}:{}'.format(int, what, what.__class__))
        elif how == 'visible':
            if not isinstance(what, bool):
                raise TypeError('expected {}, got {!r}:{}'.format(bool, what, what.__class__))
        elif how == 'visible_text':
            if type(what) not in [six.text_type, six.binary_type, Pattern]:
                raise TypeError('expected str or regexp, got {}')
        else:
            if isinstance(what, list) and how != 'class_name':
                raise TypeError("only 'class_name' locator can have a value of a list")
            if type(what) not in self.VALID_WHATS:
                raise TypeError(
                    'expected one of {}, got {!r}:{}'.format(self.VALID_WHATS, what, what.__class__))

    @property
    def should_use_label_element(self):
        return not self._is_valid_attribute('label')

    def build(self, selector, values):
        if 'xpath' in selector or 'css' in selector:
            return self._given_xpath_or_css(selector)
        built = self._build_wd_selector(selector, values)
        nerodia.logger.debug('Converted {} to {}'.format(selector, built))
        return built

    # private

    def _normalize_selector(self, how, what):
        if how in ['tag_name', 'text', 'xpath', 'index', 'class', 'label', 'css', 'visible',
                   'visible_text', 'adjacent']:
            # include 'class' since the valid attribute is 'class_name'
            return [how, what]
        elif how == 'class_name':
            return ['class', what]
        elif how == 'caption':
            return ['text', what]
        else:
            self._check_custom_attribute(how)
            return [how, what]

    def _check_custom_attribute(self, attribute):
        if self._is_valid_attribute(attribute) or self.WILDCARD_ATTRIBUTE.search(attribute):
            return None
        self.custom_attributes.append(attribute)

    def _given_xpath_or_css(self, selector):
        locator = {}
        if 'xpath' in selector:
            locator['xpath'] = selector.pop('xpath')
        if 'css' in selector:
            locator['css'] = selector.pop('css')

        if not locator:
            return

        if len(locator) > 1:
            raise ValueError("'xpath' and 'css' cannot be combined ({})".format(selector))

        if selector and not self._can_be_combined_with_xpath_or_css(selector):
            raise ValueError('{} cannot be combined with other locators '
                             '{})'.format(list(locator.keys()[0]), selector))

        return list(list(locator.items())[0])

    def _build_wd_selector(self, selector, values):
        return self._xpath_builder.build(selector, values)

    @property
    def _xpath_builder(self):
        if self.xpath_builder is None:
            self.xpath_builder = self._xpath_builder_class(self.should_use_label_element)
        return self.xpath_builder

    def _is_valid_attribute(self, attribute):
        return self.valid_attributes and attribute in self.valid_attributes

    @staticmethod
    def _can_be_combined_with_xpath_or_css(selector):
        keys = list(selector)
        if keys == ['tag_name']:
            return True

        if selector.get('tag_name') == 'input':
            keys.sort()
            return keys == ['tag_name', 'type']
        return False

    @property
    def _xpath_builder_class(self):
        try:
            mod = import_module(self.__module__)
            return getattr(mod, 'XPath', XPath)
        except ImportError:
            return XPath


class XPath(object):
    # Regular expressions that can be reliably converted to xpath `contains`
    # expressions in order to optimize the locator.
    CONVERTABLE_REGEXP = re.compile(r'\A'
                                    r'([^\[\]\\^$.|?*+()]*)'  # leading literal characters
                                    r'[^|]*?'  # do not try to convert expressions with alternates
                                    r'([^\[\]\\^$.|?*+()]*)'  # trailing literal characters
                                    r'\Z',
                                    re.X)

    def __init__(self, use_element_label):
        self._should_use_label_element = use_element_label

    def build(self, selector, values):
        adjacent = selector.pop('adjacent', None)
        xpath = self._process_adjacent(adjacent) if adjacent else self.default_start
        xpath += self.add_tag_name(selector)
        index = selector.pop('index', None)

        # the remaining entries should be attributes
        xpath += self.add_attributes(selector)

        if adjacent and index is not None:
            xpath += "[{}]".format(index + 1)

        xpath = self.add_regexp_predicates(xpath, values)

        logging.debug({'xpath': xpath, 'selector': selector})

        return [By.XPATH, xpath]

    @property
    def default_start(self):
        return './/*'

    def add_tag_name(self, selector):
        if 'tag_name' in selector:
            return "[local-name()='{}']".format(selector.pop('tag_name'))
        else:
            return ''

    def add_attributes(self, selector):
        element_attr_exp = self.attribute_expression(None, selector)
        return '[{}]'.format(element_attr_exp) if element_attr_exp else ''

    def add_regexp_predicates(self, what, selector):
        if not self._convert_regexp_to_contains:
            return what

        for key, value in selector.items():
            if key in ['tag_name', 'text', 'visible_text', 'visible', 'index']:
                continue

            predicates = self._regexp_selector_to_predicates(key, value)
            if predicates:
                what = "({})[{}]".format(what, ' and '.join(predicates))

        return what

    # TODO: Get rid of building
    def attribute_expression(self, building, selector):
        expressions = []
        for key, val in selector.items():
            if isinstance(val, list) and key == 'class':
                term = '({})'.format(' and '.join([self._build_class_match(v) for v in val]))
            elif isinstance(val, list):
                term = '({})'.format(' or '.join([self.equal_pair(building, key, v) for v in val]))
            elif val is True:
                term = self._attribute_presence(key)
            elif val is False:
                term = self._attribute_absence(key)
            else:
                term = self.equal_pair(building, key, val)
            expressions.append(term)
        return ' and '.join(expressions)

    # TODO: Get rid of building
    def equal_pair(self, building, key, value):
        if key in ['class', 'class_name']:
            if ' ' in value.strip():
                nerodia.logger.deprecate("using the 'class_name' locator to locate multiple "
                                         "classes with a str value (i.e. {!r})".format(value),
                                         "list (e.g. {!r})".format(value.split()),
                                         ids=['class_array'])
            return self._build_class_match(value)
        elif key == 'label' and self._should_use_label_element:
            # we assume 'label' means a corresponding label element, not the attribute
            text = 'normalize-space()={}'.format(XpathSupport.escape(value))
            return '(@id=//label[{0}]/@for or parent::label[{0}])'.format(text)
        else:
            return '{}={}'.format(self.lhs_for(building, key), XpathSupport.escape(value))

    # TODO: Get rid of building
    @staticmethod
    def lhs_for(building, key):
        if key == 'text':
            return 'normalize-space()'
        elif key == 'href':
            # TODO: change this behaviour?
            return 'normalize-space(@href)'
        elif key == 'type':
            # type attributes can be upper case - downcase them
            # https://github.com/watir/watir/issues/72
            return XpathSupport.lower('@type')
        else:
            return '@{}'.format(key.replace('_', '-'))

    # private

    def _process_adjacent(self, adjacent):
        xpath = './'
        if adjacent == 'ancestor':
            xpath += 'ancestor::*'
        elif adjacent == 'preceding':
            xpath += 'preceding-sibling::*'
        elif adjacent == 'following':
            xpath += 'following-sibling::*'
        elif adjacent == 'child':
            xpath += 'child::*'
        return xpath

    def _build_class_match(self, value):
        if re.match('!', value):
            escaped = XpathSupport.escape(" {} ".format(value[1:]))
            return "not(contains(concat(' ', @class, ' '), {}))".format(escaped)
        else:
            escaped = XpathSupport.escape(" {} ".format(value))
            return "contains(concat(' ', @class, ' '), {})".format(escaped)

    def _attribute_presence(self, attribute):
        return self.lhs_for(None, attribute)

    def _attribute_absence(self, attribute):
        return "not({})".format(self.lhs_for(None, attribute))

    def _convert_regexp_to_contains(self):
        return True

    def _regexp_selector_to_predicates(self, key, regex):
        if regex.flags & re.IGNORECASE:
            return []

        match = self.CONVERTABLE_REGEXP.search(regex.pattern)
        if match is None:
            return None

        lhs = self.lhs_for(None, key)

        return ['contains({}, {})'.format(lhs, XpathSupport.escape(group)) for
                group in match.groups() if group]
