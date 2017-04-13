import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Anchor(HTMLElement):
    _attr_href = (str, 'href')

# TODO: container
