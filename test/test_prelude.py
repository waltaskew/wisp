"""Tests for prelude functions."""

import pytest

import wisp.prelude as prelude
import wisp.wtypes as wtypes


def test_add():
    """Ensure add maths properly."""
    res = prelude.env()['+'].call(
        [wtypes.Integer(1), wtypes.Integer(2)], {}
    )
    assert res == wtypes.Integer(3)


def test_sub():
    """Ensure sub maths properly."""
    res = prelude.env()['-'].call(
        [wtypes.Integer(3), wtypes.Integer(1)], {}
    )
    assert res == wtypes.Integer(2)


def test_mul():
    """Ensure mul maths properly."""
    res = prelude.env()['*'].call(
        [wtypes.Integer(3), wtypes.Integer(2)], {}
    )
    assert res == wtypes.Integer(6)


def test_div():
    """Ensure div maths properly."""
    res = prelude.env()['/'].call(
        [wtypes.Integer(4), wtypes.Integer(2)], {}
    )
    assert res == wtypes.Integer(2)


def test_equal():
    """Ensure equal tests equality properly."""
    assert prelude.env()['eq?'].call(
        [wtypes.Integer(4), wtypes.Integer(4)], {}
    ) == wtypes.Bool(True)

    assert prelude.env()['eq?'].call(
        [wtypes.Integer(4), wtypes.Integer(2)], {}
    ) == wtypes.Bool(False)

    assert prelude.env()['eq?'].call(
        [wtypes.Integer(4), wtypes.String('abc')], {}
    ) == wtypes.Bool(False)


def test_quote():
    """Ensure quote does nothing."""
    assert prelude.env()['quote'].call(
        [wtypes.Symbol('abc')], {}
    ) == wtypes.Symbol('abc')


def test_cons():
    """Ensure cons sticks things together."""
    env = prelude.env()
    res = env['cons'].call([
        wtypes.Integer(1),
        quoted_list([wtypes.Integer(2), wtypes.Integer(3)])
    ], env)
    assert res == wtypes.List([
        wtypes.Integer(1), wtypes.Integer(2), wtypes.Integer(3)
    ])


def test_car():
    """Ensure car takes the head."""
    env = prelude.env()
    res = env['car'].call([
        quoted_list([wtypes.Integer(1), wtypes.Integer(2), wtypes.Integer(3)])
    ], env)
    assert res == wtypes.Integer(1)


def test_cdr():
    """Ensure cdr takes the rest."""
    env = prelude.env()
    res = env['cdr'].call([
        quoted_list([wtypes.Integer(1), wtypes.Integer(2), wtypes.Integer(3)])
    ], env)
    assert res == wtypes.List([
        wtypes.Integer(2), wtypes.Integer(3)
    ])


def test_empty_car_and_cdr():
    """Ensure car and cdr raise an error on empty lists."""
    env = prelude.env()

    with pytest.raises(wtypes.WispException):
        env['car'].call([quoted_list([])], env)

    with pytest.raises(wtypes.WispException):
        env['cdr'].call([quoted_list([])], env)


def quoted_list(elems):
    """Build a quoted list consisting of the given elements, safe from eval."""
    return wtypes.List([
        wtypes.List(elems),
        wtypes.Symbol('quote')
    ])
