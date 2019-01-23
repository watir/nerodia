import pytest
from selenium.webdriver.remote.webelement import WebElement

from nerodia.locators.button.matcher import Matcher


@pytest.fixture
def matcher(browser_mock):
    yield Matcher(browser_mock, {})


def wd_element(mocker, values, attrs=None):
    mock = mocker.MagicMock(spec=WebElement)
    attrs = attrs if attrs else {}
    mock.get_attribute.side_effect = lambda x: attrs.get(x)
    for key, value in values.items():
        setattr(mock, key, value)
    return mock


class TestMatch(object):
    def test_value_attribute_matches_value(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'text': 'foo'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'text': 'bar'}, attrs={'value': 'bar'}),
            wd_element(mocker, values={'text': ''}, attrs={'value': 'foobar'})
        ]
        values_to_match = {'value': 'foobar'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[2]]

    def test_value_attribute_matches_text(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'text': 'foo'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'text': 'bar'}, attrs={'value': 'bar'}),
            wd_element(mocker, values={'text': 'foobar'})
        ]
        values_to_match = {'value': 'foobar'}

        assert not elements[2].get_attribute.called
        assert matcher.match(elements, values_to_match, 'all') == [elements[2]]

    def test_returns_empty_list_if_neither_value_nor_text_match(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'text': 'foo'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'text': 'bar'}, attrs={'value': 'bar'}),
            wd_element(mocker, values={'text': ''}, attrs={'value': 'foobar'})
        ]
        values_to_match = {'value': 'nope'}

        assert matcher.match(elements, values_to_match, 'all') == []

    def test_does_not_evaluate_other_parameters_if_value_locator_is_not_satisfied(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'text': 'foo'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'text': 'bar'}, attrs={'value': 'bar'}),
            wd_element(mocker, values={'text': ''}, attrs={'value': 'foobar'})
        ]
        values_to_match = {'value': 'nope', 'visible': True}

        for element in elements:
            assert not element.is_displayed.called

        assert matcher.match(elements, values_to_match, 'all') == []

    def test_does_not_calculate_value_if_not_passed_in(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'displayed': True, 'text': 'foo'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'displayed': True, 'text': 'bar'}, attrs={'value': 'bar'}),
        ]
        values_to_match = {'visible': False}

        assert not elements[0].get_attribute.called
        assert not elements[1].get_attribute.called

        assert matcher.match(elements, values_to_match, 'all') == []

    def test_returns_empty_list_if_element_is_an_input_or_button_element(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'wrong', 'text': 'foob'}, attrs={'value': 'foo'}),
            wd_element(mocker, values={'tag_name': 'wrong', 'text': 'bar'}, attrs={'value': 'bar'}),
        ]
        values_to_match = {'tag_name': 'button', 'value': 'foo'}

        assert matcher.match(elements, values_to_match, 'all') == []

    def test_returns_empty_list_if_element_is_an_input_element_with_wrong_type(self, mocker, matcher):
        elements = [
            wd_element(mocker, values={'tag_name': 'input', 'text': 'foob'}, attrs={'value': 'foo', 'type': 'radio'}),
            wd_element(mocker, values={'tag_name': 'input', 'text': 'bar'}, attrs={'value': 'bar', 'type': 'radio'}),
        ]
        values_to_match = {'tag_name': 'button', 'value': 'foo'}

        assert matcher.match(elements, values_to_match, 'all') == []
