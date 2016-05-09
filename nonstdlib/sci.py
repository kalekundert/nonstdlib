#!/usr/bin/env python3
# encoding: utf-8

import math

def sci(x, precision=2):
    """
    Convert the given floating point number into scientific notation, using 
    unicode superscript characters to nicely render the exponent.
    """

    # Handle the corner cases of zero and non-finite numbers, which can't be 
    # represented using scientific notation.
    if x == 0 or not math.isfinite(x):
        return '{1:.{0}f}'.format(precision, x)

    exponent = math.floor(math.log10(abs(x)))
    mantissa = x / 10**exponent

    # Handle the corner case where the mantissa would round up to 10 (at the 
    # given level of precision) by incrementing the exponent.
    if abs(mantissa) + 10**-precision >= 10:
        exponent += 1
        mantissa /= 10

    superscripts = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    superscript_exponent = str(exponent).translate(superscripts)
    return '{1:.{0}f}×10{2}'.format(precision, mantissa, superscript_exponent)

