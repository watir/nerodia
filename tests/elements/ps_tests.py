import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestOls(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.ols(class_name='chemistry').to_list == [browser.ol(class_name='chemistry')]

    def test_returns_the_correct_number_of_ols(self, browser):
        assert len(browser.ols()) == 2

    def test_get_item_returns_the_ol_at_the_given_index(self, browser):
        assert browser.ols()[0].id == 'favorite_compounds'

    def test_iterates_through_ols_correctly(self, browser):
        count = 0

        for index, ol in enumerate(browser.ols()):
            assert ol.id == browser.ol(index=index).id
            count += 1

        assert count > 0
