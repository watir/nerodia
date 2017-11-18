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

        if browser_options:
            if self.selenium_browser == 'chrome':
                self._process_chrome_options(browser_options)
            elif self.selenium_browser == 'firefox':
                self._process_chrome_options(browser_options)
            elif self.selenium_browser == 'safari':
                self._process_safari_options(browser_options)

    def _process_chrome_options(self, browser_options):
        from selenium.webdriver.chrome.options import Options
        if isinstance(browser_options, Options):
            options = browser_options
        else:
            options = Options()
            if 'args' in self.options:
                for arg in self.options.pop('args'):
                    options.add_argument(arg)
            if 'binary' in self.options or 'binary_location' in self.options:
                options.binary_location = self.options.pop('binary') or \
                                          self.options.pop('binary_location')
            if 'debugger_address' in self.options:
                options.debugger_address = self.options.pop('debugger_address')
            if 'extensions' in self.options:
                for path in self.options.pop('extensions'):
                    options.add_extension(path)
            if 'encoded_extensions' in self.options:
                for string in self.options.pop('encoded_extensions'):
                    options.add_encoded_extension(string)
            if 'experimental_options' in self.options:
                for name, value in self.options.pop('experimental_options').items():
                    options.add_experimental_option(name, value)
        self.selenium_opts['options'] = options

    def _process_firefox_options(self, browser_options):
        from selenium.webdriver.firefox.options import Options
        if isinstance(browser_options, Options):
            options = browser_options
        else:
            options = Options()
            if 'args' in self.options:
                for arg in self.options.pop('args'):
                    options.add_argument(arg)
            if 'binary' in self.options or 'binary_location' in self.options:
                options.binary = self.options.pop('binary') or self.options.pop('binary_location')
            if 'prefs' in self.options:
                for name, value in self.options.pop('prefs').items():
                    options.set_preference(name, value)
            if 'proxy' in self.options:
                options.proxy = self.options.pop('proxy')
            if 'profile' in self.options:
                options.profile = self.options.pop('profile')
            if 'log_level' in self.options:
                options.log.level = self.options.pop('log_level')
        self.selenium_opts['options'] = options

    def _process_safari_options(self, browser_options):
        if 'technology_preview' in self.options:
            from selenium.webdriver import DesiredCapabilities
            if 'desired_capabilities' in self.options:
                caps = self.options.pop('desired_capabilities')
            else:
                caps = DesiredCapabilities.SAFARI.copy()
            caps['safari.options'] = {'technologyPreview': self.options.pop('technology_preview')}
            self.selenium_opts['desired_capabilities'] = caps

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
