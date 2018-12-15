from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.text_area.selector_builder import SelectorBuilder

ATTRIBUTES = HTMLElement.ATTRIBUTES


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


class TestBuild(object):
    def test_always_return_value_argument_for_string(self, builder):
        items = {
            'selector': {'tag_name': 'textarea', 'value': 'Foo'},
            'built': {'xpath': ".//*[local-name()='textarea']", 'value': 'Foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_always_return_value_argument_for_regex(self, builder):
        items = {
            'selector': {'tag_name': 'textarea', 'value': compile(r'Foo')},
            'built': {'xpath': ".//*[local-name()='textarea']", 'value': compile(r'Foo')}
        }
        assert builder.build(items['selector']) == items['built']
