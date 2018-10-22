import six

from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Button(Input):
    """
    Class representing button elements

    This class covers both <button> and <input type="submit|reset|image|button" /> elements
    """
    VALID_TYPES = ['button', 'reset', 'submit', 'image']

    @property
    def text(self):
        """
        Returns the text of the button.

        For input elements, returns the 'value' attribute.
        For button elements, returns the inner text.

        :rtype: str
        """

        if self.tag_name == 'input':
            return self.value
        else:
            return super(Button, self).text
