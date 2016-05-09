#!/usr/bin/env python

# encoding: utf-8

import pytest
import doctest

from nonstdlib import approx
from operator import eq, ne
from decimal import Decimal
from fractions import Fraction
inf, nan = float('inf'), float('nan')

class MyDocTestRunner(doctest.DocTestRunner):

    def __init__(self):
        doctest.DocTestRunner.__init__(self)

    def report_failure(self, out, test, example, got):
        raise AssertionError("'{}' evaluates to '{}', not '{}'".format(
            example.source.strip(), got.strip(), example.want.strip()))



def test_repr_string():
    # Just make sure the Unicode handling doesn't raise any exceptions.
    print(approx(1.0))
    print(approx([1.0, 2.0, 3.0]))
    print(approx(inf))
    print(approx(1.0, rel=nan))
    print(approx(1.0, rel=inf))

def test_operator_overloading():
    assert 1 == approx(1, rel=1e-6, abs=1e-12)
    assert not (1 != approx(1, rel=1e-6, abs=1e-12))
    assert 10 != approx(1, rel=1e-6, abs=1e-12)
    assert not (10 == approx(1, rel=1e-6, abs=1e-12))

def test_exactly_equal():
    examples = [
            (2.0, 2.0),
            (0.1e200, 0.1e200),
            (1.123e-300, 1.123e-300),
            (12345, 12345.0),
            (0.0, -0.0),
            (345678, 345678),
            (Decimal('1.0001'), Decimal('1.0001')),
            (Fraction(1, 3), Fraction(-1, -3)),
    ]
    for a, x in examples:
        assert a == approx(x)

def test_opposite_sign():
    examples = [
            (eq, 1e-100, -1e-100),
            (ne, 1e100, -1e100),
    ]
    for op, a, x in examples:
        assert op(a, approx(x))

def test_zero_tolerance():
    within_1e10 = [
            (1.1e-100, 1e-100),
            (-1.1e-100, -1e-100),
    ]
    for a, x in within_1e10:
        assert x == approx(x, rel=0.0, abs=0.0)
        assert a != approx(x, rel=0.0, abs=0.0)
        assert a == approx(x, rel=0.0, abs=5e-101)
        assert a != approx(x, rel=0.0, abs=5e-102)
        assert a == approx(x, rel=5e-1, abs=0.0)
        assert a != approx(x, rel=5e-2, abs=0.0)

def test_negative_tolerance():
    # Negative tolerances are not allowed.
    illegal_kwargs = [
            dict(rel=-1e100),
            dict(abs=-1e100),
            dict(rel=1e100, abs=-1e100),
            dict(rel=-1e100, abs=1e100),
            dict(rel=-1e100, abs=-1e100),
    ]
    for kwargs in illegal_kwargs:
        with pytest.raises(ValueError):
            1.1 == approx(1, **kwargs)

def test_inf_tolerance():
    # Everything should be equal if the tolerance is infinite.
    large_diffs = [
            (1, 1000),
            (1e-50, 1e50),
            (-1.0, -1e300),
            (0.0, 10),
    ]
    for a, x in large_diffs:
        assert a != approx(x, rel=0.0, abs=0.0)
        assert a == approx(x, rel=inf, abs=0.0)
        assert a == approx(x, rel=0.0, abs=inf)
        assert a == approx(x, rel=inf, abs=inf)

def test_inf_tolerance_expecting_zero():
    # If the relative tolerance is zero but the expected value is infinite,
    # the actual tolerance is a NaN, which should be an error.
    illegal_kwargs = [
            dict(rel=inf, abs=0.0),
            dict(rel=inf, abs=inf),
    ]
    for kwargs in illegal_kwargs:
        with pytest.raises(ValueError):
            1 == approx(0, **kwargs)

def test_nan_tolerance():
    illegal_kwargs = [
            dict(rel=nan),
            dict(abs=nan),
            dict(rel=nan, abs=nan),
    ]
    for kwargs in illegal_kwargs:
        with pytest.raises(ValueError):
            1.1 == approx(1, **kwargs)

def test_reasonable_defaults():
    # Whatever the defaults are, they should work for numbers close to 1
    # than have a small amount of floating-point error.
    assert 0.1 + 0.2 == approx(0.3)

def test_default_tolerances():
    # This tests the defaults as they are currently set.  If you change the
    # defaults, this test will fail but you should feel free to change it.
    # None of the other tests (except the doctests) should be affected by
    # the choice of defaults.
    examples = [
            # Relative tolerance used.
            (eq, 1e100 + 1e94, 1e100),
            (ne, 1e100 + 2e94, 1e100),
            (eq, 1e0 + 1e-6, 1e0),
            (ne, 1e0 + 2e-6, 1e0),
            # Absolute tolerance used.
            (eq, 1e-100, + 1e-106),
            (eq, 1e-100, + 2e-106),
            (eq, 1e-100, 0),
    ]
    for op, a, x in examples:
        assert op(a, approx(x))

