#!/usr/bin/env python
# encoding: utf-8

class approx:

    def __init__(self, expected, plus_or_minus=1e-5):
        self.expected = expected
        self.plus_or_minus = plus_or_minus

    def __repr__(self):
        return '{}±{}'.format(self.expected, self.plus_or_minus)

    def __eq__(self, actual):
        from collections import Iterable
        expected = self.expected
        eps = self.plus_or_minus

        if isinstance(actual, Iterable) and isinstance(expected, Iterable):
            return all(abs(a - x) < eps for a, x in zip(actual, expected))
        else:
            return abs(actual - expected) < eps



