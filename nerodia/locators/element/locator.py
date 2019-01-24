from copy import copy
from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from nerodia.exception import LocatorException
from nerodia.locators import W3C_FINDERS
from nerodia.locators.class_helpers import ClassHelpers


class Locator(object):
    built = None
    driver_scope = None

    def __init__(self, element_matcher):
        self.element_matcher = element_matcher
        self.query_scope = element_matcher.query_scope  # either element or browser
        self.selector = element_matcher.selector

    def locate(self, built):
        try:
            self.built = copy(built)
            self.driver_scope = self._locator_scope.wd
            return self._matching_elements(self.built, 'first')
        except (NoSuchElementException):
            return None

    def locate_all(self, built):
        self.built = copy(built)
        self.driver_scope = self._locator_scope.wd
        if 'index' in self.built:
            raise ValueError("can't locate all elements by 'index'")

        return list(ClassHelpers._flatten(self._matching_elements(self.built, 'all')))

    # private

    def _matching_elements(self, built, filter='first'):
        if len(built) == 1 and filter == 'first':
            return self._locate_element(*list(ClassHelpers._flatten(built.items())))

        wd_locator_int = list(set(W3C_FINDERS).intersection(self.built.keys()))
        wd_locator_key = wd_locator_int[0] if wd_locator_int else None
        wd_locator = {}
        match_values = {}
        for key, value in built.items():
            if wd_locator_key == key:
                wd_locator[key] = value
            else:
                match_values[key] = value

        retries = 0
        while retries <= 2:
            try:
                elements = self._locate_elements(*list(ClassHelpers._flatten(wd_locator.items())))

                return self.element_matcher.match(elements, match_values, filter)
            except StaleElementReferenceException:
                retries += 1
                sleep(0.5)
                pass

        target = 'element collection' if filter == 'all' else 'element'
        raise LocatorException('Unable to locate {} from {} due to changing '
                               'page'.format(target, self.selector))

    @property
    def _locator_scope(self):
        return self.built.pop('scope') if 'scope' in self.built else self.query_scope.browser

    def _locate_element(self, how, what, scope=None):
        scope = scope or self.driver_scope
        return scope.find_element(W3C_FINDERS.get(how), what)

    def _locate_elements(self, how, what, scope=None):
        scope = scope or self.driver_scope
        return scope.find_elements(W3C_FINDERS.get(how), what)
