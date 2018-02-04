import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestTextFields(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.text_fields(name='new_user_email').to_list == [browser.text_field(name='new_user_email')]

    def test_returns_the_correct_number_of_text_fields(self, browser):
        assert len(browser.text_fields()) == 17

    def test_get_item_returns_the_text_field_at_the_given_index(self, browser):
        assert browser.text_fields()[0].id == 'new_user_first_name'
        assert browser.text_fields()[1].id == 'new_user_last_name'
        assert browser.text_fields()[2].id == 'new_user_email'

    def test_iterates_through_text_fields_correctly(self, browser):
        count = 0

        for index, text_field in enumerate(browser.text_fields()):
            assert text_field.name == browser.text_field(index=index).name
            assert text_field.id == browser.text_field(index=index).id
            assert text_field.value == browser.text_field(index=index).value
            count += 1

        assert count > 0
