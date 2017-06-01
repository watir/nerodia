from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    def locate_all(self):
        return self._find_all_by_multiple()

    # private

    def _by_id(self):
        return None
