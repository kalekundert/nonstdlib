#!/usr/bin/env python3

from nonstdlib import *

def test_plural():
    assert plural(0, 'apple') == 'apples'
    assert plural(1, 'apple') == 'apple'
    assert plural(2, 'apple') == 'apples'

    assert plural(0, 'tomato', 'tomatoes') == 'tomatoes'
    assert plural(1, 'tomato', 'tomatoes') == 'tomato'
    assert plural(2, 'tomato', 'tomatoes') == 'tomatoes'

def test_oxford_comma():
    assert oxford_comma([]) == ''
    assert oxford_comma([1]) == '1'
    assert oxford_comma([1,2]) == '1 and 2'
    assert oxford_comma([1,2,3]) == '1, 2, and 3'
    assert oxford_comma([1,2,3,4]) == '1, 2, 3, and 4'

    assert oxford_comma([], conj='or') == ''
    assert oxford_comma([1], conj='or') == '1'
    assert oxford_comma([1,2], conj='or') == '1 or 2'
    assert oxford_comma([1,2,3], conj='or') == '1, 2, or 3'
    assert oxford_comma([1,2,3,4], conj='or') == '1, 2, 3, or 4'

def test_pretty_range():
    assert pretty_range([]) == ''
    assert pretty_range([1]) == '1'
    assert pretty_range([1,2]) == '1,2'
    assert pretty_range([2,1]) == '1,2'
    assert pretty_range([1,2,3]) == '1-3'
    assert pretty_range([3,2,1]) == '1-3'
    assert pretty_range([1,3]) == '1,3'
    assert pretty_range([3,1]) == '1,3'
    assert pretty_range([1,2,3,5]) == '1-3,5'
    assert pretty_range([1,2,3,5,6]) == '1-3,5,6'
    assert pretty_range([1,2,3,5,6,7]) == '1-3,5-7'
    assert pretty_range([1,2,3,5,7]) == '1-3,5,7'
    assert pretty_range([1,3,5]) == '1,3,5'
    assert pretty_range([1,3,5,6]) == '1,3,5,6'
    assert pretty_range([1,3,5,6,7]) == '1,3,5-7'
    assert pretty_range([1,3,5,7]) == '1,3,5,7'

def test_indices_from_str():
    assert indices_from_str('') == []
    assert indices_from_str('1') == [1]
    assert indices_from_str('1,2') == [1,2]
    assert indices_from_str('1-3') == [1,2,3]
    assert indices_from_str('1,3') == [1,3]
    assert indices_from_str('1-3,5') == [1,2,3,5]
    assert indices_from_str('1-3,5,6') == [1,2,3,5,6]
    assert indices_from_str('1-3,5-7') == [1,2,3,5,6,7]
    assert indices_from_str('1-3,5,7') == [1,2,3,5,7]
    assert indices_from_str('1,3,5') == [1,3,5]
    assert indices_from_str('1,3,5,6') == [1,3,5,6]
    assert indices_from_str('1,3,5-7') == [1,3,5,6,7]
    assert indices_from_str('1,3,5,7') == [1,3,5,7]
