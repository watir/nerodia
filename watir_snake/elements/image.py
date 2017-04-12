import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Form(HTMLElement):
    @property
    def loaded(self):
        """
        Returns True if the image is loaded
        :rtype: bool
        """
        if not self.complete:
            return False

        return self.driver.execute_script('return typeof arguments[0].naturalWidth != "undefined" '
                                          '&& arguments[0].naturalWidth > 0', self.element)

    @property
    def width(self):
        """
        Returns the image's width in pixels
        :rtype: int
        """
        self._wait_for_exists()
        return self.driver.execute_script("return arguments[0].width", self.element)
