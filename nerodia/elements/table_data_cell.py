import six

from .table_cell import TableCell
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TableDataCell(TableCell):
    _attr_abbr = (str, 'abbr')
    pass
