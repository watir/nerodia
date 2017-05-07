import logging
from importlib import import_module

import re

from ...exception import MissingWayOfFindingObjectException
from ...xpath_support import XpathSupport


class SelectorBuilder(object):
    VALID_WHATS = [re._pattern_type, str, bool]
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
                raise TypeError('expected Integer, got {}:{}'.format(what, what.__class__))
        elif how == 'visible':
            if not isinstance(what, bool):
                raise TypeError('expected boolean, got {}:{}'.format(what, what.__class__))
        else:
            if type(what) not in self.VALID_WHATS:
                raise TypeError(
                    'expected one of {}, got {}'.format(self.VALID_WHATS, what, what.__class__))

    @property
    def should_use_label_element(self):
        return not self._is_valid_attribute('label')

    def build(self, selector):
        return self._given_xpath_or_css(selector) or self._build_wd_selector(selector)

    @property
    def xpath_builder(self):
        return self._xpath_builder_class(self.should_use_label_element)

    # private

    def _normalize_selector(self, how, what):
        if how in ['tag_name', 'text', 'xpath', 'index', 'class', 'label', 'css', 'visible']:
            # include 'class' since the valid attribute is 'class_name'
            return [how, what]
        elif how == 'class_name':
            return ['class', what]
        elif 'caption':
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
            how = 'xpath'
            what = xpath
        elif css:
            how = 'css'
            what = css

        if selector and not self._can_be_combined_with_xpath_or_css(selector):
            raise ValueError('{} cannot be combined with other selectors {})'.format(how, selector))

        return [how, what]

    def _build_wd_selector(self, selectors):
        if any(isinstance(selector, re._pattern_type) for selector in selectors):
            return None
        return self._build_xpath(selectors)

    def _is_valid_attribute(self, attribute):
        return self.valid_attributes and attribute in self.valid_attributes

    @staticmethod
    def _can_be_combined_with_xpath_or_css(selector):
        keys = selector.keys()
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
            return mod.XPath
        except ImportError:
            return XPath


class XPath(object):
    def __init__(self, should_use_label_element):
        self.should_use_label_element = should_use_label_element

    def build(self, selectors):
        xpath = ".//"
        xpath += selectors.pop('tag_name') or '*'

        selectors.pop('index', None)

        # the remaining entries should be attributes
        if selectors:
            xpath += '[{}]'.format(self.attribute_expression(None, selectors))

        logging.debug({'xpath': xpath, 'selectors': selectors})

        return ['xpath', xpath]

    # TODO: Get rid of building
    def attribute_expression(self, building, selectors):
        expressions = []
        for key, val in selectors.items():
            if isinstance(val, list):
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
            klass = XpathSupport.escape(' {} '.format(value))
            return "contains(concat(' ', @class, ' '), {})".format(klass)
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
            '@{}'.format(key.replace('_', '-'))

    # private

    def _attribute_presence(self, attribute):
        return self.lhs_for(None, attribute)

    def _attribute_absence(self, attribute):
        return "not({})".format(self.lhs_for(None, attribute))
