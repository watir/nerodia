import six

from .element import Element
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class HTMLElement(Element):
    pass
