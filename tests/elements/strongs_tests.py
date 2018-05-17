import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestStrongs(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.strongs(class_name='descartes')) == [browser.strong(class_name='descartes')]

    def test_returns_the_correct_number_of_strongs(self, browser):
        assert len(browser.strongs()) == 2

    def test_get_item_returns_the_strong_at_the_given_index(self, browser):
        assert browser.strongs()[0].id == 'descartes'

    def test_iterates_through_strongs_correctly(self, browser):
        count = 0

        for index, strong in enumerate(browser.strongs()):
            assert strong.id == browser.strong(index=index).id
            assert strong.class_name == browser.strong(index=index).class_name
            count += 1

        assert count > 0
