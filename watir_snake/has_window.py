from .window import Window


class HasWindow(object):
    def windows(self, *args, **kwargs):
        """
        Returns browser windows list
        :rtype: list[Window]

        :Example:

        browser.windows(title='closeable window')
        """
        all = [Window(self.driver, handle=handle) for handle in self.driver.window_handles]

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
        return Window(self.driver, self._extract_selector(*args, **kwargs))

    # private

    def _filter_windows(self, selector, windows):
        if not all(key in ['title', 'url'] for key in selector.keys()):
            raise ValueError('invalid window selector: {}'.format(selector))

        return filter(lambda w: all(v == getattr(w, k) for k, v in selector.items()), windows)
