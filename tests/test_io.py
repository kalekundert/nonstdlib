#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import nonstdlib

def test_capture_output():
    import sys

    with nonstdlib.capture_output() as output:
        print('std', end='', file=sys.stdout)
        print('st', end='', file=sys.stderr)
        print('out', file=sys.stdout)
        print('derr', file=sys.stderr)

    assert 'stdout' in output
    assert 'stderr' in output
    assert output.stdout == 'stdout\n'
    assert output.stderr == 'stderr\n'

def test_muffle():
    with nonstdlib.muffle():
        print("""\
This test doesn't really test anything, it just makes sure the 
muffle function returns without raising any exceptions.  You shouldn't ever see 
this message.""")
