import six

from .table_row import TableRow
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Row(TableRow):
    pass

# TODO: collection
