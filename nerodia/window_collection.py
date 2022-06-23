import re

from selenium.common.exceptions import NoSuchWindowException

import nerodia
from nerodia.wait.wait import Waitable
from nerodia.window import Window


class WindowCollection(Waitable):

    def __init__(self, browser, selector=None):
        if selector and not all(key in ['title', 'url', 'element'] for key in selector.keys()):
            raise ValueError('invalid window selector: {}'.format(selector))
        self.browser = browser
        self.selector = selector
        self._windows = []

    def __iter__(self):
        self.reset()
        for window in self.windows:
            yield window

    def __len__(self):
        """
        Returns the number of windows in the collection
        :rtype: int
        """
        return len([_ for _ in self])

    def __getitem__(self, idx):
        """
        Get the window at the given index

        Any call to an ElementCollection that includes an adjacent selector
        can not be lazy loaded because it must store correct type

        Slices can only be lazy loaded if the indices are positive

        :param idx: index of wanted element, 0-indexed
        :type idx: int
        :return: instance of Element subclass
        :rtype: nerodia.elements.element.Element
        """
        nerodia.logger.deprecate('using indexing with windows',
                                 'Browser.switch_window() or Browser.window() with title, url, '
                                 'or element selectors',
                                 reference='https://watir.com/window_indexes',
                                 ids=['window_index'])
        try:
            return self._windows[idx]
        except IndexError:
            return None

    def __eq__(self, other):
        return list(self) == list(other)

    @property
    def is_empty(self):
        return len(self) == 0

    empty = is_empty

    @property
    def windows(self):
        if len(self._windows) == 0:
            handles = [wh for wh in self.browser.driver.window_handles if self._matches(wh)]
            self._windows = [Window(self.browser, {'handle': handle}) for handle in handles]
        return self._windows

    def reset(self):
        self._windows = []

    # Same code as Window

    def _matches(self, handle):
        try:
            orig = self.browser.driver.current_window_handle
        except NoSuchWindowException:
            orig = None
        try:
            if self.selector is None or len(self.selector) == 0:
                return True

            self.browser.driver.switch_to.window(handle)

            if 'title' in self.selector:
                title_value = self.selector.get('title')
                driver_title = self.browser.title
                matches_title = re.search(title_value, driver_title) is not None
            else:
                matches_title = True

            if 'url' in self.selector:
                url_value = self.selector.get('url')
                driver_url = self.browser.url
                matches_url = re.search(url_value, driver_url) is not None
            else:
                matches_url = True

            if 'element' in self.selector:
                matches_element = True if self.selector['element'].exists else False
            else:
                matches_element = True

            return matches_title and matches_url and matches_element
        except NoSuchWindowException:
            return False
        finally:
            current = self.browser.driver.window_handles
            orig = orig if orig in current else current[0]
            self.browser.driver.switch_to.window(orig)
