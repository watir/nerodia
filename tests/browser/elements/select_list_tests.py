import re

import pytest

import nerodia
from nerodia.exception import Error, NoValueFoundException, UnknownObjectException


@pytest.fixture
def reset_form(browser_manager):
    yield
    browser_manager.instance.link().click()


pytestmark = [pytest.mark.page('forms_with_input_elements.html'),
              pytest.mark.usefixtures('reset_form')]


class TestSelectListExists(object):
    def test_returns_true_if_the_select_list_exists(self, browser):
        assert browser.select_list(id='new_user_country').exists is True
        assert browser.select_list(id=re.compile('new_user_country')).exists is True
        assert browser.select_list(name='new_user_country').exists is True
        assert browser.select_list(name=re.compile('new_user_country')).exists is True
        assert browser.select_list(class_name='country').exists is True
        assert browser.select_list(class_name=re.compile('country')).exists is True
        assert browser.select_list(index=0).exists is True
        assert browser.select_list(xpath="//select[@id='new_user_country']").exists is True

    def test_returns_the_first_select_list_if_given_no_args(self, browser):
        assert browser.select_list().exists

    def test_returns_false_if_the_select_list_doesnt_exist(self, browser):
        assert browser.select_list(id='no_such_id').exists is False
        assert browser.select_list(id=re.compile('no_such_id')).exists is False
        assert browser.select_list(name='no_such_name').exists is False
        assert browser.select_list(name=re.compile('no_such_name')).exists is False
        assert browser.select_list(value='no_such_value').exists is False
        assert browser.select_list(value=re.compile('no_such_value')).exists is False
        assert browser.select_list(text='no_such_text').exists is False
        assert browser.select_list(text=re.compile('no_such_id')).exists is False
        assert browser.select_list(class_name='no_such_class').exists is False
        assert browser.select_list(class_name=re.compile('no_such_class')).exists is False
        assert browser.select_list(index=1337).exists is False
        assert browser.select_list(xpath="//select[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.select_list(id=3.14).exists


class TestSelectListAttributes(object):
    # id
    def test_returns_the_id_if_the_select_list_exists_and_has_id(self, browser):
        assert browser.select_list(index=0).id == 'new_user_country'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(index=1337).id

    # name
    def test_returns_the_name_if_the_select_list_exists_and_has_name(self, browser):
        assert browser.select_list(index=0).name == 'new_user_country'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_name_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(index=1337).name

    # multiple
    def test_knows_whether_the_select_list_allows_multiple_selections(self, browser):
        assert not browser.select_list(index=0).multiple
        assert browser.select_list(index=1).multiple

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_multiple_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(index=1337).multiple

    # value
    def test_returns_the_value_if_the_select_list_exists_and_has_value(self, browser):
        browser.select_list(index=0).select(re.compile('Norway'))
        assert browser.select_list(index=0).value == '2'
        browser.select_list(index=0).select(re.compile('Sweden'))
        assert browser.select_list(index=0).value == '3'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_value_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(index=1337).value

    # text
    def test_returns_the_text_if_the_select_list_exists_and_has_text(self, browser):
        browser.select_list(index=0).select(re.compile('Norway'))
        assert browser.select_list(index=0).text == 'Norway'
        browser.select_list(index=0).select(re.compile('Sweden'))
        assert browser.select_list(index=0).text == 'Sweden'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(index=1337).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.select_list(index=0), 'class_name')
    assert hasattr(browser.select_list(index=0), 'id')
    assert hasattr(browser.select_list(index=0), 'name')
    assert hasattr(browser.select_list(index=0), 'value')


class TestSelectListAccess(object):
    # enabled
    def test_returns_true_if_the_select_list_is_enabled(self, browser):
        assert browser.select_list(name='new_user_country').enabled is True

    def test_returns_false_if_the_select_list_is_disabled(self, browser):
        assert browser.select_list(name='new_user_role').enabled is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_enabled_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(name='no_such_name').enabled

    # disabled
    def test_returns_true_if_the_select_list_is_disabled(self, browser):
        assert browser.select_list(index=2).disabled is True

    def test_returns_false_if_the_select_list_is_enabled(self, browser):
        assert browser.select_list(index=0).disabled is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_disabled_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(index=1337).disabled


