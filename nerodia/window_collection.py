import nerodia


class WindowCollection():
    def __init__(self, windows):
        self._windows = windows

    def __iter__(self):
        for window in self._windows:
            yield window

    def __len__(self):
        """
        Returns the number of windows in the collection
        :rtype: int
        """
        return len(self._windows)

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
