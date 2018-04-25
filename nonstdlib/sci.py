#!/usr/bin/env python3
# encoding: utf-8

import math

def sci(x, precision=2, base=10, exp_only=False):
    """
    Convert the given floating point number into scientific notation, using 
    unicode superscript characters to nicely render the exponent.
    """

    # Handle the corner cases of zero and non-finite numbers, which can't be 
    # represented using scientific notation.
    if x == 0 or not math.isfinite(x):
        return '{1:.{0}f}'.format(precision, x)

    exponent = math.floor(math.log(abs(x), base))
    mantissa = x / base**exponent

    # Handle the corner case where the mantissa would round up to 10 (at the 
    # given level of precision) by incrementing the exponent.
    if abs(mantissa) + base**-precision >= base:
        exponent += 1
        mantissa /= base

    superscripts = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    superscript_exponent = str(exponent).translate(superscripts)

    if exp_only:
        return '{0}{1}'.format(base, superscript_exponent)
    else:
        return '{1:.{0}f}×{2}{3}'.format(precision, mantissa, base, superscript_exponent)


