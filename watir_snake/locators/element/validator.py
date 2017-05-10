
class Validator(object):

    @staticmethod
    def validate(element, selector):
        selector_tag_name = selector.get('tag_name')
        element_tag_name = element.tag_name.lower()

        if selector_tag_name and selector_tag_name != element_tag_name:
            return None

        if element_tag_name == 'input':
            # TODO - Verify this is desired behavior based on https://bugzilla.mozilla.org/show_bug.cgi?id=1290963
            if selector.get('type') and selector.get('type') != element.get_attribute('type').lower():
                return None

        return element
