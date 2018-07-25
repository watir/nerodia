import logging


class Logger(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__.split('.')[0])
        self.level = logging.WARNING
        self._filename = None
        self._ignored = []

    @property
    def level(self):
        return self._logger.level

    @level.setter
    def level(self, severity):
        if type(severity) == str:
            severity = severity.upper()
        self._logger.setLevel(severity)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, path):
        self._filename = path
        for hdlr in self._logger.handlers[:]:  # remove all old handlers
            hdlr.close()
            self._logger.removeHandler(hdlr)

        if path is not None:
            fileh = logging.FileHandler(path, 'a')
            self._logger.addHandler(fileh)

    def ignore(self, ign):
        self._ignored.append(ign)

    def warning(self, msg, ignores=None, *args, **kwargs):
        ignores = ignores or []
        if ignores:
            message = '[{}]'.format(', '.join(ignores))
        else:
            message = ''
        message += msg
        if len(set(self._ignored).intersection(ignores)) == 0:
            self._logger.warning(message, *args, **kwargs)

    warn = warning

    def deprecate(self, old, new, ignores=None):
        ignores = ignores or []
        if 'deprecations' in self._ignored or set(self._ignored).intersection(ignores):
            return
        if ignores:
            message = '[{}]'.format(', '.join(ignores))
        else:
            message = ''
        self.warning('[DEPRECATION] {}{} is deprecated. Use {} instead.'.format(message, old, new))

    def __getattr__(self, item):
        return getattr(self._logger, item)
