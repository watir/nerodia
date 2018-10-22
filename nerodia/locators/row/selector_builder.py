from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder,\
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):
    def _build_wd_selector(self, selector, values):
        self._xpath_builder.scope_tag_name = self.query_scope.selector.get('tag_name')
        return super(SelectorBuilder, self)._build_wd_selector(selector, values)


class XPath(ElementXPath):

    def __init__(self, use_element_label):
        super(XPath, self).__init__(use_element_label)
        self.scope_tag_name = None

    def add_attributes(self, selector):
        attr_expr = self.attribute_expression(None, selector)

        expressions = self._generate_expressions()
        if attr_expr:
            expressions = ['{}[{}]'.format(x, attr_expr) for x in expressions]
        return ' | '.join(expressions)

    def add_tag_name(self, selector):
        selector.pop('tag_name', None)
        return ''

    @property
    def default_start(self):
        return ''

    # private

    def _generate_expressions(self):
        expressions = ['./tr']

        if not self.scope_tag_name or self.scope_tag_name in ['tbody', 'tfoot', 'thead']:
            return expressions
        else:
            expressions += ['./tbody/tr', './thead/tr', './tfoot/tr']

        return expressions
