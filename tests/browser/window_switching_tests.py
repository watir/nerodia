import os
import re

import pytest

from nerodia.exception import NoMatchingWindowFoundException
from nerodia.wait.wait import Wait, TimeoutError
from nerodia.window import Window
from nerodia.window_collection import WindowCollection
from tests.browser.wait_tests import executed_within


@pytest.fixture
def multiple_windows(browser, page):
    url = page.url('window_switching.html')
    browser.goto(url)
    browser.link(id='open').click()
    browser.windows().wait_until(lambda w: len(w) == 2)
    yield
    original = browser.original_window.use()
    for window in browser.windows():
        if window != original:
            window.close()


@pytest.fixture
def current_window(browser, page):
    url = page.url('window_switching.html')
    browser.goto(url)
    browser.link(id='open').click()
    Wait.until(lambda: len(browser.windows()) == 2)
    browser.window(title='closeable window').use()
    browser.link(id='close').click()
    Wait.until(lambda: len(browser.windows()) == 1)
    yield
    browser.window(index=0).use()
    for window in browser.windows()[1:]:
        window.close()


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestBrowserWindows(object):
    def test_returns_a_window_collection(self, browser):
        assert isinstance(browser.windows(), WindowCollection)

    def test_stores_window_instances(self, browser):
        assert all((isinstance(win, Window) for win in browser.windows(title='closeable window')))

    def test_filters_windows_to_match_the_given_selector(self, browser):
        assert len(browser.windows(title='closeable window')) == 1

    def test_raises_correct_exception_if_the_windows_selector_is_invalid(self, browser):
        with pytest.raises(ValueError):
            browser.windows(name='foo')

    def test_returns_an_empty_array_if_no_window_matches_the_selector(self, browser):
        assert browser.windows(title='noop').is_empty


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestBrowserWindow(object):
    def test_finds_window_by_url(self, browser):
        assert isinstance(browser.window(url=re.compile(r'closeable\.html')).use(), Window)

    def test_finds_window_by_title(self, browser):
        assert isinstance(browser.window(title='closeable window').use(), Window)

    def test_finds_window_by_index(self, browser):
        assert isinstance(browser.window(index=1).use(), Window)

    def test_finds_window_by_element(self, browser):
        assert isinstance(browser.window(element=browser.link(id='close')).use(), Window)

    def test_finds_window_multiple_values(self, browser):
        win = browser.window(url=re.compile(r'closeable\.html'), title='closeable window').use()
        assert isinstance(win, Window)

    def test_should_not_find_incorrect_handle(self, browser):
        assert not browser.window(handle='bar').present

    def test_returns_current_window_if_no_argument_is_given(self, browser):
        assert re.search(r'window_switching\.html', browser.window().url)

    def test_stores_the_reference_to_a_window_when_no_argument_is_given(self, browser):
        original = browser.window()
        browser.window(index=1).use()
        assert re.search(r'window_switching\.html', original.url)

    def test_executes_within_window_context(self, browser):
        with browser.window(title='closeable window') as window:
            link = browser.link(id='close')
            assert link.exists
            link.click()
            window.wait_until_not(method=lambda w: w.present)
        assert len(browser.windows()) == 1

    def test_raises_correct_exception_if_the_window_selector_is_invalid(self, browser):
        with pytest.raises(ValueError):
            browser.window(name='foo')

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_no_window_matches_the_selector(self, browser):
        with pytest.raises(NoMatchingWindowFoundException):
            browser.window(title='noop').use()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_if_no_window_at_given_index(self, browser):
        with pytest.raises(NoMatchingWindowFoundException):
            browser.window(index=100).use()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_attempting_to_use_window_with_wrong_handle(self, browser):
        with pytest.raises(NoMatchingWindowFoundException):
            browser.window(handle='bar').use()


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestSwitchWindow():
    def test_switches_to_second_window(self, browser):
        original_window = browser.window()
        browser.switch_window()
        new_window = browser.window()
        assert original_window != new_window
        assert all(win in browser.windows() for win in [original_window, new_window])

    def test_returns_an_instance_of_window(self, browser):
        assert isinstance(browser.switch_window(), Window)

    def test_times_out_if_there_is_no_second_window(self, browser):
        for window in browser.windows():
            if browser.window() != window:
                window.close()
        with pytest.raises(TimeoutError, match=r"waiting for true condition on.*title='window "
                                               r"switching'.*"):
            browser.switch_window()

    def test_provides_previous_window_value_to_original_window(self, browser):
        browser.switch_window()
        assert browser.original_window is not None

    def test_waits_for_second_window(self, browser):
        for window in browser.windows():
            if browser.window() != window:
                window.close()
        def func():
            browser.link(id='delayed').click()
            browser.switch_window()

        result, duration = executed_within(func, min=1)
        assert result, f'New window was not found between 1 and 2 seconds! ({duration})'


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestWindows(object):
    # close
    # TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1280517
    def test_closes_a_window(self, browser):
        browser.link(id='open').click()
        Wait.until(lambda: len(browser.windows()) == 3)
        browser.window(title='closeable window').close()
        assert len(browser.windows()) == 2

    # TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1280517
    def test_closes_the_current_window(self, browser):
        browser.link(id='open').click()
        Wait.until(lambda: len(browser.windows()) == 3)
        window = browser.window(title='closeable window').use()
        window.close()
        assert len(browser.windows()) == 2

    # use

    def test_switches_to_the_window(self, browser):
        browser.window(title='closeable window').use()
        assert browser.title == 'closeable window'

    # current

    def test_returns_true_if_it_is_the_current_window(self, browser):
        assert browser.window(title=browser.title).is_current

    def test_returns_false_if_it_is_not_the_current_window(self, browser):
        assert not browser.window(title='closeable window').is_current

    # title

    def test_returns_the_title_of_the_window(self, browser):
        titles = [window.title for window in browser.windows()]
        assert len(titles) == 2
        assert 'window switching' in titles
        assert 'closeable window' in titles

    # url

    def test_returns_the_url_of_the_window(self, browser):
        urls = [window.url for window in browser.windows()]
        assert len(urls) == 2
        assert len(list(filter(lambda w: re.search(r'window_switching\.html', w.url),
                               browser.windows()))) == 1
        assert len(list(filter(lambda w: re.search(r'closeable\.html', w.url),
                               browser.windows()))) == 1

    def test_does_not_change_the_current_window_when_checking_url(self, browser):
        assert re.search(r'window_switching\.html', browser.url)
        assert next((w for w in browser.windows() if re.search(r'closeable\.html', w.url)),
                    None) is not None
        assert re.search(r'window_switching\.html', browser.url)

    # eql

    def test_knows_when_two_windows_are_equal(self, browser):
        assert browser.window() == browser.window(title='window switching')

    def test_knows_when_two_windows_are_not_equal(self, browser):
        assert browser.window(title='closeable window') != browser.window(title='window_switching')

    # handle

    def test_does_not_find_if_not_matching(self, browser):
        assert browser.window(title='noop').handle is None

    def test_finds_window_by_url(self, browser):
        assert browser.window(url=re.compile(r'closeable.html')).handle is not None

    def test_finds_window_by_title(self, browser):
        assert browser.window(title='closeable window').handle is not None

    def test_finds_window_by_index(self, browser):
        assert browser.window(index=1).handle is not None

    def test_finds_window_by_element(self, browser):
        assert browser.window(element=browser.link(id='close')).handle is not None


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestWindow(object):
    # with a closed window
    # exists
    # TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1280517
    def test_returns_false_if_previously_refrenced_window_is_closed(self, browser):
        window = browser.window(title='closeable window').use()
        browser.link(id='close').click()
        Wait.until(lambda: len(browser.windows()) == 1)
        assert not window.present

    # TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1280517
    def test_returns_false_if_closed_window_is_referenced(self, browser):
        closed = browser.window(title='closeable window').use()
        browser.link(id='close').click()
        Wait.until(lambda: len(browser.windows()) == 1)
        assert not closed.present

    def test_returns_false_if_window_closes_during_iteration(self, browser, mocker):
        from nerodia.wait.wait import Wait
        browser.window(title='closeable window').use()
        original_handle = browser.original_window.window_handle
        handles = [x.window_handle for x in browser.windows()]

        browser.link(id='close').click()
        Wait.until(lambda: len(browser.windows()) == 1)

        mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.window_handles')
        mock.side_effect = [handles, [original_handle]]

        assert browser.window(title='closeable window').exists is False

    # current

    def test_returns_false_if_the_referenced_window_is_closed(self, browser):
        original = browser.window()
        browser.window(title='closeable window').use()
        original.close()
        assert not original.is_current

    # eql

    def test_returns_false_when_checking_equivalence_to_a_closed_window(self, browser):
        original = browser.window()
        other = browser.window(index=1).use()
        original.close()
        assert other != original

    # use

    # TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1223277
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_attempting_to_use_closed_referenced_window(self, browser):
        with pytest.raises(NoMatchingWindowFoundException):
            original = browser.window()
            browser.window(index=1).use()
            original.close()
            original.use()

    # TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1223277
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_attempting_to_use_current_window_if_it_is_closed(self, browser):
        with pytest.raises(NoMatchingWindowFoundException):
            closed = browser.window(title='closeable window').use()
            browser.link(id='close').click()
            Wait.until(lambda: len(browser.windows()) == 1)
            closed.use()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_using_an_element_on_a_closed_window(self, browser):
        browser.window(title='closeable window').use()
        browser.link(id='close').click()
        with pytest.raises(NoMatchingWindowFoundException) as e:
            browser.link().text
        assert e.value.args[0] == 'browser window was closed'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_locating_a_closed_window(self, browser, mocker):
        browser.window(title='closeable window').use()
        handles = [x.window_handle for x in browser.windows()]
        browser.link(id='close').click()
        Wait.until(lambda: len(browser.windows()) == 1)

        mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.window_handles')
        mock.side_effect = [handles, [browser.original_window.window_handle]]

        with pytest.raises(NoMatchingWindowFoundException):
            browser.window(title='closeable window').use()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_an_exception_when_locating_a_window_closed_during_lookup(self, bkwargs, page):
        from time import sleep
        from nerodia.browser import Browser

        class Dscrpt(object):
            def __init__(slf):
                slf.method = lambda x: x.driver.title

            def __get__(slf, instance, owner):
                return slf.method(instance)

            def __set__(slf, instance, value):
                slf.method = value

        class TmpBrowser(Browser):
            title = Dscrpt()

        def title(b):
            sleep(0.5)
            return b.driver.title

        browser = TmpBrowser(**bkwargs)
        try:
            browser.goto(page.url('window_switching.html'))
            browser.link(id='open').click()
            Wait.until(lambda: len(browser.windows()) == 2)
            browser.window(title='closeable window').use()
            browser.link(id='close-delay').click()

            browser.title = title

            with pytest.raises(NoMatchingWindowFoundException):
                browser.window(title='closeable window').use()
        finally:
            browser.close()


