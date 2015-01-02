#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# This module provides a function that prints out the file, function, and line 
# number that it was called from.  This is useful for debugging messages, which 
# can sometimes be hard to find once the bug has been fixed.

import inspect

def mark(message=""):
    frame = inspect.stack()[1][0]
    info = inspect.getframeinfo(frame)
    loc = 'File "{0.filename}", line {0.lineno}, in {0.function}'.format(info)
    if message: print(loc + ': ' + message)
    else: print(loc)


if __name__ == '__main__':

    mark()

    def foo():
        mark("Hello world")

    foo()

    class Bar:
        def __init__(self):
            mark("Hello world")

    Bar()
