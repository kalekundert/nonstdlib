#!/usr/bin/env python3

class MagicFormatter:

    def __init__(self, args=None, kwargs=None, level=1):
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.level = level

    def __call__(self, *args, **kwargs):
        return self.__class__(args, kwargs, self.level)

    def __ror__(self, operand):
        import inspect

        # Make sure the operand is a string.
        if not isinstance(operand, str):
            raise TypeError("'{}' is not a string", repr(operand))

        # Inspect variables from the source frame.
        frame = inspect.stack()[self.level][0]

        # Collect all the variables in the scope of the calling code, so they 
        # can be substituted into the message.
        kwargs = {}
        kwargs.update(frame.f_globals)
        kwargs.update(frame.f_locals)
        kwargs.update(self.kwargs)

        return operand.format(*self.args, **kwargs)



fmt = MagicFormatter()

