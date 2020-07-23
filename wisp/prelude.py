"""Provide basic builtin wisp functions."""

import functools
import operator
import typing

import wisp.wtypes as wtypes

T = typing.TypeVar('T')


def arity(n: int) -> typing.Callable[[wtypes.Callable], wtypes.Callable]:
    """Decorator enforcing the function is called with right number of arguments.

    Raise an exception if the decorated function is called with an arguments
    list of length besides n.
    """
    def decorator(func: wtypes.Callable) -> wtypes.Callable:
        def wrapper(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
            if len(args) != n:
                raise wtypes.WispException(
                    'called with %d arguments, requires %d' % (len(args), n)
                )
            else:
                return func(args)
        return wrapper
    return decorator


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


@arity(2)
def equal(args: typing.List[wtypes.Expression]) -> wtypes.Bool:
    """Return a boolean indicating if the two elements are equal."""
    return wtypes.Bool(args[0] == args[1])


@arity(1)
def quote(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Return the argument as-is, un-evaluated."""
    return args[0]


@arity(2)
def cons(args: typing.List[wtypes.Expression]) -> wtypes.List:
    """Attach the first argument to the head of the list in the second."""
    head, rest = args
    if isinstance(rest, wtypes.List):
        return wtypes.List([head] + rest.lst)
    else:
        raise wtypes.WispException('expected %s, not %s' % (wtypes.List, rest))


@arity(1)
def car(args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Return the first element of the given list."""
    return __list_op(lambda wlst: wlst.lst[0], args)


@arity(1)
def cdr(args: typing.List[wtypes.Expression]) -> wtypes.List:
    """Return all but the first element of the given list."""
    return __list_op(lambda wlst: wtypes.List(wlst.lst[1:]), args)


def __list_op(op: typing.Callable[[wtypes.List], T],
              args: typing.List[wtypes.Expression]) -> T:
    """Ensure args is a non-empty List and return the call of op on it."""
    val = args[0]
    if isinstance(val, wtypes.List):
        if val.lst:
            return op(val)
        else:
            raise wtypes.WispException('can not apply cdr to an empty list')
    else:
        raise wtypes.WispException('expected %s, not %s' % (wtypes.List, val))


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
        'eq?': wtypes.Function(equal),
        'quote': wtypes.SpecialForm(quote),
        'cons': wtypes.Function(cons),
        'car': wtypes.Function(car),
        'cdr': wtypes.Function(cdr),
    }
