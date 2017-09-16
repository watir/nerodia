
class Validator(object):

    @staticmethod
    def validate(element, selector):
        selector_tag_name = selector.get('tag_name')
        element_tag_name = element.tag_name.lower()

        if selector_tag_name and selector_tag_name != element_tag_name:
            return None

        return element
