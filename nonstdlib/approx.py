#!/usr/bin/env python
# encoding: utf-8

import sys, math

class approx(object):
    """
    Assert that two numbers (or two sets of numbers) are equal to each other
    within some tolerance.

    Due to the `intricacies of floating-point arithmetic`__, numbers that we
    would intuitively expect to be equal are not always so::

        >>> 0.1 + 0.2 == 0.3
        False

    __ https://docs.python.org/3/tutorial/floatingpoint.html

    This problem is commonly encountered when writing tests, e.g. when making
    sure that floating-point values are what you expect them to be.  One way to
    deal with this problem is to assert that two floating-point numbers are
    equal to within some appropriate tolerance::

        >>> abs((0.1 + 0.2) - 0.3) < 1e-6
        True

    However, comparisons like this are tedious to write and difficult to
    understand.  Furthermore, absolute comparisons like the one above are
    usually discouraged because there's no tolerance that works well for all
    situations.  ``1e-6`` is good for numbers around ``1``, but too small for
    very big numbers and too big for very small ones.  It's better to express
    the tolerance as a fraction of the expected value, but relative comparisons
    like that are even more difficult to write correctly and concisely.

    The ``approx`` class performs floating-point comparisons using a syntax
    that's as intuitive as possible::

        >>> from pytest import approx
        >>> 0.1 + 0.2 == approx(0.3)
        True

    The same syntax also works on sequences of numbers::

        >>> (0.1 + 0.2, 0.2 + 0.4) == approx((0.3, 0.6))
        True

    By default, ``approx`` considers numbers within a relative tolerance of
    ``1e-6`` (i.e. one part in a million) of its expected value to be equal.
    This treatment would lead to surprising results if the expected value was
    ``0.0``, because nothing but ``0.0`` itself is relatively close to ``0.0``.
    To handle this case less surprisingly, ``approx`` also considers numbers
    within an absolute tolerance of ``1e-12`` of its expected value to be
    equal.  Infinite numbers are another special case.  They are only
    considered equal to themselves, regardless of the relative tolerance.  Both
    the relative and absolute tolerances can be changed by passing arguments to
    the ``approx`` constructor::

        >>> 1.0001 == approx(1)
        False
        >>> 1.0001 == approx(1, rel=1e-3)
        True
        >>> 1.0001 == approx(1, abs=1e-3)
        True

    If you specify ``abs`` but not ``rel``, the comparison will not consider
    the relative tolerance at all.  In other words, two numbers that are within
    the default relative tolerance of ``1e-6`` will still be considered unequal
    if they exceed the specified absolute tolerance.  If you specify both
    ``abs`` and ``rel``, the numbers will be considered equal if either
    tolerance is met::

        >>> 1 + 1e-8 == approx(1)
        True
        >>> 1 + 1e-8 == approx(1, abs=1e-12)
        False
        >>> 1 + 1e-8 == approx(1, rel=1e-6, abs=1e-12)
        True

    If you're thinking about using ``approx``, then you might want to know how
    it compares to other good ways of comparing floating-point numbers.  All of
    these algorithms are based on relative and absolute tolerances and should
    agree for the most part, but they do have meaningful differences:

    - ``math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)``:  True if the relative
      tolerance is met w.r.t. either ``a`` or ``b`` or if the absolute
      tolerance is met.  Because the relative tolerance is calculated w.r.t.
      both ``a`` and ``b``, this test is symmetric (i.e.  neither ``a`` nor
      ``b`` is a "reference value").  You have to specify an absolute tolerance
      if you want to compare to ``0.0`` because there is no tolerance by
      default.  Only available in python>=3.5.  `More information...`__

      __ https://docs.python.org/3/library/math.html#math.isclose

    - ``numpy.isclose(a, b, rtol=1e-5, atol=1e-8)``: True if the difference
      between ``a`` and ``b`` is less that the sum of the relative tolerance
      w.r.t. ``b`` and the absolute tolerance.  Because the relative tolerance
      is only calculated w.r.t. ``b``, this test is asymmetric and you can
      think of ``b`` as the reference value.  Support for comparing sequences
      is provided by ``numpy.allclose``.  `More information...`__

      __ http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.isclose.html

    - ``unittest.TestCase.assertAlmostEqual(a, b)``: True if ``a`` and ``b``
      are within an absolute tolerance of ``1e-7``.  No relative tolerance is
      considered and the absolute tolerance cannot be changed, so this function
      is not appropriate for very large or very small numbers.  Also, it's only
      available in subclasses of ``unittest.TestCase`` and it's ugly because it
      doesn't follow PEP8.  `More information...`__

      __ https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual

    - ``a == pytest.approx(b, rel=1e-6, abs=1e-12)``: True if the relative
      tolerance is met w.r.t. ``b`` or if the absolute tolerance is met.
      Because the relative tolerance is only calculated w.r.t. ``b``, this test
      is asymmetric and you can think of ``b`` as the reference value.  In the
      special case that you explicitly specify an absolute tolerance but not a
      relative tolerance, only the absolute tolerance is considered.
    """

    def __init__(self, expected, rel=None, abs=None):
        self.expected = expected
        self.abs = abs
        self.rel = rel

    def __repr__(self):
        return ', '.join(repr(x) for x in self.expected)

    def __eq__(self, actual):
        from collections import Iterable
        if not isinstance(actual, Iterable):
            actual = [actual]
        if len(actual) != len(self.expected):
            return False
        return all(a == x for a, x in zip(actual, self.expected))

    def __ne__(self, actual):
        return not (actual == self)

    @property
    def expected(self):
        # Regardless of whether the user-specified expected value is a number
        # or a sequence of numbers, return a list of ApproxNonIterable objects
        # that can be compared against.
        from collections import Iterable
        approx_non_iter = lambda x: ApproxNonIterable(x, self.rel, self.abs)
        if isinstance(self._expected, Iterable):
            return [approx_non_iter(x) for x in self._expected]
        else:
            return [approx_non_iter(self._expected)]

    @expected.setter
    def expected(self, expected):
        self._expected = expected


