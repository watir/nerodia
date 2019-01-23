import pytest
from selenium.common.exceptions import StaleElementReferenceException

from nerodia.exception import LocatorException

pytestmark = pytest.mark.page('collections.html')


def test_returns_inner_elements_of_parent_element_having_different_html_tag(browser):
    assert len(browser.span(id='a_span').divs()) == 2


def test_returns_inner_elements_of_parent_element_having_same_html_tag(browser):
    assert len(browser.span(id='a_span').spans()) == 2


def test_returns_correct_subtype_of_elements(browser):
    from nerodia.elements.html_elements import Span
    collection = browser.span(id='a_span').spans()
    assert all(isinstance(el, Span) for el in collection)


def test_returns_correct_subtype_of_elements_without_tag_name(browser):
    from nerodia.elements.html_elements import Span
    from nerodia.elements.html_elements import Div
    collection = browser.span(id='a_span').elements()
    collection.locate()
    assert isinstance(collection[0], Div)
    assert isinstance(collection[-1], Span)


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


def test_returns_value_for_empty(browser):
    assert browser.span(id='a_span').options().is_empty


def test_locates_elements(browser, mocker):
    mock = mocker.patch('nerodia.container.Container.spans')
    mock.return_value = []
    spans = browser.span(id='a_span').spans()
    assert spans == []


def test_lazy_loads_collections_referenced_with_getitem(browser, mocker):
    mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.find_elements')
    browser.spans()[3]
    assert not mock.called


def test_does_not_relocate_collections_when_previously_evaluated(browser, mocker):
    elements = browser.spans()
    list(elements)

    mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.find_elements')

    elements[1].id
    assert not mock.called


def test_relocates_cached_elements_that_go_stale(browser):
    elements = browser.spans()
    list(elements)

    browser.refresh()
    assert elements[1].stale


def test_does_not_retrieve_tag_name_on_elements_when_specifying_tag_name(browser, mocker):
    mock = mocker.patch('selenium.webdriver.remote.webdriver.WebElement.tag_name',
                        new_callable=mocker.PropertyMock)
    browser.span(id='a_span').spans().locate()
    assert not mock.called


def test_does_not_retrieve_tag_name_on_elements_without_specifying_tag_name(browser, mocker):
    mock = mocker.patch('selenium.webdriver.remote.webdriver.WebElement.tag_name',
                        new_callable=mocker.PropertyMock)
    browser.span(id='a_span').elements().locate()
    assert not mock.called


def test_does_not_execute_script_to_retrieve_tag_names_when_specifying_tag_name(browser, mocker):
    mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.execute_script')
    browser.span(id='a_span').spans().locate()
    assert not mock.called


def test_returns_correct_containers_without_specifying_tag_name(browser):
    from nerodia.elements.html_elements import Span
    from nerodia.elements.html_elements import Div
    elements = list(browser.span(id='a_span').elements())
    assert isinstance(elements[0], Div)
    assert isinstance(elements[-1], Span)


def test_raises_exception_if_any_element_in_collection_continues_to_go_stale(browser, mocker):
    mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.execute_script')
    mock.side_effect = [StaleElementReferenceException()] * 3
    message_parts = [
        'Unable to locate element collection from',
        "'xpath': './/span'",
        'due to changing page'
    ]

    with pytest.raises(LocatorException) as e:
        list(browser.span().elements(xpath='.//span'))
    assert all(part in e.value.args[0] for part in message_parts)
