"""Provide basic builtin wisp functions."""

import functools
import operator
import typing

import wisp.wtypes as wtypes


def add(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Add each argument, returning zero for no arguments."""
    return __wrap_operator(operator.add, args)


def sub(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Subtract each argument, returning zero for no arguments."""
    return __wrap_operator(operator.sub, args)


def mul(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Multiply each argument, returning zero for no arguments."""
    return __wrap_operator(operator.mul, args)


def div(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Divide each argument, returning zero for no arguments."""
    return __wrap_operator(operator.floordiv, args)


def __wrap_operator(op,
                    args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Reduce the given operator over the given args. Return 0 for no args."""
    if not args:
        return wtypes.Integer(0)
    else:
        return functools.reduce(op, args)


def env() -> wtypes.Environment:
    """Build an environment with wisp builtin functions defined."""
    return {
        '+': wtypes.Function(add),
        '-': wtypes.Function(sub),
        '*': wtypes.Function(mul),
        '/': wtypes.Function(div),
    }
