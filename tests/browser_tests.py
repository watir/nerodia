import re

import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from nerodia.browser import Browser
from nerodia.elements.html_elements import Body

BROWSERS = ['chrome',
            'firefox',
            'ie',
            'edge',
            'safari',
            'remote']

W3C_BROWSERS = ['firefox']


@pytest.fixture
def cleanup_browser(browser):
    yield
    browser.original_window.use()
    for window in browser.windows()[1:]:
        window.close()


@pytest.mark.usefixtures('cleanup_browser')
class TestBrowserExists(object):
    @pytest.mark.page('non_control_elements.html')
    def test_returns_true_if_we_are_at_a_page(self, browser):
        assert browser.exists

    @pytest.mark.page('window_switching.html')
    def test_returns_false_if_window_is_closed(self, browser):
        browser.link(id='open').click()
        browser.wait_until(lambda b: len(b.windows()) == 2)
        browser.window(title='closeable window').use()
        browser.link(id='close').click()
        browser.wait_until(lambda b: len(b.windows()) == 1)
        assert not browser.exists

    def test_returns_false_after_browser_close(self, browser, bkwargs):
        b = browser.__class__(**bkwargs)
        b.close()
        assert not b.exists


class TestBrowserAttributes(object):
    # html

    @pytest.mark.page('right_click.html')
    def test_returns_the_dom_of_the_page_as_an_html_string(self, browser):
        html = browser.html.lower()
        assert re.search(r'^<html', html)
        assert '<meta ' in html
        assert 'content="text/html; charset=utf-8"' in html
        if 'explore' not in browser.name:
            assert ' http-equiv="content-type"' in html

    # title

    @pytest.mark.page('non_control_elements.html')
    def test_returns_the_current_page_title(self, browser):
        assert browser.title == 'Non-control elements'

    # status

    @pytest.mark.xfail_ie(reason='setting window.status does not work')
    @pytest.mark.page('non_control_elements.html')
    def test_returns_the_current_value_of_window_status(self, browser):
        """
        for Firefox, this needs to be enabled in
        Preferences -> Content -> Advanced -> Change status bar text

        for IE9, this needs to be enabled in
        View => Toolbars -> Status bar
        """
        browser.execute_script("window.status = 'All done!';")
        assert browser.status == 'All done!'

    # name

    def test_returns_browser_name(self, browser, bkwargs):
        name = bkwargs.get('browser')
        if name == 'ie':
            name = 'internet explorer'
        assert browser.name == name

    # text

    @pytest.mark.page('non_control_elements.html')
    def test_returns_the_text_of_the_page(self, browser):
        assert 'Dubito, ergo cogito, ergo sum.' in browser.text

    @pytest.mark.page('plain_text')
    def test_returns_the_text_also_if_the_content_type_is_text_plain(self, browser):
        assert browser.text.strip() == 'This is text/plain'

    @pytest.mark.page('nested_iframes.html')
    def test_returns_text_of_top_most_browsing_context(self, browser):
        browser.iframe(id='two').h3().exists
        assert browser.text == 'Top Layer'

    # url

    @pytest.mark.page('non_control_elements.html')
    def test_returns_the_current_url(self, browser, page):
        assert browser.url.lower() == page.url('non_control_elements.html').lower()

    @pytest.mark.page('frames.html')
    def test_always_returns_top_url(self, browser, page):
        browser.frame().body().exists  # switches to frame
        assert browser.url.lower() == page.url('frames.html').lower()

    # title

    @pytest.mark.page('non_control_elements.html')
    def test_returns_the_current_title(self, browser):
        assert browser.title == 'Non-control elements'

    @pytest.mark.page('frames.html')
    def test_always_returns_top_title(self, browser):
        browser.element(tag_name='title').text
        browser.frame().body().exists  # switches to frame
        assert browser.title == 'Frames'

    # start

    def test_goes_to_the_given_url_and_return_an_instance_of_itself(self, page, bkwargs):
        from nerodia.browser import Browser
        browser = Browser.start(page.url('non_control_elements.html'), **bkwargs)

        assert isinstance(browser, Browser)
        assert browser.title == 'Non-control elements'
        browser.close()

    # goto

    # TODO: xfail IE
    def test_adds_http_to_urls_with_no_url_scheme_specified(self, browser, webserver):
        url = webserver.host
        assert url is not None
        browser.goto(webserver.path_for('non_control_elements.html').split('://')[-1])
        assert re.search('http://{}'.format(url), browser.url)

    def test_goes_to_the_given_url_without_raising_errors(self, browser, page):
        browser.goto(page.url('non_control_elements.html'))

    def test_goes_to_the_url_about_blank_without_raising_errors(self, browser):
        browser.goto('about:blank')

    # TODO: xfail IE, safari
    def test_goes_to_a_data_url_scheme_address_without_raising_errors(self, browser):
        browser.goto('data:text/html;content-type=utf-8,foobar')

    @pytest.mark.page('timeout_window_location.html')
    def test_updates_the_page_when_location_is_changed_with_set_timeout_and_window_location(self, browser):
        browser.wait_until_not(lambda b: 'timeout_window_location.html' in b.url, timeout=10)
        assert 'non_control_elements.html' in browser.url


