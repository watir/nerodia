import re

import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestOlExists(object):
    def test_returns_true_if_the_ol_exists(self, browser):
        assert browser.ol(id='favorite_compounds').exists
        assert browser.ol(id=re.compile('favorite_compounds')).exists
        assert browser.ol(index=0).exists
        assert browser.ol(xpath="//ol[@id='favorite_compounds']").exists

    def test_returns_the_first_ol_if_given_no_args(self, browser):
        assert browser.ol().exists

    def test_returns_false_if_the_ol_doesnt_exist(self, browser):
        assert not browser.ol(id='no_such_id').exists
        assert not browser.ol(id=re.compile('no_such_id')).exists
        assert not browser.ol(text='no_such_text').exists
        assert not browser.ol(text=re.compile('no_such_id')).exists
        assert not browser.ol(class_name='no_such_class').exists
        assert not browser.ol(class_name=re.compile('no_such_class')).exists
        assert not browser.ol(index=1337).exists
        assert not browser.ol(xpath="//ol[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.ol(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.ol(no_such_how='some_value').exists


class TestOlAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_ol_exists_and_has_class_name(self, browser):
        assert browser.ol(id='favorite_compounds').class_name == 'chemistry'

    def test_returns_an_empty_string_if_the_ol_exists_and_has_no_class_name(self, browser):
        assert browser.ol(index=1).class_name == ''

    def test_raises_correct_exception_for_class_name_if_the_ol_doesnt_exist(self, browser):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.ol(id='no_such_id').class_name

    # id
    def test_returns_the_id_if_the_checkbox_exists_and_has_id(self, browser):
        assert browser.ol(class_name='chemistry').id == 'favorite_compounds'

    def test_returns_an_empty_string_if_the_checkbox_exists_and_has_no_id(self, browser):
        assert browser.ol(index=1).id == ''

    def test_raises_correct_exception_for_id_if_the_checkbox_doesnt_exist(self, browser):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.ol(id='no_such_id').id
        with pytest.raises(UnknownObjectException):
            browser.ol(index=1337).id


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.ol(index=0), 'class_name')
    assert hasattr(browser.ol(index=0), 'id')
