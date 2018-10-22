from selenium.common.exceptions import InvalidElementStateException

from nerodia.exception import Error


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
        """
        Returns value of the element
        :rtype: str
        """
        try:
            return self.attribute_value('value') or ''
        except InvalidElementStateException:
            return ''

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
        input_value = ''.join(args)
        if input_value:
            self.set(input_value[0])
            if hasattr(self, '_content_editable') and self._content_editable is not None:
                return self._set_content_editable(*args)
            if len(input_value) > 1:
                self._element_call(lambda: self._execute_js('setValue', self.el, input_value[:-1]))
                self.append(input_value[-1])
        value = self.value
        if value != input_value:
            raise Error("#js_set value: '{}' does not match expected input: "
                        "'{}'".format(value, input_value))

    def append(self, *args):
        """
        Appends the given value to the text in the text field
        :param args: value to add to the input
        """
        if hasattr(self, '_content_editable') and self._content_editable is not None:
            raise NotImplementedError('#append method is not supported with contenteditable '
                                      'element')
        self.send_keys(*args)

    def clear(self):
        """
        Clears the text field
        :return:
        """
        self._element_call(lambda: self.el.clear(), self.wait_for_writable)

    # private

    def _set_content_editable(self, *args):
        input_text = ''.join(args)
        self._element_call(lambda: self._execute_js('setText', self.el, input_text))
        text = self.text
        if text == input_text:
            return
        raise Error("#js_set text: '{}' does not match expected input: "
                    "'{}'".format(text, input_text))
