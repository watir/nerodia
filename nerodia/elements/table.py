import six

from .html_elements import HTMLElement
from ..exception import Error
from ..meta_elements import MetaHTMLElement
from ..row_container import RowContainer


@six.add_metaclass(MetaHTMLElement)
class Table(RowContainer, HTMLElement):
    def __iter__(self):
        """
        Yields each TableRow associated with this table
        :rtype: iter

        :Example:

        table = browser.table()
        for row in table:
            print(row.text)
        """
        for row in self.rows():
            yield row

    @property
    def dicts(self):
        """
        Represents table rows as dictionaries
        :rtype: list[dict]
        """
        all_rows = self.rows().locate()
        if len(all_rows) > 0:
            header_row = all_rows[0]
        else:
            raise Error('no rows in table')
        headers = [cell.text for cell in header_row.ths()]
        result = []

        for row in all_rows.to_list[1:]:
            self._cell_size_check(header_row, row)
            result.append(dict(zip(headers, [cell.text for cell in row.cells()])))
        return result

    def headers(self, row=None):
        """
        Returns first row of Table with proper subtype
        :rtype: TableCellCollection
        """
        row = row or self.rows()[0]
        if row.th().exist:
            return row.ths()
        else:
            return row.tds()

    def __getitem__(self, idx):
        """
        Returns row of this table with given index

        :param idx: row index
        :rtype: nerodia.elements.row.Row
        """
        return self.row(index=idx)

    # private

    def _cell_size_check(self, header_row, cell_row):
        header_size = len(header_row.cells())
        row_size = len(cell_row.cells())
        if header_size == row_size:
            return

        index = cell_row.selector.get('index')
        row_id = 'row at index {}'.format(index - 1) if index is not None else 'designated row'
        raise Error('{} has {} cells, while header row has '
                    '{}'.format(row_id, row_size, header_size))
