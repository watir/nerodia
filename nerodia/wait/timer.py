from time import sleep, time


class Timer(object):
    def __init__(self, timeout=None):
        self.end_time = time() + timeout if timeout else None

    def wait(self, timeout, method, interval=0, object=None, expected=True):
        """
        Executes the given method until it returns True or exceeds the timeout
        :param timeout: time in seconds to timeout after
        :param method: method to call (typically a lambda)
        :param interval: interval to wait between calls
        :param obect: object to call in the method
        :param expected: expected outcome
        :type expected: bool
        :rtype: bool
        """
        end_time = self.end_time or time() + timeout
        run_once = False
        while True:
            if time() > end_time and run_once:
                break
            run_once = True
            result = method(object) if object else method()
            if result == expected:
                return True
            sleep(interval)
        return False

    def reset(self):
        self.end_time = None

    @property
    def locked(self):
        return self.end_time is not None
