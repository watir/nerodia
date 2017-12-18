import re

MODULE_MAPPING = {'frame': 'i_frame',
                  'anchor': 'link',
                  'o_list': 'list',
                  'u_list': 'list'}


def map_module(name):
    element_module = re.sub(r'([A-Z]{1})', r'_\1', name)[1:].lower()
    if element_module in list(MODULE_MAPPING):  # special cases
        return MODULE_MAPPING.get(element_module)
    else:
        return element_module
