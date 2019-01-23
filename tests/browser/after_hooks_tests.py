import pytest
from selenium.common.exceptions import UnexpectedAlertPresentException

from nerodia.exception import UnknownObjectException


@pytest.fixture
def cleanup_hooks(browser):
    yield
    browser.window(index=0).use()
    browser.after_hooks.after_hooks = []


@pytest.fixture
def clear_alert(browser):
    yield
    if browser.alert.exists:
        browser.alert.ok()


pytestmark = pytest.mark.usefixtures('cleanup_hooks')


class TestAfterHooksAdd(object):
    def test_raises_correct_exception_when_not_given_any_arguments(self, browser):
        with pytest.raises(ValueError):
            browser.after_hooks.add()

    def test_runs_the_given_method_on_each_page_load(self, browser, page):
        output = []

        def hook(b):
            output.extend([b.text])

        browser.after_hooks.add(method=hook)
        browser.goto(page.url('non_control_elements.html'))

        assert 'Dubito, ergo cogito, ergo sum' in ''.join(output)


class TestAfterHooksDelete(object):
    def test_removes_a_previously_added_after_hook(self, browser, page):
        output = []

        def hook(b):
            output.extend([b.text])

        browser.after_hooks.add(method=hook)
        browser.goto(page.url('non_control_elements.html'))
        assert 'Dubito, ergo cogito, ergo sum' in ''.join(output)

        browser.after_hooks.delete(hook)
        browser.goto(page.url('definition_lists.html'))
        assert 'definition_lists' not in ''.join(output)


class TestAfterHooksRun(object):
    def test_runs_after_hooks_after_browser_goto(self, browser, page):
        result = {}

        def hook(b):
            result['value'] = b.title == 'The font element'

        browser.after_hooks.add(method=hook)
        browser.goto(page.url('font.html'))
        assert result['value'] is True

    @pytest.mark.page('font.html')
    def test_runs_after_hooks_after_browser_refresh(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'The font element'

        browser.after_hooks.add(method=hook)
        browser.refresh()
        assert result['value'] is True

    @pytest.mark.page('non_control_elements.html')
    def test_runs_after_hooks_after_element_click(self, browser):
        result = {}

        def hook(b):
            b.wait_until(lambda br: br.title == 'Forms with input elements')
            result['value'] = True

        browser.after_hooks.add(method=hook)
        browser.link(index=2).click()
        assert result.get('value') is True

    # TODO: xfail firefox
    @pytest.mark.page('forms_with_input_elements.html')
    def test_runs_after_hooks_after_element_submit(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.div(id='messages').text == 'submit'

        browser.after_hooks.add(method=hook)
        browser.form(id='new_user').submit()
        assert result.get('value') is True

    @pytest.mark.xfail_firefox(reason='https://github.com/mozilla/geckodriver/issues/661')
    @pytest.mark.page('non_control_elements.html')
    def test_runs_after_hooks_after_element_double_click(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Non-control elements'

        browser.after_hooks.add(method=hook)
        browser.div(id='html_test').double_click()
        assert result.get('value') is True

    # TODO: xfail safari, firefox
    @pytest.mark.page('right_click.html')
    def test_runs_after_hooks_after_element_right_click(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Right Click Test'

        browser.after_hooks.add(method=hook)
        browser.div(id='click').right_click()
        assert result.get('value') is True

    # TODO: xfail safari
    @pytest.mark.page('iframes.html')
    def test_runs_after_hooks_after_framed_driver_switch(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Iframes'

        browser.after_hooks.add(method=hook)

        browser.iframe().element(css='#senderElement').exists

        assert result.get('value') is True

    # TODO: xfail safari
    @pytest.mark.page('iframes.html')
    def test_runs_after_hooks_after_browser_ensure_context(self, browser):
        browser.iframe().element(css='#senderElement').locate()
        result = {}

        def hook(b):
            result['value'] = b.title == 'Iframes'

        browser.after_hooks.add(method=hook)

        browser.locate()

        assert result.get('value') is True

    # TODO: xfail safari
    @pytest.mark.page('alerts.html')
    def test_runs_after_hooks_after_alert_ok(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Alerts'

        browser.after_hooks.add(method=hook)
        with browser.after_hooks.without():
            browser.button(id='alert').click()
        browser.alert.ok()
        assert result.get('value') is True

    # TODO: xfail safari
    @pytest.mark.page('alerts.html')
    def test_runs_after_hooks_after_alert_close(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Alerts'

        browser.after_hooks.add(method=hook)
        with browser.after_hooks.without():
            browser.button(id='alert').click()
        browser.alert.close()
        assert result.get('value') is True

    @pytest.mark.xfail_firefox(reason='w3c currently errors when an alert is present',
                               raises=UnknownObjectException)
    @pytest.mark.page('alerts.html')
    @pytest.mark.quits_browser
    @pytest.mark.usefixtures('quick_timeout')
    def test_does_not_run_error_checks_with_alert_present(self, browser):
        result = []

        def hook(b):
            result.append(b.title == 'Alerts')
        browser.after_hooks.add(method=hook)

        browser.button(id='alert').click()
        assert not result

        browser.alert.ok()
        assert result

    @pytest.mark.usefixtures('clear_alert')
    def test_does_not_raise_error_when_running_error_checks_using_after_hooks_without_with_alert_present(self, browser, page):
        def hook(b):
            b.url

        browser.after_hooks.add(method=hook)
        browser.goto(page.url('alerts.html'))
        with browser.after_hooks.without():
            browser.button(id='alert').click()

    @pytest.mark.xfail_firefox(reason='w3c currently errors when an alert is present',
                               raises=UnexpectedAlertPresentException)
    @pytest.mark.usefixtures('clear_alert')
    def test_does_not_raise_error_if_no_error_checks_are_defined_with_alert_present(self, browser, page):
        def hook(b):
            b.url

        browser.after_hooks.add(method=hook)
        browser.goto(page.url('alerts.html'))
        browser.after_hooks.delete(hook)
        browser.button(id='alert').click()

    # TODO: xfail firefox
    def test_does_not_raise_error_when_running_error_checks_on_closed_window(self, browser, page):
        def hook(b):
            b.url

        browser.after_hooks.add(method=hook)
        browser.goto(page.url('window_switching.html'))
        browser.link(id='open').click()
        window = browser.window(title='closeable window')
        window.use()
        browser.link(id='close').click()


class TestAfterHooksLength(object):
    def test_provides_the_number_of_after_hooks(self, browser):

        def hook():
            return True

        for _ in range(4):
            browser.after_hooks.add(hook)
        assert len(browser.after_hooks) == 4


class TestAfterHooksGetItem(object):
    def test_returns_the_after_hook_at_the_provided_index(self, browser):

        def hook1():
            return True

        def hook2():
            return False

        browser.after_hooks.add(hook1)
        browser.after_hooks.add(hook2)
        assert browser.after_hooks[1] == hook2
