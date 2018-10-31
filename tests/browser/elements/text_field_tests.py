# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from re import compile, IGNORECASE

import pytest

from nerodia.exception import UnknownObjectException, ObjectReadOnlyException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestTextFieldExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.text_field(id='new_user_email').exists is True
        assert browser.text_field(id=compile(r'new_user_email')).exists is True
        assert browser.text_field(name='new_user_email').exists is True
        assert browser.text_field(name=compile(r'new_user_email')).exists is True
        assert browser.text_field(name=compile(r'new_user_occupation', flags=IGNORECASE)).exists is True
        assert browser.text_field(value='Developer').exists is True
        assert browser.text_field(value=compile(r'Developer')).exists is True
        assert browser.text_field(class_name='name').exists is True
        assert browser.text_field(class_name=compile(r'name')).exists is True
        assert browser.text_field(index=0).exists is True
        assert browser.text_field(xpath="//input[@id='new_user_email']").exists is True
        assert browser.text_field(label='First name').exists is True
        assert browser.text_field(label=compile(r'(Last|First) name')).exists is True
        assert browser.text_field(label='Without for').exists is True
        assert browser.text_field(label=compile(r'Without for')).exists is True
        assert browser.text_field(label='With hidden text').exists is True
        assert browser.text_field(visible_label='With text').exists is True

        # This will work after text is deprecated for visible_text
        # assert browser.text_field(label=compile(r'With hidden text')).exists is True

        assert browser.text_field(visible_label=compile(r'With text')).exists is True

    def test_locates_value_of_text_field_using_text_locator(self, browser):
        assert browser.text_field(text='Developer').exists is True
        assert browser.text_field(text=compile(r'Developer')).exists is True

    def test_returns_the_first_text_field_if_given_no_args(self, browser):
        assert browser.text_field().exists

    def test_respects_text_fields_types(self, browser):
        assert browser.text_field().type == 'text'

    def test_returns_true_if_the_element_exists_no_type_attribute(self, browser):
        assert browser.text_field(id='new_user_first_name').exists is True

    def test_returns_true_if_the_element_exists_invalid_type_attribute(self, browser):
        assert browser.text_field(id='new_user_last_name').exists is True

    def test_returns_true_for_element_with_upper_case_type(self, browser):
        assert browser.text_field(id='new_user_email_confirm').exists is True

    def test_returns_true_for_element_with_unknown_type(self, browser):
        assert browser.text_field(id='unknown_text_field').exists is True

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.text_field(id='no_such_id').exists is False
        assert browser.text_field(id=compile(r'no_such_id')).exists is False
        assert browser.text_field(name='no_such_name').exists is False
        assert browser.text_field(name=compile(r'no_such_name')).exists is False
        assert browser.text_field(value='no_such_value').exists is False
        assert browser.text_field(value=compile(r'no_such_value')).exists is False
        assert browser.text_field(text='no_such_text').exists is False
        assert browser.text_field(text=compile(r'no_such_text')).exists is False
        assert browser.text_field(class_name='no_such_class').exists is False
        assert browser.text_field(class_name=compile(r'no_such_class')).exists is False
        assert browser.text_field(index=1337).exists is False
        assert browser.text_field(xpath="//input[@id='no_such_id']").exists is False
        assert browser.text_field(label='bad_label').exists is False
        assert browser.text_field(label=compile(r'bad_label')).exists is False
        assert browser.text_field(label='With text').exists is False
        assert browser.text_field(visible_label='With hidden text').exists is False

        # This will work after text is deprecated for visible_text
        # assert browser.text_field(label=compile(r'With text')).exists is False

        assert browser.text_field(visible_label=compile(r'With hidden text')).exists is False

        # input type='hidden' should not be found by #text_field
        assert browser.text_field(id='new_user_interests_dolls').exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.text_field(id=3.14).exists


class TestTextFieldAttributes(object):
    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.text_field(index=4).id == 'new_user_occupation'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).id

    # name
    def test_returns_the_name_if_the_element_exists_and_has_name(self, browser):
        assert browser.text_field(index=3).name == 'new_user_email_confirm'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).name

    # title
    def test_returns_the_title_if_the_element_exists_and_has_title(self, browser):
        assert browser.text_field(id='new_user_code').title == 'Your personal code'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).title

    # type
    def test_returns_the_type_if_the_element_exists_and_has_type(self, browser):
        assert browser.text_field(index=3).type == 'text'

    def returns_text_if_the_type_attribute_is_invalid(self, browser):
        assert browser.text_field(id='new_user_last_name').type == 'text'

    def returns_text_if_the_type_attribute_does_not_exist(self, browser):
        assert browser.text_field(id='new_user_first_name').type == 'text'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).type

    # value
    def test_returns_the_value_if_the_element_exists_and_has_value(self, browser):
        assert browser.text_field(name='new_user_occupation').value == 'Developer'
        assert browser.text_field(index=4).value == 'Developer'
        assert browser.text_field(name=compile(r'new_user_occupation',
                                               flags=IGNORECASE)).value == 'Developer'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).value


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.text_field(index=0), 'class_name')
    assert hasattr(browser.text_field(index=0), 'id')
    assert hasattr(browser.text_field(index=0), 'name')
    assert hasattr(browser.text_field(index=0), 'title')
    assert hasattr(browser.text_field(index=0), 'type')
    assert hasattr(browser.text_field(index=0), 'value')


class TestTextFieldAccessMethods(object):
    # enabled

    def test_returns_true_for_enabled_text_fields(self, browser):
        assert browser.text_field(name='new_user_occupation').enabled is True
        assert browser.text_field(id='new_user_email').enabled is True

    def test_returns_false_for_disabled_text_fields(self, browser):
        assert browser.text_field(name='new_user_species').enabled is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).enabled

    # disabled

    def test_returns_true_for_disabled_text_fields(self, browser):
        assert browser.text_field(name='new_user_species').disabled is True

    def test_returns_false_for_enabled_text_fields(self, browser):
        assert browser.text_field(index=0).disabled is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_disabled_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).disabled

    # readonly

    def test_returns_true_for_readonly(self, browser):
        assert browser.text_field(name='new_user_code').readonly is True
        assert browser.text_field(id='new_user_code').readonly is True

    def test_returns_false_for_writable_text_fields(self, browser):
        assert browser.text_field(name='new_user_email').readonly is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_readonly_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=1337).readonly

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_sending_keys_to_readonly_element(self, browser):
        with pytest.raises(ObjectReadOnlyException):
            browser.text_field(id='new_user_code').set('foo')
