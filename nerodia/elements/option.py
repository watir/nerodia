import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Option(HTMLElement):
    # alias
    def select(self):
        self.click()

    toggle = select

    def clear(self):
        """ Un-selects the option """
        if self.is_selected:
            self.click()

    @property
    def is_selected(self):
        """
        Returns True if the option is selected
        :rtype: bool
        """
        return self._element_call(lambda: self.el.is_selected())

    @property
    def text(self):
        """
        Returns the text of the option
        getAttribute atom pulls the text value if the label does not exist
        :rtype: str
        """
        return self.attribute_value('label')
