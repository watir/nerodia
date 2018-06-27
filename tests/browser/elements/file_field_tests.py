import ntpath
from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestFileFieldExist(object):
    def test_returns_true_if_the_file_field_exists(self, browser):
        assert browser.file_field(id='new_user_portrait').exists
        assert browser.file_field(id=compile(r'new_user_portrait')).exists
        assert browser.file_field(name='new_user_portrait').exists
        assert browser.file_field(name=compile(r'new_user_portrait')).exists
        assert browser.file_field(class_name='portrait').exists
        assert browser.file_field(class_name=compile(r'portrait')).exists
        assert browser.file_field(xpath="//input[@id='new_user_portrait']").exists

    def test_returns_the_first_file_field_if_given_no_args(self, browser):
        assert browser.file_field().exists

    def test_returns_false_if_the_file_field_does_not_exist(self, browser):
        assert not browser.file_field(id='no_such_id').exists
        assert not browser.file_field(id=compile(r'no_such_id')).exists
        assert not browser.file_field(name='no_such_name').exists
        assert not browser.file_field(name=compile(r'no_such_name')).exists
        assert not browser.file_field(class_name='no_such_class').exists
        assert not browser.file_field(class_name=compile(r'no_such_class')).exists
        assert not browser.file_field(index=1337).exists
        assert not browser.file_field(xpath="//input[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.file_field(id=3.14).exists


class TestFileFieldAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_file_field_exists_and_has_class_name(self, browser):
        assert browser.file_field(index=0).class_name == 'portrait'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_the_file_field_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.file_field(index=1337).class_name

    # id
    def test_returns_the_id_if_the_file_field_exists_and_has_id(self, browser):
        assert browser.file_field(index=0).id == 'new_user_portrait'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_file_field_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.file_field(index=1337).id

    # name
    def test_returns_the_name_if_the_file_field_exists_and_has_name(self, browser):
        assert browser.file_field(index=0).name == 'new_user_portrait'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_the_file_field_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.file_field(index=1337).name

    # title
    def test_returns_the_title_if_the_file_field_exists_and_has_title(self, browser):
        assert browser.file_field(id='new_user_portrait').title == 'Smile!'

    # type
    def test_returns_the_type_if_the_file_field_exists(self, browser):
        assert browser.file_field(index=0).type == 'file'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_the_file_field_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.file_field(index=1337).type


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.file_field(index=0), 'class_name')
    assert hasattr(browser.file_field(index=0), 'id')
    assert hasattr(browser.file_field(index=0), 'name')
    assert hasattr(browser.file_field(index=0), 'title')
    assert hasattr(browser.file_field(index=0), 'type')
    assert hasattr(browser.file_field(index=0), 'value')


class TestFileFieldManipulation(object):
    # set
    def test_is_able_to_set_a_file_path_in_the_field_and_click_the_upload_button_and_fire_the_onchange_event(self, browser, messages, temp_file):
        path = temp_file.name
        element = browser.file_field(name='new_user_portrait')

        element.set(path)

        filename = ntpath.basename(path)
        assert filename in element.value  # only some browser will return the full path
        assert filename in messages.list[0]
        browser.button(name='new_user_submit').click()

    def test_raises_error_if_the_file_does_not_exist(self, browser):
        from errno import ENOENT
        path = 'unlikely-to_exist'
        with pytest.raises(OSError) as e:
            browser.file_field().set(path)
        assert e.value.args[0] == ENOENT
        assert e.value.args[1] == '{!r} does not exist.'.format(path)

    # value
    def test_is_able_to_set_a_file_path_in_the_field_via_value_attribute(self, browser, temp_file):
        path = temp_file.name
        element = browser.file_field(name='new_user_portrait')

        element.value = path

        assert ntpath.basename(path) in element.value  # only some browser will return the full path
