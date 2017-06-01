from copy import copy

from ..element.locator import Locator as ElementLocator
from ...elements.text_field import TextField


class Locator(ElementLocator):
    def locate_all(self):
        return self._find_all_by_multiple()

    # private

    def _wd_find_first_by(self, how, what):
        if how == 'tag_name':
            how, what = self.selector_builder._build_wd_selector({'how': what})
        return super(Locator, self)._wd_find_first_by(how, what)

    def _matches_selector(self, element, selector):
        selector = copy(selector)

        tag_name = element.tag_name.lower()

        for key in ['text', 'value', 'label']:
            if key in selector:
                correct_key = 'value' if tag_name == 'input' else 'text'
                selector[correct_key] = selector.pop(key)

        return super(Locator, self)._matches_selector(element, selector)

    def _by_id(self):
        element = super(Locator, self)._by_id()

        if element and element.get_attribute('type') not in TextField.NON_TEXT_TYPES:
            return element
