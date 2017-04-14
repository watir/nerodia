import six

from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Radio(Input):
    @property
    def is_set(self):
        """
        Returns True if the element is selected
        :rtype: bool
        """
        return self._element_call(lambda: self.element.selected)

    def set(self, value=True):
        """ Selects the radio input """
        if not self.is_set:
            self.click()

# TODO: Add container portion
# TODO: Add collection portion
