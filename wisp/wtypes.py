# Avoids circular imports we'd otherwise hit importing just for the types.
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import wisp.env

from dataclasses import dataclass
import operator
import typing

import wisp.exceptions as exceptions


class Expression:
    """An evaluate-able wisp expression."""
    def eval(self, env: wisp.env.Environment) -> 'Expression':
        return self

    def __add__(self, other: 'Expression') -> 'Expression':
        raise exceptions.WispException('Can not add %s' % self)

    def __sub__(self, other: 'Expression') -> 'Expression':
        raise exceptions.WispException('Can not subtract %s' % self)

    def __mul__(self, other: 'Expression') -> 'Expression':
        raise exceptions.WispException('Can not multiply %s' % self)

    def __floordiv__(self, other: 'Expression') -> 'Expression':
        raise exceptions.WispException('Can not divide %s' % self)


Callable = typing.Callable[
    [typing.List[Expression], 'wisp.env.Environment'], Expression
]


@dataclass
class String(Expression):
    """A wisp string."""
    val: str


@dataclass
class Integer(Expression):
    """A wisp integer."""
    val: int

    def __add__(self, other: Expression) -> Expression:
        return self.__wrap_operator(other, 'add', operator.add)

    def __sub__(self, other: Expression) -> Expression:
        return self.__wrap_operator(other, 'subtract', operator.sub)

    def __mul__(self, other: Expression) -> Expression:
        return self.__wrap_operator(other, 'multiply', operator.mul)

    def __floordiv__(self, other: Expression) -> Expression:
        return self.__wrap_operator(other, 'divide', operator.floordiv)

    def __wrap_operator(self,
                        other: Expression,
                        op_name: str,
                        op: typing.Callable[[int, int], int]) -> Expression:
        """Call the given operator between self and other.

        Calls the given operator between the underlying integers boxed by self
        and other. Wraps the resulting value back in the Integer class.
        Raises an exception if other not an Integer.
        """
        if not isinstance(other, self.__class__):
            raise exceptions.WispException('Can not %s %s' % (op_name, other))
        else:
            return self.__class__(op(self.val, other.val))


@dataclass
class Bool(Expression):
    """A wisp boolean."""
    val: bool


@dataclass
class Function(Expression):
    """A wisp function.

    Implemented as a python function which accepts a list of Expressions
    as arguments and returns an Expression.
    """
    func: Callable

    def call(self,
             args: typing.List[Expression],
             env: wisp.env.Environment) -> Expression:
        """Evaluate the given args and call the function with them."""
        args = [arg.eval(env) for arg in args]
        # mypy gets confused and thinks this is a method call.
        return self.func(args, env)  # type: ignore


@dataclass
class SpecialForm(Expression):
    """A wisp function with special evaluation rules.

    Similar to Function, but expressions in the arguments list are not
    evaluated before the function is called.
    """
    func: Callable

    def call(self,
             args: typing.List[Expression],
             env: wisp.env.Environment) -> Expression:
        """Call the function with the un-evaluated arguments list."""
        # mypy gets confused and thinks this is a method call.
        return self.func(args, env)  # type: ignore


@dataclass
class List(Expression):
    """A wisp list of expressions."""
    items: typing.List[Expression]

    def eval(self, env: wisp.env.Environment) -> Expression:
        """Evaluate a list as a postfix function call.

        Treat the last item in the list as a symbol pointing to a function.
        Treat other members of the list as arguments to the function.
        An empty list evaluates to an empty list.
        """
        if not self.items:
            return self

        fn = self.items[-1].eval(env)
        if not isinstance(fn, (Function, SpecialForm)):
            raise exceptions.WispException(
                '%s is not applicable' % self.items[-1]
            )

        args = list(reversed(self.items[:-1]))
        return fn.call(args, env)


@dataclass
class Symbol(Expression):
    """A wisp symbol."""
    name: str

    def eval(self, env: wisp.env.Environment) -> Expression:
        """Evaluate a symbol by looking up its value in the environment."""
        return env[self]
