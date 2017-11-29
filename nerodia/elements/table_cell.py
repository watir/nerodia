import six

import nerodia
from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class TableCell(HTMLElement):
    _attr_colspan = (int, 'colSpan')
    _attr_rowspan = (int, 'rowSpan')
    _attr_headers = (str, 'headers')
    _attr_cellindex = (int, 'cellIndex')
    _attr_align = (str, 'align')
    _attr_axis = (str, 'axis')
    _attr_ch = (str, 'ch')
    _attr_choff = (str, 'choff')
    _attr_nowrap = (bool, 'noWrap')
    _attr_valign = (str, 'vAlign')
    _attr_bgcolor = (str, 'bgcolor')

    @property
    def column_header(self):
        current_row = self.parent(tag_name='tr')
        return self._header_row(current_row, index=len(self.previous_siblings()))

    def sibling_from_header(self, **opt):
        current_row = self.parent(tag_name='tr')
        header = self._header_row(current_row, **opt)
        index = len(header.previous_siblings())

        return self.__class__(current_row, {'tag_name': 'td', 'index': index})

    # private

    def _header_row(self, current_row, **opt):
        table = self.parent(tag_name='table')
        header_row = table.tr()

        table._cell_size_check(header_row, current_row)

        header_type = 'th' if table.th().exist else 'tr'
        opt['tag_name'] = header_type

        return nerodia.tag_to_class[header_type](header_row, opt)
