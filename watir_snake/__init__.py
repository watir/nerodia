from . import browser, elements, html_attributes, locators, svg_attributes

#
# Whether or not Watip should wait for an element to be found or present before taking an action.
# Defaults to true.
#

relaxed_locate = True

#
# Default wait time for wait methods.
#

default_timeout = 30

#
# Whether the locators should be used from a different namespace.
# Defaults to watir_snake.locators.
#

locator_namespace = locators

ttc = None


@property
def tag_to_class():
    """
    :rtype: dict
    """
    return ttc or {}


def element_class_for(tag_name):
    return tag_to_class.get(tag_name.to_sym) or elements.html_elements.HTMLElement
