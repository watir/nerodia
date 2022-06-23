import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement
from ..user_editable import UserEditable


@six.add_metaclass(MetaHTMLElement)
class TextArea(UserEditable, HTMLElement):
    pass
