import nerodia
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
        :type timeout: float
        :param message:  message to raise if timeout is exceeded
        :type message: str
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        Wait.until(lambda: browser.text_field(name='abrakadbra').present)
        """
        timeout = timeout or nerodia.default_timeout
        result = cls._run_with_timer(timeout, interval, method, object, until=True)
        if result:
            return result
        raise TimeoutError(cls._message_for(timeout, object, message))

    @classmethod
    def until_not(cls, method=None, timeout=None, message=None, interval=None, object=None):
        """
        Waits while the method evaluates to True or times out
        :param method: method to run, typically lambda
        :param object: object to evaluate method with
        :param timeout: time to wait
        :type timeout: float
        :param message:  message to raise if timeout is exceeded
        :type message: str
        :param interval: time to wait between each check
        :type interval: float
        :Example:

        Wait.until_not(lambda: browser.text_field(name='abrakadbra').present)
        """
        timeout = timeout or nerodia.default_timeout
        result = cls._run_with_timer(timeout, interval, method, object, until=False)
        if result:
            return result
        raise TimeoutError(cls._message_for(timeout, object, message))

    whilst = until_not

    @classmethod
    def _message_for(cls, timeout, object, message):
        if callable(message):
            message = message(object)
        err = 'timed out after {} seconds'.format(timeout)
        if message:
            err += ', {}'.format(message)
        return err

    @classmethod
    def _run_with_timer(cls, timeout, interval, method, object, until=True):
        if timeout == 0:
            return method(object) if object else method()
        else:
            interval = interval or cls.INTERVAL
            result = cls.timer.wait(timeout, method, interval=interval,
                                    object=object, expected=until)
            return result


class Waitable(object):
    def wait_until(self, method=None, timeout=None, message=None, interval=None, object=None):
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
        if not message:
            def msg(obj):
                return 'waiting for true condition on {}'.format(obj)
            message = msg
        if object is None:
            object = self
        Wait.until(method=method, timeout=timeout, message=message, interval=interval,
                   object=object)
        return self

    def wait_until_not(self, method=None, timeout=None, message=None, interval=None, object=None):
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
        if not message:
            def msg(obj):
                return 'waiting for false condition on {}'.format(obj)
            message = msg
        if object is None:
            object = self
        Wait.until_not(method=method, timeout=timeout, message=message, interval=interval,
                       object=object)
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
        return self.wait_until(method=lambda x: x.present, timeout=timeout, interval=interval)

    def wait_until_not_present(self, timeout=None, interval=None):
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
            from nerodia.elements.element import Element
            if isinstance(arg, Element):
                arg.reset()
            return arg.present

        return self.wait_until_not(method=method, timeout=timeout, interval=interval)


class TimeoutError(Exception):
    pass
