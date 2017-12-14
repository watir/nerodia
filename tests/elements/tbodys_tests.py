import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTbodys(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.tbodys(id='first').to_list == [browser.tbody(id='first')]

    def test_returns_the_correct_number_of_tbodys(self, browser):
        assert len(browser.tbodys()) == 5

    def test_get_item_returns_the_tbody_at_the_given_index(self, browser):
        assert browser.tbodys()[0].id == 'first'

    def test_get_item_returns_the_tbody_at_the_given_index_in_table(self, browser):
        assert browser.table(index=0).tbodys()[0].id == 'first'

    def test_iterates_through_tbodys_correctly(self, browser):
        count = 0

        for index, tbody in enumerate(browser.tbodys()):
            assert tbody.id == browser.tbody(index=index).id
            count += 1

        assert count > 0

    def test_iterates_through_tbodys_correctly_in_table(self, browser):
        count = 0

        for index, tbody in enumerate(browser.table(index=0).tbodys()):
            assert tbody.id == browser.table().tbody(index=index).id
            count += 1

        assert count > 0
