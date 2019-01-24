from importlib import import_module
from itertools import islice
from time import sleep

from selenium.common.exceptions import StaleElementReferenceException

import nerodia
from nerodia.exception import LocatorException
from nerodia.js_snippet import JSSnippet
from .locators.class_helpers import ClassHelpers


class ElementCollection(ClassHelpers, JSSnippet):

    _selector_builder = None
    _element_matcher = None
    _located = False
    _locator = None

    def __init__(self, query_scope, selector):
        self.query_scope = query_scope
        self.selector = selector
        self.generator = ()
        self._els = []
        if 'element' not in self.selector:
            self.build()

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
        for idx, (el, tag_name) in enumerate(self._elements_with_tags):
            selector = self.selector.copy()
            if idx != 0:
                selector['index'] = idx
            selector = dict(self.selector, index=idx)
            element = self._element_class(self.query_scope, selector)
            if element.__class__ in [HTMLElement, Input]:
                element = self._construct_subtype(element, dic, tag_name)
            element.cache = el
            yield element

    def __len__(self):
        """
        Returns the number of elements in the collection
        :rtype: int
        """
        self._els = self._els or [_ for _ in self]
        return len(self._els)

    def __getitem__(self, idx):
        """
        Get the element at the given index or slice

        Any call to an ElementCollection that includes an adjacent selector
        can not be lazy loaded because it must store correct type

        Slices can only be lazy loaded if the indices are positive

        :param idx: index of wanted element, 0-indexed
        :type idx: int
        :return: instance of Element subclass
        :rtype: nerodia.elements.element.Element
        """
        if isinstance(idx, slice):
            if idx.start and idx.start < 0 or idx.stop and idx.stop < 0:
                return list(self)[idx.start:idx.stop]
            else:
                return list(islice(self, idx.start, idx.stop, idx.step))
        elif 'adjacent' in self.selector:
            try:
                return list(islice(self, idx + 1))[idx]
            except IndexError:
                return self._element_class(self.query_scope, {'invalid_locator': True})
        elif len(self._els) > 0:
            try:
                return self._els[idx]
            except IndexError:
                pass
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

    def build(self):
        self.selector_builder.build(self.selector.copy())

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
        self.els = list(self)
        return self

    @property
    def browser(self):
        """
        Returns the browser of the current query_scope

        :rtype: nerodia.browser.Browser
        """
        return self.query_scope.browser

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
        self._ensure_context()
        if 'scope' in self.selector_builder.built:
            return self.query_scope._element_call(lambda: self._locate_all())
        else:
            return self._locate_all()

    @property
    def _elements_with_tags(self):
        els = self._elements
        if 'tag_name' in self.selector:
            return [(e, self.selector['tag_name']) for e in els]
        else:
            retries = 0
            while retries <= 2:
                try:
                    return zip(els, self._execute_js('getElementTags', els))
                except StaleElementReferenceException:
                    retries += 1
                    sleep(0.5)
                    pass

        raise LocatorException('Unable to locate element collection from {} due to changing '
                               'page'.format(self.selector))

    def _ensure_context(self):
        from nerodia.elements.i_frame import IFrame
        from nerodia.browser import Browser
        if isinstance(self.query_scope, Browser) or \
                (self.query_scope._located and self.query_scope.stale):
            self.query_scope.locate()
        if isinstance(self.query_scope, IFrame):
            self.query_scope.switch_to()

    def _locate_all(self):
        return self.locator.locate_all(self.selector_builder.built)

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

    def _construct_subtype(self, element, dic, tag_name):
        selector = element.selector
        dic[tag_name] = dic.get(tag_name, 0)
        dic[tag_name] += 1
        kls = nerodia.element_class_for(tag_name)
        selector.update({'index': dic[tag_name] - 1, 'tag_name': tag_name})
        return kls(self.query_scope, selector)
