import logging

import re

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXpath
from ...elements.button import Button
from ...exception import Error
from ...xpath_support import XpathSupport


class SelectorBuilder(ElementSelectorBuilder):
    def _build_wd_selector(self, selectors):
        if any(isinstance(selector, re._pattern_type) for selector in selectors):
            return None

        if not selectors.pop('tag_name', None):
            raise Error('internal error: no tag_name?!')

        button_attr_exp = self.xpath_builder.attribute_expression('button', selectors)

        selectors['type'] = Button.VALID_TYPES
        input_attr_exp = self.xpath_builder.attribute_expression('input', selectors)

        xpath = './/button'
        if button_attr_exp:
            xpath += '[{}]'.format(button_attr_exp)
        xpath += ' | .//input'
        xpath += '[{}]'.format(input_attr_exp)

        logging.debug({'build_wd_selector': xpath})

        return ['xpath', xpath]


class XPath(ElementXpath):
    @staticmethod
    def lhs_for(building, key):
        if building == 'input' and key == 'text':
            return '@value'
        else:
            return super(XPath, XPath).lhs_for(building, key)

    def equal_pair(self, building, key, value):
        if building == 'button' and key == 'value':
            # :value should look for both node text and @value attribute
            text = XpathSupport.escape(value)
            return '(text()={0} or @value={0})'.format(text)
        else:
            return super(XPath, self).equal_pair(building, key, value)
