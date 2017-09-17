import pytest


def verify_cookies_count(browser, size):
    cookies = browser.cookies.to_list
    assert len(cookies) == size, 'expected {} cookies, ' \
                                 'got {}: {}'.format(size, len(cookies), cookies)


@pytest.fixture
def clear_cookies(browser):
    yield
    browser.cookies.clear()


@pytest.fixture
def verify_cookie(browser):
    verify_cookies_count(browser, 1)


@pytest.mark.page('set_cookie/index.html')
@pytest.mark.usefixtures('clear_cookies', 'verify_cookie')
class TestBrowserCookies(object):
    def test_gets_an_empty_list_of_cookies(self, browser, page):
        browser.goto(page.url('collections.html'))
        browser.cookies.clear()
        assert browser.cookies.to_list == []

    def test_gets_any_cookies_set(self, browser):
        cookie = browser.cookies.to_list[0]
        assert cookie.get('name') == 'monster'
        assert cookie.get('value') == '1'

    #
    # __getitem__

    def test_returns_cookie_by_name(self, browser):
        cookie = browser.cookies['monster']
        assert cookie.get('name') == 'monster'
        assert cookie.get('value') == '1'

    def test_returns_none_if_there_is_no_cookie_with_such_name(self, browser):
        assert browser.cookies['non_monster'] is None

    # TODO: xfail IE
    def test_adds_a_cookie(self, browser, page, bkwargs):
        # Use temp browser for safari
        temp_browser = browser.__class__(**bkwargs)
        try:
            temp_browser.goto(page.url('set_cookie/index.html'))
            verify_cookies_count(temp_browser, 1)
            temp_browser.cookies.add('foo', 'bar')
            verify_cookies_count(temp_browser, 2)
        finally:
            temp_browser.close()

    # TODO: xfail IE
    def test_removes_a_cookie(self, browser):
        browser.cookies.delete('monster')
        verify_cookies_count(browser, 0)

    # TODO: xfail IE, safari
    def test_clears_all_cookies(self, browser):
        browser.cookies.add('foo', 'bar')
        verify_cookies_count(browser, 2)
        browser.cookies.clear()
        verify_cookies_count(browser, 0)

    # TODO: xfail IE
    def test_saves_cookies_to_file(self, browser, temp_file):
        from json import load
        browser.cookies.save(temp_file.name)
        assert load(temp_file) == browser.cookies.to_list

    # TODO: xfail IE
    def test_loads_cookies_from_file(self, browser, temp_file):
        from json import load
        browser.cookies.save(temp_file.name)
        browser.cookies.clear()
        browser.cookies.load(temp_file.name)

        expected = browser.cookies.to_list
        actual = load(temp_file)
        # https://code.google.com/p/selenium/issues/detail?id=6834
        for each in expected:
            each.pop('expires', None)
            each.pop('expiry', None)
        for each in actual:
            each.pop('expires', None)
            each.pop('expiry', None)

        assert actual == expected
