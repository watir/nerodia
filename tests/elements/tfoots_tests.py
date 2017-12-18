import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTableFooters(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.tfoots(id='tax_totals').to_list == [browser.tfoot(id='tax_totals')]

    def test_returns_the_correct_number_of_tfoots(self, browser):
        assert len(browser.tfoots()) == 1

    def test_returns_the_correct_number_of_tfoots_within_table(self, browser):
        assert len(browser.table(index=0).tfoots()) == 1

    def test_get_item_returns_the_row_at_the_given_index(self, browser):
        assert browser.tfoots()[0].id == 'tax_totals'

    def test_get_item_returns_the_row_at_the_given_index_within_table(self, browser):
        assert browser.table(index=0).tfoots()[0].id == 'tax_totals'

    def test_iterates_through_tfoots_correctly(self, browser):
        count = 0

        for index, tfoot in enumerate(browser.tfoots()):
            assert tfoot.id == browser.tfoot(index=index).id
            assert tfoot.class_name == browser.tfoot(index=index).class_name
            count += 1

        assert count > 0

    def test_iterates_through_tfoots_correctly_within_table(self, browser):
        count = 0

        for index, tfoot in enumerate(browser.table(index=0).tfoots()):
            assert tfoot.id == browser.tfoot(index=index).id
            assert tfoot.class_name == browser.tfoot(index=index).class_name
            count += 1

        assert count > 0
