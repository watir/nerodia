import re

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):
    # private

    def _normalize_locator(self, how, what):
        # We need to iterate through located elements and fetch
        # attribute value using Selenium because XPath doesn't understand
        # difference between IDL vs content attribute.
        # Current Element design doesn't allow to do that in any
        # obvious way except to use regular expression.

        if how == 'value' and isinstance(what, str):
            return [how, re.compile(r'^{}$'.format(re.escape(what)))]
        else:
            return super(SelectorBuilder, self)._normalize_locator(how, what)


class XPath(ElementXPath):
    # private

    # value always requires a wire call since we want the property not the attribute
    def _predicate_conversion(self, key, regexp):
        if key != 'value':
            return super(XPath, self)._predicate_conversion(key, regexp)
        else:
            self.requires_matches['value'] = regexp
            return None
