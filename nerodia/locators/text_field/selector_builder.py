from nerodia.exception import LocatorException
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

    def build(self, selector):
        if 'adjacent' in selector:
            return super(XPath, self).build(selector)

        selector['tag_name'] = 'input'
        type_string = self._create_type_string(selector)
        if not type_string:
            return super(XPath, self).build(selector)

        selector.pop('type', None)
        wd_locator = super(XPath, self).build(selector)

        start_string = self.default_start
        input_string = "[local-name()='input']"
        common_string = wd_locator['xpath'].replace(start_string, '').replace(input_string, '')

        xpath = ''.join((start_string, input_string, type_string, common_string))
        return {'xpath': xpath}

    def add_text(self):
        if 'text' not in self.selector:
            return ''

        text = self.selector.pop('text')
        if not isinstance(text, Pattern):
            return '[@value={}]'.format(XpathSupport.escape(text))
        elif self.is_simple_regexp(text):
            return "[contains(@value, '{}')]".format(text.pattern)
        else:
            self.selector['value'] = text
            return ''

    # private

    def _create_type_string(self, selector):
        typ = selector.get('type')
        if typ is True:
            return '[{}]'.format(self._negative_type_text)
        elif typ in TextField.NON_TEXT_TYPES:
            raise LocatorException('TextField Elements can not be located by type: {}'.format(typ))
        elif typ is None:
            return '[not(@type) or ({})]'.format(self._negative_type_text)

    @property
    def _negative_type_text(self):
        types = ["{}!={}".format(XpathSupport.lower('@type'), XpathSupport.escape(typ)) for
                 typ in TextField.NON_TEXT_TYPES]
        return ' and '.join(types)
