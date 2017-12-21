from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestHiddenExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.hidden(id='new_user_interests_dolls').exists is True
        assert browser.hidden(id=compile(r'new_user_interests_dolls')).exists is True
        assert browser.hidden(name='new_user_interests').exists is True
        assert browser.hidden(name=compile(r'new_user_interests')).exists is True
        assert browser.hidden(value='dolls').exists is True
        assert browser.hidden(value=compile(r'dolls')).exists is True
        assert browser.hidden(class_name='fun').exists is True
        assert browser.hidden(class_name=compile(r'fun')).exists is True
        assert browser.hidden(index=0).exists is True
        assert browser.hidden(xpath="//input[@id='new_user_interests_dolls']").exists is True

    def test_returns_the_first_hidden_if_given_no_args(self, browser):
        assert browser.hidden().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.hidden(id='no_such_id').exists is False
        assert browser.hidden(id=compile(r'no_such_id')).exists is False
        assert browser.hidden(name='no_such_name').exists is False
        assert browser.hidden(name=compile(r'no_such_name')).exists is False
        assert browser.hidden(value='no_such_value').exists is False
        assert browser.hidden(value=compile(r'no_such_value')).exists is False
        assert browser.hidden(class_name='no_such_class').exists is False
        assert browser.hidden(class_name=compile(r'no_such_class')).exists is False
        assert browser.hidden(index=1337).exists is False
        assert browser.hidden(xpath="//hidden[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.hidden(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.hidden(no_such_how='some_value').exists


class TestHiddenAttributes(object):
    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.hidden(index=1).id == 'new_user_interests_dolls'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.hidden(index=1337).id

    # name
    def test_returns_the_name_if_the_element_exists_and_has_name(self, browser):
        assert browser.hidden(index=1).name == 'new_user_interests'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.hidden(index=1337).name

    # type
    def test_returns_the_type_if_the_element_exists(self, browser):
        assert browser.hidden(index=1).type == 'hidden'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.hidden(index=1337).type

    # value
    def test_returns_the_value_if_the_element_exists(self, browser):
        assert browser.hidden(index=1).value == 'dolls'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.hidden(index=1337).type


def test_raises_correct_exception_when_attempting_to_click(browser):
    from nerodia.exception import ObjectDisabledException
    with pytest.raises(ObjectDisabledException):
        browser.hidden(index=1337).click()


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.hidden(index=1), 'id')
    assert hasattr(browser.hidden(index=1), 'name')
    assert hasattr(browser.hidden(index=1), 'type')
    assert hasattr(browser.hidden(index=1), 'value')
