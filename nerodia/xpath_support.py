import re

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class XpathSupport(object):
    LITERAL_REGEXP = re.compile(r'\A([^\[\]\\^$.|?*+()]*)\Z')

    @staticmethod
    def escape(value):
        if "'" in value:
            parts = ["'{}'".format(part) for part in value.split("'", -1)]
            string = ",\"'\",".join(parts)

            return 'concat({})'.format(string)
        else:
            return "'{}'".format(value)

    @staticmethod
    def lower(value):
        return "translate({},'ABCDEFGHIJKLMNOPQRSTUVWXYZ'," \
               "'abcdefghijklmnopqrstuvwxyz')".format(value)

    @staticmethod
    def is_simple_regexp(regex):
        if not isinstance(regex, Pattern) or regex.flags & re.IGNORECASE or not regex.pattern:
            return False

        return re.search(XpathSupport.LITERAL_REGEXP, regex.pattern) is not None
