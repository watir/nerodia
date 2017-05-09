import logging

import re

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath
from ...elements.text_field import TextField
from ...xpath_support import XpathSupport


class SelectorBuilder(ElementSelectorBuilder):
    # private

    def _build_wd_selector(self, selectors):
        if any(isinstance(val, re._pattern_type) for val in selectors.values()):
            return None

        selectors.pop('tag_name', None)

        input_attr_exp = self.xpath_builder.attribute_expression('input', selectors)

        xpath = './/input[(not(@type) or ({}))'.format(self._negative_type_expr)
        if input_attr_exp:
            xpath += ' and {}'.format(input_attr_exp)
        xpath += ']'

        logging.debug({'build_wd_selector': xpath})

        return ['xpath', xpath]

    @property
    def _negative_type_expr(self):
        types = ['{}!={}'.format(XpathSupport.lower('@type'), typ) for
                 typ in TextField.NON_TEXT_TYPES]
        return ' and '.join(types)


class XPath(ElementXPath):
    @staticmethod
    def lhs_for(building, key):
        if building == 'input' and key == 'text':
            return '@value'
        else:
            return super(XPath, XPath).lhs_for(building, key)
