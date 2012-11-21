#!/usr/bin/env python

def reset_defaults(function):
    from copy import deepcopy
    defaults = function.func_defaults

    def decorator(*args, **kwargs):
        function.func_defaults = deepcopy(defaults)
        return function(*args, **kwargs)


    decorator.__name__ = function.__name__
    decorator.__doc__ = function.__doc__

    return decorator

if __name__ == '__main__':

    @reset_defaults
    def dont_increment(value, list=[]):
        list.append(value)
        print list

    dont_increment(1)
    dont_increment(2)
    dont_increment(3, [1, 2])


