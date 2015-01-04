#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# This module provides a function that prints out the file, function, and line 
# number that it was called from.  This is useful for debugging messages, which 
# can sometimes be hard to find once the bug has been fixed.

import inspect, logging
from pprint import pprint

logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s')

def get_logger(frame_depth=1):
    try:
        frame = inspect.stack()[frame_depth][0]
        function = inspect.getframeinfo(frame).function
        module = frame.f_globals['__name__']
        self = frame.f_locals.get('self', None)
        location = str(self.__class__) if self else module
        if function != '<module>': location += '.' + function

    finally:
        del frame

    return logging.getLogger(location)

def set_log_level(lvl):
    if isinstance(lvl, str): lvl = getattr(logging, str)
    logging.getLogger().setLevel(lvl)

def log(lvl, msg, *args, **kwargs):
    get_logger(2).log(lvl, msg.format(*args, **kwargs))

def debug(msg, *args, **kwargs):
    get_logger(2).debug(msg.format(*args, **kwargs))

def info(msg, *args, **kwargs):
    get_logger(2).info(msg.format(*args, **kwargs))

def warning(msg, *args, **kwargs):
    get_logger(2).warning(msg.format(*args, **kwargs))

def error(msg, *args, **kwargs):
    get_logger(2).error(msg.format(*args, **kwargs))

def exception(msg, *args):
    get_logger(2).exception(msg.format(*args))

def critical(msg, *args, **kwargs):
    get_logger(2).critical(msg.format(*args, **kwargs))


if __name__ == '__main__':
    warning("Module level")

    def foo():
        error("Function level")
        pass

    foo()

    class Bar:
        def __init__(self):
            critical("Method level")

    Bar()
