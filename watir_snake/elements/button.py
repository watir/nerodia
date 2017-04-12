import six

from watir_snake.exception import Error
from .input import Input
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
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
        tn = self.tag_name

        if tn == 'input':
            return self.value
        elif tn == 'button':
            return super(Button, self).text
        else:
            raise Error("unknown tag name for button: {}".format(tn))
