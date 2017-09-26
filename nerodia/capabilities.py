import nerodia


class Capabilities(object):
    DEFAULT_URL = 'http://127.0.0.1:{}/wd/hub'

    def __init__(self, browser, **options):
        self.browser = options.pop('browser') if browser == 'remote' else browser
        if browser == 'remote' or options.pop('url', None):
            self.selenium_browser = 'remote'
        else:
            self.selenium_browser = browser

        self.options = options
        self.selenium_opts = {}

    @property
    def kwargs(self):
        self._process_capabilities()
        return self.selenium_opts

    # private

    def _process_capabilities(self):
        url = None
        port = self.options.pop('port', None)
        if port:
            url = self.DEFAULT_URL.format(port)

        url = self.options.pop('url', url)
        if url:
            self.selenium_opts['command_executor'] = url

        self._process_browser_options()
        self._process_caps()

    def _process_browser_options(self):
        browser_options = self.options.pop('options', None)

        if self.selenium_browser == 'chrome':
            from selenium.webdriver.chrome.options import Options
            if isinstance(browser_options, Options):
                options = browser_options
                self.selenium_opts['chrome_options'] = options
            else:
                if 'args' in self.options:
                    options = Options()
                    args = self.options.pop('args')
                    for arg in args:
                        options.add_argument(arg)
                    self.selenium_opts['chrome_options'] = options
        elif self.selenium_browser == 'firefox' and browser_options is not None:
            from selenium.webdriver.firefox.options import Options
            if not isinstance(browser_options, Options):
                raise TypeError('options must be a type of Firefox Options class')
            self.selenium_opts['firefox_options'] = browser_options
        elif self.selenium_browser == 'safari' and browser_options is not None:
            if 'technology_preview' in self.options:
                self.selenium_opts['safari.options'] = \
                    {'technologyPreview': self.options.pop('technology_preview')}

    def _process_caps(self):
        caps = self.options.pop('desired_capabilities', None)

        if caps:
            nerodia.logger.warn('You can now pass values directly into nerodia.browser.Browser '
                                'without needing to use desired_capabilities')
            self.selenium_opts.update(self.options)
        else:
            from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
            browser = 'internetexplorer' if self.browser == 'ie' else self.browser
            caps = getattr(DesiredCapabilities, browser.upper())

        if self.browser in ['firefox', 'ie', 'edge']:
            self.selenium_opts['capabilities'] = caps
        else:
            self.selenium_opts['desired_capabilities'] = caps
