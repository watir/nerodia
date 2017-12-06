import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestLis(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.lis(class_name='nonlink').to_list == \
            [browser.li(class_name='nonlink')]

    def test_returns_the_correct_number_of_lis(self, browser):
        assert len(browser.lis()) == 18

    def test_get_item_returns_the_li_at_the_given_index(self, browser):
        assert browser.lis()[4].id == 'non_link_1'

    def test_iterates_through_lis_correctly(self, browser):
        count = 0

        for index, li in enumerate(browser.lis()):
            assert li.id == browser.li(index=index).id
            assert li.value == browser.li(index=index).value
            count += 1

        assert count > 0
