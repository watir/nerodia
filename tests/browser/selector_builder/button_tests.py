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
            'wd': {'xpath': ".//*[local-name()='button' or "
                            "(local-name()='input' and {})]".format(DEFAULT_TYPES)},
            'data': 'user submit'
        }
        verify_build(browser, **items)

    # with type

    def test_false_locates_button_elements(self, browser):
        items = {
            'selector': {'type': False},
            'wd': {'xpath': ".//*[local-name()='button']"},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_true_locates_input_elements(self, browser):
        items = {
            'selector': {'type': True},
            'wd': {'xpath': ".//*[(local-name()='input' and {})]".format(DEFAULT_TYPES)},
            'data': 'user submit'
        }
        verify_build(browser, **items)

    def test_locates_input_element_with_specified_type(self, browser):
        reset_only = "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'," \
                     "'abcdefghijklmnopqrstuvwxyz')='reset'"
        items = {
            'selector': {'type': 'reset'},
            'wd': {'xpath': ".//*[(local-name()='input' and {})]".format(reset_only)},
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

    def test_string_for_text(self, browser):
        items = {
            'selector': {'text': 'Button 2'},
            'wd': {'xpath': ".//*[local-name()='button' or (local-name()='input' and {})]"
                            "[normalize-space()='Button 2' or "
                            "@value='Button 2']".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    def test_simple_regexp_for_text(self, browser):
        items = {
            'selector': {'text': compile(r'Prev')},
            'wd': {'xpath': ".//*[local-name()='button' or (local-name()='input' and {})]"
                            "[contains(text(), 'Prev') or "
                            "contains(@value, 'Prev')]".format(DEFAULT_TYPES)},
            'data': 'preview'
        }
        verify_build(browser, **items)

    def test_returns_complicated_regexp_to_the_locator(self, browser):
        items = {
            'selector': {'text': compile(r'^foo$')},
            'wd': {'xpath': ".//*[local-name()='button' or (local-name()='input' and "
                            "{})]".format(DEFAULT_TYPES)},
            'remaining': {'text': compile(r'^foo$')}
        }
        verify_build(browser, **items)

    # with value

    def test_string_for_value(self, browser):
        items = {
            'selector': {'value': 'Preview'},
            'wd': {'xpath': ".//*[local-name()='button' or (local-name()='input' and {})]"
                            "[normalize-space()='Preview' or "
                            "@value='Preview']".format(DEFAULT_TYPES)},
            'data': 'preview'
        }
        verify_build(browser, **items)

    def test_simple_regexp_for_value(self, browser):
        items = {
            'selector': {'value': compile(r'2')},
            'wd': {'xpath': ".//*[local-name()='button' or (local-name()='input' and {})]"
                            "[contains(text(), '2') or "
                            "contains(@value, '2')]".format(DEFAULT_TYPES)},
            'data': 'Benjamin'
        }
        verify_build(browser, **items)

    # with multiple locators

    def test_locates_using_class_and_attributes(self, browser):
        items = {
            'selector': {'class_name': 'image', 'name': 'new_user_image', 'src': True},
            'wd': {'xpath': ".//*[local-name()='button' or (local-name()='input' and {})]"
                            "[contains(concat(' ', @class, ' '), ' image ')]"
                            "[@name='new_user_image' and @src]".format(DEFAULT_TYPES)},
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
