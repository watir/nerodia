import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Input(HTMLElement):
    _aliases = [['readonly', 'read_only']]
