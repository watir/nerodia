from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder,\
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):

    def add_attributes(self, selector):
        attr_exp = self.attribute_expression(None, selector)

        expressions = ['./th', './td']
        if attr_exp:
            expressions = ['{}[{}]'.format(x, attr_exp) for x in expressions]

        return ' | '.join(expressions)

    @property
    def default_start(self):
        return ''

    def add_tag_name(self, selector):
        selector.pop('tag_name', None)
        return ''
