from copy import copy
from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from nerodia.exception import LocatorException
from nerodia.locators import W3C_FINDERS
from nerodia.locators.class_helpers import ClassHelpers


class Locator(object):
    built = None
    driver_scope = None
    filter = None
    locator_scope = None
    match_values = None
    wd_locator = None

    def __init__(self, element_matcher):
        self.element_matcher = element_matcher
        self.query_scope = element_matcher.query_scope  # either element or browser
        self.selector = element_matcher.selector

    def locate(self, built):
        try:
            self.built = copy(built)
            self.driver_scope = self._locator_scope.wd
            self.filter = 'first'
            return self._matching_elements
        except (NoSuchElementException):
            return None

    def locate_all(self, built):
        self.built = copy(built)
        self.driver_scope = self._locator_scope.wd
        self.filter = 'all'
        if 'index' in self.built:
            raise ValueError("can't locate all elements by 'index'")

        return list(ClassHelpers._flatten(self._matching_elements))

    # private

    @property
    def _matching_elements(self):
        if len(self.built) == 1 and self.filter == 'first':
            return self._locate_element(*list(ClassHelpers._flatten(self.built.items())))

        retries = 0
        while retries <= 2:
            try:
                locator = list(ClassHelpers._flatten(self._wd_locator.items()))
                elements = self._locate_elements(*locator)

                return self.element_matcher.match(elements, self._match_values, self.filter)
            except StaleElementReferenceException:
                retries += 1
                sleep(0.5)
                pass

        target = 'element collection' if self.filter == 'all' else 'element'
        raise LocatorException('Unable to locate {} from {} due to changing '
                               'page'.format(target, self.selector))

    @property
    def _locator_scope(self):
        scope = self.built.pop('scope', None)

        if self.locator_scope is None:
            self.locator_scope = scope if scope is not None else self.query_scope.browser
        return self.locator_scope

    @property
    def _wd_locator(self):

        self.wd_locator = {}
        for key, value in self.built.items():
            if self._wd_locator_key == key:
                self.wd_locator[key] = value
        return self.wd_locator

    @property
    def _match_values(self):
        self.match_values = {}
        for key, value in self.built.items():
            if self._wd_locator_key != key:
                self.match_values[key] = value
        return self.match_values

    @property
    def _wd_locator_key(self):
        intersect = list(set(W3C_FINDERS).intersection(self.built.keys()))
        return intersect[0] if intersect else None

    def _locate_element(self, how, what, scope=None):
        scope = scope or self.driver_scope
        return scope.find_element(W3C_FINDERS.get(how), what)

    def _locate_elements(self, how, what, scope=None):
        scope = scope or self.driver_scope
        return scope.find_elements(W3C_FINDERS.get(how), what)
