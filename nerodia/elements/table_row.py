import six

from .html_elements import HTMLElement
from ..cell_container import CellContainer
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TableRow(CellContainer, HTMLElement):
    def __iter__(self):
        """
        Yields each TableCell associated with this row
        :rtype: iter

        :Example:

        row = browser.tr()
        for cell in row:
            print(cell.text)
        """
        for cell in self.cells():
            yield cell

    def __getitem__(self, idx):
        """
        Get the nth cell (<th> or <td>) of this row
        :param idx: index to get
        :rtype: nerodia.elements.cell.Cell
        """
        return self.cell(index=idx)
