import datetime
import time
from re import compile

import pytest
from dateutil import parser

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')

now = datetime.datetime.now()
expected = now.replace(second=0, microsecond=0)


class TestDateTimeFieldExist(object):
    def test_returns_true_if_the_date_time_field_exists(self, browser):
        assert browser.date_time_field(id='html5_datetime-local').exists is True
        assert browser.date_time_field(id=compile(r'html5_datetime-local')).exists is True
        assert browser.date_time_field(name='html5_datetime-local').exists is True
        assert browser.date_time_field(name=compile(r'html5_datetime-local')).exists is True
        assert browser.date_time_field(text='').exists is True
        assert browser.date_time_field(index=0).exists is True
        assert browser.date_time_field(xpath="//input[@id='html5_datetime-local']").exists is True
        assert browser.date_time_field(label='HTML5 Datetime Local').exists is True
        assert browser.date_time_field(label=compile(r'Local')).exists is True

    def test_returns_the_first_date_time_field_if_given_no_args(self, browser):
        assert browser.date_time_field().exists

    def test_respects_date_time_field_types(self, browser):
        assert browser.date_time_field().type == 'datetime-local'

    def test_returns_false_if_the_date_time_field_doesnt_exist(self, browser):
        assert browser.date_time_field(id='no_such_id').exists is False
        assert browser.date_time_field(id=compile(r'no_such_id')).exists is False
        assert browser.date_time_field(name='no_such_name').exists is False
        assert browser.date_time_field(name=compile(r'no_such_name')).exists is False
        assert browser.date_time_field(text='no_such_text').exists is False
        assert browser.date_time_field(text=compile(r'no_such_text')).exists is False
        assert browser.date_time_field(class_name='no_such_class').exists is False
        assert browser.date_time_field(class_name=compile(r'no_such_class')).exists is False
        assert browser.date_time_field(index=1337).exists is False
        assert browser.date_time_field(xpath="//input[@id='no_such_id']").exists is False
        assert browser.date_time_field(label='bad label').exists is False
        assert browser.date_time_field(label=compile(r'bad label')).exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.date_time_field(id=3.14).exists


class TestDateTimeFieldAttributes(object):
    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.date_time_field(name='html5_datetime-local').id == 'html5_datetime-local'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(index=1337).id

    # name

    def test_returns_the_name_attribute_if_element_exists(self, browser):
        assert browser.date_time_field(id='html5_datetime-local').name == 'html5_datetime-local'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(index=1337).name

    # type

    def test_returns_the_type_attribute_if_element_exists(self, browser):
        assert browser.date_time_field(id='html5_datetime-local').type == 'datetime-local'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(index=1337).type

    # value

    def test_returns_the_value_attribute_if_element_exists(self, browser):
        assert browser.date_time_field(id='html5_datetime-local').value == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(index=1337).value


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.date_time_field(), 'class_name')
    assert hasattr(browser.date_time_field(), 'id')
    assert hasattr(browser.date_time_field(), 'name')
    assert hasattr(browser.date_time_field(), 'title')
    assert hasattr(browser.date_time_field(), 'type')
    assert hasattr(browser.date_time_field(), 'value')


class TestDateTimeFieldAccessMethods(object):
    # enabled

    def test_returns_true_for_enabled_date_time_fields(self, browser):
        assert browser.date_time_field(id='html5_datetime-local').enabled is True

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(index=1337).enabled


