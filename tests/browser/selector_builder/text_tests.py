from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.exception import LocatorException
from nerodia.locators.text_field.selector_builder import SelectorBuilder

pytestmark = pytest.mark.page('forms_with_input_elements.html')

ATTRIBUTES = HTMLElement.ATTRIBUTES
NEGATIVE_TYPES = ' and '.join([
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='file'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='radio'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='checkbox'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='submit'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='reset'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='image'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='button'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='hidden'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='range'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='color'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='date'",
    "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')!='datetime-local'"
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
            'wd': {'xpath': ".//*[local-name()='input'][not(@type) or "
                            "({})]".format(NEGATIVE_TYPES)},
            'data': 'input name'
        }
        verify_build(browser, **items)

    # with type

    def test_specified_text_field_type_that_is_text(self, browser):
        items = {
            'selector': {'type': 'text'},
            'wd': {'xpath': ".//*[local-name()='input'][translate(@type,"
                            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='text']"},
            'data': 'first text'
        }
        verify_build(browser, **items)

    def test_specified_text_field_type_that_is_not_text(self, browser):
        items = {
            'selector': {'type': 'number'},
            'wd': {'xpath': ".//*[local-name()='input'][translate(@type,'ABCDEFGHIJKLMNOPQRSTU"
                            "VWXYZ','abcdefghijklmnopqrstuvwxyz')='number']"},
            'data': '42'
        }
        verify_build(browser, **items)

    def test_true_locates_text_field_with_a_type_specified(self, browser):
        items = {
            'selector': {'type': True},
            'wd': {'xpath': ".//*[local-name()='input'][{}]".format(NEGATIVE_TYPES)},
            'data': 'input name'
        }
        verify_build(browser, **items)

    def test_false_locates_text_field_without_type_specified(self, browser):
        items = {
            'selector': {'type': False},
            'wd': {'xpath': ".//*[local-name()='input'][not(@type)]"},
            'data': 'input name'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_a_non_text_field_type_input_is_specified(self):
        match = 'TextField Elements can not be located by type: checkbox'
        with pytest.raises(LocatorException, match=match):
            SelectorBuilder(ATTRIBUTES).build({'type': 'checkbox'})

    # with text

    def test_string_for_value(self, browser):
        items = {
            'selector': {'text': 'Developer'},
            'wd': {'xpath': ".//*[local-name()='input'][not(@type) or "
                            "({})]".format(NEGATIVE_TYPES)},
            'remaining': {'text': 'Developer'}
        }
        verify_build(browser, **items)

    def test_simple_regexp_for_value(self, browser):
        items = {
            'selector': {'text': compile(r'Dev')},
            'wd': {'xpath': ".//*[local-name()='input'][not(@type) or "
                            "({})]".format(NEGATIVE_TYPES)},
            'remaining': {'text': compile(r'Dev')}
        }
        verify_build(browser, **items)

    def test_returns_complicated_regexp_to_the_locator_as_a_value(self, browser):
        items = {
            'selector': {'text': compile(r'^foo$')},
            'wd': {'xpath': ".//*[local-name()='input'][not(@type) or "
                            "({})]".format(NEGATIVE_TYPES)},
            'remaining': {'text': compile(r'^foo$')}
        }
        verify_build(browser, **items)

    # with index

    def test_index_positive(self, browser):
        items = {
            'selector': {'index': 4},
            'wd': {'xpath': "(.//*[local-name()='input'][not(@type) or "
                            "({})])[5]".format(NEGATIVE_TYPES)},
            'data': 'dev'
        }
        verify_build(browser, **items)

    def test_index_negative(self, browser):
        items = {
            'selector': {'index': -3},
            'wd': {'xpath': "(.//*[local-name()='input'][not(@type) or "
                            "({})])[last()-2]".format(NEGATIVE_TYPES)},
            'data': '42'
        }
        verify_build(browser, **items)

    def test_index_last(self, browser):
        items = {
            'selector': {'index': -1},
            'wd': {'xpath': "(.//*[local-name()='input'][not(@type) or "
                            "({})])[last()]".format(NEGATIVE_TYPES)},
            'data': 'last text'
        }
        verify_build(browser, **items)

    def test_index_does_not_return_index_if_zero(self, browser):
        items = {
            'selector': {'index': 0},
            'wd': {'xpath': ".//*[local-name()='input'][not(@type) or "
                            "({})]".format(NEGATIVE_TYPES)},
            'data': 'input name'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_index_is_not_an_integer(self, browser):
        with pytest.raises(TypeError, match="expected {}, got 'foo':{}".format(int, str)):
            SelectorBuilder(ATTRIBUTES).build({'index': 'foo'})

    # with multiple locators

    def test_locates_using_tag_name_class_attributes_text(self, browser):
        items = {
            'selector': {'text': 'Developer', 'class_name': compile(r'c'), 'id': True},
            'wd': {'xpath': ".//*[local-name()='input'][contains(@class, 'c')][not(@type) or "
                            "({})][@id]".format(NEGATIVE_TYPES)},
            'remaining': {'text': 'Developer'}
        }
        verify_build(browser, **items)

    def test_delegates_adjacent_to_element_selector_builder(self, browser):
        items = {
            'scope': browser.element(id='new_user_email').locate(),
            'selector': {'adjacent': 'ancestor', 'index': 1},
            'wd': {'xpath': './ancestor::*[2]'},
            'data': 'form'
        }
        verify_build(browser, **items)
