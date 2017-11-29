import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTables(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.tables(rules='groups').to_list == [browser.table(rules='groups')]

    def test_returns_the_number_of_tables(self, browser):
        assert len(browser.tables()) == 4

    def test_get_item_returns_the_p_at_the_given_index(self, browser):
        assert browser.tables()[0].id == 'axis_example'
        assert browser.tables()[1].id == 'outer'
        assert browser.tables()[2].id == 'inner'

    def test_iterates_through_tables_correctly(self, browser):
        count = 0
        for index, table in enumerate(browser.tables()):
            assert table.id == browser.table(index=index).id
            count += 1

        assert count > 0
