class CellContainer(object):
    def cell(self, *args, **kwargs):
        from .elements.cell import Cell
        return Cell(self, self._extract_selector(tag_name=r'^(th|td)$', *args, **kwargs))

    def cells(self, *args, **kwargs):
        from .elements.cell import CellCollection
        return CellCollection(self, self._extract_selector(tag_name=r'^(th|td)$', *args, **kwargs))
