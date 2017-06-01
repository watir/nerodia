from copy import copy

from ..element.locator import Locator as ElementLocator
from ...elements.button import Button


class Locator(ElementLocator):
    def locate_all(self):
        return self._find_all_by_multiple()

    # private

    def _wd_find_first_by(self, how, what):
        if how == 'tag_name':
            how = 'xpath'
            what = ".//button | .//input[{}]".format(
                self.selector_builder.xpath_builder.attribute_expression('input', {
                    'type': Button.VALID_TYPES}))

        return super(Locator, self)._wd_find_first_by(how, what)

    @property
    def _can_convert_regexp_to_contains(self):
        # regexp conversion won't work with the complex xpath selector
        return False

    def _matches_selector(self, element, selector):
        if 'value' in selector:
            cpy = copy(selector)
            value = cpy.pop('value', None)

            return super(Locator, self)._matches_selector(element, cpy) and \
                (value.search(self._fetch_value(element, 'value')) or
                 value.search(self._fetch_value(element, 'text')))
        else:
            return super(Locator, self)._matches_selector(element, selector)
