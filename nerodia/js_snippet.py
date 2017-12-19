from os import path


class JSSnippet(object):
    # private

    def _execute_js(self, function_name, *args):
        filepath = path.abspath(path.join(path.dirname(__file__),
                                          'js_snippets',
                                          '{}.js'.format(function_name)))
        if not path.isfile(filepath):
            from nerodia.exception import Error
            raise Error('Can not excute script as {!r} does not exist'.format(filepath))

        with open(filepath, 'r') as myfile:
            script = 'return ({}).apply(null, arguments)'.format(myfile.read())
            return self.query_scope.execute_script(script, *args)
