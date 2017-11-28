import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement
from ..row_container import RowContainer


@six.add_metaclass(MetaHTMLElement)
class TableSection(RowContainer, HTMLElement):
    def __getitem__(self, idx):
        """
        Returns row of this table with given index

        :param idx: row index
        :rtype: nerodia.elements.row.Row
        """
        return self.row(index=idx)
