import watir_snake


class MetaElement(type):
    def __new__(cls, name, parents, dct):
        final_dict = {}

        attrs = []
        for key, value in dct.items():
            if key.startswith('_attr'):
                attr_name = key.split('_attr_')[-1]
                typ, val = value
                final_dict[attr_name] = property(fget=make_attr(typ, val))
                attrs.append(attr_name)
            elif key.startswith('_aliases'):
                continue
            else:
                final_dict[key] = value
        auto_gen = getattr(watir_snake.generated_attributes, name.lower(), [])
        for each in auto_gen:
            typ, key, val = each
            final_dict[key] = property(fget=make_attr(typ, val))
            attrs.append(key)

        for parent in parents:
            attrs.extend(getattr(parent, 'ATTRIBUTES', []))

        for alias in dct.get('_aliases', []):
            new_name, old_name = alias
            final_dict[new_name] = property(fget=make_alias(old_name))
            attrs.append(new_name)

        final_dict['ATTRIBUTES'] = list(set(attrs))

        inst = super(MetaElement, cls).__new__(cls, name, parents, final_dict)

        return inst


def make_attr(typ, val):
    if typ == bool:
        def attr_bool(self):
            return getattr(self, 'attribute_value')(val) == 'true'

        return attr_bool
    elif typ == int:
        def attr_int(self):
            value = getattr(self, 'attribute_value')(val)
            return value and int(value)

        return attr_int
    elif typ == float:
        def attr_float(self):
            value = getattr(self, 'attribute_value')(val)
            return value and float(value)

        return attr_float
    else:
        def attr_str(self):
            return str(getattr(self, 'attribute_value')(val))

        return attr_str

def make_alias(old_name):
    def alias(self):
        return getattr(self, old_name)
    return alias
