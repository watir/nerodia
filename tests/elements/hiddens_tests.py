import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestHiddens(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.hiddens(value='dolls').to_list == [browser.hidden(value='dolls')]

    def test_returns_the_correct_number_of_hiddens(self, browser):
        assert len(browser.hiddens()) == 2

    def test_get_item_returns_the_hidden_at_the_given_index(self, browser):
        assert browser.hiddens()[1].id == 'new_user_interests_dolls'

    def test_iterates_through_hiddens_correctly(self, browser):
        count = 0

        for index, hidden in enumerate(browser.hiddens()):
            assert hidden.name == browser.hidden(index=index).name
            assert hidden.id == browser.hidden(index=index).id
            assert hidden.value == browser.hidden(index=index).value
            count += 1

        assert count > 0
