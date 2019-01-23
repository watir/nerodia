from copy import copy
from importlib import import_module


class ClassHelpers(object):

    @property
    def selector_builder(self):
        if not self._selector_builder:
            self._selector_builder = self._selector_builder_class(self._element_class.ATTRIBUTES,
                                                                  self.query_scope)
        return self._selector_builder

    @property
    def locator(self):
        if not self._element_matcher:
            self._element_matcher = self._element_matcher_class(self.query_scope,
                                                                copy(self.selector))
        if not self._locator:
            self._locator = self._locator_class(self._element_matcher)

        return self._locator

    # private

    @property
    def _locator_class(self):
        from .element.locator import Locator
        return getattr(self._import_module, 'Locator', Locator)

    @property
    def _element_matcher_class(self):
        from .element.matcher import Matcher
        return getattr(self._import_module, 'Matcher', Matcher)

    @property
    def _selector_builder_class(self):
        from .element.selector_builder import SelectorBuilder
        return getattr(self._import_module, 'SelectorBuilder', SelectorBuilder)

    @property
    def _import_module(self):
        from ..module_mapping import map_module
        modules = [self.browser.locator_namespace.__name__, map_module(self._element_class_name)]
        try:
            return import_module('{}.{}'.format(*modules))
        except ImportError:
            return import_module('{}.element'.format(*modules[:1]))

    @property
    def _element_class_name(self):
        return self._element_class.__name__

    @staticmethod
    def _flatten(term):
        for x in term:
            if isinstance(x, (list, tuple)):
                for y in x:
                    yield y
            else:
                yield x
