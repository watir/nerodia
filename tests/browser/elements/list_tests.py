import pytest

from nerodia.elements.html_elements import LI, LICollection

pytestmark = pytest.mark.page('non_control_elements.html')


class TestList(object):
    def test_returns_the_list_items_associated_with_an_ol(self, browser):
        items = browser.ol(id='favorite_compounds').list_items
        assert isinstance(items, LICollection)
        assert all(isinstance(item, LI) for item in items)

    def test_returns_the_list_items_associated_with_a_ul(self, browser):
        items = browser.ul(id='navbar').list_items
        assert isinstance(items, LICollection)
        assert all(isinstance(item, LI) for item in items)

    def test_gets_the_length_of_the_list(self, browser):
        ul = browser.ul(id='navbar')
        assert len(ul) == 7

    def test_iterates_over_a_list(self, browser):
        ul = browser.ul(id='navbar')
        assert [x.tag_name for x in ul] == ['li'] * 7

    def test_gets_a_list_item_at_the_specified_index(self, browser):
        ul = browser.ul(id='navbar')
        assert ul[4].text == 'Non-link 1'

    def test_returns_the_list_item_length(self, browser):
        assert len(browser.ol(id='favorite_compounds').list_items) == 5

    def test_returns_list_item_at_an_index(self, browser):
        items = browser.ol(id='favorite_compounds').list_items
        third = browser.ol(id='favorite_compounds').li(index=2)

        assert items[2] == third
