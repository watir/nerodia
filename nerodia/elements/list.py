import six

from ..elements.html_elements import LICollection, HTMLElement
from ..meta_elements import MetaHTMLElement


class List(object):
    def __iter__(self):
        """
        Yields each LI associated with this list

        :rtype: iter

        :Example:

        divs = browser.divs(class='kls')
        for li in browser.ol():
             print(li.text)
        """
        for e in self.list_items:
            yield e

    def __getitem__(self, idx):
        """
        Returns item from this list at the given index

        :param idx: index of wanted element, 0-indexed
        :type idx: int
        :return: instance of Element subclass
        :rtype: nerodia.elements.element.Element
        """
        return self.list_items[idx]

    @property
    def list_items(self):
        return LICollection(self, {'adjacent': 'child', 'tag_name': 'li'})


@six.add_metaclass(MetaHTMLElement)
class OList(HTMLElement, List):
    pass


@six.add_metaclass(MetaHTMLElement)
class UList(HTMLElement, List):
    pass
