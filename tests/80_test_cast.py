#!/usr/bin/env python3

import pytest
from nonstdlib import *

def test_minutes():
    assert minutes('1h') == 60
    assert minutes('1h00') == 60
    assert minutes('1h30') == 90
    assert minutes('90m') == 90

    with pytest.raises(ValueError):
        minutes('0')
