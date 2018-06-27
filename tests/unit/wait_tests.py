import pytest

from nerodia.wait.wait import Wait, TimeoutError, Timer


class TestWaitUntil(object):
    # until

    def test_waits_until_the_method_returns_true(self):
        assert Wait.until(timeout=0.5, method=lambda: True)

    def test_exeuctes_method_if_timeout_is_zero(self):
        assert Wait.until(timeout=0, method=lambda: True)

    def test_times_out(self):
        with pytest.raises(TimeoutError):
            Wait.until(timeout=0.5, method=lambda: False)

    def test_times_out_with_a_custom_message(self):
        msg = 'oops'
        with pytest.raises(TimeoutError) as e:
            Wait.until(timeout=0.5, message=msg, method=lambda: False)
        assert e.value.args[0] == 'timed out after 0.5 seconds, {}'.format(msg)

    def test_uses_provided_interval(self):
        count = {'value': 0}

        def method():
            count['value'] += 1

        try:
            Wait.until(timeout=0.4, interval=0.2, method=method)
        except TimeoutError:
            pass
        assert count.get('value') == 2

    def test_uses_timer_for_waiting(self, mocker):
        mocker.patch('nerodia.wait.wait.Timer.wait')
        Wait.until(timeout=0.5, method=lambda: True)
        Timer.wait.assert_called_once()


class TestWaitWhile(object):
    # until_not

    def test_waits_while_the_method_returns_true(self):
        assert Wait.until_not(timeout=0.5, method=lambda: False)

    def test_wait_until_not_alias(self):
        assert Wait.whilst(timeout=0.5, method=lambda: False)

    def test_exeuctes_method_if_timeout_is_zero(self):
        assert Wait.until_not(timeout=0, method=lambda: False)

    def test_times_out(self):
        with pytest.raises(TimeoutError):
            Wait.until_not(timeout=0.5, method=lambda: True)

    def test_times_out_with_a_custom_message(self):
        msg = 'oops'
        with pytest.raises(TimeoutError) as e:
            Wait.until_not(timeout=0.5, message=msg, method=lambda: True)
        assert e.value.args[0] == 'timed out after 0.5 seconds, {}'.format(msg)

    def test_uses_provided_interval(self):
        count = {'value': 0}

        def method():
            count['value'] += 1

        try:
            Wait.until_not(timeout=0.4, interval=0.2, method=method)
        except TimeoutError:
            pass
        assert count.get('value') == 2

    def test_uses_timer_for_waiting(self, mocker):
        mocker.patch('nerodia.wait.wait.Timer.wait')
        Wait.until_not(timeout=0.5, method=lambda: True)
        Timer.wait.assert_called_once()


class TestWaitDefaultTimer(object):
    def test_returns_default_timer(self):
        assert isinstance(Wait.timer, Timer)

    def test_changes_default_timer(self):
        class Foo():
            pass
        try:
            timer = Foo()
            Wait.timer = timer
            assert Wait.timer == timer
        finally:
            Wait.timer = Timer()
