import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Input(HTMLElement):
    def label(self):
        """
        Returns label element associated with Input element.

        :rtype: nerodia.elements.html_elements.Label
        """
        return self.parent(tag_name='form').label(**{'for': self.id})
