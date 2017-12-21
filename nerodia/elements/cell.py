import six

from .html_elements import TableCellCollection
from .table_cell import TableCell
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Cell(TableCell):
    pass


@six.add_metaclass(MetaHTMLElement)
class CellCollection(TableCellCollection):
    @property
    def _elements(self):
        # we do this craziness since the xpath used will find direct child rows
        # before any rows inside thead/tbody/tfoot...
        elements = super(CellCollection, self)._elements
        return sorted(elements, key=lambda e: int(e.get_attribute('cellIndex')))
