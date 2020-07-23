from dataclasses import dataclass
import typing


class Expression:
    """A wisp expression."""
    pass


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
class List(Expression):
    """A wisp list of expressions."""
    lst: typing.List[Expression]


@dataclass
class Symbol(Expression):
    """A wisp symbol."""
    name: str
