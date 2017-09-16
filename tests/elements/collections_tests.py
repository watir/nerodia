import pytest

pytestmark = pytest.mark.page('collections.html')


def test_returns_inner_elements_of_parent_element_having_different_html_tag(browser):
    assert len(browser.span(id='a_span').divs()) == 2


def test_returns_inner_elements_of_parent_element_having_same_html_tag(browser):
    assert len(browser.span(id='a_span').spans()) == 2


def test_returns_correct_subtype_of_elements(browser):
    from nerodia.elements.html_elements import Span
    collection = browser.span(id='a_span').spans()
    assert all(isinstance(el, Span) for el in collection)


@pytest.mark.page('nested_elements.html')
def test_can_contain_more_than_one_type_of_element(browser):
    from nerodia.elements.html_elements import Div, Span
    collection = browser.div(id='parent').children()
    assert any(isinstance(el, Span) for el in collection)
    assert any(isinstance(el, Div) for el in collection)


@pytest.mark.page('nested_elements.html')
def test_relocates_the_same_element(browser):
    collection = browser.div(id='parent').children()
    tag = collection[3].tag_name
    browser.refresh()
    assert collection[3].tag_name == tag


@pytest.mark.page('collections.html')
def test_returns_value_for_empty(browser):
    assert browser.span(id='a_span').options().is_empty


@pytest.mark.page('collections.html')
def test_locates_elements(browser, mocker):
    mock = mocker.patch('nerodia.container.Container.spans')
    mock.return_value = []
    spans = browser.span(id='a_span').spans()
    assert spans == []
