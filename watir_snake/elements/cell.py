import six
from .table_cell import TableCell
from ..meta_element import MetaElement

@six.add_metaclass(MetaElement)
class Cell(TableCell):
    pass

# TODO: collection
