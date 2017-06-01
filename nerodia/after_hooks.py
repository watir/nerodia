from contextlib import contextmanager


class AfterHooks(object):
    """
    After hooks are blocks that run after certain browser events.
    They are generally used to ensure application under test does not encounter
    any error and are automatically executed after following events:
        1. Open URL.
        2. Refresh page.
        3. Click, double-click or right-click on element.
        4. Alert closing.
    """

    def __init__(self, browser):
        self.browser = browser
        self.after_hooks = []

    def add(self, method=None, after_hook=None):
        """
        Adds new after hook
        :param method: callable method
        :param after_hook: callable object

        :Example:

        from __future__ import print_function
        browser.after_hooks.add(method=lambda b: 'Server Error' in browser.text and \
            print('Application exception or 500 error!')
        browser.goto('watir.github.io/404')    #=> 'Application exception or 500 error!'
        """
        if method:
            self.after_hooks.append(method)
        elif callable(after_hook):
            self.after_hooks.append(after_hook)
        else:
            raise ValueError('expected method or callable class')

    def delete(self, after_hook):
        """
        Deletes after hook
        :param after_hook: hook to delete

        :Example:

        from __future__ import print_function
        browser.after_hooks.add(method=lambda b: 'Server Error' in browser.text and \
            print('Application exception or 500 error!')
        browser.goto('watir.github.io/404')    #=> 'Application exception or 500 error!'
        browser.after_hooks.delete(browser.after_hooks[0])
        browser.refresh
        """
        self.after_hooks.remove(after_hook)

    def run(self):
        """ Runs after hooks """
        if self.after_hooks and self.browser.window().present:
            for hook in self.after_hooks:
                hook(self.browser)

    @contextmanager
    def without(self):
        """
        Executes a block without running error after hooks

        :Example:

        with browser.after_hooks.without():
            self.browser.element(name='new_user_button').click()
        """
        current_after_hooks = self.after_hooks
        self.after_hooks = []
        yield
        self.after_hooks = current_after_hooks

    def __len__(self):
        """
        Returns number of after hooks
        :rtype: int

        :Example:

        browser.after_hooks.add(method=lambda b: print('Some after_hook'))
        len(browser.after_hooks)    #=> 1
        """
        return len(self.after_hooks)

    def __getitem__(self, index):
        """
        Gets the after hook at the given index
        :param index: index of the after hook
        :return: callable object
        """
        return self.after_hooks[index]
