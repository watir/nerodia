from copy import copy

from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    def _using_selenium(self, *args):
        return None  # force using Nerodia

    @property
    def _can_convert_regexp_to_contains(self):
        # regexp conversion won't work with the complex xpath selector
        return False

    def _matches_selector(self, element, selector):
        from ..element.validator import Validator
        if 'value' in selector:
            cpy = copy(selector)
            value = cpy.pop('value', None)

            return super(Locator, self)._matches_selector(element, cpy) and \
                (Validator.match_str_or_regex(value, self._fetch_value(element, 'value')) or
                 Validator.match_str_or_regex(value, self._fetch_value(element, 'text')))
        else:
            return super(Locator, self)._matches_selector(element, selector)
