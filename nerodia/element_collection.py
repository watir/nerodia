from importlib import import_module
from itertools import islice

import nerodia
from .locators.class_helpers import ClassHelpers


class ElementCollection(ClassHelpers):
    def __init__(self, query_scope, selector):
        self.query_scope = query_scope
        self.selector = selector
        self.generator = ()
        self.els = []
        self.locator = None
        self.elements = None

    def __iter__(self):
        """
        Yields each element in collection

        :rtype: iter

        :Example:

        divs = browser.divs(class='kls')
        for div in divs:
             print(div.text)
        """
        from .elements.html_elements import HTMLElement
        from .elements.input import Input
        dic = {}
        for idx, e in enumerate(self._elements):
            element = self._element_class(self.query_scope, dict(self.selector, index=idx,
                                                                 element=e))
            if element.__class__ in [HTMLElement, Input]:
                tag_name = element.tag_name
                dic[tag_name] = dic.get(tag_name, 0)
                dic[tag_name] += 1
                kls = nerodia.tag_to_class.get(tag_name)
                new_selector = dict(self.selector, element=e, tag_name=tag_name,
                                    index=dic[tag_name] - 1)
                yield kls(self.query_scope, new_selector)
            else:
                yield element

    def __len__(self):
        """
        Returns the number of elements in the collection
        :rtype: int
        """
        return len([_ for _ in self])

    def __getitem__(self, idx):
        """
        Get the element at the given index

        Any call to an ElementCollection including an adjacent selector
        can not be lazy loaded because it must store correct type

        :param idx: index of wanted element, 0-indexed
        :type idx: int
        :return: instance of Element subclass
        :rtype: nerodia.elements.element.Element
        """
        if isinstance(idx, slice):
            return list(islice(self, idx.start, idx.stop, idx.step))
        elif 'adjacent' in self.selector:
            try:
                return list(islice(self, idx + 1))[idx]
            except IndexError:
                return self._element_class(self.query_scope, {'invalid_locator': True})
        else:
            return self._element_class(self.query_scope, dict(self.selector, index=idx))

    @property
    def is_empty(self):
        """
        Returns True if no elements are found

        :Example:

        browser.select_list(name='new_user_languages').options(class_name='not_here').is_empty

        :Example:

        browser.select_list(name='new_user_languages').options(id='danish').is_empty

        :return: True if no elements are found
        :rtype: bool
        """
        return len(self) == 0

    @property
    def to_list(self):
        """
        This collection as a list

        :rtype: list[nerodia.elements.element.Element]
        """
        nerodia.logger.deprecate('ElementCollection.to_list', 'list(self)')
        return list(self)

    def locate(self):
        """
        Locate all elements and return self

        :rtype: ElementCollection
        """
        list(self)
        return self

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
        return list(self) == list(other)

    eql = __eq__

    # private

    @property
    def _elements(self):
        if self.locator is None:
            self.locator = self._build_locator()
        if self.elements is None:
            self.elements = self.locator.locate_all()
        return self.elements

    @property
    def _element_class(self):
        from .elements.svg_elements import SVGElementCollection
        from .elements.html_elements import HTMLElementCollection
        from .module_mapping import map_module
        name = self.__class__.__name__.replace('Collection', '')
        element_module = map_module(name)
        try:
            module = import_module('nerodia.elements.{}'.format(element_module))
        except ImportError:
            if isinstance(self, HTMLElementCollection):
                module = import_module('nerodia.elements.html_elements')
            elif isinstance(self, SVGElementCollection):
                module = import_module('nerodia.elements.svg_elements')
            else:
                raise TypeError(
                    'element class for {} could not be determined'.format(name))
        return getattr(module, name)
