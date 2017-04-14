import six

from .html_element import HTMLElement
from ..exception import Error
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Table(HTMLElement):
    # TODO: include RowContainer

    @property
    def dicts(self):
        """
        Represents table rows as dictionaries
        :return:
        """
        all_rows = self.rows().to_list
        if all_rows:
            header_row = all_rows.pop(0)
        else:
            raise Error('no rows in table')

        headers = [cell.text for cell in header_row.ths()]
        result = []

        for idx, row in all_rows:
            cells = list(row.cells())
            if len(cells) != len(headers):
                raise Error("row at index {} has {} cells, expected "
                            "{}".format(idx, len(cells), len(headers)))

            result.append(dict(zip(headers, cells)))
        return result

    def __getitem__(self, idx):
        """
        Returns row of this table with given index

        :param idx: row index
        :rtype: watir_snake.elements.row.Row
        """
        return self.row('index', idx)
