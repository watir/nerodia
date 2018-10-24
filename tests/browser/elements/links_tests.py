from re import compile

import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestLinks(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.links(title='link_title_2')) == [browser.link(title='link_title_2')]

    def test_returns_the_correct_number_of_links(self, browser):
        assert len(browser.links()) == 7

    def test_get_item_returns_the_link_at_the_given_index(self, browser):
        assert browser.links()[2].id == 'link_3'

    def test_get_item_returns_the_link_also_when_the_index_is_out_of_bounds(self, browser):
        assert browser.links()[2000] is not None

    def test_iterates_through_links_correctly(self, browser):
        count = 0

        for index, link in enumerate(browser.links()):
            assert link.id == browser.link(index=index).id
            count += 1

        assert count > 0


class TestLinksVisibleText(object):
    def test_finds_links_by_visible_text(self, browser):
        container = browser.div(id='visible_text')
        assert len(container.links(visible_text='all visible')) == 1
        assert len(container.links(visible_text=compile(r'all visible'))) == 1
        assert len(container.links(visible_text='some visible')) == 1
        assert len(container.links(visible_text=compile(r'some visible'))) == 1
        assert len(container.links(visible_text='none visible')) == 0
        assert len(container.links(visible_text=compile(r'none visible'))) == 0
