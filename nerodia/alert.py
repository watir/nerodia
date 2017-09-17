from selenium.common.exceptions import NoAlertPresentException

import nerodia
from .exception import UnknownObjectException
from .wait.wait import Waitable, TimeoutError


class Alert(Waitable):
    def __init__(self, browser):
        self.browser = browser
        self.alert = None

    @property
    def text(self):
        """
        Returns the text of the alert
        :rtype: str

        :Example:

        browser.alert.text    #=> 'ok'
        """
        self.wait_for_exists()
        return self.alert.text

    def ok(self):
        """
        Closes alert or accepts prompts/confirms

        :Example:

        browser.alert.ok
        browser.alert.exists    #=> False
        """
        self.wait_for_exists()
        self.alert.accept()
        self.browser.after_hooks.run()

    def close(self):
        """
        Closes alert or cancels prmopts/confirms

        :Example:

        browser.alert.close()
        browser.alert.exists    #=> False
        """
        self.wait_for_exists()
        self.alert.dismiss()
        self.browser.after_hooks.run()

    def set(self, value):
        """
        Enters text to prompt
        :param value: keys to send

        :Example:

        browser.alert.set('Text for prompt')
        browser.alert.ok()
        """
        self.wait_for_exists()
        self.alert.send_keys(value)

    @property
    def exists(self):
        """
        Returns True if alert, confirm, or prompt is present and False otherwise
        :rtype: bool

        :Example:

        browser.alert.exists    #=> True
        """
        try:
            self.assert_exists()
            return True
        except UnknownObjectException:
            return False

    present = exists

    @property
    def selector_string(self):
        return 'alert'

    def assert_exists(self):
        try:
            self.alert = self.browser.driver.switch_to.alert
            self.alert.text
        except NoAlertPresentException:
            raise UnknownObjectException('unable to locate alert')

    def wait_for_exists(self):
        if not nerodia.relaxed_locate:
            return self.assert_exists()

        try:
            return self.wait_until(lambda a: a.exists, message='waiting for alert')
        except TimeoutError:
            if nerodia.default_timeout != 0:
                nerodia.logger.warn('This code has slept for the duration of the default timeout '
                                    'waiting for an Alert to exist. If the test is still passing, '
                                    'consider using Alert#exists? instead of rescuing '
                                    'UnknownObjectException')
            raise UnknownObjectException('unable to locate alert')
