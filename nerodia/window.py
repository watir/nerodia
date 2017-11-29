import re
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from .exception import NoMatchingWindowFoundException
from .wait.wait import Waitable, TimeoutError


class Window(Waitable):
    def __init__(self, browser, selector):
        self.browser = browser
        self.driver = browser.driver
        self.selector = selector
        self.original = self._current_window
        self.window_handle = None

        if not selector:
            self.window_handle = self.original
        elif 'handle' in selector:
            self.window_handle = selector.pop('handle')
        else:
            if not all(key in ['title', 'url', 'index'] for key in selector.keys()):
                raise ValueError('invalid window selector: {}'.format(selector))

    def __repr__(self):
        return '#<{}:0x{:x} located={}>'.format(self.__class__.__name__, hash(self) * 2,
                                                self.handle is not None)

    def __enter__(self):
        self.original = self._current_window
        return self.use()

    def __exit__(self, *args):
        self.unuse()

    @property
    def size(self):
        """
        Returns window size
        :rtype: dict

        :Example:

        browser.window.size    #=> {width: 1600, height: 1200}
        """
        with self:
            size = self.driver.get_window_size()
        return Dimension(**size)

    @property
    def position(self):
        """
        Returns window position
        :rtype: dict

        :Example:

        browser.window.position    #=> {x: 92, y: 76}
        """
        with self:
            pos = self.driver.get_window_position()
        return Point(**pos)

    def resize_to(self, width, height):
        """
        Resizes window to given width and height
        :param width: width to resize to
        :param height: height to resize to

        :Example:

        browser.window.resize_to(1600, 1200)
        """
        size = {'width': width, 'height': height}
        with self:
            self.driver.set_window_size(**size)
        return size

    def move_to(self, x, y):
        """
        Moves window to given x and y coordinates
        :param x: horizontal position
        :param y: vertical position

        :Example:

        browser.window.move_to(300, 200)
        """
        point = {'x': x, 'y': y}
        with self:
            self.driver.set_window_position(**point)
        return point

    def maximize(self):
        """
        Maximizes window

        :Example:

        browser.window.maximize()
        """
        with self:
            self.driver.maximize_window()

    @property
    def exists(self):
        """
        Returns True if the window exists
        :rtype: bool
        """
        try:
            self.assert_exists()
            return True
        except NoMatchingWindowFoundException:
            return False

    present = exists
    exist = exists

    def __eq__(self, other):
        """
        Returns True if two windows are equal
        :param other: the other window
        :rtype: bool

        :Example:

        browser.window(index=0) == browser.window(index=1)    #=> False
        """
        if not isinstance(other, Window):
            return False

        return self.handle == other.handle

    eql = __eq__

    def __hash__(self):
        return hash(self.handle) ^ hash(self.__class__)

    @property
    def is_current(self):
        """
        Returns True if the window is current

        :Example:

        browse.window.is_current

        :rtype: bool
        """
        return self._current_window == self.handle

    def close(self):
        """ Closes the window """
        if self == self.browser.original_window:
            self.browser._original_window = None
        if self._current_window == self.handle:
            self.driver.close()
        else:
            with self:
                self.driver.close()

    @property
    def title(self):
        """
        Returns the window title
        :rtype: str
        """
        with self:
            title = self.driver.title
        return title

    @property
    def url(self):
        """
        Returns the window URL
        :rtype: str
        """
        with self:
            url = self.driver.current_url
        return url

    def use(self):
        """
        Switches to given window

        :Example:

        browser.window(title='closeable window').use()
        :rtype: Window
        """
        if self.browser.original_window is None:
            self.browser._original_window = self
        self.wait_for_exists()
        self.driver.switch_to.window(self.handle)
        return self

    def unuse(self):
        """
        Returns to the original window

        :Example:

        window = browser.window(title='closeable window').use()
        window.unuse()
        :rtype: Window
        """
        current = self.driver.window_handles
        orig = self.original if self.original in current else current[0]
        self.driver.switch_to.window(orig)
        return self

    @property
    def handle(self):
        return self.window_handle or self._locate()

    # Referenced in EventuallyPresent
    def selector_string(self):
        return str(self.selector)

    def assert_exists(self):
        if self.handle not in self.driver.window_handles:
            raise NoMatchingWindowFoundException(str(self.selector))

    def wait_for_exists(self):
        import nerodia
        if not nerodia.relaxed_locate:
            self.assert_exists()
        try:
            self.wait_until(lambda w: w.exists)
        except TimeoutError:
            raise NoMatchingWindowFoundException(str(self.selector))

    # private

    def _locate(self):
        if not self.selector:
            self.window_handle = None
        elif 'index' in self.selector:
            try:
                self.window_handle = self.driver.window_handles[int(self.selector.get('index'))]
            except IndexError:
                self.window_handle = None
        else:
            self.window_handle = next((x for x in self.driver.window_handles if
                                       self._matches(x) is True), False)
        return self.window_handle

    @property
    def _current_window(self):
        try:
            return self.driver.current_window_handle
        except WebDriverException:
            return None

    def _matches(self, handle):
        try:
            orig = self.driver.current_window_handle
        except NoSuchWindowException:
            orig = None
        try:
            self.driver.switch_to.window(handle)

            if 'title' in self.selector:
                title_value = self.selector.get('title')
                driver_title = self.driver.title
                if isinstance(title_value, re._pattern_type):
                    matches_title = title_value.search(driver_title) is not None
                else:
                    matches_title = title_value == driver_title
            else:
                matches_title = True

            if 'url' in self.selector:
                url_value = self.selector.get('url')
                driver_url = self.driver.current_url
                if isinstance(url_value, re._pattern_type):
                    matches_url = url_value.search(driver_url) is not None
                else:
                    matches_url = url_value == driver_url
            else:
                matches_url = True

            return matches_title and matches_url
        except (NoSuchWindowException, WebDriverException):
            return False
        finally:
            current = self.driver.window_handles
            orig = orig if orig in current else current[0]
            self.driver.switch_to.window(orig)


class Dimension(object):
    __slots__ = ['width', 'height']

    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height


class Point(object):
    __slots__ = ['x', 'y']

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
