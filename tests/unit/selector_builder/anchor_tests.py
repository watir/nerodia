from re import IGNORECASE, compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.anchor.selector_builder import SelectorBuilder

ATTRIBUTES = HTMLElement.ATTRIBUTES


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


class TestBuild(object):
    def test_without_only_tag_name(self, builder):
        items = {
            'selector': {'tag_name': 'a'},
            'built': {'xpath': ".//*[local-name()='a']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_converts_visible_text_string_to_link_text(self, builder):
        items = {
            'selector': {'tag_name': 'a', 'visible_text': 'Foo'},
            'built': {'link_text': 'Foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_converts_visible_text_regexp_to_partial_link_text(self, builder):
        items = {
            'selector': {'tag_name': 'a', 'visible_text': compile(r'Foo')},
            'built': {'partial_link_text': 'Foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_does_not_convert_visible_text_with_ignorecase_regexp_to_partial_link_text(self, builder):
        items = {
            'selector': {'tag_name': 'a',
                         'visible_text': compile(r'partial text', flags=IGNORECASE)},
            'built': {'xpath': ".//*[local-name()='a']",
                      'visible_text': compile(r'partial text', flags=IGNORECASE)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_does_not_convert_visible_text_with_string_and_other_locators(self, builder):
        items = {
            'selector': {'tag_name': 'a', 'visible_text': 'Foo', 'id': 'Foo'},
            'built': {'xpath': ".//*[local-name()='a'][@id='Foo']", 'visible_text': 'Foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_does_not_convert_visible_text_with_regexp_and_other_locators(self, builder):
        items = {
            'selector': {'tag_name': 'a', 'visible_text': compile(r'Foo'), 'id': 'Foo'},
            'built': {'xpath': ".//*[local-name()='a'][@id='Foo']", 'visible_text': compile(r'Foo')}
        }
        assert builder.build(items['selector']) == items['built']
