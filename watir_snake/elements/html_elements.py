import six

from .element import Element
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class HTMLElement(Element):
    pass
