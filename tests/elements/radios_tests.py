import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestRadios(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.radios(value='yes').to_list == [browser.radio(value='yes')]

    def test_returns_the_correct_number_of_radios(self, browser):
        assert len(browser.radios()) == 7

    def test_get_item_returns_the_radio_at_the_given_index(self, browser):
        assert browser.radios()[0].id == 'new_user_newsletter_yes'

    def test_iterates_through_radios_correctly(self, browser):
        count = 0

        for index, radio in enumerate(browser.radios()):
            assert radio.name == browser.radio(index=index).name
            assert radio.id == browser.radio(index=index).id
            assert radio.value == browser.radio(index=index).value
            count += 1

        assert count > 0
