from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestLiExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.li(id='non_link_1').exists is True
        assert browser.li(id=compile(r'non_link_1')).exists is True
        assert browser.li(text='Non-link 3').exists is True
        assert browser.li(text=compile(r'Non-link 3')).exists is True
        assert browser.li(class_name='nonlink').exists is True
        assert browser.li(class_name=compile(r'nonlink')).exists is True
        assert browser.li(index=0).exists is True
        assert browser.li(xpath="//li[@id='non_link_1']").exists is True

    def test_returns_the_first_li_if_given_no_args(self, browser):
        assert browser.li().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.li(id='no_such_id').exists is False
        assert browser.li(id=compile(r'no_such_id')).exists is False
        assert browser.li(text='no_such_text').exists is False
        assert browser.li(text=compile(r'no_such_text')).exists is False
        assert browser.li(class_name='no_such_class').exists is False
        assert browser.li(class_name=compile(r'no_such_class')).exists is False
        assert browser.li(index=1337).exists is False
        assert browser.li(xpath="//li[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.li(id=3.14).exists


class TestLiAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_element_exists_and_has_class_name(self, browser):
        assert browser.li(id='non_link_1').class_name == 'nonlink'

    def test_returns_an_empty_string_if_the_li_exists_and_the_class_name_doesnt(self, browser):
        assert browser.li(index=0).class_name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.li(index=1337).class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.li(class_name='nonlink').id == 'non_link_1'

    def test_returns_an_empty_string_if_the_li_exists_and_the_id_doesnt(self, browser):
        assert browser.li(index=0).id == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.li(index=1337).id

    # title
    def test_returns_the_title_if_the_element_exists_and_has_title(self, browser):
        assert browser.li(id='non_link_1').title == 'This is not a link!'

    def test_returns_an_empty_string_if_the_li_exists_and_the_title_doesnt(self, browser):
        assert browser.li(index=0).title == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.li(index=1337).title

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.li(id='non_link_1').text == 'Non-link 1'

    def test_returns_an_empty_string_if_the_li_exists_and_the_text_doesnt(self, browser):
        assert browser.li(index=0).text == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.li(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.li(index=0), 'class_name')
    assert hasattr(browser.li(index=0), 'id')
    assert hasattr(browser.li(index=0), 'text')
    assert hasattr(browser.li(index=0), 'title')
