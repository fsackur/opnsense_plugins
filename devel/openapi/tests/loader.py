#! /usr/bin/env python3

import sys
import importlib.util
from pathlib import Path
import yaml
from apispec import APISpec


plugin_base = Path(__file__).parents[1]
script_base = plugin_base.joinpath("src/opnsense/scripts/OPNsense/OpenApi")
scripts = [
    "parse_xml_models.py",
    "parse_endpoints.py",
    "generate_openapi_spec.py",
]

for script in scripts:
    script_file = script_base.joinpath(script)

    name = script_file.stem
    spec = importlib.util.spec_from_file_location(name, script_file)

    if not spec or not spec.loader:
        raise ValueError(f"Script not found at {script_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

generate_openapi_spec = sys.modules["generate_openapi_spec"].generate_openapi_spec


def load_openapi_spec(path: str) -> APISpec:
    # print("////////////////////////////////")
    with open(path) as file:
        content = file.read()
    _spec = yaml.load(content, Loader=yaml.CLoader)
    # print(_spec.keys())
    # print(_spec["paths"]["/auth/priv/get"])

    info = _spec.pop("info")
    version = _spec.pop("openapi")
    paths = _spec.pop("paths")
    components = _spec.pop("components")["schemas"]
    # print(components)

    spec = APISpec(openapi_version=version, **info)

    for path, op in paths.items():
        description = op.pop("description")
        spec.path(path=path, description=description, operations=op)

    for ref, c in components.items():
        spec.components.schema(ref, c)
        # print(c)
        # break
        # spec.path(path=path, description=description, operations=op)

    # print(dir(spec))
    # print(list(spec._paths.keys()))
    # print("////////////////////////////////")
    return spec
