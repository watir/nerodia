import six

from .html_element import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TableCell(HTMLElement):
    # alias
    def colspan(self):
        return self.colspan()

    # alias
    def rowspan(self):
        return self.rowspan()