@pytest.mark.page('non_control_elements.html')
class TestBrowserRefresh(object):
    def test_refreshes_the_page(self, browser):
        browser.span(class_name='footer').click()
        assert 'Javascript' in browser.span(class_name='footer').text
        browser.refresh()
        browser.span(class_name='footer').wait_until_present()
        assert 'Javascript' not in browser.span(class_name='footer').text


@pytest.mark.page('non_control_elements.html')
class TestBrowserExecuteScript(object):
    def test_executes_the_given_javascript_on_the_current_page(self, browser):
        assert browser.pre(id='rspec').text != 'javascript text'
        browser.execute_script("document.getElementById('rspec').innerHTML = 'javascript text'")
        assert browser.pre(id='rspec').text == 'javascript text'

    def test_executes_the_given_javascript_in_the_context_of_an_anonymous_function(self, browser):
        assert browser.execute_script('1 + 1') is None
        assert browser.execute_script('return 1 + 1') == 2

    def test_returns_correct_python_objects(self, browser):
        assert browser.execute_script("return {a: 1, \"b\": 2}") == {'a': 1, 'b': 2}
        assert browser.execute_script("return [1, 2, \"3\"]") == [1, 2, '3']
        assert browser.execute_script("return 1.2 + 1.3") == 2.5
        assert browser.execute_script("return 2 + 2") == 4
        assert browser.execute_script("return \"hello\"") == 'hello'
        assert browser.execute_script("return") is None
        assert browser.execute_script("return null") is None
        assert browser.execute_script("return undefined") is None
        assert browser.execute_script("return true") is True
        assert browser.execute_script("return false") is False

    def test_works_correctly_with_multi_line_strings_and_special_characters(self, browser):
        assert browser.execute_script("//multiline rocks!\n"
                                      "var a = 22; // comment on same line\n"
                                      "/* more\n"
                                      "comments */\n"
                                      "var b = '33';\n"
                                      "var c = \"44\";\n"
                                      "return a + b + c;") == '223344'


@pytest.mark.page('non_control_elements.html')
# TODO: xfail safari
class TestBrowserBackForth(object):
    def test_goes_to_the_previous_page(self, browser, page):
        orig_url = browser.url
        browser.goto(page.url('tables.html'))
        new_url = browser.url
        assert new_url != orig_url
        browser.back()
        assert browser.url == orig_url

    def test_goes_to_the_next_page(self, browser, page):
        urls = [browser.url]
        browser.goto(page.url('tables.html'))
        urls.append(browser.url)

        browser.back()
        assert browser.url == urls[0]
        browser.forward()
        assert browser.url == urls[-1]

    def test_navigates_between_several_history_items(self, browser, page):
        paths = ['non_control_elements.html',
                 'tables.html',
                 'forms_with_input_elements.html',
                 'definition_lists.html']
        urls = []
        for path in paths:
            browser.goto(page.url(path))
            urls.append(browser.url)

        for _ in range(3):
            browser.back()
        assert browser.url == urls[0]

        for _ in range(2):
            browser.forward()
        assert browser.url == urls[2]

    @pytest.mark.page('plain_text')
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_trying_to_access_dom_elements_on_plain_text_page(self, browser):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.div(id='foo').id


@pytest.mark.page('non_control_elements.html')
# TODO: xfail safari
class TestBrowserInit(object):

    @pytest.mark.only(W3C_BROWSERS)
    def test_passes_capabilities_to_selenium(self, browser_manager):
        browser_name = browser_manager.name
        caps_name = 'internetexplorer' if browser_name == 'ie'else browser_name
        caps = getattr(DesiredCapabilities, caps_name.upper()).copy()
        caps.update({'acceptInsecureCerts': True})
        browser = Browser(browser_name, desired_capabilities=caps)
        insecure = browser.wd.capabilities['acceptInsecureCerts']
        browser.quit()

        assert insecure is True

    def test_remote_when_passed_url_arg(self, browser, browser_manager):
        from selenium.webdriver.remote.webdriver import RemoteConnection, WebDriver
        caps_name = 'internetexplorer' if browser.name == 'internet explorer'else browser.name
        caps = getattr(DesiredCapabilities, caps_name.upper()).copy()
        browser = Browser(browser_manager.name, desired_capabilities=caps)
        driver = browser.wd
        executor = driver.command_executor
        browser.quit()

        assert driver.__class__.__name__ == WebDriver.__name__
        assert driver.name == caps.get('browserName')
        assert isinstance(executor, RemoteConnection)

    @pytest.mark.only(['firefox'])
    def test_accepts_firefox_profile(self, browser_manager, webserver):
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        home_page = webserver.path_for('special_chars.html')

        profile = FirefoxProfile()
        profile.set_preference('browser.startup.homepage', home_page)
        profile.set_preference('browser.startup.page', 1)
        kwargs = browser_manager.kwargs.copy()
        kwargs['options'] = {'profile': profile}

        new_browser = Browser(**kwargs)
        try:
            assert new_browser.url == home_page
        finally:
            new_browser.quit()

    def test_accepts_browser_options(self, browser_manager, mocker):
        from importlib import import_module
        browser_name = browser_manager.name
        module = import_module('selenium.webdriver.{}.options'.format(browser_name))
        opts = module.Options()

        mock = mocker.patch('selenium.webdriver.{}.webdriver.WebDriver'.format(browser_name))

        caps_name = 'internetexplorer' if browser_name == 'ie' else browser_name
        caps = getattr(DesiredCapabilities, caps_name.upper()).copy()

        browser = Browser(browser_name, options=opts)
        browser.quit()

        key = 'desired_capabilities' if browser_name in ['safari', 'chrome'] else 'capabilities'

        kwargs = {}
        kwargs[key] = caps
        kwargs['options'] = opts
        mock.assert_called_once_with(**kwargs)

    def test_takes_driver_instance_as_argument(self, browser):
        new_browser = Browser(browser.wd)
        assert new_browser.wd == browser.wd

    def test_takes_listener_as_argument(self, browser_manager):
        from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
        from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
        ael = AbstractEventListener()
        new_browser = None
        try:
            new_browser = Browser(**dict(browser_manager.kwargs, listener=ael))
            assert isinstance(new_browser.wd, EventFiringWebDriver)
        finally:
            if new_browser:
                new_browser.quit()


