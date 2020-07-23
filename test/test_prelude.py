"""Tests for prelude functions."""

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
