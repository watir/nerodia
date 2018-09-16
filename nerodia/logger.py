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

    def ignore(self, *ids):
        for _id in ids:
            self._ignored.append(_id)

    def warning(self, msg, ids=None, *args, **kwargs):
        ids = ids or []
        if ids:
            message = '[{}]'.format(', '.join(ids))
        else:
            message = ''
        message += msg
        if len(set(self._ignored).intersection(ids)) == 0:
            self._logger.warning(message, *args, **kwargs)

    warn = warning

    def deprecate(self, old, new, reference=None, ids=None):
        ids = ids or []
        if 'deprecations' in self._ignored or set(self._ignored).intersection(ids):
            return
        message = '[{}]'.format(', '.join(ids)) if ids else ''
        ref_msg = '.'
        if reference:
            ref_msg += '; see explanation for this deprecation: {}.'.format(reference)

        self.warning('[DEPRECATION] {}{} is deprecated. Use {} instead'
                     '{}'.format(message, old, new, ref_msg))

    def __getattr__(self, item):
        return getattr(self._logger, item)
