from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.cell.selector_builder import SelectorBuilder

ATTRIBUTES = HTMLElement.ATTRIBUTES


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


class TestBuild(object):
    def test_without_any_elements(self, builder):
        items = {
            'selector': {},
            'built': {'xpath': "./*[local-name()='th' or local-name()='td']"}
        }
        assert builder.build(items['selector']) == items['built']

    # with index

    def test_index_positive(self, builder):
        items = {
            'selector': {'index': 3},
            'built': {'xpath': "(./*[local-name()='th' or local-name()='td'])[4]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_negative(self, builder):
        items = {
            'selector': {'index': -3},
            'built': {'xpath': "(./*[local-name()='th' or local-name()='td'])[last()-2]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_last(self, builder):
        items = {
            'selector': {'index': -1},
            'built': {'xpath': "(./*[local-name()='th' or local-name()='td'])[last()]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_does_not_return_index_if_zero(self, builder):
        items = {
            'selector': {'index': 0},
            'built': {'xpath': "./*[local-name()='th' or local-name()='td']"}
        }
        builder.build(items['selector']) == items['built']

    def test_raises_exception_when_index_is_not_an_integer(self, builder):
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            builder.build({'index': 'foo'})
        assert e.value.args[0] == msg

    # with multiple locators

    def test_attribute_and_text(self, builder):
        items = {
            'selector': {'headers': compile(r'before_tax'), 'text': '5 934'},
            'built': {'xpath': "./*[local-name()='th' or local-name()='td'][normalize-space()="
                               "'5 934'][contains(@headers, 'before_tax')]"}
        }
        assert builder.build(items['selector']) == items['built']
