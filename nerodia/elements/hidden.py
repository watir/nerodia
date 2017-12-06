import six

from .html_elements import Input, InputCollection
from ..exception import ObjectDisabledException
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Hidden(Input):
    @property
    def visible(self):
        return False

    def click(self):
        raise ObjectDisabledException('click is not available on the hidden field element')


@six.add_metaclass(MetaHTMLElement)
class HiddenCollection(InputCollection):
    pass
