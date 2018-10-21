from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder,\
    XPath as ElementXPath
from ...elements.button import Button
from ...xpath_support import XpathSupport

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):

    def add_tag_name(self, selector):
        selector.pop('tag_name', None)
        return "[local-name()='button']"

    def add_attributes(self, selector):
        button_attr_exp = self.attribute_expression('button', selector)
        xpath = '' if not button_attr_exp else '[{}]'.format(button_attr_exp)
        if selector.get('type') is False:
            return xpath

        if selector.get('type') in [None, True]:
            selector['type'] = Button.VALID_TYPES
        xpath += " | .//*[local-name()='input']"
        input_attr_exp = self.attribute_expression('input', selector)
        if input_attr_exp:
            xpath += '[{}]'.format(input_attr_exp)
        return xpath

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

    @property
    def _convert_regexp_to_contains(self):
        # regexp conversion won't work with the complex xpath selector
        return False
