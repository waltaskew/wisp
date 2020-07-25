"""Provide basic builtin wisp functions."""

import functools
import operator
import typing

import wisp.env
import wisp.exceptions as exceptions
import wisp.wtypes as wtypes

T = typing.TypeVar('T')


def arity(n: int) -> typing.Callable[[wtypes.Callable], wtypes.Callable]:
    """Decorator enforcing the function is called with right number of arguments.

    Raise an exception if the decorated function is called with an arguments
    list of length besides n.
    """
    def decorator(func: wtypes.Callable) -> wtypes.Callable:
        @functools.wraps(func)
        def wrapper(args: typing.List[wtypes.Expression],
                    env: wisp.env.Environment) -> wtypes.Expression:
            if len(args) != n:
                raise exceptions.WispException(
                    'called with %d arguments, requires %d' % (len(args), n)
                )
            else:
                return func(args, env)
        return wrapper
    return decorator


def add(args: typing.List[wtypes.Expression],
        env: wisp.env.Environment) -> wtypes.Expression:
    """Add each argument, returning zero for no arguments."""
    return __wrap_operator(operator.add, args)


def sub(args: typing.List[wtypes.Expression],
        env: wisp.env.Environment) -> wtypes.Expression:
    """Subtract each argument, returning zero for no arguments."""
    return __wrap_operator(operator.sub, args)


def mul(args: typing.List[wtypes.Expression],
        env: wisp.env.Environment) -> wtypes.Expression:
    """Multiply each argument, returning zero for no arguments."""
    return __wrap_operator(operator.mul, args)


def div(args: typing.List[wtypes.Expression],
        env: wisp.env.Environment) -> wtypes.Expression:
    """Divide each argument, returning zero for no arguments."""
    return __wrap_operator(operator.floordiv, args)


@arity(2)
def is_equal(args: typing.List[wtypes.Expression],
             env: wisp.env.Environment) -> wtypes.Bool:
    """Return a boolean indicating if the two elements are equal."""
    return wtypes.Bool(args[0] == args[1])


@arity(1)
def quote(args: typing.List[wtypes.Expression],
          env: wisp.env.Environment) -> wtypes.Expression:
    """Return the argument as-is, un-evaluated."""
    return args[0]


@arity(2)
def cons(args: typing.List[wtypes.Expression],
         env: wisp.env.Environment) -> wtypes.List:
    """Attach the first argument to the head of the list in the second."""
    head, rest = args
    if isinstance(rest, wtypes.List):
        return wtypes.List([head] + rest.items)
    else:
        raise exceptions.type_error(wtypes.List, rest)


@arity(1)
def car(args: typing.List[wtypes.Expression],
        env: wisp.env.Environment) -> wtypes.Expression:
    """Return the first element of the given list."""
    return __list_op(lambda wlst: wlst.items[0], args)


@arity(1)
def cdr(args: typing.List[wtypes.Expression],
        env: wisp.env.Environment) -> wtypes.List:
    """Return all but the first element of the given list."""
    return __list_op(lambda wlst: wtypes.List(wlst.items[1:]), args)


@arity(1)
def is_atom(args: typing.List[wtypes.Expression],
            env: wisp.env.Environment) -> wtypes.Bool:
    """Indicate whether we're passed a list or an atom."""
    return wtypes.Bool(not isinstance(args[0], wtypes.List))


@arity(2)
def define(args: typing.List[wtypes.Expression],
           env: wisp.env.Environment) -> wtypes.Symbol:
    """Add a binding to the given environment for the symbol and expression."""
    key, val = args
    if isinstance(key, wtypes.Symbol):
        env.add_binding(key, val.eval(env))
        return key
    else:
        raise exceptions.type_error(wtypes.Symbol, key)


@arity(2)
def w_lambda(args: typing.List[wtypes.Expression],
             env: wisp.env.Environment) -> wtypes.Function:
    """Create a lambda given an argument list and a body."""
    arg_def, body = args
    if isinstance(arg_def, wtypes.List):
        if all(isinstance(arg, wtypes.Symbol) for arg in arg_def.items):
            if isinstance(body, wtypes.List):
                # mypy isn't smart enough to understand the
                # all(isinstance()) call above.
                return make_lamba(arg_def.items, body)  # type: ignore
    raise exceptions.WispException('invalid lambda %s %s' % (arg_def, body))


def make_lamba(arg_def: typing.List[wtypes.Symbol],
               body: wtypes.List) -> wtypes.Function:
    """Create a lambda for the argument list and body."""
    @arity(len(arg_def))
    def func(args: typing.List[wtypes.Expression],
             env: wisp.env.Environment) -> wtypes.Expression:
        """Bind arguments to a new frame and evaluate the body.

        This is the function which is actually called when the lambda
        is evaluated. It creates a new stack frame, evaluates the
        arguments passed, binds them according to the parameter list
        and then evaluates the body in that frame.
        """
        vals = [arg.eval(env) for arg in args]

        env.add_frame()
        for symbol, val in zip(arg_def, vals):
            env.add_binding(symbol, val)
        ret = body.eval(env)
        env.pop_frame()

        return ret

    return wtypes.Function(func)


def __list_op(op: typing.Callable[[wtypes.List], T],
              args: typing.List[wtypes.Expression]) -> T:
    """Ensure args is a non-empty List and return the call of op on it."""
    val = args[0]
    if isinstance(val, wtypes.List):
        if val.items:
            return op(val)
        else:
            raise exceptions.WispException(
                'can not apply cdr to an empty list'
            )
    else:
        raise exceptions.type_error(wtypes.List, val)


def __wrap_operator(op,
                    args: typing.List[wtypes.Expression]) -> wtypes.Expression:
    """Reduce the given operator over the given args. Return 0 for no args."""
    if not args:
        return wtypes.Integer(0)
    else:
        return functools.reduce(op, args)


def env() -> wisp.env.Environment:
    """Build an environment with wisp builtin functions defined."""
    return wisp.env.Environment({
        '+': wtypes.Function(add),
        '-': wtypes.Function(sub),
        '*': wtypes.Function(mul),
        '/': wtypes.Function(div),
        'eq?': wtypes.Function(is_equal),
        'quote': wtypes.SpecialForm(quote),
        'cons': wtypes.Function(cons),
        'car': wtypes.Function(car),
        'cdr': wtypes.Function(cdr),
        'atom?': wtypes.Function(is_atom),
        'define': wtypes.SpecialForm(define),
        'lambda': wtypes.SpecialForm(w_lambda),
    })
