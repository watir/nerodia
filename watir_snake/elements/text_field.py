import six

from .input import Input
from ..meta_elements import MetaHTMLElement
from ..user_editable import UserEditable


@six.add_metaclass(MetaHTMLElement)
class TextField(UserEditable, Input):
    # TODO update
    pass
