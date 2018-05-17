from importlib import import_module

import nerodia


class ClassHelpers(object):
    # private

    @property
    def _locator_class(self):
        from .element.locator import Locator
        return getattr(self._import_module, 'Locator', Locator)

    @property
    def _element_validator_class(self):
        from .element.validator import Validator
        return getattr(self._import_module, 'Validator', Validator)

    @property
    def _selector_builder_class(self):
        from .element.selector_builder import SelectorBuilder
        return getattr(self._import_module, 'SelectorBuilder', SelectorBuilder)

    @property
    def _import_module(self):
        from ..module_mapping import map_module
        modules = [nerodia.locator_namespace.__name__, map_module(self._element_class_name)]
        try:
            return import_module('{}.{}'.format(*modules))
        except ImportError:
            return import_module('{}.element'.format(*modules[:1]))

    @property
    def _element_class_name(self):
        return self._element_class.__name__

    def _build_locator(self):
        self.query_scope._ensure_context()

        element_validator = self._element_validator_class()
        selector_builder = self._selector_builder_class(self.query_scope, self.selector.copy(),
                                                        self._element_class.ATTRIBUTES)
        return self._locator_class(self.query_scope, self.selector.copy(), selector_builder,
                                   element_validator)
