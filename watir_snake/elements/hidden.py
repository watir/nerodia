import six

from .input import Input
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Hidden(Input):
    @property
    def visible(self):
        return False

# TODO: container
# TODO: collection
