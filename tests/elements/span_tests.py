from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestSpanExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.span(id='lead').exists is True
        assert browser.span(id=compile(r'lead')).exists is True
        assert browser.span(text='Dubito, ergo cogito, ergo sum.').exists is True
        assert browser.span(text=compile(r'Dubito, ergo cogito, ergo sum')).exists is True
        assert browser.span(class_name='lead').exists is True
        assert browser.span(class_name=compile(r'lead')).exists is True
        assert browser.span(index=0).exists is True
        assert browser.span(xpath="//span[@id='lead']").exists is True

    def test_returns_the_first_span_if_given_no_args(self, browser):
        assert browser.span().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.span(id='no_such_id').exists is False
        assert browser.span(id=compile(r'no_such_id')).exists is False
        assert browser.span(text='no_such_text').exists is False
        assert browser.span(text=compile(r'no_such_text')).exists is False
        assert browser.span(class_name='no_such_class').exists is False
        assert browser.span(class_name=compile(r'no_such_class')).exists is False
        assert browser.span(index=1337).exists is False
        assert browser.span(xpath="//span[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.span(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.span(no_such_how='some_value').exists


class TestSpanAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_element_exists_and_has_class_name(self, browser):
        assert browser.span(index=0).class_name == 'lead'

    def test_returns_an_empty_string_if_the_element_exists_and_the_class_name_doesnt(self, browser):
        assert browser.span(index=2).class_name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.span(index=1337).class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.span(index=0).id == 'lead'

    def test_returns_an_empty_string_if_the_element_exists_and_the_id_doesnt(self, browser):
        assert browser.span(index=2).id == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.span(index=1337).id

    # title
    def test_returns_the_title_if_the_element_exists_and_has_title(self, browser):
        assert browser.span(index=0).title == 'Lorem ipsum'

    def test_returns_an_empty_string_if_the_element_exists_and_the_title_doesnt(self, browser):
        assert browser.span(index=2).title == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.span(index=1337).title

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.span(index=1).text == 'Sed pretium metus et quam. Nullam odio dolor, vestibulum non, tempor ut, vehicula sed, sapien. Vestibulum placerat ligula at quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.'

    def test_returns_an_empty_string_if_the_element_exists_and_the_text_doesnt(self, browser):
        assert browser.span(index=4).text == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.span(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.span(index=0), 'class_name')
    assert hasattr(browser.span(index=0), 'id')
    assert hasattr(browser.span(index=0), 'title')
    assert hasattr(browser.span(index=0), 'text')


class TestSpanClick(object):
    def test_fires_events(self, browser):
        assert 'Javascript' not in browser.span(class_name='footer').text
        browser.span(class_name='footer').click()
        assert 'Javascript' in browser.span(class_name='footer').text

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.span(index=1337).click()