@pytest.mark.page('definition_lists.html')
class TestBrowserElementWrap(object):
    def test_wraps_elements_as_package_objects(self, browser):
        returned = browser.execute_script('return document.body;')
        assert isinstance(returned, Body)

    def test_wraps_elements_in_a_list(self, browser):
        lst = browser.execute_script('return [document.body];')
        assert len(lst) == 1
        assert isinstance(lst[0], Body)

    def test_wraps_elements_in_a_dict(self, browser):
        dct = browser.execute_script('return {element: document.body};')
        assert isinstance(dct.get('element'), Body)

    def test_wraps_elements_in_a_deep_object(self, browser):
        dct = browser.execute_script('return {elements: [document.body], '
                                     'body: {element: document.body}};')
        assert isinstance(dct.get('elements')[0], Body)
        assert isinstance(dct.get('body').get('element'), Body)


class TestBrowserSendKeys(object):
    @pytest.mark.page('forms_with_input_elements.html')
    def test_sends_keystrokes_to_the_active_element(self, browser):
        browser.send_keys('hello')
        assert browser.text_field(id='new_user_first_name').value == 'hello'

    @pytest.mark.page('frames.html')
    def test_sends_keystrokes_to_a_frame(self, browser):
        tf = browser.frame().text_field(id='senderElement')
        tf.clear()

        browser.frame().send_keys('hello')
        assert tf.value == 'hello'


class TestBrowserClosed(object):
    def test_raises_correct_exception_when_trying_to_interact_with_a_closed_browser(self, bkwargs, page):
        from nerodia.browser import Browser
        from nerodia.exception import Error
        with pytest.raises(Error) as e:
            b = Browser(**bkwargs)
            b.goto(page.url('definition_lists.html'))
            b.close()
            b.dl(id='experience-list').id
        assert e.value.args[0] == 'browser was closed'


class TestBrowserWait(object):
    def test_delegates_wait_until_not_to_the_wait_module(self, browser, mocker):
        mock = mocker.patch('nerodia.wait.wait.Wait.until_not')

        def method():
            pass

        browser.wait_until_not(timeout=3, message='foo', interval=0.2, method=method)
        mock.assert_called_once_with(timeout=3, message='foo', interval=0.2, method=method,
                                     object=browser)

    def test_delegates_wait_until_to_the_wait_module(self, browser, mocker):
        mock = mocker.patch('nerodia.wait.wait.Wait.until')

        def method():
            pass

        browser.wait_until(timeout=3, message='foo', interval=0.2, method=method)
        mock.assert_called_once_with(timeout=3, message='foo', interval=0.2, method=method,
                                     object=browser)

    def test_waits_until_document_readystate_is_complete(self, browser, mocker):
        mock = mocker.patch('nerodia.browser.Browser.ready_state',
                            new_callable=mocker.PropertyMock)
        mock.side_effect = ['incomplete', 'complete']
        browser.wait()
        assert mock.call_count == 2


class TestBrowserReadyState(object):
    def test_gets_the_document_ready_state_property(self, browser, mocker):
        mock = mocker.patch('nerodia.browser.Browser.ready_state',
                            new_callable=mocker.PropertyMock)
        browser.ready_state
        assert mock.call_count == 1


class TestBrowserRepr(object):
    def test_works_even_if_browser_is_closed(self, browser, bkwargs):
        b = Browser(**bkwargs)
        b.close()
        repr(b)


class TestBrowserScreenshot(object):
    def test_returns_an_instance_of_screenshot(self, browser):
        from nerodia.screenshot import Screenshot
        assert isinstance(browser.screenshot, Screenshot)