class TestSelectListOther(object):
    # option
    def test_returns_an_instance_of_option(self, browser):
        from nerodia.elements.option import Option
        option = browser.select_list(name='new_user_country').option(text='Denmark')
        assert isinstance(option, Option)
        assert option.value == '1'

    # options
    def test_returns_all_the_options(self, browser):
        options = browser.select_list(name='new_user_country').options()
        assert [opt.text for opt in options] == ['Denmark', 'Norway', 'Sweden',
                                                 'United Kingdom', 'USA', 'Germany']

    # selected_options
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_selected_options_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(name='no_such_name').selected_options

    def test_returns_the_currently_selected_items(self, browser):
        selected = browser.select_list(name='new_user_country').selected_options
        assert [opt.text for opt in selected] == ['Norway']
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    # clear
    def test_clears_the_selection_when_possible(self, browser):
        browser.select_list(name='new_user_languages').clear()
        assert not browser.select_list(name='new_user_languages').selected_options

    def test_does_not_clear_selections_if_the_select_list_does_not_allow_multiple_selections(self, browser):
        with pytest.raises(Error):
            browser.select_list(name='new_user_country').clear()
        opts = browser.select_list(name='new_user_country').selected_options
        assert [opt.text for opt in opts] == ['Norway']

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_clear_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(name='no_such_name').clear()

    def test_clear_fires_onchange_event(self, browser, messages):
        browser.select_list(name='new_user_languages').clear()
        assert len(messages.list) == 2

    def test_clear_doesnt_fire_onchange_event_for_already_cleared_option(self, browser, messages):
        browser.select_list(name='new_user_languages').option().clear()
        assert len(messages.list) == 0

    # include
    def test_returns_true_if_the_given_option_exists_by_text(self, browser):
        assert browser.select_list(name='new_user_country').includes('Denmark') is True

    def test_returns_true_if_the_given_option_exists_by_label(self, browser):
        assert browser.select_list(name='new_user_country').includes('Germany') is True

    def test_returns_false_if_the_given_option_doesnt_exist(self, browser):
        assert browser.select_list(name='new_user_country').includes('Ireland') is False

    # is_selected
    def test_returns_true_if_the_given_option_is_selected_by_text(self, browser):
        browser.select_list(name='new_user_country').select('Denmark')
        assert browser.select_list(name='new_user_country').is_selected('Denmark') is True

    def test_returns_false_if_the_given_option_is_not_selected_by_text(self, browser):
        assert browser.select_list(name='new_user_country').is_selected('Sweden') is False

    def test_returns_true_if_the_given_option_is_selected_by_label(self, browser):
        browser.select_list(name='new_user_country').select('Germany')
        assert browser.select_list(name='new_user_country').is_selected('Germany') is True

    def test_returns_false_if_the_given_option_is_not_selected_by_label(self, browser):
        browser.select_list(name='new_user_country').option(label='Germany').clear()
        assert browser.select_list(name='new_user_country').is_selected('Germany') is False

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_selected_if_the_select_list_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.select_list(name='new_user_country').is_selected('missing_option')


