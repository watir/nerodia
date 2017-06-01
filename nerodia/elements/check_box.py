import six

from .html_elements import InputCollection
from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class CheckBox(Input):
    @property
    def is_set(self):
        """
        Returns True if the element is checked
        :rtype: bool
        """
        return self._element_call(lambda: self.el.is_selected())

    def set(self, value=True):
        """
        Sets checkbox to the given value

        :param value: True to check, False to uncheck

        :Example:

        checkbox = browser.checkbox(id='new_user_interests_cars')
        checkbox.is_set        #=> false
        checkbox.set()
        checkbox.is_set         #=> true
        checkbox.set(False)
        checkbox.set            #=> false
        """
        self._assert_enabled() if self.is_set == value else self.click()

    def clear(self):
        self.set(value=False)


@six.add_metaclass(MetaHTMLElement)
class CheckBoxCollection(InputCollection):
    pass
