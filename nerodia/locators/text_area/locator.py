from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    @property
    def _can_convert_regexp_to_contains(self):
        return False
