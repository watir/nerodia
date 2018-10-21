from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath

from ...elements.text_field import TextField
from ...xpath_support import XpathSupport

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):

    def add_attributes(self, selector):
        input_attr_exp = self.attribute_expression('input', selector)
        xpath = '[(not(@type) or ({}))'.format(self._negative_type_expr)
        if input_attr_exp:
            xpath += ' and {}'.format(input_attr_exp)
        xpath += ']'
        return xpath

    def add_tag_name(self, selector):
        selector.pop('tag_name', None)
        return "[local-name()='input']"

    @staticmethod
    def lhs_for(building, key):
        if building == 'input' and key == 'text':
            return '@value'
        else:
            return super(XPath, XPath).lhs_for(building, key)

    # private

    @property
    def _negative_type_expr(self):
        types = ['{}!={!r}'.format(XpathSupport.lower('@type'), typ) for
                 typ in TextField.NON_TEXT_TYPES]
        return ' and '.join(types)
