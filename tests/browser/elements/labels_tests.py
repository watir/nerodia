import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestLabels(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.labels('for', 'new_user_first_name')) == \
            [browser.label('for', 'new_user_first_name')]

    def test_returns_the_correct_number_of_labels(self, browser):
        assert len(browser.labels()) == 41

    def test_get_item_returns_the_label_at_the_given_index(self, browser):
        assert browser.labels()[0].id == 'first_label'

    def test_iterates_through_labels_correctly(self, browser):
        count = 0

        for index, label in enumerate(browser.labels()):
            assert label.id == browser.label(index=index).id
            count += 1

        assert count > 0
