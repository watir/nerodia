import six

from .table_cell import TableCell
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Cell(TableCell):
    pass

# TODO: collection
