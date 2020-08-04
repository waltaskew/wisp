"""Tests for the env module."""
import pytest  # type: ignore

import wisp.exceptions as exceptions
import wisp.env
import wisp.wtypes as wtypes


def test_pop_and_add():
    """Ensure we can add and pop frames to the environment."""
    env = wisp.env.Environment()
    env.add_frame({'a': wtypes.String('apple')})
    env.add_frame({'b': wtypes.String('banana')})
    env.add_frame({'c': wtypes.String('carrot')})

    assert env.pop_frame() == {'c': wtypes.String('carrot')}
    assert env.pop_frame() == {'b': wtypes.String('banana')}
    assert env.pop_frame() == {'a': wtypes.String('apple')}


def test_get_add_binding():
    """Ensure we get the binding from the top frame."""
    env = wisp.env.Environment()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('apple'))

    env.add_frame()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('aardvark'))

    env.add_frame()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('adorno'))

    assert env[wtypes.Symbol('a')] == wtypes.String('adorno')

    env.pop_frame()
    assert env[wtypes.Symbol('a')] == wtypes.String('aardvark')

    env.pop_frame()
    assert env[wtypes.Symbol('a')] == wtypes.String('apple')


def test_get_nearest():
    """Ensure we get bindings past the top frame."""
    env = wisp.env.Environment()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('apple'))
    env.add_frame()
    env.add_frame()

    assert env[wtypes.Symbol('a')] == wtypes.String('apple')


def test_get_missing():
    """Ensure we raise an exception for missing bindings."""
    env = wisp.env.Environment()
    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('a')]


def test_set_bindings():
    """Ensure we set bindings in the current frame."""
    env = wisp.env.Environment()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('apple'))

    env.add_frame()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('aardvark'))

    env[wtypes.Symbol('a')] = wtypes.String('adorno')

    assert env[wtypes.Symbol('a')] == wtypes.String('adorno')

    env.pop_frame()
    assert env[wtypes.Symbol('a')] == wtypes.String('apple')


def test_set_missing():
    """Ensure we raise an exception for missing bindings."""
    env = wisp.env.Environment()
    with pytest.raises(exceptions.WispException):
        env[wtypes.Symbol('a')] = wtypes.String('apple')


def test_local_global_scope():
    """Ensure we return the local and global scope properly."""
    env = wisp.env.Environment()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('apple'))

    env.add_frame()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('aardvark'))

    env.add_frame()
    env.add_binding(wtypes.Symbol('a'), wtypes.String('adorno'))

    assert env.global_scope() == {'a': wtypes.String('apple')}
    assert env.local_scope() == {'a': wtypes.String('adorno')}

    env.pop_frame()
    assert env.global_scope() == {'a': wtypes.String('apple')}
    assert env.local_scope() == {'a': wtypes.String('aardvark')}

    env.pop_frame()
    assert env.global_scope() == {'a': wtypes.String('apple')}
    assert env.local_scope() == {}
