from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestPreExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.pre(id='rspec').exists is True
        assert browser.pre(id=compile(r'rspec')).exists is True
        assert browser.pre(text='browser.pre(id: "rspec").should exist').exists is True
        assert browser.pre(text=compile(r'browser\.pre')).exists is True
        assert browser.pre(class_name='ruby').exists is True
        assert browser.pre(class_name=compile(r'ruby')).exists is True
        assert browser.pre(index=0).exists is True
        assert browser.pre(xpath="//pre[@id='rspec']").exists is True

    def test_returns_the_first_pre_if_given_no_args(self, browser):
        assert browser.pre().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.pre(id='no_such_id').exists is False
        assert browser.pre(id=compile(r'no_such_id')).exists is False
        assert browser.pre(text='no_such_text').exists is False
        assert browser.pre(text=compile(r'no_such_text')).exists is False
        assert browser.pre(class_name='no_such_class').exists is False
        assert browser.pre(class_name=compile(r'no_such_class')).exists is False
        assert browser.pre(index=1337).exists is False
        assert browser.pre(xpath="//pre[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.pre(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.pre(no_such_how='some_value').exists


class TestPreAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_element_exists_and_has_class_name(self, browser):
        assert browser.pre(id='rspec').class_name == 'ruby'

    def test_returns_an_empty_string_if_the_element_exists_and_the_class_name_doesnt(self, browser):
        assert browser.pre(index=0).class_name == ''

    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.pre(index=1337).class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.pre(class_name='ruby').id == 'rspec'

    def test_returns_an_empty_string_if_the_element_exists_and_the_id_doesnt(self, browser):
        assert browser.pre(index=0).id == ''

    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.pre(index=1337).id

    # title
    def test_returns_the_title_if_the_element_exists_and_has_title(self, browser):
        assert browser.pre(class_name='brainfuck').title == 'The brainfuck language is an esoteric programming language noted for its extreme minimalism'

    def test_returns_an_empty_string_if_the_element_exists_and_the_title_doesnt(self, browser):
        assert browser.pre(index=0).title == ''

    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.pre(index=1337).title

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.pre(class_name='haskell').text == 'main = putStrLn "Hello World"'

    def test_returns_an_empty_string_if_the_element_exists_and_the_text_doesnt(self, browser):
        assert browser.pre(index=0).text == ''

    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.pre(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.pre(index=0), 'class_name')
    assert hasattr(browser.pre(index=0), 'id')
    assert hasattr(browser.pre(index=0), 'title')
    assert hasattr(browser.pre(index=0), 'text')
