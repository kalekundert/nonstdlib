#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging
import contextlib

def log_level(level):
    """
    Attempt to convert the given argument into a log level.

    Log levels are represented as integers, where higher values are more 
    severe.  If the given level is already an integer, it is simply returned.  
    If the given level is a string that can be converted into an integer, it is 
    converted and that value is returned.  Finally, if the given level is a 
    string naming one of the levels defined in the logging module, return that 
    level.  If none of those conditions are met, raise a ValueError.
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

def config(stream=sys.stderr,
           level=logging.NOTSET,
           format='%(levelname)s [%(name)s:%(lineno)s] %(message)s',
           file=None,
           file_level=None,
           file_format=None):
    """
    Configure logging to stream and file concurrently.

    Allows setting a file and stream to log to concurrently with differing 
    level if desired.  Must provide either stream or file.

    Parameters
    ----------
    stream: File like:
        Stream to write file to [Default: sys.stderr]. If none, will not write 
        to stream.

    level: str|int
        Log level. Allowable levels are those recognized by the logging module.

    format: str
        Format string for the emitted logs. Default: 'log_level [logger_name] 
        message'

    file: str
        Path to write log to file. If None, will not log to file.

    file_level: str|int|None
        Overwrite log level for the file. Will default to `level` if None.

    file_format: str|None
        Overwrite format of logs for file. Will default to `format` if None.
    """
    # It doesn't make sense to configure a logger with no handlers.
    assert file is not None or stream is not None

    # Set the formats.
    stream_format = format
    if file_format is None:
        file_format = stream_format

    # Get the log levels
    stream_level = log_level(level)
    if file_level is None:
        file_level = stream_level
    else:
        file_level = log_level(file_level)

    # Everything falls to pieces if I don't use basicConfig.
    if stream is not None:
        logging.basicConfig(stream=stream,
                            level=stream_level,
                            format=stream_format)
        # Configure file
        if file is not None:
            file = logging.FileHandler(filename=file)
            file.setLevel(file_level)
            file.setFormatter(logging.Formatter(file_format))
            logging.getLogger().addHandler(file)
    elif file is not None:
        logging.basicConfig(filename=file,
                            level=file_level,
                            format=file_format)


def log(level, message, **kwargs):
    _log(level, message, **kwargs)

def debug(message, **kwargs):
    _log(logging.DEBUG, message, **kwargs)

def info(message, **kwargs):
    _log(logging.INFO, message, **kwargs)

def warn(message, **kwargs):
    _log(logging.WARNING, message, **kwargs)

def warning(message, **kwargs):
    _log(logging.WARNING, message, **kwargs)

def error(message, **kwargs):
    _log(logging.ERROR, message, **kwargs)

def critical(message, **kwargs):
    _log(logging.CRITICAL, message, **kwargs)

def fatal(message, **kwargs):
    _log(logging.FATAL, message, **kwargs)


def _log(level, message, frame_depth=2, **kwargs):
    """
    Log the given message with the given log level using a logger named based 
    on the scope of the calling code.  This saves you time because you will be 
    able to see where all your log messages are being generated from without 
    having to type anything.  This function is meant to be called by one or 
    more wrapper functions, so the `frame_depth` argument is provided to 
    specify which scope should be used to name the logger.
    """
    import inspect

    try:
        # Inspect variables two frames up from where we currently are (by 
        # default).  One frame up is assumed to be one of the helper methods 
        # defined in this module, so we aren't interested in that.  Two frames 
        # up should be the frame that's actually trying to log something.

        frame = inspect.stack()[frame_depth][0]
        frame_below = inspect.stack()[frame_depth-1][0]
        
        # Collect all the variables in the scope of the calling code, so they 
        # can be substituted into the message.

        scope = {}
        scope.update(frame.f_globals)
        scope.update(frame.f_locals)

        # If the calling frame is inside a class (deduced based on the presence 
        # of a 'self' variable), name the logger after that class.  Otherwise 
        # if the calling frame is inside a function, name the logger after that 
        # function.  Otherwise name it after the module of the calling scope.

        self = frame.f_locals.get('self')
        function = inspect.getframeinfo(frame).function
        module = frame.f_globals['__name__']

        if self is not None:
            name = '.'.join([
                    self.__class__.__module__,
                    self.__class__.__name__
            ])

        elif function != '<module>':
            name = '.'.join([module, function])

        else:
            name = module

        # Trick the logging module into reading file names and line numbers 
        # from the correct frame by monkey-patching logging.currentframe() with 
        # a function that returns the frame below the real calling frame (this 
        # indirection is necessary because the logging module will look one 
        # frame above whatever this function returns).  Undo all this after 
        # logging our message, to avoid interfering with other loggers.

        with _temporarily_set_logging_frame(frame_below):
            logger = logging.getLogger(name)
            logger.log(level, message.format(**scope), **kwargs)

    finally:
        try: del frame
        except UnboundLocalError: pass

@contextlib.contextmanager
def _temporarily_set_logging_frame(frame):
    try:
        stdlib_currentframe = logging.currentframe
        logging.currentframe = lambda: frame
        yield
    finally:
        logging.currentframe = stdlib_currentframe


