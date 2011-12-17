#!/usr/bin/env python

import sys

class Muffler(object):

    # Dummy File {{{1
    class File:

        def __init__(self):
            self.string = ""

        def __str__(self):
            return self.string

        def write(self, string):
            self.string += string

    # }}}1

    # Constructor {{{1
    def __init__(self, **files):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.files = {
                "stdout" : files["stdout"] if "stdout" in files else True,
                "stderr" : files["stderr"] if "stderr" in files else True }

        self.file = Muffler.File()

    # String Operator {{{1
    def __str__(self):
        return str(self.file)

    # "With" Operators {{{1
    def __enter__(self):
        if self.files["stdout"]:
            sys.stdout = self.file
            
        if self.files["stderr"]:
            sys.stderr = self.file

        return self

    def __exit__(self, *ignore):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    # }}}1

if __name__ == "__main__":

    muffler = Muffler()
    greeting = "Hello world!"

    with muffler:
        print greeting

    assert str(muffler) == greeting + '\n'
    print "All tests passed!"

