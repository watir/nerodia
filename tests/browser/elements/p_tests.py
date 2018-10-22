import re

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestPExists(object):
    def test_returns_true_if_the_p_exists(self, browser):
        assert browser.p(id='lead').exists
        assert browser.p(id=re.compile('lead')).exists
        assert browser.p(text='Dubito, ergo cogito, ergo sum.').exists
        assert browser.p(text=re.compile('Dubito, ergo cogito, ergo sum.')).exists
        assert browser.p(class_name='lead').exists
        assert browser.p(class_name=re.compile('lead')).exists
        assert browser.p(index=0).exists
        assert browser.p(xpath="//p[@id='lead']").exists

    def test_returns_the_first_p_if_given_no_args(self, browser):
        assert browser.p().exists

    def test_returns_false_if_the_p_doesnt_exist(self, browser):
        assert not browser.p(id='no_such_id').exists
        assert not browser.p(id=re.compile('no_such_id')).exists
        assert not browser.p(text='no_such_text').exists
        assert not browser.p(text=re.compile('no_such_text')).exists
        assert not browser.p(class_name='no_such_class').exists
        assert not browser.p(class_name=re.compile('no_such_class')).exists
        assert not browser.p(index=1337).exists
        assert not browser.p(xpath="//p[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.p(id=3.14).exists


class TestPAttributes(object):
    # id
    def test_returns_the_id_if_the_p_exists_and_has_id(self, browser):
        assert browser.p(index=0).id == 'lead'

    def test_returns_an_empty_string_if_the_p_exists_and_has_no_id(self, browser):
        assert browser.p(index=2).id == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_p_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.p(id='no_such_id').id
        with pytest.raises(UnknownObjectException):
            browser.p(index=1337).id

    # title
    def test_returns_the_title_if_the_p_exists_and_has_title(self, browser):
        assert browser.p(index=0).title == 'Lorem ipsum'

    def test_returns_an_empty_string_if_the_p_exists_and_has_no_title(self, browser):
        assert browser.p(index=2).title == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_title_if_the_p_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.p(id='no_such_id').title
        with pytest.raises(UnknownObjectException):
            browser.p(index=1337).title

    # text
    def test_returns_the_text_if_the_p_exists_and_has_text(self, browser):
        assert browser.p(index=1).text == 'Sed pretium metus et quam. Nullam odio dolor, vestibulum non, tempor ut, vehicula sed, sapien. Vestibulum placerat ligula at quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.'

    def test_returns_an_empty_string_if_the_p_exists_and_has_no_text(self, browser):
        assert browser.p(index=4).text == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_p_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.p(id='no_such_id').text
        with pytest.raises(UnknownObjectException):
            browser.p(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.p(index=0), 'class_name')
    assert hasattr(browser.p(index=0), 'id')
    assert hasattr(browser.p(index=0), 'title')
    assert hasattr(browser.p(index=0), 'text')
