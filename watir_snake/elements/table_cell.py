import six

from .html_element import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TableCell(HTMLElement):
    _aliases = [['colspan', 'col_span'], ['rowspan', 'row_span']]
