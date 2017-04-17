from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from .exception import NoMatchingWindowFoundException
from .wait.wait import Waitable, TimeoutError


class Window(Waitable):
    # TODO: include EventuallyPresent

    def __init__(self, driver, selector):
        self.driver = driver
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
        self.use()

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
        return size

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
        return pos

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
        hash(self.handle) ^ hash(self.__class__)

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
        self.driver.switch_to.window(self.original)
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
        import watir_snake
        if not watir_snake.relaxed_locate:
            self.assert_exists()
        try:
            self.wait_until(lambda: self.exists)
        except TimeoutError:
            raise NoMatchingWindowFoundException(str(self.selector))

    # private

    def _locate(self):
        if not self.selector:
            self.window_handle = None
        elif 'index' in self.selector:
            self.window_handle = self.driver.window_handles[int(self.selector.get('index'))]
        else:
            self.window_handle = next((x for x in self.driver.window_handles if
                                       self._matches(x) is True), False)
        return self.window_handle

    @property
    def _current_window(self):
        try:
            return self.driver.window_handle
        except WebDriverException:
            return None

    def _matches(self, handle):
        orig = self.driver.current_window_handle
        try:
            self.driver.switch_to.window(handle)

            matches_title = (not self.selector.get('title')) or \
                            self.selector.get('title') == self.driver.title
            matches_url = (not self.selector.get('url')) or \
                          self.selector.get('url') == self.driver.current_url

            return matches_title and matches_url
        except (NoSuchWindowException, WebDriverException):
            return False
        finally:
            self.driver.switch_to.window(orig)
