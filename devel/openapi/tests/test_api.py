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
# urls = list(_spec._paths.keys())
# urls = [u for u in urls if not "firmware" in u]

if "--slice" in sys.argv:
    index = sys.argv.index("--slice")
    _slice = sys.argv[index + 1]
    urls = eval(f"urls{_slice}")

if "--url" in sys.argv:
    index = sys.argv.index("--url")
    url = sys.argv[index + 1]
    urls = [u for u in urls if url in u]


import logging
logger = logging.getLogger("api_tests")
handler = logging.FileHandler("pytest.log")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


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
        response_body = response.json()
        print(f"=== {url} ===")
        print(f"response = {response_body}")
        print(f"schema = {schema}")
        try:
            validate(response_body, schema)
            logger.info(f"{url}: pass")
        except Exception as ex:
            logger.error(f"{url}: {ex.__class__.__name__}: {ex.args[0]}")
            raise


def resolve_schema(schema: StrDict, components: StrDict) -> StrDict:
    _schema = schema.copy()
    ref: str | None = _schema.pop("$ref", None)
    if ref is not None:
        model_parts = ref.replace("#/components/schemas/", "")
        if "/" in model_parts:
            model_name, model_path = model_parts.split("/", maxsplit=1)
        else:
            model_name, model_path = model_parts, None

        _schema = components[model_name]
        if model_path:
            breadcrumbs = model_path.split("/")
            for breadcrumb in breadcrumbs:
                _schema = _schema[breadcrumb]

    for k, v in _schema.items():
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
