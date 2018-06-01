import re

import pytest
from selenium.webdriver.common.by import By

from nerodia.elements.html_elements import HTMLElement
from nerodia.locators.element import Validator, SelectorBuilder
from nerodia.locators.element.locator import Locator


def to_dict(selector):
    if isinstance(selector, list):
        dic = {}
        for k, v in zip(selector[0::2], selector[1::2]):
            dic[k] = v
        return dic
    else:
        return selector


def element(mocker, values, attrs=None):
    mock = mocker.patch('nerodia.elements.element.Element', selector=values).return_value
    attrs = attrs if attrs else {}
    mock.get_attribute.side_effect = lambda x: attrs[x]
    mock.tag_name = values.get('tag_name')
    mock.text = values.get('text', '')
    return mock


def locator(browser, selector, attrs):
    selector_builder = SelectorBuilder(browser.wd, selector, attrs or HTMLElement.ATTRIBUTES)
    return Locator(browser, selector, selector_builder, Validator())


def locate_one(browser, selector, attrs=None):
    return locator(browser, to_dict(selector), attrs).locate()


def locate_all(browser, selector, attrs=None):
    return locator(browser, to_dict(selector), attrs).locate_all()


@pytest.fixture
def expect_one(mocker):
    def spec(by, value):  # allow passing by args or kwargs
        pass

    yield mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.find_element', spec=spec)


@pytest.fixture
def expect_all(mocker):
    def spec(by, value):  # allow passing by args or kwargs
        pass

    yield mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.find_elements', spec=spec)


