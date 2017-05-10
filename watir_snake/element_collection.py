from importlib import import_module

import re

import watir_snake


class ElementCollection(object):
    def __init__(self, query_scope, selector):
        self.query_scope = query_scope
        self.selector = selector
        self.as_list = []
        self.elements = []

    def __iter__(self):
        """
        Yields each element in collection

        :rtype: iter

        :Example:

        divs = browser.divs(class='kls')
        for div in divs:
             print(div.text)
        """
        for e in self.to_list:
            yield e

    def __len__(self):
        """
        Returns the number of elements in the collection
        :rtype: int
        """
        return len(self.to_list)

    def __getitem__(self, idx):
        """
        Get the element at the given index

        Also note that because of lazy loading, this will return an Element instance even if
        the index is out of bounds

        :param idx: index of wanted element, 0-indexed
        :type idx: int
        :return: instance of Element subclass
        :rtype: watir_snake.elements.element.Element
        """
        return self.to_list[idx] or self._element_class(self.query_scope,
                                                        dict(index=idx, **self.selector))

    @property
    def to_list(self):
        """
        This collection as a list
        :rtype: list[watir_snake.elements.element.Element]
        """
        from .elements.html_elements import HTMLElement
        if not self.as_list:
            elements = []
            for idx, e in enumerate(self._elements):
                element = self._element_class(self.query_scope, dict(index=idx, **self.selector))
                if self._element_class == HTMLElement:
                    elements.append(element.to_subtype())
                else:
                    elements.append(element)
            self.as_list = elements
        return self.as_list

    def __eq__(self, other):
        """
        Returns true if two element collections are equal.

        :param other: other collection
        :rtype: bool

        :Example:

        browser.select_list(name='new_user_languages').options == \
            browser.select_list(id='new_user_languages').options   #=> True

        browser.select_list(name=;new_user_role').options == \
            browser.select_list(id='new_user_languages').options   #=> false
        """
        return self.to_list == other.to_list

    eql = __eq__

    # private

    @property
    def _elements(self):
        from .elements.i_frame import IFrame
        if isinstance(self.query_scope, IFrame):
            self.query_scope.switch_to()
        else:
            getattr(self.query_scope, 'assert_exists')()

        element_validator = self._element_validator_class()
        selector_builder = self._selector_builder_class(self.query_scope, self.selector,
                                                        self._element_class.ATTRIBUTES)
        locator = self._locator_class(self.query_scope, self.selector, selector_builder,
                                      element_validator)

        if not self.elements:
            self.elements = locator.locate_all()
        return self.elements

    @property
    def _locator_class(self):
        return self._import_module.Locator

    @property
    def _element_validator_class(self):
        return self._import_module.Validator

    @property
    def _selector_builder_class(self):
        return self._import_module.SelectorBuilder

    @property
    def _import_module(self):
        modules = [watir_snake.locator_namespace.__name__, self._element_class_name.lower()]
        try:
            return import_module('{}.{}'.format(*modules))
        except ImportError:
            return import_module('{}.element'.format(*modules[:1]))

    @property
    def _element_class_name(self):
        return self._element_class.__name__

    @property
    def _element_class(self):
        from .elements.svg_elements import SVGElementCollection
        from .elements.html_elements import HTMLElementCollection
        name = self.__class__.__name__.replace('Collection', '')
        element_module = re.sub(r'^(\w+)([A-Z]{1}\w+)$', r'\1_\2'.lower(), name).lower()
        try:
            module = import_module('watir_snake.elements.{}'.format(element_module))
        except ImportError:
            if isinstance(self, HTMLElementCollection):
                module = import_module('watir_snake.elements.html_elements')
            elif isinstance(self, SVGElementCollection):
                module = import_module('watir_snake.elements.svg_elements')
            else:
                raise TypeError(
                    'element class for {} could not be determined'.format(self.__class__.__name__))
        return getattr(module, name)
