#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, logging
from nonstdlib.debug import *

class ListHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.records = []

    def __getitem__(self, key):
        return self.records[key]

    def handle(self, record):
        self.records.append(record)



## Configure the logging system for the tests.
handler = ListHandler()
root = logging.getLogger()
root.setLevel(0)
root.addHandler(handler)

## Make sure there aren't any stupid typos in the public interface.

debug("Debug level")
info("Info level")
warning("Warning level")
warn("Warning level")
error("Error level")
critical("Critical error")
fatal("Fatal error")

## Make sure different scopes are properly incorporated into the output.

info("Module level")

def foo():  # (no fold)
    info("Function level")

foo()

class Bar:  # (no fold)
    def __init__(self):
        info("Method level")

Bar()


def test_public_interface():
    assert handler[0].levelno == 10
    assert handler[0].levelname == 'DEBUG'
    assert handler[0].msg == "Debug level"
    
    assert handler[1].levelno == 20
    assert handler[1].levelname == 'INFO'
    assert handler[1].msg == "Info level"
    
    assert handler[2].levelno == 30
    assert handler[2].levelname == 'WARNING'
    assert handler[2].msg == "Warning level"
    
    assert handler[3].levelno == 30
    assert handler[3].levelname == 'WARNING'
    assert handler[3].msg == "Warning level"
    
    assert handler[4].levelno == 40
    assert handler[4].levelname == 'ERROR'
    assert handler[4].msg == "Error level"
    
    assert handler[5].levelno == 50
    assert handler[5].levelname == 'CRITICAL'
    assert handler[5].msg == "Critical error"
    
    assert handler[6].levelno == 50
    assert handler[6].levelname == 'CRITICAL'
    assert handler[6].msg == "Fatal error"
    
def test_logger_names():
    assert handler[7].name == '10_test_debug'
    assert handler[7].msg == "Module level"

    assert handler[8].name == '10_test_debug.foo'
    assert handler[8].msg == "Function level"

    assert handler[9].name == '10_test_debug.Bar'
    assert handler[9].msg == "Method level"

def test_logger_scopes():
    assert handler[7].pathname == __file__
    assert handler[7].lineno == 42
    assert handler[7].funcName == '<module>'
    
    assert handler[8].pathname == __file__
    assert handler[8].lineno == 45
    assert handler[8].funcName == 'foo'
    
    assert handler[9].pathname == __file__
    assert handler[9].lineno == 51
    assert handler[9].funcName == '__init__'
    
def test_log_level():
    assert log_level(1) == 1
    assert log_level("99") == 99
    assert log_level("info") == logging.INFO

def test_verbosity():
    assert verbosity(0) == logging.WARNING
    assert verbosity(1) == logging.INFO
    assert verbosity(2) == logging.DEBUG
    assert verbosity(3) == 0