def test_custom_tolerances():
    assert 1e8 + 1e0 == approx(1e8, rel=5e-8, abs=5e0)
    assert 1e8 + 1e0 == approx(1e8, rel=5e-9, abs=5e0)
    assert 1e8 + 1e0 == approx(1e8, rel=5e-8, abs=5e-1)
    assert 1e8 + 1e0 != approx(1e8, rel=5e-9, abs=5e-1)

    assert 1e0 + 1e-8 == approx(1e0, rel=5e-8, abs=5e-8)
    assert 1e0 + 1e-8 == approx(1e0, rel=5e-9, abs=5e-8)
    assert 1e0 + 1e-8 == approx(1e0, rel=5e-8, abs=5e-9)
    assert 1e0 + 1e-8 != approx(1e0, rel=5e-9, abs=5e-9)

    assert 1e-8 + 1e-16 == approx(1e-8, rel=5e-8, abs=5e-16)
    assert 1e-8 + 1e-16 == approx(1e-8, rel=5e-9, abs=5e-16)
    assert 1e-8 + 1e-16 == approx(1e-8, rel=5e-8, abs=5e-17)
    assert 1e-8 + 1e-16 != approx(1e-8, rel=5e-9, abs=5e-17)

def test_relative_tolerance():
    within_1e8_rel = [
            (1e8 + 1e0, 1e8),
            (1e0 + 1e-8, 1e0),
            (1e-8 + 1e-16, 1e-8),
    ]
    for a, x in within_1e8_rel:
        assert a == approx(x, rel=5e-8, abs=0.0)
        assert a != approx(x, rel=5e-9, abs=0.0)

def test_absolute_tolerance():
    within_1e8_abs = [
            (1e8 + 9e-9, 1e8),
            (1e0 + 9e-9, 1e0),
            (1e-8 + 9e-9, 1e-8),
    ]
    for a, x in within_1e8_abs:
        assert a == approx(x, rel=0, abs=5e-8)
        assert a != approx(x, rel=0, abs=5e-9)

def test_expecting_zero():
    examples = [
            (ne, 1e-6, 0.0),
            (ne, -1e-6, 0.0),
            (eq, 1e-12, 0.0),
            (eq, -1e-12, 0.0),
            (ne, 2e-12, 0.0),
            (ne, -2e-12, 0.0),
            (ne, inf, 0.0),
            (ne, nan, 0.0),
     ]
    for op, a, x in examples:
        assert op(a, approx(x, rel=0.0, abs=1e-12))
        assert op(a, approx(x, rel=1e-6, abs=1e-12))

def test_expecting_inf():
    examples = [
            (eq, inf, inf),
            (eq, -inf, -inf),
            (ne, inf, -inf),
            (ne, 0.0, inf),
            (ne, nan, inf),
    ]
    for op, a, x in examples:
        assert op(a, approx(x))

def test_expecting_nan():
    examples = [
            (nan, nan),
            (-nan, -nan),
            (nan, -nan),
            (0.0, nan),
            (inf, nan),
    ]
    for a, x in examples:
        # If there is a relative tolerance and the expected value is NaN,
        # the actual tolerance is a NaN, which should be an error.
        with pytest.raises(ValueError):
            a != approx(x, rel=inf)

        # You can make comparisons against NaN by not specifying a relative
        # tolerance, so only an absolute tolerance is calculated.
        assert a != approx(x, abs=inf)

def test_expecting_sequence():
    within_1e8 = [
            (1e8 + 1e0, 1e8),
            (1e0 + 1e-8, 1e0),
            (1e-8 + 1e-16, 1e-8),
    ]
    actual, expected = zip(*within_1e8)
    assert actual == approx(expected, rel=5e-8, abs=0.0)

def test_expecting_sequence_wrong_len():
    assert [1, 2] != approx([1])
    assert [1, 2] != approx([1,2,3])

def test_complex():
    within_1e6 = [
            ( 1.000001 + 1.0j, 1.0 + 1.0j),
            (1.0 + 1.000001j, 1.0 + 1.0j),
            (-1.000001 + 1.0j, -1.0 + 1.0j),
            (1.0 - 1.000001j, 1.0 - 1.0j),
    ]
    for a, x in within_1e6:
        assert a == approx(x, rel=5e-6, abs=0)
        assert a != approx(x, rel=5e-7, abs=0)

def test_int():
    within_1e6 = [
            (1000001, 1000000),
            (-1000001, -1000000),
    ]
    for a, x in within_1e6:
        assert a == approx(x, rel=5e-6, abs=0)
        assert a != approx(x, rel=5e-7, abs=0)

def test_decimal():
    within_1e6 = [
            (Decimal('1.000001'), Decimal('1.0')),
            (Decimal('-1.000001'), Decimal('-1.0')),
    ]
    for a, x in within_1e6:
        assert a == approx(x, rel=Decimal('5e-6'), abs=0)
        assert a != approx(x, rel=Decimal('5e-7'), abs=0)

def test_fraction():
    within_1e6 = [
            (1 + Fraction(1, 1000000), Fraction(1)),
            (-1 - Fraction(-1, 1000000), Fraction(-1)),
    ]
    for a, x in within_1e6:
        assert a == approx(x, rel=5e-6, abs=0)
        assert a != approx(x, rel=5e-7, abs=0)

def test_doctests():
    parser = doctest.DocTestParser()
    test = parser.get_doctest(
            approx.__doc__,
            {'approx': approx},
            approx.__name__,
            None, None,
    )
    runner = MyDocTestRunner()
    runner.run(test)

