#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def memoize(function):
    previous_results = {}

    def decorator(*args):
        try:
            return previous_results[args]
        except KeyError:
            previous_results[args] = function(*args)
            return previous_results[args]


    decorator.__name__ = function.__name__
    decorator.__doc__ = function.__doc__

    return decorator

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

def singleton(cls):
    """ Decorator function that turns a class into a singleton. """
    import inspect

    # Create a structure to store instances of any singletons that get
    # created.
    instances = {}

    # Make sure that the constructor for this class doesn't take any
    # arguments.  Since singletons can only be instantiated once, it doesn't
    # make any sense for the constructor to take arguments.  If the class 
    # doesn't implement its own constructor, don't do anything.  This case is 
    # considered specially because it causes a TypeError in python 3.3 but not 
    # in python 3.4.
    if cls.__init__ is not object.__init__:
        argspec = inspect.getfullargspec(cls.__init__)
        if len(argspec.args) != 1 or argspec.varargs or argspec.varkw:
            raise TypeError("Singleton classes cannot accept arguments to the constructor.")


    def get_instance():
        """ Creates and returns the singleton object.  This function is what 
        gets returned by this decorator. """

        # Check to see if an instance of this class has already been
        # instantiated.  If it hasn't, create one.  The `instances` structure
        # is technically a global variable, so it will be preserved between
        # calls to this function.
        if cls not in instances:
            instances[cls] = cls()

        # Return a previously instantiated object of the requested type.
        return instances[cls]

    # Return the decorator function.
    return get_instance





