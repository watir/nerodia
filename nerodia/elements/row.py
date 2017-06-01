import six

from .html_elements import TableRowCollection
from .table_row import TableRow
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Row(TableRow):
    pass


@six.add_metaclass(MetaHTMLElement)
class RowCollection(TableRowCollection):
    def to_a(self):
        # we do this craziness since the xpath used will find direct child rows
        # before any rows inside thead/tbody/tfoot...
        elements = super(RowCollection, self).to_list
        return sorted(elements, key=lambda e: int(e.attribute_value('rowIndex')))
