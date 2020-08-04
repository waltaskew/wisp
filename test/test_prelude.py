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


def test_begin():
    """Ensure begin return the last expression."""
    env = prelude.env()
    call = wtypes.List([
        wtypes.List([
            wtypes.Integer(1),
            wtypes.Integer(2),
            wtypes.Symbol('+'),
        ]),
        wtypes.List([
            wtypes.Integer(1),
            wtypes.Integer(1),
            wtypes.Symbol('+'),
        ]),
        wtypes.Symbol('begin')
    ])
    assert call.eval(env) == wtypes.Integer(3)


def test_set():
    """Ensure set mutates bindings."""
    env = prelude.env()

    # ensure we can't set non-existent bindings
    bad_call = wtypes.List([
        wtypes.Integer(1),
        wtypes.Symbol('x'),
        wtypes.Symbol('set!')
    ])
    with pytest.raises(exceptions.WispException):
        assert bad_call.eval(env)

    # ensure we can set previously-existent bindings
    define_call = wtypes.List([
        wtypes.Integer(1),
        wtypes.Symbol('x'),
        wtypes.Symbol('define')
    ])
    define_call.eval(env)
    assert wtypes.Symbol('x').eval(env) == wtypes.Integer(1)

    set_call = wtypes.List([
        wtypes.Integer(2),
        wtypes.Symbol('x'),
        wtypes.Symbol('set!')
    ])
    set_call.eval(env)
    assert wtypes.Symbol('x').eval(env) == wtypes.Integer(2)


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


def test_recursion():
    """Ensure we can handle simple recursion."""
    env = prelude.env()
    fib_def = wtypes.List([
        wtypes.List([
            wtypes.List([
                wtypes.List([
                    wtypes.List([
                        wtypes.List([
                            wtypes.List([
                                wtypes.Integer(2),
                                wtypes.Symbol('n'),
                                wtypes.Symbol('-')
                            ]),
                            wtypes.Symbol('fib')
                        ]),
                        wtypes.List([
                            wtypes.List([
                                wtypes.Integer(1),
                                wtypes.Symbol('n'),
                                wtypes.Symbol('-')
                            ]),
                            wtypes.Symbol('fib')
                        ]),
                        wtypes.Symbol('+')
                    ]),
                    wtypes.Symbol('else')
                ]),
                wtypes.List([
                    wtypes.Integer(1),
                    wtypes.List([
                        wtypes.Integer(1),
                        wtypes.Symbol('n'),
                        wtypes.Symbol('eq?')
                    ])
                ]),
                wtypes.List([
                    wtypes.Integer(0),
                    wtypes.List([
                        wtypes.Integer(0),
                        wtypes.Symbol('n'),
                        wtypes.Symbol('eq?')
                    ])
                ]),
                wtypes.Symbol('cond')
            ]),
            wtypes.List([
                wtypes.Symbol('n')
            ]),
            wtypes.Symbol('lambda')
        ]),
        wtypes.Symbol('fib'),
        wtypes.Symbol('define'),
    ])
    fib_def.eval(env)

    call = wtypes.List([wtypes.Integer(0), wtypes.Symbol('fib')])
    assert call.eval(env) == wtypes.Integer(0)

    call = wtypes.List([wtypes.Integer(1), wtypes.Symbol('fib')])
    assert call.eval(env) == wtypes.Integer(1)

    call = wtypes.List([wtypes.Integer(5), wtypes.Symbol('fib')])
    assert call.eval(env) == wtypes.Integer(5)

    call = wtypes.List([wtypes.Integer(6), wtypes.Symbol('fib')])
    assert call.eval(env) == wtypes.Integer(8)

    call = wtypes.List([wtypes.Integer(7), wtypes.Symbol('fib')])
    assert call.eval(env) == wtypes.Integer(13)


def test_closures():
    """Ensure we handle closures properly."""
    env = prelude.env()
    counter_def = wtypes.List([
        wtypes.List([
            wtypes.List([
                wtypes.List([
                    wtypes.Symbol('x'),
                    wtypes.List([
                        wtypes.List([
                            wtypes.Integer(1),
                            wtypes.Symbol('x'),
                            wtypes.Symbol('+')
                        ]),
                        wtypes.Symbol('x'),
                        wtypes.Symbol('set!')
                    ]),
                    wtypes.Symbol('begin')
                ]),
                wtypes.List([]),
                wtypes.Symbol('lambda')
            ]),
            wtypes.List([
                wtypes.Symbol('x')
            ]),
            wtypes.Symbol('lambda')
        ]),
        wtypes.Symbol('make-counter'),
        wtypes.Symbol('define'),
    ])
    counter_def.eval(env)

    counter = wtypes.List([
        wtypes.List([
            wtypes.Integer(0),
            wtypes.Symbol('make-counter')
        ]),
        wtypes.Symbol('c'),
        wtypes.Symbol('define'),
    ])
    counter.eval(env)

    call = wtypes.List([wtypes.Symbol('c')])

    assert call.eval(env) == wtypes.Integer(1)
    assert call.eval(env) == wtypes.Integer(2)
    assert call.eval(env) == wtypes.Integer(3)

    # ensure 'x' from the closure hasn't leaked into the global scope.
    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('x')]


def quoted_list(elems):
    """Build a quoted list consisting of the given elements, safe from eval."""
    return wtypes.List([
        wtypes.List(elems),
        wtypes.Symbol('quote')
    ])
