# -*- coding: utf-8 -*-

from collections import OrderedDict
from re import IGNORECASE, compile

import pytest
import six

from nerodia.elements.html_elements import HTMLElement
from nerodia.exception import LocatorException
from nerodia.locators.element.locator import Locator
from nerodia.locators.element.selector_builder import SelectorBuilder

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern

pytestmark = pytest.mark.page('forms_with_input_elements.html')

ATTRIBUTES = HTMLElement.ATTRIBUTES


@pytest.fixture
def selector_builder():
    return SelectorBuilder(ATTRIBUTES)


def verify_build(browser, selector, wd, data=None, remaining=None, scope=None, attributes=None,
                 tag_name=None):
    builder = SelectorBuilder(attributes or ATTRIBUTES)
    query_scope = scope or browser
    built = builder.build(selector)
    assert built == [wd, remaining or {}]

    if data is None and tag_name is None:
        return

    by, value = list(wd.items())[0]
    located = query_scope.wd.find_element(Locator.W3C_FINDERS[by], value)

    if data:
        assert located.get_attribute('data-locator') == data
    else:
        assert located.tag_name == tag_name


class TestBuild(object):
    def test_without_any_elements(self, browser):
        items = {
            'selector': {},
            'wd': {'xpath': './/*'},
            'tag_name': 'html'
        }
        verify_build(browser, **items)

    # with xpath or css

    def test_locates_with_xpath_only(self, browser):
        items = {
            'selector': {'xpath': './/div'},
            'wd': {'xpath': './/div'},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_locates_with_css_only(self, browser):
        items = {
            'selector': {'css': 'div'},
            'wd': {'css': 'div'},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_using_xpath_and_css(self, browser, selector_builder):
        message_parts = ["'xpath' and 'css' cannot be combined",
                         "'xpath': './/*'",
                         "'css': 'div'"]
        with pytest.raises(LocatorException) as e:
            selector_builder.build({'xpath': './/*', 'css': 'div'})
        assert all(part in e.value.args[0] for part in message_parts)

    def test_raises_exception_when_combining_with_xpath(self, browser, selector_builder):
        msg = "xpath cannot be combined with all of these locators ({'foo': 'div'})"
        with pytest.raises(LocatorException) as e:
            selector_builder.build({'xpath': './/*', 'foo': 'div'})
        assert e.value.args[0] == msg

    def test_raises_exception_when_combining_with_css(self, browser, selector_builder):
        msg = "css cannot be combined with all of these locators ({'foo': 'div'})"
        with pytest.raises(LocatorException) as e:
            selector_builder.build({'css': 'div', 'foo': 'div'})
        assert e.value.args[0] == msg

    def test_raises_exception_when_not_a_string(self, browser, selector_builder):
        from nerodia.locators.element.selector_builder import STRING_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_TYPES, int)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'xpath': 7})
        assert e.value.args[0] == msg

    # with tag_name

    def test_with_string_equals(self, browser):
        items = {
            'selector': {'tag_name': 'div'},
            'wd': {'xpath': ".//*[local-name()='div']"},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_with_simple_regexp_contains(self, browser):
        items = {
            'selector': {'tag_name': compile(r'div')},
            'wd': {'xpath': ".//*[contains(local-name(), 'div')]"},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_not_a_string_or_regexp(self, browser, selector_builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'tag_name': 7})
        assert e.value.args[0] == msg

    # with class names

    def test_class_name_is_converted_to_class(self, browser):
        items = {
            'selector': {'class_name': 'user'},
            'wd': {'xpath': ".//*[contains(concat(' ', @class, ' '), ' user ')]"},
            'data': 'form'
        }
        verify_build(browser, **items)

    def test_class_name_values_with_spaces(self, browser):
        items = {
            'selector': {'class_name': 'multiple classes here'},
            'wd': {'xpath': ".//*[contains(concat(' ', @class, ' '), ' multiple classes here ')]"},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_list_of_string_concatenates_with_and(self, browser):
        items = {
            'selector': {'class_name': ['multiple', 'here']},
            'wd': {'xpath': ".//*[contains(concat(' ', @class, ' '), ' multiple ') and "
                            "contains(concat(' ', @class, ' '), ' here ')]"},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_simple_regexp_contains(self, browser):
        items = {
            'selector': {'class_name': compile(r'use')},
            'wd': {'xpath': ".//*[contains(@class, 'use')]"},
            'data': 'form'
        }
        verify_build(browser, **items)

    def test_negated_string_concatenates_with_not(self, browser):
        items = {
            'selector': {'class_name': '!multiple'},
            'wd': {'xpath': ".//*[not(contains(concat(' ', @class, ' '), ' multiple '))]"},
            'tag_name': 'html'
        }
        verify_build(browser, **items)

    def test_single_boolean_true_provides_the_at(self, browser):
        items = {
            'selector': {'class_name': True},
            'wd': {'xpath': './/*[@class]'},
            'data': 'first div'
        }
        verify_build(browser, **items)

    def test_single_boolean_false_provides_the_not_at(self, browser):
        items = {
            'selector': {'class_name': False},
            'wd': {'xpath': './/*[not(@class)]'},
            'tag_name': 'html'
        }
        verify_build(browser, **items)

    def test_list_of_mixed_string_regexp_boolean_contains_and_concatenates_with_and_and_not(self, browser):
        items = {
            'selector': {'class_name': [compile(r'mult'), 'classes', '!here']},
            'wd': {'xpath': ".//*[contains(@class, 'mult') and contains(concat(' ', @class, ' '), "
                            "' classes ') and not(contains(concat(' ', @class, ' '), ' here '))]"},
            'data': 'second div'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_not_a_string_regexp_list(self, browser, selector_builder):
        msg = 'expected one of [{}, {}, {}, {}], got 7:{}'.format(Pattern, bool, six.text_type,
                                                                  six.binary_type, int)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'class_name': 7})
        assert e.value.args[0] == msg

    def test_raises_exception_when_list_values_are_not_a_str_or_regexp(self, browser, selector_builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES + [bool], int)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'class_name': [7]})
        assert e.value.args[0] == msg

    def test_raises_exception_when_class_list_is_empty(self, browser, selector_builder):
        match = "Cannot locate elements with an empty list for 'class_name'"
        with pytest.raises(LocatorException, match=match):
            selector_builder.build({'class_name': []})

    # with attributes as predicates

    def test_with_href_attribute(self, browser):
        items = {
            'selector': {'href': 'watirspec.css'},
            'wd': {'xpath': ".//*[normalize-space(@href)='watirspec.css']"},
            'data': 'link'
        }
        verify_build(browser, **items)

    def test_with_string_attribute(self, browser):
        items = {
            'selector': {'name': 'user_new'},
            'wd': {'xpath': ".//*[@name='user_new']"},
            'data': 'form'
        }
        verify_build(browser, **items)

    def test_with_true_no_equals(self, browser):
        items = {
            'selector': {'tag_name': 'input', 'name': True},
            'wd': {'xpath': ".//*[local-name()='input'][@name]"},
            'data': 'input name'
        }
        verify_build(browser, **items)

    def test_with_false_not_with_no_equals(self, browser):
        items = {
            'selector': {'tag_name': 'input', 'name': False},
            'wd': {'xpath': ".//*[local-name()='input'][not(@name)]"},
            'data': 'input nameless'
        }
        verify_build(browser, **items)

    def test_with_multiple_attributes_no_equals_and_not_with_no_equals_and_equals(self, browser):
        items = {
            'selector': OrderedDict([('readonly', True), ('foo', False), ('id', 'good_luck')]),
            'wd': {'xpath': ".//*[@readonly and not(@foo) and @id='good_luck']"},
            'data': 'Good Luck'
        }
        verify_build(browser, **items)

    # with attributes as partials

    def test_with_regexp(self, browser):
        items = {
            'selector': {'name': compile(r'user')},
            'wd': {'xpath': ".//*[contains(@name, 'user')]"},
            'data': 'form'
        }
        verify_build(browser, **items)

    def test_with_multiple_regexp_attributes_separated_by_and(self, browser):
        items = {
            'selector': OrderedDict([('readonly', compile(r'read')), ('id', compile(r'good'))]),
            'wd': {'xpath': ".//*[contains(@readonly, 'read') and contains(@id, 'good')]"},
            'data': 'Good Luck'
        }
        verify_build(browser, **items)

    # text

    def test_string_uses_normalize_space_equals(self, browser):
        items = {
            'selector': {'text': 'Add user'},
            'wd': {'xpath': ".//*[normalize-space()='Add user']"},
            'data': 'add user'
        }
        verify_build(browser, **items)

    def test_with_caption_attribute(self, browser):
        items = {
            'selector': {'caption': 'Add user'},
            'wd': {'xpath': ".//*[normalize-space()='Add user']"},
            'data': 'add user'
        }
        verify_build(browser, **items)

    def test_raises_exception_when_text_is_not_a_str_or_regexp(self, browser, selector_builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'text': 7})
        assert e.value.args[0] == msg

    # with index

    def test_index_positive(self, browser):
        items = {
            'selector': {'tag_name': 'div', 'index': 7},
            'wd': {'xpath': "(.//*[local-name()='div'])[8]"},
            'data': 'content'
        }
        verify_build(browser, **items)

    def test_index_negative(self, browser):
        items = {
            'selector': {'tag_name': 'div', 'index': -7},
            'wd': {'xpath': "(.//*[local-name()='div'])[last()-6]"},
            'data': 'second div'
        }
        verify_build(browser, **items)

    def test_index_last(self, browser):
        items = {
            'selector': {'tag_name': 'div', 'index': -1},
            'wd': {'xpath': "(.//*[local-name()='div'])[last()]"},
            'data': 'content'
        }
        verify_build(browser, **items)

    def test_index_does_not_return_index_if_zero(self, browser):
        items = {
            'selector': {'tag_name': 'div', 'index': 0},
            'wd': {'xpath': ".//*[local-name()='div']"}
        }
        verify_build(browser, **items)

    def test_raises_exception_when_index_is_not_an_integer(self, browser, selector_builder):
        msg = "expected one of {!r}, got 'foo':{}".format([int], str)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'index': 'foo'})
        assert e.value.args[0] == msg

    # with labels

    def test_locates_the_element_associated_with_the_label_element_located_by_the_text_of_the_provided_label_key(self, browser):
        items = {
            'selector': {'label': 'Cars'},
            'wd': {'xpath': ".//*[(@id=//label[normalize-space()='Cars']/@for or "
                            "parent::label[normalize-space()='Cars'])]"},
            'data': 'cars'
        }
        verify_build(browser, **items)

    def test_does_not_use_the_label_element_when_label_is_a_valid_attribute(self, browser):
        from nerodia.elements.option import Option
        items = {
            'attributes': Option.ATTRIBUTES,
            'selector': {'tag_name': 'option', 'label': 'Germany'},
            'wd': {'xpath': ".//*[local-name()='option'][@label='Germany']"},
            'data': 'Berliner'
        }
        verify_build(browser, **items)

    # with adjacent locators

    @pytest.mark.page('nested_elements.html')
    def test_raises_exception_when_not_a_valid_value(self, browser, selector_builder):
        with pytest.raises(LocatorException, match='Unable to process adjacent locator with foo'):
            selector_builder.build({'adjacent': 'foo', 'index': 0})

    # parent

    @pytest.mark.page('nested_elements.html')
    def test_parent_with_no_other_arguments(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'ancestor', 'index': 0},
            'wd': {'xpath': './ancestor::*[1]'},
            'data': 'parent'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_parent_with_index(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'ancestor', 'index': 2},
            'wd': {'xpath': './ancestor::*[3]'},
            'data': 'grandparent'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_parent_with_multiple_locators(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'ancestor', 'id': True, 'tag_name': 'div',
                         'class_name': 'ancestor', 'index': 1},
            'wd': {'xpath': "./ancestor::*[local-name()='div'][contains(concat(' ', @class, ' '), "
                            "' ancestor ')][@id][2]"},
            'data': 'grandparent'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_raises_exception_for_parent_when_text_locator_is_used(self, browser, selector_builder):
        with pytest.raises(LocatorException, match='Can not find parent element with text locator'):
            selector_builder.build({'adjacent': 'ancestor', 'index': 0, 'text': 'Foo'})

    # following sibling

    @pytest.mark.page('nested_elements.html')
    def test_following_with_no_other_arguments(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'following', 'index': 0},
            'wd': {'xpath': './following-sibling::*[1]'},
            'data': 'between_siblings1'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_following_with_index(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'following', 'index': 2},
            'wd': {'xpath': './following-sibling::*[3]'},
            'data': 'between_siblings2'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_following_with_multiple_locators(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'following', 'tag_name': 'div', 'class_name': 'b',
                         'index': 0, 'id': True},
            'wd': {'xpath': "./following-sibling::*[local-name()='div']"
                            "[contains(concat(' ', @class, ' '), ' b ')][@id][1]"},
            'data': 'second_sibling'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_following_with_text(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'following', 'text': 'Third', 'index': 0},
            'wd': {'xpath': "./following-sibling::*[normalize-space()='Third'][1]"},
            'data': 'third_sibling'
        }
        verify_build(browser, **items)

    # previous sibling

    @pytest.mark.page('nested_elements.html')
    def test_previous_with_no_other_arguments(self, browser):
        items = {
            'scope': browser.div(id='third_sibling'),
            'selector': {'adjacent': 'preceding', 'index': 0},
            'wd': {'xpath': './preceding-sibling::*[1]'},
            'data': 'between_siblings2'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_previous_with_index(self, browser):
        items = {
            'scope': browser.div(id='third_sibling'),
            'selector': {'adjacent': 'preceding', 'index': 2},
            'wd': {'xpath': './preceding-sibling::*[3]'},
            'data': 'between_siblings1'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_previous_with_multiple_locators(self, browser):
        items = {
            'scope': browser.div(id='third_sibling'),
            'selector': {'adjacent': 'preceding', 'tag_name': 'div', 'class_name': 'b',
                         'index': 0, 'id': True},
            'wd': {'xpath': "./preceding-sibling::*[local-name()='div']"
                            "[contains(concat(' ', @class, ' '), ' b ')][@id][1]"},
            'data': 'second_sibling'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_previous_with_text(self, browser):
        items = {
            'scope': browser.div(id='third_sibling'),
            'selector': {'adjacent': 'preceding', 'text': 'Second', 'index': 0},
            'wd': {'xpath': "./preceding-sibling::*[normalize-space()='Second'][1]"},
            'data': 'second_sibling'
        }
        verify_build(browser, **items)

    # child

    @pytest.mark.page('nested_elements.html')
    def test_child_with_no_other_arguments(self, browser):
        items = {
            'scope': browser.div(id='first_sibling'),
            'selector': {'adjacent': 'child', 'index': 0},
            'wd': {'xpath': './child::*[1]'},
            'data': 'child span'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_child_with_index(self, browser):
        items = {
            'scope': browser.div(id='parent'),
            'selector': {'adjacent': 'child', 'index': 2},
            'wd': {'xpath': './child::*[3]'},
            'data': 'second_sibling'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_child_with_multiple_locators(self, browser):
        items = {
            'scope': browser.div(id='parent'),
            'selector': {'adjacent': 'child', 'tag_name': 'div', 'class_name': 'b',
                         'id': True, 'index': 0},
            'wd': {'xpath': "./child::*[local-name()='div']"
                            "[contains(concat(' ', @class, ' '), ' b ')][@id][1]"},
            'data': 'second_sibling'
        }
        verify_build(browser, **items)

    @pytest.mark.page('nested_elements.html')
    def test_child_with_text(self, browser):
        items = {
            'scope': browser.div(id='parent'),
            'selector': {'adjacent': 'child', 'text': 'Second', 'index': 0},
            'wd': {'xpath': "./child::*[normalize-space()='Second'][1]"},
            'data': 'second_sibling'
        }
        verify_build(browser, **items)

    # with multiple locators

    def test_locates_using_tag_name_class_attributes_text(self, browser):
        items = {
            'selector': {'tag_name': 'div', 'class_name': 'content', 'contenteditable': 'true',
                         'text': 'Foo'},
            'wd': {'xpath': ".//*[local-name()='div'][contains(concat(' ', @class, ' '), ' content "
                            "')][normalize-space()='Foo'][@contenteditable='true']"},
            'data': 'content'
        }
        verify_build(browser, **items)

    # with simple regexp

    def test_simple_regexp_handles_spaces(self, browser):
        items = {
            'selector': {'title': compile(r'od Lu')},
            'wd': {'xpath': ".//*[contains(@title, 'od Lu')]"},
            'data': 'Good Luck'
        }
        verify_build(browser, **items)

    def test_simple_regexp_handles_escaped_characters(self, browser):
        items = {
            'selector': {'src': compile(r'ages/but')},
            'wd': {'xpath': ".//*[contains(@src, 'ages/but')]"},
            'data': 'submittable button'
        }
        verify_build(browser, **items)

    # with complex regexp

    def test_complex_regexp_handles_wildcards(self, browser):
        items = {
            'selector': {'src': compile(r'ages.*but')},
            'wd': {'xpath': ".//*[contains(@src, 'ages') and contains(@src, 'but')]"},
            'data': 'submittable button',
            'remaining': {'src': compile(r'ages.*but')}
        }
        verify_build(browser, **items)

    def test_complex_regexp_handles_optional_characters(self, browser):
        items = {
            'selector': {'src': compile(r'ages ?but')},
            'wd': {'xpath': ".//*[contains(@src, 'ages') and contains(@src, 'but')]"},
            'data': 'submittable button',
            'remaining': {'src': compile(r'ages ?but')}
        }
        verify_build(browser, **items)

    def test_complex_regexp_handles_anchors(self, browser):
        items = {
            'selector': {'name': compile(r'^new_user_image$')},
            'wd': {'xpath': ".//*[contains(@name, 'new_user_image')]"},
            'data': 'submittable button',
            'remaining': {'name': compile(r'^new_user_image$')}
        }
        verify_build(browser, **items)

    def test_complex_regexp_handles_beginning_anchor(self, browser):
        items = {
            'selector': {'src': compile(r'^i')},
            'wd': {'xpath': ".//*[starts-with(@src, 'i')]"},
            'data': 'submittable button'
        }
        verify_build(browser, **items)

    def test_complex_regexp_handles_case_insensitive(self, browser):
        items = {
            'selector': {'action': compile(r'me', flags=IGNORECASE)},
            'wd': {'xpath': ".//*[contains(translate(@action,'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇ"
                            "ÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠŒ','abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëì"
                            "íîïðñòóôõöøùúûüýþÿžšœ'), 'me')]"},
            'data': 'form'
        }
        verify_build(browser, **items)

    # returns locators that cannot be directly translated

    def test_attribute_with_complicated_regexp_at_end(self, browser):
        items = {
            'selector': {'action': compile(r'me$')},
            'wd': {'xpath': ".//*[contains(@action, 'me')]"},
            'remaining': {'action': compile(r'me$')}
        }
        verify_build(browser, **items)

    def test_class_with_complicated_regexp(self, browser):
        items = {
            'selector': {'class_name': compile(r'he?r')},
            'wd': {'xpath': ".//*[contains(@class, 'h') and contains(@class, 'r')]"},
            'remaining': {'class': [compile(r'he?r')]}
        }
        verify_build(browser, **items)

    def test_not_translated_visible(self, browser):
        items = {
            'selector': {'tag_name': 'div', 'visible': True},
            'wd': {'xpath': ".//*[local-name()='div']"},
            'remaining': {'visible': True}
        }
        verify_build(browser, **items)

    def test_not_translated_not_visible(self, browser):
        items = {
            'selector': {'tag_name': 'span', 'visible': False},
            'wd': {'xpath': ".//*[local-name()='span']"},
            'remaining': {'visible': False}
        }
        verify_build(browser, **items)

    def test_not_translated_visible_text(self, browser):
        items = {
            'selector': {'tag_name': 'span', 'visible_text': 'foo'},
            'wd': {'xpath': ".//*[local-name()='span']"},
            'remaining': {'visible_text': 'foo'}
        }
        verify_build(browser, **items)

    def test_raises_exception_when_visible_is_not_a_boolean(self, browser, selector_builder):
        msg = "expected one of {!r}, got 'foo':{}".format([bool], str)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'visible': 'foo'})
        assert e.value.args[0] == msg

    def test_raises_exception_when_text_is_not_a_string_or_regexp(self, browser, selector_builder):
        from nerodia.locators.element.selector_builder import STRING_REGEX_TYPES
        msg = 'expected one of {!r}, got 7:{}'.format(STRING_REGEX_TYPES, int)
        with pytest.raises(TypeError) as e:
            selector_builder.build({'visible_text': 7})
        assert e.value.args[0] == msg