class ApproxNonIterable(object):
    """
    Perform approximate comparisons for single numbers only.

    In other words, the ``expected`` attribute for objects of this class must
    be some sort of number.  This is in contrast to the ``approx`` class, where
    the ``expected`` attribute can either be a number of a sequence of numbers.
    This class is responsible for making comparisons, while ``approx`` is
    responsible for abstracting the difference between numbers and sequences of
    numbers.  Although this class can stand on its own, it's only meant to be
    used within ``approx``.
    """

    def __init__(self, expected, rel=None, abs=None):
        self.expected = expected
        self.abs = abs
        self.rel = rel

    def __repr__(self):
        # Infinities aren't compared using tolerances, so don't show a
        # tolerance.
        if math.isinf(self.expected):
            return str(self.expected)

        # If a sensible tolerance can't be calculated, self.tolerance will
        # raise a ValueError.  In this case, display '???'.
        try:
            vetted_tolerance = '{:.1e}'.format(self.tolerance)
        except ValueError:
            vetted_tolerance = '???'

        plus_minus = u'{0} \u00b1 {1}'.format(self.expected, vetted_tolerance)

        # In python2, __repr__() must return a string (i.e. not a unicode
        # object).  In python3, __repr__() must return a unicode object
        # (although now strings are unicode objects and bytes are what
        # strings were).
        if sys.version_info[0] == 2:
            return plus_minus.encode('utf-8')
        else:
            return plus_minus

    def __eq__(self, actual):
        # Short-circuit exact equality.
        if actual == self.expected:
            return True

        # Infinity shouldn't be approximately equal to anything but itself, but
        # if there's a relative tolerance, it will be infinite and infinity
        # will seem approximately equal to everything.  The equal-to-itself
        # case would have been short circuited above, so here we can just
        # return false if the expected value is infinite.  The abs() call is
        # for compatibility with complex numbers.
        if math.isinf(abs(self.expected)):
            return False

        # Return true if the two numbers are within the tolerance.
        return abs(self.expected - actual) <= self.tolerance

    def __ne__(self, actual):
        return not (actual == self)

    @property
    def tolerance(self):
        set_default = lambda x, default: x if x is not None else default

        # Figure out what the absolute tolerance should be.  ``self.abs`` is
        # either None or a value specified by the user.
        absolute_tolerance = set_default(self.abs, 1e-12)

        if absolute_tolerance < 0:
            raise ValueError("absolute tolerance can't be negative: {}".format(absolute_tolerance))
        if math.isnan(absolute_tolerance):
            raise ValueError("absolute tolerance can't be NaN.")

        # If the user specified an absolute tolerance but not a relative one,
        # just return the absolute tolerance.
        if self.rel is None:
            if self.abs is not None:
                return absolute_tolerance

        # Figure out what the relative tolerance should be.  ``self.rel`` is
        # either None or a value specified by the user.  This is done after
        # we've made sure the user didn't ask for an absolute tolerance only,
        # because we don't want to raise errors about the relative tolerance if
        # we aren't even going to use it.
        relative_tolerance = set_default(self.rel, 1e-6) * abs(self.expected)

        if relative_tolerance < 0:
            raise ValueError("relative tolerance can't be negative: {}".format(absolute_tolerance))
        if math.isnan(relative_tolerance):
            raise ValueError("relative tolerance can't be NaN.")

        # Return the larger of the relative and absolute tolerances.
        return max(relative_tolerance, absolute_tolerance)


