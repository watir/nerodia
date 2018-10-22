class Error(Exception):
    pass


class UnknownObjectException(Error):
    pass


class ObjectDisabledException(Error):
    pass


class ObjectReadOnlyException(Error):
    pass


class NoValueFoundException(Error):
    pass


class NoMatchingWindowFoundException(Error):
    pass


class UnknownFrameException(Error):
    pass


class LocatorException(Error):
    pass