class TestSelectListSelect(object):
    # finding by value

    def test_selects_an_option_by_value_with_a_string(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select('2')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN']

    def test_selects_an_option_by_value_with_a_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select(re.compile(r'1|3'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'NO']

    # finding by text

    def test_selects_an_option_by_text_with_a_string(self, browser):
        browser.select_list(name='new_user_country').select('Denmark')
        selected = browser.select_list(name='new_user_country').selected_options
        assert [opt.text for opt in selected] == ['Denmark']

    def test_selects_an_option_by_text_with_a_regexp(self, browser):
        browser.select_list(name='new_user_country').select(re.compile(r'Denmark'))
        selected = browser.select_list(name='new_user_country').selected_options
        assert [opt.text for opt in selected] == ['Denmark']

    # finding by label

    def test_selects_an_option_by_label_with_a_string(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select('NO')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['NO']

    def test_selects_an_option_by_label_with_a_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select(re.compile(r'^N'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['NO']

    def test_selects_multiple_options_successively(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select('Danish')
        browser.select_list(name='new_user_languages').select('Swedish')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'Swedish']

    def test_selects_empty_options(self, browser):
        browser.select_list(id='delete_user_username').select('')
        selected = browser.select_list(name='delete_user_username').selected_options
        assert [opt.text for opt in selected] == ['']

    def test_returns_the_value_selected(self, browser):
        assert browser.select_list(name='new_user_languages').select('Danish') == 'Danish'

    def test_fires_onchange_event_when_selecting_an_item(self, browser, messages):
        browser.select_list(id='new_user_languages').select('Danish')
        assert messages.list == ['changed language']

    def test_doesnt_fires_onchange_event_when_selecting_an_item(self, browser, messages):
        browser.select_list(id='new_user_languages').clear()  # removes the two pre-selected options
        browser.select_list(id='new_user_languages').select('English')
        assert len(messages) == 3

        browser.select_list(id='new_user_languages').select('English')
        assert len(messages) == 3

    def test_an_empty_string_when_selecting_an_option_that_disappears_when_selected(self, browser):
        assert browser.select_list(id='obsolete').select('sweden') == ''

    def test_selects_options_with_a_single_quoted_value(self, browser):
        browser.select_list(id='single-quote').select("'foo'")
        selected = browser.select_list(id='single-quote').selected_options
        assert [opt.text for opt in selected] == ["'foo'"]

    @pytest.mark.skipif('nerodia.relaxed_locate is False',
                        reason='only applicable when relaxed locating')
    @pytest.mark.usefixtures('timeout_reset')
    @pytest.mark.page('wait.html')
    def test_waits_to_select_an_option(self, browser):
        from time import time
        browser.link(id='add_select').click()
        select_list = browser.select_list(id='languages')
        nerodia.default_timeout = 2
        start_time = time()
        with pytest.raises(NoValueFoundException):
            select_list.select('No')
        assert time() - start_time > 2

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_option_doesnt_exist(self, browser):
        message_parts = ["#<Select: located: False;",
                         "'name': 'new_user_country'",
                         "'tag_name': 'select'"]
        with pytest.raises(NoValueFoundException) as e:
            browser.select_list(name='new_user_country').select('missing_option')
        assert all(part in e.value.args[0] for part in message_parts)

        message_parts = ["#<Select: located: False;",
                         "'name': {}".format(re.compile('new_user_country')),
                         "'tag_name': 'select'"]
        with pytest.raises(NoValueFoundException) as e:
            browser.select_list(name=re.compile('new_user_country')).select('missing_option')
        assert all(part in e.value.args[0] for part in message_parts)

    # This test doesn't like quick timeout
    def test_raises_correct_exception_if_the_option_is_disabled(self, browser):
        from nerodia.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            browser.select_list(name='new_user_languages').select('Russian')

    def test_raises_correct_exception_if_argument_is_not_a_string_regexp_numeric_list(self, browser):
        with pytest.raises(TypeError):
            browser.select_list(name='new_user_languages').select({})


class TestSelectListSelectMultipleOptions():

    def test_selects_each_item_in_a_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select(['Danish', 'Swedish'])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'Swedish']

    def test_selects_each_item_in_a_parameter_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select('Danish', 'Swedish')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'Swedish']

    def test_selects_each_item_based_on_text(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select([re.compile(r'ish')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish']

    def test_selects_each_item_based_on_label_and_single_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select([re.compile(r'NO|EN')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    def test_selects_each_item_based_on_label_and_multiple_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select([re.compile(r'NO'),
                                                               re.compile(r'EN')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    def test_selects_each_item_from_a_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select([re.compile(r'ish'),
                                                               re.compile(r'Latin')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin',
                                                  'Latin']

    def test_selects_each_item_from_multiple_arguments(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select(re.compile(r'ish'),
                                                              re.compile(r'Latin'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin',
                                                  'Latin']

    def test_returns_the_first_matching_value_if_there_are_multiple_matches(self, browser):
        browser.select_list(name='new_user_languages').clear()
        selected = browser.select_list(name='new_user_languages').select([re.compile(r'ish')])
        assert selected == 'Danish'


class TestSelectListJsSelectMultipleOptions():

    def test_selects_each_item_in_a_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select(['Danish', 'Swedish'])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'Swedish']

    def test_selects_each_item_in_a_parameter_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select('Danish', 'Swedish')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'Swedish']

    def test_selects_each_item_based_on_text(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select([re.compile(r'ish')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish']

    def test_selects_each_item_based_on_label_and_single_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select([re.compile(r'NO|EN')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    def test_selects_each_item_based_on_label_and_multiple_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select([re.compile(r'NO'),
                                                                 re.compile(r'EN')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    def test_selects_each_item_from_a_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select([re.compile(r'ish'),
                                                                 re.compile(r'Latin')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin',
                                                  'Latin']

    def test_selects_each_item_from_multiple_arguments(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select(re.compile(r'ish'),
                                                                 re.compile(r'Latin'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin',
                                                  'Latin']

    def test_returns_the_first_matching_value_if_there_are_multiple_matches(self, browser):
        browser.select_list(name='new_user_languages').clear()
        selected = browser.select_list(name='new_user_languages').js_select([re.compile(r'ish')])
        assert selected == 'Danish'


class TestSelectListJsSelect(object):
    # finding by value

    def test_js_selects_an_option_by_value_with_a_string(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select('2')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN']

    def test_js_selects_an_option_by_value_with_a_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select(re.compile(r'2'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN']

    # finding by text

    def test_js_selects_an_option_by_text_with_a_string(self, browser):
        browser.select_list(name='new_user_country').js_select('Denmark')
        selected = browser.select_list(name='new_user_country').selected_options
        assert [opt.text for opt in selected] == ['Denmark']

    def test_js_selects_an_option_by_text_with_a_regexp(self, browser):
        browser.select_list(name='new_user_country').js_select(re.compile(r'Denmark'))
        selected = browser.select_list(name='new_user_country').selected_options
        assert [opt.text for opt in selected] == ['Denmark']

    # finding by label

    def test_js_selects_an_option_by_label_with_a_string(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select('NO')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['NO']

    def test_js_selects_an_option_by_label_with_a_regexp(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select(re.compile(r'NO'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['NO']

    def test_js_selects_multiple_options_successively(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select('Danish')
        browser.select_list(name='new_user_languages').js_select('Swedish')
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'Swedish']

    def test_js_selects_empty_options(self, browser):
        browser.select_list(id='delete_user_username').js_select('')
        selected = browser.select_list(name='delete_user_username').selected_options
        assert [opt.text for opt in selected] == ['']

    def test_returns_the_value_js_selected(self, browser):
        assert browser.select_list(name='new_user_languages').js_select('Danish') == 'Danish'

    def test_js_selects_options_with_a_single_quoted_value(self, browser):
        browser.select_list(id='single-quote').js_select("'foo'")
        selected = browser.select_list(id='single-quote').selected_options
        assert [opt.text for opt in selected] == ["'foo'"]

    def test_selects_exact_matches_when_using_string(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select('Latin')
        selected_options = [el.text for el in browser.select_list(name='new_user_languages').selected_options]
        assert 'Azeri - Latin' not in selected_options
        assert 'Latin' in selected_options

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_option_doesnt_exist(self, browser):
        with pytest.raises(NoValueFoundException):
            browser.select_list(name='new_user_country').js_select('missing_option')
        with pytest.raises(NoValueFoundException):
            browser.select_list(name=re.compile('new_user_country')).js_select('missing_option')

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_option_is_disabled(self, browser):
        from nerodia.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            browser.select_list(name='new_user_languages').js_select('Russian')

    def test_raises_correct_exception_if_argument_is_not_a_string_regexp_numeric_list(self, browser):
        with pytest.raises(TypeError):
            browser.select_list(name='new_user_languages').js_select({})


class TestSelectListSelectAll(object):
    def test_selects_multiple_options_based_on_text(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select_all(re.compile(r'ish'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish']

    def test_selects_multiple_options_based_on_labels(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select_all(re.compile(r'NO|EN'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    def test_selects_all_options_in_a_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select_all([re.compile(r'ish'), re.compile(r'Latin')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin', 'Latin']

    def test_selects_all_options_in_a_parameter_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').select_all(re.compile(r'ish'), re.compile(r'Latin'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin', 'Latin']

    def test_returns_the_first_matching_value_if_there_are_multiple_matches(self, browser):
        browser.select_list(name='new_user_languages').clear()
        assert browser.select_list(name='new_user_languages').select_all(re.compile(r'ish')) == 'Danish'


class TestSelectListJsSelectAll(object):
    def test_selects_multiple_options_based_on_value(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select_all(re.compile(r'\d+'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'NO', 'Russian']

    def test_selects_multiple_options_based_on_text(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select_all(re.compile(r'ish'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish']

    def test_selects_multiple_options_based_on_labels(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select_all(re.compile(r'NO|EN'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['EN', 'NO']

    def test_selects_all_options_in_a_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select_all([re.compile(r'ish'), re.compile(r'Latin')])
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin', 'Latin']

    def test_selects_all_options_in_a_parameter_list(self, browser):
        browser.select_list(name='new_user_languages').clear()
        browser.select_list(name='new_user_languages').js_select_all(re.compile(r'ish'), re.compile(r'Latin'))
        selected = browser.select_list(name='new_user_languages').selected_options
        assert [opt.text for opt in selected] == ['Danish', 'EN', 'Swedish', 'Azeri - Latin', 'Latin']

    def test_returns_the_first_matching_value_if_there_are_multiple_matches(self, browser):
        browser.select_list(name='new_user_languages').clear()
        assert browser.select_list(name='new_user_languages').js_select_all(re.compile(r'ish')) == 'Danish'
