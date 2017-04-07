from time import time


class Timer(object):
    def __init__(self, timeout=None):
        self.end_time = time() + timeout if timeout else None

    def wait(self, method, timeout, object=None):
        """
        Executes the given method until it returns True or exceeds the timeout
        :param timeout: time in seconds to timeout after
        :param method: method to call (typically a lambda)
        :param obect: object to call in the method
        :rtype: bool
        """
        end_time = self.end_time or time() + timeout
        result = method(object) if object else method()
        while result is not True:
            result = method(object) if object else method()
            if time() > end_time:
                break
        return result

    def reset(self):
        self.end_time = None

    @property
    def locked(self):
        return self.end_time is not None
