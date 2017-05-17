import pytest
import re
from selenium.webdriver.common.by import By

from watir_snake.elements.html_elements import HTMLElement
from watir_snake.exception import MissingWayOfFindingObjectException
from watir_snake.locators.element import Validator, SelectorBuilder
from watir_snake.locators.element.locator import Locator


def to_dict(selector):
    if isinstance(selector, list):
        dic = {}
        for k, v in zip(selector[0::2], selector[1::2]):
            dic[k] = v
        return dic
    else:
        return selector


def element(mocker, values, attrs=None):
    mock = mocker.patch('watir_snake.elements.element.Element', selector=values).return_value
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

    @pytest.mark.parametrize('finder', Locator.WD_FINDERS.items())
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
        expect_one.assert_called_once_with(By.XPATH, ".//div[@dir='bar' and @title='foo']")

    def test_handles_selector_with_no_tag_name_and_multiple_attributes(self, browser, expect_one):
        locate_one(browser, {'title': 'bar', 'dir': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//*[@dir='foo' and @title='bar']")

    def test_handles_selector_with_attribute_presence(self, browser, expect_one):
        locate_one(browser, ['data_view', True])
        expect_one.assert_called_once_with(By.XPATH, ".//*[@data-view]")

    def test_handles_selector_with_attribute_absence(self, browser, expect_one):
        locate_one(browser, ['data_view', False])
        expect_one.assert_called_once_with(By.XPATH, ".//*[not(@data-view)]")

    # with special cased selectors

    def test_normalizes_space_for_text(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'text': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[normalize-space()='foo']")

    def test_translates_caption_to_text(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'caption': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[normalize-space()='foo']")

    def test_translates_class_name_to_class(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'class_name': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[contains(concat(' ', @class, ' '), ' foo ')]")

    def test_handles_data_attributes(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'data_name': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[@data-name='foo']")

    def test_handles_aria_attributes(self, browser, expect_one):
        locate_one(browser, {'tag_name': 'div', 'aria_label': 'foo'})
        expect_one.assert_called_once_with(By.XPATH, ".//div[@aria-label='foo']")

    def test_normalizes_space_for_the_href_attribute(self, browser, expect_one):
        from watir_snake.elements.link import Anchor
        locate_one(browser, {'tag_name': 'a', 'href': 'foo'}, Anchor.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//a[normalize-space(@href)='foo']")

    def test_wraps_type_attribute_with_translate_for_upper_case_values(self, browser, expect_one):
        from watir_snake.elements.input import Input
        translated_type = "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
        locate_one(browser, {'tag_name': 'input', 'type': 'file'}, Input.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//input[{}='file']".format(translated_type))

    # uses the corresponding <label>'s @for attribute or parent::label when locating by label
    def test_uses_the_corresponding_label_for_attribute_for_parent_label_when_locating_by_label(
            self, browser, expect_one):
        from watir_snake.elements.input import Input
        translated_type = "translate(@type,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
        locate_one(browser, {'tag_name': 'input', 'type': 'text', 'label': 'foo'}, Input.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//input[{}='text' and (@id=//label[normalize-space()='foo']/@for or parent::label[normalize-space()='foo'])]".format(translated_type))

    def test_uses_label_attribute_if_it_is_valid_for_element(self, browser, expect_one):
        from watir_snake.elements.option import Option
        locate_one(browser, {'tag_name': 'option', 'label': 'foo'}, Option.ATTRIBUTES)
        expect_one.assert_called_once_with(By.XPATH, ".//option[@label='foo']")

    def test_translates_ruby_attribute_names_to_content_attribute_names(self, browser, expect_one):
        from watir_snake.elements.html_elements import Meta
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

    def test_handles_label_regexp_selector(self, browser, mocker, expect_all):
        label1 = element(mocker, values={'tag_name': 'label', 'text': 'foo'}, attrs={'for': 'bar'})
        label2 = element(mocker, values={'tag_name': 'label', 'text': 'foob'}, attrs={'for': 'baz'})
        div = element(mocker, values={'tag_name': 'div'})
        expect_all.side_effect = [[label1, label2], [div]]
        selector = {'tag_name': 'div', 'label': re.compile(r'oob')}
        assert locate_one(browser, selector) == div

    def test_returns_none_when_no_label_matching_the_regexp_is_found(self, browser, mocker, expect_all):
        expect_all.return_value = []
        selector = {'tag_name': 'div', 'label': re.compile(r'foo')}
        assert locate_one(browser, selector) is None

    def test_finds_all_if_index_is_given(self, browser, mocker, expect_all):
        elements = [element(mocker, values={'tag_name': 'div'})] * 2
        expect_all.return_value = elements
        selector = {'tag_name': 'div', 'dir': 'foo', 'index': 1}
        assert locate_one(browser, selector) == elements[1]

    def test_returns_none_if_found_element_didnt_match_the_selector_tag_name(self, browser, mocker, expect_one):
        from watir_snake.elements.input import Input
        expect_one.return_value = element(mocker, values={'tag_name': 'div'})
        selector = {'tag_name': 'input', 'xpath': '//div'}
        assert locate_one(browser, selector, Input.ATTRIBUTES) is None

    # errors

    def test_raises_correct_exception_if_index_is_not_an_integer(self, browser, mocker, expect_all):
        with pytest.raises(TypeError) as e:
            selector = {'tag_name': 'div', 'index': 'bar'}
            locate_one(browser, selector)
        assert e.value.message == "expected {}, got 'bar':{}".format(int, str)

    def test_raises_correct_exception_if_selector_value_is_not_a_string_regexp_or_boolean(self, browser, mocker, expect_all):
        with pytest.raises(TypeError) as e:
            selector = {'tag_name': 123}
            locate_one(browser, selector)
        assert e.value.message == "expected one of [{}, {}, {}], got 123:{}".format(str, re._pattern_type, bool, int)

    def test_raises_correct_exception_if_the_attribute_is_not_valid(self, browser, mocker, expect_all):
        from watir_snake.elements.input import Input
        with pytest.raises(MissingWayOfFindingObjectException) as e:
            selector = {'tag_name': 'input', 'href': 'foo'}
            locate_one(browser, selector, Input.ATTRIBUTES)
        assert e.value.message == "invalid attribute: {}".format('href')


# class TestElementLocatorFindsSeveralElements(object):

# by delegating to Selenium

#     describe "by delegating to Selenium" do
#       SELENIUM_SELECTORS.each do |loc|
#         it "delegates to Selenium's #{loc} locator" do
#           expect_all(loc, "bar").and_return([element(tag_name: "div")])
#           locate_all(loc => "bar")
#         end
#       end
#     end
#
#     describe "with an empty selector" do
#       it "finds all when an empty selctor is given" do
#         expect_all :xpath, './/*'
#         locate_all({})
#       end
#     end
#
#     describe "with selectors not supported by Selenium" do
#       it "handles selector with tag name and a single attribute" do
#         expect_all :xpath, ".//div[@dir='foo']"
#         locate_all tag_name: "div",
#                    dir: "foo"
#       end
#
#       it "handles selector with tag name and multiple attributes" do
#         expect_all :xpath, ".//div[@dir='foo' and @title='bar']"
#         locate_all [:tag_name, "div",
#                     :dir     , "foo",
#                     :title   , 'bar']
#       end
#     end
#
#     describe "with regexp selectors" do
#       it "handles selector with tag name and a single regexp attribute" do
#         elements = [
#           element(tag_name: "div", attributes: { class: "foo" }),
#           element(tag_name: "div", attributes: { class: "foob"}),
#           element(tag_name: "div", attributes: { class: "doob"}),
#           element(tag_name: "div", attributes: { class: "noob"})
#         ]
#
#         expect_all(:xpath, "(.//div)[contains(@class, 'oob')]").and_return(elements)
#         expect(locate_all(tag_name: "div", class: /oob/)).to eq elements.last(3)
#       end
#
#       it "handles mix of string and regexp attributes" do
#         elements = [
#           element(tag_name: "div", attributes: { dir: "foo", title: "bar" }),
#           element(tag_name: "div", attributes: { dir: "foo", title: "baz" }),
#           element(tag_name: "div", attributes: { dir: "foo", title: "bazt"})
#         ]
#
#         expect_all(:xpath, "(.//div[@dir='foo'])[contains(@title, 'baz')]").and_return(elements)
#
#         selector = {
#           tag_name: "div",
#           dir: "foo",
#           title: /baz/
#         }
#
#         expect(locate_all(selector)).to eq elements.last(2)
#       end
#
#       context "and xpath" do
#         it "converts a leading run of regexp literals to a contains() expression" do
#           elements = [
#             element(tag_name: "div", attributes: { class: "foo" }),
#             element(tag_name: "div", attributes: { class: "foob" }),
#             element(tag_name: "div", attributes: { class: "bar" })
#           ]
#
#           expect_all(:xpath, "(.//div)[contains(@class, 'fo')]").and_return(elements.first(2))
#
#           expect(locate_one(tag_name: "div", class: /fo.b$/)).to eq elements[1]
#         end
#
#         it "converts a trailing run of regexp literals to a contains() expression" do
#           elements = [
#             element(tag_name: "div", attributes: { class: "foo" }),
#             element(tag_name: "div", attributes: { class: "foob" })
#           ]
#
#           expect_all(:xpath, "(.//div)[contains(@class, 'b')]").and_return(elements.last(1))
#
#           expect(locate_one(tag_name: "div", class: /^fo.b/)).to eq elements[1]
#         end
#
#         it "converts a leading and a trailing run of regexp literals to a contains() expression" do
#           elements = [
#             element(tag_name: "div", attributes: { class: "foo" }),
#             element(tag_name: "div", attributes: { class: "foob" })
#           ]
#
#           expect_all(:xpath, "(.//div)[contains(@class, 'fo') and contains(@class, 'b')]").
#             and_return(elements.last(1))
#
#           expect(locate_one(tag_name: "div", class: /fo.b/)).to eq elements[1]
#         end
#
#         it "does not try to convert case insensitive expressions" do
#           elements = [
#             element(tag_name: "div", attributes: { class: "foo" }),
#             element(tag_name: "div", attributes: { class: "foob"})
#           ]
#
#           expect_all(:xpath, ".//div").and_return(elements.last(1))
#
#           expect(locate_one(tag_name: "div", class: /FOOB/i)).to eq elements[1]
#         end
#
#         it "does not try to convert expressions containing '|'" do
#           elements = [
#             element(tag_name: "div", attributes: { class: "foo" }),
#             element(tag_name: "div", attributes: { class: "foob"})
#           ]
#
#           expect_all(:xpath, ".//div").and_return(elements.last(1))
#
#           expect(locate_one(tag_name: "div", class: /x|b/)).to eq elements[1]
#         end
#       end
#     end
#
#     describe "errors" do
#       it "raises ArgumentError if :index is given" do
#         expect { locate_all(tag_name: "div", index: 1) }.to \
#         raise_error(ArgumentError, "can't locate all elements by :index")
#       end
#     end
#   end
#
# end
