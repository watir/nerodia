import six

from .html_elements import InputCollection
from .html_elements import Input
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

    is_selected = is_set

    def set(self):
        """ Selects the radio input """
        if not self.is_set:
            self.click()

    select = set


@six.add_metaclass(MetaHTMLElement)
class RadioCollection(InputCollection):
    # private

    @property
    def _element_class(self):
        return Radio
