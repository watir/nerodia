import pytest
from selenium.webdriver.remote.webelement import WebElement

from nerodia.locators.text_field.matcher import Matcher


def ignored(*args, **kwargs):
    pass


@pytest.fixture
def matcher(browser_mock):
    matcher = Matcher(browser_mock, {})
    matcher._deprecate_text_regexp = ignored
    yield matcher


def wd_element(mocker, values, attrs=None):
    mock = mocker.MagicMock(spec=WebElement)
    attrs = attrs if attrs else {}
    mock.get_attribute.side_effect = lambda x: attrs.get(x)
    for key, value in values.items():
        setattr(mock, key, value)
    return mock


class TestMatch(object):

    # input element

    def test_converts_text_to_value(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'input'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'tag_name': 'input'}, attrs={'value': 'Foob'}),
        ]
        values_to_match = {'text': 'Foob'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1]]

    def test_converts_label_to_value(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'input'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'tag_name': 'input'}, attrs={'value': 'Foob'}),
        ]
        values_to_match = {'label': 'Foob'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1]]

    def test_converts_visible_text_to_value(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'input'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'tag_name': 'input'}, attrs={'value': 'Foob'}),
        ]
        values_to_match = {'visible_text': 'Foob'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1]]

    # label element

    def test_converts_value_to_text(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'}),
            wd_element(mocker, values={'tag_name': 'label', 'text': 'Foob'}),
        ]
        values_to_match = {'value': 'Foob'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1]]

        assert not elements[0].get_attribute.called
        assert not elements[1].get_attribute.called

    def test_converts_label_to_text(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'}),
            wd_element(mocker, values={'tag_name': 'label', 'text': 'Foob'}),
        ]
        values_to_match = {'label': 'Foob'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1]]

        assert not elements[0].get_attribute.called
        assert not elements[1].get_attribute.called

    def test_returns_empty_list_if_element_is_not_an_input(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'wrong', 'value': 'foo'}),
            wd_element(mocker, values={'tag_name': 'wrong', 'value': 'bar'}),
        ]
        values_to_match = {'tag_name': 'input', 'value': 'foo'}

        assert matcher.match(elements, values_to_match, 'all') == []
