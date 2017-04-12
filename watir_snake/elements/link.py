import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Anchor(HTMLElement):
    _attr_href = (str, 'href')

# TODO: container
