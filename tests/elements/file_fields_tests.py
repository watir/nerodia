import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestFileFields(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.file_fields(class_name='portrait').to_list == \
            [browser.file_field(class_name='portrait')]

    def test_returns_the_correct_number_of_file_fields(self, browser):
        assert len(browser.file_fields()) == 3

    def test_get_item_returns_the_file_field_at_the_given_index(self, browser):
        assert browser.file_fields()[0].id == 'new_user_portrait'

    def test_iterates_through_file_fields_correctly(self, browser):
        count = 0

        for index, file_field in enumerate(browser.file_fields()):
            assert file_field.name == browser.file_field(index=index).name
            assert file_field.id == browser.file_field(index=index).id
            assert file_field.value == browser.file_field(index=index).value
            count += 1

        assert count > 0
