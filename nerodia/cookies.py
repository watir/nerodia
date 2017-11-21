import time
from json import dump, load


class Cookies(object):
    def __init__(self, driver):
        self.driver = driver

    @property
    def to_list(self):
        """
        Returns array of cookies
        :rtype: list[dict]

        :Example:

        browser.cookies.to_list
        #=> [{name: 'my_session', value: 'BAh7B0kiD3Nlc3Npb25faWQGOgZFRkk', domain: 'mysite.com'}]
        """
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            expire = cookie.get('expires')
            cookie['expires'] = self._to_time(expire) if expire else None
        return cookies

    def __getitem__(self, name):
        """
        Returns a cookie by name
        :param name: name of cookie
        :rtype: dict

        :Example:

        browser.cookies['my_session']
        #=> {name: 'my_session', value: 'BAh7B0kiD3Nlc3Npb25faWQGOgZFRkk', domain: 'mysite.com'}
        """
        return next((c for c in self.to_list if c.get('name') == name), None)

    def add(self, name, value, **kwargs):
        """
        Adds new cookie

        :Example:

        browser.cookies.add('my_session', 'BAh7B0kiD3Nlc3Npb25faWQGOgZFRkk', domain='mysite.com')
        """
        cookie = {'name': name, 'value': value}
        keys = list(kwargs)
        if 'secure' in keys:
            cookie['secure'] = kwargs.get('secure')
        if 'path' in keys:
            cookie['path'] = kwargs.get('path')
        if 'expires' in keys:
            cookie['expires'] = kwargs.get('expires')
        if 'domain' in keys:
            cookie['domain'] = kwargs.get('domain')
        self.driver.add_cookie(cookie)

    def delete(self, name):
        """ Deletes cookie by given name """
        self.driver.delete_cookie(name)

    def clear(self):
        """ Deletes all cookies """
        self.driver.delete_all_cookies()

    def save(self, file='.cookies'):
        """
        Save cookies to file
        :param file: file path

        :Example:

        browser.cookies.save('.cookies')
        """
        with open(file, 'w') as f:
            dump(self.to_list, f, indent=4)

    def load(self, file='.cookies'):
        """
        Loads cookies from file
        :param file: file path

        :Example:

        browser.cookies.load('.cookies')
        """
        with open(file, 'r') as f:
            for cookie in load(f):
                self.add(cookie.pop('name'), cookie.pop('value'), **cookie)

    # private

    def _to_time(self, dt):
        return time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(time.mktime(dt.timetuple())))
