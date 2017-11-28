import re
from .elements.cell import Cell, CellCollection


class CellContainer(object):
    def cell(self, *args, **kwargs):
        return Cell(self, self._extract_selector(tag_name=re.compile('^(th|td)$'), *args, **kwargs))

    def cells(self, *args, **kwargs):
        return CellCollection(self, self._extract_selector(tag_name=re.compile('^(th|td)$'), *args,
                                                           **kwargs))
