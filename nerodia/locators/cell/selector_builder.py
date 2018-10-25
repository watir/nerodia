from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder,\
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):
    # private

    @property
    def _start_string(self):
        return './' if self.adjacent is not None else './*'

    @property
    def _tag_string(self):
        if self.adjacent is not None:
            return super(XPath, self)._text_string

        return '[{} or {}]'.format(self._process_attribute('tag_name', 'th'),
                                   self._process_attribute('tag_name', 'td'))
