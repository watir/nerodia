import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Option(HTMLElement):
    _aliases = [['select', 'click'], ['toggle', 'click']]

    def clear(self):
        """ Un-selects the option """
        if self.selected:
            self.click()

    @property
    def selected(self):
        """
        Returns True if the option is selected
        :rtype: bool
        """
        return self._element_call(lambda _: self.element.is_selected)

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
        attribute = next((x for x in ['label', 'text'] if self._is_attribute(x) is True), False)
        if attribute is not False:
            return self._attribute_value(attribute)
        else:
            return super(Option, self).text
