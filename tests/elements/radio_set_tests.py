from re import compile

import pytest

from nerodia.elements.radio import Radio, RadioCollection
from nerodia.exception import UnknownObjectException, ObjectDisabledException

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestRadioSetExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.radio_set(id='new_user_newsletter_yes').exists is True
        assert browser.radio_set(id=compile(r'new_user_newsletter_yes')).exists is True
        assert browser.radio_set(name='new_user_newsletter').exists is True
        assert browser.radio_set(name=compile(r'new_user_newsletter')).exists is True
        assert browser.radio_set(value='yes').exists is True
        assert browser.radio_set(value=compile(r'yes')).exists is True
        assert browser.radio_set(text='Yes').exists is True
        assert browser.radio_set(text=compile(r'Yes')).exists is True
        assert browser.radio_set(class_name='huge').exists is True
        assert browser.radio_set(class_name=compile(r'huge')).exists is True
        assert browser.radio_set(index=0).exists is True
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_yes']").exists is True

    def test_returns_the_first_radio_set_if_given_no_args(self, browser):
        assert browser.radio_set().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.radio_set(id='no_such_id').exists is False
        assert browser.radio_set(id=compile(r'no_such_id')).exists is False
        assert browser.radio_set(name='no_such_name').exists is False
        assert browser.radio_set(name=compile(r'no_such_name')).exists is False
        assert browser.radio_set(value='no_such_value').exists is False
        assert browser.radio_set(value=compile(r'no_such_value')).exists is False
        assert browser.radio_set(text='no_such_text').exists is False
        assert browser.radio_set(text=compile(r'no_such_text')).exists is False
        assert browser.radio_set(class_name='no_such_class').exists is False
        assert browser.radio_set(class_name=compile(r'no_such_class')).exists is False
        assert browser.radio_set(index=1337).exists is False
        assert browser.radio_set(xpath="input[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.radio_set(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.radio_set(no_such_how='some_value').exists


class TestRadioSetAttributes(object):
    # name
    def test_returns_the_name_if_the_element_exists_and_has_name(self, browser):
        assert browser.radio_set(id='new_user_newsletter_yes').name == 'new_user_newsletter'

    def test_returns_an_empty_string_if_the_element_exists_and_the_name_doesnt(self, browser):
        assert browser.radio_set(id='new_user_newsletter_absolutely').name == ''

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(index=1337).name

    def test_finds_specified_radio_without_name_specified(self, browser):
        assert len(browser.radio_set(id='new_user_newsletter_absolutely')) == 1
        assert len(browser.radio_set(id='new_user_newsletter_absolutely').radios()) == 1
        assert browser.radio_set(id='new_user_newsletter_absolutely').radio(value='absolutely').exists is True

    # type
    def test_returns_the_type_if_the_element_exists_and_has_type(self, browser):
        assert browser.radio_set(index=0).type == 'radio'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_type_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(index=1337).type

    # value
    def test_returns_the_value_if_the_element_exists_and_has_value(self, browser):
        assert browser.radio_set(id='new_user_newsletter_yes').value == 'yes'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(index=1337).value

    # text
    def test_returns_the_text_if_the_element_exists_and_has_text(self, browser):
        assert browser.radio_set(id='new_user_newsletter_yes').text == 'Yes'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.radio_set(index=0), 'class_name')
    assert hasattr(browser.radio_set(index=0), 'id')
    assert hasattr(browser.radio_set(index=0), 'name')
    assert hasattr(browser.radio_set(index=0), 'title')
    assert hasattr(browser.radio_set(index=0), 'type')
    assert hasattr(browser.radio_set(index=0), 'value')
    assert hasattr(browser.radio_set(index=0), 'text')
    assert not hasattr(browser.radio_set(index=0), 'clear')


