"""Parser for the wisp language."""

import parsec  # type: ignore

import wisp.wtypes as wtypes


@parsec.generate
def parse_string():
    """Parse a string as any characters enclosed between two "s."""
    yield parsec.string('"')
    chars = yield parsec.many(parsec.none_of('"'))
    yield parsec.string('"')
    return wtypes.String(''.join(chars))


@parsec.generate
def parse_symbol():
    """Parse a symbol as a non-digit followed by any characters."""
    first = yield parsec.letter()
    rest = yield parsec.many(parsec.letter() | parsec.digit())
    return wtypes.Symbol(first + ''.join(rest))


@parsec.generate
def parse_int():
    """Parse an integer as a sequence of digits."""
    digits = yield parsec.many1(parsec.digit())
    return wtypes.Integer(int(''.join(digits)))


@parsec.generate
def parse_true():
    """Parse a boolean true from a #t lexeme."""
    yield parsec.string('#t')
    return wtypes.Bool(True)


@parsec.generate
def parse_false():
    """Parse a boolean false from a #f lexeme."""
    yield parsec.string('#f')
    return wtypes.Bool(False)


@parsec.generate
def parse_bool():
    """Parse a boolean true or false."""
    val = yield parse_true ^ parse_false
    return val


@parsec.generate
def parse_list():
    """Parse a list as a ()-enclosed sequence of expressions."""
    yield parsec.string('(')
    vals = yield parsec.sepBy(parse_expr, parsec.many1(parsec.space()))
    yield parsec.string(')')
    return wtypes.List(vals)


parse_expr = (parse_bool |
              parse_string |
              parse_symbol |
              parse_int |
              parse_list)
