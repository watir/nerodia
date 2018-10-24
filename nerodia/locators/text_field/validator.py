from ..element.validator import Validator as ElementValidator


class Validator(ElementValidator):
    @staticmethod
    def validate(element, selector):
        return element.tag_name.lower() == 'input'
