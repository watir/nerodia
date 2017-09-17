import logging


class Logger(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__.split('.')[0])
        self.level = logging.WARNING
        self._filename = None

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
            self._logger.removeHandler(hdlr)

        if path is not None:
            fileh = logging.FileHandler(path, 'a')
            self._logger.addHandler(fileh)

    def deprecate(self, old, new):
        self.warn('[DEPRECATION] {} is deprecated. Use {} instead.'.format(old, new))

    def __getattr__(self, item):
        return getattr(self._logger, item)
