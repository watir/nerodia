import six

from .html_elements import TableRowCollection
from .table_row import TableRow
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Row(TableRow):
    pass


@six.add_metaclass(MetaHTMLElement)
class RowCollection(TableRowCollection):
    def __init__(self, *args, **kwargs):
        self.list = None
        super(RowCollection, self).__init__(*args, **kwargs)

    @property
    def to_list(self):
        # we do this craziness since the xpath used will find direct child rows
        # before any rows inside thead/tbody/tfoot...
        if not self.list:
            elements = super(RowCollection, self).to_list
            self.list = sorted(elements, key=lambda e: int(e.attribute_value('rowIndex')))
        return self.list
