class UserEditable(object):

    def set(self, *args):
        """
        Clear the element, the type in the given value
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