# TODO: xfail safari, or skip
# TODO: xfail firefox https://bugzilla.mozilla.org/show_bug.cgi?id=1280517
@pytest.mark.usefixtures('current_window')
class TestCurrentWindowClosed(object):
    # present
    def test_should_find_window_by_index(self, browser):
        assert browser.window(index=0).present

    def test_should_find_window_by_url(self, browser):
        assert browser.window(url=re.compile(r'window_switching\.html')).present

    def test_should_find_window_by_title(self, browser):
        assert browser.window(title='window switching').present

    def test_should_find_window_by_element(self, browser):
        assert browser.window(element=browser.link(id='open')).present

    # use

    def test_should_switch_window_by_index(self, browser):
        assert browser.window(index=0).use().title == 'window switching'

    def test_should_switch_window_by_url(self, browser):
        assert browser.window(
            url=re.compile(r'window_switching\.html')).use().title == 'window switching'

    def test_should_switch_window_by_title(self, browser):
        assert re.search(r'window_switching\.html',
                         browser.window(title='window switching').use().url)

    def test_should_switch_window_by_element(self, browser):
        browser.window(element=browser.link(id='open')).use()
        assert 'window_switching.html' in browser.url

    def test_should_use_window_context_by_index(self, browser):
        with browser.window(index=0):
            assert browser.title == 'window switching'

    def test_should_use_window_context_by_url(self, browser):
        with browser.window(url=re.compile(r'window_switching\.html')):
            assert browser.title == 'window switching'

    def test_should_use_window_context_by_title(self, browser):
        with browser.window(title='window switching'):
            assert re.search(r'window_switching\.html', browser.url)


