import logging
from importlib import import_module

import six

import re
from selenium.webdriver.common.by import By

import nerodia
from ...exception import MissingWayOfFindingObjectException
from ...xpath_support import XpathSupport

STRING_TYPES = [six.text_type, six.binary_type]


class SelectorBuilder(object):
    VALID_WHATS = [list, re._pattern_type, bool] + STRING_TYPES
    WILDCARD_ATTRIBUTE = re.compile(r'^(aria|data)_(.+)$')

    def __init__(self, query_scope, selector, valid_attributes):
        self.query_scope = query_scope  # either element or browser
        self.selector = selector
        self.valid_attributes = valid_attributes

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
        else:
            if isinstance(what, list) and how != 'class_name':
                raise TypeError("only 'class_name' locator can have a value of a list")
            if type(what) not in self.VALID_WHATS:
                raise TypeError(
                    'expected one of {}, got {!r}:{}'.format(self.VALID_WHATS, what, what.__class__))

    @property
    def should_use_label_element(self):
        return not self._is_valid_attribute('label')

    def build(self, selector):
        if 'xpath' in selector or 'css' in selector:
            return self._given_xpath_or_css(selector)
        built = self._build_wd_selector(selector)
        nerodia.logger.debug('Converted {} to {}'.format(selector, built))
        return built

    @property
    def xpath_builder(self):
        return self._xpath_builder_class(self.should_use_label_element)

    # private

    def _normalize_selector(self, how, what):
        if how in ['tag_name', 'text', 'xpath', 'index', 'class', 'label', 'css', 'visible',
                   'adjacent']:
            # include 'class' since the valid attribute is 'class_name'
            return [how, what]
        elif how == 'class_name':
            return ['class', what]
        elif how == 'caption':
            return ['text', what]
        else:
            self._assert_valid_as_attribute(how)
            return [how, what]

    def _assert_valid_as_attribute(self, attribute):
        if self._is_valid_attribute(attribute) or self.WILDCARD_ATTRIBUTE.search(attribute):
            return None
        raise MissingWayOfFindingObjectException('invalid attribute: {}'.format(attribute))

    def _given_xpath_or_css(self, selector):
        xpath = selector.pop('xpath', None)
        css = selector.pop('css', None)

        if not (xpath or css):
            return None

        if xpath and css:
            raise ValueError("'xpath' and 'css' cannot be combined ({})".format(selector))

        how, what = [None] * 2
        if xpath:
            how = By.XPATH
            what = xpath
        elif css:
            how = By.CSS_SELECTOR
            what = css

        if selector and not self._can_be_combined_with_xpath_or_css(selector):
            raise ValueError('{} cannot be combined with other selectors {})'.format(how, selector))

        return [how, what]

    def _build_wd_selector(self, selectors):
        if any(isinstance(val, re._pattern_type) for val in selectors.values()):
            return None
        return self._build_xpath(selectors)

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

    def _build_xpath(self, selectors):
        return self.xpath_builder.build(selectors)

    @property
    def _xpath_builder_class(self):
        try:
            mod = import_module(self.__module__)
            return getattr(mod, 'XPath', XPath)
        except ImportError:
            return XPath


class XPath(object):
    def __init__(self, should_use_label_element):
        self.should_use_label_element = should_use_label_element

    def build(self, selectors):
        adjacent = selectors.pop('adjacent', None)
        xpath = self._process_adjacent(adjacent) if adjacent else './/'

        xpath += selectors.pop('tag_name', '*')

        index = selectors.pop('index', None)

        # the remaining entries should be attributes
        if selectors:
            xpath += '[{}]'.format(self.attribute_expression(None, selectors))

        if adjacent and index is not None:
            xpath += "[{}]".format(index + 1)

        logging.debug({'xpath': xpath, 'selectors': selectors})

        return [By.XPATH, xpath]

    # TODO: Get rid of building
    def attribute_expression(self, building, selectors):
        expressions = []
        for key, val in selectors.items():
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
        if key == 'class':
            if ' ' in value.strip():
                nerodia.logger.deprecate("using the 'class_name' locator to locate multiple "
                                         "classes with a str value", "use a list instead")
            return self._build_class_match(value)
        elif key == 'label' and self.should_use_label_element:
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
            xpath += 'ancestor::'
        elif adjacent == 'preceding':
            xpath += 'preceding-sibling::'
        elif adjacent == 'following':
            xpath += 'following-sibling::'
        elif adjacent == 'child':
            xpath += 'child::'
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
