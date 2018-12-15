from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.row.selector_builder import SelectorBuilder

pytestmark = pytest.mark.page('tables.html')

ATTRIBUTES = HTMLElement.ATTRIBUTES


def verify_build(selector, built, data=None, scope=None, scope_tag=None):
    query_scope = scope
    scope_tag_name = scope_tag or query_scope.tag_name
    builder = SelectorBuilder(ATTRIBUTES, scope_tag_name)
    assert builder.build(selector) == built

    located = query_scope.wd.find_element(*list(built.items())[0])

    if data:
        assert located.get_attribute('data-locator') == data


class TestBuild(object):

    # with query scopes

    def test_with_only_table_query_scope(self, browser):
        items = {
            'scope': browser.element(id='outer').locate(),
            'selector': {},
            'built': {'xpath': "./*[local-name()='tr'] | ./*[local-name()='tbody']/"
                            "*[local-name()='tr'] | ./*[local-name()='thead']/*[local-name()='tr']"
                            " | ./*[local-name()='tfoot']/*[local-name()='tr']"},
            'data': 'first row'
        }
        verify_build(**items)

    def test_with_tbody_query_scope(self, browser):
        items = {
            'scope': browser.element(id='first').locate(),
            'selector': {},
            'built': {'xpath': "./*[local-name()='tr']"},
            'data': 'tbody row'
        }
        verify_build(**items)

    def test_with_thead_query_scope(self, browser):
        items = {
            'scope': browser.element(id='tax_headers').locate(),
            'selector': {},
            'built': {'xpath': "./*[local-name()='tr']"},
            'data': 'thead row'
        }
        verify_build(**items)

    def test_with_tfoot_query_scope(self, browser):
        items = {
            'scope': browser.element(id='tax_totals').locate(),
            'selector': {},
            'built': {'xpath': "./*[local-name()='tr']"},
            'data': 'tfoot row'
        }
        verify_build(**items)

    # with index

    def test_index_positive(self, browser):
        items = {
            'scope': browser.element(id='outer').locate(),
            'selector': {'index': 1},
            'built': {'xpath': "(./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()="
                            "'tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                            "./*[local-name()='tfoot']/*[local-name()='tr'])[2]"},
            'data': 'middle row'
        }
        verify_build(**items)

    def test_index_negative(self, browser):
        items = {
            'scope': browser.element(id='outer').locate(),
            'selector': {'index': -3},
            'built': {'xpath': "(./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()="
                            "'tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                            "./*[local-name()='tfoot']/*[local-name()='tr'])[last()-2]"},
            'data': 'first row'
        }
        verify_build(**items)

    def test_index_last(self, browser):
        items = {
            'scope': browser.element(id='outer').locate(),
            'selector': {'index': -1},
            'built': {'xpath': "(./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()="
                            "'tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                            "./*[local-name()='tfoot']/*[local-name()='tr'])[last()]"},
            'data': 'last row'
        }
        verify_build(**items)

    def test_index_does_not_return_index_if_zero(self, browser):
        items = {
            'scope': browser.element(id='outer').locate(),
            'selector': {'index': 0},
            'built': {'xpath': "./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()="
                            "'tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                            "./*[local-name()='tfoot']/*[local-name()='tr']"},
            'data': 'first row'
        }
        verify_build(**items)

    def test_raises_exception_when_index_is_not_an_integer(self, browser):
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            SelectorBuilder(ATTRIBUTES, 'table').build({'index': 'foo'})
        assert e.value.args[0] == msg

    # with multiple locators

    def test_attribute_and_class(self, browser):
        items = {
            'scope': browser.table().locate(),
            'selector': {'id': 'gregory', 'class_name': compile(r'brick')},
            'built': {'xpath': "./*[local-name()='tr'][contains(@class, 'brick')][@id='gregory'] | ./"
                            "*[local-name()='tbody']/*[local-name()='tr'][contains(@class, 'brick')"
                            "][@id='gregory'] | ./*[local-name()='thead']/*[local-name()='tr']"
                            "[contains(@class, 'brick')][@id='gregory'] | ./*[local-name()='tfoot']"
                            "/*[local-name()='tr'][contains(@class, 'brick')][@id='gregory']"},
            'data': 'House row'
        }
        verify_build(**items)

    # returns locators that cannot be directly translated

    def test_not_translated_any_text_value(self, browser):
        items = {
            'scope': browser.table(id='outer').locate(),
            'selector': {'text': 'Gregory'},
            'built': {'xpath': "./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()='tr"
                            "'] | ./*[local-name()='thead']/*[local-name()='tr'] | ./*[local-name()"
                            "='tfoot']/*[local-name()='tr']",
                      'text': 'Gregory'},
        }
        verify_build(**items)

    def test_not_translated_delegates_adjacent_to_element_selector_builder(self, browser):
        items = {
            'scope': browser.element(id='gregory').locate(),
            'scope_tag': 'table',
            'selector': {'adjacent': 'ancestor', 'index': 1},
            'built': {'xpath': './ancestor::*[2]'},
            'data': 'top table'
        }
        verify_build(**items)
