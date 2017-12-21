from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    def _using_selenium(self, *args):
        return None  # force using Nerodia
