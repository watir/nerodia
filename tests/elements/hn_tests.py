from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestHnExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.h1(id='header1').exists is True
        assert browser.h2(id=compile(r'header2')).exists is True
        assert browser.h3(text='Header 3').exists is True
        assert browser.h4(text=compile(r'Header 4')).exists is True
        assert browser.h5(index=0).exists is True
        assert browser.h6(index=0).exists is True
        assert browser.h1(xpath="//h1[@id='first_header']").exists is True

    def test_returns_the_first_h1_if_given_no_args(self, browser):
        assert browser.h1().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.h1(id='no_such_id').exists is False
        assert browser.h1(id=compile(r'no_such_id')).exists is False
        assert browser.h1(text='no_such_text').exists is False
        assert browser.h1(text=compile(r'no_such_text 1')).exists is False
        assert browser.h1(index=1337).exists is False
        assert browser.h1(xpath="//h1[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.h1(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.h1(no_such_how='some_value').exists


class TestHnAttributes(object):
    # class
    def test_returns_the_class_name_if_the_element_exists_and_has_id(self, browser):
        assert browser.h1(index=0).class_name == 'primary'

    def test_returns_an_empty_string_if_the_element_exists_and_the_class_name_doesnt(self, browser):
        assert browser.h2(index=0).class_name == ''

    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.h2(id='no_such_id').class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.h1(index=0).id == 'first_header'

    def test_returns_an_empty_string_if_the_element_exists_and_the_id_doesnt(self, browser):
        assert browser.h3(index=0).id == ''

    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.h1(id='no_such_id').id
        with pytest.raises(UnknownObjectException):
            browser.h1(index=1337).id

    # text
    def test_returns_the_text_if_the_element_exists_and_has_name(self, browser):
        assert browser.h1(index=1).text == 'Header 1'

    def test_returns_an_empty_string_if_the_element_exists_and_the_text_doesnt(self, browser):
        assert browser.h6(id='empty_header').text == ''

    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.h1(id='no_such_id').text
        with pytest.raises(UnknownObjectException):
            browser.h1(xpath="//h1[@id='no_such_id']").text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.h1(index=1), 'class_name')
    assert hasattr(browser.h1(index=1), 'id')
    assert hasattr(browser.h1(index=1), 'text')
