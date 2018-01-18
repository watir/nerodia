from nerodia import browser


class BasePage(object):

    def __init__(self, br):
        if isinstance(br, browser.Browser):
            self.browser = br
        elif isinstance(br, str):
            self.browser = browser.Browser(br)
        else:
            raise TypeError("Incorrect object type passed to constructor")

    def close(self):
        self.browser.close()

    def goto(self, url=None):
        self.browser.goto(url) if url else self.browser.goto(self.url)


class WatirPage(BasePage):
    """Page object for Watir's homepage www.watir.com."""
    def __init__(self, browser):
        super().__init__(browser)
        self.url = 'www.watir.com'
        self.intro = self.browser.div(class_name='intro')
        self.news = self.browser.link(href='/blog')


"""Sample code that should print out expected text."""
w = WatirPage('chrome')
w.goto()
print(w.intro.text)
w.news.click()
print(w.browser.text)
w.close()
