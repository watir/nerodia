from .elements.cell import Cell, CellCollection


class CellContainer(object):
    def cell(self, *args, **kwargs):
        return Cell(self, self._extract_selector(*args, **kwargs))

    def cells(self, *args, **kwargs):
        return CellCollection(self, self._extract_selector(*args, **kwargs))
