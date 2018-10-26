import re
from copy import copy

import nerodia
from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    def _using_selenium(self, *args):
        return None  # force using Nerodia

    def _matches_values(self, element, values):
        if 'value' not in values:
            return super(Locator, self)._matches_values(element, values)

        cpy = copy(values)
        value = cpy.pop('value', None)

        everything_except_value = super(Locator, self)._matches_values(element, cpy)

        matches_value = re.search(value, self._fetch_value(element, 'value')) is not None
        matches_text = re.search(value, self._fetch_value(element, 'text')) is not None

        if matches_text:
            nerodia.logger.deprecate("'value' locator key for finding button text",
                                     "user 'text' locator",
                                     ids=['value_button'])

        return everything_except_value and (matches_value or matches_text)