class TestDateTimeFieldManipulationValue(object):
    # value =

    def test_sets_the_value_of_the_element(self, browser):
        date_time = browser.date_time_field(id='html5_datetime-local')
        date_time.value = now

        assert parser.parse(date_time.value) == expected

    def test_sets_the_value_of_the_element_when_given_time(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        value = datetime.time(hour=now.hour, minute=now.minute)
        date_time_field.value = value

        assert parser.parse(date_time_field.value) == expected

    def test_sets_the_value_of_the_element_when_given_float(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        flt = time.time()
        date_time_field.value = flt
        expect = datetime.datetime.fromtimestamp(flt).replace(second=0, microsecond=0)

        assert parser.parse(date_time_field.value) == expect

    def test_sets_the_value_of_the_element_when_given_int(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        flt = int(time.time())
        date_time_field.value = flt
        expect = datetime.datetime.fromtimestamp(flt).replace(second=0, microsecond=0)

        assert parser.parse(date_time_field.value) == expect

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        date_time_field = browser.form(id='new_user').date_time_field(id='html5_datetime-local')
        date_time_field.value = now

        assert parser.parse(date_time_field.value) == expected

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(id='no_such_id').value = now

    def test_raises_correct_exception_for_value_if_using_non_date_time_parameter(self, browser):
        with pytest.raises(TypeError):
            browser.date_time_field(id='no_such_id').value = {}


class TestDateTimeFieldManipulationJsSet(object):
    # js_set

    def test_sets_the_value_of_the_element(self, browser):
        date_time = browser.date_time_field(id='html5_datetime-local')
        date_time.js_set(now)

        assert parser.parse(date_time.value) == expected

    def test_sets_the_value_of_the_element_when_given_time(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        value = datetime.time(hour=now.hour, minute=now.minute)
        date_time_field.js_set(value)

        assert parser.parse(date_time_field.value) == expected

    def test_sets_the_value_of_the_element_when_given_float(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        flt = time.time()
        date_time_field.js_set(flt)
        expect = datetime.datetime.fromtimestamp(flt).replace(second=0, microsecond=0)

        assert parser.parse(date_time_field.value) == expect

    def test_sets_the_value_of_the_element_when_given_int(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        flt = int(time.time())
        date_time_field.js_set(flt)
        expect = datetime.datetime.fromtimestamp(flt).replace(second=0, microsecond=0)

        assert parser.parse(date_time_field.value) == expect

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        date_time_field = browser.form(id='new_user').date_time_field(id='html5_datetime-local')
        date_time_field.js_set(now)

        assert parser.parse(date_time_field.value) == expected

    def test_raises_correct_exception_for_js_set_when_no_args_are_provided(self, browser):
        with pytest.raises(TypeError):
            browser.date_time_field(id='html5_datetime-local').js_set()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_js_set_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(id='no_such_id').js_set(now)


class TestDateTimeFieldManipulationSet(object):
    # set

    def test_sets_the_value_of_the_element(self, browser):
        date_time = browser.date_time_field(id='html5_datetime-local')
        date_time.set(now)

        assert parser.parse(date_time.value) == expected

    def test_sets_the_value_of_the_element_when_given_time(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        value = datetime.time(hour=now.hour, minute=now.minute)
        date_time_field.set(value)

        assert parser.parse(date_time_field.value) == expected

    def test_sets_the_value_of_the_element_when_given_float(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        flt = time.time()
        date_time_field.set(flt)
        expect = datetime.datetime.fromtimestamp(flt).replace(second=0, microsecond=0)

        assert parser.parse(date_time_field.value) == expect

    def test_sets_the_value_of_the_element_when_given_int(self, browser):
        date_time_field = browser.date_time_field(id='html5_datetime-local')
        flt = int(time.time())
        date_time_field.set(flt)
        expect = datetime.datetime.fromtimestamp(flt).replace(second=0, microsecond=0)

        assert parser.parse(date_time_field.value) == expect

    def test_sets_the_value_when_accessed_through_the_enclosing_form(self, browser):
        date_time_field = browser.form(id='new_user').date_time_field(id='html5_datetime-local')
        date_time_field.set(now)

        assert parser.parse(date_time_field.value) == expected

    def test_raises_correct_exception_for_set_when_no_args_are_provided(self, browser):
        with pytest.raises(TypeError):
            browser.date_time_field(id='html5_datetime-local').set()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_set_if_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.date_time_field(id='no_such_id').set(now)
