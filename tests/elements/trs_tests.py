import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTrs(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.trs(id='outer_second').to_list == [browser.tr(id='outer_second')]

    def test_returns_the_correct_number_of_cells_table_context(self, browser):
        assert len(browser.table(id='inner').trs()) == 1
        assert len(browser.table(id='outer').trs()) == 4

    def test_returns_the_correct_number_of_cells_page_context(self, browser):
        assert len(browser.trs()) == 14

    def test_get_item_returns_the_row_at_the_given_index_table_context(self, browser):
        assert browser.table(id='outer').trs()[0].id == 'outer_first'

    def test_get_item_returns_the_row_at_the_given_index_page_context(self, browser):
        assert browser.trs()[0].id == 'thead_row_1'

    def test_iterates_through_rows_correctly(self, browser):
        inner_table = browser.table(id='inner')
        count = 0

        for index, tr in enumerate(inner_table.trs()):
            assert tr.id == inner_table.tr(index=index).id
            count += 1

        assert count > 0

    def test_iterates_through_the_outer_table_correctly(self, browser):
        outer_table = browser.table(id='outer')
        count = 0

        for index, tr in enumerate(outer_table.trs()):
            assert tr.id == outer_table.tr(index=index).id
            count += 1

        assert count > 0
