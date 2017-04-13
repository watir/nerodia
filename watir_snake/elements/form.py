import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Form(HTMLElement):
    def submit(self):
        self._element_call(lambda: self.element.submit(), self._wait_for_present)
        # browser.after_hooks.run()  # TODO
