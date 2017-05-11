import pytest
from re import compile

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestCheckboxExist(object):
    def test_returns_true_if_the_checkbox_button_exists(self, browser):
        assert browser.checkbox(id='new_user_interests_books').exists
        assert browser.checkbox(id=compile(r'new_user_interests_books')).exists
        assert browser.checkbox(name='new_user_interests').exists
        assert browser.checkbox(name=compile(r'new_user_interests')).exists
        assert browser.checkbox(value='books').exists
        assert browser.checkbox(value=compile(r'books')).exists
        assert browser.checkbox(class_name='fun').exists
        assert browser.checkbox(class_name=compile(r'fun')).exists
        assert browser.checkbox(xpath="//input[@id='new_user_interests_books']").exists

    def test_returns_true_if_the_checkbox_button_exists_by_name_and_value(self, browser):
        assert browser.checkbox(name='new_user_interests', value='cars').exists
        assert browser.checkbox(xpath="//input[@name='new_user_interests' and @value='cars']").exists

    def test_returns_the_first_checkbox_if_given_no_args(self, browser):
        assert browser.checkbox().exists

    def test_returns_false_if_the_checkbox_button_does_not_exist(self, browser):
        assert not browser.checkbox(id='no_such_id').exists
        assert not browser.checkbox(id=compile(r'no_such_id')).exists
        assert not browser.checkbox(name='no_such_name').exists
        assert not browser.checkbox(name=compile(r'no_such_name')).exists
        assert not browser.checkbox(value='no_such_value').exists
        assert not browser.checkbox(value=compile(r'no_such_value')).exists
        assert not browser.checkbox(text='no_such_text').exists
        assert not browser.checkbox(text=compile(r'no_such_text')).exists
        assert not browser.checkbox(class_name='no_such_class').exists
        assert not browser.checkbox(class_name=compile(r'no_such_class')).exists
        assert not browser.checkbox(index=1337).exists
        assert not browser.checkbox(xpath="//input[@id='no_such_id']").exists

    def test_returns_false_if_the_checkbox_button_doesnt_exist_by_name_and_value(self, browser):
        assert not browser.checkbox(name='new_user_interests', value='no_such_value').exists
        assert not browser.checkbox(xpath="//input[@name='new_user_interests' and "
                                          "@value='no_such_value']").exists
        assert not browser.checkbox(name='no_such_name', value='cars').exists
        assert not browser.checkbox(xpath="//input[@name='no_such_name' and @value='cars']").exists

    def test_returns_true_for_checkboxes_with_a_string_value(self, browser):
        assert browser.checkbox(name='new_user_interests', value='books').exists
        assert browser.checkbox(name='new_user_interests', value='cars').exists

    def test_returns_true_for_checkbox_with_upper_case_type(self, browser):
        assert browser.checkbox(id='new_user_interests_draw').exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.checkbox(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from watir_snake.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.checkbox(no_such_how='some_value').exists


class TestCheckboxAttributes(object):
    # class_name
    def test_returns_the_class_name_if_the_checkbox_exists_and_has_class_name(self, browser):
        assert browser.checkbox(id='new_user_interests_dancing').class_name == 'fun'

    def test_returns_an_empty_string_if_the_checkbox_exists_and_has_no_class_name(self, browser):
        assert browser.checkbox(id='new_user_interests_books').class_name == ''

    def test_raises_correct_exception_for_idif_the_checkbox_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(id='no_such_id').class_name

    # id
    def test_returns_the_id_if_the_checkbox_exists_and_has_id(self, browser):
        assert browser.checkbox(index=0).id == 'new_user_interests_books'

    def test_returns_an_empty_string_if_the_checkbox_exists_and_has_no_id(self, browser):
        assert browser.checkbox(index=1).id == ''

    def test_raises_correct_exception_for_id_if_the_checkbox_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(index=1337).id

    # name
    def test_returns_the_name_if_the_checkbox_exists_and_has_name(self, browser):
        assert browser.checkbox(id='new_user_interests_books').name == 'new_user_interests'

    def test_returns_an_empty_string_if_the_checkbox_exists_and_has_no_name(self, browser):
        assert browser.checkbox(id='new_user_interests_food').name == ''

    def test_raises_correct_exception_for_name_if_the_checkbox_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(index=1337).name

    # title
    def test_returns_the_title_if_the_checkbox_exists_and_has_title(self, browser):
        assert browser.checkbox(id='new_user_interests_dancing').title == 'Dancing is fun!'

    def test_returns_an_empty_string_if_the_checkbox_exists_and_has_no_title(self, browser):
        assert browser.checkbox(id='new_user_interests_books').title == ''

    def test_raises_correct_exception_for_title_if_the_checkbox_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(index=1337).title

    # type
    def test_returns_the_type_if_the_checkbox_exists(self, browser):
        assert browser.checkbox(index=0).type == 'checkbox'

    def test_raises_correct_exception_for_type_if_the_checkbox_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(index=1337).type

    # value
    def test_returns_the_value_if_the_checkbox_exists(self, browser):
        assert browser.checkbox(id='new_user_interests_books').value == 'books'

    def test_raises_correct_exception_for_value_if_the_checkbox_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(index=1337).value


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.checkbox(index=0), 'class_name')
    assert hasattr(browser.checkbox(index=0), 'id')
    assert hasattr(browser.checkbox(index=0), 'name')
    assert hasattr(browser.checkbox(index=0), 'title')
    assert hasattr(browser.checkbox(index=0), 'type')
    assert hasattr(browser.checkbox(index=0), 'value')


