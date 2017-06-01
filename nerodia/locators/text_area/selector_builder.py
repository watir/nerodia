import re

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder


class SelectorBuilder(ElementSelectorBuilder):
    def normalize_selector(self, how, what):
        # We need to iterate through located elements and fetch
        # attribute value using Selenium because XPath doesn't understand
        # difference between IDL vs content attribute.
        # Current Element design doesn't allow to do that in any
        # obvious way except to use regular expression.

        if how == 'value' and isinstance(what, str):
            return [how, re.compile(r'^{}$'.format(re.escape(what)))]
        else:
            return super(SelectorBuilder, self).normalized_selector(how, what)
