#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

def log_level(level):
    """
    Attempt to convert the given argument into a log level.

    Log levels are represented as integers, where higher values are more 
    severe.  If the given level is already an integer, it is simply returned.  
    If the given level is a string that can be converted into an integer, it is 
    converted and that value is returned.  Finally, if the given level is a 
    string and there is a variable of the same name in the logging namespace, 
    the value of that variable is returned.
    """
    from six import string_types

    if isinstance(level, int):
        return level

    if isinstance(level, string_types):
        try: return int(level)
        except ValueError: pass

        try: return getattr(logging, level.upper())
        except AttributeError: pass

    raise ValueError("cannot convert '{}' into a log level".format(level))

def verbosity(verbosity):
    """
    Convert the number of times the user specified '-v' on the command-line 
    into a log level.
    """
    verbosity = int(verbosity)

    if verbosity == 0:
        return logging.WARNING
    if verbosity == 1:
        return logging.INFO
    if verbosity == 2:
        return logging.DEBUG
    if verbosity >= 3:
        return 0
    else:
        raise ValueError


def log(level, message, **kwargs):
    _log(level, message, **kwargs)

def debug(message, **kwargs):
    _log(logging.DEBUG, message, **kwargs)

def info(message, **kwargs):
    _log(logging.INFO, message, **kwargs)

def warning(message, **kwargs):
    _log(logging.WARNING, message, **kwargs)

def error(message, **kwargs):
    _log(logging.ERROR, message, **kwargs)

def critical(message, **kwargs):
    _log(logging.CRITICAL, message, **kwargs)


def _log(level, message, frame_depth=2, **kwargs):
    """
    Log the given message to the given level.  This function must be called 
    from within another function, because it is hard-coded to use a frame depth 
    of 2 to pick a name.
    """
    import inspect

    try:
        # Inspect variables two frames where we currently are (by default).  
        # One frame up is assumed to be one of the helper methods defined in 
        # this module, so we aren't interested in that.  Two frames up should 
        # be the frame that's actually trying to log something.

        frame = inspect.stack()[frame_depth][0]
        
        # Collect all the variables in the scope of the calling code, so they 
        # can be substituted into the message.

        scope = {}
        scope.update(frame.f_globals)
        scope.update(frame.f_locals)

        # If the calling frame is inside a class (deduced based on the presense 
        # of a 'self' variable), name the logger after that class.  Otherwise 
        # if the calling frame is inside a function, name the logger after that 
        # function.

        name = frame.f_globals['__name__']
        self = frame.f_locals.get('self')
        function = inspect.getframeinfo(frame).function

        if self is not None:
            name += '.' + self.__class__.__name__

        elif function != '<module>':
            name += '.' + function

    finally:
        try: del frame
        except UnboundLocalError: pass

    logging.getLogger(name).log(level, message.format(**scope), **kwargs)


if __name__ == '__main__':
    logging.basicConfig(
            format='%(levelname)s: %(name)s: %(message)s',
            level=0,
    )

    # Make sure log_level() works.

    log(log_level(1), "Variable level")
    log(log_level("99"), "Variable level")
    log(log_level("info"), "Variable level")

    # Make sure there aren't any stupid typos in the public interface.

    info("Info level")
    debug("Debug level")
    warning("Warning level")
    error("Error level")
    critical("Critical error")

    # Make sure different scopes are properly incorporated into the output.

    info("Module level")

    def foo():  # (no fold)
        info("Function level")
        pass

    foo()

    class Bar:  # (no fold)
        def __init__(self):
            info("Method level")

    Bar()

