import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTds(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.tds(headers='before_tax').to_list == [browser.td(headers='before_tax')]

    def test_iterates_through_all_cells_on_the_page_correctly(self, browser):
        count = 0

        for index, td in enumerate(browser.tds()):
            assert td.id == browser.td(index=index).id
            count += 1

        assert count > 0

    def test_iterates_through_cells_inside_a_table(self, browser):
        count = 0

        inner_table = browser.table(id='inner')
        for index, td in enumerate(inner_table.tds()):
            assert td.id == inner_table.td(index=index).id
            count += 1

        assert count > 0