class TestElementLocatorFindsSingleElement(object):
    # by delegating to Selenium

    @pytest.mark.parametrize('finder', Locator.W3C_FINDERS.items())
    def test_delegates_to_seleniums_locators(self, browser, finder, expect_one):
        arg, str = finder
        locate_one(browser, {arg: 'bar'})
        expect_one.assert_called_once_with(str, 'bar')

    # with selectors not supported by selenium

    def test_handles_selector_with_tag_name_and_single_attribute(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'title': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[@title='foo']")

    def test_handles_selector_with_no_tag_name_and_single_attribute(self, browser, expect_one):
        locate_one(browser, {'title': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//*[@title='foo']")

    def test_handles_single_quotes_in_the_attribute_string(self, browser, expect_one):
        locate_one(browser, {'title': "foo and 'bar'"})
        expect_one.assert_called_once_with(By.XPATH, ".//*[@title=concat('foo and ',\"'\",'bar',\"'\",'')]")

    def test_handles_selector_with_tag_name_and_multiple_attributes(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'title': 'foo', 'dir': 'bar'})
        expect_one.assert_called_once()
        by, selector = expect_one.call_args[0]
        assert by == 'xpath'
        assert '//div' in selector
        assert 'and' in selector
        assert "@dir='bar'" in selector
        assert "@title='foo'" in selector

    def test_handles_selector_with_no_tag_name_and_multiple_attributes(self, browser, expect_one):
        locate_one(browser, {'title': 'bar', 'dir': 'foo'})
        expect_one.assert_called_once()
        by, selector = expect_one.call_args[0]
        assert by == 'xpath'
        assert '//*' in selector
        assert 'and' in selector
        assert "@dir='foo'" in selector
        assert "@title='bar'" in selector

    def test_handles_selector_with_attribute_presence(self, browser, expect_one):
        locate_one(browser, ['data_view', True])
        expect_one.assert_called_once_with(By.XPATH, ".//*[@data-view]")

    def test_handles_selector_with_attribute_absence(self, browser, expect_one):
        locate_one(browser, ['data_view', False])
        expect_one.assert_called_once_with(By.XPATH, ".//*[not(@data-view)]")

    def test_handles_selector_with_class_attribute_presense(self, browser, expect_one):
        locate_one(browser, {'class_name': True})
        expect_one.assert_called_once_with(By.XPATH, ".//*[@class]")

    def test_handles_selector_with_multiple_classes_in_list(self, browser, expect_one):
        locate_one(browser, {'class_name': ['a', 'b']})
        expect_one.assert_called_once_with(By.XPATH, ".//*[(contains(concat(' ', @class, ' '), ' a ') and contains(concat(' ', @class, ' '), ' b '))]")

    def test_handles_selector_with_multiple_classes_in_string(self, browser, expect_one):
        locate_one(browser, {'class_name': 'a b'})
        expect_one.assert_called_once_with(By.XPATH, ".//*[contains(concat(' ', @class, ' '), ' a b ')]")

    def test_handles_selector_with_tag_name_and_xpath(self, browser, mocker, expect_all):
        div1 = element(mocker, values={'tag_name': 'div'}, attrs={'class_name': 'foo'})
        span = element(mocker, values={'tag_name': 'span'}, attrs={'class_name': 'foo'})
        div2 = element(mocker, values={'tag_name': 'div'}, attrs={'class_name': 'foo'})

        expect_all.return_value = [div1, span, div2]

        selector = {'xpath': './/*[@class="foo"]', 'tag_name': 'span'}
        result = locate_one(browser, selector)

        expect_all.assert_called_once_with(By.XPATH, './/*[@class="foo"]')

        assert result.tag_name == 'span'

    def test_handles_custom_attributes(self, browser, mocker, expect_one, expect_all):
        div1 = element(mocker, values={'tag_name': 'div'}, attrs={'custom_attribute': 'foo'})
        span = element(mocker, values={'tag_name': 'span'}, attrs={'custom_attribute': 'foo'})
        div2 = element(mocker, values={'tag_name': 'div'}, attrs={'custom_attribute': 'foo'})

        expect_one.return_value = span
        expect_all.return_value = [div1, span, div2]

        selector = {'custom_attribute': 'foo', 'tag_name': 'span'}
        result = locate_one(browser, selector)

        expect_one.assert_called_once_with(By.XPATH, ".//span[@custom-attribute='foo']")

        assert result.tag_name == 'span'

    # with special cased selectors

    def test_normalizes_space_for_text(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'text': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[normalize-space()='foo']")

    def test_translates_caption_to_text(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'caption': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[normalize-space()='foo']")

    def test_handles_data_attributes(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'data_name': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[@data-name='foo']")

    def test_handles_aria_attributes(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'aria_label': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[@aria-label='foo']")

    def test_normalizes_space_for_the_href_attribute(self, browser, expect_one):
        from nerodia.elements.link import Anchor
        locate_one(browser, {'tag_name': 'a', 'href': 'foo'}, Anchor.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//a[normalize-space(@href)='foo']")

    def test_wraps_type_attribute_with_translate_for_upper_case_values(self, browser, expect_one):
        from nerodia.elements.input import Input
        translated_type = "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
        locate_one(browser, {'tag_name': 'input', 'type': 'file'}, Input.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//input[{}='file']".format(translated_type))

    # uses the corresponding <label>'s @for attribute or parent::label when locating by label
    def test_uses_the_corresponding_label_for_attribute_for_parent_label_when_locating_by_label(
            self, browser, expect_one):
        from nerodia.elements.input import Input
        translated_type = "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
        locate_one(browser, {'tag_name': 'input', 'type': 'text', 'label': 'foo'}, Input.ATTRIBUTES)
        expect_one.assert_called_once()
        by, selector = expect_one.call_args[0]
        and_parts = selector.split(' and ')
        or_parts = selector.split(' or ')
        text = "{}='text'".format(translated_type)
        id = "@id=//label[normalize-space()='foo']/@for"
        parent = "parent::label[normalize-space()='foo']"
        assert by == 'xpath'
        assert (text in and_parts[0] and id in and_parts[1]) or \
            (text in and_parts[1] and id in and_parts[0])
        assert (id in or_parts[0] and parent in or_parts[1]) or \
            (id in or_parts[1] and parent in or_parts[0])

    def test_uses_label_attribute_if_it_is_valid_for_element(self, browser, expect_one):
        from nerodia.elements.option import Option
        locate_one(browser, {'tag_name': 'option', 'label': 'foo'}, Option.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//option[@label='foo']")

    def test_translates_ruby_attribute_names_to_content_attribute_names(self, browser, expect_one):
        from nerodia.elements.html_elements import Meta
        locate_one(browser, {'tag_name': 'meta', 'http_equiv': 'foo'}, Meta.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//meta[@http-equiv='foo']")

    # with regexp selectors

    def test_handles_selector_with_tag_name_and_a_single_regexp_attribute(self, browser, mocker, expect_all):
        el1 = element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'})
        el2 = element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'})

        expect_all.return_value = [el1, el2]
        selector = {'tag_name': 'div', 'class_name': re.compile(r'oob')}
        assert locate_one(browser, selector) == el2

    def test_handles_tag_name_index_and_a_single_regexp_attribute(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'})] * 2
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'foo'), 'index': 1}
        assert locate_one(browser, selector) == elements[1]

    def test_handles_xpath_and_index_selectors(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'})] * 2
        expect_all.return_value = elements
        selector = {'xpath': './/div[@class="foo"]', 'index': 1}
        assert locate_one(browser, selector) == elements[1]

    def test_handles_css_and_index_selectors(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'})] * 2
        expect_all.return_value = elements
        selector = {'css': 'div[class="foo"]', 'index': 1}
        assert locate_one(browser, selector) == elements[1]

    def test_handles_mix_of_string_and_regexp_attributes(self, browser, mocker, expect_all):
        el1 = element(mocker, values={'tag_name': 'div'}, attrs={'dir': 'foo', 'title': 'bar'})
        el2 = element(mocker, values={'tag_name': 'div'}, attrs={'dir': 'foo', 'title': 'baz'})
        expect_all.return_value = [el1, el2]
        selector = {'tag_name': 'div', 'dir': 'foo', 'title': re.compile(r'baz')}
        assert locate_one(browser, selector) == el2

    def test_handles_data_attributes_with_regexp(self, browser, mocker, expect_all):
        el1 = element(mocker, values={'tag_name': 'div'}, attrs={'data-automation-id': 'foo'})
        el2 = element(mocker, values={'tag_name': 'div'}, attrs={'data-automation-id': 'bar'})
        expect_all.return_value = [el1, el2]
        selector = {'tag_name': 'div', 'data_automation_id': re.compile(r'bar')}
        assert locate_one(browser, selector) == el2

    def test_handles_label_regexp_selector(self, browser, mocker, expect_one, expect_all):
        fetch_mock = mocker.patch('nerodia.locators.element.locator.Locator._fetch_value')
        fetch_mock.side_effect = ['foo', 'foob']

        label1 = element(mocker, values={'tag_name': 'label', 'text': 'foo'}, attrs={'for': 'bar'})
        label2 = element(mocker, values={'tag_name': 'label', 'text': 'foob'}, attrs={'for': 'baz'})
        div = element(mocker, values={'tag_name': 'div'})
        expect_all.side_effect = [[label1, label2], [div]]
        expect_one.return_value = div
        selector = {'tag_name': 'div', 'label': re.compile(r'oob')}
        mock = mocker.patch('nerodia.elements.element.Element').return_value
        mock._execute_js.side_effect = 'oob'
        assert locate_one(browser, selector) == div

    def test_returns_none_when_no_label_matching_the_regexp_is_found(self, browser, expect_all):
        expect_all.return_value = []
        selector = {'tag_name': 'div', 'label': re.compile(r'foo')}
        assert locate_one(browser, selector) is None

    def test_finds_all_if_index_is_given(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'})] * 2
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'dir': 'foo', 'index': 1}
        assert locate_one(browser, selector) == elements[1]

    def test_returns_none_if_found_element_didnt_match_the_selector_tag_name(self, browser, mocker, expect_all):
        from nerodia.elements.input import Input
        expect_all.return_value = [element(mocker, values={'tag_name': 'div'})]
        selector = {'tag_name': 'input', 'xpath': '//div'}
        assert locate_one(browser, selector, Input.ATTRIBUTES) is None

    # errors

    def test_raises_correct_exception_if_index_is_not_an_integer(self, browser, mocker, expect_all):
        with pytest.raises(TypeError) as e:
            selector = {'tag_name': 'div', 'index': 'bar'}
            locate_one(browser, selector)
        assert e.value.args[0] == "expected {}, got 'bar':{}".format(int, str)

    def test_raises_correct_exception_if_selector_value_is_not_a_list_string_unicode_regexp_or_boolean(self, browser, mocker, expect_all):
        from nerodia.locators.element.selector_builder import SelectorBuilder
        with pytest.raises(TypeError) as e:
            selector = {'tag_name': 123}
            locate_one(browser, selector)
        expected = SelectorBuilder.VALID_WHATS + [int]
        assert e.value.args[0] == "expected one of [{}, {}, {}, {}, {}], got 123:{}".format(*expected)


class TestElementLocatorFindsSeveralElements(object):

    # by delegating to Selenium

    @pytest.mark.parametrize('finder', Locator.W3C_FINDERS.items())
    def test_delegates_to_seleniums_locators(self, browser, mocker, expect_all, finder):
        arg, str = finder
        locate_all(browser, {arg: 'bar'})
        expect_all.return_value = [element(mocker, values={'tag_name': 'div'})]
        assert expect_all.call_args_list[0][0] == (str, 'bar')

    # with an empty selector

    def test_finds_all_when_an_empty_selctor_is_given(self, browser, expect_all):
        locate_all(browser, {})
        expect_all.assert_called_once_with(By.XPATH, './/*')

    # with selectors not supported by Selenium

    def test_handles_selector_with_tag_name_and_single_attribute(self, browser, expect_all):
        locate_all(browser, {'tag_name': 'div', 'dir': 'foo'})
        expect_all.assert_called_once_with(By.XPATH, ".//div[@dir='foo']")

    def test_handles_selector_with_tag_name_and_multiple_attributes(self, browser, expect_all):
        locate_all(browser, ['tag_name', 'div', 'dir', 'foo', 'title', 'bar'])
        expect_all.assert_called_once()
        by, selector = expect_all.call_args[0]
        assert by == 'xpath'
        assert '//div' in selector
        assert 'and' in selector
        assert "@dir='foo'" in selector
        assert "@title='bar'" in selector

    def test_handles_selector_with_class_attribute_presense(self, browser, expect_all):
        locate_all(browser, {'class_name': True})
        expect_all.assert_called_once_with(By.XPATH, ".//*[@class]")

    def test_handles_selector_with_multiple_classes_in_list(self, browser, expect_all):
        locate_all(browser, {'class_name': ['a', 'b']})
        expect_all.assert_called_once_with(By.XPATH, ".//*[(contains(concat(' ', @class, ' '), ' a ') and contains(concat(' ', @class, ' '), ' b '))]")

    def test_handles_selector_with_multiple_classes_in_string(self, browser, expect_all):
        locate_all(browser, {'class_name': 'a b'})
        expect_all.assert_called_once_with(By.XPATH, ".//*[contains(concat(' ', @class, ' '), ' a b ')]")

    # with regexp selectors

    def test_handles_selector_with_tag_name_and_a_single_regexp_attribute(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'doob'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'noob'})]

        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'oob')}
        assert locate_all(browser, selector) == elements[-3:]

    def test_handles_mix_of_string_and_regexp_attributes(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'dir': 'foo', 'title': 'bar'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'dir': 'foo', 'title': 'baz'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'dir': 'foo', 'title': 'bazt'})]
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'dir': 'foo', 'title': re.compile(r'baz')}
        assert locate_all(browser, selector) == elements[-2:]

    # with regexp selectors and xpath

    def test_converts_a_leading_run_of_regexp_literals_to_a_contains_expression(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'bar'})]
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'fo.b$')}
        assert locate_one(browser, selector) == elements[1]

    def test_converts_a_trailing_run_of_regexp_literals_to_a_contains_expression(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'})]
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'^fo.b')}
        assert locate_one(browser, selector) == elements[1]

    def test_converts_a_leading_and_a_trailing_run_of_regexp_literals_to_a_contains_expression(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'})]
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'fo.b')}
        assert locate_one(browser, selector) == elements[1]

    def test_does_not_try_to_convert_case_insensitive_expressions(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'})]
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'FOOB', re.IGNORECASE)}
        assert locate_one(browser, selector) == elements[1]

    def test_does_not_try_to_convert_expressions_containing_pipe(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foo'}),
                    element(mocker, values={'tag_name': 'div'}, attrs={'class': 'foob'})]
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'class_name': re.compile(r'x|b')}
        assert locate_one(browser, selector) == elements[1]

    # errors

    def test_raises_correct_exception_if_index_is_given(self, browser, mocker, expect_all):
        with pytest.raises(ValueError) as e:
            selector = {'tag_name': 'div', 'index': 1}
            locate_all(browser, selector)
        assert e.value.args[0] == "can't locate all elements by index"
