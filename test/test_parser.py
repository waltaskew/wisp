"""Tests for the wisp parser."""

import wisp.parser as parser
import wisp.wtypes as wtypes


def test_parse_bool():
    """Ensure we can parse true and false."""
    assert parser.parse_expr.parse('#t') == wtypes.Bool(True)
    assert parser.parse_expr.parse('#f') == wtypes.Bool(False)


def test_parse_string():
    """Ensure we can parse strings."""
    assert parser.parse_expr.parse('"abc"') == wtypes.String('abc')


def test_parse_symbol():
    """Ensure we can parse symbols."""
    assert parser.parse_expr.parse('abc') == wtypes.Symbol('abc')


def test_parse_integer():
    """Ensure we can parse integers."""
    assert parser.parse_expr.parse('123') == wtypes.Integer(123)


def test_parse_list():
    """Ensure we can parse lists."""
    assert parser.parse_expr.parse('(1    abc "abc" #t #f)') == wtypes.List([
        wtypes.Integer(1),
        wtypes.Symbol('abc'),
        wtypes.String('abc'),
        wtypes.Bool(True),
        wtypes.Bool(False),
    ])
