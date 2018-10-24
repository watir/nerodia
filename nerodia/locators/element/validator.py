import re


class Validator(object):

    @staticmethod
    def validate(element, tag_name):
        return re.search(r'{}'.format(tag_name), element.tag_name.lower()) is not None
