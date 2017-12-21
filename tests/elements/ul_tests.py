import re

import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestUlExists(object):
    def test_returns_true_if_the_ul_exists(self, browser):
        assert browser.ul(id='navbar').exists
        assert browser.ul(id=re.compile('navbar')).exists
        assert browser.ul(index=0).exists
        assert browser.ul(xpath="//ul[@id='navbar']").exists

    def test_returns_the_first_ul_if_given_no_args(self, browser):
        assert browser.ul().exists

    def test_returns_false_if_the_ul_doesnt_exist(self, browser):
        assert not browser.ul(id='no_such_id').exists
        assert not browser.ul(id=re.compile('no_such_id')).exists
        assert not browser.ul(text='no_such_text').exists
        assert not browser.ul(text=re.compile('no_such_id')).exists
        assert not browser.ul(class_name='no_such_class').exists
        assert not browser.ul(class_name=re.compile('no_such_class')).exists
        assert not browser.ul(index=1337).exists
        assert not browser.ul(xpath="//ul[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.ul(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.ul(no_such_how='some_value').exists


class TestUlAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_ul_exists_and_has_class_name(self, browser):
        assert browser.ul(id='navbar').class_name == 'navigation'

    def test_returns_an_empty_string_if_the_ul_exists_and_has_no_class_name(self, browser):
        assert browser.ul(index=1).class_name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_the_ul_doesnt_exist(self, browser):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.ul(id='no_such_id').class_name

    # id
    def test_returns_the_id_if_the_checkbox_exists_and_has_id(self, browser):
        assert browser.ul(class_name='navigation').id == 'navbar'

    def test_returns_an_empty_string_if_the_checkbox_exists_and_has_no_id(self, browser):
        assert browser.ul(index=1).id == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_checkbox_doesnt_exist(self, browser):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.ul(id='no_such_id').id
        with pytest.raises(UnknownObjectException):
            browser.ul(index=1337).id


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.ul(index=0), 'class_name')
    assert hasattr(browser.ul(index=0), 'id')
