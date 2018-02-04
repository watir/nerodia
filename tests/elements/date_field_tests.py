import datetime
from re import compile

import pytest
from dateutil import parser

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')

today = datetime.date.today()


class TestDateFieldExist(object):
    def test_returns_true_if_the_date_field_exists(self, browser):
        assert browser.date_field(id='html5_date').exists is True
        assert browser.date_field(id=compile(r'html5_date')).exists is True
        assert browser.date_field(name='html5_date').exists is True
        assert browser.date_field(name=compile(r'html5_date')).exists is True
        assert browser.date_field(text='').exists is True
        assert browser.date_field(index=0).exists is True
        assert browser.date_field(xpath="//input[@id='html5_date']").exists is True
        assert browser.date_field(label='HTML5 Date').exists is True
        assert browser.date_field(label=compile(r'Date$')).exists is True

    def test_returns_the_first_date_field_if_given_no_args(self, browser):
        assert browser.date_field().exists

    def test_respects_date_field_types(self, browser):
        assert browser.date_field().type == 'date'

    def test_returns_false_if_the_date_field_doesnt_exist(self, browser):
        assert browser.date_field(id='no_such_id').exists is False
        assert browser.date_field(id=compile(r'no_such_id')).exists is False
        assert browser.date_field(name='no_such_name').exists is False
        assert browser.date_field(name=compile(r'no_such_name')).exists is False
        assert browser.date_field(text='no_such_text').exists is False
        assert browser.date_field(text=compile(r'no_such_text')).exists is False
        assert browser.date_field(class_name='no_such_class').exists is False
        assert browser.date_field(class_name=compile(r'no_such_class')).exists is False
        assert browser.date_field(index=1337).exists is False
        assert browser.date_field(xpath="//input[@id='no_such_id']").exists is False
        assert browser.date_field(label='bad label').exists is False
        assert browser.date_field(label=compile(r'bad label')).exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.date_field(id=3.14).exists


class TestDateFieldAttributes(object):
    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.date_field(name='html5_date').id == 'html5_date'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(index=1337).id

    # name

    def test_returns_the_name_attribute_if_element_exists(self, browser):
        assert browser.date_field(id='html5_date').name == 'html5_date'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(index=1337).name

    # type

    def test_returns_the_type_attribute_if_element_exists(self, browser):
        assert browser.date_field(id='html5_date').type == 'date'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(index=1337).type

    # value

    def test_returns_the_value_attribute_if_element_exists(self, browser):
        assert browser.date_field(id='html5_date').value == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(index=1337).value


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.date_field(), 'class_name')
    assert hasattr(browser.date_field(), 'id')
    assert hasattr(browser.date_field(), 'name')
    assert hasattr(browser.date_field(), 'title')
    assert hasattr(browser.date_field(), 'type')
    assert hasattr(browser.date_field(), 'value')


class TestDateFieldAccessMethods(object):
    # enabled

    def test_returns_true_for_enabled_date_fields(self, browser):
        assert browser.date_field(id='html5_date').enabled is True

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(index=1337).enabled


class TestDateFieldManipulationValue(object):
    # value =

    def test_sets_the_value_of_the_element(self, browser):
        date = browser.date_field(id='html5_date')
        date.value = today

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_of_the_element_when_given_datetime(self, browser):
        date = browser.date_field(id='html5_date')
        value = datetime.datetime.now()
        date.value = value

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_of_the_element_when_given_string(self, browser):
        date = browser.date_field(id='html5_date')
        value = today.strftime('%Y-%m-%d')
        date.value = value

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        date_field = browser.form(id='new_user').date_field(id='html5_date')
        date_field.value = today

        assert parser.parse(date_field.value).date() == today

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(id='no_such_id').value = today

    def test_raises_correct_exception_for_value_if_using_non_date_parameter(self, browser):
        with pytest.raises(TypeError):
            browser.date_field(id='no_such_id').value = 5


class TestDateFieldManipulationJsSet(object):
    # js_set

    def test_sets_the_value_of_the_element(self, browser):
        date = browser.date_field(id='html5_date')
        date.js_set(today)

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_of_the_element_when_given_datetime(self, browser):
        date = browser.date_field(id='html5_date')
        value = datetime.datetime.now()
        date.js_set(value)

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_of_the_element_when_given_string(self, browser):
        date = browser.date_field(id='html5_date')
        value = today.strftime('%Y-%m-%d')
        date.js_set(value)

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        date_field = browser.form(id='new_user').date_field(id='html5_date')
        date_field.js_set(today)

        assert parser.parse(date_field.value).date() == today

    def test_raises_correct_exception_for_js_set_when_no_args_are_provided(self, browser):
        with pytest.raises(TypeError):
            browser.date_field(id='html5_date').js_set()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_js_set_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(id='no_such_id').js_set(today)


class TestDateFieldManipulationSet(object):
    # set

    def test_sets_the_value_of_the_element(self, browser):
        date = browser.date_field(id='html5_date')
        date.set(today)

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_of_the_element_when_given_datetime(self, browser):
        date = browser.date_field(id='html5_date')
        value = datetime.datetime.now()
        date.set(value)

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_of_the_element_when_given_string(self, browser):
        date = browser.date_field(id='html5_date')
        value = today.strftime('%Y-%m-%d')
        date.set(value)

        assert parser.parse(date.value).date() == today

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        date_field = browser.form(id='new_user').date_field(id='html5_date')
        date_field.set(today)

        assert parser.parse(date_field.value).date() == today

    def test_raises_correct_exception_for_set_when_no_args_are_provided(self, browser):
        with pytest.raises(TypeError):
            browser.date_field(id='html5_date').set()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_set_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_field(id='no_such_id').set(today)
