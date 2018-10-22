# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from nerodia.exception import UnknownObjectException, ObjectReadOnlyException, Error

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestUserEditableAppend(object):
    def test_appends_the_text_to_the_text_field(self, browser):
        browser.text_field(name='new_user_occupation').append(' Append This')
        assert browser.text_field(name='new_user_occupation').value == 'Developer Append This'

    def test_appends_multi_byte_characters(self, browser):
        browser.text_field(name='new_user_occupation').append(' ĳĳ')
        assert browser.text_field(name='new_user_occupation').value == 'Developer ĳĳ'

    def test_raises_notimplementederror_if_the_object_is_content_editable_element(self, browser):
        with pytest.raises(NotImplementedError) as e:
            browser.div(id='contenteditable').append('bar')
        assert e.value.args[0] == '#append method is not supported with contenteditable element'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_append_if_the_object_is_readonly(self, browser):
        with pytest.raises(ObjectReadOnlyException):
            browser.text_field(id='new_user_code').append('Append This')

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_append_if_the_object_is_disabled(self, browser):
        from nerodia.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            browser.text_field(name='new_user_species').append('Append This')

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_append_if_the_object_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(name='no_such_name').append('Append This')


class TestUserEditableClear(object):
    def test_removes_all_text_from_the_text_field(self, browser):
        browser.text_field(name='new_user_occupation').clear()
        assert browser.text_field(name='new_user_occupation').value == ''
        browser.textarea(id='delete_user_comment').clear()
        assert browser.textarea(id='delete_user_comment').value == ''

    def test_removes_all_text_from_the_content_editable_element(self, browser):
        el = browser.div(id='contenteditable')
        el.clear()
        assert el.text == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_clear_if_the_object_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(id='no_such_id').clear()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_clear_if_the_object_is_readonly(self, browser):
        with pytest.raises(ObjectReadOnlyException):
            browser.text_field(id='new_user_code').clear()


class TestUserEditableValue(object):
    def test_sets_the_value_of_the_element(self, browser):
        browser.text_field(id='new_user_email').value = 'Hello Cruel World'
        assert browser.text_field(id='new_user_email').value == 'Hello Cruel World'

    def test_is_able_to_set_multi_byte_characters(self, browser):
        browser.text_field(name='new_user_occupation').value = 'ĳĳ'
        assert browser.text_field(name='new_user_occupation').value == 'ĳĳ'

    def test_sets_the_value_of_a_textarea_element(self, browser):
        browser.textarea(id='delete_user_comment').value = 'Hello Cruel World'
        assert browser.textarea(id='delete_user_comment').value == 'Hello Cruel World'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_clear_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(name='no_such_name').clear()


class TestUserEditableSet(object):
    def test_sets_the_value_of_the_element(self, browser):
        browser.text_field(id='new_user_email').set('Hello Cruel World')
        assert browser.text_field(id='new_user_email').value == 'Hello Cruel World'

    def test_sets_the_value_of_a_textarea_element(self, browser):
        browser.textarea(id='delete_user_comment').set('Hello Cruel World')
        assert browser.textarea(id='delete_user_comment').value == 'Hello Cruel World'

    def test_sets_the_value_of_a_content_editable_element(self, browser):
        el = browser.div(id='contenteditable')
        el.set('Bar')
        assert el.text == 'Bar'

    def test_fires_events(self, browser):
        browser.text_field(id='new_user_username').set('Hello World')
        assert browser.span(id='current_length').text == '11'

    def test_sets_the_value_of_a_password_field(self, browser):
        browser.text_field(name='new_user_password').set('secret')
        assert browser.text_field(name='new_user_password').value == 'secret'

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        browser.form(id='new_user').text_field(name='new_user_password').set('secret')
        assert browser.form(id='new_user').text_field(name='new_user_password').value == 'secret'

    def test_is_able_to_set_multi_byte_characters(self, browser):
        browser.text_field(name='new_user_occupation').set('ĳĳ')
        assert browser.text_field(name='new_user_occupation').value == 'ĳĳ'

    def test_sets_the_value_to_a_concatenation_of_multiple_arguments(self, browser):
        browser.text_field(id='new_user_email').set('Bye', 'Cruel', 'World')
        assert browser.text_field(id='new_user_email').value == 'ByeCruelWorld'

    def test_sets_the_value_to_blank_when_no_arguments_are_provided(self, browser):
        browser.text_field(id='new_user_email').set()
        assert browser.text_field(id='new_user_email').value == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_set_if_the_object_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(id='no_such_id').set('secret')


class TestUserEditableJsSet(object):
    def test_sets_the_value_of_the_element(self, browser):
        browser.text_field(id='new_user_email').js_set('Bye Cruel World')
        assert browser.text_field(id='new_user_email').value == 'Bye Cruel World'

    def test_sets_the_value_of_a_textarea_element(self, browser):
        browser.textarea(id='delete_user_comment').js_set('Hello Cruel World')
        assert browser.textarea(id='delete_user_comment').value == 'Hello Cruel World'

    def test_sets_the_value_of_a_content_editable_element(self, browser):
        el = browser.div(id='contenteditable')
        el.js_set('foo')
        assert el.text == 'foo'

    def test_fires_events(self, browser):
        browser.text_field(id='new_user_username').js_set('Hello World')
        assert browser.span(id='current_length').text == '11'

    def test_sets_the_value_of_a_password_field(self, browser):
        browser.text_field(name='new_user_password').js_set('secret')
        assert browser.text_field(name='new_user_password').value == 'secret'

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        browser.form(id='new_user').text_field(name='new_user_password').js_set('secret')
        assert browser.form(id='new_user').text_field(name='new_user_password').value == 'secret'

    def test_is_able_to_set_multi_byte_characters(self, browser):
        browser.text_field(name='new_user_occupation').js_set('ĳĳ')
        assert browser.text_field(name='new_user_occupation').value == 'ĳĳ'

    def test_sets_the_value_to_a_concatenation_of_multiple_arguments(self, browser):
        browser.text_field(id='new_user_email').js_set('Bye', 'Cruel', 'World')
        assert browser.text_field(id='new_user_email').value == 'ByeCruelWorld'

    def test_sets_the_value_to_blank_when_no_arguments_are_provided(self, browser):
        browser.text_field(id='new_user_email').js_set()
        assert browser.text_field(id='new_user_email').value == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_set_if_the_object_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(id='no_such_id').js_set('secret')

    def test_raises_exception_if_the_value_of_text_field_doesnt_match(self, browser, mocker):
        mock = mocker.patch('nerodia.user_editable.UserEditable.value',
                            new_callable=mocker.PropertyMock)
        mock.return_value = 'wrong'
        el = browser.text_field(id='new_user_password')
        with pytest.raises(Error) as e:
            el.js_set('secret')
        assert e.value.args[0] == "#js_set value: 'wrong' does not match expected input: 'secret'"

    def test_raises_exception_if_the_text_of_content_editable_doesnt_match(self, browser, mocker):
        mock = mocker.patch('nerodia.elements.element.Element.text',
                            new_callable=mocker.PropertyMock)
        mock.return_value = 'wrong'
        el = browser.div(id='contenteditable')
        with pytest.raises(Error) as e:
            el.js_set('secret')
        assert e.value.args[0] == "#js_set text: 'wrong' does not match expected input: 'secret'"
