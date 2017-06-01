from os import path


def load_atoms(*args, **kwargs):
    cls = type(*args, **kwargs)
    cls.load('fireEvent')
    cls.load('getOuterHtml')
    cls.load('getInnerHtml')
    return cls


class Atoms(object):
    __metaclass__ = load_atoms

    ATOMS = {}

    @classmethod
    def load(cls, function_name):
        filepath = path.abspath(path.join(path.dirname(__file__), 'atoms',
                                          '{}.js'.format(function_name)))
        with open(filepath, 'r') as myfile:
            cls.ATOMS[function_name] = myfile.read()

    # private

    def _execute_atom(self, function_name, *args):
        script = 'return ({}).apply(null, arguments)'.format(
            self.__class__.ATOMS.get(function_name))
        return self.driver.execute_script(script, *args)
