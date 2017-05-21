import six

from .html_elements import InputCollection
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
        return self._element_call(lambda: self.el.selected)

    def set(self, value=True):
        """ Selects the radio input """
        if not self.is_set:
            self.click()


@six.add_metaclass(MetaHTMLElement)
class RadioCollection(InputCollection):
    # private

    @property
    def _element_class(self):
        return Radio
