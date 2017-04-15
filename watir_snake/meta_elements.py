from . import html_attributes, svg_attributes


class MetaHTMLElement(type):
    def __new__(cls, name, parents, dct):
        final_dict = create_attributes(name, parents, dct, html_attributes)

        inst = super(MetaHTMLElement, cls).__new__(cls, name, parents, final_dict)

        return inst


class MetaSVGElement(type):
    def __new__(cls, name, parents, dct):
        final_dict = create_attributes(name, parents, dct, svg_attributes)

        inst = super(MetaSVGElement, cls).__new__(cls, name, parents, final_dict)

        return inst


def create_attributes(name, parents, dct, generated):
    final_dict = {}

    attrs = []
    for key, value in dct.items():
        if key.startswith('_attr'):
            attr_name = key.split('_attr_')[-1]
            typ, val = value
            final_dict[attr_name] = property(fget=make_attr(typ=typ, val=val))
            attrs.append(attr_name)
        elif key.startswith('_aliases'):
            continue
        else:
            final_dict[key] = value
            attrs.append(key)
    auto_gen = getattr(generated, name.lower(), [])
    for each in auto_gen:
        typ, key, val = each
        final_dict[key] = property(fget=make_attr(typ, val))
        attrs.append(key)

    for parent in parents:
        attrs.extend(getattr(parent, 'ATTRIBUTES', []))

    final_dict['ATTRIBUTES'] = list(set(attrs))
    return final_dict


def make_attr(typ, val):
    if typ == bool:
        def attr_bool(self):
            return self.attribute_value(val) == 'true'

        return attr_bool

    elif typ == int:
        def attr_int(self):
            value = self.attribute_value(val)
            return value and int(value)

        return attr_int

    elif typ == float:
        def attr_float(self):
            value = self.attribute_value(val)
            return value and float(value)

        return attr_float

    else:
        def attr_str(self):
            return str(self.attribute_value(val))

        return attr_str
