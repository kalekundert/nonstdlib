#!/usr/bin/env python

from nonstdlib import approx

def test_approx():
    assert 5.0 == approx(4.99, 0.02)
    assert not 5.0 == approx(4.97, 0.02)
    assert [1.0, 2.0, 3.0] == approx([0.99, 2.00, 3.01], 0.02)
    assert not [1.0, 2.0, 3.0] == approx([0.99, 2.03, 3.01], 0.01)
