import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTableHeaders(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.theads(id='tax_headers')) == [browser.thead(id='tax_headers')]

    def test_returns_the_correct_number_of_theads(self, browser):
        assert len(browser.theads()) == 1

    def test_returns_the_correct_number_of_theads_within_table(self, browser):
        assert len(browser.table(index=0).theads()) == 1

    def test_get_item_returns_the_row_at_the_given_index(self, browser):
        assert browser.theads()[0].id == 'tax_headers'

    def test_get_item_returns_the_row_at_the_given_index_within_table(self, browser):
        assert browser.table(index=0).theads()[0].id == 'tax_headers'

    def test_iterates_through_theads_correctly(self, browser):
        count = 0

        for index, thead in enumerate(browser.theads()):
            assert thead.id == browser.thead(index=index).id
            count += 1

        assert count > 0

    def test_iterates_through_theads_correctly_within_table(self, browser):
        count = 0

        for index, thead in enumerate(browser.table(index=0).theads()):
            assert thead.id == browser.thead(index=index).id
            count += 1

        assert count > 0
