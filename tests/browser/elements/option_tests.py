from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestOptionExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.option(id='nor').exists is True
        assert browser.option(id=compile(r'nor')).exists is True
        assert browser.option(value='2').exists is True
        assert browser.option(value=compile(r'2')).exists is True
        assert browser.option(text='Norway').exists is True
        assert browser.option(text=compile(r'Norway')).exists is True
        assert browser.option(index=1).exists is True
        assert browser.option(xpath="//option[@id='nor']").exists is True

    def test_returns_the_first_option_if_given_no_args(self, browser):
        assert browser.option().exists

    def test_returns_true_if_the_element_exists_within_select_list(self, browser):
        assert browser.select_list(name='new_user_country').option(id='nor').exists is True
        assert browser.select_list(name='new_user_country').option(id=compile(r'nor')).exists is True
        assert browser.select_list(name='new_user_country').option(value='2').exists is True
        assert browser.select_list(name='new_user_country').option(value=compile(r'2')).exists is True
        assert browser.select_list(name='new_user_country').option(text='Norway').exists is True
        assert browser.select_list(name='new_user_country').option(text=compile(r'Norway')).exists is True
        assert browser.select_list(name='new_user_country').option(index=1).exists is True
        assert browser.select_list(name='new_user_country').option(xpath="//option[@id='nor']").exists is True

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.option(id='no_such_id').exists is False
        assert browser.option(id=compile(r'no_such_id')).exists is False
        assert browser.option(value='no_such_value').exists is False
        assert browser.option(value=compile(r'no_such_value')).exists is False
        assert browser.option(text='no_such_text').exists is False
        assert browser.option(text=compile(r'no_such_text')).exists is False
        assert browser.option(class_name='no_such_class').exists is False
        assert browser.option(index=1337).exists is False
        assert browser.option(xpath="//option[@id='no_such_id']").exists is False

    def test_returns_false_if_the_element_does_not_exist_within_select_list(self, browser):
        assert browser.select_list(name='new_user_country').option(id='no_such_id').exists is False
        assert browser.select_list(name='new_user_country').option(id=compile(r'no_such_id')).exists is False
        assert browser.select_list(name='new_user_country').option(value='no_such_value').exists is False
        assert browser.select_list(name='new_user_country').option(value=compile(r'no_such_value')).exists is False
        assert browser.select_list(name='new_user_country').option(text='no_such_text').exists is False
        assert browser.select_list(name='new_user_country').option(text=compile(r'no_such_text')).exists is False
        assert browser.select_list(name='new_user_country').option(class_name='no_such_class').exists is False
        assert browser.select_list(name='new_user_country').option(index=1337).exists is False
        assert browser.select_list(name='new_user_country').option(xpath="//option[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.option(id=3.14).exists
        with pytest.raises(TypeError):
            browser.select_list(name='new_user_country').option(id=3.14).exists


class TestOptionSelect(object):
    def test_selects_the_chosen_option(self, browser):
        browser.option(text='Denmark').select()
        assert [x.text for x in browser.select_list(name='new_user_country').selected_options] == ['Denmark']

    def test_selects_the_chosen_option_within_select_list(self, browser):
        browser.select_list(name='new_user_country').option(text='Denmark').select()
        assert [x.text for x in browser.select_list(name='new_user_country').selected_options] == ['Denmark']

    def test_selects_the_option_when_found_by_text(self, browser):
        browser.option(text='Sweden').select()
        assert browser.option(text='Sweden').is_selected

    def test_selects_the_option_when_found_by_text_within_select_list(self, browser):
        browser.select_list(name='new_user_country').option(text='Sweden').select()
        assert browser.select_list(name='new_user_country').option(text='Sweden').is_selected

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_option_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.option(text='no_such_text').select()
        with pytest.raises(UnknownObjectException):
            browser.option(text=compile(r'missing')).select()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_option_does_not_exist_within_select_list(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(name='new_user_country').option(text='no_such_text').select()
        with pytest.raises(UnknownObjectException):
            browser.select_list(name='new_user_country').option(text=compile(r'missing')).select()


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.select_list(name='new_user_country').option(text='Sweden'), 'class_name')
    assert hasattr(browser.select_list(name='new_user_country').option(text='Sweden'), 'id')
    assert hasattr(browser.select_list(name='new_user_country').option(text='Sweden'), 'text')
