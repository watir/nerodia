import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestInses(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.inses(class_name='lead').to_list == [browser.ins(class_name='lead')]

    def test_returns_the_correct_number_of_inses(self, browser):
        assert len(browser.inses()) == 5

    def test_get_item_returns_the_image_at_the_given_index(self, browser):
        assert browser.inses()[0].id == 'lead'

    def test_iterates_through_inses_correctly(self, browser):
        count = 0

        for index, ins in enumerate(browser.inses()):
            assert ins.id == browser.ins(index=index).id
            count += 1

        assert count > 0
