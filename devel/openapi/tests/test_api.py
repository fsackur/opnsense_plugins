#! /usr/bin/env python3

from fixtures import *

def test_syslog(api):
    url = "/syslog/service/stop"
    response = api.post(url)
    json = response.json()
    assert json == {"response": "STUBBED RESPONSE"}
