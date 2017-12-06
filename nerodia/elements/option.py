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
        Note that the text is either one of the following respectively:
            * label attribute
            * text attribute
            * inner element text
        :rtype: str
        """
        for attr in ['label', 'text']:
            val = self.attribute_value(attr)
            if val:
                return val

        return super(Option, self).text
