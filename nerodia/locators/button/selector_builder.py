from nerodia.exception import LocatorException
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
    def build(self, selector):
        if 'adjacent' in selector:
            return super(XPath, self).build(selector)

        selector['tag_name'] = 'button'

        typ = selector.pop('type', None)
        if typ is False:
            return super(XPath, self).build(selector)

        # both value and text selectors will locate elements by value attribute or text content
        if 'value' in selector:
            selector['text'] = selector.pop('value')

        wd_locator = super(XPath, self).build(selector)
        start_string = self.default_start
        button_string = "local-name()='button'"
        common_string = wd_locator['xpath'].replace(start_string, '')\
            .replace('[{}]'.format(button_string), '')

        input_string = "(local-name()='input' and {})".format(self._input_types(typ))

        if typ is None:
            tag_string = '[{} or {}]'.format(button_string, input_string)
        else:
            tag_string = '[{}]'.format(input_string)

        xpath = ''.join((start_string, tag_string, common_string))

        return {'xpath': xpath}

    @property
    def use_index(self):
        return False

    def add_text(self):
        if 'text' not in self.selector:
            return ''

        text = self.selector.pop('text')
        if not isinstance(text, Pattern):
            return "[normalize-space()='{0}' or @value='{0}']".format(text)
        elif XpathSupport.is_simple_regexp(text):
            return "[contains(text(), '{0}') or contains(@value, '{0}')]".format(text.pattern)
        else:
            self.requires_matches['text'] = text
            return ''

    # private

    def _input_types(self, typ):
        if typ in [None, True]:
            types = Button.VALID_TYPES
        elif typ not in Button.VALID_TYPES:
            msg = 'Button Elements can not be located by input type: {}'.format(typ)
            raise LocatorException(msg)
        else:
            types = [typ]

        return ' or '.join(['{}={}'.format(XpathSupport.lower('@type'),
                                           XpathSupport.escape(b)) for b in types])
