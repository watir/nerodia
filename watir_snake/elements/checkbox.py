import six

from .input import Input
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class CheckBox(Input):
    @property
    def is_set(self):
        """
        Returns True if the element is checked
        :rtype: bool
        """
        return self._element_call(lambda _: self.element.selected)

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
        self._assert_enabled() if self.set == value else self.click

# TODO: Add container portion
# TODO: Add collection portion
