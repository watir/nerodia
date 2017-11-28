class RowContainer(object):
    def row(self, *args, **kwargs):
        from .elements.row import Row
        return Row(self, self._extract_selector(tag_name='tr', *args, **kwargs))

    def rows(self, *args, **kwargs):
        from .elements.row import RowCollection
        return RowCollection(self, self._extract_selector(tag_name='tr', *args, **kwargs))

    @property
    def strings(self):
        """
        A table as a 2D array of strings with the text of each cell
        :rtype: list[list[str]]
        """
        self.wait_for_exists()

        rows = []
        for row in self.rows():
            rows.append([cell.text for cell in row])
        return rows
