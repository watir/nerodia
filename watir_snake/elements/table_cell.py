import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class TableCell(HTMLElement):
    _aliases = [['colspan', 'col_span'], ['rowspan', 'row_span']]
