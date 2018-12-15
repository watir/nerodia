import pytest

pytestmark = pytest.mark.page('scroll.html')


def visible(browser, element):
    return browser.execute_script('return isElementInViewport(arguments[0]);', element)


class TestScrollingBrowser(object):

    # to

    def test_scrolls_to_the_top_of_the_page(self, browser):
        browser.scroll.to('bottom')
        browser.scroll.to('top')
        assert visible(browser, browser.button(text='Top')) is True
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is False

    def test_scrolls_to_the_center_of_the_page(self, browser):
        browser.scroll.to('center')
        assert visible(browser, browser.button(text='Top')) is False
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is False

    def test_scrolls_to_the_bottom_of_the_page(self, browser):
        browser.scroll.to('bottom')
        assert visible(browser, browser.button(text='Top')) is False
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is True

    def test_scrolls_to_coordinates(self, browser):
        button = browser.button(text='Bottom')
        browser.scroll.to([button.wd.location['x'], button.wd.location['y']])
        assert visible(browser, button) is True

    def test_raises_error_when_scroll_point_is_not_valid(self, browser):
        with pytest.raises(ValueError):
            browser.scroll.to('blah')

    # by

    def test_scrolls_by_offset(self, browser):
        browser.scroll.to('bottom')
        browser.scroll.by(-10000, -10000)
        assert visible(browser, browser.button(text='Top')) is True
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is False


class TestScrollingElement(object):

    # to

    def test_scrolls_to_the_top_of_the_element(self, browser):
        browser.button(text='Center').scroll.to()
        assert visible(browser, browser.button(text='Top')) is False
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is True

    def test_scrolls_to_the_center_of_the_element(self, browser):
        browser.button(text='Center').scroll.to('center')
        assert visible(browser, browser.button(text='Top')) is False
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is False

    def test_scrolls_to_the_bottom_of_the_element(self, browser):
        browser.button(text='Center').scroll.to('bottom')
        assert visible(browser, browser.button(text='Top')) is True
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is False

    def test_scrolls_to_the_element_multiple_times(self, browser):
        for i in range(2):
            browser.button(text='Center').scroll.to('center')
            assert visible(browser, browser.button(text='Top')) is False

    def test_raises_error_when_scroll_param_is_not_valid(self, browser):
        with pytest.raises(ValueError):
            browser.button(text='TOP').scroll.to('blah')

    # by

    def test_scrolls_by_offset(self, browser):
        browser.scroll.to('bottom')
        browser.button(text='Bottom').scroll.by(-10000, -10000)
        assert visible(browser, browser.button(text='Top')) is True
        assert visible(browser, browser.button(text='Center')) is True
        assert visible(browser, browser.button(text='Bottom')) is False
