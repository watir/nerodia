from nerodia.exception import LocatorException
from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath
from ..element.xpath_support import XpathSupport
from ...elements.text_field import TextField


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):
    # private

    @property
    def _text_string(self):
        if self.adjacent is not None:
            return super(XPath, self)._text_string
        if 'text' in self.selector:
            self.requires_matches['text'] = self.selector.pop('text')
        return ''

    @property
    def _additional_string(self):
        if self.adjacent is not None:
            return ''
        return self._type_string(self.selector.pop('type', None))

    @property
    def _tag_string(self):
        if self.adjacent is None:
            self.selector['tag_name'] = 'input'
        return super(XPath, self)._tag_string

    def _type_string(self, typ):
        if typ is True:
            return '[{}]'.format(self._negative_type_text)
        elif typ in TextField.NON_TEXT_TYPES:
            raise LocatorException('TextField Elements can not be located by type: {}'.format(typ))
        elif typ is None:
            return '[not(@type) or ({})]'.format(self._negative_type_text)
        else:
            return '[{}]'.format(self._process_attribute('type', typ))

    @property
    def _negative_type_text(self):
        types = ['{}!={}'.format(self._lhs_for('type', lower=True), XpathSupport.escape(typ)) for
                 typ in TextField.NON_TEXT_TYPES]
        return ' and '.join(types)
