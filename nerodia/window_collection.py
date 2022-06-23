import re

import nerodia
from nerodia.wait.wait import Waitable
from nerodia.window import Window


class WindowCollection(Waitable):

    def __init__(self, browser, selector=None):
        if selector and not all(key in ['title', 'url'] for key in selector.keys()):
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
            wins = [Window(self.browser, {'handle': handle}) for handle in
                    self.browser.driver.window_handles]
            if self.selector is None:
                self._windows = wins
            else:
                self._windows = [w for w in wins if all(re.search(v, getattr(w, k)) is not None
                                                        for k, v in self.selector.items())]
        return self._windows

    def reset(self):
        self._windows = []
