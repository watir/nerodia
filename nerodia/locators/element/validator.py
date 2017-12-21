import re


class Validator(object):

    @staticmethod
    def validate(element, selector):
        selector_tag_name = selector.get('tag_name')
        element_tag_name = element.tag_name.lower()

        if selector_tag_name:
            if Validator.match_str_or_regex(selector_tag_name, element_tag_name):
                return element
        else:
            return None

    @staticmethod
    def match_str_or_regex(str_or_regex, term):
        if isinstance(str_or_regex, re._pattern_type) and str_or_regex.search(term):
            return True
        elif str_or_regex == term:
            return True
        else:
            return False
