from copy import copy

from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    def _using_selenium(self, *args):
        return None  # force using Nerodia

    def _matches_values(self, element, values):
        from ..element.validator import Validator
        if 'value' in values:
            cpy = copy(values)
            value = cpy.pop('value', None)

            return super(Locator, self)._matches_values(element, cpy) and \
                (Validator.match_str_or_regex(value, self._fetch_value(element, 'value')) or
                 Validator.match_str_or_regex(value, self._fetch_value(element, 'text')))
        else:
            return super(Locator, self)._matches_values(element, values)
