import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestUls(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.uls(class_name='navigation').to_list == [browser.ul(class_name='navigation')]

    def test_returns_the_correct_number_of_uls(self, browser):
        assert len(browser.uls()) == 2

    def test_get_item_returns_the_ul_at_the_given_index(self, browser):
        assert browser.uls()[0].id == 'navbar'

    def test_iterates_through_uls_correctly(self, browser):
        count = 0

        for index, ul in enumerate(browser.uls()):
            assert ul.id == browser.ul(index=index).id
            count += 1

        assert count > 0
