#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def reset_defaults(function):
    import six
    from copy import deepcopy

    defaults = six.get_function_defaults(function)

    def decorator(*args, **kwargs):
        if six.PY3: function.__defaults__ = deepcopy(defaults)
        else: function.func_defaults = deepcopy(defaults)
        return function(*args, **kwargs)


    decorator.__name__ = function.__name__
    decorator.__doc__ = function.__doc__

    return decorator

if __name__ == '__main__':

    @reset_defaults
    def dont_increment(value, list=[]):
        list.append(value)
        print(list)

    dont_increment(1)
    dont_increment(2)
    dont_increment(3, [1, 2])


