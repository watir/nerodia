from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('non_control_elements.html')


class TestLinkExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.link(id='link_2').exists is True
        assert browser.link(id=compile(r'link_2')).exists is True
        assert browser.link(title='link_title_2').exists is True
        assert browser.link(title=compile(r'link_title_2')).exists is True
        assert browser.link(text='Link 2').exists is True
        assert browser.link(text=compile(r'Link 2')).exists is True
        assert browser.link(href='non_control_elements.html').exists is True
        assert browser.link(href=compile(r'non_control_elements.html')).exists is True
        assert browser.link(index=1).exists is True
        assert browser.link(xpath="//a[@id='link_2']").exists is True

    def test_returns_the_first_link_if_given_no_args(self, browser):
        assert browser.link().exists

    def test_strips_spaces_from_href_attribute_when_locating_elements(self, browser):
        assert browser.link(href=compile(r'strip_space$')).exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.link(id='no_such_id').exists is False
        assert browser.link(id=compile(r'no_such_id')).exists is False
        assert browser.link(title='no_such_title').exists is False
        assert browser.link(title=compile(r'no_such_title')).exists is False
        assert browser.link(text='no_such_text').exists is False
        assert browser.link(text=compile(r'no_such_text')).exists is False
        assert browser.link(href='no_such_href').exists is False
        assert browser.link(href=compile(r'no_such_href')).exists is False
        assert browser.link(index=1337).exists is False
        assert browser.link(xpath="//a[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.link(id=3.14).exists


class TestLinkAttributes(object):
    # href
    def test_returns_the_href_if_the_element_exists_and_has_href(self, browser):
        assert 'non_control_elements' in browser.link(index=1).href

    def test_returns_an_empty_string_if_the_element_exists_and_the_href_doesnt(self, browser):
        assert browser.link(index=0).href == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_href_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.link(index=1337).href

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.link(index=1).id == 'link_2'

    def test_returns_an_empty_string_if_the_element_exists_and_the_id_doesnt(self, browser):
        assert browser.link(index=0).id == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.link(index=1337).id

    # title
    def test_returns_the_title_if_the_element_exists_and_has_title(self, browser):
        assert browser.link(index=1).title == 'link_title_2'

    def test_returns_an_empty_string_if_the_element_exists_and_the_title_doesnt(self, browser):
        assert browser.link(index=0).title == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.link(index=1337).title


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.link(index=0), 'class_name')
    assert hasattr(browser.link(index=0), 'href')
    assert hasattr(browser.link(index=0), 'id')
    assert hasattr(browser.link(index=0), 'style')
    assert hasattr(browser.link(index=0), 'text')
    assert hasattr(browser.link(index=0), 'title')


class TestLinkManipulation(object):
    def test_finds_an_existing_link_by_text_string_and_clicks_it(self, browser):
        browser.link(text='Link 3').click()
        assert 'User administration' in browser.text

    def test_finds_an_existing_link_by_href_regexp_and_clicks_it(self, browser):
        browser.link(href=compile(r'forms_with_input_elements')).click()
        assert 'User administration' in browser.text

    def test_finds_an_existing_link_by_index_and_clicks_it(self, browser):
        browser.link(index=2).click()
        assert 'User administration' in browser.text

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_click_if_the_link_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.link(index=1337).click()

    @pytest.mark.page('images.html')
    def test_clicks_a_link_with_no_text_content_but_an_img_child(self, browser):
        from nerodia.wait.wait import Wait
        browser.link(href=compile(r'definition_lists.html')).click()
        Wait.until_not(lambda: browser.title == 'Images' or browser.title == '')
        assert browser.title == 'definition_lists'
