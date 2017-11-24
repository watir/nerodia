from copy import copy

import six

from .html_elements import InputCollection
from .i_frame import IFrame
from .html_elements import Input
from .text_area import TextArea
from ..browser import Browser
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TextField(TextArea, Input):
    NON_TEXT_TYPES = ['file', 'radio', 'checkbox', 'submit', 'reset', 'image', 'button', 'hidden',
                      'range', 'color']

    @property
    def selector_string(self):
        selector = copy(self.selector)
        selector['type'] = '(any text type)'
        selector['tag_name'] = 'input or textarea'

        if isinstance(self.query_scope, Browser) or isinstance(self.query_scope, IFrame):
            return super(TextField, self).selector_string
        else:
            return '{} --> {}'.format(self.query_scope.selector_string, selector)


@six.add_metaclass(MetaHTMLElement)
class TextFieldCollection(InputCollection):
    # private
    @property
    def _element_class(self):
        return TextField
