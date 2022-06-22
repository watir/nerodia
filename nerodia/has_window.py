import re

from .window import Window


class HasWindow(object):
    def windows(self, *args, **kwargs):
        """
        Returns browser windows list
        :rtype: list[Window]

        :Example:

        browser.windows(title='closeable window')
        """
        all = [Window(self, {'handle': handle}) for handle in self.driver.window_handles]

        if not args and not kwargs:
            return all
        else:
            return self._filter_windows(self._extract_selector(*args, **kwargs), all)

    def window(self, *args, **kwargs):
        """
        Returns browser window
        :rtype: Window

        :Example:

        browser.window(title='closeable window')
        """
        return Window(self, self._extract_selector(*args, **kwargs))

    @property
    def original_window(self):
        """
        Returns original window if defined, current window if not
        :rtype: Window

        :Example:

        browser.window(title='closeable window').use()
        browser.original_window.use()
        """
        if not self._original_window:
            self._original_window = self.window()
        return self._original_window

    def switch_window(self):
        current_window = self.window()
        wins = self.windows()
        if len(wins) == 1:
            self.wait_until(lambda b: len(b.windows()) > 1)
        new_window = [x for x in self.windows() if x != current_window][0]
        new_window.use()
        return new_window

    # private

    def _filter_windows(self, selector, windows):
        if not all(key in ['title', 'url'] for key in selector.keys()):
            raise ValueError('invalid window selector: {}'.format(selector))
        return [w for w in windows if all(re.search(v, getattr(w, k)) is not None
                                          for k, v in selector.items())]
