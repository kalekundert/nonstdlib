#!/usr/bin/env python3

from nonstdlib import *

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
