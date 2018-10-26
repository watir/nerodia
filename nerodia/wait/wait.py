import re

import nerodia
from .timer import Timer

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


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
            return method(object) if object is not None else method()
        else:
            interval = interval or cls.INTERVAL
            result = cls.timer.wait(timeout, method, interval=interval,
                                    object=object, expected=until)
            return result


class Waitable(object):
    def wait_until(self, method=None, timeout=None, message=None, interval=None, object=None,
                   **kwargs):
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
        browser.text_field(name='new_user_first_name').wait_until(name='new_user_first_name').click
        """
        if not message:
            def msg(obj):
                return 'waiting for true condition on {}'.format(obj)
            message = msg
        if object is None:
            object = self

        if method and kwargs:
            raise ValueError('Unknown keyword(s): {}'.format(kwargs.keys()))
        method = self._create_closure(kwargs, method)

        Wait.until(method=method, timeout=timeout, message=message, interval=interval,
                   object=object)
        return self

    def wait_until_not(self, method=None, timeout=None, message=None, interval=None, object=None,
                       **kwargs):
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

        browser.wait_until_not(lambda x: not x.exists, timeout=2)]
        browser.wait_until_not(title='no')
        """
        if not message:
            def msg(obj):
                return 'waiting for false condition on {}'.format(obj)
            message = msg
        if object is None:
            object = self

        method = self._create_closure(kwargs, method, until=False)

        Wait.until_not(method=method, timeout=timeout, message=message, interval=interval,
                       object=object)
        return self

    def wait_until_present(self, timeout=None, interval=None, message=None):
        """
        Waits until the element is present
        :param timeout: time to wait
        :type timeout: int
        :param interval: time to wait between each check
        :type interval: float
        :param message: message error message for when times out
        :type message: str
        :Example:

        browser.text_field(name='new_user_first_name').wait_until_present()
        """
        nerodia.logger.deprecate('{}#wait_until_present'.format(self.__class__.__name__),
                                 '{}#wait_until(method=lambda e: e.present)',
                                 ids=['wait_until_present'])
        if not message:
            def msg(obj):
                return 'waiting for element {} to become present'.format(obj)
            message = msg
        return self.wait_until(method=lambda x: x.present, timeout=timeout, interval=interval,
                               message=message)

    def wait_until_not_present(self, timeout=None, interval=None, message=None):
        """
        Waits while the element is present
        :param timeout: time to wait
        :type timeout: int
        :param interval: time to wait between each check
        :type interval: float
        :param message: message error message for when times out
        :type message: str
        :Example:

        browser.text_field(name='abrakadbra').wait_until_not_present
        """
        nerodia.logger.deprecate('{}#wait_until_not_present'.format(self.__class__.__name__),
                                 '{}#wait_until_not(method=lambda e: e.present)',
                                 ids=['wait_until_not_present'])
        if not message:
            def msg(obj):
                return 'waiting for element {} not to be present'.format(obj)
            message = msg
        return self.wait_until_not(method=lambda x: x.present, timeout=timeout, interval=interval,
                                   message=message)

    def _create_closure(self, obj, method=None, until=True):
        from nerodia.elements.element import Element

        def func(*args):
            if isinstance(self, Element):
                self.reset()
            return (not obj or self._match_attributes(obj, until)()) and (not method or method(*args))
        return func

    def _match_attributes(self, obj, until=True):
        from ..elements.element import Element

        def check(key):
            expected = obj.get(key)
            if isinstance(self, Element) and not hasattr(self, key):
                actual = self.get_attribute(key)
            else:
                attr = getattr(self, key)
                actual = attr() if callable(attr) else attr
            if isinstance(expected, Pattern):
                return re.search(expected, actual) is not None
            else:
                return expected == actual

        def func(*args):
            truthy = all if until else any
            return truthy(check(key) for key in obj)
        return func


class TimeoutError(Exception):
    pass
