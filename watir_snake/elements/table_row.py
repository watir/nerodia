import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class TableRow(HTMLElement):
    # TODO: include CellContainer

    def __getitem__(self, idx):
        """
        Get the nth cell (<th> or <td>) of this row
        :param idx: index to get
        :rtype: watir_snake.elements.cell.Cell
        """
        return self.cell('index', idx)
