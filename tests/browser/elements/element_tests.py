from platform import system
from re import compile

import pytest
import six
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException
from selenium.webdriver.common.keys import Keys

from nerodia.exception import LocatorException, UnknownObjectException
from nerodia.window import Dimension, Point

pytestmark = pytest.mark.page('forms_with_input_elements.html')

MODIFIER = Keys.COMMAND if system().lower() == 'darwin' else Keys.CONTROL


class TestElementInit(object):
    def test_finds_elements_matching_the_conditions_when_given_a_dict_of_how_what_arguments(self, browser):
        assert browser.checkbox(name='new_user_interests',
                                title='Dancing is fun!').value == 'dancing'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_with_a_sane_error_message_when_given_a_dict_of_how_what_arguments(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.text_field(index=100, name='foo').id

    def test_raises_correct_exception_if_given_the_wrong_number_of_arguments(self):
        from nerodia.elements.element import Element
        with pytest.raises(TypeError):
            Element('container', 1, 2, 3, 4)
        with pytest.raises(TypeError):
            Element('container', 'foo')


@pytest.mark.page('definition_lists.html')
class TestElementEqual(object):
    def test_returns_true_if_the_two_elements_point_to_the_same_dom_element(self, browser):
        a = browser.dl(id='experience-list')
        b = browser.dl()

        assert a == b
        assert a.eql(b)

    def test_returns_false_if_the_two_elements_are_not_the_same(self, browser):
        a = browser.dls()[0]
        b = browser.dls()[1]

        assert a != b
        assert not a.eql(b)

    def test_returns_false_if_the_other_object_is_not_an_element(self, browser):
        assert browser.dl() != 1


@pytest.mark.page('data_attributes.html')
class TestElementDataAttributes(object):
    def test_finds_elements_by_a_data_attribute(self, browser):
        assert browser.p(data_type='ruby-library').exists

    def test_returns_the_value_of_a_data_attribute(self, browser):
        assert browser.p().data_type == 'ruby-library'
        assert browser.dl() != 1


@pytest.mark.page('aria_attributes.html')
class TestElementAriaAttributes(object):
    def test_finds_elements_by_a_data_attribute(self, browser):
        assert browser.p(aria_label='ruby-library').exists

    def test_returns_the_value_of_a_data_attribute(self, browser):
        assert browser.p().aria_label == 'ruby-library'


@pytest.mark.page('non_control_elements.html')
class TestElementVisibleText(object):
    def test_finds_elements_by_visible_text(self, browser):
        assert browser.element(visible_text='all visible').exists is True
        assert browser.element(visible_text=compile(r'all visible')).exists is True
        assert browser.element(visible_text='some visible').exists is True
        assert browser.element(visible_text=compile(r'some visible')).exists is True
        assert browser.element(visible_text='none visible').exists is False
        assert browser.element(visible_text=compile(r'none visible')).exists is False
        assert browser.element(visible_text='Link 2', class_name='external').exists is True
        assert browser.element(visible_text=compile(r'Link 2'), class_name='external').exists is True

    def test_raises_exception_unless_value_is_a_string_or_regexp(self, browser):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            browser.link(visible_text=7).exists
            browser.element(visible_text=7).exists
        assert e.value.args[0] == msg


class TestElementWithoutTagName(object):
    def test_finds_an_element_without_arguments(self, browser):
        assert browser.element().exists

    def test_finds_an_element_by_xpath(self, browser):
        assert browser.element(xpath="//*[@for='new_user_first_name']").exists

    def test_finds_an_element_by_arbitrary_attribute(self, browser):
        assert browser.element(title='no title').exists

    def test_finds_several_elements_by_xpath(self, browser):
        assert len(browser.elements(xpath="//a")) == 1

    def test_finds_several_elements_by_arbitrary_attribute(self, browser):
        assert len(browser.elements(id=compile(r'^new_user'))) == 33

    def test_finds_an_element_from_an_elements_subtree(self, browser):
        assert browser.fieldset().element(id='first_label').exists
        assert browser.field_set().element(id='first_label').exists

    def test_finds_several_elements_from_an_elements_subtree(self, browser):
        assert len(browser.fieldset().elements(xpath=".//label")) == 23


class TestElementSubtype(object):
    def test_returns_a_checkbox_instance(self, browser):
        from nerodia.elements.check_box import CheckBox
        assert isinstance(browser.input(xpath="//input[@type='checkbox']").to_subtype(), CheckBox)

    def test_returns_a_radio_instance(self, browser):
        from nerodia.elements.radio import Radio
        assert isinstance(browser.input(xpath="//input[@type='radio']").to_subtype(), Radio)

    def test_returns_a_button_instance(self, browser):
        from nerodia.elements.button import Button
        assert isinstance(browser.input(xpath="//input[@type='button']").to_subtype(), Button)
        assert isinstance(browser.input(xpath="//input[@type='submit']").to_subtype(), Button)
        assert isinstance(browser.input(xpath="//input[@type='reset']").to_subtype(), Button)
        assert isinstance(browser.input(xpath="//input[@type='image']").to_subtype(), Button)

    def test_returns_a_text_field_instance(self, browser):
        from nerodia.elements.text_field import TextField
        assert isinstance(browser.input(xpath="//input[@type='text']").to_subtype(), TextField)

    def test_returns_a_file_field_instance(self, browser):
        from nerodia.elements.file_field import FileField
        assert isinstance(browser.input(xpath="//input[@type='file']").to_subtype(), FileField)

    def test_returns_a_div_instance(self, browser):
        from nerodia.elements.html_elements import Div
        assert isinstance(browser.element(xpath="//*[@id='messages']").to_subtype(), Div)


class TestElementFocus(object):
    def test_fires_the_onfocus_event_for_the_given_element(self, browser):
        tf = browser.text_field(id='new_user_occupation')
        assert tf.value == 'Developer'
        tf.focus()
        assert browser.div(id='onfocus_test').text == 'changed by onfocus event'

    # TODO: xfail edge?
    def test_knows_if_the_element_is_focused(self, browser):
        assert browser.element(id='new_user_first_name').focused
        assert not browser.element(id='new_user_last_name').focused


class TestElementFireEvent(object):
    def test_should_fire_the_given_event(self, browser):
        assert browser.div(id='onfocus_test').text == ''
        browser.text_field(id='new_user_occupation').fire_event('onfocus')
        assert browser.div(id='onfocus_test').text == 'changed by onfocus event'


class TestElementVisibility(object):
    def test_returns_true_if_the_element_is_visible(self, browser, caplog):
        assert browser.text_field(id='new_user_email').visible
        assert 'WARNING  [visible_element]' in caplog.text

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_element_does_not_exist(self, browser, caplog):
        with pytest.raises(UnknownObjectException):
            browser.text_field(id='no_such_id').visible
        assert 'WARNING  [visible_element]' in caplog.text

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_element_is_stale(self, browser):
        element = browser.text_field(id='new_user_email')
        element.exists

        browser.refresh()

        assert element.stale
        with pytest.raises(UnknownObjectException):
            element.visible

    def test_returns_true_if_the_element_has_visibility_style_visible_even_if_parent_has_hidden(self, browser, caplog):
        assert browser.div(id='visible_child').visible
        assert 'WARNING  [visible_element]' in caplog.text

    def test_returns_false_if_the_element_is_input_element_where_type_eq_hidden(self, browser):
        assert not browser.hidden(id='new_user_interests_dolls').visible

    def test_returns_false_if_the_element_has_display_style_none(self, browser, caplog):
        assert not browser.div(id='changed_language').visible
        assert 'WARNING  [visible_element]' in caplog.text

    def test_returns_false_if_the_element_has_visibility_style_hidden(self, browser, caplog):
        assert not browser.div(id='wants_newsletter').visible
        assert 'WARNING  [visible_element]' in caplog.text

    def test_returns_false_if_one_of_the_parent_elements_is_hidden(self, browser, caplog):
        assert not browser.div(id='hidden_parent').visible
        assert 'WARNING  [visible_element]' in caplog.text


@pytest.mark.page('class_locator.html')
class TestElementExistsClassLocator(object):
    def test_matches_when_the_element_has_a_single_class(self, browser):
        e = browser.div(class_name='a')
        assert e.exists
        assert e.class_name == 'a'

    def test_matches_when_the_element_has_several_classes(self, browser):
        e = browser.div(class_name='b')
        assert e.exists
        assert e.class_name == 'a b c'

    def test_does_not_match_only_part_of_the_class_name(self, browser):
        assert not browser.div(class_name='bc').exists

    def test_matches_part_of_the_class_name_when_given_a_regexp(self, browser):
        assert browser.div(class_name=compile(r'c')).exists


@pytest.mark.page('class_locator.html')
class TestElementExistsMultipleClassLocator(object):
    def test_matches_when_the_element_has_a_single_class(self, browser):
        e = browser.div(class_name=['a'])
        assert e.exists
        assert e.class_name == 'a'

    def test_matches_a_non_ordered_subset(self, browser):
        e = browser.div(class_name=['c', 'a'])
        assert e.exists
        assert e.class_name == 'a b c'

    def test_matches_one_with_negation(self, browser):
        e = browser.div(class_name=['!a'])
        assert e.exists
        assert e.class_name == 'abc'

    def test_matches_multiple_with_negation(self, browser):
        e = browser.div(class_name=['a', '!c', 'b'])
        assert e.exists
        assert e.class_name == 'a b'


@pytest.mark.page('data_attributes.html')
class TestElementExistsAttributePresent(object):
    def test_find_element_by_attribute_presence(self, browser):
        assert browser.p(data_type=True).exists
        assert not browser.p(class_name=True).exists

    def test_find_element_by_attribute_absence(self, browser):
        assert not browser.p(data_type=False).exists
        assert browser.p(class_name=False).exists


@pytest.mark.page('data_attributes.html')
class TestElementExistsIndex(object):
    def test_finds_the_first_element_by_index_0(self, browser):
        assert browser.element(index=0).tag_name == 'html'

    def test_finds_the_second_element_by_index_1(self, browser):
        assert browser.element(index=1).tag_name == 'head'

    def test_finds_the_last_element_by_index_neg_1(self, browser):
        assert browser.element(index=-1).tag_name == 'div'


class TestElementExist(object):
    def test_doesnt_raise_when_called_on_nested_elements(self, browser):
        assert not browser.div(id='no_such_div').link(id='no_such_id').exists

    def test_raises_correct_exception_if_both_xpath_and_css_are_given(self, browser):
        message_parts = ["'xpath' and 'css' cannot be combined",
                         "'xpath': '//div'",
                         "'css': 'div'"]
        with pytest.raises(LocatorException) as e:
            browser.div(xpath='//div', css='div').exists
        assert all(part in e.value.args[0] for part in message_parts)

    def test_doesnt_raise_when_selector_with_xpath_has_index(self, browser):
        assert browser.div(xpath='//div', index=1).exists

    def test_doesnt_raise_when_selector_with_css_has_index(self, browser):
        assert browser.div(css='div', index=1).exists

    def test_finds_element_by_selenium_name_locator(self, browser):
        assert browser.element(name='new_user_first_name').exists
        assert browser.element(name=compile(r'new_user_first_name')).exists


@pytest.mark.page('keylogger.html')
class TestElementSendKeys(object):
    def test_sends_keystrokes_to_the_element(self, browser):
        receiver = browser.text_field(id='receiver')
        receiver.send_keys('hello world')
        assert receiver.value == 'hello world'
        assert len(browser.element(id='output').ps()) == 11

    def test_accepts_arbitrary_list_of_arguments(self, browser):
        receiver = browser.text_field(id='receiver')
        receiver.send_keys('hello', 'world')
        assert receiver.value == 'helloworld'
        assert len(browser.element(id='output').ps()) == 10

    @pytest.mark.xfail_chrome(reason='http://code.google.com/p/chromium/issues/detail?id=93879')
    @pytest.mark.xfail_firefox
    @pytest.mark.xfail_safari
    def test_performs_key_combinations(self, browser):
        receiver = browser.text_field(id='receiver')
        receiver.send_keys('foo')
        receiver.send_keys(MODIFIER + 'a' + Keys.NULL)
        receiver.send_keys(Keys.BACKSPACE)
        assert receiver.value == ''
        assert len(browser.element(id='output').ps()) == 6

    @pytest.mark.xfail_chrome(reason='http://code.google.com/p/chromium/issues/detail?id=93879')
    @pytest.mark.xfail_firefox
    @pytest.mark.xfail_safari
    def test_performs_arbitrary_list_of_key_combinations(self, browser):
        receiver = browser.text_field(id='receiver')
        receiver.send_keys('foo')
        receiver.send_keys(MODIFIER + 'a' + Keys.NULL + MODIFIER + 'x' + Keys.NULL)
        assert receiver.value == ''
        assert len(browser.element(id='output').ps()) == 7

    @pytest.mark.xfail_chrome(reason='http://code.google.com/p/chromium/issues/detail?id=93879')
    @pytest.mark.xfail_firefox
    @pytest.mark.xfail_safari
    def test_supports_combination_of_strings_and_arrays(self, browser):
        receiver = browser.text_field(id='receiver')
        receiver.send_keys('foo', [MODIFIER, 'a'], Keys.BACKSPACE)
        assert receiver.value == ''
        assert len(browser.element(id='output').ps()) == 6


class TestElementClick(object):
    @pytest.mark.xfail_firefox(reason='https://github.com/mozilla/geckodriver/issues/1375')
    def test_accepts_modifiers(self, browser):
        try:
            browser.link().click(Keys.SHIFT)
            assert len(browser.windows()) == 2
        finally:
            for window in browser.windows():
                if not window.is_current:
                    window.close()
            assert len(browser.windows()) == 1


class TestElementFlash(object):
    def test_returns_the_element_on_which_it_was_called(self, browser):
        h2 = browser.h2(text='Add user')
        assert h2.flash() == h2

    def test_should_keep_the_element_background_color_after_flashing(self, browser):
        h1 = browser.h1(text='User administration')
        h2 = browser.h2(text='Add user')

        assert h2.style('background-color') == \
            h2.flash('rainbow', flashes=2).style('background-color')
        assert h1.style('background-color') == h1.flash(flashes=2).style('background-color')

    def test_should_respond_to_preset_flashes_like_fast_and_slow(self, browser):
        h1 = browser.h1(text='User administration')
        h2 = browser.h2(text='Add user')

        assert h1.flash('rainbow') == h1
        assert h2.flash('slow') == h2
        assert h1.flash('fast') == h1
        assert h2.flash('long') == h2


@pytest.mark.page('non_control_elements.html')
class TestElementInnerOutter(object):
    def test_returns_text_content_of_element(self, browser):
        assert browser.div(id='shown').text_content == 'Not shownNot hidden'

    def test_returns_inner_text_of_element(self, browser):
        assert browser.div(id='shown').inner_text == 'Not hidden'

    def test_returns_inner_html_code_of_element(self, browser):
        assert browser.div(id='shown').inner_html == '<div id="hidden" style="display: none;">Not shown</div><div>Not hidden</div>'

    def test_returns_outer_html_code_of_element(self, browser):
        assert browser.div(id='shown').outer_html == '<div id="shown"><div id="hidden" style="display: none;">Not shown</div><div>Not hidden</div></div>'


@pytest.mark.page('non_control_elements.html')
class TestSelectTextSelectedText(object):
    def test_selects_text_and_returns_selected_text(self, browser):
        el = browser.element(visible_text='all visible')
        el.select_text('all visible')
        assert el.selected_text == 'all visible'


class TestElementScrollIntoView(object):
    @pytest.mark.quits_browser
    def test_scrolls_element_into_view(self, browser):
        el = browser.button(name='new_user_image')
        element_center = el.center.y
        browser.window().resize_to(browser.window().size.width, element_center - 100)

        bottom_viewport_script = 'return window.pageYOffset + window.innerHeight;'
        assert browser.execute_script(bottom_viewport_script) < element_center

        assert isinstance(el.scroll_into_view(), Point)

        assert browser.execute_script(bottom_viewport_script) > element_center


class TestElementSizeLocation(object):

    # location

    def test_returns_coordinates_for_element_location(self, browser):
        location = browser.button(name='new_user_image').location

        assert isinstance(location, Point)
        assert location.y > 0
        assert location.x > 0

    # size

    def test_returns_size_of_element(self, browser):
        size = browser.button(name='new_user_image').size

        assert isinstance(size, Dimension)
        assert size.width == 104
        assert size.height == 70

    # height

    def test_returns_height_of_element(self, browser):
        assert browser.button(name='new_user_image').height == 70

    # width

    def test_returns_width_of_element(self, browser):
        assert browser.button(name='new_user_image').width == 104

    # center

    def test_returns_center_of_element(self, browser):
        location = browser.button(name='new_user_image').center

        assert isinstance(location, Point)
        assert location.y > 0
        assert location.x > 0


@pytest.mark.page('data_attributes.html')
class TestElementAttributeValue(object):
    def test_returns_attribute_value_by_attribute_name(self, browser):
        assert browser.p().attribute_value('data-type') == 'ruby-library'


@pytest.mark.page('data_attributes.html')
class TestElementAttributeValues(object):
    def test_returns_a_dict_(self, browser):
        assert isinstance(browser.p().attribute_values, dict)

    def test_returns_attribute_values_from_an_element(self, browser):
        assert browser.p().attribute_values == {'data_type': 'ruby-library'}

    def test_returns_attribute_with_special_characters(self, browser):
        expected = {'data_type': 'description', 'data-type_$p3c!a1': 'special-description'}
        assert browser.div().attribute_values == expected

    def test_returns_attribute_with_special_characters_as_a_string(self, browser):
        assert isinstance(list(browser.div().attribute_values)[0], six.string_types)


@pytest.mark.page('data_attributes.html')
class TestElementAttributeList(object):
    def test_returns_a_list(self, browser):
        assert isinstance(browser.div().attribute_list, list)

    def test_returns_list_of_attributes_from_an_alement(self, browser):
        assert browser.p().attribute_list == ['data_type']

    def test_returns_attribute_name_with_special_characters_as_a_string(self, browser):
        assert isinstance(browser.div().attribute_list[0], six.string_types)


class TestElementLocated(object):
    def test_returns_returns_true_if_element_has_been_located(self, browser):
        el = browser.form(id='new_user')
        el.exists
        assert el._located is True

    def test_returns_returns_false_if_element_has_not_been_located(self, browser):
        assert browser.form(id='new_user')._located is False


class TestElementWd(object):
    def test_returns_a_selenium_webelement_reference(self, browser):
        from selenium.webdriver.remote.webelement import WebElement
        element = browser.text_field(id='new_user_email')
        assert isinstance(element.wd, WebElement)


class TestElementHash(object):
    def test_returns_a_hash(self, browser):
        element = browser.text_field(id='new_user_email')
        hash1 = hash(element)
        hash2 = hash(element.locate())
        assert isinstance(hash1, int)
        assert isinstance(hash2, int)
        assert hash1 != hash2


class TestElementFloat(object):
    def test_returns_float_value_of_applicable_element(self, browser):
        element = browser.text_field(id='number')
        assert isinstance(element.valueasnumber, float)

    def test_returns_none_for_an_inapplicable_element(self, browser):
        element = browser.input()
        assert element.valueasnumber is None


class TestElementInteger(object):
    def test_returns_integer_value_of_applicable_element(self, browser):
        element = browser.form()
        assert isinstance(element.length, int)

    def test_returns_negative_one_for_an_inapplicable_element(self, browser):
        element = browser.input()
        assert element.maxlength == -1


class TestElementClassName(object):
    def test_returns_single_class_name(self, browser):
        assert browser.form(id='new_user').class_name == 'user'

    def test_returns_multiple_class_names_in_a_string(self, browser):
        assert browser.div(id='messages').class_name == 'multiple classes here'

    def test_returns_an_empty_string_if_the_element_exists_but_there_is_no_class_attribute(self, browser):
        assert browser.div(id='changed_language').class_name == ''

    def test_raises_correct_exception_if_the_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.div(id='no_such_id').class_name


class TestElementClasses(object):
    def test_returns_the_class_attribute_if_the_if_the_element_exists(self, browser):
        assert browser.div(id='messages').classes == 'multiple classes here'.split()

    def test_rturns_an_empty_list_if_the_element_exists_but_there_is_no_class_attribute(self, browser):
        assert browser.div(id='changed_language').classes == []

    def test_raises_correct_exception_if_the_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.div(id='no_such_id').classes


@pytest.mark.page('obscured.html')
class TestElementObscured(object):
    def test_returns_false_if_element_center_is_not_covered(self, browser):
        btn = browser.button(id='not_obscured')
        assert not btn.obscured
        btn.click()

    def test_returns_false_if_element_center_is_covered_by_its_decendant(self, browser):
        btn = browser.button(id='has_descendant')
        assert not btn.obscured
        btn.click()

    def test_returns_true_if_element_center_is_covered_by_non_descendant(self, browser):
        btn = browser.button(id='obscured')
        assert btn.obscured
        exception = WebDriverException if browser.name == 'chrome' else \
            ElementClickInterceptedException
        with pytest.raises(exception):
            btn.click()

    def _test_returns_false_if_element_center_is_surrounded_by_non_descendants(self, browser):
        btn = browser.button(id='surrounded')
        assert not btn.obscured
        btn.click()

    def test_scrolls_element_into_view_before_checking_if_obscured(self, browser):
        btn = browser.button(id='requires_scrolling')
        assert not btn.obscured
        btn.click()

    @pytest.mark.usefixtures('quick_timeout')
    def test_returns_true_if_element_cannot_be_scrolled_into_view(self, browser):
        btn = browser.button(id='off_screen')
        assert btn.obscured
        with pytest.raises(UnknownObjectException):
            btn.click()

    @pytest.mark.usefixtures('quick_timeout')
    def test_returns_true_if_the_element_is_hidden(self, browser):
        btn = browser.button(id='hidden')
        assert btn.obscured
        with pytest.raises(UnknownObjectException):
            btn.click()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_the_element_does_not_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.button(id='does_not_exist').obscured
