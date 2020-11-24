from collections import OrderedDict
from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.exception import LocatorException
from nerodia.locators.button.selector_builder import SelectorBuilder
from nerodia.locators.element.xpath_support import XpathSupport

ATTRIBUTES = HTMLElement.ATTRIBUTES
DEFAULT_TYPES = ' or '.join([
    "translate(@type,'{0}','{1}')=translate('button','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')=translate('reset','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')=translate('submit','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')=translate('image','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE)
])


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


class TestBuild(object):
    def test_without_any_elements(self, builder):
        items = {
            'selector': {},
            'built': {'xpath': ".//*[(local-name()='button') or "
                               "(local-name()='input' and ({}))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    # with type

    def test_false_only_locates_with_button_without_a_type(self, builder):
        items = {
            'selector': {'type': False},
            'built': {'xpath': ".//*[(local-name()='button' and not(@type))]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_true_locates_button_or_input_with_a_type(self, builder):
        items = {
            'selector': {'type': True},
            'built': {'xpath': ".//*[(local-name()='button' and @type) or "
                               "(local-name()='input' and ({}))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_input_or_button_element_with_specified_type(self, builder):
        typ = "translate('reset','{}','{}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE)
        items = {
            'selector': {'type': 'reset'},
            'built': {
                'xpath': ".//*[(local-name()='button' and translate(@type,'{0}','{1}')={2})"
                         " or (local-name()='input' and (translate(@type,'{0}','{1}')={2})"
                         ")]".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE, typ)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_a_non_button_type_is_specified(self, builder):
        msg = 'Button Elements can not be located by input type: checkbox'
        with pytest.raises(LocatorException) as e:
            builder.build({'type': 'checkbox'})
        assert e.value.args[0] == msg

    # with xpath or css

    def test_returns_tag_name_and_type_to_the_locator(self, builder):
        items = {
            'selector': {'xpath': '//*[@id="disabled_button"]', 'tag_name': 'input',
                         'type': 'submit'},
            'built': {'xpath': '//*[@id="disabled_button"]', 'tag_name': 'input', 'type': 'submit'},
        }
        assert builder.build(items['selector']) == items['built']

    # text

    def test_locates_value_of_input_element_with_string(self, builder):
        items = {
            'selector': {'text': 'Button'},
            'built': {'xpath': ".//*[(local-name()='button' and normalize-space()='Button') or "
                               "(local-name()='input' and ({}) and "
                               "@value='Button')]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_text_of_button_element_with_string(self, builder):
        items = {
            'selector': {'text': 'Button 2'},
            'built': {'xpath': ".//*[(local-name()='button' and normalize-space()='Button 2') or "
                               "(local-name()='input' and ({}) and @value='Button "
                               "2')]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_value_of_input_element_with_simple_regexp(self, builder):
        items = {
            'selector': {'text': compile(r'Button')},
            'built': {'xpath': ".//*[(local-name()='button' and contains(normalize-space(), 'Button')) or "
                               "(local-name()='input' and ({}) and contains(@value, "
                               "'Button'))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_text_of_button_element_with_simple_regexp(self, builder):
        items = {
            'selector': {'text': compile(r'Button 2')},
            'built': {'xpath': ".//*[(local-name()='button' and contains(normalize-space(), 'Button 2')) or "
                               "(local-name()='input' and ({}) and contains(@value, "
                               "'Button 2'))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_with_simple_regexp_for_text(self, builder):
        items = {
            'selector': {'text': compile(r'n 2')},
            'built': {'xpath': ".//*[(local-name()='button' and contains(normalize-space(), 'n 2')) or "
                               "(local-name()='input' and ({}) and contains(@value, "
                               "'n 2'))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_with_simple_regexp_for_value(self, builder):
        items = {
            'selector': {'text': compile(r'Prev')},
            'built': {'xpath': ".//*[(local-name()='button' and contains(normalize-space(), 'Prev')) or "
                               "(local-name()='input' and ({}) and contains(@value, "
                               "'Prev'))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_returns_complex_text_regexp_to_the_locator(self, builder):
        items = {
            'selector': {'text': compile(r'^foo$')},
            'built': {'xpath': ".//*[(local-name()='button' and contains(normalize-space(), 'foo')) or "
                               "(local-name()='input' and ({}) and contains(@value, "
                               "'foo'))]".format(DEFAULT_TYPES), 'text': compile(r'^foo$')},
        }
        assert builder.build(items['selector']) == items['built']

    # with value

    def test_input_element_value_with_string(self, builder):
        items = {
            'selector': {'value': 'Preview'},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[normalize-space()='Preview' or @value="
                               "'Preview']".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_button_element_value_with_string(self, builder):
        items = {
            'selector': {'value': 'button_2'},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[normalize-space()='button_2' or @value="
                               "'button_2']".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_input_element_value_with_simple_regexp(self, builder):
        items = {
            'selector': {'value': compile(r'Prev')},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[contains(normalize-space(), 'Prev') or contains(@value, "
                               "'Prev')]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_button_element_value_with_simple_regexp(self, builder):
        items = {
            'selector': {'value': compile(r'on_2')},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[contains(normalize-space(), 'on_2') or contains(@value, "
                               "'on_2')]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_button_element_text_with_string(self, builder):
        items = {
            'selector': {'value': 'Button 2'},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[normalize-space()='Button 2' or @value="
                               "'Button 2']".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_button_element_text_with_simple_regexp(self, builder):
        items = {
            'selector': {'value': compile(r'ton 2')},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[contains(normalize-space(), 'ton 2') or contains(@value, "
                               "'ton 2')]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_returns_complex_value_regexp_to_the_locator(self, builder):
        items = {
            'selector': {'value': compile(r'^foo$')},
            'built': {'value': compile(r'^foo$'),
                      'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[contains(normalize-space(), 'foo') or contains(@value, "
                               "'foo')]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    # with index

    def test_index_positive(self, builder):
        items = {
            'selector': {'index': 3},
            'built': {'xpath': "(.//*[(local-name()='button') or (local-name()='input' and "
                               "({}))])[4]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_negative(self, builder):
        items = {
            'selector': {'index': -4},
            'built': {'xpath': "(.//*[(local-name()='button') or (local-name()='input' and "
                               "({}))])[last()-3]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_last(self, builder):
        items = {
            'selector': {'index': -1},
            'built': {'xpath': "(.//*[(local-name()='button') or (local-name()='input' and "
                               "({}))])[last()]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_does_not_return_index_if_zero(self, builder):
        items = {
            'selector': {'index': 0},
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and "
                               "({}))]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_index_is_not_an_integer(self, builder):
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            builder.build({'index': 'foo'})
        assert e.value.args[0] == msg

    # with multiple locators

    def test_locates_using_class_and_attributes(self, builder):
        items = {
            'selector': OrderedDict([('class_name', 'image'), ('name', 'new_user_image'),
                                     ('src', True)]),
            'built': {'xpath': ".//*[(local-name()='button') or (local-name()='input' and ({}))]"
                               "[contains(concat(' ', @class, ' '), ' image ')][@name="
                               "'new_user_image' and @src]".format(DEFAULT_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']
