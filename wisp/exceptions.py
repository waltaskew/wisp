class WispException(Exception):
    """A base exception to distinguish user errors issued by wisp."""
    pass


def type_error(expected, val):
    """Build an exception message about how val should be a different type."""
    return WispException(
        'expected %s, not %s' % (expected, val)
    )
