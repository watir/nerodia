from .logger import Logger

__version__ = '0.3.0'

ttc = None

tag_to_class = ttc or {}

#
# Whether or not Watip should wait for an element to be found or present before taking an action.
# Defaults to true.
#

relaxed_locate = True

#
# Default wait time for wait methods.
#

default_timeout = 30

from . import locators, tag_map  # noqa

#
# Whether the locators should be used from a different namespace.
# Defaults to nerodia.locators.
#

locator_namespace = locators

#
# Custom logger
#

logger = Logger()


def element_class_for(tag_name):
    return tag_to_class.get(tag_name)
