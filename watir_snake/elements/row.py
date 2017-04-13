import six

from .table_row import TableRow
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Row(TableRow):
    pass

# TODO: collection
