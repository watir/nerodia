from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.exception import LocatorException
from nerodia.locators.button.selector_builder import SelectorBuilder

pytestmark = pytest.mark.page('forms_with_input_elements.html')

ATTRIBUTES = HTMLElement.ATTRIBUTES
DEFAULT_TYPES = ' or '.join([
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='button'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='reset'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='submit'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='image'"
])


def verify_build(browser, selector, wd, data=None, remaining=None, scope=None):
    builder = SelectorBuilder(ATTRIBUTES)
    query_scope = scope or browser
    built = builder.build(selector)
    assert built == [wd, remaining or {}]

    located = query_scope.wd.find_element(*list(wd.items())[0])

    if data:
        assert located.get_attribute('data-locator') == data


class TestBuild(object):
    def test_without_any_elements(self, browser):
        items = {
            'selector': {},
            'wd': {'xpath': ".//*[(local-name()='button') or "
                            "(local-name()='input' and ({}))]".format(DEFAULT_TYPES)},
            'data': 'user submit'
        }
        verify_build(browser, **items)

    # with type

    def test_false_only_locates_with_button_without_a_type(self, browser):
        items = {
            'selector': {'type': False},
            'wd': {'xpath': ".//*[(local-name()='button' and not(@type))]"},
            'data': 'No Type'
        }
        verify_build(browser, **items)

    def test_true_locates_button_or_input_with_a_type(self, browser):
        items = {
            'selector': {'type': True},
            'wd': {'xpath': ".//*[(local-name()='button' and @type) or "
                            "(local-name()='input' and ({}))]".format(DEFAULT_TYPES)},
            'data': 'user submit'
        }
        verify_build(browser, **items)

    def test_locates_input_or_button_element_with_specified_type(self, browser):
        items = {
            'selector': {'type': 'reset'},
            'wd': {'xpath': ".//*[(local-name()='button' and translate(@type,'ABCDEFGHIJKLMNOPQRS"
                            "TUVWXYZ','abcdefghijklmnopqrstuvwxyz')='reset') or (local-name()='in"
                            "put' and (translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklm"
                            "nopqrstuvwxyz')='reset'))]"},
            'data': 'reset'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_a_non_button_type_is_specified(self):
        msg = 'Button Elements can not be located by input type: checkbox'
        with pytest.raises(LocatorException) as e:
            SelectorBuilder(ATTRIBUTES).build({'type': 'checkbox'})
        assert e.value.args[0] == msg

    # with xpath or css

    def test_returns_tag_name_and_type_to_the_locator(self, browser):
        items = {
            'selector': {'xpath': '//*[@id="disabled_button"]', 'tag_name': 'input',
                         'type': 'submit'},
            'wd': {'xpath': '//*[@id="disabled_button"]'},
            'remaining': {'tag_name': 'input', 'type': 'submit'}
        }
        verify_build(browser, **items)

    # text

    def test_locates_value_of_input_element_with_string(self, browser):
        items = {
            'selector': {'text': 'Button'},
            'wd': {'xpath': ".//*[(local-name()='button' and normalize-space()='Button') or "
                            "(local-name()='input' and ({}) and @value='Button')]".format(DEFAULT_TYPES)},
            'data': 'new user'
        }
        verify_build(browser, **items)

    def test_locates_text_of_button_element_with_string(self, browser):
        items = {
            'selector': {'text': 'Button 2'},
            'wd': {'xpath': ".//*[(local-name()='button' and normalize-space()='Button 2') or "
                            "(local-name()='input' and ({}) and @value='Button "
                            "2')]".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_locates_value_of_input_element_with_simple_regexp(self, browser):
        items = {
            'selector': {'text': compile(r'Button')},
            'wd': {'xpath': ".//*[(local-name()='button' and contains(text(), 'Button')) or "
                            "(local-name()='input' and ({}) and contains(@value, "
                            "'Button'))]".format(DEFAULT_TYPES)},
            'data': 'new user'
        }
        verify_build(browser, **items)

    def test_locates_text_of_button_element_with_simple_regexp(self, browser):
        items = {
            'selector': {'text': compile(r'Button 2')},
            'wd': {'xpath': ".//*[(local-name()='button' and contains(text(), 'Button 2')) or "
                            "(local-name()='input' and ({}) and contains(@value, "
                            "'Button 2'))]".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_returns_complex_text_regexp_to_the_locator(self, browser):
        items = {
            'selector': {'text': compile(r'^foo$')},
            'wd': {'xpath': ".//*[(local-name()='button' and text()) or (local-name()='input' "
                            "and ({}) and @value)]".format(DEFAULT_TYPES)},
            'remaining': {'text': compile(r'^foo$')}
        }
        verify_build(browser, **items)

    # with value

    def test_input_element_value_with_string(self, browser):
        items = {
            'selector': {'value': 'Preview'},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[normalize-space()='Preview' or @value="
                            "'Preview']".format(DEFAULT_TYPES)},
            'data': 'preview'
        }
        verify_build(browser, **items)

    def test_button_element_value_with_string(self, browser):
        items = {
            'selector': {'value': 'button_2'},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[normalize-space()='button_2' or @value="
                            "'button_2']".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_input_element_value_with_simple_regexp(self, browser):
        items = {
            'selector': {'value': compile(r'Prev')},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[contains(text(), 'Prev') or contains(@value, "
                            "'Prev')]".format(DEFAULT_TYPES)},
            'data': 'preview'
        }
        verify_build(browser, **items)

    def test_button_element_value_with_simple_regexp(self, browser):
        items = {
            'selector': {'value': compile(r'on_2')},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[contains(text(), 'on_2') or contains(@value, "
                            "'on_2')]".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_button_element_text_with_string(self, browser):
        items = {
            'selector': {'value': 'Button 2'},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[normalize-space()='Button 2' or @value="
                            "'Button 2']".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_button_element_text_with_simple_regexp(self, browser):
        items = {
            'selector': {'value': compile(r'ton 2')},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[contains(text(), 'ton 2') or contains(@value, "
                            "'ton 2')]".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_returns_complex_value_regexp_to_the_locator(self, browser):
        items = {
            'selector': {'value': compile(r'^foo$')},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[text() or @value]".format(DEFAULT_TYPES)},
            'remaining': {'value': compile(r'^foo$')}
        }
        verify_build(browser, **items)

    # with index

    def test_index_positive(self, browser):
        items = {
            'selector': {'index': 3},
            'wd': {'xpath': "(.//*[(local-name()='button') or (local-name()='input' and "
                            "({}))])[4]".format(DEFAULT_TYPES)},
            'data': 'preview'
        }
        verify_build(browser, **items)

    def test_index_negative(self, browser):
        items = {
            'selector': {'index': -4},
            'wd': {'xpath': "(.//*[(local-name()='button') or (local-name()='input' and "
                            "({}))])[last()-3]".format(DEFAULT_TYPES)},
            'data': 'submittable button'
        }
        verify_build(browser, **items)

    def test_index_last(self, browser):
        items = {
            'selector': {'index': -1},
            'wd': {'xpath': "(.//*[(local-name()='button') or (local-name()='input' and "
                            "({}))])[last()]".format(DEFAULT_TYPES)},
            'data': 'last button'
        }
        verify_build(browser, **items)

    def test_index_does_not_return_index_if_zero(self, browser):
        items = {
            'selector': {'index': 0},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and "
                            "({}))]".format(DEFAULT_TYPES)},
            'data': 'user submit'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_index_is_not_an_integer(self, browser):
        with pytest.raises(TypeError, match="expected {}, got 'foo':{}".format(int, str)):
            SelectorBuilder(ATTRIBUTES).build({'index': 'foo'})

    # with multiple locators

    def test_locates_using_class_and_attributes(self, browser):
        items = {
            'selector': {'class_name': 'image', 'name': 'new_user_image', 'src': True},
            'wd': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                            "[contains(concat(' ', @class, ' '), ' image ')][@name="
                            "'new_user_image' and @src]".format(DEFAULT_TYPES)},
            'data': 'submittable button'
        }
        verify_build(browser, **items)

    def test_delegates_adjacent_to_element_selector_builder(self, browser):
        items = {
            'scope': browser.element(id='new_user_button').locate(),
            'selector': {'adjacent': 'ancestor', 'index': 2},
            'wd': {'xpath': './ancestor::*[3]'},
            'data': 'body'
        }
        verify_build(browser, **items)
