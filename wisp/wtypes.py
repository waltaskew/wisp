from dataclasses import dataclass
import typing


class WispException(Exception):
    """A base exception to distinguish user errors issued by wisp."""
    pass


class Expression:
    """An evaluate-able wisp expression."""
    def eval(self, env: typing.Dict[str, 'Expression']) -> 'Expression':
        return self


Environment = typing.Dict[str, Expression]


@dataclass
class String(Expression):
    """A wisp string."""
    val: str


@dataclass
class Integer(Expression):
    """A wisp integer."""
    val: int


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
    func: typing.Callable[[typing.List[Expression]], Expression]


@dataclass
class List(Expression):
    """A wisp list of expressions."""
    lst: typing.List[Expression]

    def eval(self, env: Environment) -> Expression:
        """Evaluate a list as a postfix function call.

        Treat the last item in the list as a symbol pointing to a function.
        Treat other members of the list as arguments to the function.
        An empty list evaluates to an empty list.
        """
        if not self.lst:
            return self

        fn = self.lst[-1].eval(env)
        if not isinstance(fn, Function):
            raise WispException('%s is not a function' % self.lst[-1])

        args = [arg.eval(env) for arg in self.lst[:-1]]
        args.reverse()
        # mypy gets confused and thinks this is a method call.
        return fn.func(args)  # type: ignore


@dataclass
class Symbol(Expression):
    """A wisp symbol."""
    name: str

    def eval(self, env: Environment) -> Expression:
        """Evaluate a symbol by looking up its value in the environment."""
        val = env.get(self.name)
        if val is not None:
            return val
        else:
            raise WispException('No binding for %s' % self)
