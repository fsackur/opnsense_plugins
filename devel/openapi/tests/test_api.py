#! /usr/bin/env python3

from pytest import mark

from fixtures import *


_config: Config = config.__wrapped__()
_spec = spec.__wrapped__(_config["source_folder"])
urls = list(_spec._paths.keys())[0:6]


@mark.parametrize("url", urls)
def test_endpoint(url, spec, api):
    response = api.post(url)
    json = response.json()
    assert json == {"response": "STUBBED RESPONSE"}
