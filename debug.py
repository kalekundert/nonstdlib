#!/usr/bin/env python

# This module provides a function that prints out the file, function, and line 
# number that it was called from.  This is useful for debugging messages, which 
# can sometimes be hard to find once the bug has been fixed.

import inspect

def mark(message=""):
    frame = inspect.stack()[1][0]
    info = inspect.getframeinfo(frame)
    print info.filename, info.function, info.lineno

if __name__ == '__main__':

    mark()

    def foo():
        mark()

    foo()
