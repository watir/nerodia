from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestStrongExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.strong(id='descartes').exists is True
        assert browser.strong(id=compile(r'descartes')).exists is True
        assert browser.strong(text='Dubito, ergo cogito, ergo sum.').exists is True
        assert browser.strong(text=compile(r'Dubito, ergo cogito, ergo sum')).exists is True
        assert browser.strong(class_name='descartes').exists is True
        assert browser.strong(class_name=compile(r'descartes')).exists is True
        assert browser.strong(index=0).exists is True
        assert browser.strong(xpath="//strong[@id='descartes']").exists is True

    def test_returns_the_first_strong_if_given_no_args(self, browser):
        assert browser.strong().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.strong(id='no_such_id').exists is False
        assert browser.strong(id=compile(r'no_such_id')).exists is False
        assert browser.strong(text='no_such_text').exists is False
        assert browser.strong(text=compile(r'no_such_text')).exists is False
        assert browser.strong(class_name='no_such_class').exists is False
        assert browser.strong(class_name=compile(r'no_such_class')).exists is False
        assert browser.strong(index=1337).exists is False
        assert browser.strong(xpath="//strong[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.strong(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.strong(no_such_how='some_value').exists


class TestStrongAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_element_exists_and_has_class_name(self, browser):
        assert browser.strong(index=0).class_name == 'descartes'

    def test_returns_an_empty_string_if_the_element_exists_and_the_class_name_doesnt(self, browser):
        assert browser.strong(index=1).class_name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.strong(index=1337).class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.strong(index=0).id == 'descartes'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.strong(index=1337).id

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.strong(index=0).text == 'Dubito, ergo cogito, ergo sum.'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.strong(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.strong(index=0), 'class_name')
    assert hasattr(browser.strong(index=0), 'id')
    assert hasattr(browser.strong(index=0), 'text')
