from re import compile

import pytest
from selenium.webdriver.remote.webelement import WebElement

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.row.selector_builder import SelectorBuilder

ATTRIBUTES = HTMLElement.ATTRIBUTES


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


def selector_built(mocker, **opts):
    klass = opts.pop('element', HTMLElement)
    mock = mocker.MagicMock(spec=klass)
    mock.enabled = True
    if 'wd' in opts:
        mock.wd = opts.pop('wd')
    else:
        mock.wd = mocker.MagicMock(spec=WebElement)
    if 'selector' in opts:
        selector = opts.pop('selector')
    else:
        selector = {}
    for key, value in opts.items():
        setattr(mock, key, value)
    mock.selector = selector

    builder = SelectorBuilder(ATTRIBUTES, mock)
    built = builder.build(selector)
    built.pop('scope', None)
    return built


class TestBuild(object):

    # with query scopes

    def test_with_only_table_query_scope(self, mocker):
        items = {
            'built': {'xpath': "./*[local-name()='tr'] | ./*[local-name()='tbody']/"
                               "*[local-name()='tr'] | ./*[local-name()='thead']/"
                               "*[local-name()='tr'] | ./*[local-name()='tfoot']/"
                               "*[local-name()='tr']"}
        }
        built = selector_built(mocker, tag_name='table')
        assert built == items['built']

    def test_with_tbody_query_scope(self, mocker):
        items = {
            'built': {'xpath': "./*[local-name()='tr']"}
        }
        built = selector_built(mocker, tag_name='tbody')
        assert built == items['built']

    def test_with_thead_query_scope(self, mocker):
        items = {
            'built': {'xpath': "./*[local-name()='tr']"}
        }
        built = selector_built(mocker, tag_name='thead')
        assert built == items['built']

    def test_with_tfoot_query_scope(self, mocker):
        items = {
            'built': {'xpath': "./*[local-name()='tr']"}
        }
        built = selector_built(mocker, tag_name='tfoot')
        assert built == items['built']

    # with index

    def test_index_positive(self, mocker):
        items = {
            'selector': {'index': 1},
            'built': {'xpath': "(./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()="
                               "'tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                               "./*[local-name()='tfoot']/*[local-name()='tr'])[2]"}
        }
        built = selector_built(mocker, tag_name='table', selector=items['selector'])
        assert built == items['built']

    def test_index_negative(self, mocker):
        items = {
            'selector': {'index': -3},
            'built': {'xpath': "(./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()="
                               "'tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                               "./*[local-name()='tfoot']/*[local-name()='tr'])[last()-2]"}
        }
        built = selector_built(mocker, tag_name='table', selector=items['selector'])
        assert built == items['built']

    def test_index_last(self, mocker):
        items = {
            'selector': {'index': -1},
            'built': {'xpath': "(./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()"
                               "='tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                               "./*[local-name()='tfoot']/*[local-name()='tr'])[last()]"}
        }
        built = selector_built(mocker, tag_name='table', selector=items['selector'])
        assert built == items['built']

    def test_index_does_not_return_index_if_zero(self, mocker):
        items = {
            'selector': {'index': 0},
            'built': {'xpath': "./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()"
                               "='tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                               "./*[local-name()='tfoot']/*[local-name()='tr']"}
        }
        built = selector_built(mocker, tag_name='table', selector=items['selector'])
        assert built == items['built']

    def test_raises_exception_when_index_is_not_an_integer(self, mocker):
        items = {
            'selector': {'index': 'foo'}
        }
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            selector_built(mocker, tag_name='table', selector=items['selector'])
        assert e.value.args[0] == msg

    # with multiple locators

    def test_attribute_and_class(self, mocker):
        items = {
            'selector': {'id': 'gregory', 'class_name': compile(r'brick')},
            'built': {'xpath': "./*[local-name()='tr'][contains(@class, 'brick')][@id='gregory'] | "
                               "./*[local-name()='tbody']/*[local-name()='tr'][contains(@class, "
                               "'brick')][@id='gregory'] | ./*[local-name()='thead']/*[local-name"
                               "()='tr'][contains(@class, 'brick')][@id='gregory'] | ./*["
                               "local-name()='tfoot']/*[local-name()='tr'][contains(@class, "
                               "'brick')][@id='gregory']"}
        }
        built = selector_built(mocker, tag_name='table', selector=items['selector'])
        assert built == items['built']

    # returns locators that cannot be directly translated

    def test_not_translated_any_text_value(self, mocker):
        items = {
            'selector': {'text': 'Gregory'},
            'built': {'xpath': "./*[local-name()='tr'] | ./*[local-name()='tbody']/*[local-name()"
                               "='tr'] | ./*[local-name()='thead']/*[local-name()='tr'] | "
                               "./*[local-name()='tfoot']/*[local-name()='tr']",
                      'text': 'Gregory'},
        }
        built = selector_built(mocker, tag_name='table', selector=items['selector'])
        assert built == items['built']
