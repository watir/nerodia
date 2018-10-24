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

    # with multiple locators

    def test_attribute_and_text(self, browser):
        items = {
            'selector': {'headers': compile(r'before_tax'), 'text': '5 934'},
            'wd': {'xpath': "./*[local-name()='th' or local-name()='td']"
                            "[contains(@headers, 'before_tax')][normalize-space()='5 934']"},
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
