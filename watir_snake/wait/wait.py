from time import sleep

import watir_snake
from .timer import Timer


class Wait(object):
    INTERVAL = 0.1
    timer = Timer()  # Access timer implementation in use

    @classmethod
    def until(cls, method=None, timeout=None, message=None, interval=None, object=None):
        """
        Waits until the method evaluates to True or times out
        :param method: method to run, typically lambda
        :param object: object to evaluate method with
        :param timeout: time to wait
        :type timeout: int
        :param message:  message to raise if timeout is exceeded
        :type message: str
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        Wait.until(lambda _: browser.text_field(name='abrakadbra').present)
        """
        timeout = timeout or watir_snake.default_timeout
        result = cls._run_with_timer(timeout, interval, method, object)
        if result:
            return result
        raise TimeoutError(cls._message_for(timeout, message))

    @classmethod
    def until_not(cls, method=None, timeout=None, message=None, interval=None, object=None):
        """
        Waits while the method evaluates to True or times out
        :param method: method to run, typically lambda
        :param object: object to evaluate method with
        :param timeout: time to wait
        :type timeout: int
        :param message:  message to raise if timeout is exceeded
        :type message: str
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        Wait.until_not(lambda _: browser.text_field(name='abrakadbra').present)
        """
        timeout = timeout or watir_snake.default_timeout
        result = cls._run_with_timer(timeout, interval, method, object)
        if not result:
            return result
        raise cls.TimeoutError(cls._message_for(timeout, message))

    @classmethod
    def _message_for(cls, timeout, message):
        err = 'timed out after {} seconds'.format(timeout)
        if message:
            err += ', {}'.format(message)
        return err

    @classmethod
    def _run_with_timer(cls, timeout, interval, method, object):
        if timeout == 0:
            return method(object) if object else method()
        else:
            result = cls.timer.wait(timeout, method, object)
            sleep(interval or cls.INTERVAL)
            return result


class Waitable(object):
    def wait_until(self, method=None, timeout=None, message=None, interval=None):
        """
        Waits until the condition is True
        :param method: method to run, typically lambda
        :param object: object to evaluate method with
        :param timeout: time to wait
        :type timeout: int
        :param message:  message to raise if timeout is exceeded
        :type message: str
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        browser.text_field(name='new_user_first_name').wait_until(lambda x: x.present).click
        """
        message = message or 'waiting for true condition on #{}'.format(self)
        Wait.until(method, timeout, message, interval, object=self)
        return self

    def wait_while(self, method=None, timeout=None, message=None, interval=None):
        """
        Waits while the condition is True
        :param method: method to run, typically lambda
        :param object: object to evaluate method with
        :param timeout: time to wait
        :type timeout: int
        :param message: message to raise if timeout is exceeded
        :type message: str
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        browser.wait_while(lambda x: not x.exists, timeout=2)
        """
        message = message or 'waiting for false condition on {}'.format(self)
        Wait.until_not(method, timeout, message, interval, object=self)
        return self

    def wait_until_present(self, timeout=None, interval=None):
        """
        Waits until the element is present
        :param timeout: time to wait
        :type timeout: int
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        browser.text_field(name='new_user_first_name').wait_until_present()
        """
        return self.wait_until(method=lambda e: e.present, timeout=timeout, interval=interval)

    def wait_while_present(self, timeout=None, interval=None):
        """
        Waits while the element is present
        :param timeout: time to wait
        :type timeout: int
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        browser.text_field(name='abrakadbra').wait_while_present
        """

        def method(arg):
            if isinstance(arg, watir_snake.elements.element.Element):
                arg.reset()
            return arg.present

        return self.wait_while(method=method, timeout=timeout, interval=interval)


class TimeoutError(StandardError):
    pass
