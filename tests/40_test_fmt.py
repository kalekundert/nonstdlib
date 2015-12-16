#!/usr/bin/env python3

from nonstdlib import fmt

def test_fmt():
    name = 'world'
    assert 'hello {name}' | fmt == 'hello world'
    assert '{0} {name}' | fmt('bye') == 'bye world'
    assert '{greeting} {name}' | fmt(greeting='bye', name='mars') == 'bye mars'


