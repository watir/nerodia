import six

from .input import Input
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Hidden(Input):
    @property
    def visible(self):
        return False

# TODO: container
# TODO: collection
