import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Font(HTMLElement):

    @property
    def size(self):
        """
        Returns the size of the font
        :rtype: int

        :Example:

        browser.font().size    #=> 12
        """
        self.attribute_value('size')
