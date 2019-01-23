from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):
    # private

    # value always requires a wire call since we want the property not the attribute
    def _process_attribute(self, key, value):
        if key != 'value':
            return super(XPath, self)._process_attribute(key, value)
        self.built['value'] = value
        return None
