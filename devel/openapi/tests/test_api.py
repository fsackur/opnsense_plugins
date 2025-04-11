#! /usr/bin/env python3

from typing import Dict, Any, Literal
import pytest
from pytest import mark, param

from fixtures import *

StrDict = Dict[str, Any]


_config: Config = config.__wrapped__()
_spec = spec.__wrapped__(_config["source_folder"])
urls = list(_spec._paths.keys())[0:1]


@mark.parametrize("url", urls)
def test_endpoint(url, spec, api):
    method_op = spec._paths[url]
    components = spec.components.schemas

    for method, op in [(k, v) for k, v in method_op.items() if k in ("get", "post")]:
        schema = op["responses"]["200"]["content"]["application/json"]["schema"]
        expected = get_expected_response(schema, components)

        response = api.call(method, url)
        json = response.json()

        assert json == expected



def get_expected_response(schema: StrDict, components: StrDict) -> StrDict:
    # while "$ref" not in expected:
    ref: str = schema["$ref"].replace("#/components/schemas/", "")

    if "/" in ref:
        name, path = ref.split("/", maxsplit=2)[0]
    else:
        name = ref
        path = None

    component = components[name]
    if path:
        breadcrumbs = path.split("/")
        while breadcrumbs:
            prop = breadcrumbs[0]
            if "properties" in component:
                component = component["properties"][prop]
                breadcrumbs = breadcrumbs[1:]
            elif "items" in component:
                component = component["items"]
                # still on the same breadcrumb; go round again
            else:
                raise KeyError(f"could not find {prop} in {component}")

    return component["properties"]
