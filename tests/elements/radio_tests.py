from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestRadioExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.radio(id='new_user_newsletter_yes').exists is True
        assert browser.radio(id=compile(r'new_user_newsletter_yes')).exists is True
        assert browser.radio(name='new_user_newsletter').exists is True
        assert browser.radio(name=compile(r'new_user_newsletter')).exists is True
        assert browser.radio(value='yes').exists is True
        assert browser.radio(value=compile(r'yes')).exists is True
        assert browser.radio(text='Yes').exists is True
        assert browser.radio(text=compile(r'Yes')).exists is True
        assert browser.radio(class_name='huge').exists is True
        assert browser.radio(class_name=compile(r'huge')).exists is True
        assert browser.radio(index=0).exists is True
        assert browser.radio(xpath="//input[@id='new_user_newsletter_yes']").exists is True

    def test_returns_the_first_radio_if_given_no_args(self, browser):
        assert browser.radio().exists

    def test_returns_true_if_the_radio_button_exists_by_name_and_value(self, browser):
        assert browser.radio(name='new_user_newsletter', value='yes').exists is True
        browser.radio(xpath="//input[@name='new_user_newsletter' and @value='yes']").set()

    def test_returns_true_for_element_with_upper_case_type(self, browser):
        assert browser.radio(id='new_user_newsletter_probably').exists is True

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.radio(id='no_such_id').exists is False
        assert browser.radio(id=compile(r'no_such_id')).exists is False
        assert browser.radio(name='no_such_name').exists is False
        assert browser.radio(name=compile(r'no_such_name')).exists is False
        assert browser.radio(value='no_such_value').exists is False
        assert browser.radio(value=compile(r'no_such_value')).exists is False
        assert browser.radio(text='no_such_text').exists is False
        assert browser.radio(text=compile(r'no_such_text')).exists is False
        assert browser.radio(class_name='no_such_class').exists is False
        assert browser.radio(class_name=compile(r'no_such_class')).exists is False
        assert browser.radio(index=1337).exists is False
        assert browser.radio(xpath="input[@id='no_such_id']").exists is False

    def test_returns_false_if_the_element_does_not_exist_by_name_and_value(self, browser):
        assert browser.radio(name='new_user_newsletter', value='no_such_value').exists is False
        assert browser.radio(xpath="//input[@name='new_user_newsletter' and @value='no_such_value']").exists is False
        assert browser.radio(name='no_such_name', value='yes').exists is False
        assert browser.radio(xpath="//input[@name='no_such_name' and @value='yes']").exists is False

    def test_returns_true_for_radios_with_a_string_value(self, browser):
        assert browser.radio(name='new_user_newsletter', value='yes').exists is True
        assert browser.radio(name='new_user_newsletter', value='no').exists is True

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.radio(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.radio(no_such_how='some_value').exists


class TestRadioAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_element_exists_and_has_class_name(self, browser):
        assert browser.radio(id='new_user_newsletter_yes').class_name == 'huge'

    def test_returns_an_empty_string_if_the_element_exists_and_the_class_name_doesnt(self, browser):
        assert browser.radio(id='new_user_newsletter_no').class_name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).class_name

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.radio(index=0).id == 'new_user_newsletter_yes'

    def test_returns_an_empty_string_if_the_element_exists_and_the_id_doesnt(self, browser):
        assert browser.radio(index=2).id == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).id

    # name
    def test_returns_the_name_if_the_element_exists_and_has_name(self, browser):
        assert browser.radio(id='new_user_newsletter_yes').name == 'new_user_newsletter'

    def test_returns_an_empty_string_if_the_element_exists_and_the_name_doesnt(self, browser):
        assert browser.radio(id='new_user_newsletter_absolutely').name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).name

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.radio(id='new_user_newsletter_yes').text == 'Yes'

    def test_returns_an_empty_string_if_the_element_exists_and_the_label_doesnt(self, browser):
        assert browser.form(id='new_user').radio(index=2).text == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).text

    # title
    def test_returns_the_title_if_the_element_exists_and_has_title(self, browser):
        assert browser.radio(id='new_user_newsletter_no').title == 'Traitor!'

    def test_returns_an_empty_string_if_the_element_exists_and_the_title_doesnt(self, browser):
        assert browser.radio(id='new_user_newsletter_yes').title == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).title

    # type
    def test_returns_the_type_if_the_element_exists_and_has_type(self, browser):
        assert browser.radio(index=0).type == 'radio'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).type
            browser.radio(index=1337).title

    # value
    def test_returns_the_value_if_the_element_exists_and_has_value(self, browser):
        assert browser.radio(id='new_user_newsletter_yes').value == 'yes'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio(index=1337).value


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.radio(index=0), 'class_name')
    assert hasattr(browser.radio(index=0), 'id')
    assert hasattr(browser.radio(index=0), 'name')
    assert hasattr(browser.radio(index=0), 'title')
    assert hasattr(browser.radio(index=0), 'type')
    assert hasattr(browser.radio(index=0), 'value')
