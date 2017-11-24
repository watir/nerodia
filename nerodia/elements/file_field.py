from errno import ENOENT

import six
from os import path

from .html_elements import InputCollection
from .html_elements import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class FileField(Input):
    def set(self, filepath):
        """
        Set the file field to the given path

        :param filepath: path to the file
        :raises: ENOENT
        """
        if not path.exists(filepath):
            raise ENOENT
        self._element_call(lambda: self.el.send_keys(filepath))


@six.add_metaclass(MetaHTMLElement)
class FileFieldCollection(InputCollection):
    pass
