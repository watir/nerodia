import pytest

from nerodia.wait.wait import TimeoutError

pytestmark = pytest.mark.page('alerts.html')


@pytest.fixture
def cleanup_alert(browser):
    yield
    if browser.alert.exists:
        browser.alert.ok()


@pytest.mark.usefixtures('cleanup_alert')
class TestAlertAPI(object):
    # TODO: xfail safari
    def test_returns_text_of_alert(self, browser):
        browser.button(id='alert').click()
        assert 'ok' in browser.alert.text

    # exists

    def test_returns_false_if_alert_is_not_present(self, browser):
        assert not browser.alert.exists

    def test_returns_true_if_alert_is_present(self, browser):
        browser.button(id='alert').click()
        browser.wait_until(lambda b: b.alert.exists, timeout=10)

    # ok

    def test_closes_alert_by_ok(self, browser):
        browser.button(id='alert').click()
        browser.alert.ok()
        assert not browser.alert.exists

    # close

    def test_closes_alert_by_close(self, browser):
        browser.button(id='alert').click()
        browser.alert.close()
        assert not browser.alert.exists

    # wait_until_present

    @pytest.mark.skipif('nerodia.relaxed_locate',
                        reason='only applicable when not relaxed locating')
    def test_waits_until_alert_is_present_and_goes_on(self, browser):
        browser.button(id='timeout-alert').click()
        browser.alert.wait_until_present().ok()
        assert not browser.alert.exists

    @pytest.mark.skipif('nerodia.relaxed_locate',
                        reason='only applicable when not relaxed locating')
    def test_raises_error_if_alert_is_not_present_after_timeout(self, browser):
        with pytest.raises(TimeoutError):
            browser.alert.wait_until_present().ok()

    # confirm

    def test_accepts_confirm(self, browser):
        browser.button(id='confirm').click()
        browser.alert.ok()
        assert browser.button(id='confirm').value == 'true'

    # close

    def test_cancels_confirm(self, browser):
        browser.button(id='confirm').click()
        browser.alert.close()
        assert browser.button(id='confirm').value == 'false'

    # prompt set

    def test_enters_text_into_prompt(self, browser):
        browser.button(id='prompt').click()
        browser.alert.set('My Name')
        browser.alert.ok()
        assert browser.button(id='prompt').value == 'My Name'
