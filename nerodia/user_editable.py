class UserEditable(object):

    def set(self, *args):
        """
        Clear the element, then type in the given value
        :param args: value to set the input to
        """
        def func():
            self.el.clear()
            self.el.send_keys(*args)
        self._element_call(func, self.wait_for_writable)

    @property
    def value(self):
        return self.attribute_value('value')

    @value.setter  # alias
    def value(self, *args):
        self.set(*args)

    def js_set(self, *args):
        """
        Uses JavaScript to enter most of the given value
        Selenium is used to enter the first and last characters (in order to raise an error if the
        element would normally raise on sending keys)

        :param value: value to set the input to
        """
        from nerodia.exception import Error
        value = ''.join(args)
        if value:
            self.set(value[0])
            if len(value) > 1:
                self._element_call(lambda: self._execute_js('setValue', self.el, value[:-1]))
                self.append(value[-1])
        if self.value != value:
            raise Error('js_set value does not match expected input')

    def append(self, *args):
        """
        Appends the given value to the text in the text field
        :param args: value to add to the input
        """
        self.send_keys(*args)

    def clear(self):
        """
        Clears the text field
        :return:
        """
        self._element_call(lambda: self.el.clear(), self.wait_for_writable)
