#! /usr/bin/env python3

from pytest import fixture

from fixtures import *

def test_spec(spec, spec_validator):
    spec_validator(spec)
