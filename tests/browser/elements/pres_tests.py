import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestPres(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.pres(class_name='c-plus-plus')) == [browser.pre(class_name='c-plus-plus')]

    def test_returns_the_correct_number_of_pres(self, browser):
        assert len(browser.pres()) == 7

    def test_get_item_returns_the_pre_at_the_given_index(self, browser):
        assert browser.pres()[1].id == 'rspec'

    def test_iterates_through_pres_correctly(self, browser):
        count = 0

        for index, pre in enumerate(browser.pres()):
            assert pre.id == browser.pre(index=index).id
            count += 1

        assert count > 0
