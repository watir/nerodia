import pytest
from re import compile

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestButtonExist(object):
    def test_returns_true_if_the_button_exists_input_tag(self, browser):
        assert browser.button(id='new_user_submit').exists
        assert browser.button(id=compile(r'new_user_submit')).exists
        assert browser.button(name='new_user_reset').exists
        assert browser.button(name=compile(r'new_user_reset')).exists
        assert browser.button(value='Button').exists
        assert browser.button(value=compile(r'Button')).exists
        # TODO: xfail IE
        assert browser.button(src='images/button.png').exists
        assert browser.button(src=compile(r'button\.png')).exists
        assert browser.button(text='Button 2').exists
        assert browser.button(text=compile(r'Button 2')).exists
        assert browser.button(class_name='image').exists
        assert browser.button(class_name=compile(r'image')).exists
        assert browser.button(index=0).exists
        assert browser.button(xpath="//input[@id='new_user_submit']").exists
        assert browser.button(alt='Create a new user').exists
        assert browser.button(alt=compile(r'Create a')).exists

    def test_returns_true_if_the_button_exists_button_tag(self, browser):
        assert browser.button(name='new_user_button_2').exists
        assert browser.button(name=compile(r'new_user_button_2')).exists
        assert browser.button(value='button_2').exists
        assert browser.button(value=compile(r'button_2')).exists
        assert browser.button(text='Button 2').exists
        assert browser.button(text=compile(r'Button 2')).exists
        assert browser.button(value='Button 2').exists
        assert browser.button(value=compile(r'Button 2')).exists

    def test_returns_true_if_the_button_exists_caption(self, browser):
        assert browser.button(caption='Button 2').exists
        assert browser.button(caption=compile(r'Button 2')).exists

    def test_returns_the_first_button_if_given_no_args(self, browser):
        assert browser.button().exists

    def test_returns_true_for_element_with_upper_case_type(self, browser):
        assert browser.button(id='new_user_button_preview').exist

    def test_returns_false_if_the_button_doesnt_exist(self, browser):
        assert not browser.button(id='no_such_id').exists
        assert not browser.button(id=compile(r'no_such_id')).exists
        assert not browser.button(name='no_such_name').exists
        assert not browser.button(name=compile(r'no_such_name')).exists
        assert not browser.button(value='no_such_value').exists
        assert not browser.button(value=compile(r'no_such_value')).exists
        assert not browser.button(src='no_such_src').exists
        assert not browser.button(src=compile(r'no_such_src')).exists
        assert not browser.button(text='no_such_text').exists
        assert not browser.button(text=compile(r'no_such_text')).exists
        assert not browser.button(class_name='no_such_class').exists
        assert not browser.button(class_name=compile(r'no_such_class')).exists
        assert not browser.button(index=1337).exists
        assert not browser.button(xpath="//input[@id='no_such_id']").exists

    def test_checks_the_tag_name_and_type_attribute_when_locating_by_xpath(self, browser):
        assert not browser.button(xpath="//input[@type='text']").exists
        assert browser.button(xpath="//input[@type='button']").exists

    def test_matches_the_specific_type_when_locating_by_type(self, browser):
        assert browser.button(type='button').type == 'button'
        assert browser.button(type='reset').type == 'reset'
        assert browser.button(type='submit').type == 'submit'
        assert browser.button(type='image').type == 'image'

    def test_matches_valid_input_types_when_type_is_boolean(self, browser):
        assert all(button.tag_name == 'button' for button in browser.buttons(type=False))

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.button(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.button(no_such_how='some_value').exists


class TestButtonAttributes(object):
    # class_name
    def test_returns_the_class_name_of_the_button(self, browser):
        assert browser.button(name='new_user_image').class_name == 'image'

    def test_returns_an_empty_string_if_the_button_has_no_class_name(self, browser):
        assert browser.button(name='new_user_submit').class_name == ''

    # id
    def test_returns_the_id_if_the_button_exists(self, browser):
        assert browser.button(index=0).id == 'new_user_submit'
        assert browser.button(index=1).id == 'new_user_reset'
        assert browser.button(index=2).id == 'new_user_button'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_button_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(index=1337).id

    # name
    def test_returns_the_name_if_button_exists(self, browser):
        assert browser.button(index=0).name == 'new_user_submit'
        assert browser.button(index=1).name == 'new_user_reset'
        assert browser.button(index=2).name == 'new_user_button'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_button_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').name

    # src
    def test_returns_the_src_attribute_for_the_button_image(self, browser):
        # varies between browsers
        assert 'images/button.png' in browser.button(name='new_user_image').src

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_src_if_button_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').src

    # style
    # TODO: xfail for IE and safari
    def test_returns_the_style_attribute_if_the_button_exists(self, browser):
        assert browser.button(id='delete_user_submit').style() == 'border: 4px solid red;'

    def test_returns_an_empty_string_if_the_element_exists_and_the_attribute_doesnt_exist(self, browser):
        assert browser.button(id='new_user_submit').style() == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_style_if_the_button_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').style()

    # title
    def test_returns_the_title_of_the_button(self, browser):
        assert browser.button(index=0).title == 'Submit the form'

    def test_returns_an_empty_string_for_button_without_title(self, browser):
        assert browser.button(index=1).title == ''

    # type
    def test_returns_the_type_if_button_exists(self, browser):
        assert browser.button(index=0).type == 'submit'
        assert browser.button(index=1).type == 'reset'
        assert browser.button(index=2).type == 'button'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_button_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').type

    # value
    def test_returns_the_value_if_button_exists(self, browser):
        assert browser.button(index=0).value == 'Submit'
        assert browser.button(index=1).value == 'Reset'
        assert browser.button(index=2).value == 'Button'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_button_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').value

    # text
    def test_returns_the_text_of_the_button(self, browser):
        assert browser.button(index=0).text == 'Submit'
        assert browser.button(index=1).text == 'Reset'
        assert browser.button(index=2).text == 'Button'
        assert browser.button(index=3).text == 'Preview'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.button(index=0), 'class_name')
    assert hasattr(browser.button(index=0), 'id')
    assert hasattr(browser.button(index=0), 'name')
    assert hasattr(browser.button(index=0), 'src')
    assert hasattr(browser.button(index=0), 'style')
    assert hasattr(browser.button(index=0), 'title')
    assert hasattr(browser.button(index=0), 'type')
    assert hasattr(browser.button(index=0), 'value')


