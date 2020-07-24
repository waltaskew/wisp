import collections
import typing

import wisp.exceptions as exceptions
import wisp.wtypes as wtypes


class Environment:
    """An environment of wisp bindings in which expressions are evaluated.

    The environment maps symbol names to wisp expressions. It consists of
    multiple frames which are searched in order for bindings. New frames
    may be used to build call stacks such that functions have their own
    local scope frames to mess about it.
    """
    frames: typing.Deque[typing.Dict[str, wtypes.Expression]]

    def __init__(self,
                 frame: typing.Optional[
                     typing.Dict[str, wtypes.Expression]] = None):
        self.frames = collections.deque([frame or {}])

    def add_frame(self,
                  env: typing.Optional[
                      typing.Dict[str, wtypes.Expression]] = None):
        """Add a new frame to the environment. Defaults to an empty frame."""
        self.frames.appendleft(env or {})

    def pop_frame(self) -> typing.Dict[str, wtypes.Expression]:
        """Remove the current frame from the environment."""
        return self.frames.popleft()

    def __getitem__(self, key: wtypes.Symbol) -> wtypes.Expression:
        """Search each frame in the environment for the symbol.

        Raises an exception if the symbol can not be found in any frame.
        """
        for frame in self.frames:
            if key.name in frame:
                return frame[key.name]
        else:
            raise exceptions.WispException('No binding for %s' % key)

    def add_binding(self, key: wtypes.Symbol, val: wtypes.Expression):
        """Bind the symbol to the given value in the current frame."""
        self.frames[0][key.name] = val

    def __setitem__(self, key: wtypes.Symbol, val: wtypes.Expression):
        """Set a symbol's value in whichever frame it is first bound.

        Raises an exception if the symbol is not yet bound.
        """
        for frame in self.frames:
            if key.name in frame:
                frame[key.name] = val
                break
        else:
            raise exceptions.WispException('No binding for %s' % key)
