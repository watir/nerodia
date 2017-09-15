from time import sleep, time


class Timer(object):
    def __init__(self, timeout=None):
        self.end_time = self._current_time() + timeout if timeout else None
        self.remaining_time = self.end_time - self._current_time() if self.end_time else None

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
        end_time = self.end_time or self._current_time() + timeout
        run_once = False
        while True:
            if self._current_time() > end_time and run_once:
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

    # private

    def _current_time(self):
        return time()
