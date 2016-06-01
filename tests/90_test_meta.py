#!/usr/bin/env python3

import pytest
from nonstdlib import *

def test_memoize():
    import time

    @memoize
    def slow_func(i):
        time.sleep(i)
        return i


    start_time = time.time()
    for i in range(100):
        assert slow_func(1) == 1
    assert time.time() - start_time < 2

def test_reset_defaults():
    # 

    @reset_defaults 
    def dont_increment(value, list=[]):
        list.append(value)
        return list


    assert dont_increment(1) == [1]
    assert dont_increment(2) == [2]
    assert dont_increment(3, [1, 2]) == [1, 2, 3]

def test_simple_singleton():
    # This is the simplest possible singleton class, and it should work
    # without issue.

    @singleton
    class Simple:
        pass

    assert Simple() is Simple()

def test_singleton_ctor_args():
    # This should fail, because singleton constructors are not allowed to take
    # any arguments.

    with pytest.raises(TypeError):
        @singleton
        class Broken:
            def __init__(self, arg):
                pass

    with pytest.raises(TypeError):
        @singleton
        class Broken:
            def __init__(self, *args):
                pass

    with pytest.raises(TypeError):
        @singleton
        class Broken:
            def __init__(self, **kwargs):
                pass

