"""Tests for prelude functions."""

import pytest  # type: ignore

import wisp.exceptions as exceptions
import wisp.prelude as prelude
import wisp.wtypes as wtypes


def test_add():
    """Ensure add maths properly."""
    res = prelude.env()[wtypes.Symbol('+')].call(
        [wtypes.Integer(1), wtypes.Integer(2)], {}
    )
    assert res == wtypes.Integer(3)


def test_sub():
    """Ensure sub maths properly."""
    res = prelude.env()[wtypes.Symbol('-')].call(
        [wtypes.Integer(3), wtypes.Integer(1)], {}
    )
    assert res == wtypes.Integer(2)


def test_mul():
    """Ensure mul maths properly."""
    res = prelude.env()[wtypes.Symbol('*')].call(
        [wtypes.Integer(3), wtypes.Integer(2)], {}
    )
    assert res == wtypes.Integer(6)


def test_div():
    """Ensure div maths properly."""
    res = prelude.env()[wtypes.Symbol('/')].call(
        [wtypes.Integer(4), wtypes.Integer(2)], {}
    )
    assert res == wtypes.Integer(2)


def test_equal():
    """Ensure equal tests equality properly."""
    assert prelude.env()[wtypes.Symbol('eq?')].call(
        [wtypes.Integer(4), wtypes.Integer(4)], {}
    ) == wtypes.Bool(True)

    assert prelude.env()[wtypes.Symbol('eq?')].call(
        [wtypes.Integer(4), wtypes.Integer(2)], {}
    ) == wtypes.Bool(False)

    assert prelude.env()[wtypes.Symbol('eq?')].call(
        [wtypes.Integer(4), wtypes.String('abc')], {}
    ) == wtypes.Bool(False)


def test_quote():
    """Ensure quote does nothing."""
    assert prelude.env()[wtypes.Symbol('quote')].call(
        [wtypes.Symbol('abc')], {}
    ) == wtypes.Symbol('abc')


def test_cons():
    """Ensure cons sticks things together."""
    env = prelude.env()
    res = env[wtypes.Symbol('cons')].call([
        wtypes.Integer(1),
        quoted_list([wtypes.Integer(2), wtypes.Integer(3)])
    ], env)
    assert res == wtypes.List([
        wtypes.Integer(1), wtypes.Integer(2), wtypes.Integer(3)
    ])


def test_car():
    """Ensure car takes the head."""
    env = prelude.env()
    res = env[wtypes.Symbol('car')].call([
        quoted_list([wtypes.Integer(1), wtypes.Integer(2), wtypes.Integer(3)])
    ], env)
    assert res == wtypes.Integer(1)


def test_cdr():
    """Ensure cdr takes the rest."""
    env = prelude.env()
    res = env[wtypes.Symbol('cdr')].call([
        quoted_list([wtypes.Integer(1), wtypes.Integer(2), wtypes.Integer(3)])
    ], env)
    assert res == wtypes.List([
        wtypes.Integer(2), wtypes.Integer(3)
    ])


def test_empty_car_and_cdr():
    """Ensure car and cdr raise an error on empty lists."""
    env = prelude.env()

    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('car')].call([quoted_list([])], env)

    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('cdr')].call([quoted_list([])], env)


def test_atom():
    """Ensure atom indicates atomicity."""
    env = prelude.env()

    assert env[wtypes.Symbol('atom?')].call([
        wtypes.Integer(1)
    ], env) == wtypes.Bool(True)

    assert env[wtypes.Symbol('atom?')].call([
        quoted_list([wtypes.Integer(1)])
    ], env) == wtypes.Bool(False)


def test_define():
    """Ensure define binds values to symbols."""
    env = prelude.env()

    res = env[wtypes.Symbol('define')].call([
        wtypes.Symbol('a'),
        quoted_list([wtypes.String('apple')])
    ], env)
    assert res == wtypes.Symbol('a')
    assert env[wtypes.Symbol('a')] == wtypes.List([wtypes.String('apple')])


def test_lambda():
    """Ensure lambdas can be defined and called."""
    env = prelude.env()

    # define a lambda performing x - y
    sub_lambda = env[wtypes.Symbol('lambda')].call([
        wtypes.List([wtypes.Symbol('x'), wtypes.Symbol('y')]),
        wtypes.List([
            wtypes.Symbol('y'), wtypes.Symbol('x'), wtypes.Symbol('-')
        ]),
    ], env)

    # ensure we can call the above lambda
    call = wtypes.List([wtypes.Integer(1), wtypes.Integer(3), sub_lambda])
    res = call.eval(env)
    assert res == wtypes.Integer(2)

    # ensure we didn't pollute the environment with bindings from the call.
    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('x')]


def test_bad_lambda():
    """Ensure we handle lambdas which raise exceptions."""
    env = prelude.env()

    # define a lambda calling a non-existent symbol
    bad_lambda = env[wtypes.Symbol('lambda')].call([
        wtypes.List([wtypes.Symbol('x')]),
        wtypes.List([wtypes.Symbol('snakes')])
    ], env)

    # raise an exception when we call it
    call = wtypes.List([wtypes.Integer(2), bad_lambda])
    with pytest.raises(exceptions.WispException):
        call.eval(env)

    # ensure we didn't pollute even though the call raised an exception
    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('x')]


def test_cond():
    """Ensure we evaluate cond properly."""
    env = prelude.env()
    call = wtypes.List([
        wtypes.List([
            wtypes.String('two'),
            wtypes.List([
                wtypes.Integer(2), wtypes.Integer(2), wtypes.Symbol('eq?')
            ])
        ]),
        wtypes.List([
            wtypes.String('one'),
            wtypes.List([
                wtypes.Integer(1), wtypes.Integer(1), wtypes.Symbol('eq?')
            ])
        ]),
        wtypes.List([
            wtypes.String('not-one'),
            wtypes.List([
                wtypes.Integer(2), wtypes.Integer(1), wtypes.Symbol('eq?')
            ])
        ]),
        wtypes.Symbol('cond')
    ])
    result = call.eval(env)
    assert result == wtypes.String('one')


def test_cond_with_else():
    """Ensure we handle else expressions."""
    env = prelude.env()
    call = wtypes.List([
        wtypes.List([
            wtypes.String('else-case'),
            wtypes.Symbol('else')
        ]),
        wtypes.List([
            wtypes.String('not-two'),
            wtypes.List([
                wtypes.Integer(3), wtypes.Integer(2), wtypes.Symbol('eq?')
            ])
        ]),
        wtypes.List([
            wtypes.String('not-one'),
            wtypes.List([
                wtypes.Integer(2), wtypes.Integer(1), wtypes.Symbol('eq?')
            ])
        ]),
        wtypes.Symbol('cond')
    ])
    result = call.eval(env)
    assert result == wtypes.String('else-case')


def quoted_list(elems):
    """Build a quoted list consisting of the given elements, safe from eval."""
    return wtypes.List([
        wtypes.List(elems),
        wtypes.Symbol('quote')
    ])