class TestRadioSetAccess(object):
    # enabled

    def test_returns_true_if_any_radio_button_in_the_set_is_enabled(self, browser):
        assert browser.radio_set(id='new_user_newsletter_nah').enabled is True
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_nah']").enabled is True

    def test_returns_false_if_all_radio_buttons_are_disabled(self, browser):
        assert browser.radio_set(id='new_user_newsletter_none').enabled is False
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_none']").enabled is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(index=1337).enabled

    # disabled

    def test_returns_false_if_any_radio_button_in_the_set_is_enabled(self, browser):
        assert browser.radio_set(id='new_user_newsletter_nah').disabled is False
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_nah']").disabled is False

    def test_returns_true_if_all_radio_buttons_are_disabled(self, browser):
        assert browser.radio_set(id='new_user_newsletter_none').disabled is True
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_none']").disabled is True

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_disabled_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(index=1337).disabled


class TestRadioSetRadio(object):
    def test_returns_first_instance_of_radio_if_no_arguments_specified(self, browser):
        radio = browser.radio_set(id='new_user_newsletter_yes').radio()
        assert isinstance(radio, Radio)
        assert radio.value == 'yes'

    def test_returns_provided_instance_of_radio_if_element_has_no_name(self, browser):
        radio = browser.radio_set(id='new_user_newsletter_absolutely').radio()
        assert isinstance(radio, Radio)
        assert radio.value == 'absolutely'

    def test_returns_an_instance_of_radio_matching_the_provided_value(self, browser):
        radio = browser.radio_set(id='new_user_newsletter_yes').radio(id='new_user_newsletter_no')
        assert isinstance(radio, Radio)
        assert radio.value == 'no'

    def test_does_not_exist_when_using_bad_locator(self, browser):
        assert not browser.radio_set(id='new_user_newsletter_yes').radio(id='new_user_newsletter_not_there').exists

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_it_specifies_the_wrong_name(self, browser):
        radio_set = browser.radio_set(id='new_user_newsletter_yes')
        with pytest.raises(UnknownObjectException):
            radio_set.radio(name='')
        with pytest.raises(UnknownObjectException):
            radio_set.radio(name='foo')


class TestRadioSetRadios(object):
    def test_returns_list_of_all_radios_in_the_set_if_no_arguments_specfiied(self, browser):
        radios = browser.radio_set(id='new_user_newsletter_yes').radios()
        assert isinstance(radios, RadioCollection)
        assert [r.value for r in radios] == ['yes', 'no', 'certainly', 'nah', 'nah']

    def test_returns_radio_collection_matching_the_provided_value(self, browser):
        radios = browser.radio_set(id='new_user_newsletter_yes').radios(id=compile(r'new_user_newsletter_n'))
        assert isinstance(radios, RadioCollection)
        assert [r.value for r in radios] == ['no', 'nah']

    def test_returns_provided_instance_of_radios_if_element_has_no_name(self, browser):
        radios = browser.radio_set(id='new_user_newsletter_absolutely').radios()
        assert isinstance(radios, RadioCollection)
        assert len(radios) == 1
        assert radios[0].value == 'absolutely'

    def test_returns_empty_collection_if_specified_radio_does_not_exist(self, browser):
        assert len(browser.radio_set(id='new_user_newsletter_yes').radios(id='new_user_newsletter_not_there')) == 0

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_it_specifies_the_wrong_name(self, browser):
        radio_set = browser.radio_set(id='new_user_newsletter_yes')
        with pytest.raises(UnknownObjectException):
            radio_set.radios(name='')


class TestRadioSetSelected(object):
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_it_the_radio_set_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(name='no_such_name').selected

    def test_gets_the_currently_selected_radio(self, browser):
        assert browser.radio_set(id='new_user_newsletter_no').selected.text == 'Yes'
        assert browser.radio_set(id='new_user_newsletter_no').selected.value == 'yes'


class TestRadioSetIncludes(object):
    def test_returns_true_if_the_given_radio_exists_by_text(self, browser):
        assert browser.radio_set(id='new_user_newsletter_no').includes('Yes') is True

    def test_returns_false_if_the_given_radio_doesnt_exist(self, browser):
        assert browser.radio_set(id='new_user_newsletter_no').includes('Mother') is False


class TestRadioSetIsSelected(object):
    def test_returns_true_if_the_given_radio_is_selected_by_text(self, browser):
        browser.radio_set(id='new_user_newsletter_yes').select('No')
        assert browser.radio_set(id='new_user_newsletter_yes').is_selected('No') is True

    def test_returns_false_if_the_given_radio_is_not_selected_by_text(self, browser):
        assert browser.radio_set(id='new_user_newsletter_no').is_selected('Probably') is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_is_selected_if_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(id='new_user_newsletter_yes').is_selected('missing_option')


