class XpathSupport(object):
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
