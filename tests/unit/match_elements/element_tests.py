from re import compile

import pytest
from selenium.webdriver.remote.webelement import WebElement

from nerodia.elements.element import Element
from nerodia.elements.html_elements import Label
from nerodia.elements.input import Input
from nerodia.locators.element.matcher import Matcher


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


def element(mocker, values, klass=Element, attrs=None):
    mock = mocker.MagicMock(spec=klass)
    attrs = attrs if attrs else {}
    mock.get_attribute.side_effect = lambda x: attrs[x]
    mock.wd = wd_element(mocker, values={})
    for key, value in values.items():
        setattr(mock, key, value)
    return mock


class TestMatchLabel(object):
    def test_returns_elements_with_for_id_pairs(self, mocker, matcher):
        input_wds = [wd_element(mocker, values={'tag_name': 'input'}, attrs={'id': 'foob_id'}),
                     wd_element(mocker, values={'tag_name': 'input'}, attrs={'id': 'bfoo_id'}),
                     wd_element(mocker, values={'tag_name': 'input'}, attrs={'id': 'foo_id'})]

        label_wds = [wd_element(mocker, values={'tag_name': 'label', 'text': 'foob'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'bfoo'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'})]

        labels = [element(mocker, values={'klass': Label, 'wd': label_wds[0]},
                          attrs={'htmlFor': 'foob_id'}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[1]},
                          attrs={'htmlFor': 'bfoo_id'}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[2]},
                          attrs={'htmlFor': 'foo_id'})]

        values_to_match = {'label_element': 'foo'}
        matcher.query_scope.labels = lambda: labels
        mocker.patch('nerodia.elements.input.Input.wd',
                     new_callable=mocker.PropertyMock).return_value = input_wds[2]

        assert matcher.match(input_wds, values_to_match, 'all') == [input_wds[2]]

    def test_returns_elements_without_for_id_pairs(self, mocker, matcher):
        input_wds = [wd_element(mocker, values={'tag_name': 'input'}),
                     wd_element(mocker, values={'tag_name': 'input'}),
                     wd_element(mocker, values={'tag_name': 'input'})]

        inputs = [wd_element(mocker, values={'klass': Input, 'wd': input_wds[0]}),
                  wd_element(mocker, values={'klass': Input, 'wd': input_wds[1]}),
                  wd_element(mocker, values={'klass': Input, 'wd': input_wds[2]})]

        label_wds = [wd_element(mocker, values={'tag_name': 'label', 'text': 'foob'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'Foo'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'})]

        labels = [element(mocker, values={'klass': Label, 'wd': label_wds[0]},
                          attrs={'htmlFor': ''}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[1]},
                          attrs={'htmlFor': ''}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[2]},
                          attrs={'htmlFor': ''})]

        values_to_match = {'label_element': 'foo'}
        matcher.query_scope.labels = lambda: labels
        labels[0].input = lambda: inputs[0]
        labels[1].input = lambda: inputs[1]
        labels[2].input = lambda: inputs[2]

        assert matcher.match(input_wds, values_to_match, 'all') == [input_wds[2]]

    def test_returns_elements_with_multiple_matching_label_text_but_first_missing_corresponding_element(self, mocker, matcher):
        input_wds = [wd_element(mocker, values={'tag_name': 'input'}),
                     wd_element(mocker, values={'tag_name': 'input'})]

        inputs = [wd_element(mocker, values={'klass': Input, 'wd': wd_element(mocker, values={'tag_name': 'input'})}),
                  wd_element(mocker, values={'klass': Input, 'wd': input_wds[1]})]

        label_wds = [wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'})]

        labels = [element(mocker, values={'klass': Label, 'wd': label_wds[0]},
                          attrs={'htmlFor': ''}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[1]},
                          attrs={'htmlFor': ''})]

        values_to_match = {'label_element': 'foo'}
        matcher.query_scope.labels = lambda: labels
        labels[0].input = lambda: inputs[0]
        labels[1].input = lambda: inputs[1]

        assert matcher.match(input_wds, values_to_match, 'all') == [input_wds[1]]

    def test_returns_an_empty_list_if_no_label_element_matches(self, mocker, matcher):
        input_wds = [wd_element(mocker, values={'tag_name': 'input'}, attrs={'id': 'foo'}),
                     wd_element(mocker, values={'tag_name': 'input'}, attrs={'id': 'bfoo'})]

        label_wds = [wd_element(mocker, values={'tag_name': 'label', 'text': 'Not this'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'Or This'})]

        labels = [element(mocker, values={'klass': Label, 'wd': label_wds[0]},
                          attrs={'htmlFor': 'foo'}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[1]},
                          attrs={'htmlFor': 'bfoo'})]

        values_to_match = {'label_element': 'foo'}
        matcher.query_scope.labels = lambda: labels

        assert matcher.match(input_wds, values_to_match, 'all') == []

    def test_returns_an_empty_list_if_matching_label_elements_do_not_have_a_corresponding_input_element(self, mocker, matcher):
        input_wds = [wd_element(mocker, values={'tag_name': 'input'}),
                     wd_element(mocker, values={'tag_name': 'input'})]

        inputs = [wd_element(mocker, values={'klass': Input, 'wd': wd_element(mocker, values={'tag_name': 'input'})}),
                  wd_element(mocker, values={'klass': Input, 'wd': wd_element(mocker, values={'tag_name': 'input'})})]

        label_wds = [wd_element(mocker, values={'tag_name': 'label', 'text': 'foob'}),
                     wd_element(mocker, values={'tag_name': 'label', 'text': 'foo'})]

        labels = [element(mocker, values={'klass': Label, 'wd': label_wds[0]},
                          attrs={'htmlFor': ''}),
                  element(mocker, values={'klass': Label, 'wd': label_wds[1]},
                          attrs={'htmlFor': ''})]

        values_to_match = {'label_element': 'foo'}
        matcher.query_scope.labels = lambda: labels
        labels[0].input = lambda: inputs[0]
        labels[1].input = lambda: inputs[1]

        assert matcher.match(input_wds, values_to_match, 'all') == []


class TestMatchOneElement(object):
    def test_by_tag_name(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'})]

        values_to_match = {'tag_name': 'span'}

        assert matcher.match(elements, values_to_match, 'first') == elements[1]

    def test_by_attribute(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'id': 'foo'}),
                    wd_element(mocker, values={}, attrs={'id': 'bar'}),
                    wd_element(mocker, values={}, attrs={'id': 'foobar'})]

        values_to_match = {'id': 'foobar'}

        assert matcher.match(elements, values_to_match, 'first') == elements[2]

    def test_by_class_list(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'class': 'foob bar'}),
                    wd_element(mocker, values={}, attrs={'class': 'bar'}),
                    wd_element(mocker, values={}, attrs={'class': 'bar foo'})]

        values_to_match = {'class': ['foo', 'bar']}

        assert matcher.match(elements, values_to_match, 'first') == elements[2]

    def test_by_positive_index(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'}),
                    wd_element(mocker, values={'tag_name': 'div'})]

        values_to_match = {'tag_name': 'div', 'index': 1}

        assert matcher.match(elements, values_to_match, 'first') == elements[2]

    def test_by_negative_index(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'}),
                    wd_element(mocker, values={'tag_name': 'div'})]

        expected = elements[2]  # reverse() down the line causes these to reverse as well

        values_to_match = {'tag_name': 'div', 'index': -1}

        assert matcher.match(elements, values_to_match, 'first') == expected

    def test_by_visibility_true(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'})]

        elements[0].is_displayed = lambda: False
        elements[1].is_displayed = lambda: True

        values_to_match = {'visible': True}

        assert matcher.match(elements, values_to_match, 'first') == elements[1]

    def test_by_visibility_false(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'})]

        elements[0].is_displayed = lambda: True
        elements[1].is_displayed = lambda: False

        values_to_match = {'visible': False}

        assert matcher.match(elements, values_to_match, 'first') == elements[1]

    def test_by_text(self, mocker, matcher):
        elements = [wd_element(mocker, values={'text': 'foo'}),
                    wd_element(mocker, values={'text': 'Foob'})]

        values_to_match = {'text': 'Foob'}

        assert matcher.match(elements, values_to_match, 'first') == elements[1]

    def test_by_visible_text(self, mocker, matcher):
        elements = [wd_element(mocker, values={'text': 'foo'}),
                    wd_element(mocker, values={'text': 'Foob'})]

        values_to_match = {'visible_text': compile(r'Foo|Bar')}

        assert matcher.match(elements, values_to_match, 'first') == elements[1]

    def test_by_href(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}, attrs={'href': 'froo.com'}),
                    wd_element(mocker, values={'tag_name': 'span'}, attrs={'href': 'bar.com'})]

        values_to_match = {'href': compile(r'foo|bar')}

        assert matcher.match(elements, values_to_match, 'first') == elements[1]

    def test_returns_none_if_found_element_doesnt_match_the_selector_tag_name(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'})]

        values_to_match = {'tag_name': 'span'}

        assert matcher.match(elements, values_to_match, 'first') is None


class TestMatchCollection(object):
    def test_by_tag_name(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'}),
                    wd_element(mocker, values={'tag_name': 'div'})]

        values_to_match = {'tag_name': 'div'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]

    def test_by_attribute(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'foo': 'foo'}),
                    wd_element(mocker, values={}, attrs={'foo': 'bar'}),
                    wd_element(mocker, values={}, attrs={'foo': 'foo'})]

        values_to_match = {'foo': 'foo'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]

    def test_by_single_class(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'class': 'foo bar cool'}),
                    wd_element(mocker, values={}, attrs={'class': 'foob bar'}),
                    wd_element(mocker, values={}, attrs={'class': 'bar foo foobar'})]

        values_to_match = {'class': 'foo'}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]

    def test_by_class_list(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'class': 'foo bar cool'}),
                    wd_element(mocker, values={}, attrs={'class': 'foob bar'}),
                    wd_element(mocker, values={}, attrs={'class': 'bar foo foobar'})]

        values_to_match = {'class': ['foo', 'bar']}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]

    def test_by_visibility_true(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'}),
                    wd_element(mocker, values={'tag_name': 'div'})]

        elements[0].is_displayed = lambda: False
        elements[1].is_displayed = lambda: True
        elements[2].is_displayed = lambda: True

        values_to_match = {'visible': True}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1], elements[2]]

    def test_by_visibility_false(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'}),
                    wd_element(mocker, values={'tag_name': 'div'})]

        elements[0].is_displayed = lambda: False
        elements[1].is_displayed = lambda: True
        elements[2].is_displayed = lambda: False

        values_to_match = {'visible': False}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]

    def test_by_text(self, mocker, matcher):
        elements = [wd_element(mocker, values={'text': 'foo'}),
                    wd_element(mocker, values={'text': 'Foob'}),
                    wd_element(mocker, values={'text': 'bBarb'})]

        values_to_match = {'text': compile(r'Foo|Bar')}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1], elements[2]]

    def test_by_visible_text(self, mocker, matcher):
        elements = [wd_element(mocker, values={'text': 'foo'}),
                    wd_element(mocker, values={'text': 'Foob'}),
                    wd_element(mocker, values={'text': 'bBarb'})]

        values_to_match = {'visible_text': compile(r'Foo|Bar')}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1], elements[2]]

    def test_by_href(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'href': 'froo.com'}),
                    wd_element(mocker, values={}, attrs={'href': 'bar.com'}),
                    wd_element(mocker, values={}, attrs={'href': 'foobar.com'})]

        values_to_match = {'href': compile(r'foo|bar')}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1], elements[2]]

    def test_returns_none_if_found_element_doesnt_match_the_selector_tag_name(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'})]

        values_to_match = {'tag_name': 'span'}

        assert matcher.match(elements, values_to_match, 'all') == []


class TestMatchRegex(object):
    def test_with_tag_name(self, mocker, matcher):
        elements = [wd_element(mocker, values={'tag_name': 'div'}),
                    wd_element(mocker, values={'tag_name': 'span'}),
                    wd_element(mocker, values={'tag_name': 'div'})]

        values_to_match = {'tag_name': compile(r'd|g')}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]

    def test_with_single_class(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'class': 'foo bar cool'}),
                    wd_element(mocker, values={}, attrs={'class': 'foob bar'}),
                    wd_element(mocker, values={}, attrs={'class': 'bar foo foobar'})]

        values_to_match = {'class': compile(r'foob|q')}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1], elements[2]]

    def test_with_class_list(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'class': 'foo bar cool'}),
                    wd_element(mocker, values={}, attrs={'class': 'foob bar'}),
                    wd_element(mocker, values={}, attrs={'class': 'bar foo foobar'})]

        values_to_match = {'class': [compile(r'foob'), compile(r'bar')]}

        assert matcher.match(elements, values_to_match, 'all') == [elements[1], elements[2]]

    def test_with_attributes(self, mocker, matcher):
        elements = [wd_element(mocker, values={}, attrs={'foo': 'foo'}),
                    wd_element(mocker, values={}, attrs={'foo': 'bar'}),
                    wd_element(mocker, values={}, attrs={'foo': 'foo'})]

        values_to_match = {'foo': compile(r'fo')}

        assert matcher.match(elements, values_to_match, 'all') == [elements[0], elements[2]]
