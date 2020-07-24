"""Tests ensuring types are evaluated properly."""

import pytest  # type: ignore

import wisp.env
import wisp.exceptions as exceptions
import wisp.wtypes as wtypes


def test_eval_string():
    """Ensure strings evaluate to themselves."""
    assert wtypes.String('abc').eval({}) == wtypes.String('abc')


def test_eval_integer():
    """Ensure integers evaluate to themselves."""
    assert wtypes.Integer(123).eval({}) == wtypes.Integer(123)


def test_eval_bool():
    """Ensure bools evaluate to themselves."""
    assert wtypes.Bool(True).eval({}) == wtypes.Bool(True)


def test_eval_symbol():
    """Ensure symbols evaluate to their bound value."""
    env = wisp.env.Environment({'a': wtypes.String('def')})
    assert wtypes.Symbol('a').eval(env) == wtypes.String('def')


def test_eval_missing_symbol():
    """Ensure an error is raised on missing symbols."""
    env = wisp.env.Environment({'a': wtypes.String('def')})
    with pytest.raises(exceptions.WispException):
        wtypes.Symbol('b').eval(env)


def test_eval_list():
    """Ensure lists are evaluated as post-fix function calls."""
    env = wisp.env.Environment({'+': wtypes.Function(
        lambda xs: wtypes.Integer(xs[0].val + xs[1].val)
    )})
    res = wtypes.List([
            wtypes.Integer(1), wtypes.Integer(2), wtypes.Symbol('+')
    ]).eval(env)
    assert res == wtypes.Integer(3)


def test_eval_empty_list():
    """Ensure empty lists are evaluated to empty lists."""
    assert wtypes.List([]).eval({}) == wtypes.List([])


def test_eval_list_without_a_func():
    """Ensure an error is raised when applying non-functions."""
    with pytest.raises(exceptions.WispException):
        wtypes.List([wtypes.Integer(1)]).eval({})
