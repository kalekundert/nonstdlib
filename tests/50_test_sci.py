#!/usr/bin/env python3
# encoding: utf-8

from nonstdlib import *

def test_wikipedia_examples():
    assert sci(2, 0) == '2×10⁰'
    assert sci(300, 0) == '3×10²'
    assert sci(4321.768, 6) == '4.321768×10³'
    assert sci(-53000, 1) == '-5.3×10⁴'
    assert sci(6720000000, 2) == '6.72×10⁹'
    assert sci(0.2, 0) == '2×10⁻¹'
    assert sci(0.00000000751, 2) == '7.51×10⁻⁹'

def test_numbers_that_divide_by_ten():
    assert sci(100, 2) == '1.00×10²'
    assert sci(10, 2) == '1.00×10¹'
    assert sci(1, 2) == '1.00×10⁰'
    assert sci(0.1, 2) == '1.00×10⁻¹'
    assert sci(0.01, 2) == '1.00×10⁻²'

    assert sci(-100, 2) == '-1.00×10²'
    assert sci(-10, 2) == '-1.00×10¹'
    assert sci(-1, 2) == '-1.00×10⁰'
    assert sci(-0.1, 2) == '-1.00×10⁻¹'
    assert sci(-0.01, 2) == '-1.00×10⁻²'

def test_numbers_that_round_to_ten():
    assert sci(10004, 2) == '1.00×10⁴'
    assert sci(9995, 2) == '1.00×10⁴'
    assert sci(0.09995, 2) == '1.00×10⁻¹'
    assert sci(0.10004, 2) == '1.00×10⁻¹'

    assert sci(-10004, 2) == '-1.00×10⁴'
    assert sci(-9996, 2) == '-1.00×10⁴'
    assert sci(-0.09996, 2) == '-1.00×10⁻¹'
    assert sci(-0.10004, 2) == '-1.00×10⁻¹'

def test_exponents_with_multiple_digits():
    assert sci(1.23e100, 2) == '1.23×10¹⁰⁰'
    assert sci(1.23e10, 2) == '1.23×10¹⁰'
    assert sci(1.23e1, 2) == '1.23×10¹'
    assert sci(1.23e-1, 2) == '1.23×10⁻¹'
    assert sci(1.23e-10, 2) == '1.23×10⁻¹⁰'
    assert sci(1.23e-100, 2) == '1.23×10⁻¹⁰⁰'

    assert sci(-1.23e100, 2) == '-1.23×10¹⁰⁰'
    assert sci(-1.23e10, 2) == '-1.23×10¹⁰'
    assert sci(-1.23e1, 2) == '-1.23×10¹'
    assert sci(-1.23e-1, 2) == '-1.23×10⁻¹'
    assert sci(-1.23e-10, 2) == '-1.23×10⁻¹⁰'
    assert sci(-1.23e-100, 2) == '-1.23×10⁻¹⁰⁰'

def test_increasing_mantissa_precision():
    assert sci(123456789, 0) == '1×10⁸'
    assert sci(123456789, 1) == '1.2×10⁸'
    assert sci(123456789, 2) == '1.23×10⁸'
    assert sci(123456789, 3) == '1.235×10⁸'
    assert sci(123456789, 4) == '1.2346×10⁸'
    assert sci(123456789, 5) == '1.23457×10⁸'
    assert sci(123456789, 6) == '1.234568×10⁸'
    assert sci(123456789, 7) == '1.2345679×10⁸'
    assert sci(123456789, 8) == '1.23456789×10⁸'
    assert sci(123456789, 9) == '1.234567890×10⁸'

def test_default_mantissa_precision():
    assert sci(123456789) == '1.23×10⁸'

def test_nan_inf_zero():
    assert sci(float('nan')) == 'nan'
    assert sci(-float('nan')) == 'nan'

    assert sci(float('inf')) == 'inf'
    assert sci(-float('inf')) == '-inf'

    assert sci(0, 2) == '0.00'
    assert sci(-0, 2) == '0.00'
