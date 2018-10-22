import os
import re

import pytest

from nerodia.exception import NoMatchingWindowFoundException
from nerodia.wait.wait import Wait
from nerodia.window import Window


@pytest.fixture
def multiple_windows(browser, page):
    url = page.url('window_switching.html')
    browser.goto(url)
    browser.link(id='open').click()
    Wait.until(lambda: len(browser.windows()) == 2)
    yield
    browser.window(index=0).use()
    for window in browser.windows()[1:]:
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
    browser.original_window.use()
    for window in browser.windows()[1:]:
        window.close()


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestBrowserWindows(object):
    def test_returns_an_array_of_window_handles(self, browser):
        wins = browser.windows()
        assert wins
        for win in wins:
            assert isinstance(win, Window)

    def test_only_returns_windows_matching_the_given_selector(self, browser):
        browser.wait_until(lambda b: b.window(title='closeable window').exists)
        assert len(browser.windows(title='closeable window')) == 1

    def test_raises_correct_exception_if_the_windows_selector_is_invalid(self, browser):
        with pytest.raises(ValueError):
            browser.windows(name='foo')

    def test_returns_an_empty_array_if_no_window_matches_the_selector(self, browser):
        assert browser.windows(title='noop') == []


# TODO: xfail safari, or skip
@pytest.mark.usefixtures('multiple_windows')
class TestBrowserWindow(object):
    def test_finds_window_by_url(self, browser):
        win = browser.window(url=re.compile(r'closeable\.html')).use()
        assert isinstance(win, Window)

    def test_finds_window_by_title(self, browser):
        win = browser.window(title='closeable window').use()
        assert isinstance(win, Window)

    def test_finds_window_by_index(self, browser):
        win = browser.window(index=1).use()
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
        assert titles.sort() == ['window switching', 'closeable window'].sort()

    def test_does_not_change_the_current_window_when_checking_title(self, browser):
        assert browser.title == 'window switching'
        assert next((w for w in browser.windows() if w.title == 'closeable window'),
                    None) is not None
        assert browser.title == 'window switching'

    # url

    def test_returns_the_url_of_the_window(self, browser):
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
        assert browser.window() == browser.window(index=0)

    def test_knows_when_two_windows_are_not_equal(self, browser):
        assert browser.window(index=0) != browser.window(index=1)

    # wait_until_present
    def test_times_out_waiting_for_a_non_present_window(self, browser):
        from nerodia.wait.wait import TimeoutError
        with pytest.raises(TimeoutError):
            browser.window(title='noop').wait_until(timeout=0.5, method=lambda w: w.present)


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
        browser.window(title='closeable window').use()
        browser.link(id='close').click()
        Wait.until(lambda: len(browser.windows()) == 1)
        assert not browser.window().present

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
            browser.window(title='closeable window').use()
            browser.link(id='close').click()
            Wait.until(lambda: len(browser.windows()) == 1)
            browser.window().use()


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

    # use

    def test_should_switch_window_by_index(self, browser):
        assert browser.window(index=0).use().title == 'window switching'

    def test_should_switch_window_by_url(self, browser):
        assert browser.window(
            url=re.compile(r'window_switching\.html')).use().title == 'window switching'

    def test_should_switch_window_by_title(self, browser):
        assert re.search(r'window_switching\.html',
                         browser.window(title='window switching').use().url)

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
        assert size.width > 0
        assert size.height > 0

    def test_should_get_the_position_of_the_current_window(self, browser):
        pos = browser.window().position
        assert pos.x >= 0
        assert pos.y >= 0

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
        browser.window().resize_to(initial_size.width, initial_size.height - 20)
        browser.window().maximize()
        browser.wait_until(lambda b: b.window().size != initial_size)

        new_size = browser.window().size

        assert new_size.width >= initial_size.width
        assert new_size.height > initial_size.height - 20
