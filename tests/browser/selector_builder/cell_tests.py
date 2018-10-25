from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.cell.selector_builder import SelectorBuilder

pytestmark = pytest.mark.page('tables.html')

ATTRIBUTES = HTMLElement.ATTRIBUTES


def verify_build(browser, selector, wd, data=None, remaining=None, scope=None):
    builder = SelectorBuilder(ATTRIBUTES)
    query_scope = scope or browser.element(id='gregory').locate()
    built = builder.build(selector)
    assert built == [wd, remaining or {}]

    located = query_scope.wd.find_element(*list(wd.items())[0])

    if data:
        assert located.get_attribute('data-locator') == data


class TestBuild(object):
    def test_without_any_elements(self, browser):
        items = {
            'selector': {},
            'wd': {'xpath': "./*[local-name()='th' or local-name()='td']"},
            'data': 'first cell'
        }
        verify_build(browser, **items)

    # with index

    def test_index_positive(self, browser):
        items = {
            'selector': {'index': 3},
            'wd': {'xpath': "(./*[local-name()='th' or local-name()='td'])[4]"},
            'data': 'after tax'
        }
        verify_build(browser, **items)

    def test_index_negative(self, browser):
        items = {
            'selector': {'index': -3},
            'wd': {'xpath': "(./*[local-name()='th' or local-name()='td'])[last()-2]"},
            'data': 'before tax'
        }
        verify_build(browser, **items)

    def test_index_last(self, browser):
        items = {
            'selector': {'index': -1},
            'wd': {'xpath': "(./*[local-name()='th' or local-name()='td'])[last()]"},
            'data': 'after tax'
        }
        verify_build(browser, **items)

    def test_index_does_not_return_index_if_zero(self, browser):
        items = {
            'selector': {'index': 0},
            'wd': {'xpath': "./*[local-name()='th' or local-name()='td']"},
            'data': 'first cell'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_index_is_not_an_integer(self, browser):
        with pytest.raises(TypeError, match="expected {}, got 'foo':{}".format(int, str)):
            SelectorBuilder(ATTRIBUTES).build({'index': 'foo'})

    # with multiple locators

    def test_attribute_and_text(self, browser):
        items = {
            'selector': {'headers': compile(r'before_tax'), 'text': '5 934'},
            'wd': {'xpath': "./*[local-name()='th' or local-name()='td'][normalize-space()="
                            "'5 934'][contains(@headers, 'before_tax')]"},
            'data': 'before tax'
        }
        verify_build(browser, **items)

    def test_delegates_adjacent_to_element_selector_builder(self, browser):
        items = {
            'scope': browser.element(id='p3').locate(),
            'selector': {'adjacent': 'ancestor', 'index': 2},
            'wd': {'xpath': './ancestor::*[3]'},
            'data': 'top table'
        }
        verify_build(browser, **items)
