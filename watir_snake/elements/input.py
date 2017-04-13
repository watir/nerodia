import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Input(HTMLElement):
    _aliases = [['readonly', 'read_only']]
