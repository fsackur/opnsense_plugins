#! /usr/bin/env python3

import sys
from typing import Dict, Any, Literal, Hashable, Mapping
import pytest
from pytest import mark, param
from unittest.mock import ANY
# import openapi_schema_validator
from openapi_schema_validator import validate
from referencing import Registry, Resource

from fixtures import *
from urls import urls

StrDict = Dict[str, Any]



# if "--yaml" in sys.argv:
#     _spec = load_spec_from_file.__wrapped__()
# else:
#     _config: Config = config.__wrapped__()
#     _spec = generate_spec.__wrapped__(_config["source_folder"])
# urls = list(_spec._paths.keys())[8:9]

@fixture
def registry(spec: APISpec) -> Registry:
    components = spec.components.schemas

    # priv = components["opnsense.auth.priv"]
    # print(priv)
    # reg = Registry().with_resource(f"opnsense.auth.priv", Resource.from_contents(priv, default_specification=DRAFT202012))

    # parent_schema = {"components": spec.components}
    parent_schema = {"components": {"schemas": spec.components.schemas}}
    # parent_schema = {"schemas": spec.components.schemas}

    schema = Resource(contents=parent_schema, specification=DRAFT202012)
    reg = Registry().with_resource(uri="/components", resource=schema)
    return reg


from pprint import pprint, pformat

@mark.parametrize("url", urls)
def test_endpoint(url, spec, api):
    method_op = spec._paths[url]
    for method, op in [(k, v) for k, v in method_op.items() if k in ("get", "post")]:
        schema = op["responses"]["200"]["content"]["application/json"]["schema"]
        # schema = {"$ref": '#/components/schemas/opnsense.auth.priv'}
        schema = resolve_schema(schema, spec.components.schemas)
        response = api.call(method, url)
        # response.raise_for_status()
        # response_body = {
        #     "priv": {
        #         "users": {
        #             "8f9fbebf-b918-443f-9ea2-4faf264ac1b0": {"value": "freddie", "selected": 0},
        #             "788305db-e7db-4241-9eb6-51631c6aa616": {"value": "root", "selected": 0},
        #         },
        #         "groups": {
        #             "9172be89-d270-48b6-9482-e7925b4a3ce7": {"value": "admins", "selected": 0}
        #         },
        #     }
        # }
        response_body = response.json()
        print(response_body)
        print(schema)
        validate(response_body, schema)


def resolve_schema(schema: StrDict, components: StrDict) -> StrDict:
    _schema = {}
    ref: str | None = schema.get("$ref", None)
    if ref is not None:
        model_name = ref.replace("#/components/schemas/", "").split("/", maxsplit=1)[0]
        _schema = components[model_name]
    for k, v in schema.items():
        if k == "$ref":
            continue
        if isinstance(v, Mapping):
            v = resolve_schema(v, components)
        _schema[k] = v
    return _schema



# def get_expected_response(schema: StrDict, components: StrDict) -> StrDict:
#     schema = deepcopy(schema)
#     # while "$ref" not in expected:
#     ref: str = schema["$ref"].replace("#/components/schemas/", "")
#     print(ref)
#     if "/" in ref:
#         name, path = ref.split("/", maxsplit=1)
#     else:
#         name = ref
#         path = None

#     component = components[name]
#     if path:
#         breadcrumbs = path.split("/")
#         for breadcrumb in breadcrumbs:
#             component = component[breadcrumb]
#         # while breadcrumbs:
#         #     prop = breadcrumbs[0]
#         #     if "properties" in component:
#         #         component = component["properties"][prop]
#         #         breadcrumbs = breadcrumbs[1:]
#         #     elif "items" in component:
#         #         component = component["items"]
#         #         # still on the same breadcrumb; go round again
#         #     else:
#         #         raise KeyError(f"could not find {prop} in {component}")

#     return component["properties"]


# if __name__ == "__main__":
#     pytest.
