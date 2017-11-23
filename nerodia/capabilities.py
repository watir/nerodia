from selenium.webdriver import DesiredCapabilities

import nerodia


class Capabilities(object):
    DEFAULT_URL = 'http://127.0.0.1:{}/wd/hub'

    def __init__(self, browser, **options):
        self.options = options.copy()

        if browser == 'remote' and 'browser' in self.options:
            self.browser = self.options.pop('browser')
        elif browser == 'remote' and 'desired_capabilities' in self.options:
            self.browser = self.options['desired_capabilities'].get('browserName')
        else:
            self.browser = browser

        if browser == 'remote' or options.get('url'):
            self.selenium_browser = 'remote'
        else:
            self.selenium_browser = browser

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
                self._process_firefox_options(browser_options)
            elif self.selenium_browser == 'safari':
                self._process_safari_options(browser_options)
            elif self.selenium_browser == 'remote':
                self._process_remote_options(browser_options)

    def _process_chrome_options(self, opts):
        from selenium.webdriver.chrome.options import Options
        if isinstance(opts, Options):
            options = opts
        else:
            options = Options()
            if 'args' in opts:
                for arg in opts.pop('args'):
                    options.add_argument(arg)
            # TODO: update this after next selenium py release, there is a headless convenience
            # method
            if 'headless' in opts:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
            if 'binary' in opts or 'binary_location' in opts:
                options.binary_location = opts.pop('binary') or opts.pop('binary_location')
            if 'debugger_address' in opts:
                options.debugger_address = opts.pop('debugger_address')
            if 'extensions' in opts:
                for path in opts.pop('extensions'):
                    options.add_extension(path)
            if 'encoded_extensions' in opts:
                for string in opts.pop('encoded_extensions'):
                    options.add_encoded_extension(string)
            if 'experimental_options' in opts:
                for name, value in opts.pop('experimental_options').items():
                    options.add_experimental_option(name, value)
        self.selenium_opts['chrome_options'] = options

    def _process_firefox_options(self, opts):
        from selenium.webdriver.firefox.options import Options
        if isinstance(opts, Options):
            options = opts
        else:
            options = Options()
            if 'args' in opts:
                for arg in opts.pop('args'):
                    options.add_argument(arg)
            if 'binary' in opts or 'binary_location' in opts:
                options.binary = opts.pop('binary') or opts.pop('binary_location')
            if 'prefs' in opts:
                for name, value in opts.pop('prefs').items():
                    options.set_preference(name, value)
            if 'proxy' in opts:
                options.proxy = opts.pop('proxy')
            if 'profile' in opts:
                options.profile = opts.pop('profile')
            if 'log_level' in opts:
                options.log.level = opts.pop('log_level')
        self.selenium_opts['firefox_options'] = options

    def _process_safari_options(self, opts):
        if 'technology_preview' in opts:
            self.selenium_opts['executable_path'] = \
                '/Applications/Safari Technology Preview.app/Contents/MacOS/safaridriver'

    def _process_remote_options(self, opts):
        if self.browser == 'chrome' and self.options.pop('headless', None):
            # TODO: update this after next selenium py release, options classes will be able to be
            # passed through remote
            args = self.options.pop('args', [])
            if 'desired_capabilities' in opts:
                caps = opts.pop('desired_capabilities')
            else:
                caps = DesiredCapabilities.CHROME.copy()
            caps['goog:chromeOptions'] = {'args': args + ['--headless', '--disable-gpu']}
            self.selenium_opts['desired_capabilities'] = caps

        if self.browser == 'safari' and self.options.pop('technology_preview', None):
            if 'desired_capabilities' in opts:
                caps = opts.pop('desired_capabilities')
            else:
                caps = DesiredCapabilities.SAFARI.copy()
            caps['safari.options'] = {'technologyPreview': opts.pop('technology_preview')}
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
