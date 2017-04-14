import six

from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Hidden(Input):
    @property
    def visible(self):
        return False

# TODO: container
# TODO: collection
