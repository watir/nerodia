from nerodia.exception import LocatorException
from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder,\
    XPath as ElementXPath
from ...elements.button import Button

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):
    # private

    @property
    def _tag_string(self):
        if self.adjacent is not None:
            return super(XPath, self)._text_string

        # Selector builder ignores tag name and builds for both button elements and input
        # elements of type button
        self.selector.pop('tag_name', None)

        typ = self.selector.pop('type', None)
        text = self.selector.pop('text', None)

        string = '({})'.format(self._button_string(text=text, typ=typ))
        if typ is not False:
            string += ' or ({})'.format(self._input_string(text=text, typ=typ))
        return '[{}]'.format(string)

    def _button_string(self, text=None, typ=None):
        string = self._process_attribute('tag_name', 'button')
        if text is not None:
            string += ' and {}'.format(self._process_attribute('text', text))
        if typ is not None:
            string += ' and {}'.format(self._input_types(typ))
        return string

    def _input_string(self, text=None, typ=None):
        string = self._process_attribute('tag_name', 'input')
        if typ is True:
            typ = None
        string += ' and ({})'.format(self._input_types(typ))
        if text is not None:
            string += ' and {}'.format(self._process_attribute('value', text))
            self.requires_matches.pop('value', None)
        return string

    @property
    def _text_string(self):
        if self.adjacent is not None:
            return super(XPath, self)._text_string
        # text locator is already dealt with in #tag_name_string
        value = self.selector.pop('value', None)
        if value is None:
            return ''
        elif isinstance(value, Pattern):
            res = '[{} or {}]'.format(self._predicate_conversion('text', value),
                                      self._predicate_conversion('value', value))
            self.requires_matches.pop('text', None)
            return res
        else:
            return '[{} or {}]'.format(self._predicate_expression('text', value),
                                       self._predicate_expression('value', value))

    def _predicate_conversion(self, key, regexp):
        if key == 'text':
            res = super(XPath, self)._predicate_conversion('contains_text', regexp)
        else:
            res = super(XPath, self)._predicate_conversion(key, regexp)
        if 'contains_text' in self.requires_matches:
            self.requires_matches[key] = self.requires_matches.pop('contains_text')
        return res

    def _input_types(self, typ):
        if typ is None:
            types = Button.VALID_TYPES
        elif typ in Button.VALID_TYPES or typ in [True, False]:
            types = [typ]
        else:
            msg = 'Button Elements can not be located by input type: {}'.format(typ)
            raise LocatorException(msg)

        types = [self._predicate_expression('type', t) for t in types if t is not None]

        return ' or '.join(types)
