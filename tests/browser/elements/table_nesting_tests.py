import re

import pytest

pytestmark = pytest.mark.page('nested_tables.html')


class TestNestedTables(object):
    def test_returns_the_correct_number_of_rows_under_a_table_element(self, browser):
        tables = browser.div(id='table-rows-test').tables(id=re.compile(r'^tbl'))
        assert len(tables) > 0

        for table in tables:
            expected = int(table.data_row_count)
            actual = len(table.rows())
            browser_count = int(table.data_browser_count)

            assert actual == expected, 'expected {} rows, got {} for table id={}, browser reported: {}'.format(expected, actual, table.id, browser_count)

    def test_returns_the_correct_number_of_cells_under_a_row(self, browser):
        rows = browser.div(id='row-cells-test').trs(id=re.compile(r'^row'))
        assert len(rows) > 0

        for row in rows:
            expected = int(row.data_cell_count)
            actual = len(row.cells())
            browser_count = int(row.data_browser_count)

            assert actual == expected, 'expected {} rows, got {} for row id={}, browser reported: {}'.format(expected, actual, row.id, browser_count)

    def test_returns_the_correct_number_of_rows_under_a_table_section(self, browser):
        tbodies = browser.table(id='tbody-rows-test').tbodys(id=re.compile(r'^body'))
        assert len(tbodies) > 0

        for tbody in tbodies:
            expected = int(tbody.data_rows_count)
            actual = len(tbody.rows())
            browser_count = int(tbody.data_browser_count)

            assert actual == expected, 'expected {} rows, got {} for tbody id={}, browser reported: {}'.format(expected, actual, tbody.id, browser_count)
