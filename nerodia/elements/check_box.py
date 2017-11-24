import six

from .html_elements import InputCollection
from .html_elements import Input
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

    is_checked = is_set

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

    check = set

    def clear(self):
        self.set(value=False)

    uncheck = clear


@six.add_metaclass(MetaHTMLElement)
class CheckBoxCollection(InputCollection):
    pass
