"""Tests for prelude functions."""

import wisp.prelude as prelude
import wisp.wtypes as wtypes


def test_add():
    """Ensure add maths properly."""
    prelude.add([wtypes.Integer(1), wtypes.Integer(2)]) == wtypes.Integer(3)


def test_sub():
    """Ensure sub maths properly."""
    prelude.sub([wtypes.Integer(3), wtypes.Integer(1)]) == wtypes.Integer(2)


def test_mul():
    """Ensure mul maths properly."""
    prelude.sub([wtypes.Integer(3), wtypes.Integer(2)]) == wtypes.Integer(6)


def test_div():
    """Ensure div maths properly."""
    prelude.sub([wtypes.Integer(4), wtypes.Integer(2)]) == wtypes.Integer(2)


def test_equal():
    """Ensure equal tests equality properly."""
    assert (prelude.equal([wtypes.Integer(4), wtypes.Integer(4)]) ==
            wtypes.Bool(True))
    assert (prelude.equal([wtypes.Integer(4), wtypes.Integer(3)]) ==
            wtypes.Bool(False))
    assert (prelude.equal([wtypes.String('abc'), wtypes.Integer(3)]) ==
            wtypes.Bool(False))
