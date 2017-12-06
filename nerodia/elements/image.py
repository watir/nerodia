import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Image(HTMLElement):
    @property
    def loaded(self):
        """
        Returns True if the image is loaded
        :rtype: bool
        """
        if not self.complete:
            return False

        return self.driver.execute_script('return typeof arguments[0].naturalWidth != "undefined" '
                                          '&& arguments[0].naturalWidth > 0', self.el)
