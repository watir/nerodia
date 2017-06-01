from ..element.validator import Validator as ElementValidator


class Validator(ElementValidator):
    @staticmethod
    def validate(element, selector):
        if element.tag_name.lower() == 'input':
            return element