class TestRadioSetIsSelect(object):
    def test_selects_radio_text_by_string(self, browser):
        browser.radio_set(id='new_user_newsletter_yes').select('Probably')
        assert browser.radio_set(id='new_user_newsletter_yes').selected.text == 'Probably'

    def test_selects_radio_text_by_regexp(self, browser):
        browser.radio_set(id='new_user_newsletter_yes').select(compile(r'Prob'))
        assert browser.radio_set(id='new_user_newsletter_yes').selected.text == 'Probably'

    def test_selects_radio_text_when_given_an_xpath(self, browser):
        browser.radio_set(xpath="//input[@id='new_user_newsletter_no']").select('Probably')
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_no']").selected.text == 'Probably'

    def test_selects_radio_value_by_string(self, browser):
        browser.radio_set(id='new_user_newsletter_yes').select('no')
        assert browser.radio_set(id='new_user_newsletter_yes').selected.text == 'No'

    def test_selects_radio_value_by_regexp(self, browser):
        browser.radio_set(id='new_user_newsletter_yes').select(compile(r'nah'))
        assert browser.radio_set(id='new_user_newsletter_yes').selected.text == 'Probably'

    def test_returns_the_value_selected(self, browser):
        assert browser.radio_set(id='new_user_newsletter_yes').select('no') == 'no'

    def test_fires_onchange_event_when_selecting_a_radio(self, browser, messages):
        browser.radio_set(id='new_user_newsletter_yes').radio(value='certainly').set()
        assert messages.list == ['changed: new_user_newsletter']

        browser.radio_set(id='new_user_newsletter_yes').radio(value='certainly').set()
        assert messages.list == ['changed: new_user_newsletter']  # no event fired here - didn't change

        browser.radio_set(id='new_user_newsletter_yes').radio(value='yes').set()
        browser.radio_set(id='new_user_newsletter_yes').radio(value='certainly').set()
        assert messages.list == ['changed: new_user_newsletter', 'clicked: new_user_newsletter_yes',
                                 'changed: new_user_newsletter']

    def test_doesnt_fire_onchange_event_when_selecting_an_already_selected_radio(self, browser, messages):
        browser.radio_set(id='new_user_newsletter_yes').radio(value='no').set()

        browser.radio_set(id='new_user_newsletter_yes').radio(value='no').set()
        assert len(messages) == 1

        browser.radio_set(id='new_user_newsletter_yes').radio(value='no').set()
        assert len(messages) == 1

    def test_returns_the_text_of_the_selected_radio(self, browser):
        assert browser.radio_set(id='new_user_newsletter_yes').select('No') == 'No'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.radio_set(id='new_user_newsletter_yes').select('missing_option')
        with pytest.raises(UnknownObjectException):
            browser.radio_set(id='new_user_newsletter_yes').select(compile(r'missing_option'))

    def test_raises_correct_exception_if_the_element_is_disabled(self, browser):
        with pytest.raises(ObjectDisabledException):
            browser.radio_set(id='new_user_newsletter_none').select('None')

    def test_raises_correct_exception_if_the_argument_is_not_a_string_regexp_int(self, browser):
        with pytest.raises(TypeError):
            browser.radio_set(id='new_user_newsletter_yes').select([])


class TestRadioSetEqual(object):
    def test_returns_true_when_located_by_any_radio_button(self, browser):
        rs = browser.radio_set(id='new_user_newsletter_yes')
        assert browser.radio_set(id=compile(r'new_user_newsletter_no')) == rs
        assert browser.radio_set(name="new_user_newsletter", index=2) == rs
        assert browser.radio_set(name=compile(r'new_user_newsletter')) == rs
        assert browser.radio_set(value="yes") == rs
        assert browser.radio_set(value=compile(r'yes')) == rs
        assert browser.radio_set(class_name="huge") == rs
        assert browser.radio_set(class_name=compile(r'huge')) == rs
        assert browser.radio_set(index=0) == rs
        assert browser.radio_set(xpath="//input[@id='new_user_newsletter_probably']") == rs
