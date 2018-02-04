import six

from .html_elements import InputCollection
from .i_frame import IFrame
from .input import Input
from ..browser import Browser
from ..meta_elements import MetaHTMLElement
from ..user_editable import UserEditable


@six.add_metaclass(MetaHTMLElement)
class TextField(UserEditable, Input):
    NON_TEXT_TYPES = ['file', 'radio', 'checkbox', 'submit', 'reset', 'image', 'button', 'hidden',
                      'range', 'color', 'date', 'datetime-local']

    @property
    def selector_string(self):
        selector = self.selector.copy()
        selector['type'] = '(any text type)'
        selector['tag_name'] = 'input'

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
