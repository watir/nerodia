from re import compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.exception import LocatorException
from nerodia.locators.element.xpath_support import XpathSupport
from nerodia.locators.text_field.selector_builder import SelectorBuilder

ATTRIBUTES = HTMLElement.ATTRIBUTES
NEGATIVE_TYPES = ' and '.join([
    "translate(@type,'{0}','{1}')!=translate('file','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('radio','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('checkbox','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('submit','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('reset','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('image','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('button','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('hidden','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('range','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('color','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('date','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE),
    "translate(@type,'{0}','{1}')!=translate('datetime-local','{0}','{1}')".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE)
])


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


class TestBuild(object):
    def test_without_any_elements(self, builder):
        items = {
            'selector': {},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or "
                               "({})]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    # with type

    def test_specified_text_field_type_that_is_text(self, builder):
        items = {
            'selector': {'type': 'text'},
            'built': {'xpath': ".//*[local-name()='input'][translate(@type,'{0}','{1}')=translate("
                               "'text','{0}','{1}')"
                               "]".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_specified_text_field_type_that_is_not_text(self, builder):
        items = {
            'selector': {'type': 'number'},
            'built': {'xpath': ".//*[local-name()='input'][translate(@type,'{0}','{1}')=translate("
                               "'number','{0}','{1}')"
                               "]".format(XpathSupport.UPPERCASE, XpathSupport.LOWERCASE)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_true_locates_text_field_with_a_type_specified(self, builder):
        items = {
            'selector': {'type': True},
            'built': {'xpath': ".//*[local-name()='input'][{}]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_false_locates_text_field_without_type_specified(self, builder):
        items = {
            'selector': {'type': False},
            'built': {'xpath': ".//*[local-name()='input'][not(@type)]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_a_non_text_field_type_input_is_specified(self, builder):
        match = 'TextField Elements can not be located by type: checkbox'
        with pytest.raises(LocatorException, match=match):
            builder.build({'type': 'checkbox'})

    # with index

    def test_index_positive(self, builder):
        items = {
            'selector': {'index': 4},
            'built': {'xpath': "(.//*[local-name()='input'][not(@type) or "
                               "({})])[5]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_negative(self, builder):
        items = {
            'selector': {'index': -3},
            'built': {'xpath': "(.//*[local-name()='input'][not(@type) or "
                               "({})])[last()-2]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_last(self, builder):
        items = {
            'selector': {'index': -1},
            'built': {'xpath': "(.//*[local-name()='input'][not(@type) or "
                               "({})])[last()]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_does_not_return_index_if_it_is_zero(self, builder):
        items = {
            'selector': {'index': 0},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or "
                               "({})]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_index_is_not_an_integer(self, builder):
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            builder.build({'index': 'foo'})
        assert e.value.args[0] == msg

    # with text

    def test_string_for_value(self, builder):
        items = {
            'selector': {'text': 'Developer'},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or "
                               "({})]".format(NEGATIVE_TYPES),
                      'text': 'Developer'},
        }
        assert builder.build(items['selector']) == items['built']

    def test_simple_regexp_for_value(self, builder):
        items = {
            'selector': {'text': compile(r'Dev')},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or "
                               "({})]".format(NEGATIVE_TYPES),
                      'text': compile(r'Dev')},
        }
        assert builder.build(items['selector']) == items['built']

    def test_returns_complicated_regexp_to_the_locator_as_a_value(self, builder):
        items = {
            'selector': {'text': compile(r'^foo$')},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or "
                               "({})]".format(NEGATIVE_TYPES),
                      'text': compile(r'^foo$')},
        }
        assert builder.build(items['selector']) == items['built']

    # with label

    def test_using_string(self, builder):
        items = {
            'selector': {'label': 'First name'},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or ({})][@id=//label"
                               "[normalize-space()='First name']/@for or parent::label"
                               "[normalize-space()='First name']]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    def test_using_string_with_hidden_text(self, builder):
        items = {
            'selector': {'label': 'With hidden text'},
            'built': {'xpath': ".//*[local-name()='input'][not(@type) or ({})][@id=//label"
                               "[normalize-space()='With hidden text']/@for or parent::label"
                               "[normalize-space()='With hidden text']]".format(NEGATIVE_TYPES)}
        }
        assert builder.build(items['selector']) == items['built']

    # def test_using_simple_regex(self, builder):
    #     items = {
    #         'selector': {'label': compile(r'First')},
    #         'built': {'xpath': ".//*[local-name()='input'][not(@type) or ({})][@id=//label"
    #                         "[contains(text(), 'First')]/@for or parent::"
    #                         "label[contains(text(), 'First')]]".format(NEGATIVE_TYPES)}
    #     }
    #     assert builder.build(items['selector']) == items['built']
    #
    # def test_using_complex_regex(self, builder):
    #     items = {
    #         'selector': {'label': compile(r'([qa])st? name')},
    #         'built': {'xpath': ".//*[local-name()='input'][not(@type) or ({})]"
    #                         "[@id=//label[contains(text(), 's') and contains(text(), ' name')]"
    #                         "/@for or parent::label[contains(text(), 's') and "
    #                         "contains(text(), ' name')]]".format(NEGATIVE_TYPES),
    #                'label_element': compile(r'([qa])st? name')},
    #     }
    #     assert builder.build(items['selector']) == items['built']

    # with multiple locators

    def test_locates_using_tag_name_class_attributes_text(self, builder):
        items = {
            'selector': {'text': 'Developer', 'class_name': compile(r'c'), 'id': True},
            'built': {'xpath': ".//*[local-name()='input'][contains(@class, 'c')][not(@type) or "
                               "({})][@id]".format(NEGATIVE_TYPES),
                      'text': 'Developer'},
        }
        assert builder.build(items['selector']) == items['built']
