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

    def __iter__(self):
        """
        Yields each row in collection

        :rtype: iter

        :Example:

        rows = browser.rows(class='kls')
        for row in rows:
             print(row.text)
        """
        # we do this craziness since the xpath used will find direct child rows
        # before any rows inside thead/tbody/tfoot...
        if not self.list:
            self._get_list()
        for item in self.list:
            yield item

    @property
    def to_list(self):
        # we do this craziness since the xpath used will find direct child rows
        # before any rows inside thead/tbody/tfoot...
        import nerodia
        nerodia.logger.deprecate('RowCollection.to_list', 'list(RowCollection)')
        return list(self)

    # private

    def _get_list(self):
        if not self.list:
            elements = list(super(RowCollection, self).__iter__())
            self.list = sorted(elements, key=lambda e: int(e.attribute_value('rowIndex')))
