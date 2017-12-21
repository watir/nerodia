from copy import copy

from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    def _using_selenium(self, *args):
        return None  # force using Nerodia

    def _matches_selector(self, element, selector):
        selector = copy(selector)

        tag_name = element.tag_name.lower()

        for key in ['text', 'value', 'label']:
            if key in selector:
                correct_key = 'value' if tag_name == 'input' else 'text'
                selector[correct_key] = selector.pop(key)

        return super(Locator, self)._matches_selector(element, selector)
