#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# This module defines a class which can be used to temporarily suppress stdout 
# and stderr, using the natural 'with-statement' syntax.  Anything written to 
# either file descriptor while it is being muffled can be accessed as a string.

import sys

class Muffler(object):

    class File:

        def __init__(self):
            self.string = ""

        def __str__(self):
            return self.string

        def write(self, string):
            self.string += string

        def flush(self):
            pass


    def __init__(self, **files):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.files = {
                'stdout' : files['stdout'] if 'stdout' in files else True,
                'stderr' : files['stderr'] if 'stderr' in files else True }

        self.file = Muffler.File()

    def __str__(self):
        return str(self.file)

    def __enter__(self):
        if self.files['stdout']:
            sys.stdout = self.file
            
        if self.files['stderr']:
            sys.stderr = self.file

        return self

    def __exit__(self, *ignore):
        sys.stdout = self.stdout
        sys.stderr = self.stderr


if __name__ == '__main__':

    muffler = Muffler()
    greeting = "Hello world!"

    with muffler:
        print(greeting)

    assert str(muffler) == greeting + '\n'
    print("All tests passed!")

