from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestLabelExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.label(id='first_label').exists is True
        assert browser.label(id=compile(r'first_label')).exists is True
        assert browser.label('for', 'new_user_first_name').exists is True
        assert browser.label(**{'for': 'new_user_first_name'}).exists is True
        assert browser.label(**{'for': compile(r'new_user_first_name')}).exists is True
        assert browser.label(text='First name').exists is True
        assert browser.label(text=compile(r'First name')).exists is True
        assert browser.label(index=0).exists is True
        assert browser.label(xpath="//label[@id='first_label']").exists is True

    def test_returns_the_first_label_if_given_no_args(self, browser):
        assert browser.label().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.label(id='no_such_id').exists is False
        assert browser.label(id=compile(r'no_such_id')).exists is False
        assert browser.label(text='no_such_text').exists is False
        assert browser.label(text=compile(r'no_such_text')).exists is False
        assert browser.label(index=1337).exists is False
        assert browser.label(xpath="//label[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.label(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.label(no_such_how='some_value').exists


def test_fires_the_onclick_event(browser, messages):
    browser.label(id='first_label').click()
    assert messages[0] == 'label'


class TestLabelAttributes(object):
    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.label(index=0).id == 'first_label'

    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.label(index=1337).id

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.label(index=1).text == 'This is an labelerted text tag 2'

    def test_returns_an_empty_string_if_the_label_exists_and_the_text_doesnt(self, browser):
        assert browser.label(index=3).text == ''

    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.label(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.label(index=0), 'id')
