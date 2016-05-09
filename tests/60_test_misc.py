#!/usr/bin/env python3

from nonstdlib import *

def test_span():
    assert list(span(0, 1, 6)) == approx([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    assert list(span(0, 1, 5)) == approx([0, 0.25, 0.50, 0.75, 1.0])
    assert list(span(0, 1, 3)) == approx([0, 0.5, 1.0])

def test_clamp():
    assert clamp(0, 1, 3) == 1
    assert clamp(1, 1, 3) == 1
    assert clamp(2, 1, 3) == 2
    assert clamp(3, 1, 3) == 3
    assert clamp(4, 1, 3) == 3

