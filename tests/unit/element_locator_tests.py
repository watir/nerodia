import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from nerodia.exception import LocatorException
from nerodia.locators.element import Matcher
from nerodia.locators.element.locator import Locator


def wd_element(mocker, values=None, attrs=None):
    mock = mocker.MagicMock(spec=WebElement)
    attrs = attrs if attrs else {}
    mock.get_attribute.side_effect = lambda x: attrs.get(x)
    if values:
        for key, value in values.items():
            setattr(mock, key, value)
    return mock


@pytest.fixture
def driver_mock(mocker):
    yield mocker.MagicMock(spec=WebDriver)


def matcher(mocker, browser_mock, selector):
    match = mocker.MagicMock(spec=Matcher)
    match.query_scope = browser_mock
    match.selector = selector
    return match


def locate_one(matcher, selector=None):
    selector = selector or {}
    return Locator(matcher).locate(selector)


def locate_all(matcher, selector=None):
    selector = selector or {}
    return Locator(matcher).locate_all(selector)


def expect_one(driver_mock, ret):
    driver_mock.find_element.return_value = ret
    return driver_mock.find_element


def expect_all(driver_mock, ret):
    driver_mock.find_elements.return_value = ret
    return driver_mock.find_element


class TestLocate(object):

    # xpath can be built to represent entire selector

    def test_locates_without_using_match(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div'}
        mtcher = matcher(mocker, browser_mock, locator)
        exp_one = expect_one(driver_mock, el)

        assert locate_one(mtcher, locator) == el
        exp_one.assert_called_once_with('xpath', locator['xpath'])
        assert not mtcher.match.called

    def test_locates_none_if_not_found(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div'}
        mtcher = matcher(mocker, browser_mock, locator)
        exp_one = expect_one(driver_mock, el)
        exp_one.side_effect = NoSuchElementException('not found')

        assert locate_one(mtcher, locator) is None

    # when SelectorBuilder result has additional locators to match

    def test_locates_using_match(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div', 'id': 'foo'}
        mtcher = matcher(mocker, browser_mock, locator)
        expect_all(driver_mock, [el])
        mtcher.match.return_value = el

        assert locate_one(mtcher, locator) == el

    def test_relocates_if_element_goes_stale(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div', 'id': 'foo'}
        mtcher = matcher(mocker, browser_mock, locator)
        expect_all(driver_mock, [el])
        mtcher.match.side_effect = [StaleElementReferenceException(), el]

        assert locate_one(mtcher, locator) == el

    def test_raises_exception_if_element_continues_to_go_stale(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div', 'id': 'foo'}
        mtcher = matcher(mocker, browser_mock, locator)
        expect_all(driver_mock, [el])
        mtcher.match.side_effect = [StaleElementReferenceException()] * 3

        message_parts = ['Unable to locate element from',
                         "'xpath': './/div'",
                         "'id': 'foo'",
                         'due to changing page']

        with pytest.raises(LocatorException) as e:
            locate_one(mtcher, locator)
        assert all(part in e.value.args[0] for part in message_parts)


class TestLocateAll(object):
    def test_locates_using_match(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div', 'id': 'foo'}
        mtcher = matcher(mocker, browser_mock, locator)
        expect_all(driver_mock, [el])
        mtcher.match.return_value = [el]

        assert locate_all(mtcher, locator) == [el]

    def test_raises_locator_exception_if_element_continues_to_go_stale(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        el = wd_element(mocker)
        locator = {'xpath': './/div', 'id': 'foo'}
        mtcher = matcher(mocker, browser_mock, locator)
        expect_all(driver_mock, [el])
        mtcher.match.side_effect = [StaleElementReferenceException()] * 3

        message_parts = ['Unable to locate element collection from',
                         "'xpath': './/div'",
                         "'id': 'foo'",
                         'due to changing page']

        with pytest.raises(LocatorException) as e:
            locate_all(mtcher, locator)
        assert all(part in e.value.args[0] for part in message_parts)

    def test_raises_argument_error_if_using_index_key(self, mocker, browser_mock, driver_mock):
        browser_mock.wd = driver_mock
        locator = {'index': 2}
        mtcher = matcher(mocker, browser_mock, locator)

        with pytest.raises(ValueError) as e:
            locate_all(mtcher, locator)
        assert e.value.args[0] == "can't locate all elements by 'index'"
