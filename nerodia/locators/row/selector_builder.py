from importlib import import_module

from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder, \
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):

    def _build_wd_selector(self, selector):
        scope_tag_name = self.query_scope.selector.get('tag_name', self.query_scope.tag_name)
        try:
            mod = import_module(self.__module__)
            xpath = getattr(mod, 'XPath', XPath)
        except ImportError:
            xpath = XPath
        return xpath().build(selector, scope_tag_name)

    @property
    def _merge_scope(self):
        return False


class XPath(ElementXPath):

    def build(self, selector, scope_tag_name):
        if 'adjacent' in selector:
            return super(XPath, self).build(selector)

        index = selector.pop('index', None)

        super(XPath, self).build(selector)
        common_string = self.built.pop('xpath', None)

        expressions = self._generate_expressions(scope_tag_name)
        if len(common_string) > 0:
            expressions = ["{}{}".format(e, common_string) for e in expressions]

        xpath = ' | '.join(expressions)
        self.built['xpath'] = self._add_index(xpath, index) if index is not None else xpath

        return self.built

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
            self.built['text'] = self.selector.pop('text')
        return ''

    def _generate_expressions(self, scope_tag_name):
        if scope_tag_name in ['tbody', 'tfoot', 'thead']:
            return ["./*[local-name()='tr']"]
        else:
            return ["./*[local-name()='tr']",
                    "./*[local-name()='tbody']/*[local-name()='tr']",
                    "./*[local-name()='thead']/*[local-name()='tr']",
                    "./*[local-name()='tfoot']/*[local-name()='tr']"]
