import pytest

pytestmark = pytest.mark.page('images.html')


class TestPres(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.pres(name='triangle_pre').to_list == [browser.pre(name='triangle_pre')]

    def test_returns_the_correct_number_of_pres(self, browser):
        assert len(browser.pres()) == 2

    def test_get_item_returns_the_pre_at_the_given_index(self, browser):
        assert browser.pres()[0].id == 'triangle_pre'

    def test_iterates_through_pres_correctly(self, browser):
        count = 0

        for index, pre in enumerate(browser.pres()):
            assert pre.name == browser.pre(index=index).name
            assert pre.id == browser.pre(index=index).id
            count += 1

        assert count > 0
