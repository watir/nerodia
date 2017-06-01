import six

from .html_elements import InputCollection
from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Hidden(Input):
    @property
    def visible(self):
        return False


@six.add_metaclass(MetaHTMLElement)
class HiddenCollection(InputCollection):
    pass
