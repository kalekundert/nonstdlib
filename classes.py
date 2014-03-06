from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def singleton(cls):
    """ Decorator function that turns a class into a singleton. """
    import inspect

    # Create a structure to store instances of any singletons that get
    # created.
    instances = {}

    # Make sure that the constructor for this class doesn't take any
    # arguments.  Since singletons can only be instantiated once, it doesn't
    # make any sense for the constructor to take arguments.
    try:
        specification = inspect.getargspec(cls.__init__)
        positional, variable, keyword, default = specification

    # If the class doesn't have a constructor, that's ok.
    except TypeError:
        pass

    # Otherwise, make sure the constructor has only a self argument.
    else:
        message = "Singleton classes cannot accept arguments to the constructor."

        if len(positional) is not 1:
            raise TypeError(message)
        if (variable is not None) or (keyword is not None):
            raise TypeError(message)

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


if __name__ == "__main__":

    # This is the simplest possible singleton class, and it should work
    # without issue.
    
    @singleton
    class Simple:
        pass


    assert Simple() is Simple()

    # This should fail, because singleton constructors are not allowed to take
    # any arguments.

    try:
        @singleton
        class Broken:
            def __init__(self, illegal):
                pass

    except TypeError:
        pass
    else:
        raise AssertionError

    print("All tests passed.")


