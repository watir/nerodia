from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestInsExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.ins(id='lead').exists is True
        assert browser.ins(id=compile(r'lead')).exists is True
        assert browser.ins(text='This is an inserted text tag 1').exists is True
        assert browser.ins(text=compile(r'This is an inserted text tag 1')).exists is True
        assert browser.ins(class_name='lead').exists is True
        assert browser.ins(class_name=compile(r'lead')).exists is True
        assert browser.ins(index=0).exists is True
        assert browser.ins(xpath="//ins[@id='lead']").exists is True

    def test_returns_the_first_ins_if_given_no_args(self, browser):
        assert browser.ins().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.ins(id='no_such_id').exists is False
        assert browser.ins(id=compile(r'no_such_id')).exists is False
        assert browser.ins(text='no_such_text').exists is False
        assert browser.ins(text=compile(r'no_such_text')).exists is False
        assert browser.ins(class_name='no_such_class').exists is False
        assert browser.ins(class_name=compile(r'no_such_class')).exists is False
        assert browser.ins(index=1337).exists is False
        assert browser.ins(xpath="//ins[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.ins(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.ins(no_such_how='some_value').exists


class TestInsAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_element_exists_and_has_class_name(self, browser):
        assert browser.ins(index=0).class_name == 'lead'

    def test_returns_an_empty_string_if_the_ins_exists_and_the_class_name_doesnt(self, browser):
        assert browser.ins(index=2).class_name == ''

    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.ins(index=1337).class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.ins(index=0).id == 'lead'

    def test_returns_an_empty_string_if_the_ins_exists_and_the_id_doesnt(self, browser):
        assert browser.ins(index=2).id == ''

    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.ins(index=1337).id

    # title
    def test_returns_the_title_if_the_element_exists(self, browser):
        assert browser.ins(index=0).title == 'Lorem ipsum'

    def test_returns_an_empty_string_if_the_ins_exists_and_the_title_doesnt(self, browser):
        assert browser.ins(index=2).title == ''

    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.ins(index=1337).title

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.ins(index=1).text == 'This is an inserted text tag 2'

    def test_returns_an_empty_string_if_the_ins_exists_and_the_text_doesnt(self, browser):
        assert browser.ins(index=3).text == ''

    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.ins(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.ins(index=0), 'class_name')
    assert hasattr(browser.ins(index=0), 'id')
    assert hasattr(browser.ins(index=0), 'title')
    assert hasattr(browser.ins(index=0), 'text')


class TestInsClick(object):
    def test_fires_events(self, browser):
        assert 'Javascript' not in browser.ins(class_name='footer').text
        browser.ins(class_name='footer').click()
        assert 'Javascript' in browser.ins(class_name='footer').text

    def test_raises_correct_exception_for_click_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.ins(id='no_such_id').click()