class TestButtonEnabled(object):
    # enabled
    def test_returns_true_if_the_button_is_enabled(self, browser):
        assert browser.button(name='new_user_submit').enabled

    def test_returns_false_if_the_button_is_disabled(self, browser):
        assert not browser.button(name='new_user_submit_disabled').enabled

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_the_button_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').enabled

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_disabled_button_is_clicked(self, browser):
        from nerodia.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            browser.button(name='new_user_submit_disabled').click()

    # diabled
    def test_returns_false_when_button_is_enabled(self, browser):
        assert not browser.button(name='new_user_submit').disabled

    def test_returns_true_when_button_is_disabled(self, browser):
        assert browser.button(name='new_user_submit_disabled').disabled

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_disabled_if_the_button_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').disabled


class TestButtonManipulation(object):
    def test_clicks_the_button_if_it_exists(self, browser):
        browser.button(id='delete_user_submit').click()
        browser.wait_until(lambda b: 'forms_with_input_elements.html' not in b.url)
        assert 'Semantic table' in browser.text

    def test_fires_events(self, browser):
        browser.button(id='new_user_button').click()
        assert browser.button(id='new_user_button').value == 'new_value_set_by_onclick_event'

    @pytest.mark.parametrize('selector',
                             [{'value': 'no_such_value'},
                              {'id': 'no_such_id'}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_clicking_a_button_that_doesnt_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.button(**selector).click()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_clicking_a_disabled_button(self, browser):
        from nerodia.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            browser.button(value='Disabled').click()
