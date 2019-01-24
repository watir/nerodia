from copy import copy

import nerodia
from nerodia.locators.element.matcher import Matcher as ElementMatcher


class Matcher(ElementMatcher):
    # private

    def _elements_match(self, element, values_to_match):
        copy_values_to_match = copy(values_to_match)
        value = copy_values_to_match.pop('value', None)

        if value:
            matching = self._matches_values(self._fetch_value(element, 'text'), value)
            if matching:
                self._deprecate_value_button()
            if not matching:
                matching = self._matches_values(self._fetch_value(element, 'value'), value)

            if not matching:
                return False
            if len(copy_values_to_match) == 0:
                return True

        return super(Matcher, self)._elements_match(element, copy_values_to_match)

    def _deprecate_value_button(self):
        nerodia.logger.deprecate("'value' locator key for finding button text",
                                 "use 'text' locator", ids=['value_button'])

    def _validate_tag(self, element, _expected):
        from nerodia.elements.button import Button
        tag_name = self._fetch_value(element, 'tag_name')
        if tag_name not in ('input', 'button'):
            return

        typ = element.get_attribute('type').lower()
        if tag_name == 'input' and typ not in Button.VALID_TYPES:
            return

        return element
