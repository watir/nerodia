import logging

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class SelectorBuilder(ElementSelectorBuilder):
    def _build_wd_selector(self, selectors):
        if any(isinstance(val, Pattern) for val in selectors.values()):
            return None

        expressions = ['./th', './td']
        attr_expr = self.xpath_builder.attribute_expression(None, selectors)

        if attr_expr:
            expressions = ['{}[{}]'.format(e, attr_expr) for e in expressions]

        xpath = " | ".join(expressions)

        logging.debug({'build_wd_selector': xpath})

        return ['xpath', xpath]
