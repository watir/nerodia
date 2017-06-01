import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class DList(HTMLElement):
    def to_dict(self):
        keys = [e.text for e in self.dts()]
        values = [e.text for e in self.dds()]
        return dict(zip(keys, values))
