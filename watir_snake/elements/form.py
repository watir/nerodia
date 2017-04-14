import six

from .html_element import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Form(HTMLElement):
    def submit(self):
        self._element_call(lambda: self.element.submit(), self._wait_for_present)
        # browser.after_hooks.run()  # TODO
