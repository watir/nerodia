from ..element.validator import Validator as ElementValidator
from ...elements.button import Button


class Validator(ElementValidator):
    @staticmethod
    def validate(element, selector):
        if element.tag_name.lower() not in ['input', 'button']:
            return None
        # TODO - Verify this is desired behavior based on
        # https://bugzilla.mozilla.org/show_bug.cgi?id=1290963
        if element.tag_name.lower() == 'input' and element.get_attribute(
                'type').lower() not in Button.VALID_TYPES:
            return None

        return element
