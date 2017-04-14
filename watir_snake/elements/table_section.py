import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TableSection(HTMLElement):
    # TODO: include RowContainer

    def __getitem__(self, idx):
        """
        Returns row of this table with given index

        :param idx: row index
        :rtype: watir_snake.elements.row.Row
        """
        return self.row('index', idx)
