import six

from .element import Element
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class HTMLElement(Element):
    pass

# TODO: collection
