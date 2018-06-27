import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestPs(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.ps(class_name='lead')) == [browser.p(class_name='lead')]

    def test_returns_the_correct_number_of_ps(self, browser):
        assert len(browser.ps()) == 5

    def test_get_item_returns_the_p_at_the_given_index(self, browser):
        assert browser.ps()[0].id == 'lead'

    def test_iterates_through_ps_correctly(self, browser):
        count = 0

        for index, p in enumerate(browser.ps()):
            assert p.id == browser.p(index=index).id
            count += 1

        assert count > 0