class TestCheckboxEnabled(object):
    # enabled
    def test_returns_true_if_the_checkbox_button_is_enabled(selfself, browser):
        assert browser.checkbox(id='new_user_interests_books').enabled
        assert browser.checkbox(xpath="//input[@id='new_user_interests_books']").enabled

    def test_returns_false_if_the_checkbox_button_is_disabled(self, browser):
        assert not browser.checkbox(id='new_user_interests_dentistry').enabled
        assert not browser.checkbox('xpath', "//input[@id='new_user_interests_dentistry']").enabled

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'xpath': "//input[@id='no_such_id']"}])
    def test_raises_correct_exception_for_enabled_if_the_checkbox_button_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(**selector).enabled

    # disabled
    def test_returns_true_if_the_checkbox_is_disabled(self, browser):
        assert browser.checkbox(id='new_user_interests_dentistry').disabled

    def test_returns_false_if_the_checkbox_is_enabled(self, browser):
        assert not browser.checkbox(id='new_user_interests_books').disabled

    def test_raises_correct_exception_for_disabled_if_the_checkbox_button_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(index=1337).disabled


class TestCheckboxManipulation(object):
    # clear
    @pytest.mark.parametrize('selector',
                             [{'id': 'new_user_interests_dentistry'},
                              {'xpath': "//input[@id='new_user_interests_dentistry']"}])
    def test_raises_correct_exception_for_clear_if_the_checkbox_is_disabled(self, browser, selector):
        from watir_snake.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            assert not browser.checkbox(id='new_user_interests_dentistry').is_set
            browser.checkbox(**selector).clear()

    def test_clears_the_checkbox_button_if_it_is_set(self, browser):
        browser.checkbox(id='new_user_interests_books').clear()
        assert not browser.checkbox(id='new_user_interests_books').is_set

    def test_clears_the_checkbox_button_when_found_by_xpath(self, browser):
        browser.checkbox(xpath="//input[@id='new_user_interests_books']").clear()
        assert not browser.checkbox(xpath="//input[@id='new_user_interests_books']").is_set

    @pytest.mark.parametrize('selector',
                             [{'name': 'no_such_name'},
                              {'xpath': "//input[@id='no_such_name']"}])
    def test_raises_correct_exception_for_clear_if_the_checkbox_button_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(**selector).clear()

    # set
    def test_sets_the_checkbox_button(self, browser):
        browser.checkbox(id='new_user_interests_cars').set()
        assert browser.checkbox(id='new_user_interests_cars').is_set

    def test_sets_the_checkbox_button_when_found_by_xpath(self, browser):
        browser.checkbox(xpath="//input[@id='new_user_interests_cars']").set()
        assert browser.checkbox(xpath="//input[@id='new_user_interests_cars']").is_set

    def test_fires_the_onclick_event(self, browser):
        assert browser.button(id='disabled_button').disabled
        browser.checkbox(id='toggle_button_checkbox').set()
        assert not browser.button(id='disabled_button').disabled
        browser.checkbox(id='toggle_button_checkbox').clear()
        assert browser.button(id='disabled_button').disabled

    @pytest.mark.parametrize('selector',
                             [{'name': 'no_such_name'},
                              {'xpath': "//input[@id='no_such_name']"}])
    def test_raises_correct_exception_for_set_if_the_checkbox_button_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(**selector).set()

    @pytest.mark.parametrize('selector',
                             [{'id': 'new_user_interests_dentistry'},
                              {'xpath': "//input[@id='new_user_interests_dentistry']"}])
    def test_raises_correct_exception_for_set_if_the_checkbox_is_disabled(self, browser, selector):
        from watir_snake.exception import ObjectDisabledException
        with pytest.raises(ObjectDisabledException):
            browser.checkbox(**selector).set()

    # is_set
    def test_returns_true_if_the_checkbox_button_is_set(self, browser):
        assert browser.checkbox(id='new_user_interests_books').is_set

    def test_returns_false_if_the_checkbox_button_unset(self, browser):
        assert not browser.checkbox(id='new_user_interests_cars').is_set

    def test_returns_the_state_for_checkboxes_with_string_values(self, browser):
        assert not browser.checkbox(name='new_user_interests', value='cars').is_set
        browser.checkbox(name='new_user_interests', value='cars').set()
        assert browser.checkbox(name='new_user_interests', value='cars').is_set
        browser.checkbox(name='new_user_interests', value='cars').clear()
        assert not browser.checkbox(name='new_user_interests', value='cars').is_set

    @pytest.mark.parametrize('selector',
                             [{'name': 'no_such_name'},
                              {'xpath': "//input[@id='no_such_name']"}])
    def test_raises_correct_exception_for_is_set_if_the_checkbox_button_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.checkbox(**selector).is_set
