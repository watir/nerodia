# -*- coding: utf-8 -*-

from collections import OrderedDict
from re import IGNORECASE, compile

import pytest

from nerodia.elements.html_elements import HTMLElement
from nerodia.exception import LocatorException
from nerodia.locators.element.selector_builder import SelectorBuilder

ATTRIBUTES = HTMLElement.ATTRIBUTES


@pytest.fixture
def builder(browser_mock):
    yield SelectorBuilder(ATTRIBUTES, browser_mock)


def element_builder(element_mock, scope_built=None):
    scope_built = scope_built or {'xpath': ".//*[local-name()='div'][@id='table-rows-test']"}
    builder = SelectorBuilder(ATTRIBUTES, element_mock)
    element_mock.selector_builder = builder
    element_mock.selector_builder.built = scope_built
    return builder


class TestBuild(object):
    def test_without_any_elements(self, builder):
        items = {
            'selector': {},
            'built': {'xpath': './/*'},
            'tag_name': 'html'
        }
        assert builder.build(items['selector']) == items['built']

    # with xpath or css

    def test_locates_with_xpath_only(self, builder):
        items = {
            'selector': {'xpath': './/div'},
            'built': {'xpath': './/div'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_with_css_only(self, builder):
        items = {
            'selector': {'css': 'div'},
            'built': {'css': 'div'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_when_attributes_combined_with_xpath(self, builder):
        items = {
            'selector': {'xpath': './/div', 'random': 'foo'},
            'built': {'xpath': './/div', 'random': 'foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_locates_when_attributes_combined_with_css(self, builder):
        items = {
            'selector': {'css': 'div', 'random': 'foo'},
            'built': {'css': 'div', 'random': 'foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_using_xpath_and_css(self, builder):
        message_parts = ["Can not locate element with", "'xpath'", "'css'"]
        with pytest.raises(LocatorException) as e:
            builder.build({'xpath': './/*', 'css': 'div'})
        assert all(part in e.value.args[0] for part in message_parts)

    def test_raises_exception_when_not_a_string(self, builder):
        from nerodia.locators.element.selector_builder import STRING_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_TYPES, int)
        with pytest.raises(TypeError) as e:
            builder.build({'xpath': 7})
        assert e.value.args[0] == msg

    # with tag_name

    def test_with_string_equals(self, builder):
        items = {
            'selector': {'tag_name': 'div'},
            'built': {'xpath': ".//*[local-name()='div']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_simple_regexp_contains(self, builder):
        items = {
            'selector': {'tag_name': compile(r'div')},
            'built': {'xpath': ".//*[contains(local-name(), 'div')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_not_a_string_or_regexp(self, builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            builder.build({'tag_name': 7})
        assert e.value.args[0] == msg

    # with class names

    def test_class_name_is_converted_to_class(self, builder):
        items = {
            'selector': {'class_name': 'user'},
            'built': {'xpath': ".//*[contains(concat(' ', @class, ' '), ' user ')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_class_name_values_with_spaces(self, builder):
        items = {
            'selector': {'class_name': 'multiple classes here'},
            'built': {
                'xpath': ".//*[contains(concat(' ', @class, ' '), ' multiple classes here ')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_list_of_string_concatenates_with_and(self, builder):
        items = {
            'selector': {'class_name': ['multiple', 'here']},
            'built': {'xpath': ".//*[contains(concat(' ', @class, ' '), ' multiple ') and "
                               "contains(concat(' ', @class, ' '), ' here ')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_merges_values_when_class_and_class_name_are_both_used(self, builder):
        items = {
            'selector': {'class': 'foo', 'class_name': 'bar'},
            'built': {'xpath': ".//*[contains(concat(' ', @class, ' '), ' foo ') and "
                               "contains(concat(' ', @class, ' '), ' bar ')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_simple_regexp_contains(self, builder):
        items = {
            'selector': {'class_name': compile(r'use')},
            'built': {'xpath': ".//*[contains(@class, 'use')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_negated_string_concatenates_with_not(self, builder):
        items = {
            'selector': {'class_name': '!multiple'},
            'built': {'xpath': ".//*[not(contains(concat(' ', @class, ' '), ' multiple '))]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_single_boolean_true_provides_the_at(self, builder):
        items = {
            'selector': {'class_name': True},
            'built': {'xpath': './/*[@class]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_single_boolean_false_provides_the_not_at(self, builder):
        items = {
            'selector': {'class_name': False},
            'built': {'xpath': './/*[not(@class)]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_list_of_mixed_string_regexp_boolean_contains_and_concatenates_with_and_and_not(self, builder):
        items = {
            'selector': {'class_name': [compile(r'mult'), 'classes', '!here']},
            'built': {
                'xpath': ".//*[contains(@class, 'mult') and contains(concat(' ', @class, ' '), "
                         "' classes ') and not(contains(concat(' ', @class, ' '), ' here '))]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_empty_string_finds_elements_without_class(self, builder):
        items = {
            'selector': {'class_name': ''},
            'built': {'xpath': './/*[not(@class)]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_empty_list_finds_elements_without_class(self, builder):
        items = {
            'selector': {'class_name': []},
            'built': {'xpath': './/*[not(@class)]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_not_a_string_regexp_list(self, builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES + [bool], int)
        with pytest.raises(TypeError) as e:
            builder.build({'class_name': 7})
        assert e.value.args[0] == msg

    def test_raises_exception_when_list_values_are_not_a_str_or_regexp(self, builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES + [bool], int)
        with pytest.raises(TypeError) as e:
            builder.build({'class_name': [7]})
        assert e.value.args[0] == msg

    # with attributes as predicates

    def test_with_href_attribute(self, builder):
        items = {
            'selector': {'href': 'watirspec.css'},
            'built': {'xpath': ".//*[normalize-space(@href)='watirspec.css']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_string_attribute(self, builder):
        items = {
            'selector': {'id': 'user_new'},
            'built': {'xpath': ".//*[@id='user_new']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_true_no_equals(self, builder):
        items = {
            'selector': {'tag_name': 'input', 'name': True},
            'built': {'xpath': ".//*[local-name()='input'][@name]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_false_not_with_no_equals(self, builder):
        items = {
            'selector': {'tag_name': 'input', 'name': False},
            'built': {'xpath': ".//*[local-name()='input'][not(@name)]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_multiple_attributes_no_equals_and_not_with_no_equals_and_equals(self, builder):
        items = {
            'selector': OrderedDict([('readonly', True), ('foo', False), ('id', 'good_luck')]),
            'built': {'xpath': ".//*[@readonly and not(@foo) and @id='good_luck']"}
        }
        assert builder.build(items['selector']) == items['built']

    # with attributes as partials

    def test_with_regexp(self, builder):
        items = {
            'selector': {'name': compile(r'user')},
            'built': {'xpath': ".//*[contains(@name, 'user')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_multiple_regexp_attributes_separated_by_and(self, builder):
        items = {
            'selector': OrderedDict([('readonly', compile(r'read')), ('id', compile(r'good'))]),
            'built': {'xpath': ".//*[contains(@readonly, 'read') and contains(@id, 'good')]"}
        }
        assert builder.build(items['selector']) == items['built']

    # text

    def test_string_uses_normalize_space_equals(self, builder):
        items = {
            'selector': {'text': 'Add user'},
            'built': {'xpath': ".//*[normalize-space()='Add user']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_with_caption_attribute(self, builder):
        items = {
            'selector': {'caption': 'Add user'},
            'built': {'xpath': ".//*[normalize-space()='Add user']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_text_is_not_a_str_or_regexp(self, builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            builder.build({'text': 7})
        assert e.value.args[0] == msg

    # with index

    def test_index_positive(self, builder):
        items = {
            'selector': {'tag_name': 'div', 'index': 7},
            'built': {'xpath': "(.//*[local-name()='div'])[8]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_negative(self, builder):
        items = {
            'selector': {'tag_name': 'div', 'index': -7},
            'built': {'xpath': "(.//*[local-name()='div'])[last()-6]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_last(self, builder):
        items = {
            'selector': {'tag_name': 'div', 'index': -1},
            'built': {'xpath': "(.//*[local-name()='div'])[last()]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_index_does_not_return_index_if_zero(self, builder):
        items = {
            'selector': {'tag_name': 'div', 'index': 0},
            'built': {'xpath': ".//*[local-name()='div']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_index_is_not_an_integer(self, builder):
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            builder.build({'index': 'foo'})
        assert e.value.args[0] == msg

    # with labels

    def test_locates_the_element_associated_with_the_label_element_located_by_the_text_of_the_provided_label_key(
            self, builder):
        items = {
            'selector': {'label': 'Cars'},
            'built': {'xpath': ".//*[@id=//label[normalize-space()='Cars']/@for or "
                               "parent::label[normalize-space()='Cars']]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_returns_a_label_element_if_complex(self, builder):
        items = {
            'selector': {'label': compile(r'Ca|rs')},
            'built': {'xpath': './/*', 'label_element': compile(r'Ca|rs')}
        }
        assert builder.build(items['selector']) == items['built']

    def test_returns_a_visible_label_element_if_complex(self, builder):
        items = {
            'selector': {'visible_label': compile(r'Ca|rs')},
            'built': {'xpath': './/*', 'visible_label_element': compile(r'Ca|rs')}
        }
        assert builder.build(items['selector']) == items['built']

    def test_does_not_use_the_label_element_when_label_is_a_valid_attribute(self, browser_mock):
        from nerodia.elements.option import Option
        builder = SelectorBuilder(Option.ATTRIBUTES, browser_mock)
        items = {
            'selector': {'tag_name': 'option', 'label': 'Germany'},
            'built': {'xpath': ".//*[local-name()='option'][@label='Germany']"}
        }
        assert builder.build(items['selector']) == items['built']

    # with adjacent locators

    def test_raises_exception_when_not_a_valid_value(self, builder):
        with pytest.raises(LocatorException, match='Unable to process adjacent locator with foo'):
            builder.build({'adjacent': 'foo', 'index': 0})

    # parent

    def test_parent_with_no_other_arguments(self, builder):
        items = {
            'selector': {'adjacent': 'ancestor', 'index': 0},
            'built': {'xpath': './ancestor::*[1]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_parent_with_index(self, builder):
        items = {
            'selector': {'adjacent': 'ancestor', 'index': 2},
            'built': {'xpath': './ancestor::*[3]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_parent_with_multiple_locators(self, builder):
        items = {
            'selector': {'adjacent': 'ancestor', 'id': True, 'tag_name': 'div',
                         'class_name': 'ancestor', 'index': 1},
            'built': {
                'xpath': "./ancestor::*[local-name()='div'][contains(concat(' ', @class, ' '), "
                         "' ancestor ')][@id][2]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_for_parent_when_text_locator_is_used(self, builder):
        with pytest.raises(LocatorException, match='Can not find parent element with text locator'):
            builder.build({'adjacent': 'ancestor', 'index': 0, 'text': 'Foo'})

    # following sibling

    def test_following_with_no_other_arguments(self, builder):
        items = {
            'selector': {'adjacent': 'following', 'index': 0},
            'built': {'xpath': './following-sibling::*[1]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_following_with_index(self, builder):
        items = {
            'selector': {'adjacent': 'following', 'index': 2},
            'built': {'xpath': './following-sibling::*[3]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_following_with_multiple_locators(self, builder):
        items = {
            'selector': {'adjacent': 'following', 'tag_name': 'div', 'class_name': 'b',
                         'index': 0, 'id': True},
            'built': {'xpath': "./following-sibling::*[local-name()='div']"
                               "[contains(concat(' ', @class, ' '), ' b ')][@id][1]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_following_with_text(self, builder):
        items = {
            'selector': {'adjacent': 'following', 'text': 'Third', 'index': 0},
            'built': {'xpath': "./following-sibling::*[normalize-space()='Third'][1]"}
        }
        assert builder.build(items['selector']) == items['built']

    # previous sibling

    def test_previous_with_no_other_arguments(self, builder):
        items = {
            'selector': {'adjacent': 'preceding', 'index': 0},
            'built': {'xpath': './preceding-sibling::*[1]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_previous_with_index(self, builder):
        items = {
            'selector': {'adjacent': 'preceding', 'index': 2},
            'built': {'xpath': './preceding-sibling::*[3]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_previous_with_multiple_locators(self, builder):
        items = {
            'selector': {'adjacent': 'preceding', 'tag_name': 'div', 'class_name': 'b',
                         'index': 0, 'id': True},
            'built': {'xpath': "./preceding-sibling::*[local-name()='div']"
                               "[contains(concat(' ', @class, ' '), ' b ')][@id][1]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_previous_with_text(self, builder):
        items = {
            'selector': {'adjacent': 'preceding', 'text': 'Second', 'index': 0},
            'built': {'xpath': "./preceding-sibling::*[normalize-space()='Second'][1]"}
        }
        assert builder.build(items['selector']) == items['built']

    # child

    def test_child_with_no_other_arguments(self, builder):
        items = {
            'selector': {'adjacent': 'child', 'index': 0},
            'built': {'xpath': './child::*[1]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_child_with_index(self, builder):
        items = {
            'selector': {'adjacent': 'child', 'index': 2},
            'built': {'xpath': './child::*[3]'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_child_with_multiple_locators(self, builder):
        items = {
            'selector': {'adjacent': 'child', 'tag_name': 'div', 'class_name': 'b',
                         'id': True, 'index': 0},
            'built': {'xpath': "./child::*[local-name()='div']"
                               "[contains(concat(' ', @class, ' '), ' b ')][@id][1]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_child_with_text(self, builder):
        items = {
            'selector': {'adjacent': 'child', 'text': 'Second', 'index': 0},
            'built': {'xpath': "./child::*[normalize-space()='Second'][1]"}
        }
        assert builder.build(items['selector']) == items['built']

    # with multiple locators

    def test_locates_using_tag_name_class_attributes_text(self, builder):
        items = {
            'selector': {'tag_name': 'div', 'class_name': 'content', 'contenteditable': 'true',
                         'text': 'Foo'},
            'built': {
                'xpath': ".//*[local-name()='div'][contains(concat(' ', @class, ' '), ' content "
                         "')][normalize-space()='Foo'][@contenteditable='true']"}
        }
        assert builder.build(items['selector']) == items['built']

    # with simple regexp

    def test_simple_regexp_handles_spaces(self, builder):
        items = {
            'selector': {'title': compile(r'od Lu')},
            'built': {'xpath': ".//*[contains(@title, 'od Lu')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_simple_regexp_handles_escaped_characters(self, builder):
        items = {
            'selector': {'src': compile(r'ages/but')},
            'built': {'xpath': ".//*[contains(@src, 'ages/but')]"}
        }
        assert builder.build(items['selector']) == items['built']

    # with complex regexp

    def test_complex_regexp_handles_wildcards(self, builder):
        items = {
            'selector': {'src': compile(r'ages.*but')},
            'built': {'xpath': ".//*[contains(@src, 'ages') and contains(@src, 'but')]",
                      'src': compile(r'ages.*but')}
        }
        assert builder.build(items['selector']) == items['built']

    def test_complex_regexp_handles_optional_characters(self, builder):
        items = {
            'selector': {'src': compile(r'ages ?but')},
            'built': {'xpath': ".//*[contains(@src, 'ages') and contains(@src, 'but')]",
                      'src': compile(r'ages ?but')}
        }
        assert builder.build(items['selector']) == items['built']

    def test_complex_regexp_handles_anchors(self, builder):
        items = {
            'selector': {'name': compile(r'^new_user_image$')},
            'built': {'xpath': ".//*[contains(@name, 'new_user_image')]",
                      'name': compile(r'^new_user_image$')}
        }
        assert builder.build(items['selector']) == items['built']

    def test_complex_regexp_handles_beginning_anchor(self, builder):
        items = {
            'selector': {'src': compile(r'^i')},
            'built': {'xpath': ".//*[starts-with(@src, 'i')]"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_complex_regexp_handles_case_insensitive(self, builder):
        items = {
            'selector': {'action': compile(r'me', flags=IGNORECASE)},
            'built': {'xpath': ".//*[contains(translate(@action,"
                               "'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ',"
                               "'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ'), "
                               "translate('me',"
                               "'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ',"
                               "'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ'))]"}
        }
        assert builder.build(items['selector']) == items['built']

    # with special cased selectors

    def test_handles_data_attributes_with_string(self, builder):
        items = {
            'selector': {'data_foo': 'user_new'},
            'built': {'xpath': ".//*[@data-foo='user_new']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_handles_aria_attributes(self, builder):
        items = {
            'selector': {'aria_foo': 'user_new'},
            'built': {'xpath': ".//*[@aria-foo='user_new']"}
        }
        assert builder.build(items['selector']) == items['built']

    def test_translates_arg_attributes_to_content_atribute_names(self, builder):
        items = {
            'selector': {'http_equiv': 'foo'},
            'built': {'xpath': ".//*[@http-equiv='foo']"}
        }
        assert builder.build(items['selector']) == items['built']

    # returns locators that cannot be directly translated

    def test_attribute_with_complicated_regexp_at_end(self, builder):
        items = {
            'selector': {'action': compile(r'me$')},
            'built': {'xpath': ".//*[contains(@action, 'me')]",
                      'action': compile(r'me$')}
        }
        assert builder.build(items['selector']) == items['built']

    def test_class_with_complicated_regexp(self, builder):
        items = {
            'selector': {'class_name': compile(r'he?r')},
            'built': {'xpath': ".//*[contains(@class, 'h') and contains(@class, 'r')]",
                      'class': [compile(r'he?r')]}
        }
        assert builder.build(items['selector']) == items['built']

    def test_not_translated_visible(self, builder):
        items = {
            'selector': {'tag_name': 'div', 'visible': True},
            'built': {'xpath': ".//*[local-name()='div']", 'visible': True}
        }
        assert builder.build(items['selector']) == items['built']

    def test_not_translated_not_visible(self, builder):
        items = {
            'selector': {'tag_name': 'span', 'visible': False},
            'built': {'xpath': ".//*[local-name()='span']", 'visible': False},
        }
        assert builder.build(items['selector']) == items['built']

    def test_not_translated_visible_text(self, builder):
        items = {
            'selector': {'tag_name': 'span', 'visible_text': 'foo'},
            'built': {'xpath': ".//*[local-name()='span']", 'visible_text': 'foo'}
        }
        assert builder.build(items['selector']) == items['built']

    def test_raises_exception_when_visible_is_not_a_boolean(self, builder):
        msg = "expected one of {!r}, got 'foo':{}".format([bool], str)
        with pytest.raises(TypeError) as e:
            builder.build({'visible': 'foo'})
        assert e.value.args[0] == msg

    def test_raises_exception_when_text_is_not_a_string_or_regexp(self, builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            builder.build({'visible_text': 7})
        assert e.value.args[0] == msg

    # with element scope

    def test_uses_scope(self, element_mock):
        scope_built = {'xpath': ".//*[local-name()='div'][@id='table-rows-test']"}
        builder = element_builder(element_mock)

        items = {
            'selector': {'tag_name': 'div'},
            'built': {'xpath': "({})[1]//*[local-name()='div']".format(scope_built['xpath'])}
        }
        assert builder.build(items['selector']) == items['built']

    def test_does_not_use_scope_if_selector_is_a_css(self, element_mock):
        selector = {'css': 'div'}
        builder = element_builder(element_mock)

        build_selector = builder.build(selector)
        assert build_selector.pop('scope', None) is not None
        assert build_selector == selector

    def test_does_not_use_scope_if_selector_is_an_xpath(self, element_mock):
        selector = {'xpath': './/*'}
        builder = element_builder(element_mock)

        build_selector = builder.build(selector)
        assert build_selector.pop('scope', None) is not None
        assert build_selector == selector

    def test_does_not_use_scope_if_selector_has_adjacent(self, element_mock):
        builder = element_builder(element_mock)
        selector = {'adjacent': 'ancestor', 'index': 0}
        built = {'xpath': './ancestor::*[1]'}

        build_selector = builder.build(selector)
        assert build_selector.pop('scope', None) is not None
        assert build_selector == built

    # with invalid query scopes

    def test_does_not_use_scope_if_query_scope_built_has_multiple_keys(self, element_mock):
        scope_built = {'xpath': ".//*[local-name()='div']", 'visible': True}
        selector = {'tag_name': 'div'}
        built = {'xpath': ".//*[local-name()='div']"}
        builder = element_builder(element_mock, scope_built)

        build_selector = builder.build(selector)
        assert build_selector.pop('scope', None) is not None
        assert build_selector == built

    def test_does_not_use_scope_if_query_scope_uses_different_selenium_locator(self, element_mock):
        scope_built = {'css': '#foo'}
        selector = {'tag_name': 'div'}
        built = {'xpath': ".//*[local-name()='div']"}
        builder = element_builder(element_mock, scope_built)

        build_selector = builder.build(selector)
        assert build_selector.pop('scope', None) is not None
        assert build_selector == built

    # with specific element scope

    def test_does_not_use_scope_if_query_scope_is_an_iframe(self, mocker, element_mock):
        scope_built = {'xpath': ".//*[local-name()='iframe'][@id='one']"}
        from nerodia.elements.i_frame import IFrame
        frame_mock = mocker.MagicMock(spec=IFrame)
        builder = SelectorBuilder(ATTRIBUTES, frame_mock)
        frame_mock.selector_builder.built = scope_built

        selector = {'tag_name': 'div'}
        built = {'xpath': ".//*[local-name()='div']"}

        build_selector = builder.build(selector)
        assert build_selector.pop('scope', None) is not None
        assert build_selector == built

    def test_respects_case_when_locating_unknown_element_with_known_attribute(self, builder):
        assert builder.build({'hreflang': 'en'}) == {'xpath': ".//*[@hreflang='en']"}
        assert builder.build({'hreflang': compile(r'en')}) == {'xpath': ".//*[contains(@hreflang, 'en')]"}

    def test_ignores_case_when_locating_unknown_element_with_defined_attribute(self, builder):
        lhs = "translate(@lang,'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ'," \
              "'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ')"
        rhs = "translate('en','ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ'," \
              "'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ')"


        assert builder.build({'lang': 'en'}) == {'xpath': ".//*[{}={}]".format(lhs, rhs)}
        assert builder.build({'lang': compile(r'en')}) == {'xpath': ".//*[contains({}, {})]".format(lhs, rhs)}
        assert builder.build({'tag_name': compile(r'a'), 'lang': 'en'}) == {'xpath': ".//*[contains(local-name(), 'a')][{}={}]".format(lhs, rhs)}
        assert builder.build({'tag_name': compile(r'a'), 'lang': compile(r'en')}) == {'xpath': ".//*[contains(local-name(), 'a')][contains({}, {})]".format(lhs, rhs)}

    def test_ignores_case_when_attribute_is_defined_for_element(self, builder):
        lhs = "translate(@hreflang,'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ'," \
              "'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ')"
        rhs = "translate('en','ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ'," \
              "'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžšœ')"


        assert builder.build({'tag_name': 'a', 'hreflang': 'en'}) == {'xpath': ".//*[local-name()='a'][{}={}]".format(lhs, rhs)}
        assert builder.build({'tag_name': 'a', 'hreflang': compile(r'en')}) == {'xpath': ".//*[local-name()='a'][contains({}, {})]".format(lhs, rhs)}

    def test_respects_case_when_attribute_is_not_defined_for_element(self, builder):
        assert builder.build({'tag_name': 'table', 'hreflang': 'en'}) == {'xpath': ".//*[local-name()='table'][@hreflang='en']"}
        assert builder.build({'tag_name': 'table', 'hreflang': compile(r'en')}) == {'xpath': ".//*[local-name()='table'][contains(@hreflang, 'en')]"}
        assert builder.build({'tag_name': compile(r'a'), 'hreflang': 'en'}) == {'xpath': ".//*[contains(local-name(), 'a')][@hreflang='en']"}
        assert builder.build({'tag_name': compile(r'a'), 'hreflang': compile(r'en')}) == {'xpath': ".//*[contains(local-name(), 'a')][contains(@hreflang, 'en')]"}
