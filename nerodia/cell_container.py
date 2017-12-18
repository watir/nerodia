import re
from .elements.cell import Cell, CellCollection


class CellContainer(object):
    def cell(self, *args, **kwargs):
        return Cell(self, dict(self._extract_selector(*args, **kwargs),
                               tag_name=re.compile('^(th|td)$')))

    def cells(self, *args, **kwargs):
        return CellCollection(self, dict(self._extract_selector(*args, **kwargs),
                                         tag_name=re.compile('^(th|td)$')))
