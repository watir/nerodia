from importlib import import_module

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):

    def __init__(self, valid_attributes, scope_tag_name):
        self.scope_tag_name = scope_tag_name
        super(SelectorBuilder, self).__init__(valid_attributes)

    def _build_wd_selector(self, selector):
        try:
            mod = import_module(self.__module__)
            xpath = getattr(mod, 'XPath', XPath)
        except ImportError:
            xpath = XPath
        return xpath().build(selector, self.scope_tag_name)


class XPath(ElementXPath):

    def build(self, selector, scope_tag_name):
        if 'adjacent' in selector:
            return super(XPath, self).build(selector)

        index = selector.pop('index', None)

        common_string = super(XPath, self).build(selector).get('xpath')

        expressions = self._generate_expressions(scope_tag_name)
        if len(common_string) > 0:
            expressions = ["{}{}".format(e, common_string) for e in expressions]

        xpath = ' | '.join(expressions)

        if index is not None:
            xpath = self._add_index(xpath, index)

        self.selector.update(self.requires_matches)

        return {'xpath': xpath}

    # private

    @property
    def _start_string(self):
        return './' if self.adjacent is not None else ''

    @property
    def _text_string(self):
        if self.adjacent is not None:
            return super(XPath, self)._text_string

        # Can not directly locate a Row with Text because all text is in the Cells;
        # needs to use Locator#locate_matching_elements
        if 'text' in self.selector:
            self.requires_matches['text'] = self.selector.pop('text')
        return ''

    def _generate_expressions(self, scope_tag_name):
        if scope_tag_name in ['tbody', 'tfoot', 'thead']:
            return ["./*[local-name()='tr']"]
        else:
            return ["./*[local-name()='tr']",
                    "./*[local-name()='tbody']/*[local-name()='tr']",
                    "./*[local-name()='thead']/*[local-name()='tr']",
                    "./*[local-name()='tfoot']/*[local-name()='tr']"]
