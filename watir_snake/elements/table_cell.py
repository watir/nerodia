import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class TableCell(HTMLElement):
    _aliases = [['colspan', 'col_span'], ['rowspan', 'row_span']]
