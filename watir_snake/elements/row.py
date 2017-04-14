import six

from .table_row import TableRow
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Row(TableRow):
    pass

# TODO: collection
