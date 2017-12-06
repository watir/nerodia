import pytest

from selenium.common.exceptions import UnexpectedAlertPresentException

from nerodia.exception import UnknownObjectException


class TestAfterHooksAdd(object):
    def test_raises_correct_exception_when_not_given_any_arguments(self, browser):
        with pytest.raises(ValueError):
            browser.after_hooks.add()

    def test_runs_the_given_method_on_each_page_load(self, browser, page):
        output = []

        def hook(b):
            output.extend([b.text])

        try:
            browser.after_hooks.add(method=hook)
            browser.goto(page.url('non_control_elements.html'))

            assert 'Dubito, ergo cogito, ergo sum' in ''.join(output)
        finally:
            browser.after_hooks.delete(hook)


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
    @staticmethod
    def cleanup(browser, method):
        browser.original_window.use()
        browser.after_hooks.delete(method)

    def test_runs_after_hooks_after_browser_goto(self, browser, page):
        result = {}

        def hook(b):
            result['value'] = b.title == 'The font element'

        try:
            browser.after_hooks.add(method=hook)
            browser.goto(page.url('font.html'))
            assert result['value'] is True
        finally:
            self.cleanup(browser, hook)

    @pytest.mark.page('font.html')
    def test_runs_after_hooks_after_browser_refresh(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'The font element'

        try:
            browser.after_hooks.add(method=hook)
            browser.refresh()
            assert result['value'] is True
        finally:
            self.cleanup(browser, hook)

    @pytest.mark.page('non_control_elements.html')
    def test_runs_after_hooks_after_element_click(self, browser):
        result = {}

        def hook(b):
            b.wait_until(lambda br: br.title == 'Forms with input elements')
            result['value'] = True

        try:
            browser.after_hooks.add(method=hook)
            browser.link(index=2).click()
            assert result.get('value') is True
        finally:
            self.cleanup(browser, hook)

    # TODO: xfail firefox
    @pytest.mark.page('forms_with_input_elements.html')
    def test_runs_after_hooks_after_element_submit(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.div(id='messages').text == 'submit'

        try:
            browser.after_hooks.add(method=hook)
            browser.form(id='new_user').submit()
            assert result.get('value') is True
        finally:
            self.cleanup(browser, hook)

    @pytest.mark.xfail_firefox(reason='https://github.com/mozilla/geckodriver/issues/661')
    @pytest.mark.page('non_control_elements.html')
    def test_runs_after_hooks_after_element_double_click(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Non-control elements'

        try:
            browser.after_hooks.add(method=hook)
            browser.div(id='html_test').double_click()
            assert result.get('value') is True
        finally:
            self.cleanup(browser, hook)

    # TODO: xfail safari, firefox
    @pytest.mark.page('right_click.html')
    def test_runs_after_hooks_after_element_right_click(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Right Click Test'

        try:
            browser.after_hooks.add(method=hook)
            browser.div(id='click').right_click()
            assert result.get('value') is True
        finally:
            self.cleanup(browser, hook)

    # TODO: xfail safari
    @pytest.mark.page('alerts.html')
    def test_runs_after_hooks_after_alert_ok(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Alerts'

        try:
            browser.after_hooks.add(method=hook)
            with browser.after_hooks.without():
                browser.button(id='alert').click()
            browser.alert.ok()
            assert result.get('value') is True
        finally:
            self.cleanup(browser, hook)

    # TODO: xfail safari
    @pytest.mark.page('alerts.html')
    def test_runs_after_hooks_after_alert_close(self, browser):
        result = {}

        def hook(b):
            result['value'] = b.title == 'Alerts'

        try:
            browser.after_hooks.add(method=hook)
            with browser.after_hooks.without():
                browser.button(id='alert').click()
            browser.alert.close()
            assert result.get('value') is True
        finally:
            self.cleanup(browser, hook)

    @pytest.mark.xfail_firefox(reason='w3c currently errors when an alert is present',
                               raises=UnknownObjectException)
    def test_raises_correct_exception_when_running_error_checks_with_alert_present(self, browser, page):
        from selenium.common.exceptions import UnexpectedAlertPresentException
        with pytest.raises(UnexpectedAlertPresentException):
            def hook(b):
                b.url

            try:
                browser.after_hooks.add(method=hook)
                browser.goto(page.url('alerts.html'))
                browser.button(id='alert').click()
            finally:
                browser.alert.ok()
                self.cleanup(browser, hook)

    def test_does_not_raise_error_when_running_error_checks_using_after_hooks_without_with_alert_present(self, browser, page):
        def hook(b):
            b.url

        try:
            browser.after_hooks.add(method=hook)
            browser.goto(page.url('alerts.html'))
            with browser.after_hooks.without():
                browser.button(id='alert').click()
        finally:
            browser.alert.ok()
            self.cleanup(browser, hook)

    @pytest.mark.xfail_firefox(reason='w3c currently errors when an alert is present',
                               raises=UnexpectedAlertPresentException)
    def test_does_not_raise_error_if_no_error_checks_are_defined_with_alert_present(self, browser, page):
        def hook(b):
            b.url

        try:
            browser.after_hooks.add(method=hook)
            browser.goto(page.url('alerts.html'))
            browser.after_hooks.delete(hook)
            browser.button(id='alert').click()
        finally:
            browser.alert.ok()
            browser.window(index=0).use()

    # TODO: xfail firefox
    def test_does_not_raise_error_when_running_error_checks_on_closed_window(self, browser, page):
        def hook(b):
            b.url

        try:
            browser.after_hooks.add(method=hook)
            browser.goto(page.url('window_switching.html'))
            browser.link(id='open').click()
            window = browser.window(title='closeable window')
            window.use()
            browser.link(id='close').click()
        finally:
            self.cleanup(browser, hook)