# TODO: xfail safari, or skip
# TODO: xfail IE
@pytest.mark.page('window_switching.html')
class TestWindowRect(object):
    def test_should_get_the_size_of_the_current_window(self, browser):
        size = browser.window().size
        assert size.width == browser.execute_script('return window.outerWidth;')
        assert size.height == browser.execute_script('return window.outerHeight;')

    def test_should_get_the_position_of_the_current_window(self, browser):
        pos = browser.window().position
        assert pos.x == browser.execute_script('return window.screenX;')
        assert pos.y == browser.execute_script('return window.screenY;')

    def test_should_resize_the_window(self, browser):
        initial_size = browser.window().size
        browser.window().resize_to(initial_size.width - 20, initial_size.height - 20)
        new_size = browser.window().size

        assert new_size.width == initial_size.width - 20
        assert new_size.height == initial_size.height - 20

    def test_should_move_the_window(self, browser):
        initial_pos = browser.window().position
        browser.window().move_to(initial_pos.x + 2, initial_pos.y + 2)
        new_pos = browser.window().position

        assert new_pos.x == initial_pos.x + 2
        assert new_pos.y == initial_pos.y + 2

    @pytest.mark.skipif(os.environ.get('CI') == 'true',
                        reason='Maximize command does not work on Travis')
    @pytest.mark.quits_browser
    def test_should_maximize_the_window(self, browser):
        initial_size = browser.window().size
        browser.window().resize_to(initial_size.width - 40, initial_size.height - 40)
        browser.wait_until(lambda b: b.window().size != initial_size)
        new_size = browser.window().size

        browser.window().maximize()
        browser.wait_until(lambda b: b.window().size != initial_size)

        final_size = browser.window().size

        assert final_size.width >= new_size.width
        assert final_size.height > new_size.height


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestWindowCollection():

    # new

    def test_returns_all_windows_by_default(self, browser):
        windows = WindowCollection(browser)
        assert len(windows) == 2

    def test_filters_available_by_url(self, browser):
        windows = WindowCollection(browser, {'url': re.compile(r'closeable.html')})
        assert len(windows) == 1

    def test_filters_available_by_title(self, browser):
        windows = WindowCollection(browser, {'title': re.compile(r'closeable')})
        assert len(windows) == 1

    def test_filters_available_by_element(self, browser):
        windows = WindowCollection(browser, {'element': browser.element(id='close')})
        assert len(windows) == 1

    def test_raises_error_if_unrecognzied_locator(self, browser):
        with pytest.raises(ValueError):
            WindowCollection(browser, {'foo': re.compile(r'closeable')})

    # size

    def test_counts_the_number_of_matching_windows(self, browser):
        assert len(WindowCollection(browser)) == 2

    # get item

    def test_returns_window_instance_at_provided_index(self, browser):
        windows = browser.windows()
        assert all((isinstance(window, Window) for window in windows))
        assert windows[0] != windows[-1]

    # equal

    def test_compares_the_equivalence_of_window_handles(self, browser):
        windows1 = browser.windows(title=re.compile(r'.*'))
        windows2 = browser.windows(url=re.compile(r'.*'))

        assert windows1 == windows2
        assert set([w.handle for w in windows1]) == set([w.handle for w in windows2])
