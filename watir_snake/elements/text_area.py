import six

from .html_element import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TextArea(HTMLElement):
    # TODO: include UserEditable
    pass
