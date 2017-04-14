import six

from .element import Element
from ..meta_elements import MetaSVGElement


@six.add_metaclass(MetaSVGElement)
class SVGElement(Element):
    pass

# TODO: collection
