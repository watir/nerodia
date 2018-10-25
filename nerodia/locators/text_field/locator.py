from ..element.locator import Locator as ElementLocator


class Locator(ElementLocator):
    # private

    def _using_selenium(self, *args):
        return None  # force using Nerodia

    def _matches_values(self, element, selector):
        tag_name = None

        for key in ['text', 'value', 'label', 'visible_text']:
            if key in selector.copy():
                tag_name = tag_name or element.tag_name.lower()
                correct_key = 'value' if tag_name == 'input' else 'text'
                selector[correct_key] = selector.pop(key)

        return super(Locator, self)._matches_values(element, selector)

    def _text_regexp_deprecation(self, *args):
        return None  # does not apply to text_field
